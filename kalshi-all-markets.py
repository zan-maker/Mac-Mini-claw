#!/usr/bin/env python3
"""Kalshi Full Scanner - All Categories"""

import requests
import datetime
import base64
import json
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

API_KEY_ID = 'fb109d35-efc3-42b1-bdba-0ee2a1e90ef8'
BASE_URL = 'https://api.elections.kalshi.com'

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
    return serialization.load_pem_private_key(key_pem.encode('utf-8'), password=None, backend=default_backend())

def create_signature(private_key, timestamp, method, path):
    path_without_query = path.split('?')[0]
    message = f"{timestamp}{method}{path_without_query}".encode('utf-8')
    signature = private_key.sign(message, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.DIGEST_LENGTH), hashes.SHA256())
    return base64.b64encode(signature).decode('utf-8')

def make_request(private_key, path):
    timestamp = str(int(datetime.datetime.now().timestamp() * 1000))
    signature = create_signature(private_key, timestamp, "GET", path)
    headers = {'KALSHI-ACCESS-KEY': API_KEY_ID, 'KALSHI-ACCESS-SIGNATURE': signature, 'KALSHI-ACCESS-TIMESTAMP': timestamp}
    return requests.get(BASE_URL + path, headers=headers)

def main():
    print("=" * 60)
    print("📊 KALSHI - ALL OPEN MARKETS")
    print("=" * 60)
    
    private_key = load_private_key(PRIVATE_KEY_PEM)
    
    # Get all open markets without category filter
    resp = make_request(private_key, "/trade-api/v2/markets?limit=100&status=open")
    
    if resp.status_code != 200:
        print(f"Error: {resp.status_code}")
        print(resp.text[:500])
        return
    
    data = resp.json()
    markets = data.get('markets', [])
    
    # Filter for binary markets with volume and real prices
    binary_markets = []
    for m in markets:
        if m.get('market_type') == 'binary' and m.get('volume', 0) > 100:
            yes_bid = m.get('yes_bid', 0) / 100
            yes_ask = m.get('yes_ask', 0) / 100
            no_bid = m.get('no_bid', 0) / 100
            no_ask = m.get('no_ask', 0) / 100
            
            # Real arb check for binary: YES ask + NO ask should be ~100
            total = yes_ask + no_ask
            arb = 100 - total if 95 < total < 100 else 0
            
            binary_markets.append({
                'ticker': m.get('ticker'),
                'title': m.get('title', '')[:55],
                'yes_bid': yes_bid,
                'yes_ask': yes_ask,
                'no_bid': no_bid,
                'no_ask': no_ask,
                'volume': m.get('volume', 0),
                'total': total,
                'arb': arb,
                'spread': yes_ask - yes_bid,
                'category': m.get('category', 'unknown'),
            })
    
    # Sort by volume
    binary_markets.sort(key=lambda x: x['volume'], reverse=True)
    
    print(f"\n✓ Found {len(binary_markets)} active binary markets\n")
    
    # Top 15 by volume
    print("=" * 60)
    print("🔥 TOP 15 BY VOLUME")
    print("=" * 60)
    for i, m in enumerate(binary_markets[:15], 1):
        arb_flag = f" ⚡ARB {m['arb']:.1f}¢" if m['arb'] > 0.5 else ""
        print(f"\n{i}. [{m['category']}] {m['ticker']}")
        print(f"   {m['title']}")
        print(f"   YES: {m['yes_bid']:.1f}¢/{m['yes_ask']:.1f}¢ | NO: {m['no_bid']:.1f}¢/{m['no_ask']:.1f}¢")
        print(f"   Vol: {m['volume']:,} | Spread: {m['spread']:.1f}¢ | Total: {m['total']:.1f}¢{arb_flag}")
    
    # Any real arbitrage
    real_arb = [m for m in binary_markets if m['arb'] > 0.5]
    if real_arb:
        print("\n" + "=" * 60)
        print("🚨 REAL ARBITRAGE (YES+NO < 100)")
        print("=" * 60)
        for m in real_arb:
            print(f"\n  {m['ticker']}")
            print(f"  YES @ {m['yes_ask']:.1f}¢ + NO @ {m['no_ask']:.1f}¢ = {m['total']:.1f}¢")
            print(f"  → Profit: {m['arb']:.1f}¢ per pair")
    
    # Recommendations for trading
    print("\n" + "=" * 60)
    print("💡 TRADING RECOMMENDATIONS")
    print("=" * 60)
    
    # Best liquidity
    liquid = [m for m in binary_markets if m['spread'] <= 1 and m['volume'] > 500]
    if liquid:
        print("\n✅ BEST FOR TRADING (Low spread, high volume):")
        for m in liquid[:5]:
            print(f"  • {m['ticker']}: {m['spread']:.1f}¢ spread, {m['volume']:,} vol")
    
    # Interesting prices
    extreme_yes = [m for m in binary_markets if 85 < m['yes_ask'] < 95]
    extreme_no = [m for m in binary_markets if 85 < m['no_ask'] < 95]
    
    if extreme_yes:
        print("\n📈 HIGH CONFIDENCE YES (>85%):")
        for m in extreme_yes[:3]:
            print(f"  • {m['ticker']}: YES @ {m['yes_ask']:.1f}¢")
    
    if extreme_no:
        print("\n📉 HIGH CONFIDENCE NO (>85%):")
        for m in extreme_no[:3]:
            print(f"  • {m['ticker']}: NO @ {m['no_ask']:.1f}¢")
    
    # Save
    with open('/Users/cubiczan/.openclaw/workspace/kalshi-trading.json', 'w') as f:
        json.dump(binary_markets, f, indent=2)
    print(f"\n📁 Full data saved to kalshi-trading.json")

if __name__ == '__main__':
    main()
