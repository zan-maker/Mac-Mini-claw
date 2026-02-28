#!/usr/bin/env python3
"""Test Tomba API with proper authentication"""

import requests
import json

def test_tomba_auth():
    """Test Tomba authentication"""
    print("🔑 Testing Tomba API Authentication...")
    
    # Tomba requires BOTH key and secret
    api_key = "ta_hsrcgwy0fwj29bbxm0ar3dns0nc6e5p2151pg"
    api_secret = None  # We need the secret!
    
    # Test 1: Try with just key (might fail)
    print("\n1️⃣ Testing with just API key...")
    headers = {
        "X-Tomba-Key": api_key,
        "Content-Type": "application/json",
        "User-Agent": "OpenClaw/1.0"
    }
    
    try:
        # First test the /me endpoint to check authentication
        url = "https://api.tomba.io/v1/me"
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS! Authentication working")
            print(f"   Plan: {data.get('data', {}).get('plan', {}).get('name', 'unknown')}")
            print(f"   Credits: {data.get('data', {}).get('credits', {}).get('remaining', 0)}")
            return True
        else:
            print(f"   ❌ FAILED: {response.text[:100]}")
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Test 2: Try domain search (might work without secret for some endpoints)
    print("\n2️⃣ Testing domain search...")
    try:
        url = "https://api.tomba.io/v1/domain-search"
        params = {
            "domain": "openai.com",
            "limit": 3
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS! Domain search working")
            print(f"   Emails found: {len(data.get('data', {}).get('emails', []))}")
            
            if data.get("data", {}).get("emails"):
                for i, email in enumerate(data["data"]["emails"][:3]):
                    print(f"   {i+1}. {email.get('email', 'No email')}")
            
            return True
        else:
            print(f"   ❌ FAILED: {response.text[:100]}")
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Test 3: Check if we need secret
    print("\n3️⃣ Checking documentation...")
    print("   According to Tomba docs:")
    print("   - Some endpoints require ONLY X-Tomba-Key")
    print("   - Some endpoints require BOTH X-Tomba-Key AND X-Tomba-Secret")
    print("   - Free tier: 50 verifications/month")
    print("   - Need to check dashboard for secret key")
    
    return False

def check_tomba_dashboard():
    """Instructions to check Tomba dashboard"""
    print("\n📋 Steps to get Tomba working:")
    print("   1. Go to https://app.tomba.io/dashboard")
    print("   2. Login with your account")
    print("   3. Go to Settings → API Keys")
    print("   4. You should see:")
    print("      - API Key: ta_xxxxxxxxxxxxxxxx")
    print("      - Secret Key: ts_xxxxxxxxxxxxxxxx")
    print("   5. Copy BOTH keys")
    print("   6. Update the integration with both keys")

def main():
    print("🧪 Tomba API Authentication Test")
    print("="*60)
    
    success = test_tomba_auth()
    
    print("\n" + "="*60)
    
    if success:
        print("✅ Tomba API is working with just the key!")
        print("\n🎯 Ready for email finding:")
        print("   - Domain search: Find emails for companies")
        print("   - Email verification: Validate email addresses")
        print("   - Lead enrichment: Get company information")
    else:
        print("⚠️  Tomba API needs attention")
        check_tomba_dashboard()
        
        print("\n🔧 Alternative options:")
        print("   1. Use Hunter.io (50 searches/month free)")
        print("   2. Use FindThatLead (100 searches/month free)")
        print("   3. Use EmailHippo (100 verifications/month free)")
        print("   4. Use APILayer's email validation APIs")

if __name__ == "__main__":
    main()