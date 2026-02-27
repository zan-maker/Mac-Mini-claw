#!/usr/bin/env python3
"""
Quick test: Send 1 test email via AgentMail to verify everything works
"""

import requests
import json

# AgentMail configuration
AGENTMAIL_API_KEY = "am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f"
FROM_EMAIL = "Zane@agentmail.to"
CC_EMAIL = "sam@impactquadrant.info"

def test_agentmail():
    """Test AgentMail API"""
    print("Testing AgentMail API...")
    
    url = "https://api.agentmail.to/v1/emails"
    
    headers = {
        "Authorization": f"Bearer {AGENTMAIL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Test email
    payload = {
        "from": FROM_EMAIL,
        "to": ["test@example.com"],  # Using test email
        "cc": [CC_EMAIL],
        "subject": "Test: Defense Sector Outreach System",
        "body": """This is a test email to verify the AgentMail integration is working.

The Hunter.io API key has been updated and is now working.

Next step: Send actual outreach emails to defense companies.

Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    }
    
    try:
        print("Sending test email...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ AgentMail API is working!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ AgentMail API error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("AGENTMAIL INTEGRATION TEST")
    print("=" * 60)
    
    success = test_agentmail()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ All systems ready for defense sector outreach!")
    else:
        print("❌ AgentMail test failed - check API key")
    print("=" * 60)