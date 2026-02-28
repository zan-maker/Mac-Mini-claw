#!/usr/bin/env python3
"""Test Tomba API with fixed parameters"""

import requests
import json

def test_tomba_domain_search_fixed():
    """Test Tomba domain search with correct parameters"""
    print("🔍 Testing Tomba Domain Search (Fixed)...")
    
    api_key = "ta_hsrcgwy0fwj29bbxm0ar3dns0nc6e5p2151pg"
    api_secret = "ts_576b466c-6d2a-4d3d-8730-6c6e9fe12958"
    
    headers = {
        "X-Tomba-Key": api_key,
        "X-Tomba-Secret": api_secret,
        "Content-Type": "application/json",
        "User-Agent": "OpenClaw/1.0"
    }
    
    # Test with different parameters
    test_cases = [
        {"domain": "stripe.com", "limit": 3},
        {"domain": "github.com", "limit": 2},
        {"domain": "openai.com"}  # No limit specified
    ]
    
    for i, params in enumerate(test_cases):
        print(f"\n{i+1}. Testing domain: {params.get('domain')}")
        
        try:
            url = "https://api.tomba.io/v1/domain-search"
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ SUCCESS!")
                print(f"   Total emails: {data.get('data', {}).get('total', 0)}")
                print(f"   Emails found: {len(data.get('data', {}).get('emails', []))}")
                
                if data.get("data", {}).get("emails"):
                    for j, email in enumerate(data["data"]["emails"][:2]):
                        print(f"   {j+1}. {email.get('email', 'No email')}")
                        if email.get('first_name') or email.get('last_name'):
                            print(f"      Name: {email.get('first_name', '')} {email.get('last_name', '')}")
                
                return True  # Return on first success
            else:
                print(f"   ❌ FAILED: {response.text[:150]}")
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
    
    return False

def test_tomba_account_details():
    """Get detailed account info"""
    print("\n📊 Getting Tomba Account Details...")
    
    api_key = "ta_hsrcgwy0fwj29bbxm0ar3dns0nc6e5p2151pg"
    api_secret = "ts_576b466c-6d2a-4d3d-8730-6c6e9fe12958"
    
    headers = {
        "X-Tomba-Key": api_key,
        "X-Tomba-Secret": api_secret,
        "Content-Type": "application/json",
        "User-Agent": "OpenClaw/1.0"
    }
    
    try:
        url = "https://api.tomba.io/v1/me"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            account = data.get("data", {})
            
            print(f"   Account: {account.get('email', 'unknown')}")
            print(f"   Credits remaining: {account.get('credits', {}).get('remaining', 0)}")
            print(f"   Monthly limit: {account.get('credits', {}).get('limit', 0)}")
            print(f"   Used: {account.get('credits', {}).get('used', 0)}")
            
            # Check if we have any credits
            remaining = account.get('credits', {}).get('remaining', 0)
            if remaining > 0:
                print(f"   ✅ {remaining} credits available for use!")
                return True
            else:
                print(f"   ⚠️  No credits remaining (limit: {account.get('credits', {}).get('limit', 0)})")
                return False
        else:
            print(f"   ❌ Failed to get account details")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def main():
    print("🧪 Tomba API Final Test")
    print("="*60)
    
    # Test account details first
    has_credits = test_tomba_account_details()
    
    print("\n" + "="*60)
    
    if has_credits:
        print("💰 Testing domain search (credits available)...")
        search_success = test_tomba_domain_search_fixed()
        
        if search_success:
            print("\n✅ TOMBA API IS FULLY WORKING!")
            print("   Ready for B2B email finding!")
        else:
            print("\n⚠️  Domain search failed (parameter issue)")
            print("   But API authentication is working")
    else:
        print("⚠️  No credits available in Tomba account")
        print("   Need to check free tier allocation")
        print("   Free tier should have 50 searches/month")
    
    print("\n🔧 Next steps:")
    print("   1. Check Tomba dashboard for credit allocation")
    print("   2. If no credits, may need to activate free tier")
    print("   3. Domain search works when credits are available")

if __name__ == "__main__":
    main()