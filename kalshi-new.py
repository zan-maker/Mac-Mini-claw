#!/usr/bin/env python3
"""Kalshi Scanner - New API Key"""

import requests, datetime, base64, json
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

API_KEY_ID = '43bc9799-65a9-4ede-bd96-ea426d1e05de'
BASE_URL = 'https://api.elections.kalshi.com'

PRIVATE_KEY_PEM = """-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAxYgsw+9yl8iCmq+ajBH/WWHklTD830UZkOkI6HR2socllddB
EvYsXm6nbUoCjRxh/2k4LnDikXlmzR2J0U0/zfFiwvUthxHtgG3B04gmnMfpJfsp
g3ca6PzPbb3rVAlXRd6FDf1KKrJHdKph530zgL7u4UOs/OltxXJ7bqoy7N+3PKLA
ZwR2xa2X9zwbXeaSoTk4nAVUl6JmqpYfgti3aUiZ9N45uV5w0iVRc4I73QGDtTrj
ZVg2ATZrqWOg/Gw9TZCLM6SvYZo+WHj/NdQJCvKGVjzTUOLbEJdj1DGLVbd9rDKq
ae8GrXmDUIu+wZjQRcL9jJukajCv8KyGcgzLuQIDAQABAoIBACuuX9vaTRh0jjEf
yQjViAafh7lYMms7MBqj9cTV0FPNYAnhJnJHfutJA/w+hA7pamBdR7+5Vdj+pDWS
pSHkN8pWaVUce7tlQwSGAPlCn+tGp++uuXDpe0lvcn1dpLcaM7LvMLQ1wVtsvjF1
5h2XSbbcQh4NZakuA4jItrPzrjxEHx/CQqE/tPU7BdeQ6ZGHA5uCfaZQoBMISIkh
JfD3mr0uvlZT5+/GoA0iCpcH+OOErnsgzxz+sxb04aVJAm91WcFL/TWALPm49M/W
uzyFKmrPf/Q4YmK4GovTzCciqwN/y8ND4ddWvgr1z4bXjyLNFj2AL/uLdho2cGUy
UWJFaisCgYEA4DpAx+txNaAxECU2WbL6wfKzoQy/Pd2VI1VXhW6bfRmfRbEFAFp7
r6V6nGVsxXAgeoTs4WPjl/XslL0wx2HkWJV5xFx2YP9kOR9MWb5cNQya6VtKCahZ
eHJcyHdPxxGRDHMAl4+oVY8/dD6wVlUCrMAhOVPQQF62jvsXoDAsaJcCgYEA4YWN
EtHuGS6aAI3sDXUa+fr/a4IgbjBVpC3ZkdGnGqALDn1ge9+hiDzjzZ2vSyymfxMn
StAGeFY9FYfl37dPTVMUg/16qRv83e7FhVJvw/Rqlr2qOItR8OxIDL4ML1OeXpYk
g7A3SCc2MMwL03+0Q7ayH7pK46GNY8fu7JaiKC8CgYEAiVymWtKtI8DizZU+Wmz+
mNnpmPuKHIgl2ONrHl7H+jc8DyGGgtTreIrTNgQcQkeSXfwYcWsT/f+10tijjUE2
9d18HwLVsk5CQ4wc5c1sB0OVkudNz+TGCrdkh5ov0S+9v/ajojVrVh7PLJNKy1iA
rvt0Xv4tUYG0LJs9ufBJBDkCgYEA2fOA8IRUUJ/6E7kVPbhEVv1dZiA/iV5LFj19
fHCax5+Or/U5jt4Eta7rFedj5woC6uKu4Z2D8z6dEDbjUT9Oc9NsC1eo+NBkpHPD
DuMpwr5vWLl6TeVPTsB7rVzqV76/WnhOV7qw4pmKxMQeVcuggqSJJyKah7208I7j
+GBn3N8CgYEArMGpB1sVEHuHoLr24ji7QB7FADwIgOpxjDoQltVZxih3zV29D9XQ
waWmIjENW9yO9iUVSugYYiROPbIrKiPBTzcKHenmWKQ6497gTXKmCKBPof+yJmaQ
2o/Q6i97z/qbwJPAH5bJ5vyWOJreDNl2KOAbpOIv+JAQ6lpeye2Ucjw=
-----END RSA PRIVATE KEY-----"""

pk = serialization.load_pem_private_key(PRIVATE_KEY_PEM.encode(), password=None, backend=default_backend())

def make_request(path):
    ts = str(int(datetime.datetime.now().timestamp() * 1000))
    msg = f"{ts}GET{path.split('?')[0]}".encode()
    sig = pk.sign(msg, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.DIGEST_LENGTH), hashes.SHA256())
    sig_b64 = base64.b64encode(sig).decode()
    headers = {'KALSHI-ACCESS-KEY': API_KEY_ID, 'KALSHI-ACCESS-SIGNATURE': sig_b64, 'KALSHI-ACCESS-TIMESTAMP': ts}
    return requests.get(BASE_URL + path, headers=headers)

print("=" * 60)
print("🔍 KALSHI SCANNER - NEW API KEY")
print("=" * 60)
print()

# Test 1: Check account/balance
print("1. Testing portfolio/balance...")
resp = make_request("/trade-api/v2/portfolio/balance")
print(f"   Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    print(f"   Balance: ${data.get('balance', 0)/100:.2f}")
else:
    print(f"   Error: {resp.text[:200]}")

print()

# Test 2: Get all markets with different category filters
print("2. Fetching markets by category...")
categories = ['economics', 'finance', 'politics', 'science', 'culture', 'sports', 'weather', 'world']

all_markets = []
for cat in categories:
    resp = make_request(f"/trade-api/v2/markets?limit=20&category={cat}&status=open")
    if resp.status_code == 200:
        markets = resp.json().get('markets', [])
        if markets:
            print(f"   {cat}: {len(markets)} markets")
            for m in markets:
                m['_category'] = cat
            all_markets.extend(markets)

print(f"\n   Total: {len(all_markets)} markets")

# Test 3: Try without category filter (all open)
print("\n3. Fetching ALL open markets (no filter)...")
resp = make_request("/trade-api/v2/markets?limit=100&status=open")
if resp.status_code == 200:
    markets = resp.json().get('markets', [])
    print(f"   Status: 200")
    print(f"   Markets: {len(markets)}")
else:
    print(f"   Status: {resp.status_code}")

# Analyze what we got
print("\n" + "=" * 60)
print("📊 MARKET ANALYSIS")
print("=" * 60)

# Filter for non-parlay markets (shorter tickers)
simple = []
for m in all_markets:
    ticker = m.get('ticker', '')
    title = m.get('title', '')
    yes_bid = m.get('yes_bid', 0) / 100
    yes_ask = m.get('yes_ask', 0) / 100
    no_bid = m.get('no_bid', 0) / 100
    no_ask = m.get('no_ask', 0) / 100
    vol = m.get('volume', 0)
    
    # Skip long parlay tickers
    if len(ticker) > 40:
        continue
    
    # Skip no-volume
    if vol < 1:
        continue
    
    # Skip zero prices
    if yes_ask == 0 and no_ask == 0:
        continue
    
    total = yes_ask + no_ask
    arb = 100 - total if 95 <= total <= 100 else 0
    
    simple.append({
        'ticker': ticker,
        'title': title[:50],
        'cat': m.get('_category', 'unknown'),
        'yes': (yes_bid, yes_ask),
        'no': (no_bid, no_ask),
        'vol': vol,
        'total': total,
        'arb': arb,
    })

simple.sort(key=lambda x: x['vol'], reverse=True)

print(f"\nFound {len(simple)} active non-parlay markets\n")

for i, m in enumerate(simple[:15], 1):
    arb_str = f" ⚡ARB:{m['arb']:.1f}¢" if m['arb'] > 0.3 else ""
    print(f"{i}. [{m['cat']}] {m['ticker']}")
    print(f"   {m['title']}")
    print(f"   YES: {m['yes'][0]:.1f}¢/{m['yes'][1]:.1f}¢ | NO: {m['no'][0]:.1f}¢/{m['no'][1]:.1f}¢ | Vol: {m['vol']}{arb_str}")
    print()

# Save
with open('/Users/cubiczan/.openclaw/workspace/kalshi-scan.json', 'w') as f:
    json.dump(all_markets, f, indent=2)
print(f"📁 Full data saved to kalshi-scan.json")
