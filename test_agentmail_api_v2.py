#!/usr/bin/env python3
"""Test AgentMail API connectivity with different endpoints"""

import requests
import json

api_key = "am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f"

# Try different base URLs
endpoints = [
    "https://api.agentmail.to/v0",
    "https://api.agentmail.to/v1",
    "https://api.agentmail.to",
    "https://agentmail.to/api/v0",
    "https://agentmail.to/api/v1",
    "https://agentmail.to/api"
]

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

for base_url in endpoints:
    print(f"\n🔍 Testing: {base_url}")
    
    # Try GET request first
    try:
        response = requests.get(f"{base_url}/account", headers=headers, timeout=5)
        print(f"   GET /account: {response.status_code} - {response.text[:100]}")
    except Exception as e:
        print(f"   GET /account: Error - {e}")
    
    # Try POST request
    payload = {
        'to': 'test@example.com',
        'from': 'sam@impactquadrant.info',
        'subject': 'Test',
        'body': 'Test'
    }
    
    try:
        response = requests.post(f"{base_url}/send", headers=headers, json=payload, timeout=5)
        print(f"   POST /send: {response.status_code} - {response.text[:100]}")
    except Exception as e:
        print(f"   POST /send: Error - {e}")