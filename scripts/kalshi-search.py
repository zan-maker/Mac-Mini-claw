#!/usr/bin/env python3
"""
Kalshi API Search for CPI and Senate markets
Using provided API credentials
"""

import requests
import json
import base64
import time
import hashlib
import hmac
from datetime import datetime

# Kalshi API credentials from user
API_KEY_ID = "4dd243e0-5d05-4e63-841a-be980f08b43a"
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEApkd5dd4Kn6HZ/bx+cIdkw/gnVcD4jjrzIMgxAZGBzxwKUdHc
JXaEvTxxp5v4q6HnCPMCRXReTUTSTVOhsjnh7BxZmVQEdNJmobkfo1fbmUpuJ5sp
iGIdLFSquGisOVy1YY61GQ2LnGX0oHJAFj0dNzCzTR0vb9n3FDeyC+/7cghhq5yz
CRJysb2QG6h8IsDIuradLHSUOUYjPIkFrX4ZrfZt4NnQmSuUvUh5VaHDPrAtB7R5
Y6ZtVADe1JUCMRwitgdc6vqP845JeLydeskJ3gDZJFBG6rY5kSdsgilkIwi8fLJD
p+n6vgqdUi+RUeG5YP9c7nmaOmU3hZ08AFqaqwIDAQABAoIBAAFQICvnmHLhPszr
n53427lWbM0XDH9nBMN2ATkPcpR1lrlFrHTZRjwOTaFysFh+m0ntTU/KFvKKQBTf
O7AiF+Aa6zQ0PyLDBI9zXEYYbAH+XfdPGNlcWPmgI4b4QJ/lVQNTsqdjfX47Kd7Y
eBwU2HW2mzvZJqY99N8Cf5PrjbM9TXFchcDLqOR0G+PWSrrQ0tk/H1EtHTireL7P
4QzzjICMQcFrJ9U4sOdVXnpaxfc2Kl2ZyGeCF5bZgYKD4C8UB17/WGf8Swd5TAK9
2RC46KIv4hm95Mr7apqTmbT3iwSH+rddQMuiM7oFaf89GEg3xu+g/7NoSFAXgGLn
hAjrXdUCgYEAxm1hrEiqrB3r7FCHd88HmUBajW++FgpH4Y/pJF/nwvJletjsQ5Ib
G+t3u9iFadan8b1iPNqhggrVTm1i6PbfId4/1uY2fQ7ew3eCQnyIPiJMFrmZ9uvA
5r6q/OYBvDnOt1YZnZlcwl/me/GfJB5CKsiU1y5+N3opz1zR5jlmxCUCgYEA1oY5
fFRcDr7bHcKhG4Ynqp67wHCQszjKmpPUIy4gIcDhL4sQTUYf/iAWlY5M6tn+DWZx
5NT0i9cZFTdEjQG9Juu1BTyRHSZRSx48rVLbdN5TaU/BLa07R3Kpzo5tagngm12F
hjSkyXKZ2024fGHY3UwE8t/lwgpHiZjjmtFjwo8CgYBwvjOSBVPcKcAj7HmcTGif
3d3VoRkbQsom0nMAtPFlZf7c9yX/GqQGkBrfA56CTXHtO9L2iq7bybX7MtHRVnvf
rX0OaI2rLujJnTzI9CMhUrFy9BAUKU3YjZtvyGxR+3KF3wj87+exlXXLFLV8eyjT
UFapkQQsF2BsLuwgaJsIdQKBgQC9rgLILuMS2qhtgPjomE8caqvB9QXMogtqcAlj
bdZVYfD6E7C/UqDZFtBBPog+I6+hc5KC7dSojPENtEd1kjMIZeMyFSKOLqI0lDC8
ZAXNKQOBm1ZIp+JBQ15nV8Hgv4kMdr2oM4X85MqrgOX9fJq+2QeLJHNHhcVJIZkl
+7yEewKBgQC9Rpn+VDY89e3H9KuIdGjgI5fRKf3oUoF6uQUCYJcYVwmXS0Y5RYQq
YnHcgq5fOwa4jm2fTxSq3joh2DJ9r9BFoAKxqexJHcN7xCTha/gFp14M3l8F8fQc
Gg5V7OkM77+nPL/g7h7SM6LnKwo2VdW9OUOlJCIfUO2uugkG4dv8xw==
-----END RSA PRIVATE KEY-----"""

# Kalshi API endpoints
BASE_URL = "https://trading-api.kalshi.com"
API_VERSION = "v1"

def create_signature(method, path, body, timestamp):
    """Create HMAC signature for Kalshi API"""
    # Kalshi uses HMAC-SHA256 with specific format
    message = f"{method}\n{path}\n{timestamp}\n{body}"
    
    # Using the private key for HMAC (simplified - actual implementation may differ)
    # Note: Kalshi might use JWT or other auth, need to check their docs
    signature = hmac.new(
        PRIVATE_KEY.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return signature

def search_markets(query, category=None, limit=50):
    """Search for markets on Kalshi"""
    
    # Try to authenticate first
    headers = {
        "Authorization": f"Bearer {API_KEY_ID}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # First, try to get markets endpoint
    try:
        # Search for CPI markets
        print(f"Searching for markets with query: '{query}'")
        
        # Try different endpoints based on Kalshi API docs
        endpoints_to_try = [
            f"{BASE_URL}/{API_VERSION}/markets?query={query}",
            f"{BASE_URL}/{API_VERSION}/markets/search?q={query}",
            f"{BASE_URL}/{API_VERSION}/events?search={query}"
        ]
        
        for endpoint in endpoints_to_try:
            try:
                print(f"Trying endpoint: {endpoint}")
                response = requests.get(endpoint, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"Success! Found {len(data.get('markets', []))} markets")
                    return data
                else:
                    print(f"Endpoint failed with status {response.status_code}: {response.text[:200]}")
            except Exception as e:
                print(f"Error trying endpoint {endpoint}: {str(e)}")
                continue
        
        # If none worked, try a simpler approach
        print("\nTrying alternative approach...")
        
        # Common Kalshi market patterns
        cpi_patterns = [
            "CPI", "inflation", "consumer price index", "economic indicator"
        ]
        
        senate_patterns = [
            "senate", "election", "congress", "2026 election"
        ]
        
        all_results = []
        
        for pattern in cpi_patterns + senate_patterns:
            try:
                test_url = f"{BASE_URL}/{API_VERSION}/markets?limit={limit}"
                response = requests.get(test_url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    markets = response.json().get('markets', [])
                    
                    # Filter by query
                    filtered = [
                        m for m in markets 
                        if query.lower() in m.get('title', '').lower() 
                        or query.lower() in m.get('ticker', '').lower()
                    ]
                    
                    if filtered:
                        print(f"Found {len(filtered)} markets matching '{query}'")
                        all_results.extend(filtered)
                        
            except Exception as e:
                print(f"Error searching for pattern '{pattern}': {str(e)}")
                continue
        
        return {"markets": all_results[:limit]}
        
    except Exception as e:
        print(f"Error in search_markets: {str(e)}")
        return {"error": str(e), "markets": []}

def main():
    """Main execution"""
    print("=" * 60)
    print("KALSHI MARKET SEARCH")
    print("=" * 60)
    
    # Search for CPI markets
    print("\n1. Searching for CPI/Inflation markets...")
    cpi_results = search_markets("CPI")
    
    if cpi_results.get('markets'):
        print(f"\nFound {len(cpi_results['markets'])} CPI-related markets:")
        for i, market in enumerate(cpi_results['markets'][:10], 1):
            print(f"\n{i}. {market.get('title', 'Unknown')}")
            print(f"   Ticker: {market.get('ticker', 'N/A')}")
            print(f"   Status: {market.get('status', 'N/A')}")
            if 'yes_price' in market and 'no_price' in market:
                print(f"   YES: ${market.get('yes_price', 'N/A')} | NO: ${market.get('no_price', 'N/A')}")
    else:
        print("No CPI markets found or API access issue")
    
    # Search for Senate markets
    print("\n\n2. Searching for Senate election markets...")
    senate_results = search_markets("senate")
    
    if senate_results.get('markets'):
        print(f"\nFound {len(senate_results['markets'])} Senate-related markets:")
        for i, market in enumerate(senate_results['markets'][:15], 1):
            print(f"\n{i}. {market.get('title', 'Unknown')}")
            print(f"   Ticker: {market.get('ticker', 'N/A')}")
            print(f"   Status: {market.get('status', 'N/A')}")
            if 'yes_price' in market and 'no_price' in market:
                print(f"   YES: ${market.get('yes_price', 'N/A')} | NO: ${market.get('no_price', 'N/A')}")
    else:
        print("No Senate markets found or API access issue")
    
    # Search specifically for 2026
    print("\n\n3. Searching for 2026 election markets...")
    election_2026_results = search_markets("2026")
    
    if election_2026_results.get('markets'):
        print(f"\nFound {len(election_2026_results['markets'])} 2026-related markets:")
        for i, market in enumerate(election_2026_results['markets'][:10], 1):
            print(f"\n{i}. {market.get('title', 'Unknown')}")
            print(f"   Ticker: {market.get('ticker', 'N/A')}")
    
    print("\n" + "=" * 60)
    print("SEARCH COMPLETE")
    print("=" * 60)
    
    # Save results to file
    try:
        with open('/Users/cubiczan/.openclaw/workspace/kalshi-search-results.json', 'w') as f:
            json.dump({
                "cpi_markets": cpi_results.get('markets', []),
                "senate_markets": senate_results.get('markets', []),
                "election_2026_markets": election_2026_results.get('markets', []),
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
        print("\nResults saved to: kalshi-search-results.json")
    except Exception as e:
        print(f"\nCould not save results: {str(e)}")

if __name__ == "__main__":
    main()
