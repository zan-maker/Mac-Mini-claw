#!/usr/bin/env python3
"""
Test various Bright Data API patterns
"""

import requests
import json

API_KEY = "ff572e99-0217-4d64-8ef2-768ff4fdd142"

# Different Bright Data API patterns
test_patterns = [
    # Pattern 1: Standard Bright Data API
    {
        "name": "Standard API",
        "url": "https://api.brightdata.com/account",
        "headers": {"Authorization": f"Bearer {API_KEY}"},
        "method": "GET"
    },
    
    # Pattern 2: With basic auth
    {
        "name": "Basic Auth",
        "url": "https://api.brightdata.com/account",
        "auth": ("user", API_KEY),
        "method": "GET"
    },
    
    # Pattern 3: Different base URL
    {
        "name": "Alternative URL",
        "url": "https://brightdata.com/api/account",
        "headers": {"Authorization": f"Bearer {API_KEY}"},
        "method": "GET"
    },
    
    # Pattern 4: Data collector API
    {
        "name": "Data Collector",
        "url": "https://api.brightdata.com/datasets",
        "headers": {"Authorization": f"Bearer {API_KEY}"},
        "method": "GET"
    },
    
    # Pattern 5: Proxy API
    {
        "name": "Proxy API",
        "url": "https://api.brightdata.com/proxy",
        "headers": {"Authorization": f"Bearer {API_KEY}"},
        "method": "GET"
    },
    
    # Pattern 6: With API key in params
    {
        "name": "API Key in Params",
        "url": f"https://api.brightdata.com/account?api_key={API_KEY}",
        "method": "GET"
    },
    
    # Pattern 7: Different authentication format
    {
        "name": "Custom Auth Header",
        "url": "https://api.brightdata.com/account",
        "headers": {"X-API-Key": API_KEY},
        "method": "GET"
    },
    
    # Pattern 8: Check if it's a Luminary API key
    {
        "name": "Luminary Test",
        "url": "https://luminary.brightdata.com/api/account",
        "headers": {"Authorization": f"Bearer {API_KEY}"},
        "method": "GET"
    }
]

def run_tests():
    print("🔍 Testing Bright Data API Patterns")
    print(f"API Key: {API_KEY[:10]}...{API_KEY[-10:]}")
    print("="*60)
    
    successful_tests = []
    
    for test in test_patterns:
        print(f"\n🧪 Test: {test['name']}")
        print(f"   URL: {test['url']}")
        
        try:
            if test['method'] == 'GET':
                kwargs = {
                    "url": test['url'],
                    "timeout": 10
                }
                
                if 'headers' in test:
                    kwargs['headers'] = test['headers']
                if 'auth' in test:
                    kwargs['auth'] = test['auth']
                
                response = requests.get(**kwargs)
            else:
                # For POST if needed
                pass
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ SUCCESS!")
                successful_tests.append(test)
                
                try:
                    data = response.json()
                    print(f"   Response: {json.dumps(data, indent=2)[:500]}...")
                except:
                    print(f"   Response: {response.text[:500]}...")
            elif response.status_code == 401:
                print(f"   🔐 Authentication failed")
            elif response.status_code == 403:
                print(f"   🚫 Forbidden")
            elif response.status_code == 404:
                print(f"   ❌ Endpoint not found")
            else:
                print(f"   ⚠️  Unexpected status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"   🔌 Connection failed")
        except requests.exceptions.Timeout:
            print(f"   ⏱️  Timeout")
        except Exception as e:
            print(f"   ❌ Error: {type(e).__name__}: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("📋 Test Summary")
    print("="*60)
    
    if successful_tests:
        print(f"✅ {len(successful_tests)} successful pattern(s):")
        for test in successful_tests:
            print(f"   - {test['name']}: {test['url']}")
    else:
        print("❌ No successful API patterns found")
        print("\n🔍 Next steps:")
        print("1. Check if API key is active in Bright Data dashboard")
        print("2. Look for correct API documentation")
        print("3. Try different authentication methods")
        print("4. Contact Bright Data support")
    
    return successful_tests

if __name__ == "__main__":
    run_tests()