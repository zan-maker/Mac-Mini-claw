#!/usr/bin/env python3
"""
Test AgentMail API connectivity
"""

import requests
import json

def test_agentmail_api(api_key, from_email):
    """Test AgentMail API connectivity"""
    url = "https://api.agentmail.to/v1/send"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    test_payload = {
        "to": "test@example.com",
        "from": from_email,
        "subject": "Test email from AgentMail API",
        "text": "This is a test email to verify API connectivity.",
        "html": "<p>This is a test email to verify API connectivity.</p>"
    }
    
    print(f"🔧 Testing AgentMail API...")
    print(f"   API Key: {api_key[:20]}...")
    print(f"   From: {from_email}")
    print(f"   URL: {url}")
    
    try:
        response = requests.post(url, headers=headers, json=test_payload, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        
        if response.status_code == 200:
            print("✅ API connection successful!")
            return True
        elif response.status_code == 401:
            print("❌ Authentication failed - check API key")
        elif response.status_code == 404:
            print("❌ Endpoint not found - check API URL")
        else:
            print(f"❌ API error: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
    
    return False

if __name__ == "__main__":
    # Test with primary account
    print("="*60)
    print("Testing Primary Account")
    print("="*60)
    
    with open("agentmail_config.json", "r") as f:
        config = json.load(f)
    
    primary = config['agentmail_accounts'][0]
    test_agentmail_api(primary['api_key'], primary['from_email'])