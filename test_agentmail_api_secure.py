#!/usr/bin/env python3
"""
Test AgentMail API connectivity - SECURE VERSION
Uses environment variables for API keys
"""

import os
import requests
import json
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_env_var(name, required=True):
    """Safely get environment variable"""
    value = os.environ.get(name)
    if required and not value:
        print(f"❌ ERROR: {name} environment variable not set")
        print(f"   Add it to your .env file or export it")
        sys.exit(1)
    return value

def test_agentmail_api():
    """Test AgentMail API connectivity using environment variables"""
    # Get credentials from environment
    api_key = get_env_var("AGENTMAIL_API_KEY")
    from_email = get_env_var("AGENTMAIL_FROM_EMAIL", required=False) or "test@agentmail.to"
    
    url = "https://api.agentmail.to/v1/send"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    test_payload = {
        "to": "test@example.com",
        "from": from_email,
        "subject": "AgentMail API Test",
        "text": "This is a test email from AgentMail API.",
        "html": "<p>This is a test email from AgentMail API.</p>"
    }
    
    print(f"🔧 Testing AgentMail API...")
    print(f"   From: {from_email}")
    print(f"   API Key: {api_key[:10]}...")
    
    try:
        response = requests.post(url, headers=headers, json=test_payload, timeout=10)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ AgentMail API is working!")
            return True
        else:
            print(f"❌ AgentMail API error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("AGENTMAIL API TEST - SECURE VERSION")
    print("=" * 60)
    print("")
    print("📋 This script uses environment variables from .env file")
    print("   Make sure you have:")
    print("   1. Created .env file from .env.template")
    print("   2. Added your actual AGENTMAIL_API_KEY")
    print("   3. Optionally set AGENTMAIL_FROM_EMAIL")
    print("")
    
    # Test the API
    success = test_agentmail_api()
    
    print("")
    print("=" * 60)
    if success:
        print("✅ TEST COMPLETE - API IS WORKING")
    else:
        print("❌ TEST FAILED - CHECK YOUR CONFIGURATION")
    print("=" * 60)

if __name__ == "__main__":
    main()