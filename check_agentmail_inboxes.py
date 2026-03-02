#!/usr/bin/env python3
"""Check AgentMail inboxes"""

import requests
import json

API_KEY = "am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f"
BASE_URL = "https://api.agentmail.to"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("Checking AgentMail inboxes...")
print(f"API Key: {API_KEY[:20]}...{API_KEY[-10:]}")
print()

# Try v0 API
print("1. Trying /v0/inboxes...")
try:
    response = requests.get(f"{BASE_URL}/v0/inboxes", headers=headers, timeout=30)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:500]}")
    if response.status_code == 200:
        data = response.json()
        print(f"\n   Inboxes: {json.dumps(data, indent=2)}")
except Exception as e:
    print(f"   Error: {str(e)}")

print()

# Try v1 API
print("2. Trying /v1/inboxes...")
try:
    response = requests.get(f"{BASE_URL}/v1/inboxes", headers=headers, timeout=30)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:500]}")
    if response.status_code == 200:
        data = response.json()
        print(f"\n   Inboxes: {json.dumps(data, indent=2)}")
except Exception as e:
    print(f"   Error: {str(e)}")

print()

# Try root
print("3. Trying / (root)...")
try:
    response = requests.get(f"{BASE_URL}/", headers=headers, timeout=30)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:500]}")
except Exception as e:
    print(f"   Error: {str(e)}")
