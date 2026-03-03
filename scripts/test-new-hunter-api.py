#!/usr/bin/env python3
"""
Test Hunter.io API with new API key
"""

import requests
import json

API_KEY = "e341bb9af29f1da98190364caafb01a6b38e8e1c"

def test_account_info():
    """Test getting account information"""
    url = "https://api.hunter.io/v2/account"
    params = {"api_key": API_KEY}
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        print("✅ Hunter.io API Key Test Successful!")
        print(f"API Key: {API_KEY[:8]}...{API_KEY[-8:]}")
        print()
        print("Account Information:")
        print(f"  Email: {data.get('data', {}).get('email', 'N/A')}")
        print(f"  Plan: {data.get('data', {}).get('plan_name', 'N/A')}")
        print(f"  Credits: {data.get('data', {}).get('calls', {}).get('available', 'N/A')}")
        print(f"  Reset Date: {data.get('data', {}).get('reset_date', 'N/A')}")
        print()
        print("API Key is valid and ready to use!")
        
        return True
    except Exception as e:
        print(f"❌ API Key Test Failed: {e}")
        print(f"API Key: {API_KEY}")
        print("Please check the API key and try again.")
        return False

def test_domain_search():
    """Test domain search functionality"""
    url = "https://api.hunter.io/v2/domain-search"
    params = {
        "domain": "google.com",
        "api_key": API_KEY,
        "limit": 1
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data.get('data'):
            print("✅ Domain Search Test Successful!")
            print(f"Domain: google.com")
            print(f"Emails found: {data.get('meta', {}).get('results', 0)}")
            return True
        else:
            print("⚠️ Domain search returned no data")
            return False
    except Exception as e:
        print(f"❌ Domain Search Test Failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("HUNTER.IO API KEY TEST")
    print("=" * 60)
    print()
    
    # Test account info
    if test_account_info():
        # Test domain search
        test_domain_search()
    
    print()
    print("=" * 60)
    print("Test Complete")
    print("=" * 60)