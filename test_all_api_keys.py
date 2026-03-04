#!/usr/bin/env python3
"""
Test different AgentMail API keys
"""

import requests
import json

# API keys from config
API_KEYS = {
    "Primary (sam@impactquadrant.info)": "am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f",
    "Secondary (zanking@agentmail.to)": "am_us_0c848180ab2f23ce83d97643f50db7610c3e7b62b3b163ecb5bf3222d0395d5c"
}

BASE_URL = "https://api.agentmail.to/v0"

test_inboxes = [
    "Zander@agentmail.to",
    "zander@agentmail.to",
    "sam@impactquadrant.info",
    "zanking@agentmail.to"
]

for account_name, api_key in API_KEYS.items():
    print("="*70)
    print(f"Testing API Key: {account_name}")
    print(f"Key: {api_key[:20]}...")
    print("="*70)
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
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
                print(f"   Data: {json.dumps(data, indent=2)[:200]}")
            else:
                print(f"❌ {inbox}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {inbox}: Error - {str(e)[:100]}")
    
    print()
