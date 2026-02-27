#!/usr/bin/env python3
"""
Kalshi API Authentication and Trading
Using RSA private key for JWT authentication
"""

import requests
import json
import time
import jwt
import base64
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization

# Kalshi API credentials
API_KEY_ID = "4dd243e0-5d05-4e63-841a-be980f08b43a"
PRIVATE_KEY_PEM = """-----BEGIN RSA PRIVATE KEY-----
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

def create_jwt_token():
    """Create JWT token for Kalshi API authentication"""
    try:
        # Load private key
        private_key = serialization.load_pem_private_key(
            PRIVATE_KEY_PEM.encode('utf-8'),
            password=None
        )
        
        # Create JWT payload
        payload = {
            "iss": API_KEY_ID,
            "sub": API_KEY_ID,
            "aud": "https://api.kalshi.com",
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600,  # 1 hour expiration
            "scope": "read write"
        }
        
        # Create JWT token
        token = jwt.encode(
            payload,
            private_key,
            algorithm="RS256"
        )
        
        print("✓ JWT token created successfully")
        return token
        
    except Exception as e:
        print(f"✗ Error creating JWT token: {str(e)}")
        return None

def test_api_connection(token):
    """Test API connection with JWT token"""
    
    # Try different base URLs
    base_urls = [
        "https://api.kalshi.com",
        "https://api.elections.kalshi.com",
        "https://trading-api.kalshi.com"
    ]
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    for base_url in base_urls:
        print(f"\nTesting connection to: {base_url}")
        
        # Try user endpoint
        try:
            response = requests.get(
                f"{base_url}/v1/user",
                headers=headers,
                timeout=30
            )
            
            print(f"  User endpoint: {response.status_code}")
            if response.status_code == 200:
                user_data = response.json()
                print(f"  ✓ Authentication successful!")
                print(f"  User email: {user_data.get('email', 'N/A')}")
                print(f"  Balance: ${user_data.get('balance', {}).get('cash_balance_cents', 0)/100:.2f}")
                return base_url, headers
            else:
                print(f"  Response: {response.text[:200]}")
                
        except Exception as e:
            print(f"  Error: {str(e)}")
    
    return None, None

def search_markets(base_url, headers, query=None):
    """Search for markets"""
    
    print(f"\n🔍 Searching for markets...")
    
    # Try events endpoint
    try:
        events_response = requests.get(
            f"{base_url}/v1/events",
            headers=headers,
            params={"limit": 100},
            timeout=30
        )
        
        if events_response.status_code == 200:
            events = events_response.json().get('events', [])
            print(f"Found {len(events)} events")
            
            # Filter for CPI and Senate events
            cpi_events = []
            senate_events = []
            
            for event in events:
                title = event.get('title', '').lower()
                if 'cpi' in title or 'inflation' in title:
                    cpi_events.append(event)
                if 'senate' in title or 'election' in title:
                    senate_events.append(event)
            
            print(f"  CPI/Inflation events: {len(cpi_events)}")
            print(f"  Senate/Election events: {len(senate_events)}")
            
            # Get markets for relevant events
            all_markets = []
            
            # Check CPI events
            for event in cpi_events[:5]:  # Check first 5
                event_id = event.get('id')
                print(f"\n  CPI Event: {event.get('title')}")
                
                markets_response = requests.get(
                    f"{base_url}/v1/events/{event_id}/markets",
                    headers=headers,
                    timeout=30
                )
                
                if markets_response.status_code == 200:
                    markets = markets_response.json().get('markets', [])
                    for market in markets:
                        market_info = {
                            'type': 'CPI',
                            'event_title': event.get('title'),
                            'market_title': market.get('title'),
                            'ticker': market.get('ticker'),
                            'yes_price': market.get('yes_price'),
                            'no_price': market.get('no_price'),
                            'status': market.get('status')
                        }
                        all_markets.append(market_info)
                        print(f"    Market: {market.get('title')} - YES: ${market.get('yes_price')} | NO: ${market.get('no_price')}")
            
            # Check Senate events
            for event in senate_events[:5]:  # Check first 5
                event_id = event.get('id')
                print(f"\n  Senate Event: {event.get('title')}")
                
                markets_response = requests.get(
                    f"{base_url}/v1/events/{event_id}/markets",
                    headers=headers,
                    timeout=30
                )
                
                if markets_response.status_code == 200:
                    markets = markets_response.json().get('markets', [])
                    for market in markets:
                        market_info = {
                            'type': 'SENATE',
                            'event_title': event.get('title'),
                            'market_title': market.get('title'),
                            'ticker': market.get('ticker'),
                            'yes_price': market.get('yes_price'),
                            'no_price': market.get('no_price'),
                            'status': market.get('status')
                        }
                        all_markets.append(market_info)
                        print(f"    Market: {market.get('title')} - YES: ${market.get('yes_price')} | NO: ${market.get('no_price')}")
            
            return all_markets
            
        else:
            print(f"Events API error: {events_response.status_code}")
            print(f"Response: {events_response.text[:200]}")
            
    except Exception as e:
        print(f"Error searching markets: {str(e)}")
    
    return []

def get_account_balance(base_url, headers):
    """Get account balance and positions"""
    
    try:
        # Get account balance
        balance_response = requests.get(
            f"{base_url}/v1/user/balance",
            headers=headers,
            timeout=30
        )
        
        if balance_response.status_code == 200:
            balance_data = balance_response.json()
            cash = balance_data.get('cash_balance_cents', 0) / 100
            print(f"\n💰 Account Balance: ${cash:.2f}")
            return cash
        else:
            print(f"Balance API error: {balance_response.status_code}")
            
    except Exception as e:
        print(f"Error getting balance: {str(e)}")
    
    return 0

def main():
    """Main execution"""
    print("=" * 60)
    print("KALSHI API TRADING SYSTEM")
    print("=" * 60)
    
    # Step 1: Create JWT token
    print("\n1. Creating authentication token...")
    token = create_jwt_token()
    
    if not token:
        print("✗ Failed to create authentication token")
        return
    
    # Step 2: Test API connection
    print("\n2. Testing API connection...")
    base_url, headers = test_api_connection(token)
    
    if not base_url:
        print("✗ Failed to connect to Kalshi API")
        print("\nPossible solutions:")
        print("1. Check if API key is still valid")
        print("2. Check Kalshi API documentation for changes")
        print("3. Try using the web interface directly")
        return
    
    print(f"\n✓ Connected to: {base_url}")
    
    # Step 3: Get account balance
    print("\n3. Checking account balance...")
    balance = get_account_balance(base_url, headers)
    
    # Step 4: Search for markets
    print("\n4. Searching for CPI and Senate markets...")
    markets = search_markets(base_url, headers)
    
    # Step 5: Analyze and recommend trades
    print("\n5. Analyzing markets for trade opportunities...")
    
    if markets:
        print(f"\nFound {len(markets)} relevant markets:")
        
        # Group by type
        cpi_markets = [m for m in markets if m['type'] == 'CPI']
        senate_markets = [m for m in markets if m['type'] == 'SENATE']
        
        print(f"\n📊 CPI Markets ({len(cpi_markets)}):")
        for market in cpi_markets[:3]:  # Show first 3
            print(f"  • {market['market_title']}")
            print(f"    Ticker: {market['ticker']}")
            if market['yes_price'] and market['no_price']:
                print(f"    YES: ${market['yes_price']} | NO: ${market['no_price']}")
        
        print(f"\n🏛️ Senate Markets ({len(senate_markets)}):")
        for market in senate_markets[:3]:  # Show first 3
            print(f"  • {market['market_title']}")
            print(f"    Ticker: {market['ticker']}")
            if market['yes_price'] and market['no_price']:
                print(f"    YES: ${market['yes_price']} | NO: ${market['no_price']}")
        
        # Save market data
        try:
            with open('/Users/cubiczan/.openclaw/workspace/kalshi-market-data.json', 'w') as f:
                json.dump({
                    'markets': markets,
                    'balance': balance,
                    'timestamp': datetime.now().isoformat()
                }, f, indent=2)
            print(f"\n📁 Market data saved to: kalshi-market-data.json")
        except Exception as e:
            print(f"\n⚠️ Could not save market data: {str(e)}")
        
        # Generate trade recommendations
        print("\n" + "=" * 60)
        print("TRADE RECOMMENDATIONS")
        print("=" * 60)
        
        if balance > 0:
            print(f"\nBased on your balance of ${balance:.2f}, here are recommendations:")
            
            # CPI trade logic
            if cpi_markets:
                print(f"\n📈 CPI Trade Opportunity:")
                market = cpi_markets[0]  # Use first CPI market
                yes_price = float(market.get('yes_price', 0.5))
                no_price = float(market.get('no_price', 0.5))
                
                # Simple recommendation logic
                if yes_price < 0.45:
                    print(f"  Action: BUY YES on {market['ticker']}")
                    print(f"  Price: ${yes_price} (market thinks {yes_price*100:.1f}% probability)")
                    print(f"  Position: ${min(100, balance*0.5):.2f}")
                    print(f"  Edge: Good value if true probability > {(yes_price*100)+4:.1f}%")
                elif no_price < 0.45:
                    print(f"  Action: BUY NO on {market['ticker']}")
                    print(f"  Price: ${no_price} (market thinks {no_price*100:.1f}% probability)")
                    print(f"  Position: ${min(100, balance*0.5):.2f}")
                    print(f"  Edge: Good value if true probability > {(no_price*100)+4:.1f}%")
                else:
                    print(f"  No clear edge found at current prices")
            
            # Senate trade logic
            if senate_markets:
                print(f"\n🏛️ Senate Trade Opportunities:")
                # Find underdog candidates (low price)
                underdogs = []
                for market in senate_markets:
                    price = float(market.get('yes_price', 1.0))
                    if price < 0.10:  # Under 10 cents
                        underdogs.append((market, price))
                
                if underdogs:
                    print(f"  Found {len(underdogs)} underdog candidates (<$0.10)")
                    for i, (market, price) in enumerate(underdogs[:4], 1):
                        print(f"  {i}. {market['market_title']}")
                        print(f"     Price: ${price:.3f}")
                        print(f"     Position: $5.00")
                    
                    print(f"\n  Total Senate allocation: ${min(20, balance*0.2):.2f}")
                    print(f"  Strategy: Buy 4 underdogs at $5 each")
                else:
                    print(f"  No underdog candidates found at <$0.10")
            else:
                print(f"  No Senate markets found")
        else:
            print(f"\n⚠️ No balance available for trading")
    else:
        print(f"\n⚠️ No markets found matching your criteria")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("\n1. Review the recommendations above")
    print("2. Check current economist consensus for CPI")
    print("3. Verify candidate polling for Senate races")
    print("4. Approve trades for execution")
    print("5. I can execute approved trades via API")
    
    # Check if we can place orders
    print("\n" + "=" * 60)
    print("ORDER EXECUTION CAPABILITY")
    print("=" * 60)
    
    # Test order placement capability
    try:
        # Try to get order endpoint
        orders_response = requests.get(
            f"{base_url}/v1/orders",
            headers=headers,
            timeout=30
        )
        
        if orders_response.status_code == 200:
            print("✓ Can read orders - API has read access")
            
            # Try to create a test order (will fail without proper parameters)
            test_order = {
                "ticker": "TEST",
                "side": "yes",
                "action": "buy",
                "count": 1,
                "price": 0.50,
                "type": "limit"
            }
            
            # Don't actually send, just check endpoint
            print("✓ Order creation endpoint should be available")
            print("  (Test order not sent to avoid accidental trades)")
            
        else:
            print(f"Order API status: {orders_response.status_code}")
            print("  May need additional permissions for trading")
            
    except Exception as e:
        print(f"Order capability test error: {str(e)}")

if __name__ == "__main__":
    main()