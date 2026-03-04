#!/usr/bin/env python3
"""Test AgentMail API connectivity"""

import requests
import json

# Test with Primary account
api_key = "am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f"
base_url = "https://api.agentmail.to/v0"

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# Test 1: Check API status
print("🔍 Testing AgentMail API connectivity...")
print(f"   API Key: {api_key[:20]}...")
print(f"   Base URL: {base_url}")

try:
    # Try to get account info or test endpoint
    response = requests.get(f"{base_url}/account", headers=headers, timeout=10)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Try sending a test email
print("\n📧 Testing send endpoint...")
payload = {
    'to': 'test@example.com',
    'from': 'sam@impactquadrant.info',
    'from_name': 'Sam Desigan',
    'subject': 'Test from AgentMail API',
    'body': 'This is a test email from AgentMail API integration.',
    'reply_to': 'sam@impactquadrant.info',
    'tracking': True
}

try:
    response = requests.post(f"{base_url}/send", headers=headers, json=payload, timeout=30)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"   Error: {e}")