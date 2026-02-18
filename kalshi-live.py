#!/usr/bin/env python3
"""Kalshi Live Scanner - Find Real Trading Opportunities"""

import requests
import datetime
import base64
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

def load_key(pem): return serialization.load_pem_private_key(pem.encode(), password=None, backend=default_backend())
def sign(pk, ts, method, path):
    msg = f"{ts}{method}{path.split('?')[0]}".encode()
    sig = pk.sign(msg, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.DIGEST_LENGTH), hashes.SHA256())
    return base64.b64encode(sig).decode()

def get_markets(pk, cursor=None):
    ts = str(int(datetime.datetime.now().timestamp() * 1000))
    path = "/trade-api/v2/markets?limit=100&status=open"
    if cursor: path += f"&cursor={cursor}"
    headers = {'KALSHI-ACCESS-KEY': API_KEY_ID, 'KALSHI-ACCESS-SIGNATURE': sign(pk, ts, "GET", path), 'KALSHI-ACCESS-TIMESTAMP': ts}
    return requests.get(BASE_URL + path, headers=headers).json()

def main():
    pk = load_key(PRIVATE_KEY_PEM)
    
    print("🔍 SCANNING KALSHI MARKETS...\n")
    
    # Get multiple pages
    all_markets = []
    data = get_markets(pk)
    all_markets.extend(data.get('markets', []))
    
    # Get more if available
    cursor = data.get('cursor')
    if cursor:
        data2 = get_markets(pk, cursor)
        all_markets.extend(data2.get('markets', []))
    
    print(f"Found {len(all_markets)} total markets\n")
    
    # Filter for simple binary markets (not parlays)
    simple = []
    for m in all_markets:
        ticker = m.get('ticker', '')
        title = m.get('title', '')
        
        # Skip multi-game parlays (long tickers with "MULTIGAME")
        if 'MULTIGAME' in ticker or len(ticker) > 50:
            continue
            
        yes_bid = m.get('yes_bid', 0) / 100
        yes_ask = m.get('yes_ask', 0) / 100
        no_bid = m.get('no_bid', 0) / 100
        no_ask = m.get('no_ask', 0) / 100
        vol = m.get('volume', 0)
        
        # Check for real pricing
        if yes_ask > 0 and no_ask > 0:
            total = yes_ask + no_ask
            arb = 100 - total if 95 <= total <= 100 else 0
            
            simple.append({
                'ticker': ticker,
                'title': title[:50],
                'yes': (yes_bid, yes_ask),
                'no': (no_bid, no_ask),
                'vol': vol,
                'total': total,
                'arb': arb,
                'spread': yes_ask - yes_bid,
            })
    
    # Sort by volume
    simple.sort(key=lambda x: x['vol'], reverse=True)
    
    print("=" * 60)
    print("📊 SIMPLE BINARY MARKETS")
    print("=" * 60)
    
    for i, m in enumerate(simple[:20], 1):
        arb_str = f" ⚡ARB:{m['arb']:.1f}¢" if m['arb'] > 0.3 else ""
        print(f"\n{i}. {m['ticker']}")
        print(f"   {m['title']}")
        print(f"   YES: {m['yes'][0]:.1f}¢/{m['yes'][1]:.1f}¢ | NO: {m['no'][0]:.1f}¢/{m['no'][1]:.1f}¢")
        print(f"   Vol: {m['vol']:,} | Spread: {m['spread']:.1f}¢ | Sum: {m['total']:.1f}¢{arb_str}")
    
    # Arbitrage
    arb_ops = [m for m in simple if m['arb'] > 0.3]
    if arb_ops:
        print("\n" + "=" * 60)
        print("🚨 ARBITRAGE FOUND")
        print("=" * 60)
        for m in arb_ops:
            print(f"\n  {m['ticker']}")
            print(f"  Buy YES @ {m['yes'][1]:.1f}¢ + NO @ {m['no'][1]:.1f}¢ = {m['total']:.1f}¢")
            print(f"  GUARANTEED PROFIT: {m['arb']:.1f}¢ per contract pair")
    else:
        print("\n✓ No arbitrage opportunities found")
    
    # Best trading candidates
    liquid = [m for m in simple if m['spread'] <= 2 and m['vol'] > 100]
    if liquid:
        print("\n" + "=" * 60)
        print("💰 BEST FOR TRADING")
        print("=" * 60)
        for m in liquid[:5]:
            print(f"  • {m['ticker']}: {m['spread']:.1f}¢ spread, {m['vol']:,} vol")

if __name__ == '__main__':
    main()
