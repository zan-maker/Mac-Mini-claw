#!/usr/bin/env python3
"""
Test Nimbleway API integration
API Key: 5b98a2e870df43059dfe1c39a23468db2e63e4e830dc4902a23501bf22706a31
"""

import requests
import json

API_KEY = "5b98a2e870df43059dfe1c39a23468db2e63e4e830dc4902a23501bf22706a31"
BASE_URL = "https://api.nimbleway.com"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_endpoints():
    """Test various API endpoints"""
    endpoints = [
        "/v1/search",
        "/api/v1/search",
        "/search",
        "/v1/query",
        "/api/search",
        "/",
        "/health",
        "/status"
    ]
    
    for endpoint in endpoints:
        url = f"{BASE_URL}{endpoint}"
        print(f"\n🔍 Testing: {url}")
        
        # Try GET first
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   GET Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   Response: {response.text[:200]}...")
        except Exception as e:
            print(f"   GET Error: {e}")
        
        # Try POST with simple query
        try:
            payload = {"query": "test mining investors"}
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            print(f"   POST Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   Response: {response.text[:200]}...")
        except Exception as e:
            print(f"   POST Error: {e}")

def test_search_directly():
    """Test search with common patterns"""
    print("\n🎯 Testing search patterns...")
    
    # Pattern 1: Google-style search API
    test_urls = [
        "https://api.nimbleway.com/v1/search?q=mining+investors+canada",
        "https://api.nimbleway.com/api/v1/search?query=mining+investors+canada&num=5",
        "https://api.nimbleway.com/search?q=test",
        "https://api.nimbleway.com/v1/query",
    ]
    
    for url in test_urls:
        print(f"\n🔍 Testing URL: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Keys: {list(data.keys())}")
                if 'results' in data:
                    print(f"   Results: {len(data['results'])}")
        except Exception as e:
            print(f"   Error: {e}")

def check_account_info():
    """Check account/balance information"""
    print("\n💰 Checking account info...")
    
    account_endpoints = [
        "/v1/account",
        "/api/v1/account",
        "/account",
        "/v1/balance",
        "/api/v1/balance"
    ]
    
    for endpoint in account_endpoints:
        url = f"{BASE_URL}{endpoint}"
        print(f"\n🔍 Testing: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   Response: {response.text[:200]}...")
        except Exception as e:
            print(f"   Error: {e}")

if __name__ == "__main__":
    print("🚀 Testing Nimbleway API Integration")
    print(f"API Key: {API_KEY[:10]}...{API_KEY[-10:]}")
    print(f"Base URL: {BASE_URL}")
    
    test_endpoints()
    test_search_directly()
    check_account_info()
    
    print("\n📋 Summary:")
    print("If all tests fail, check:")
    print("1. API key validity")
    print("2. Correct base URL")
    print("3. API documentation at https://online.nimbleway.com/")
    print("4. Account status and credits")