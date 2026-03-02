#!/usr/bin/env python3
"""Test all AgentMail API keys"""

import requests
import json

# All API keys from config
api_keys = {
    "Primary": "am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f",
    "Secondary": "am_us_0c848180ab2f23ce83d97643f50db7610c3e7b62b3b163ecb5bf3222d0395d5c"
}

BASE_URL = "https://api.agentmail.to"

for account_name, api_key in api_keys.items():
    print(f"\n{'='*60}")
    print(f"Testing {account_name} Account")
    print(f"{'='*60}")
    print(f"API Key: {api_key[:20]}...{api_key[-10:]}")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Try v0/inboxes
    print(f"\n1. Testing /v0/inboxes...")
    try:
        response = requests.get(f"{BASE_URL}/v0/inboxes", headers=headers, timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS!")
            print(f"   Inboxes: {json.dumps(data, indent=2)}")
        else:
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    
    # Try sending a test email
    print(f"\n2. Testing email send...")
    try:
        payload = {
            "inbox_id": "test@agentmail.to",
            "to": ["test@example.com"],
            "subject": "API Test",
            "text": "Testing API"
        }
        response = requests.post(
            f"{BASE_URL}/v0/inboxes/test@agentmail.to/messages/send",
            headers=headers,
            json=payload,
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   Error: {str(e)}")

print(f"\n{'='*60}")
print("Summary")
print(f"{'='*60}")
print("Check which API key works above")
