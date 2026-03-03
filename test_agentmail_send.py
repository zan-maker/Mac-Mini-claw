#!/usr/bin/env python3
"""
Test AgentMail sending with Bdev.ai generated messages
"""

import requests
import json
import pandas as pd
from datetime import datetime
import sys

def test_agentmail_api(api_key, from_email):
    """Test AgentMail API connectivity"""
    BASE_URL = "https://api.agentmail.to/v0"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print(f"Testing AgentMail API for: {from_email}")
    
    # Test inbox access
    try:
        response = requests.get(
            f"{BASE_URL}/inboxes/{from_email}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✅ Inbox accessible: {from_email}")
            return True
        else:
            print(f"❌ Inbox error {response.status_code}: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ API error: {e}")
        return False

def send_agentmail_email(api_key, from_email, to_email, subject, text_content, cc=None):
    """Send email via AgentMail API"""
    BASE_URL = "https://api.agentmail.to/v0"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inbox_id": from_email,
        "to": [to_email],
        "subject": subject,
        "text": text_content
    }
    
    if cc:
        payload["cc"] = [cc] if isinstance(cc, str) else cc
    
    try:
        response = requests.post(
            f"{BASE_URL}/inboxes/{from_email}/messages/send",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Email sent to {to_email}: {result.get('message_id', 'No ID')}")
            return True
        else:
            print(f"❌ Send failed {response.status_code}: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Send error: {e}")
        return False

def main():
    # Load configuration
    with open('/Users/cubiczan/.openclaw/workspace/agentmail_config.json', 'r') as f:
        config = json.load(f)
    
    accounts = config['agentmail_accounts']
    
    print("="*60)
    print("AgentMail API Test with Bdev.ai Configuration")
    print("="*60)
    
    # Test each account
    for account in accounts:
        if account['enabled']:
            print(f"\nTesting account: {account['name']}")
            print(f"  From: {account['from_email']}")
            print(f"  API Key: {account['api_key'][:20]}...")
            
            # Test API connectivity
            if test_agentmail_api(account['api_key'], account['from_email']):
                # Try sending a test email
                test_to = "test@example.com"  # Test email
                test_subject = f"AgentMail Test - {account['name']} - {datetime.now().strftime('%H:%M')}"
                test_text = f"This is a test email from {account['name']} account.\n\nIf received, AgentMail API is working!"
                
                print(f"  Sending test email to {test_to}...")
                send_agentmail_email(
                    account['api_key'],
                    account['from_email'],
                    test_to,
                    test_subject,
                    test_text,
                    cc=account.get('from_email')
                )
    
    print("\n" + "="*60)
    print("Testing complete!")
    print("="*60)

if __name__ == "__main__":
    main()