#!/usr/bin/env python3
"""Kalshi Production Scanner - Real Trading Opportunities"""

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

def analyze_market(m):
    ticker = m.get('ticker', 'N/A')
    title = m.get('title', 'N/A')
    yes_bid = m.get('yes_bid', 0) / 100
    yes_ask = m.get('yes_ask', 0) / 100
    no_bid = m.get('no_bid', 0) / 100
    no_ask = m.get('no_ask', 0) / 100
    volume = m.get('volume', 0)
    status = m.get('status', 'unknown')
    close_time = m.get('close_time', '')
    
    # Check for arbitrage
    total = yes_ask + no_ask
    arb_profit = 100 - total if total < 100 else 0
    
    # Spread
    spread = yes_ask - yes_bid
    
    return {
        'ticker': ticker,
        'title': title[:60],
        'yes_bid': yes_bid,
        'yes_ask': yes_ask,
        'no_bid': no_bid,
        'no_ask': no_ask,
        'volume': volume,
        'status': status,
        'close_time': close_time,
        'total': total,
        'arb_profit': arb_profit,
        'spread': spread,
    }

def main():
    print("=" * 60)
    print("📊 KALSHI PRODUCTION SCANNER")
    print("=" * 60)
    
    private_key = load_private_key(PRIVATE_KEY_PEM)
    print("✓ API Key loaded\n")
    
    # Fetch markets
    categories = ['economics', 'finance', 'politics']
    all_markets = []
    
    for cat in categories:
        print(f"Scanning {cat}...")
        resp = make_request(private_key, f"/trade-api/v2/markets?limit=50&category={cat}&status=open")
        if resp.status_code == 200:
            markets = resp.json().get('markets', [])
            for m in markets:
                if m.get('volume', 0) > 0:  # Only active markets
                    all_markets.append(analyze_market(m))
    
    print(f"\n✓ Found {len(all_markets)} active markets\n")
    
    # Sort by volume
    all_markets.sort(key=lambda x: x['volume'], reverse=True)
    
    # Top by volume
    print("=" * 60)
    print("🔥 TOP 10 BY VOLUME")
    print("=" * 60)
    for i, m in enumerate(all_markets[:10], 1):
        arb = f" 🚨 ARB: {m['arb_profit']:.1f}¢" if m['arb_profit'] > 0 else ""
        print(f"\n{i}. {m['ticker']}")
        print(f"   {m['title']}")
        print(f"   YES: {m['yes_bid']:.1f}¢ / {m['yes_ask']:.1f}¢ | NO: {m['no_bid']:.1f}¢ / {m['no_ask']:.1f}¢")
        print(f"   Vol: {m['volume']:,} | Spread: {m['spread']:.1f}¢{arb}")
    
    # Arbitrage opportunities
    arb_markets = [m for m in all_markets if m['arb_profit'] > 0.5]
    if arb_markets:
        print("\n" + "=" * 60)
        print("🚨 ARBITRAGE OPPORTUNITIES")
        print("=" * 60)
        for m in arb_markets[:5]:
            print(f"\n  📌 {m['ticker']}")
            print(f"     {m['title']}")
            print(f"     YES @ {m['yes_ask']:.1f}¢ + NO @ {m['no_ask']:.1f}¢ = {m['total']:.1f}¢")
            print(f"     → LOCKED PROFIT: {m['arb_profit']:.1f}¢ per contract")
    
    # Best spreads (liquidity)
    liquid = [m for m in all_markets if m['spread'] < 2 and m['volume'] > 1000]
    if liquid:
        print("\n" + "=" * 60)
        print("💰 MOST LIQUID (Lowest Spreads)")
        print("=" * 60)
        liquid.sort(key=lambda x: x['spread'])
        for m in liquid[:5]:
            print(f"  {m['ticker']}: Spread {m['spread']:.1f}¢ | Vol: {m['volume']:,}")
    
    # Save results
    with open('/Users/cubiczan/.openclaw/workspace/kalshi-opportunities.json', 'w') as f:
        json.dump(all_markets[:50], f, indent=2)
    print(f"\n📁 Saved to kalshi-opportunities.json")

if __name__ == '__main__':
    main()
