#!/usr/bin/env python3
"""
Kalshi API Search - Updated for new API endpoint
"""

import requests
import json
from datetime import datetime

# New API endpoint from error message
BASE_URL = "https://api.elections.kalshi.com"
API_VERSION = "v1"

# Try with the API key as Bearer token
API_KEY_ID = "4dd243e0-5d05-4e63-841a-be980f08b43a"

def search_kalshi_markets():
    """Search Kalshi markets using the new API"""
    
    headers = {
        "Authorization": f"Bearer {API_KEY_ID}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    print("Testing Kalshi API connection...")
    
    # Try to get user info first to test auth
    try:
        user_response = requests.get(
            f"{BASE_URL}/{API_VERSION}/user",
            headers=headers,
            timeout=30
        )
        print(f"User API status: {user_response.status_code}")
        if user_response.status_code == 200:
            print("✓ Authentication successful!")
            user_data = user_response.json()
            print(f"User: {user_data.get('email', 'N/A')}")
            print(f"Balance: ${user_data.get('balance', {}).get('cash_balance_cents', 0)/100:.2f}")
        else:
            print(f"User API error: {user_response.text[:200]}")
    except Exception as e:
        print(f"User API error: {str(e)}")
    
    print("\n" + "="*60)
    print("SEARCHING FOR MARKETS")
    print("="*60)
    
    # Try different search approaches
    search_patterns = [
        ("CPI/Inflation", ["CPI", "inflation", "consumer price"]),
        ("Senate Elections", ["senate", "senator", "congress"]),
        ("2026 Elections", ["2026", "election 2026"]),
        ("Economic Indicators", ["economic", "indicator", "data release"])
    ]
    
    all_markets = []
    
    for category, patterns in search_patterns:
        print(f"\n📊 Searching for: {category}")
        
        for pattern in patterns:
            try:
                # Try events endpoint
                events_url = f"{BASE_URL}/{API_VERSION}/events"
                params = {"limit": 50}
                
                response = requests.get(
                    events_url,
                    headers=headers,
                    params=params,
                    timeout=30
                )
                
                if response.status_code == 200:
                    events = response.json().get('events', [])
                    
                    # Filter events by pattern
                    filtered_events = [
                        e for e in events
                        if pattern.lower() in e.get('title', '').lower()
                        or pattern.lower() in e.get('ticker', '').lower()
                    ]
                    
                    if filtered_events:
                        print(f"  Found {len(filtered_events)} events with '{pattern}'")
                        
                        # Get markets for each event
                        for event in filtered_events[:5]:  # Limit to 5 events
                            event_id = event.get('id')
                            event_title = event.get('title', 'Unknown')
                            
                            try:
                                markets_url = f"{BASE_URL}/{API_VERSION}/events/{event_id}/markets"
                                markets_response = requests.get(
                                    markets_url,
                                    headers=headers,
                                    timeout=30
                                )
                                
                                if markets_response.status_code == 200:
                                    markets = markets_response.json().get('markets', [])
                                    print(f"    Event: {event_title} - {len(markets)} markets")
                                    
                                    for market in markets[:3]:  # Show first 3 markets
                                        market_info = {
                                            'category': category,
                                            'event_title': event_title,
                                            'market_title': market.get('title', 'Unknown'),
                                            'ticker': market.get('ticker', 'N/A'),
                                            'status': market.get('status', 'N/A'),
                                            'yes_price': market.get('yes_price', 'N/A'),
                                            'no_price': market.get('no_price', 'N/A'),
                                            'volume': market.get('volume', 'N/A')
                                        }
                                        all_markets.append(market_info)
                                        
                                        # Print market details
                                        print(f"      • {market.get('title', 'Unknown')}")
                                        if market.get('yes_price') and market.get('no_price'):
                                            print(f"        YES: ${market.get('yes_price')} | NO: ${market.get('no_price')}")
                                
                            except Exception as e:
                                print(f"    Error getting markets for event: {str(e)}")
                                continue
                    
                else:
                    print(f"  Events API error for '{pattern}': {response.status_code}")
                    
            except Exception as e:
                print(f"  Error searching '{pattern}': {str(e)}")
                continue
    
    # Try direct markets endpoint
    print("\n🔍 Trying direct markets search...")
    try:
        markets_url = f"{BASE_URL}/{API_VERSION}/markets"
        params = {"limit": 100, "status": "open"}
        
        response = requests.get(markets_url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            markets = response.json().get('markets', [])
            print(f"Found {len(markets)} total markets")
            
            # Look for CPI and Senate markets
            cpi_markets = [m for m in markets if 'CPI' in m.get('title', '').upper()]
            senate_markets = [m for m in markets if 'senate' in m.get('title', '').lower()]
            
            print(f"  CPI markets: {len(cpi_markets)}")
            print(f"  Senate markets: {len(senate_markets)}")
            
            # Add to all_markets
            for market in cpi_markets + senate_markets:
                market_info = {
                    'category': 'CPI' if 'CPI' in market.get('title', '').upper() else 'Senate',
                    'market_title': market.get('title', 'Unknown'),
                    'ticker': market.get('ticker', 'N/A'),
                    'status': market.get('status', 'N/A'),
                    'yes_price': market.get('yes_price', 'N/A'),
                    'no_price': market.get('no_price', 'N/A'),
                    'volume': market.get('volume', 'N/A')
                }
                all_markets.append(market_info)
                
        else:
            print(f"Markets API error: {response.status_code}")
            
    except Exception as e:
        print(f"Direct markets search error: {str(e)}")
    
    return all_markets

def main():
    """Main execution"""
    print("=" * 60)
    print("KALSHI MARKET SEARCH - UPDATED API")
    print("=" * 60)
    
    markets = search_kalshi_markets()
    
    print("\n" + "=" * 60)
    print("SEARCH RESULTS SUMMARY")
    print("=" * 60)
    
    if markets:
        # Group by category
        categories = {}
        for market in markets:
            cat = market['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(market)
        
        for category, cat_markets in categories.items():
            print(f"\n{category.upper()} MARKETS ({len(cat_markets)}):")
            print("-" * 40)
            
            for i, market in enumerate(cat_markets[:10], 1):  # Show first 10
                print(f"\n{i}. {market['market_title']}")
                print(f"   Ticker: {market['ticker']}")
                print(f"   Status: {market['status']}")
                if market['yes_price'] != 'N/A' and market['no_price'] != 'N/A':
                    print(f"   YES: ${market['yes_price']} | NO: ${market['no_price']}")
                if market.get('event_title'):
                    print(f"   Event: {market['event_title']}")
    else:
        print("\nNo markets found. Possible issues:")
        print("1. API key may need different authentication method")
        print("2. Markets may not exist yet for 2026")
        print("3. API endpoint may require different parameters")
    
    # Save results
    try:
        output_file = '/Users/cubiczan/.openclaw/workspace/kalshi-markets-found.json'
        with open(output_file, 'w') as f:
            json.dump({
                "markets": markets,
                "search_timestamp": datetime.now().isoformat(),
                "total_markets_found": len(markets)
            }, f, indent=2)
        print(f"\n\nResults saved to: {output_file}")
    except Exception as e:
        print(f"\nError saving results: {str(e)}")
    
    print("\n" + "=" * 60)
    print("RECOMMENDED NEXT STEPS")
    print("=" * 60)
    print("\n1. Check Kalshi website directly for current markets")
    print("2. Verify API authentication method (may need JWT)")
    print("3. Search for specific tickers on Kalshi platform")
    print("4. Check if 2026 markets are available yet")

if __name__ == "__main__":
    main()
