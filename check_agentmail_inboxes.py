#!/usr/bin/env python3
"""
Check available AgentMail inboxes
"""

import requests
import json

API_KEY = "am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f"
BASE_URL = "https://api.agentmail.to/v0"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("Checking available inboxes for API key...")
print(f"API Key: {API_KEY[:20]}...")
print()

# Try to list inboxes
try:
    response = requests.get(
        f"{BASE_URL}/inboxes",
        headers=headers,
        timeout=10
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
except Exception as e:
    print(f"Error: {e}")

# Try specific inboxes
print("\n" + "="*60)
print("Testing specific inboxes:")
print("="*60)

test_inboxes = [
    "Zander@agentmail.to",
    "zander@agentmail.to",
    "sam@impactquadrant.info",
    "zanking@agentmail.to"
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
            print(f"   Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ {inbox}: {response.status_code} - {response.text[:100]}")
            
    except Exception as e:
        print(f"❌ {inbox}: Error - {e}")
    
    print()
