#!/usr/bin/env python3
"""
Test Zane@agentmail.to API key from memory
"""

import requests
import json

# API key from memory file
API_KEY = "am_us_6aa957b36fb69693140cb0787c894d90ec2e65ffe937049634b685b911c1ac14"
BASE_URL = "https://api.agentmail.to/v0"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("="*70)
print("Testing Zane@agentmail.to API Key")
print("="*70)
print(f"API Key: {API_KEY[:20]}...")
print()

# Test inbox access
test_inboxes = [
    "Zane@agentmail.to",
    "zane@agentmail.to",
    "Zander@agentmail.to",
    "zander@agentmail.to"
]

for inbox in test_inboxes:
    try:
        response = requests.get(
            f"{BASE_URL}/inboxes/{inbox}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✅ {inbox}: Accessible")
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)[:300]}")
        else:
            print(f"❌ {inbox}: {response.status_code} - {response.text[:100]}")
            
    except Exception as e:
        print(f"❌ {inbox}: Error - {str(e)[:100]}")
    print()

# Try to send a test email
print("="*70)
print("Testing Send Function")
print("="*70)

test_payload = {
    "inbox_id": "Zane@agentmail.to",
    "to": ["test@example.com"],
    "cc": ["sam@impactquadrant.info"],
    "subject": "Test Email from Defense Outreach Script",
    "text": "This is a test email to verify AgentMail is working."
}

try:
    response = requests.post(
        f"{BASE_URL}/inboxes/Zane@agentmail.to/messages/send",
        headers=headers,
        json=test_payload,
        timeout=30
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
except Exception as e:
    print(f"Error: {e}")
