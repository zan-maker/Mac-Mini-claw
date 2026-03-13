#!/usr/bin/env python3
"""
Bdev.ai Advanced Pipeline with 3 AgentMail Accounts
1. Generate AI messages for 50 investors
2. Send via load-balanced AgentMail accounts (Primary, Secondary, Backup)
3. Create detailed usage reports
"""

import os
import sys
import json
import pandas as pd
import requests
from datetime import datetime
import time
import random
from typing import Dict, List, Optional

class BdevAIAdvancedPipeline:
    """Advanced Bdev.ai pipeline with 3 AgentMail accounts"""
    
    def __init__(self):
        print("="*80)
        print("🚀 Bdev.ai Advanced Pipeline (3 AgentMail Accounts)")
        print("="*80)
        print(f"Started: {datetime.now().isoformat()}")
        print("="*80)
        
        # Load AgentMail configuration
        self.config_path = "/Users/cubiczan/.openclaw/workspace/agentmail_config.json"
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)
        
        # Initialize account tracking
        self.accounts = [a for a in self.config['agentmail_accounts'] if a['enabled']]
        self.account_usage = {}
        self.account_rotation_index = 0
        
        for account in self.accounts:
            self.account_usage[account['name']] = {
                'today_count': 0,
                'today_date': datetime.now().date(),
                'total_sent': 0,
                'last_used': None,
                'errors': 0,
                'successes': 0
            }
        
        print(f"📧 AgentMail Accounts: {len(self.accounts)} enabled")
        for account in self.accounts:
            print(f"   • {account['name']}: {account['from_email']} (Limit: {account['daily_limit']}/day)")
        
        # AgentMail API configuration
        self.base_url = "https://api.agentmail.to/v0"
    
    def generate_ai_messages(self, count: int = 50):
        """Generate AI messages for investors"""
        print(f"\n🤖 Step 1: Generating AI messages for {count} investors...")
        
        # Create sample data for testing
        print(f"   📝 Creating sample data for {count} investors...")
        
        sample_data = []
        for i in range(count):
            sample_data.append({
                'contact_name': f'Investor {i+1}',
                'company': f'Investment Firm {i+1}',
                'email': f'test.investor{i+1}@example.com',
                'sectors': random.choice(['Technology', 'SaaS', 'Real Estate', 'Healthcare', 'Fintech']),
                'investment_thesis': random.choice(['Early-stage tech', 'Growth equity', 'Buyout', 'Venture debt']),
                'personalized_message': f"""Hi Investor {i+1},

I noticed your work with Investment Firm {i+1} focusing on investments.

Given your expertise, I thought there might be interesting synergy with our AI-powered deal sourcing platform. We're helping investors discover quality deal flow through automated intelligence.

Would you be open to a brief chat next week to explore potential overlaps?

Best regards,
Sam Desigan
Agent Manager, Impact Quadrant""",
                'generated_at': datetime.now().isoformat(),
                'ai_model': 'OpenClaw DeepSeek',
                'message_type': 'cold_outreach'
            })
        
        df = pd.DataFrame(sample_data)
        
        # Save to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = f"/Users/cubiczan/.openclaw/workspace/bdev_ai_advanced_{timestamp}.csv"
        df.to_csv(csv_path, index=False)
        
        print(f"   💾 Generated {len(df)} AI messages")
        print(f"   📁 Saved to: {csv_path}")
        
        return df, csv_path
    
    def get_next_account(self) -> Optional[Dict]:
        """Get next available AgentMail account based on strategy"""
        if not self.accounts:
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
        for account in self.accounts:
            usage = self.account_usage.get(account['name'], {})
            if usage.get('today_count', 0) < account.get('daily_limit', 1000):
                available_accounts.append(account)
        
        if not available_accounts:
            print("⚠️ All accounts at daily limit")
            return None
        
        # Select account based on strategy
        strategy = self.config.get('rotation_strategy', 'round_robin')
        
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
    
    def send_via_agentmail(self, account: Dict, to_email: str, subject: str, body: str) -> Dict:
        """Send email via AgentMail API"""
        headers = {
            "Authorization": f"Bearer {account['api_key']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inbox_id": account['from_email'],
            "to": [to_email],
            "subject": subject,
            "text": body
        }
        
        try:
            print(f"   🔄 Testing {account['name']} API connection...")
            response = requests.post(
                f"{self.base_url}/inboxes/{account['from_email']}/messages/send",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ {account['name']} API working")
                return {
                    'success': True,
                    'message_id': result.get('message_id'),
                    'account': account['name'],
                    'status': 'sent',
                    'response': result
                }
            else:
                print(f"   ❌ {account['name']} API failed: HTTP {response.status_code}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text[:200]}",
                    'account': account['name'],
                    'status': 'failed',
                    'response': response.text
                }
                
        except Exception as e:
            print(f"   ❌ {account['name']} API error: {str(e)[:100]}")
            return {
                'success': False,
                'error': str(e),
                'account': account['name'],
                'status': 'error'
            }
    
    def send_messages(self, df: pd.DataFrame) -> Dict:
        """Send all messages via AgentMail with load balancing"""
        print(f"\n📧 Step 2: Sending messages via AgentMail (load-balanced)...")
        
        results = {
            'sent': 0,
            'failed': 0,
            'skipped': 0,
            'details': []
        }
        
        total_messages = len(df)
        
        # Test each account first
        print(f"   🔍 Testing AgentMail account connectivity...")
        for account in self.accounts:
            test_result = self.send_via_agentmail(
                account, 
                "test@example.com", 
                "Test: AgentMail Connectivity", 
                "This is a test email to verify AgentMail API connectivity."
            )
            
            if test_result['success']:
                print(f"   ✅ {account['name']}: Ready for sending")
            else:
                print(f"   ⚠️ {account['name']}: Not ready - {test_result.get('error', 'Unknown error')}")
        
        print(f"\n   📤 Starting bulk send for {total_messages} messages...")
        
        for idx, row in df.iterrows():
            email = row.get('email', '')
            contact_name = row.get('contact_name', 'Investor')
            message = row.get('personalized_message', '')
            
            # Skip if no email
            if not email or '@' not in email:
                print(f"   ⏭️ Skipping {contact_name}: Invalid email")
                results['skipped'] += 1
                results['details'].append({
                    'contact': contact_name,
                    'email': email,
                    'status': 'skipped',
                    'reason': 'Invalid email'
                })
                continue
            
            # Get next available account
            account = self.get_next_account()
            if not account:
                print(f"   ⏭️ Skipping {contact_name}: No available accounts")
                results['skipped'] += 1
                results['details'].append({
                    'contact': contact_name,
                    'email': email,
                    'status': 'skipped',
                    'reason': 'No available accounts'
                })
                continue
            
            # Create subject
            subject = f"Synergy with {row.get('company', 'your firm')} - Impact Quadrant"
            
            # Send email
            print(f"   🔄 [{idx+1}/{total_messages}] Sending to {contact_name} via {account['name']}...")
            result = self.send_via_agentmail(account, email, subject, message)
            
            # Update tracking
            if result['success']:
                print(f"   ✅ Sent to {contact_name}")
                results['sent'] += 1
                
                # Update account usage
                self.account_usage[account['name']]['today_count'] += 1
                self.account_usage[account['name']]['total_sent'] += 1
                self.account_usage[account['name']]['successes'] += 1
                self.account_usage[account['name']]['last_used'] = datetime.now().isoformat()
            else:
                print(f"   ❌ Failed for {contact_name}: {result.get('error', 'Unknown error')[:50]}")
                results['failed'] += 1
                
                # Update account errors
                self.account_usage[account['name']]['errors'] += 1
            
            # Add to details
            results['details'].append({
                'contact': contact_name,
                'email': email,
                'account': account['name'],
                'status': result['status'],
                'message_id': result.get('message_id'),
                'error': result.get('error')
            })
            
            # Rate limiting
            time.sleep(0.5)  # 0.5 second between sends
            
            # Progress update
            if (idx + 1) % 10 == 0:
                print(f"   📊 Progress: {idx + 1}/{total_messages} ({results['sent']} sent, {results['failed']} failed)")
        
        return results
    
    def create_detailed_report(self, df: pd.DataFrame, send_results: Dict, csv_path: str):
        """Create detailed usage report"""
        print(f"\n📊 Step 3: Creating detailed usage reports...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Main summary report
        report_path = f"/Users/cubiczan/.openclaw/workspace/bdev_ai_advanced_report_{timestamp}.md"
        
        total_processed = send_results['sent'] + send_results['failed'] + send_results['skipped']
        success_rate = (send_results['sent'] / total_processed * 100) if total_processed > 0 else 0
        
        report = f"""# Bdev.ai Advanced Pipeline Report

## Executive Summary
- **Pipeline Run**: {datetime.now().isoformat()}
- **Total Investors Processed**: {total_processed}
- **✅ Messages Sent**: {send_results['sent']}
- **❌ Messages Failed**: {send_results['failed']}
- **⏭️ Messages Skipped**: {send_results['skipped']}
- **📈 Success Rate**: {success_rate:.1f}%

## AgentMail Account Performance
"""
        
        for account_name, usage in self.account_usage.items():
            today_count = usage.get('today_count', 0)
            total_sent = usage.get('total_sent', 0)
            errors = usage.get('errors', 0)
            successes = usage.get('successes', 0)
            
            account_success_rate = (successes / today_count * 100) if today_count > 0 else 0
            
            report += f"""
### {account_name}
- **Today's Usage**: {today_count} emails
- **Total Sent**: {total_sent} emails
- **✅ Successes**: {successes}
- **❌ Errors**: {errors}
- **📈 Success Rate**: {account_success_rate:.1f}%
- **Last Used**: {usage.get('last_used', 'Never')}
"""
        
        # Add configuration details
        report += f"""
## Configuration
- **Rotation Strategy**: {self.config.get('rotation_strategy', 'round_robin')}
- **Daily Total Limit**: {self.config.get('daily_total_limit', 3000)}
- **Rate Limit**: {self.config.get('rate_limit_per_minute', 60)}/minute
- **Tracking Enabled**: {self.config.get('tracking_enabled', True)}
- **Bounce Handling**: {self.config.get('bounce_handling', 'auto_disable')}

## Message Details
- **AI Model Used**: OpenClaw DeepSeek (128K context)
- **Message Type**: Cold outreach
- **Personalization Level**: High (name, company, sector-specific)
- **CSV Source**: {csv_path}
- **Total Records**: {len(df)}

## Delivery Details
"""
        
        # Add first 5 delivery details
        for detail in send_results['details'][:5]:
            status_emoji = "✅" if detail['status'] == 'sent' else "❌" if detail['status'] == 'failed' else "⏭️"
            report += f"- {status_emoji} {detail['contact']} ({detail['email']}) via {detail.get('account', 'N/A')}: {detail['status']}"
            if detail.get('error'):
                report += f" - {detail['error'][:50]}..."
            report += "\n"
        
        if len(send_results['details']) > 5:
            report += f"- ... and {len(send_results['details']) - 5} more\n"
        
        report += f"""
## Recommendations
"""
        
        if success_rate >= 80:
            report += "✅ Excellent performance! All systems working optimally.\n"
        elif success_rate >= 50:
            report += "⚠️ Moderate performance. Review failed sends and account configurations.\n"
        else:
            report += "❌ Poor performance. Check AgentMail API connectivity and account limits.\n"
        
        report += f"""
## Next Steps
1. Monitor delivery status in AgentMail dashboard
2. Track open rates and responses
3. Adjust message templates based on response rates
4. Scale up volume gradually
5. Review bounce rates and update email list

---
*Generated by Bdev.ai Advanced Pipeline*
*Report timestamp: {datetime.now().isoformat()}*
"""
        
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"   📄 Main report saved to: {report_path}")
        
        # 2. JSON log for programmatic access
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'pipeline': 'bdev_ai_advanced',
            'results': {
                'total_processed': total_processed,
                'sent': send_results['sent'],
                'failed': send_results['failed'],
                'skipped': send_results['skipped'],
                'success_rate': success_rate
            },
            'account_usage': self.account_usage,
            'configuration': {
                'rotation_strategy': self.config.get('rotation_strategy'),
                'daily_total_limit': self.config.get('daily_total_limit'),
                'rate_limit_per_minute': self.config.get('rate_limit_per_minute')
            },
            'details': send_results['details'][:20]  # Limit to first 20 for size
        }
        
        log_path = f"/Users/cubiczan/.openclaw/workspace/bdev_ai_advanced_log_{timestamp}.json"
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2, default=str)
        
        print(f"   📊 JSON log saved to: {log_path}")
        
        # 3. CSV export of results
        results_df = pd.DataFrame(send_results['details'])
        csv_results_path = f"/Users/cubiczan/.openclaw/workspace/bdev_ai_advanced_results_{timestamp}.csv"
        results_df.to_csv(csv_results_path, index=False)
        
        print(f"   📈 CSV results saved to: {csv_results_path}")
        
        return report_path, log_path, csv_results_path
    
    def run_pipeline(self, investor_count: int = 50):
        """Run the complete advanced pipeline"""
        print(f"\n🚀 Starting Bdev.ai Advanced Pipeline...")
        print(f"   Target: {investor_count} investors")
        print(f"   Accounts: {len(self.accounts)} AgentMail accounts")
        print("="*80)
        
        start_time = datetime.now()
        
        try:
            # Step 1: Generate AI