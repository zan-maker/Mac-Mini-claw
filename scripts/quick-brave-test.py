#!/usr/bin/env python3
"""
Quick test of Brave Search API key
"""

import requests
import json

API_KEY = "BSA4VYA3FjSPQmTjZeKjsq5CqWvFy2u"
url = "https://api.search.brave.com/res/v1/web/search"

headers = {
    "Accept": "application/json",
    "X-Subscription-Token": API_KEY
}

params = {
    "q": "test search",
    "count": 2
}

print("Testing Brave Search API key...")
print(f"Key: {API_KEY}")

try:
    response = requests.get(url, headers=headers, params=params, timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ SUCCESS! API key works!")
        print(f"Found {len(data.get('web', {}).get('results', []))} results")
    elif response.status_code == 401:
        print("❌ 401 Unauthorized - Invalid API key")
        print(f"Response: {response.text[:200]}")
    elif response.status_code == 429:
        print("⚠️ 429 Rate Limited - Still hitting limits")
        print(f"Response: {response.text[:200]}")
    else:
        print(f"❌ Error {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")