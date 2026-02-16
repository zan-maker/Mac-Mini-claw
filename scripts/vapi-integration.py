#!/usr/bin/env python3
"""
Vapi Voice Agent Integration
Phone: +1 (572) 300 6475
"""

import requests
import json
from datetime import datetime

VAPI_API_KEY = "24455236-8179-4d7b-802a-876aa44d4677"
VAPI_PUBLIC_KEY = "be077154-0347-4c8e-a668-36bee62039ca"
VAPI_PHONE_1 = "+1 (572) 300 6475"
VAPI_PHONE_2 = "+1 (575) 232 9474"
VAPI_PHONE_1_ID = "07867d73-85a2-475c-b7c1-02f2879a4916"
VAPI_PHONE_2_ID = "c7b4cd62-0a0a-426a-bc0f-890c7b171d3a"
LEAD_AGENT_ID = "3f5b4b81-9975-4f29-958b-cadd7694deca"
BASE_URL = "https://api.vapi.ai"

headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json"
}

def get_phone_numbers():
    """List all phone numbers"""
    response = requests.get(f"{BASE_URL}/phone-number", headers=headers)
    return response.json()

def get_assistants():
    """List all assistants"""
    response = requests.get(f"{BASE_URL}/assistant", headers=headers)
    return response.json()

def create_lead_qualification_assistant():
    """Create a lead qualification assistant"""
    payload = {
        "name": "Lead Qualification Agent",
        "model": {
            "provider": "openai",
            "model": "gpt-4o-mini"
        },
        "firstMessage": "Hi, this is an automated call following up on your interest in expense reduction services. Is now a good time to talk?",
        "systemPrompt": """You are a lead qualification agent for expense reduction services.

Your goal is to:
1. Confirm the prospect is interested
2. Ask qualifying questions:
   - How many employees does your company have?
   - What's your biggest expense challenge right now?
   - Are you the decision maker for expense management?
3. If qualified, offer to schedule a free analysis
4. Capture their email and best callback number
5. Be professional and brief

If they're not interested, thank them and end the call politely."""
    }
    
    response = requests.post(
        f"{BASE_URL}/assistant",
        headers=headers,
        json=payload
    )
    return response.json()

def make_outbound_call(to_number, assistant_id=None):
    """Make an outbound call"""
    payload = {
        "type": "outboundPhoneCall",
        "phoneNumberId": "YOUR_PHONE_ID",  # Get from get_phone_numbers()
        "customer": {
            "number": to_number
        }
    }
    
    if assistant_id:
        payload["assistantId"] = assistant_id
    
    response = requests.post(
        f"{BASE_URL}/call",
        headers=headers,
        json=payload
    )
    return response.json()

def get_call_logs():
    """Get recent call logs"""
    response = requests.get(f"{BASE_URL}/call", headers=headers)
    return response.json()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Vapi Voice Agent Integration")
    print("="*60 + "\n")
    
    print(f"Phone: {VAPI_PHONE}")
    print(f"API Key: {VAPI_API_KEY[:20]}...")
    
    # Test connection
    print("\n📊 Fetching phone numbers...")
    try:
        phones = get_phone_numbers()
        if isinstance(phones, list):
            print(f"✅ Found {len(phones)} phone number(s)")
            for p in phones[:3]:
                print(f"   - {p.get('number', 'N/A')}")
        else:
            print(f"Response: {phones}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n📊 Fetching assistants...")
    try:
        assistants = get_assistants()
        if isinstance(assistants, list):
            print(f"✅ Found {len(assistants)} assistant(s)")
            for a in assistants[:3]:
                print(f"   - {a.get('name', 'N/A')}")
        else:
            print(f"Response: {assistants}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*60 + "\n")
