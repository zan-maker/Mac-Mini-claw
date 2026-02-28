#!/usr/bin/env python3
"""Quick test of NewsAPI and Tomba API keys"""

import requests
import json
from datetime import datetime

def test_newsapi():
    """Test NewsAPI directly"""
    print("📰 Testing NewsAPI...")
    
    api_key = "4eb2186b017a49c38d6f6ded502dd55b"
    url = "https://newsapi.org/v2/top-headlines"
    
    params = {
        "category": "business",
        "pageSize": 3,
        "country": "us",
        "apiKey": api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS! {data.get('totalResults', 0)} articles found")
            
            if data.get("articles"):
                for i, article in enumerate(data["articles"][:2]):
                    print(f"   {i+1}. {article.get('title', 'No title')[:60]}...")
            
            return True
        else:
            print(f"   ❌ FAILED: {response.text[:100]}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def test_tomba():
    """Test Tomba directly"""
    print("\n📧 Testing Tomba Email Finder...")
    
    api_key = "ta_hsrcgwy0fwj29bbxm0ar3dns0nc6e5p2151pg"
    url = "https://api.tomba.io/v1/domain-search"
    
    params = {
        "domain": "openai.com"
    }
    
    headers = {
        "X-Tomba-Key": api_key,
        "User-Agent": "OpenClaw/1.0"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS! Response received")
            
            # Check if we have data
            if data.get("data") and data["data"].get("emails"):
                emails = data["data"]["emails"]
                print(f"   Found {len(emails)} emails")
                
                for i, email in enumerate(emails[:3]):
                    print(f"   {i+1}. {email.get('email', 'No email')} - {email.get('first_name', '')} {email.get('last_name', '')}")
            else:
                print(f"   ⚠️  No emails found (might be rate limited or domain protected)")
            
            return True
        else:
            print(f"   ❌ FAILED: {response.text[:100]}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def test_alphavantage():
    """Test Alpha Vantage (already working)"""
    print("\n💰 Testing Alpha Vantage...")
    
    api_key = "T0Z2YW467F7PNA9Z"
    url = "https://www.alphavantage.co/query"
    
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": "AAPL",
        "apikey": api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            quote = data.get("Global Quote", {})
            
            if quote:
                price = quote.get("05. price", "0")
                print(f"   ✅ SUCCESS! AAPL price: ${price}")
                return True
            else:
                print(f"   ⚠️  No quote data (might be rate limited)")
                return False
        else:
            print(f"   ❌ FAILED: {response.text[:100]}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def main():
    print("🧪 Quick API Key Test")
    print("="*60)
    
    results = {
        "NewsAPI": test_newsapi(),
        "Tomba": test_tomba(),
        "Alpha Vantage": test_alphavantage()
    }
    
    print("\n" + "="*60)
    print("📊 FINAL RESULTS:")
    print("="*60)
    
    for api, success in results.items():
        status = "✅ WORKING" if success else "❌ NEEDS ATTENTION"
        print(f"   {api}: {status}")
    
    print("\n" + "="*60)
    
    working_apis = sum(1 for success in results.values() if success)
    total_apis = len(results)
    
    print(f"   {working_apis}/{total_apis} APIs are working")
    
    if working_apis == total_apis:
        print("\n🎉 ALL APIS ARE WORKING PERFECTLY!")
    elif working_apis >= 2:
        print(f"\n👍 {working_apis} out of {total_apis} APIs are working")
    else:
        print("\n⚠️  Need to check API configurations")
    
    print("\n🔧 Next steps:")
    if results["NewsAPI"]:
        print("   - NewsAPI ready for market sentiment analysis")
    if results["Tomba"]:
        print("   - Tomba ready for B2B email finding")
    if results["Alpha Vantage"]:
        print("   - Alpha Vantage ready for stock analysis")

if __name__ == "__main__":
    main()