#!/usr/bin/env python3
"""
Bdev.ai + AgentMail Advanced Integration
Supports multiple AgentMail accounts with load balancing
"""

import os
import sys
import json
import pandas as pd
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import hashlib

class AgentMailManager:
    """Manage multiple AgentMail accounts with load balancing"""
    
    def __init__(self, config_path: str = None):
        # Load configuration
        if config_path is None:
            config_path = "/Users/cubiczan/.openclaw/workspace/agentmail_config.json"
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Initialize account tracking
        self.accounts = self.config['agentmail_accounts']
        self.account_usage = {}
        self.account_rotation_index = 0
        
        for account in self.accounts:
            if account['enabled']:
                self.account_usage[account['name']] = {
                    'today_count': 0,
                    'today_date': datetime.now().date(),
                    'total_sent': 0,
                    'last_used': None,
                    'errors': 0
                }
        
        print(f"🔧 AgentMail Manager initialized")
        print(f"   Accounts: {len([a for a in self.accounts if a['enabled']])} enabled")
        print(f"   Strategy: {self.config['rotation_strategy']}")
        print(f"   Daily limit: {self.config['daily_total_limit']}")
    
    def get_next_account(self, strategy: str = None) -> Optional[Dict]:
        """Get next available AgentMail account based on strategy"""
        if strategy is None:
            strategy = self.config['rotation_strategy']
        
        enabled_accounts = [a for a in self.accounts if a['enabled']]
        if not enabled_accounts:
            print("❌ No enabled AgentMail accounts")
            return None
        
        # Reset daily counts if new day
        today = datetime.now().date()
        for account_name, usage in self.account_usage.items():
            if usage['today_date'] != today:
                usage['today_count'] = 0
                usage['today_date'] = today
        
        # Filter accounts under daily limit
        available_accounts = []
        for account in enabled_accounts:
            usage = self.account_usage.get(account['name'], {})
            if usage.get('today_count', 0) < account.get('daily_limit', 1000):
                available_accounts.append(account)
        
        if not available_accounts:
            print("⚠️ All accounts at daily limit")
            return None
        
        # Select account based on strategy
        if strategy == "round_robin":
            account = available_accounts[self.account_rotation_index % len(available_accounts)]
            self.account_rotation_index += 1
            return account
        
        elif strategy == "random":
            return random.choice(available_accounts)
        
        elif strategy == "least_used":
            # Select account with least usage today
            least_used = min(available_accounts, 
                           key=lambda a: self.account_usage.get(a['name'], {}).get('today_count', 0))
            return least_used
        
        elif strategy == "priority":
            # Select by priority (lower number = higher priority)
            available_accounts.sort(key=lambda a: a.get('priority', 999))
            return available_accounts[0]
        
        else:
            # Default to round robin
            account = available_accounts[self.account_rotation_index % len(available_accounts)]
            self.account_rotation_index += 1
            return account
    
    def update_account_usage(self, account_name: str, success: bool = True):
        """Update usage statistics for an account"""
        if account_name not in self.account_usage:
            self.account_usage[account_name] = {
                'today_count': 0,
                'today_date': datetime.now().date(),
                'total_sent': 0,
                'last_used': datetime.now(),
                'errors': 0
            }
        
        usage = self.account_usage[account_name]
        
        if success:
            usage['today_count'] += 1
            usage['total_sent'] += 1
            usage['last_used'] = datetime.now()
        else:
            usage['errors'] += 1
    
    def get_usage_stats(self) -> Dict:
        """Get current usage statistics"""
        stats = {
            'total_accounts': len(self.accounts),
            'enabled_accounts': len([a for a in self.accounts if a['enabled']]),
            'today_total': sum(usage.get('today_count', 0) for usage in self.account_usage.values()),
            'total_sent': sum(usage.get('total_sent', 0) for usage in self.account_usage.values()),
            'accounts': {}
        }
        
        for account in self.accounts:
            if account['enabled']:
                usage = self.account_usage.get(account['name'], {})
                stats['accounts'][account['name']] = {
                    'today': usage.get('today_count', 0),
                    'total': usage.get('total_sent', 0),
                    'last_used': usage.get('last_used'),
                    'errors': usage.get('errors', 0),
                    'limit': account.get('daily_limit', 1000),
                    'remaining': account.get('daily_limit', 1000) - usage.get('today_count', 0)
                }
        
        return stats
    
    def send_email(self, recipient_data: Dict, email_content: Dict) -> bool:
        """Send email using selected AgentMail account"""
        
        # Get next available account
        account = self.get_next_account()
        if not account:
            print(f"❌ No available AgentMail accounts for {recipient_data.get('name', 'recipient')}")
            return False
        
        print(f"📧 Using account: {account['name']} ({account['from_email']})")
        print(f"   To: {recipient_data.get('email')}")
        print(f"   Name: {recipient_data.get('name', 'Investor')}")
        
        # Prepare payload for AgentMail API
        payload = {
            "campaign": {
                "name": f"Bdev.ai Outreach - {datetime.now().strftime('%Y-%m-%d')}",
                "subject": email_content.get('subject', f"Potential Synergy: {recipient_data.get('company', 'Opportunity')}"),
                "from_name": account['from_name'],
                "from_email": account['from_email'],
                "reply_to": self.config.get('default_reply_to', account['from_email'])
            },
            "recipient": {
                "email": recipient_data['email'],
                "name": recipient_data.get('name', 'Investor'),
                "company": recipient_data.get('company', ''),
                "custom_fields": {
                    "sectors": recipient_data.get('sectors', ''),
                    "source": "Bdev.ai AI Personalization",
                    "campaign_id": f"bdev_{datetime.now().strftime('%Y%m%d')}",
                    "account_used": account['name']
                }
            },
            "content": {
                "html": self.format_html_email(email_content['body'], account),
                "text": email_content['body']
            },
            "tracking": {
                "opens": self.config.get('tracking_enabled', True),
                "clicks": self.config.get('tracking_enabled', True),
                "unsubscribes": True
            },
            "metadata": {
                "bdev_ai_batch": datetime.now().strftime('%Y%m%d_%H%M%S'),
                "investor_id": hashlib.md5(recipient_data['email'].encode()).hexdigest()[:8],
                "ai_model": "DeepSeek-128K"
            }
        }
        
        # Simulate sending (replace with actual AgentMail API call)
        success = self.simulate_send(account, payload)
        
        # Update usage statistics
        self.update_account_usage(account['name'], success)
        
        if success:
            print(f"   ✅ Sent via {account['name']}")
            return True
        else:
            print(f"   ❌ Failed via {account['name']}")
            return False
    
    def simulate_send(self, account: Dict, payload: Dict) -> bool:
        """Simulate sending email (replace with actual API call)"""
        # Simulate API call delay
        import time
        time.sleep(0.05)
        
        # Simulate occasional failure (5% chance)
        if random.random() < 0.05:
            print(f"   ⚠️ Simulated API failure")
            return False
        
        # In production, this would be:
        # api_url = "https://api.agentmail.com/v1/campaigns/send"
        # headers = {"Authorization": f"Bearer {account['api_key']}", "Content-Type": "application/json"}
        # response = requests.post(api_url, headers=headers, json=payload)
        # return response.status_code == 200
        
        return True
    
    def format_html_email(self, body: str, account: Dict) -> str:
        """Format plain text as HTML email"""
        html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Powered Investment Insights</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6; 
            color: #333; 
            max-width: 600px; 
            margin: 0 auto; 
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .container {{
            background: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .message {{
            white-space: pre-line;
            margin: 20px 0;
            font-size: 16px;
        }}
        .signature {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }}
        .footer {{
            font-size: 12px;
            color: #666;
            margin-top: 30px;
            text-align: center;
        }}
        .unsubscribe {{
            color: #999;
            font-size: 11px;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="message">
{body}
        </div>
        
        <div class="signature">
            <strong>Best regards,</strong><br>
            {account['from_name']}<br>
            {account['from_email']}
        </div>
        
        <div class="footer">
            This email was sent by an AI-powered outreach system.<br>
            Message generated and personalized by Bdev.ai + OpenClaw AI.
        </div>
        
        <div class="unsubscribe">
            To unsubscribe from future communications, reply with "UNSUBSCRIBE" in the subject line.
        </div>
    </div>
</body>
</html>"""
        return html_template

class BdevAIAgentMailAdvanced:
    """Advanced Bdev.ai + AgentMail integration with multiple accounts"""
    
    def __init__(self):
        self.agentmail_manager = AgentMailManager()
        print("🔧 Bdev.ai + AgentMail Advanced Integration")
    
    def load_bdev_ai_output(self, csv_path: str = None) -> pd.DataFrame:
        """Load latest Bdev.ai output"""
        import glob
        
        if csv_path and os.path.exists(csv_path):
            return pd.read_csv(csv_path)
        
        # Find latest file
        bdev_files = glob.glob("/Users/cubiczan/.openclaw/workspace/bdev_ai_openclaw_*.csv")
        if not bdev_files:
            print("❌ No Bdev.ai output files found")
            return pd.DataFrame()
        
        latest_file = max(bdev_files, key=os.path.getctime)
        print(f"📂 Loading: {latest_file}")
        
        try:
            df = pd.read_csv(latest_file)
            # Clean email column
            if 'email' in df.columns:
                df['email'] = df['email'].astype(str).replace('nan', '')
            return df
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            return pd.DataFrame()
    
    def process_batch(self, csv_path: str = None, limit: int = 50) -> Dict:
        """Process batch of Bdev.ai output"""
        print(f"\n🔨 Processing Bdev.ai output (limit: {limit})...")
        
        df = self.load_bdev_ai_output(csv_path)
        if df.empty:
            print("❌ No data to process")
            return {'total': 0, 'sent': 0, 'failed': 0, 'skipped': 0}
        
        print(f"📊 Found {len(df)} AI-generated messages")
        
        # Show usage stats before processing
        stats_before = self.agentmail_manager.get_usage_stats()
        print(f"📈 Starting stats: {stats_before['today_total']} sent today")
        
        # Process messages
        results = {'total': 0, 'sent': 0, 'failed': 0, 'skipped': 0}
        sent_messages = []
        
        for idx, row in df.head(limit).iterrows():
            try:
                results['total'] += 1
                
                # Extract data
                email = str(row.get('email', '')).strip()
                if not email or '@' not in email or email.lower() == 'nan':
                    print(f"   {idx+1}. Skipped - invalid email")
                    results['skipped'] += 1
                    continue
                
                recipient_data = {
                    'email': email,
                    'name': str(row.get('contact_name', 'Investor')).strip(),
                    'company': str(row.get('company', '')).strip(),
                    'sectors': str(row.get('sectors', '')).strip()
                }
                
                email_content = {
                    'subject': f"AI-Powered Insights: {recipient_data['company']}",
                    'body': str(row.get('personalized_message', '')).strip()
                }
                
                print(f"   {idx+1}. {recipient_data['name']} - {recipient_data['company']}")
                
                # Send email
                success = self.agentmail_manager.send_email(recipient_data, email_content)
                
                if success:
                    results['sent'] += 1
                    sent_messages.append({
                        'recipient': recipient_data,
                        'timestamp': datetime.now().isoformat(),
                        'message_preview': email_content['body'][:100] + '...'
                    })
                else:
                    results['failed'] += 1
                
            except Exception as e:
                print(f"   {idx+1}. Error: {e}")
                results['failed'] += 1
                continue
        
        # Show usage stats after processing
        stats_after = self.agentmail_manager.get_usage_stats()
        
        print(f"\n📊 Processing complete:")
        print(f"   Total: {results['total']}")
        print(f"   Sent: {results['sent']} ✅")
        print(f"   Failed: {results['failed']} ❌")
        print(f"   Skipped: {results['skipped']} ⚠️")
        
        print(f"\n📈 Usage stats:")
        print(f"   Today total: {stats_after['today_total']} emails")
        for account_name, account_stats in stats_after['accounts'].items():
            print(f"   {account_name}: {account_stats['today']}/{account_stats['limit']} ({(account_stats['today']/account_stats['limit']*100):.1f}%)")
        
        # Save results
        self.save_results(results, sent_messages, stats_after)
        
        return results
    
    def save_results(self, results: Dict, sent_messages: List, stats: Dict):
        """Save processing results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed log
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'results': results,
            'stats': stats,
            'sent_messages': sent_messages[:10]  # Save first 10 for reference
        }
        
        log_file = f"/Users/cubiczan/.openclaw/workspace/bdev_ai_agentmail_log_{timestamp}.json"
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        # Update summary log
        summary_file = "/Users/cubiczan/.openclaw/workspace/bdev_ai_agentmail_summary.json"
        summary = []
        
        if os.path.exists(summary_file):
            with open(summary_file, 'r') as f:
                summary = json.load(f)
        
        summary.append({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'results': results,
            'total_today': stats['today_total']
        })
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n💾 Logs saved:")
        print(f"   Detailed: {log_file}")
        print(f"   Summary: {summary_file}")
    
    def create_advanced_pipeline_script(self):
        """Create advanced pipeline script"""
        
        script = '''#!/bin/bash
# bdev_ai_advanced_pipeline.sh
# Advanced Bdev.ai → AgentMail pipeline with multiple accounts

cd /Users/cubiczan/.openclaw/workspace

LOG_DIR="logs/bdev_ai_advanced"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/pipeline_$TIMESTAMP.log"

echo "================================================" | tee -a "$LOG_FILE"
echo "Bdev.ai Advanced Pipeline" | tee -a "$LOG_FILE"
echo "Started: $(date)" | tee -a "$LOG_FILE"
echo "================================================" | tee -a "$LOG_FILE"

# Step 1: Check AgentMail accounts
echo "🔍 Step 1: Checking AgentMail accounts..." | tee -a "$LOG_FILE"
python3 -c "
import json
try:
    with open('agentmail_config.json', 'r') as f:
        config = json.load(f)
    enabled = [a for a in config['agentmail_accounts'] if a['enabled']]
    print(f'   Accounts configured: {len(config[\"agentmail_accounts\"])}')
    print(f'   Accounts enabled: {len(enabled)}')
    for acc in enabled:
        print(f'   • {acc[\"name\"]}: {acc[\"from_email\"]}')
except Exception as e:
    print(f'   ❌ Error: {e}')
" 2>&1 | tee -a "$LOG_FILE"

# Step 2: Generate AI messages
echo "🤖 Step 2: Bdev.ai AI Message Generation" | tee -a "$LOG_FILE"
python3 bdev_ai_openclaw_integration_final.py --batch-size 50 2>&1 | tee -a "$LOG_FILE"

# Step 3: Send via AgentMail (advanced)
echo "📧 Step 3: Advanced AgentMail Integration" | tee -a "$LOG_FILE"
python3 bdev_ai_agentmail_advanced.py --limit 50 2>&1 | tee -a "$LOG_FILE"

# Step 4: Create summary
echo "📊 Step 4: Pipeline Summary" | tee -a "$LOG_FILE"

# Count AI messages
AI_OUTPUT=$(ls -t bdev_ai_openclaw_*.csv 2>/dev/null | head -1)
if [ -n "$AI_OUTPUT" ]; then
    MSG_COUNT=$(wc -l < "$AI_OUTPUT" | awk '{print $1-1}')
    echo "AI Messages Generated: $MSG_COUNT" | tee -a "$LOG_FILE"
fi

# Check AgentMail logs
if [ -f "bdev_ai_agentmail_summary.json" ]; then
    LATEST_LOG=$(tail -1 bdev_ai_agentmail_summary.json | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    sent = data['results']['sent']
    total = data['results']['total']
    print(f'AgentMail Results: {sent}/{total} sent ({sent/total*100:.1f}%)')
except:
    print('AgentMail Results: Check log')
" 2>/dev/null)
    echo "$LATEST_LOG" | tee -a "$LOG_FILE"
fi

# Show account usage
echo "👥 Account Usage:" | tee -a "$LOG_FILE"
python3 -c "
import json
try:
    with open('agentmail_config.json', 'r') as f:
        config = json.load(f)
    
    # Check for usage logs
    import glob
    log_files = glob.glob('bdev_ai_agentmail_log_*.json')
    if log_files:
        latest_log = max(log_files, key=lambda x: x.split('_')[-1].split('.')[0])
        with open(latest_log, 'r') as f:
            log_data = json.load(f)
        
        stats = log_data.get('stats', {})
        if 'accounts' in stats:
            for acc_name, acc_stats in stats['accounts'].items():
                today = acc_stats.get('today', 0)
                limit = acc_stats.get('limit', 1000)
                pct = (today/limit*100) if limit > 0 else 0
                print(f'   {acc_name}: {today}/{limit} ({pct:.1f}%)')
    else:
        print('   No usage data yet')
except Exception as e:
    print(f'   Error: {e}')
" 2>&1 | tee -a "$LOG_FILE"

echo "================================================" | tee -a "$LOG_FILE"
echo "Advanced pipeline completed!" | tee -a "$LOG_FILE"
echo "================================================" | tee -a "$LOG_FILE"
'''
        
        script_path = "/Users/cubiczan/.openclaw/workspace/bdev_ai_advanced_pipeline.sh"
        with open(script_path, 'w') as f:
            f.write(script)
        
        os.chmod(script_path, 0o755)
        
        print(f"\n📋 Advanced pipeline script created: {script_path}")
        return script_path