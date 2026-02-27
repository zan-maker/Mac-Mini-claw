#!/usr/bin/env python3
"""
Gmail Rotation Module for Cron Jobs
Simple rotation between 2 Gmail accounts with failover
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import json
import os
from datetime import datetime
import time

class GmailRotator:
    """Gmail account rotation system"""
    
    def __init__(self, state_file=None):
        # Gmail accounts for rotation
        self.accounts = [
            {
                "email": "zan@impactquadrant.info",
                "password": "apbj bvsl tngo vqhu",
                "name": "Zane",
                "daily_limit": 40  # Conservative limit (80% of 50)
            },
            {
                "email": "sam@impactquadrant.info",
                "password": "ajup xyhf abbx iugj",
                "name": "Sam",
                "daily_limit": 40
            }
        ]
        
        # State tracking
        self.state_file = state_file or "/Users/cubiczan/.openclaw/workspace/gmail-rotation-state.json"
        self.cc_email = "sam@impactquadrant.info"
        
        # Load or initialize state
        self.state = self._load_state()
    
    def _load_state(self):
        """Load rotation state from file"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                
                # Check if we need to reset daily counts
                today = datetime.now().strftime('%Y-%m-%d')
                if state.get('last_reset_date') != today:
                    state['last_reset_date'] = today
                    for account in self.accounts:
                        email = account['email']
                        if email in state['account_stats']:
                            state['account_stats'][email]['sent_today'] = 0
                
                return state
            except:
                pass
        
        # Initialize new state
        state = {
            'current_account_index': 0,
            'last_reset_date': datetime.now().strftime('%Y-%m-%d'),
            'account_stats': {}
        }
        
        for account in self.accounts:
            state['account_stats'][account['email']] = {
                'sent_today': 0,
                'total_sent': 0,
                'last_used': None
            }
        
        return state
    
    def _save_state(self):
        """Save rotation state to file"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def _get_next_account(self):
        """Get next available account with rotation logic"""
        
        # Try current account first
        current_idx = self.state['current_account_index']
        current_account = self.accounts[current_idx]
        current_email = current_account['email']
        
        # Check if current account is under limit
        current_stats = self.state['account_stats'][current_email]
        if current_stats['sent_today'] < current_account['daily_limit']:
            return current_account
        
        # Try next account
        next_idx = (current_idx + 1) % len(self.accounts)
        next_account = self.accounts[next_idx]
        next_email = next_account['email']
        next_stats = self.state['account_stats'][next_email]
        
        if next_stats['sent_today'] < next_account['daily_limit']:
            self.state['current_account_index'] = next_idx
            self._save_state()
            return next_account
        
        # Both accounts at limit - use whichever has fewer sent today
        if current_stats['sent_today'] <= next_stats['sent_today']:
            return current_account
        else:
            self.state['current_account_index'] = next_idx
            self._save_state()
            return next_account
    
    def send_email(self, to_email, to_name, subject, body, delay_seconds=5):
        """
        Send email using Gmail rotation
        
        Args:
            to_email: Recipient email
            to_name: Recipient name
            subject: Email subject
            body: Email body (plain text)
            delay_seconds: Delay after sending (default: 5)
        
        Returns:
            tuple: (success, account_used, error_message)
        """
        
        account = self._get_next_account()
        account_email = account['email']
        
        print(f"[GmailRotator] Using account: {account['name']} ({account_email})")
        print(f"[GmailRotator] Sent today: {self.state['account_stats'][account_email]['sent_today']}/{account['daily_limit']}")
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{account['name']} <{account['email']}>"
            msg['To'] = to_email
            msg['Cc'] = self.cc_email
            
            # Create HTML version
            html_body = body.replace('\n', '<br>')
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Create plain text version
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                server.login(account['email'], account['password'])
                server.send_message(msg)
            
            # Update state
            self.state['account_stats'][account_email]['sent_today'] += 1
            self.state['account_stats'][account_email]['total_sent'] += 1
            self.state['account_stats'][account_email]['last_used'] = datetime.now().isoformat()
            self._save_state()
            
            # Rotate to next account for next email
            self.state['current_account_index'] = (self.accounts.index(account) + 1) % len(self.accounts)
            self._save_state()
            
            print(f"[GmailRotator] ✅ Email sent to: {to_name} ({to_email})")
            
            # Delay before next email
            if delay_seconds > 0:
                time.sleep(delay_seconds)
            
            return True, account_email, None
            
        except Exception as e:
            error_msg = str(e)
            print(f"[GmailRotator] ❌ Failed to send to {to_name} ({to_email}): {error_msg}")
            
            # Try with other account as backup
            other_idx = (self.accounts.index(account) + 1) % len(self.accounts)
            other_account = self.accounts[other_idx]
            
            print(f"[GmailRotator] Trying backup account: {other_account['name']} ({other_account['email']})")
            
            try:
                # Retry with other account
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = f"{other_account['name']} <{other_account['email']}>"
                msg['To'] = to_email
                msg['Cc'] = self.cc_email
                
                html_body = body.replace('\n', '<br>')
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
                
                text_part = MIMEText(body, 'plain')
                msg.attach(text_part)
                
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                    server.login(other_account['email'], other_account['password'])
                    server.send_message(msg)
                
                # Update state for backup account
                other_email = other_account['email']
                self.state['account_stats'][other_email]['sent_today'] += 1
                self.state['account_stats'][other_email]['total_sent'] += 1
                self.state['account_stats'][other_email]['last_used'] = datetime.now().isoformat()
                self.state['current_account_index'] = other_idx
                self._save_state()
                
                print(f"[GmailRotator] ✅ Email sent via backup to: {to_name} ({to_email})")
                
                # Delay before next email
                if delay_seconds > 0:
                    time.sleep(delay_seconds)
                
                return True, other_email, None
                
            except Exception as e2:
                error_msg2 = f"Primary: {error_msg}, Backup: {str(e2)}"
                print(f"[GmailRotator] ❌ Backup also failed: {str(e2)}")
                return False, None, error_msg2
    
    def get_stats(self):
        """Get current rotation statistics"""
        stats = {
            'total_accounts': len(self.accounts),
            'current_account_index': self.state['current_account_index'],
            'last_reset_date': self.state['last_reset_date'],
            'accounts': []
        }
        
        for account in self.accounts:
            email = account['email']
            account_stats = self.state['account_stats'][email]
            stats['accounts'].append({
                'email': email,
                'name': account['name'],
                'sent_today': account_stats['sent_today'],
                'daily_limit': account['daily_limit'],
                'total_sent': account_stats['total_sent'],
                'last_used': account_stats['last_used']
            })
        
        return stats
    
    def print_stats(self):
        """Print current statistics"""
        stats = self.get_stats()
        
        print("=" * 60)
        print("GMAIL ROTATION STATISTICS")
        print("=" * 60)
        print(f"Last reset: {stats['last_reset_date']}")
        print(f"Current account index: {stats['current_account_index']}")
        print()
        
        for account in stats['accounts']:
            status = "✅ AVAILABLE" if account['sent_today'] < account['daily_limit'] else "⚠️ AT LIMIT"
            print(f"{account['name']} ({account['email']}):")
            print(f"  {status}")
            print(f"  Sent today: {account['sent_today']}/{account['daily_limit']}")
            print(f"  Total sent: {account['total_sent']}")
            if account['last_used']:
                print(f"  Last used: {account['last_used']}")
            print()


# Example usage
if __name__ == "__main__":
    # Initialize rotator
    rotator = GmailRotator()
    
    # Print current stats
    rotator.print_stats()
    
    # Example email (commented out - won't actually send)
    """
    subject = "Test email from Gmail Rotator"
    body = \"\"\"Hello,

This is a test email sent using the Gmail rotation system.

The system automatically rotates between 2 Gmail accounts to avoid rate limits.

Best regards,

Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.\"\"\"
    
    # Send test email
    # success, account_used, error = rotator.send_email(
    #     to_email="test@example.com",
    #     to_name="Test Recipient",
    #     subject=subject,
    #     body=body,
    #     delay_seconds=0  # No delay for test
    # )
    """
    
    print("=" * 60)
    print("Gmail Rotation System Ready")
    print("=" * 60)
    print()
    print("To use in your scripts:")
    print("1. from gmail_rotation import GmailRotator")
    print("2. rotator = GmailRotator()")
    print("3. success, account, error = rotator.send_email(...)")
    print()
    print("Features:")
    print("- Automatic rotation between 2 Gmail accounts")
    print("- 5-second delays between emails (configurable)")
    print("- Automatic failover if account fails")
    print("- Daily limit tracking (40 emails per account)")
    print("- State persistence to JSON file")
