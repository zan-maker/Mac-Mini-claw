#!/usr/bin/env python3
"""
Kalshi API Trading with New API Key
Using RSA private key for JWT authentication
"""

import requests
import json
import time
import jwt
from datetime import datetime
from cryptography.hazmat.primitives import serialization

# NEW Kalshi API credentials
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
    
    # Try different base URLs - Kalshi might have changed endpoints
    base_urls = [
        "https://api.kalshi.com",
        "https://api.elections.kalshi.com", 
        "https://trading-api.kalshi.com",
        "https://api.trade.kalshi.com"
    ]
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    for base_url in base_urls:
        print(f"\n🔗 Testing connection to: {base_url}")
        
        # Try different endpoints
        endpoints = [
            "/v1/user",
            "/v1/account",
            "/v1/markets",
            "/v1/events"
        ]
        
        for endpoint in endpoints:
            try:
                url = f"{base_url}{endpoint}"
                print(f"  Testing: {endpoint}")
                
                response = requests.get(
                    url,
                    headers=headers,
                    timeout=30
                )
                
                print(f"    Status: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"    ✓ SUCCESS! Connected to {base_url}")
                    
                    # Try to get user info
                    if endpoint == "/v1/user" or endpoint == "/v1/account":
                        try:
                            user_data = response.json()
                            print(f"\n    Account Information:")
                            print(f"      Email: {user_data.get('email', 'N/A')}")
                            if 'balance' in user_data:
                                balance = user_data.get('balance', {})
                                cash = balance.get('cash_balance_cents', 0) / 100
                                print(f"      Balance: ${cash:.2f}")
                        except:
                            pass
                    
                    return base_url, headers
                    
                elif response.status_code == 401:
                    print(f"    ✗ Authentication failed")
                elif response.status_code == 404:
                    print(f"    ✗ Endpoint not found")
                else:
                    print(f"    Response: {response.text[:100]}")
                    
            except requests.exceptions.ConnectionError:
                print(f"    ✗ Connection failed (DNS/Network)")
            except Exception as e:
                print(f"    Error: {str(e)[:100]}")
    
    return None, None

def search_markets_direct(base_url, headers):
    """Search for markets directly"""
    
    print(f"\n🔍 Searching for CPI and Senate markets...")
    
    # Try to get all markets
    try:
        markets_url = f"{base_url}/v1/markets"
        params = {
            "limit": 100,
            "status": "open"
        }
        
        response = requests.get(
            markets_url,
            headers=headers,
            params=params,
            timeout=30
        )
        
        if response.status_code == 200:
            markets_data = response.json()
            markets = markets_data.get('markets', [])
            print(f"Found {len(markets)} total markets")
            
            # Search for CPI markets
            cpi_markets = []
            for market in markets:
                title = market.get('title', '').lower()
                ticker = market.get('ticker', '').lower()
                
                if 'cpi' in title or 'inflation' in title or 'cpi' in ticker:
                    cpi_markets.append(market)
            
            # Search for Senate markets
            senate_markets = []
            for market in markets:
                title = market.get('title', '').lower()
                ticker = market.get('ticker', '').lower()
                
                if 'senate' in title or 'election' in title or 'senate' in ticker:
                    senate_markets.append(market)
            
            print(f"\n📊 CPI Markets Found: {len(cpi_markets)}")
            for market in cpi_markets[:5]:  # Show first 5
                print(f"  • {market.get('title', 'Unknown')}")
                print(f"    Ticker: {market.get('ticker', 'N/A')}")
                print(f"    Status: {market.get('status', 'N/A')}")
                if market.get('yes_price') and market.get('no_price'):
                    print(f"    YES: ${market.get('yes_price')} | NO: ${market.get('no_price')}")
            
            print(f"\n🏛️ Senate Markets Found: {len(senate_markets)}")
            for market in senate_markets[:5]:  # Show first 5
                print(f"  • {market.get('title', 'Unknown')}")
                print(f"    Ticker: {market.get('ticker', 'N/A')}")
                print(f"    Status: {market.get('status', 'N/A')}")
                if market.get('yes_price') and market.get('no_price'):
                    print(f"    YES: ${market.get('yes_price')} | NO: ${market.get('no_price')}")
            
            return {
                'cpi_markets': cpi_markets,
                'senate_markets': senate_markets,
                'all_markets': markets[:50]  # Return first 50
            }
            
        else:
            print(f"Markets API error: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"Error searching markets: {str(e)}")
    
    return {'cpi_markets': [], 'senate_markets': [], 'all_markets': []}

def analyze_trade_opportunities(market_data, balance=1000):
    """Analyze markets for trade opportunities"""
    
    print(f"\n" + "="*60)
    print("TRADE ANALYSIS & RECOMMENDATIONS")
    print("="*60)
    
    cpi_markets = market_data.get('cpi_markets', [])
    senate_markets = market_data.get('senate_markets', [])
    
    recommendations = []
    
    # Analyze CPI markets
    if cpi_markets:
        print(f"\n📈 CPI INFLATION TRADE OPPORTUNITIES:")
        
        for market in cpi_markets:
            ticker = market.get('ticker', 'Unknown')
            title = market.get('title', 'Unknown')
            yes_price = float(market.get('yes_price', 0.5))
            no_price = float(market.get('no_price', 0.5))
            
            print(f"\n  Market: {title}")
            print(f"  Ticker: {ticker}")
            print(f"  Current Prices: YES=${yes_price:.3f} | NO=${no_price:.3f}")
            
            # Check for trade opportunities based on your criteria
            if yes_price < 0.45:
                print(f"  ✅ BUY YES Opportunity!")
                print(f"     Price: ${yes_price:.3f} (market thinks {yes_price*100:.1f}% probability)")
                print(f"     Edge needed: ≥4% → Need true probability > {(yes_price*100)+4:.1f}%")
                print(f"     Position: $100-200")
                
                recommendations.append({
                    'type': 'CPI',
                    'action': 'BUY YES',
                    'ticker': ticker,
                    'price': yes_price,
                    'position': min(200, balance * 0.5),
                    'reason': f'Price < $0.45, market underestimates probability'
                })
                
            elif no_price < 0.45:
                print(f"  ✅ BUY NO Opportunity!")
                print(f"     Price: ${no_price:.3f} (market thinks {no_price*100:.1f}% probability)")
                print(f"     Edge needed: ≥4% → Need true probability > {(no_price*100)+4:.1f}%")
                print(f"     Position: $100-200")
                
                recommendations.append({
                    'type': 'CPI',
                    'action': 'BUY NO',
                    'ticker': ticker,
                    'price': no_price,
                    'position': min(200, balance * 0.5),
                    'reason': f'Price < $0.45, market underestimates probability'
                })
            else:
                print(f"  ⚠️ No clear edge at current prices")
    
    # Analyze Senate markets
    if senate_markets:
        print(f"\n🏛️ SENATE ELECTION TRADE OPPORTUNITIES:")
        
        # Find underdog candidates (low price)
        underdogs = []
        for market in senate_markets:
            yes_price = float(market.get('yes_price', 1.0))
            title = market.get('title', '').lower()
            
            # Look for underdogs (cheap prices)
            if yes_price < 0.10:  # Under 10 cents
                underdogs.append({
                    'market': market,
                    'price': yes_price,
                    'title': market.get('title', 'Unknown'),
                    'ticker': market.get('ticker', 'Unknown')
                })
        
        if underdogs:
            print(f"  Found {len(underdogs)} underdog candidates (<$0.10)")
            
            # Sort by price (cheapest first)
            underdogs.sort(key=lambda x: x['price'])
            
            # Recommend top 4 underdogs
            top_underdogs = underdogs[:4]
            
            for i, underdog in enumerate(top_underdogs, 1):
                print(f"\n  {i}. {underdog['title']}")
                print(f"     Ticker: {underdog['ticker']}")
                print(f"     Price: ${underdog['price']:.3f}")
                print(f"     Position: $5.00")
                
                recommendations.append({
                    'type': 'SENATE',
                    'action': 'BUY YES',
                    'ticker': underdog['ticker'],
                    'price': underdog['price'],
                    'position': 5.00,
                    'reason': f'Underdog candidate at ${underdog["price"]:.3f}'
                })
            
            print(f"\n  💰 Total Senate Allocation: $20.00")
            print(f"     Strategy: Buy 4 underdogs at $5 each")
            print(f"     Potential payout: $25-$100 per winning ticket")
        else:
            print(f"  ⚠️ No underdog candidates found at <$0.10")
    
    return recommendations

def main():
    """Main execution"""
    print("=" * 60)
    print("KALSHI API TRADING - NEW API KEY")
    print("=" * 60)
    
    # Step 1: Create JWT token
    print("\n1. Creating authentication token...")
    token = create_jwt_token()
    
    if not token:
        print("✗ Failed to create authentication token")
        print("\nPossible issues:")
        print("1. Private key format incorrect")
        print("2. RSA key loading failed")
        print("3. JWT library issue")
        return
    
    # Step 2: Test API connection
    print("\n2. Testing API connection...")
    base_url, headers = test_api_connection(token)
    
    if not base_url:
        print("\n✗ Failed to connect to Kalshi API")
        print("\nTroubleshooting steps:")
        print("1. Check if API key is still valid")
        print("2. Check Kalshi API documentation for current endpoints")
        print("3. Try using the web interface directly")
        print("4. Contact Kalshi support for API access")
        return
    
    print(f"\n✓ Successfully connected to: {base_url}")
    
    # Step 3: Search for markets
    print("\n3. Searching for markets...")
    market_data = search_markets_direct(base_url, headers)
    
    # Step 4: Analyze trade opportunities
    print("\n4. Analyzing trade opportunities...")
    
    # Assume $1000 balance for analysis (adjust based on actual balance)
    balance = 1000  # Default for analysis
    
    recommendations = analyze_trade_opportunities(market_data, balance)
    
    # Step 5: Generate trade plan
    print(f"\n" + "="*60)
    print("TRADE EXECUTION PLAN")
    print("="*60)
    
    if recommendations:
        print(f"\nFound {len(recommendations)} trade opportunities:")
        
        total_investment = 0
        cpi_trades = [r for r in recommendations if r['type'] == 'CPI']
        senate_trades = [r for r in recommendations if r['type'] == 'SENATE']
        
        if cpi_trades:
            print(f"\n📈 CPI Trades ({len(cpi_trades)}):")
            for trade in cpi_trades:
                print(f"  • {trade['action']} {trade['ticker']} @ ${trade['price']:.3f}")
                print(f"    Position: ${trade['position']:.2f}")
                print(f"    Reason: {trade['reason']}")
                total_investment += trade['position']
        
        if senate_trades:
            print(f"\n🏛️ Senate Trades ({len(senate_trades)}):")
            for trade in senate_trades:
                print(f"  • {trade['action']} {trade['ticker']} @ ${trade['price']:.3f}")
                print(f"    Position: ${trade['position']:.2f}")
                print(f"    Reason: {trade['reason']}")
                total_investment += trade['position']
        
        print(f"\n💰 Total Investment Required: ${total_investment:.2f}")
        
        # Save recommendations
        try:
            with open('/Users/cubiczan/.openclaw/workspace/kalshi-trade-recommendations.json', 'w') as f:
                json.dump({
                    'recommendations': recommendations,
                    'market_data_summary': {
                        'cpi_markets': len(market_data.get('cpi_markets', [])),
                        'senate_markets': len(market_data.get('senate_markets', [])),
                        'total_markets': len(market_data.get('all_markets', []))
                    },
                    'analysis_timestamp': datetime.now().isoformat(),
                    'api_connected': True,
                    'base_url': base_url
                }, f, indent=2)
            print(f"\n📁 Trade recommendations saved to: kalshi-trade-recommendations.json")
        except Exception as e:
            print(f"\n⚠️ Could not save recommendations: {str(e)}")
        
        # Next steps
        print(f"\n" + "="*60)
        print("NEXT STEPS")
        print("="*60)
        print("\n1. Review the recommendations above")
        print("2. Check current economist consensus for CPI trades")
        print("3. Verify candidate polling for Senate trades")
        print("4. Approve specific trades for execution")
        print("5. I can execute approved trades via API")
        
        # Check order execution capability
        print(f"\n" + "="*60)
        print("ORDER EXECUTION CAPABILITY")
        print("="*60)
        
        try:
            # Test order placement capability
            orders_response = requests.get(
                f"{base_url}/v1/orders",
                headers=headers,
                timeout=30
            )
            
            if orders_response.status_code == 200:
                print("✓ Can read orders - API has read access")
                print("✓ Order creation should be available")
                print("\nTo execute a trade, I would use:")
                print(f"  POST {base_url}/v1/orders")
                print("  With payload: {'ticker': 'XXX', 'side': 'yes/no', 'action': 'buy', 'count': N, 'price': X.XX}")
            else:
                print(f"Order API status: {orders_response.status_code}")
                print("May need additional permissions for trading")
                
        except Exception as e:
            print(f"Order capability test error: {str(e)}")
        
    else:
        print(f"\n⚠️ No trade opportunities found matching your criteria")
        print("\nPossible reasons:")
        print("1. No CPI markets with prices < $0.45")
        print("2. No Senate underdogs with prices < $0.10")
        print("3. Markets for 2026 may not exist yet")
        print("4. Current market prices don't offer sufficient edge")
        
        # Save empty results
        try:
            with open('/Users/cubiczan/.openclaw/workspace/kalshi-trade-recommendations.json', 'w') as f:
                json.dump({
                    'recommendations': [],
                    'market_data_summary': {
                        'cpi_markets': len(market_data.get('cpi_markets', [])),
                        'senate_markets': len(market_data.get('senate_markets', [])),
                        'total_markets': len(market_data.get('all_markets', []))
                    },
                    'analysis_timestamp': datetime.now().isoformat(),
                    'api_connected': True,
                    'base_url': base_url,
                    'note': 'No trade opportunities found matching criteria'
                }, f, indent=2)
            print(f"\n📁 Analysis saved to: kalshi-trade-recommendations.json")
        except Exception as e:
            print(f"\n⚠️ Could not save analysis: {str(e)}")
    
    print(f"\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
