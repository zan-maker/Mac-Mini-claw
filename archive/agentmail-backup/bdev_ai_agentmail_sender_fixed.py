#!/usr/bin/env python3
"""
Bdev.ai → AgentMail Integration - FIXED VERSION
Actually sends emails using AgentMail API with 3-account load balancing
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
import glob

class AgentMailSender:
    """Send Bdev.ai generated messages via AgentMail with load balancing"""
    
    def __init__(self, config_path: str = None):
        # Load configuration
        if config_path is None:
            config_path = "/Users/cubiczan/.openclaw/workspace/agentmail_config.json"
        
        with open(config_path, 'r') as f:
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
                'errors': 0
            }
        
        print(f"🔧 AgentMail Sender initialized")
        print(f"   Accounts: {len(self.accounts)} enabled")
        print(f"   Strategy: {self.config['rotation_strategy']}")
        print(f"   Daily limit: {self.config['daily_total_limit']}")
        
        # AgentMail API configuration
        self.base_url = "https://api.agentmail.to/v0"
    
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
    
    def send_email(self, account: Dict, to_email: str, subject: str, text_content: str) -> Dict:
        """Send email via AgentMail API"""
        headers = {
            "Authorization": f"Bearer {account['api_key']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inbox_id": account['from_email'],
            "to": [to_email],
            "subject": subject,
            "text": text_content
        }
        
        # Add CC if specified in config
        if self.config.get('default_reply_to'):
            payload["cc"] = [self.config['default_reply_to']]
        
        try:
            response = requests.post(
                f"{self.base_url}/inboxes/{account['from_email']}/messages/send",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'message_id': result.get('message_id'),
                    'account': account['name'],
                    'status': 'sent'
                }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text[:200]}",
                    'account': account['name'],
                    'status': 'failed'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'account': account['name'],
                'status': 'error'
            }
    
    def process_csv_file(self, csv_path: str, limit: int = 50) -> Dict:
        """Process CSV file and send emails"""
        print(f"📄 Processing: {csv_path}")
        
        try:
            df = pd.read_csv(csv_path)
            print(f"   Found {len(df)} AI-generated messages")
            
            # Filter to limit
            if limit and len(df) > limit:
                df = df.head(limit)
                print(f"   Limiting to {limit} messages")
            
            results = {
                'total': len(df),
                'sent': 0,
                'failed': 0,
                'skipped': 0,
                'details': []
            }
            
            sent_count = 0
            for idx, row in df.iterrows():
                try:
                    email = str(row.get('email', '')).strip()
                    contact_name = str(row.get('contact_name', '')).strip()
                    company = str(row.get('company', '')).strip()
                    message = str(row.get('personalized_message', '')).strip()
                    
                    # Skip if no email
                    if not email or '@' not in email:
                        results['skipped'] += 1
                        results['details'].append({
                            'index': idx,
                            'contact': contact_name,
                            'email': email,
                            'status': 'skipped',
                            'reason': 'Invalid email'
                        })
                        continue
                    
                    # Get next available account
                    account = self.get_next_account()
                    if not account:
                        print(f"   ⚠️ No accounts available for {contact_name}")
                        results['skipped'] += 1
                        results['details'].append({
                            'index': idx,
                            'contact': contact_name,
                            'email': email,
                            'status': 'skipped',
                            'reason': 'No available accounts'
                        })
                        continue
                    
                    # Create subject
                    subject = f"Re: {company} - AI-Powered Deal Sourcing"
                    
                    print(f"   {idx+1}. {contact_name} ({email}) → {account['name']}")
                    
                    # Send email
                    send_result = self.send_email(account, email, subject, message)
                    
                    # Update account usage
                    if send_result['success']:
                        self.account_usage[account['name']]['today_count'] += 1
                        self.account_usage[account['name']]['total_sent'] += 1
                        self.account_usage[account['name']]['last_used'] = datetime.now().isoformat()
                        sent_count += 1
                        results['sent'] += 1
                        status = 'sent'
                    else:
                        self.account_usage[account['name']]['errors'] += 1
                        results['failed'] += 1
                        status = 'failed'
                    
                    results['details'].append({
                        'index': idx,
                        'contact': contact_name,
                        'email': email,
                        'account': account['name'],
                        'status': status,
                        'message_id': send_result.get('message_id'),
                        'error': send_result.get('error')
                    })
                    
                    # Rate limiting
                    if (idx + 1) % 10 == 0:
                        print(f"      Sent {idx+1}/{len(df)}...")
                        time.sleep(1)  # Brief pause
                    
                except Exception as e:
                    print(f"   {idx+1}. Error processing: {e}")
                    results['failed'] += 1
                    results['details'].append({
                        'index': idx,
                        'contact': 'Unknown',
                        'email': 'Unknown',
                        'status': 'error',
                        'error': str(e)
                    })
                    continue
            
            return results
            
        except Exception as e:
            print(f"❌ Error processing CSV: {e}")
            return {
                'total': 0,
                'sent': 0,
                'failed': 0,
                'skipped': 0,
                'details': [],
                'error': str(e)
            }
    
    def save_results(self, results: Dict, source_file: str):
        """Save sending results to log file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed log
        log_file = f"/Users/cubiczan/.openclaw/workspace/bdev_ai_agentmail_log_{timestamp}.json"
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'source_file': source_file,
            'results': results,
            'account_usage': self.account_usage,
            'config': {
                'rotation_strategy': self.config['rotation_strategy'],
                'daily_total_limit': self.config['daily_total_limit']
            }
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        # Update summary file
        summary_file = "/Users/cubiczan/.openclaw/workspace/bdev_ai_agentmail_summary.json"
        summary = {
            'last_run': datetime.now().isoformat(),
            'source_file': source_file,
            'results': {
                'sent': results['sent'],
                'failed': results['failed'],
                'skipped': results['skipped'],
                'total': results['total']
            },
            'account_stats': self.account_usage
        }
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        return log_file, summary_file
    
    def print_summary(self, results: Dict):
        """Print summary of sending results"""
        print("\n" + "="*60)
        print("📊 AGENTMAIL SENDING SUMMARY")
        print("="*60)
        
        print(f"Total messages: {results['total']}")
        print(f"✅ Sent: {results['sent']}")
        print(f"❌ Failed: {results['failed']}")
        print(f"⚠️ Skipped: {results['skipped']}")
        
        if results['sent'] > 0:
            success_rate = (results['sent'] / results['total']) * 100
            print(f"📈 Success rate: {success_rate:.1f}%")
        
        print("\n👥 Account Usage:")
        for account_name, usage in self.account_usage.items():
            today = usage.get('today_count', 0)
            total = usage.get('total_sent', 0)
            errors = usage.get('errors', 0)
            print(f"   • {account_name}: {today} sent today, {total} total, {errors} errors")
        
        print("\n" + "="*60)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Bdev.ai → AgentMail Integration')
    parser.add_argument('--csv', type=str, help='Path to CSV file (default: latest)')
    parser.add_argument('--limit', type=int, default=50, help='Number of emails to send')
    parser.add_argument('--test', action='store_true', help='Test mode (don\'t actually send)')
    
    args = parser.parse_args()
    
    print("="*60)
    print("Bdev.ai → AgentMail Integration - FIXED VERSION")
    print("="*60)
    
    # Find latest CSV if not specified
    csv_path = args.csv
    if not csv_path:
        csv_files = glob.glob("/Users/cubiczan/.openclaw/workspace/bdev_ai_openclaw_*.csv")
        if not csv_files:
            print("❌ No Bdev.ai CSV files found")
            return
        
        csv_path = max(csv_files, key=os.path.getctime)
        print(f"Using latest file: {csv_path}")
    
    # Initialize sender
    sender = AgentMailSender()
    
    if args.test:
        print("🧪 TEST MODE: Emails will not be sent")
        # In test mode, just show what would be sent
        df = pd.read_csv(csv_path)
        print(f"Found {len(df)} messages")
        print("First 5 messages:")
        for idx, row in df.head(5).iterrows():
            print(f"  {idx+1}. {row.get('contact_name', 'Unknown')} → {row.get('email', 'No email')}")
        return
    
    # Process and send
    results = sender.process_csv_file(csv_path, limit=args.limit)
    
    # Save results
    log_file, summary_file = sender.save_results(results, csv_path)
    
    # Print summary
    sender.print_summary(results)
    
    print(f"📁 Log saved to: {log_file}")
    print(f"📁 Summary saved to: {summary_file}")
    print("="*60)
    print("✅ AgentMail integration complete!")

if __name__ == "__main__":
    main()