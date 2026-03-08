#!/usr/bin/env python3
"""
Bdev.ai → Gmail SMTP Integration
Replaces failing AgentMail integration with Gmail SMTP
"""

import os
import sys
import json
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time
import random
from typing import Dict, List, Optional
import glob

class GmailSender:
    """Send Bdev.ai generated messages via Gmail SMTP"""
    
    def __init__(self, config_path: str = None):
        # Load configuration
        if config_path is None:
            config_path = "/Users/cubiczan/.openclaw/workspace/gmail_config.json"
        
        # Try to load config, create default if not exists
        try:
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Config file not found: {config_path}")
            print("   Using default Gmail configuration")
            self.config = self.create_default_config()
            # Save default config
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        
        # Initialize Gmail accounts
        self.accounts = self.config.get('gmail_accounts', [])
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
        
        print(f"🔧 Gmail Sender initialized")
        print(f"   Accounts: {len(self.accounts)} configured")
        print(f"   Strategy: {self.config.get('rotation_strategy', 'round_robin')}")
        print(f"   Daily limit: {self.config.get('daily_total_limit', 500)}")
    
    def create_default_config(self) -> Dict:
        """Create default Gmail configuration"""
        return {
            "gmail_accounts": [
                {
                    "name": "Primary",
                    "email": "sam@cubiczan.com",
                    "password": "YOUR_GMAIL_APP_PASSWORD_HERE",  # Use App Password, not regular password
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "from_name": "Sam Desigan",
                    "daily_limit": 500,
                    "priority": 1,
                    "enabled": True
                }
            ],
            "rotation_strategy": "round_robin",
            "daily_total_limit": 500,
            "rate_limit_per_minute": 60,
            "default_sender": "Sam Desigan",
            "default_reply_to": "sam@cubiczan.com",
            "tracking_enabled": False
        }
    
    def get_next_account(self) -> Optional[Dict]:
        """Get next available Gmail account based on rotation strategy"""
        if not self.accounts:
            return None
        
        # Simple round-robin for now
        account = self.accounts[self.account_rotation_index % len(self.accounts)]
        self.account_rotation_index += 1
        
        # Check if account is enabled and under daily limit
        if not account.get('enabled', True):
            return self.get_next_account()  # Try next account
        
        if self.account_usage[account['name']]['today_count'] >= account.get('daily_limit', 500):
            print(f"   ⚠️ Account {account['name']} reached daily limit")
            return self.get_next_account()  # Try next account
        
        return account
    
    def send_email(self, account: Dict, to_email: str, subject: str, text_content: str) -> Dict:
        """Send email via Gmail SMTP"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{account.get('from_name', 'Sam Desigan')} <{account['email']}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add CC if specified in config
            if self.config.get('default_reply_to'):
                msg['Cc'] = self.config['default_reply_to']
            
            # Add body
            msg.attach(MIMEText(text_content, 'plain'))
            
            # Connect to Gmail SMTP server
            server = smtplib.SMTP(account['smtp_server'], account['smtp_port'])
            server.starttls()  # Secure the connection
            server.login(account['email'], account['password'])
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            return {
                'success': True,
                'account': account['name'],
                'status': 'sent',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'account': account['name'],
                'status': 'failed',
                'timestamp': datetime.now().isoformat()
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
                        'error': send_result.get('error'),
                        'timestamp': send_result.get('timestamp')
                    })
                    
                    # Rate limiting
                    if (idx + 1) % 10 == 0:
                        print(f"      Sent {idx+1}/{len(df)}...")
                        time.sleep(2)  # Brief pause to avoid rate limiting
                    
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
        log_file = f"/Users/cubiczan/.openclaw/workspace/bdev_ai_gmail_log_{timestamp}.json"
        
        # Convert account_usage to serializable format
        serializable_account_usage = {}
        for acc_name, acc_stats in self.account_usage.items():
            serializable_account_usage[acc_name] = {
                'today_count': acc_stats['today_count'],
                'today_date': acc_stats['today_date'].isoformat() if hasattr(acc_stats['today_date'], 'isoformat') else str(acc_stats['today_date']),
                'total_sent': acc_stats['total_sent'],
                'last_used': acc_stats['last_used'],
                'errors': acc_stats['errors']
            }
        
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'source_file': source_file,
            'results': results,
            'account_usage': serializable_account_usage,
            'config': {
                'rotation_strategy': self.config.get('rotation_strategy'),
                'daily_total_limit': self.config.get('daily_total_limit')
            }
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        # Update summary file
        summary_file = "/Users/cubiczan/.openclaw/workspace/bdev_ai_gmail_summary.json"
        summary = {
            'last_run': datetime.now().isoformat(),
            'source_file': source_file,
            'results': {
                'sent': results['sent'],
                'failed': results['failed'],
                'skipped': results['skipped'],
                'total': results['total']
            },
            'account_usage': serializable_account_usage
        }
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📊 Results saved to: {log_file}")
        print(f"   Sent: {results['sent']}, Failed: {results['failed']}, Skipped: {results['skipped']}")
        
        return log_file

def main():
    """Main function"""
    print("="*70)
    print("Bdev.ai → Gmail SMTP Integration")
    print("="*70)
    
    # Find the most recent enriched CSV file
    csv_files = glob.glob("/Users/cubiczan/.openclaw/workspace/bdev_ai_enriched_*.csv")
    
    if not csv_files:
        print("❌ No enriched CSV files found")
        print("   Looking for: bdev_ai_enriched_*.csv")
        return
    
    # Use the most recent file
    latest_csv = max(csv_files, key=os.path.getctime)
    print(f"📁 Using file: {latest_csv}")
    
    # Initialize sender
    sender = GmailSender()
    
    # Process and send emails
    results = sender.process_csv_file(latest_csv, limit=50)
    
    # Save results
    log_file = sender.save_results(results, latest_csv)
    
    print("="*70)
    print("✅ Gmail sending complete!")
    print(f"   Total: {results['total']}")
    print(f"   Sent: {results['sent']} ✅")
    print(f"   Failed: {results['failed']} ❌")
    print(f"   Skipped: {results['skipped']} ⚠️")
    print(f"   Log: {log_file}")
    print("="*70)

if __name__ == "__main__":
    main()