#!/usr/bin/env python3
"""Kalshi Raw Dump - See What's Actually Available"""

import requests, datetime, base64, json
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

pk = serialization.load_pem_private_key(PRIVATE_KEY_PEM.encode(), password=None, backend=default_backend())

ts = str(int(datetime.datetime.now().timestamp() * 1000))
path = "/trade-api/v2/markets?limit=50&status=open"
msg = f"{ts}GET{path}".encode()
sig = pk.sign(msg, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.DIGEST_LENGTH), hashes.SHA256())
sig_b64 = base64.b64encode(sig).decode()

headers = {'KALSHI-ACCESS-KEY': API_KEY_ID, 'KALSHI-ACCESS-SIGNATURE': sig_b64, 'KALSHI-ACCESS-TIMESTAMP': ts}
resp = requests.get(BASE_URL + path, headers=headers)
data = resp.json()

print("RAW MARKET DATA SAMPLE")
print("=" * 60)

for i, m in enumerate(data.get('markets', [])[:10], 1):
    print(f"\n{i}. {m.get('ticker', 'N/A')}")
    print(f"   Title: {m.get('title', 'N/A')[:60]}")
    print(f"   Type: {m.get('market_type', 'N/A')}")
    print(f"   YES bid/ask: {m.get('yes_bid', 0)}/{m.get('yes_ask', 0)}")
    print(f"   NO bid/ask: {m.get('no_bid', 0)}/{m.get('no_ask', 0)}")
    print(f"   Volume: {m.get('volume', 0)}")
    print(f"   Status: {m.get('status', 'N/A')}")
    print(f"   Category: {m.get('category', 'N/A')}")

# Save full dump
with open('/Users/cubiczan/.openclaw/workspace/kalshi-raw.json', 'w') as f:
    json.dump(data, f, indent=2)
print(f"\n\nFull dump saved to kalshi-raw.json")
