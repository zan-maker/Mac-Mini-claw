#!/usr/bin/env python3
"""
Kalshi API Market Scanner
Fetches current markets and identifies trading opportunities
"""

import requests
import datetime
import base64
import json
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

# Configuration
API_KEY_ID = 'fb109d35-efc3-42b1-bdba-0ee2a1e90ef8'
BASE_URL = 'https://demo-api.kalshi.co'  # Demo (try production: https://trading.kalshi.com)

# Private key (from user)
PRIVATE_KEY_PEM = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA4+LPLFirxRAFlAxRI7xkdIAVuOkg4KCOIk7q1LAZy70Ek0Qj
Z8mTwDFkgEu3iv/6s2ecSo2n03XE+Kkxs5q6avkL9DD2Bci/yKiRiLyfzgjJ0YQt
pxo4Ddlc2JlM45n+WEhu7tpajPD9DPoisFF6dxWfaMfX3LAIm4dUm2TGcYuhG9dh
lWbJS4wM0O9NxY+upX3S2zsvAtl8lJ9MBuH2GVevPvgoyKJikx2Wz19fO8vapWod
kiXa6l1/VqtWFdLhhzGKRwhQyYDsw6ie7H7wX9YwUuVmglU2bNy1b9RCwM+ciQNY
fXqY3Ru8r1F2XxQe7F6p+YImxmBN2orEljEVcwIDAQABAoIBABv88jbfGRGV2ymI
rbp229uXE5PnRftwnKRIDv1aN4DXUSWJG9QWZMgZCN/c7MjskWzRT9e0OCV3dF6Z
4RnO6hBTUA2Iqd6h/jP1yBIEIJhcafUKh9TbGoFQ7d9ITLIzapKLKty5AqAGxP2A
BxyilSjlBfQHf1KCaDw5zcFcCidNpGw5h+LuVJkQXZigW1sW6odGhmoaU0jcq5x5
T+BAdNcFG0ZLj7QZTqjKj4kh9l8CS2kBuuervJC5lGNVdrxcm0LjjLct80dJgzXm
cdMoqVdhtb6tLipPdZYdJNGU1Z6OHTceTXdjKhypKJ60ResiEFfV9Ki4nR0mR+jj
5ZYoV1ECgYEA5M49U6RlKCH7BOz8xPA/lbq/hQgSPWKvuM/PSBUxvIBtITwX4gwW
65j34dJL3IdWlqIgVQmVOaHAfetJJvfO9mGcHfN+TSlS+ugt2sl/dp7o0lCyo47v
6132PeOS27fItyJnXRq8tYnZEgq3JP6beVUvQiTkaybHMoWBHyRhh8kCgYEA/viW
hUKEJCfJXl52Zj8vCDaQtIkgL2KnQMI0/FtFY3AUfxTyV3oSU5Mns0fl4soQflWA
C7metlLyBGlyuHUmkP7BbBy/2IWpHEW4SUEJ1APwap96M3ZBEgNlNnuyLWRQ+koY
ascA4rn7io5Pjk178H63rNOGrexEkRHOwnshyVsCgYBfss89s63HmmbWSZTzfhTq
OECwkI6odCVRJEHrQUobMI/0baEDn9DaW5GaNw4Zv9V8jXT+fFKY10meoRFopg8/
R9Y3RMeX2Gfnn8LGFq8kWxTAGpaNCFTa2eMLQasEERt3VYFsFKnHOE+9VxQA+ijn
F7T7cljDZGW+gM5fyySr2QKBgQCMyAGETvfbZsR/ALVrO1Piuw4nQNeuklA7J4BO
Hq8veoE2sgAlYNehocz35qj+EggNWXQ8BR+nGCFdYkPfqX/D64YtBarACP0ZCT35
5JlioVIr7SZyJ8dCBPHrpVz6RzuXFzZoLr1EcuB63pz6u7nFTpJoMNtaSOyLFUQO
iiJbpQKBgDb8qJKW3qL573WF1JdBcs+qgTGCKBGu+a6ZdWUwnAMD8NJ3aS3uC3cB
clt58r2qWh8XW5th5XS5z6oa41gaLUz4huqbcYrudKhG4fekL3nTIx+w1FlxCCi8
8nHLCTEW+VABJjTfxm3KTvvamyLVCzyK2YtYRcehHHVSaICLe5hp
-----END RSA PRIVATE KEY-----"""

def load_private_key(key_pem):
    """Load the private key from PEM string."""
    return serialization.load_pem_private_key(
        key_pem.encode('utf-8'),
        password=None,
        backend=default_backend()
    )

def create_signature(private_key, timestamp, method, path):
    """Create the request signature using RSA-PSS."""
    # Strip query parameters before signing
    path_without_query = path.split('?')[0]
    message = f"{timestamp}{method}{path_without_query}".encode('utf-8')
    
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.DIGEST_LENGTH
        ),
        hashes.SHA256()
    )
    
    return base64.b64encode(signature).decode('utf-8')

def make_request(private_key, path, method="GET"):
    """Make an authenticated request to the Kalshi API."""
    timestamp = str(int(datetime.datetime.now().timestamp() * 1000))
    signature = create_signature(private_key, timestamp, method, path)
    
    headers = {
        'KALSHI-ACCESS-KEY': API_KEY_ID,
        'KALSHI-ACCESS-SIGNATURE': signature,
        'KALSHI-ACCESS-TIMESTAMP': timestamp
    }
    
    url = BASE_URL + path
    response = requests.get(url, headers=headers)
    
    return response

def get_markets(private_key, limit=50, cursor=None):
    """Get list of markets."""
    path = f"/trade-api/v2/markets?limit={limit}"
    if cursor:
        path += f"&cursor={cursor}"
    
    response = make_request(private_key, path)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def analyze_market(market):
    """Analyze a single market for trading opportunity."""
    ticker = market.get('ticker', 'N/A')
    title = market.get('title', 'N/A')
    yes_bid = market.get('yes_bid', 0)
    yes_ask = market.get('yes_ask', 0)
    no_bid = market.get('no_bid', 0)
    no_ask = market.get('no_ask', 0)
    volume = market.get('volume', 0)
    status = market.get('status', 'unknown')
    
    # Convert from cents to probability (0-100)
    yes_bid_pct = yes_bid / 100 if yes_bid else 0
    yes_ask_pct = yes_ask / 100 if yes_ask else 0
    no_bid_pct = no_bid / 100 if no_bid else 0
    no_ask_pct = no_ask / 100 if no_ask else 0
    
    # Check for arbitrage (simplified)
    # If YES + NO < 100, there's arb opportunity
    total_yes_no = yes_ask_pct + no_ask_pct
    
    # Calculate mid prices
    yes_mid = (yes_bid_pct + yes_ask_pct) / 2
    no_mid = (no_bid_pct + no_ask_pct) / 2
    
    # Spread
    yes_spread = yes_ask_pct - yes_bid_pct
    no_spread = no_ask_pct - no_bid_pct
    
    return {
        'ticker': ticker,
        'title': title,
        'status': status,
        'yes_bid': yes_bid_pct,
        'yes_ask': yes_ask_pct,
        'yes_mid': yes_mid,
        'no_bid': no_bid_pct,
        'no_ask': no_ask_pct,
        'no_mid': no_mid,
        'total': total_yes_no,
        'yes_spread': yes_spread,
        'no_spread': no_spread,
        'volume': volume,
        'arbitrage': total_yes_no < 98,  # Simple arb detection
    }

def main():
    print("Kalshi Market Scanner")
    print("=" * 60)
    
    # Load private key
    try:
        private_key = load_private_key(PRIVATE_KEY_PEM)
        print("✓ Private key loaded successfully")
    except Exception as e:
        print(f"✗ Error loading private key: {e}")
        return
    
    # Get markets
    print("\nFetching markets...")
    data = get_markets(private_key, limit=50)
    
    if not data or 'markets' not in data:
        print("✗ No markets data received")
        return
    
    markets = data['markets']
    print(f"✓ Retrieved {len(markets)} markets\n")
    
    # Analyze markets
    print("Analyzing markets for opportunities...")
    print("=" * 60)
    
    opportunities = []
    
    for market in markets:
        analysis = analyze_market(market)
        
        # Filter for open markets with volume
        if analysis['status'] == 'open' and analysis['volume'] > 0:
            opportunities.append(analysis)
    
    # Sort by volume (highest first)
    opportunities.sort(key=lambda x: x['volume'], reverse=True)
    
    # Display top opportunities
    print(f"\n📊 TOP 10 ACTIVE MARKETS BY VOLUME:\n")
    
    for i, opp in enumerate(opportunities[:10], 1):
        arb_flag = " 🚨 ARB" if opp['arbitrage'] else ""
        print(f"{i}. {opp['ticker']}")
        print(f"   {opp['title'][:60]}")
        print(f"   YES: {opp['yes_bid']:.1f}¢ / {opp['yes_ask']:.1f}¢ (mid: {opp['yes_mid']:.1f}¢)")
        print(f"   NO:  {opp['no_bid']:.1f}¢ / {opp['no_ask']:.1f}¢ (mid: {opp['no_mid']:.1f}¢)")
        print(f"   Spread: YES {opp['yes_spread']:.1f}¢ | NO {opp['no_spread']:.1f}¢")
        print(f"   Volume: {opp['volume']:,} | Total: {opp['total']:.1f}%{arb_flag}")
        print()
    
    # Check for arbitrage opportunities
    arb_opportunities = [o for o in opportunities if o['arbitrage']]
    
    if arb_opportunities:
        print("\n🚨 ARBITRAGE OPPORTUNITIES DETECTED:\n")
        for opp in arb_opportunities[:5]:
            profit = 100 - opp['total']
            print(f"  {opp['ticker']}: Buy YES @ {opp['yes_ask']:.1f}¢ + NO @ {opp['no_ask']:.1f}¢ = {opp['total']:.1f}¢")
            print(f"  → Locked profit: {profit:.1f}¢ per contract")
            print()
    else:
        print("\n✓ No clear arbitrage opportunities detected")
    
    # Save full results
    output_file = '/Users/cubiczan/.openclaw/workspace/kalshi-markets.json'
    with open(output_file, 'w') as f:
        json.dump(opportunities, f, indent=2)
    
    print(f"\n📁 Full results saved to: {output_file}")

if __name__ == '__main__':
    main()
