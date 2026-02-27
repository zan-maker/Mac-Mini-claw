#!/usr/bin/env python3
"""
Kalshi API Explorer - Discover available endpoints and markets
"""

import requests
import json
import time
import jwt
from datetime import datetime
from cryptography.hazmat.primitives import serialization

# Kalshi API credentials
API_KEY_ID = "59b40b53-f282-4778-810f-012dc3eda27a"
PRIVATE_KEY_PEM = """-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAu/HdxpYAY3QpA2sK+2QEwXVMA+PhBlLl3sKoBypOlhWZl/0u
LlpoL4yFvkmmRP+FfVS7+rSRBRDs0f1+LxDt5yG45CCwSi2YIcU+mY6ji7DpT66/
JtpWBSR/Oz+yg+CzVGzaI8c0X8Pwxo62nc78IbxkjlqnXn+IM5etUQ99CxuEx93C
ryqehGVxsx5prGvTbT3PE6DpIXj+wtcMGUZhlW5xUWvmTQp5hkrzTclYsimFCXDo
BpuXDxcqgWydlO92UWwrXgAOo33qh2qx5xK9p1zQ7QijOafkTJ98OdqYWzdW5OOJ
0tAbd97wWjXjCQp9VjLx/ddj9/auAEGaGvUM3wIDAQABAoIBAALWzoDXdz4JXS0+
CrZtdlztxq4wXQ/ZZLuOuTcSfolp3h4bpvzwRK6jMsoDFs3oBj40b3qEC8TF0q4B
ZEyVtuJM8hwQGlmkgq3P6vgq3XGYxI19mEmf9rixKnLcrXesh0j5M/piYfooXZTC
RyPvIoPn8qTr3adhyc7ttaKJ11u5kgzITlyKTp29BPLh7Ru3n7S4meMT/t5Mycrv
Fp4wWhDbrXmTNz5kQqHp/eoeUsp12THReB34I6JnuVDq7OBsRzaji2FFMWGCChiV
O06pPPcho+XWi5f26qaXhDw80AIGG1zGNiMNZkZ4Xts/65hAEUvLkyPJO2AZ/5yG
BZPEN9ECgYEA7CAheXql6W35zo/NRzj46AASQwSY6MBDNmE/wlEjPIFGD1JH5moL
NUIWq45tG9W5CD06o0Fk1K7ZxDUWX3JUeO7pjpZquPC8WPWDbdpgdURkem0OV927
NsAJ2kPs7pba/NJznZoW069emITT8x+6MmU9WmHcs+bT3Ys1g0YvMSsCgYEAy8OS
GWgQC3GJdJ4tc703E604UbOFsCRFyoWQrkzMthdTvTZMpPdLixLpVa6/0RYyhB/S
eKH63q37RhFRH8pjOrDsoLTRKIXpfkYNkJ5l1oNlMepmh7yA8nXJIszNBJKuvaiG
9biVxPjyz+piwM39qZ6A/J+A2iFUiXg+vvd58R0CgYB6Bxzll+HYYhKAksaGsUXJ
OAg4BE81se7KUrXNqXrpUPGxB1fLFzCVpILsxB1VDj2iqWn9ZtVCKN63zKu0RfSr
zuR64Pdkfl0IKFF02y+QSvkWX/fSpu+Smuo8l3AB2YpwsB4566EyYuYjMjoK4nGq
i7GKXRrfCkKhssjD/+hxowKBgGJoUk/o3Q7Zx3vFxMfH0yiymKeEnwUhj38uoGA9
gQRUIcIYzk1BjX9eI8iYu9Tb9ouu3rQZ7pHKzrbZOCe1U9UNi0pV6Um72rd8V6LH
jQFbtey0es4FMPVoAzrGVCFoQfIgyQU1H0fgv0vAs+7PzTk07rCSy+UNAcneg9cw
p/jVAoGALOGAfTqE/D34Fyu2GYRW7LuZHNCqrLSks77AHdbnBiIe0z35n4sjNHUf
kHYVEYSrKagFTpjF4QPNuuLXSWj8xAHswtycypo35x1dOT7ADPQD9NaodntTD2Od
GiJfe18GHMaNptatp8FQYpro3l2YUP5AkvWVU5hmcqydaTetLkI=
-----END RSA PRIVATE KEY-----"""

def create_jwt_token():
    """Create JWT token for Kalshi API authentication"""
    try:
        private_key = serialization.load_pem_private_key(
            PRIVATE_KEY_PEM.encode('utf-8'),
            password=None
        )
        
        payload = {
            "iss": API_KEY_ID,
            "sub": API_KEY_ID,
            "aud": "https://api.kalshi.com",
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600,
            "scope": "read write"
        }
        
        token = jwt.encode(payload, private_key, algorithm="RS256")
        return token
        
    except Exception as e:
        print(f"Error creating JWT: {str(e)}")
        return None

def explore_api(base_url, headers):
    """Explore available API endpoints"""
    
    print(f"\n🔍 Exploring API at: {base_url}")
    
    # Common endpoints to try
    endpoints = [
        "/",
        "/v1/",
        "/v1/events",
        "/v1/markets",
        "/v1/trades",
        "/v1/orders",
        "/v1/portfolio",
        "/v1/account",
        "/v1/user",
        "/api/v1/events",
        "/api/v1/markets",
        "/events",
        "/markets"
    ]
    
    available_endpoints = []
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, headers=headers, timeout=10)
            
            print(f"  {endpoint}: {response.status_code}")
            
            if response.status_code == 200:
                available_endpoints.append(endpoint)
                
                # Try to get a sample of data
                try:
                    data = response.json()
                    if isinstance(data, list):
                        print(f"    Found {len(data)} items")
                    elif isinstance(data, dict):
                        keys = list(data.keys())[:5]
                        print(f"    Keys: {', '.join(keys)}...")
                except:
                    pass
                    
        except Exception as e:
            print(f"  {endpoint}: Error - {str(e)[:50]}")
    
    return available_endpoints

def get_events_data(base_url, headers):
    """Get events data from /v1/events endpoint"""
    
    try:
        response = requests.get(
            f"{base_url}/v1/events",
            headers=headers,
            params={"limit": 50},
            timeout=30
        )
        
        if response.status_code == 200:
            events_data = response.json()
            events = events_data.get('events', [])
            
            print(f"\n📅 Found {len(events)} events")
            
            # Look for CPI and Senate events
            cpi_events = []
            senate_events = []
            all_events = []
            
            for event in events:
                title = event.get('title', '').lower()
                event_id = event.get('id')
                
                event_info = {
                    'id': event_id,
                    'title': event.get('title', 'Unknown'),
                    'status': event.get('status', 'Unknown'),
                    'category': event.get('category', 'Unknown')
                }
                all_events.append(event_info)
                
                if 'cpi' in title or 'inflation' in title:
                    cpi_events.append(event_info)
                if 'senate' in title or 'election' in title:
                    senate_events.append(event_info)
            
            print(f"\n📊 CPI Events: {len(cpi_events)}")
            for event in cpi_events[:3]:
                print(f"  • {event['title']}")
                print(f"    ID: {event['id']}, Status: {event['status']}")
            
            print(f"\n🏛️ Senate Events: {len(senate_events)}")
            for event in senate_events[:3]:
                print(f"  • {event['title']}")
                print(f"    ID: {event['id']}, Status: {event['status']}")
            
            # Try to get markets for first few events
            print(f"\n🔍 Exploring markets for events...")
            
            sample_events = cpi_events[:2] + senate_events[:2]
            
            for event in sample_events:
                try:
                    markets_response = requests.get(
                        f"{base_url}/v1/events/{event['id']}/markets",
                        headers=headers,
                        timeout=30
                    )
                    
                    if markets_response.status_code == 200:
                        markets_data = markets_response.json()
                        markets = markets_data.get('markets', [])
                        
                        print(f"\n  Event: {event['title']}")
                        print(f"    Found {len(markets)} markets")
                        
                        for market in markets[:3]:  # Show first 3 markets
                            print(f"    • {market.get('title', 'Unknown')}")
                            if market.get('yes_price') and market.get('no_price'):
                                print(f"      YES: ${market.get('yes_price')} | NO: ${market.get('no_price')}")
                    else:
                        print(f"\n  Event {event['id']}: Markets endpoint status {markets_response.status_code}")
                        
                except Exception as e:
                    print(f"\n  Error getting markets for event {event['id']}: {str(e)}")
            
            return {
                'all_events': all_events,
                'cpi_events': cpi_events,
                'senate_events': senate_events,
                'total_events': len(events)
            }
            
        else:
            print(f"Events API error: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"Error getting events: {str(e)}")
    
    return {'all_events': [], 'cpi_events': [], 'senate_events': [], 'total_events': 0}

def main():
    """Main execution"""
    print("=" * 60)
    print("KALSHI API EXPLORER")
    print("=" * 60)
    
    # Create JWT token
    print("\n1. Creating authentication token...")
    token = create_jwt_token()
    
    if not token:
        print("✗ Failed to create authentication token")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    base_url = "https://api.elections.kalshi.com"
    
    # Explore API endpoints
    print(f"\n2. Exploring API endpoints at {base_url}...")
    available_endpoints = explore_api(base_url, headers)
    
    if available_endpoints:
        print(f"\n✓ Available endpoints: {', '.join(available_endpoints)}")
    else:
        print(f"\n✗ No standard endpoints found")
    
    # Get events data
    print(f"\n3. Getting events data...")
    events_data = get_events_data(base_url, headers)
    
    # Save results
    try:
        output_file = '/Users/cubiczan/.openclaw/workspace/kalshi-api-exploration.json'
        with open(output_file, 'w') as f:
            json.dump({
                'available_endpoints': available_endpoints,
                'events_data': events_data,
                'exploration_timestamp': datetime.now().isoformat(),
                'api_base_url': base_url
            }, f, indent=2)
        print(f"\n📁 Exploration results saved to: {output_file}")
    except Exception as e:
        print(f"\n⚠️ Could not save results: {str(e)}")
    
    # Recommendations based on findings
    print(f"\n" + "="*60)
    print("RECOMMENDATIONS")
    print("="*60)
    
    if events_data['total_events'] > 0:
        print(f"\nFound {events_data['total_events']} total events")
        print(f"CPI Events: {len(events_data['cpi_events'])}")
        print(f"Senate Events: {len(events_data['senate_events'])}")
        
        if events_data['cpi_events'] or events_data['senate_events']:
            print(f"\n✅ API is working! You can:")
            print(f"1. Browse events at {base_url}/v1/events")
            print(f"2. Get markets for specific events")
            print(f"3. Place trades via API")
        else:
            print(f"\n⚠️ No CPI or Senate events found")
            print(f"  2026 markets may not be available yet")
            print(f"  Try searching for current events")
    else:
        print(f"\n❌ No events found")
        print(f"  API might have different structure")
        print(f"  Or markets for 2026 don't exist yet")
    
    print(f"\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print(f"\n1. Check Kalshi website for current markets")
    print(f"2. Search for 'CPI' and 'Senate' on the platform")
    print(f"3. Share exact market names/tickers you find")
    print(f"4. I'll analyze and provide trade recommendations")

if __name__ == "__main__":
    main()