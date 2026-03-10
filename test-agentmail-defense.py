#!/usr/bin/env python3
"""
Test AgentMail API for Defense Outreach
"""

import requests
import json

# Test both configurations
configs = [
    {
        "name": "Cron Instructions",
        "api_key": "am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f",
        "inbox_id": "zander@agentmail.to"
    },
    {
        "name": "Config Secondary",
        "api_key": "am_us_0c848180ab2f23ce83d97643f50db7610c3e7b62b3b163ecb5bf3222d0395d5c",
        "inbox_id": "zanking@agentmail.to"
    },
    {
        "name": "Config Primary",
        "api_key": "am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f",
        "inbox_id": "sam@impactquadrant.info"
    },
    {
        "name": "Memory Config",
        "api_key": "am_us_6aa957b36fb69693140cb0787c894d90ec2e65ffe937049634b685b911c1ac14",
        "inbox_id": "zane@agentmail.to"
    }
]

BASE_URL = "https://api.agentmail.to/v0"

for config in configs:
    print(f"\n{'='*60}")
    print(f"Testing: {config['name']}")
    print(f"  Inbox: {config['inbox_id']}")
    print(f"  API Key: {config['api_key'][:20]}...")
    print('='*60)
    
    # Test 1: Check inbox
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/inboxes/{config['inbox_id']}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✅ Inbox accessible")
            inbox_data = response.json()
            print(f"   Inbox ID: {inbox_data.get('inbox_id')}")
        else:
            print(f"❌ Inbox check failed: {response.status_code}")
            print(f"   Error: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Try to send (to a test address)
    print("\n  Testing send...")
    payload = {
        "inbox_id": config['inbox_id'],
        "to": ["test@example.com"],
        "subject": f"Defense Outreach Test - {config['name']}",
        "text": "This is a test email from defense sector outreach."
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/inboxes/{config['inbox_id']}/messages/send",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Send successful!")
            print(f"   Message ID: {result.get('message_id')}")
        else:
            print(f"❌ Send failed: {response.status_code}")
            print(f"   Error: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Send error: {e}")

print(f"\n{'='*60}")
print("Testing complete!")
print('='*60)
