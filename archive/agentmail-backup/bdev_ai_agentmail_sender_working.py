#!/usr/bin/env python3
"""
Bdev.ai → AgentMail Integration - WORKING VERSION
Actually sends emails using AgentMail API with 3-account load balancing
"""

import os
import sys
import json
import pandas as pd
import requests
from datetime import datetime, date
import time
import random
from typing import Dict, List, Optional
import glob

def date_serializer(obj):
    """JSON serializer for datetime and date objects"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

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
    
    def get_next_account(self, strategy: str = None) -> Optional[Dict]:
        """Get next available AgentMail account based on strategy"""
        if strategy is None:
            strategy = self.config['rotation_strategy']
        
        available_accounts = []
        for account in self.accounts:
            usage = self.account_usage[account['name']]
            
            # Reset daily count if it's a new day
            if usage['today_date'] != datetime.now().date():
                usage['today_count'] = 0
                usage['today_date'] = datetime.now().date()
            
            # Check if account is within daily limit
            if usage['today_count'] < account['daily_limit']:
                available_accounts.append(account)
        
        if not available_accounts:
            print("   ⚠️  No accounts available (all at daily limit)")
            return None
        
        if strategy == "round_robin":
            # Simple round-robin
            account = available_accounts[self.account_rotation_index % len(available_accounts)]
            self.account_rotation_index += 1
            return account
        elif strategy == "least_used":
            # Use account with least usage today
            account = min(available_accounts, 
                         key=lambda a: self.account_usage[a['name']]['today_count'])
            return account
        else:
            # Default: random
            return random.choice(available_accounts)
    
    def send_email(self, to_email: str, subject: str, body: str, 
                   from_name: str = None, from_email: str = None) -> Dict:
        """Send email via AgentMail API"""
        
        # Get next available account
        account = self.get_next_account()
        if not account:
            return {'success': False, 'error': 'No available accounts'}
        
        # Prepare API request
        api_key = account['api_key']
        if from_name is None:
            from_name = account['from_name']
        if from_email is None:
            from_email = account['from_email']
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'to': to_email,
            'from': from_email,
            'from_name': from_name,
            'subject': subject,
            'body': body,
            'reply_to': self.config.get('default_reply_to', from_email),
            'tracking': self.config.get('tracking_enabled', True)
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/send",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            # Update account usage
            usage = self.account_usage[account['name']]
            usage['today_count'] += 1
            usage['total_sent'] += 1
            usage['last_used'] = datetime.now()
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'message_id': result.get('message_id'),
                    'account': account['name'],
                    'status': 'sent'
                }
            else:
                usage['errors'] += 1
                return {
                    'success': False,
                    'error': f"API error: {response.status_code}",
                    'account': account['name'],
                    'status': 'failed'
                }
                
        except Exception as e:
            usage = self.account_usage[account['name']]
            usage['errors'] += 1
            return {
                'success': False,
                'error': str(e),
                'account': account['name'],
                'status': 'failed'
            }
    
    def process_csv(self, csv_path: str, limit: int = None) -> Dict:
        """Process CSV file and send emails"""
        print(f"📄 Processing: {csv_path}")
        
        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            print(f"   ❌ Error reading CSV: {e}")
            return {'sent': 0, 'failed': 0, 'skipped': 0, 'total': 0}
        
        # Filter to limit if specified
        if limit and len(df) > limit:
            df = df.head(limit)
        
        print(f"   Found {len(df)} AI-generated messages")
        
        results = {
            'sent': 0,
            'failed': 0,
            'skipped': 0,
            'total': len(df)
        }
        
        detailed_results = []
        
        for idx, row in df.iterrows():
            # Check if email is available
            email = str(row.get('email', '')).strip()
            if not email or email.lower() in ['nan', 'none', '']:
                print(f"   {idx+1}/{len(df)}: ❌ Skipped - No email")
                results['skipped'] += 1
                detailed_results.append({
                    'index': idx,
                    'contact': row.get('contact_name', 'Unknown'),
                    'company': row.get('company', 'Unknown'),
                    'status': 'skipped',
                    'reason': 'No email address'
                })
                continue
            
            # Get personalized message
            message = row.get('personalized_message', '')
            if not message:
                message = f"Hello {row.get('contact_name', 'Investor')},\n\nI was reviewing your profile at {row.get('company', 'your firm')} and wanted to connect regarding potential investment opportunities.\n\nBest regards,\nSam Desigan"
            
            # Create subject
            subject = f"Investment Opportunity - {row.get('company', 'Your Firm')}"
            
            # Send email
            print(f"   {idx+1}/{len(df)}: 📧 Sending to {email}...", end='')
            
            result = self.send_email(
                to_email=email,
                subject=subject,
                body=message
            )
            
            if result['success']:
                print(f" ✅ Sent via {result['account']}")
                results['sent'] += 1
                status = 'sent'
                reason = f"Sent via {result['account']}"
            else:
                print(f" ❌ Failed: {result.get('error', 'Unknown error')}")
                results['failed'] += 1
                status = 'failed'
                reason = result.get('error', 'Unknown error')
            
            detailed_results.append({
                'index': idx,
                'contact': row.get('contact_name', 'Unknown'),
                'company': row.get('company', 'Unknown'),
                'email': email,
                'status': status,
                'reason': reason,
                'account': result.get('account'),
                'timestamp': datetime.now().isoformat()
            })
            
            # Small delay to avoid rate limiting
            if idx < len(df) - 1:
                time.sleep(1)
        
        return {
            'sent': results['sent'],
            'failed': results['failed'],
            'skipped': results['skipped'],
            'total': results['total'],
            'detailed': detailed_results
        }
    
    def save_results(self, results: Dict, source_file: str):
        """Save results to log files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed log
        log_file = f"/Users/cubiczan/.openclaw/workspace/bdev_ai_agentmail_log_{timestamp}.json"
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'source_file': source_file,
            'results': {
                'sent': results['sent'],
                'failed': results['failed'],
                'skipped': results['skipped'],
                'total': results['total']
            },
            'detailed_results': results.get('detailed', []),
            'account_usage': self.account_usage,
            'config': {
                'rotation_strategy': self.config['rotation_strategy'],
                'daily_total_limit': self.config['daily_total_limit']
            }
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2, default=date_serializer)
        
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
            json.dump(summary, f, indent=2, default=date_serializer)
        
        return log_file, summary_file
    
    def print_summary(self, results: Dict):
        """Print summary of sending results"""
        print("\n" + "="*60)
        print("📊 AGENTMAIL SENDING SUMMARY")
        print("="*60)
        print(f"   Total processed: {results['total']}")
        print(f"   ✅ Successfully sent: {results['sent']}")
        print(f"   ❌ Failed: {results['failed']}")
        print(f"   ⏭️  Skipped (no email): {results['skipped']}")
        
        if results['total'] > 0:
            success_rate = (results['sent'] / results['total']) * 100
            print(f"   📈 Success rate: {success_rate:.1f}%")
        
        print("\n👥 Account Usage:")
        for account_name, usage in self.account_usage.items():
            print(f"   • {account_name}: {usage['today_count']} sent today")
        
        print("="*60)

def find_latest_bdev_file():
    """Find the latest Bdev.ai generated CSV file"""
    pattern = "/Users/cubiczan/.openclaw/workspace/bdev_ai_openclaw_*.csv"
    files = glob.glob(pattern)
    if not files:
        return None
    
    # Get the most recent file
    latest = max(files, key=os.path.getctime)
    return latest

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Send Bdev.ai messages via AgentMail')
    parser.add_argument('--csv', type=str, help='Path to CSV file')
    parser.add_argument('--limit', type=int, default=50, help='Limit number of emails to send')
    args = parser.parse_args()
    
    print("="*60)
    print("Bdev.ai → AgentMail Integration - WORKING VERSION")
    print("="*60)
    
    # Find CSV file
    csv_path = args.csv
    if not csv_path:
        csv_path = find_latest_bdev_file()
    
    if not csv_path or not os.path.exists(csv_path):
        print("❌ No Bdev.ai CSV file found!")
        print("   Run the AI message generator first:")
        print("   python3 bdev_ai_openclaw_integration_final.py --batch-size 50")
        return
    
    print(f"Using latest file: {csv_path}")
    
    # Initialize sender
    sender = AgentMailSender()
    
    # Process and send
    results = sender.process_csv(csv_path, limit=args.limit)
    
    # Save results
    log_file, summary_file = sender.save_results(results, csv_path)
    
    # Print summary
    sender.print_summary(results)
    
    print(f"\n📁 Log saved: {log_file}")
    print(f"📊 Summary saved: {summary_file}")
    print("="*60)
    print("✅ AgentMail sending complete!")

if __name__ == "__main__":
    main()