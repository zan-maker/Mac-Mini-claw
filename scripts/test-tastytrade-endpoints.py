#!/usr/bin/env python3
"""
Test TastyTrade API endpoints with JWT token
"""

import requests
import json

API_TOKEN = "eyJhbGciOiJFZERTQSIsInR5cCI6InJ0K2p3dCIsImtpZCI6Ik9UTUMzeThCTVB0Q3hxbHBSWUlod2N0UzY3aGdfd3hEM0NOYXdSX2lXanMiLCJqa3UiOiJodHRwczovL2ludGVyaW9yLWFwaS5hcjIudGFzdHl0cmFkZS5zeXN0ZW1zL29hdXRoL2p3a3MifQ.eyJpc3MiOiJodHRwczovL2FwaS50YXN0eXRyYWRlLmNvbSIsInN1YiI6IlViMTA4NzI0Yy0yNDRhLTRlZWUtYjc0NC1jMmYzMWNmYjBlY2QiLCJpYXQiOjE3NzIwNTM3NDAsImF1ZCI6IjBjN2I4ODk4LWEyZjEtNDliYi1hMjNkLTg0M2U0N2I2ODYzMSIsImdyYW50X2lkIjoiRzJlMjFlNjVmLTdhMjAtNDNiZi04MmUyLTY0YzkxOGFlMTlkYyIsInNjb3BlIjoicmVhZCB0cmFkZSBvcGVuaWQifQ.ieHeNMq49QwHCDoqNRhZmAfpc_qkd1MFRqnYze9TiDjuJZVGW4xkrcnXrNi6LHcvfXtyp-tBR-wBbdD44iX5Bw"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Try different TastyTrade API endpoints
endpoints = [
    "https://api.tastytrade.com/ws/api",
    "https://api.tastytrade.com/api",
    "https://api.tastytrade.com/oauth/api",
    "https://api.tastytrade.com/tastyworks/api",
    "https://api.tastytrade.com/tastyworks-api",
    "https://api.tastytrade.com/v1",
    "https://api.tastytrade.com/v1/accounts",
    "https://api.tastytrade.com/accounts",
    "https://api.tastytrade.com/session",
    "https://api.tastytrade.com/customer",
    "https://api.tastytrade.com/quote/SPY",
    "https://api.tastytrade.com/market-data/quotes/SPY"
]

print("Testing TastyTrade API endpoints...")
print("=" * 60)

for endpoint in endpoints:
    try:
        print(f"\nTesting: {endpoint}")
        response = requests.get(endpoint, headers=headers, timeout=10)
        
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"  ✅ SUCCESS!")
            try:
                data = response.json()
                print(f"  Response keys: {list(data.keys())[:5]}")
            except:
                print(f"  Response: {response.text[:100]}")
        elif response.status_code == 401:
            print(f"  ❌ Unauthorized (token invalid/expired)")
        elif response.status_code == 403:
            print(f"  ❌ Forbidden (no permission)")
        elif response.status_code == 404:
            print(f"  ❌ Not Found (wrong endpoint)")
        else:
            print(f"  Response: {response.text[:100]}")
            
    except requests.exceptions.ConnectionError:
        print(f"  ❌ Connection failed")
    except Exception as e:
        print(f"  Error: {str(e)[:50]}")

print("\n" + "=" * 60)
print("API TEST COMPLETE")

# Try the TastyTrade SDK approach
print("\n\nTrying TastyTrade SDK approach...")
print("=" * 60)

try:
    # Check if tastytrade-sdk is installed
    import subprocess
    import sys
    
    result = subprocess.run([sys.executable, "-c", "import tastytrade; print('SDK available')"], 
                          capture_output=True, text=True)
    
    if "SDK available" in result.stdout:
        print("✅ tastytrade-sdk is installed")
        
        # Try to use the SDK
        test_script = """
import tastytrade
import json

api_token = """ + json.dumps(API_TOKEN) + """

try:
    # Try different initialization methods
    print("Method 1: Direct token")
    session = tastytrade.Session(api_token=api_token)
    print(f"Session created: {session}")
    
    # Try to get accounts
    accounts = session.get_accounts()
    print(f"Accounts: {accounts}")
    
except Exception as e:
    print(f"Error: {e}")
    
    # Try alternative method
    print("\\nMethod 2: Alternative")
    try:
        from tastytrade import Tastytrade
        client = Tastytrade(api_token=api_token)
        print(f"Client created: {client}")
    except Exception as e2:
        print(f"Error 2: {e2}")
"""
        
        exec(test_script)
    else:
        print("❌ tastytrade-sdk not installed")
        print("Install with: pip install tastytrade-sdk")
        
except Exception as e:
    print(f"SDK test error: {str(e)}")