#!/usr/bin/env python3
"""Test various Kalshi production endpoints"""
import requests
import datetime
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

API_KEY_ID = 'fb109d35-efc3-42b1-bdba-0ee2a1e90ef8'

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

def test_endpoint(base_url, private_key, name):
    timestamp = str(int(datetime.datetime.now().timestamp() * 1000))
    path = "/trade-api/v2/markets?limit=5&category=economics"
    signature = create_signature(private_key, timestamp, "GET", path)
    headers = {'KALSHI-ACCESS-KEY': API_KEY_ID, 'KALSHI-ACCESS-SIGNATURE': signature, 'KALSHI-ACCESS-TIMESTAMP': timestamp}
    
    print(f"\nTesting: {name}")
    print(f"URL: {base_url}{path}")
    try:
        resp = requests.get(base_url + path, headers=headers, timeout=10)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            markets = data.get('markets', [])
            print(f"✓ Markets: {len(markets)}")
            for m in markets[:3]:
                print(f"  - {m.get('ticker')}: {m.get('title', '')[:40]}")
        else:
            print(f"Error: {resp.text[:200]}")
    except Exception as e:
        print(f"Failed: {e}")

def main():
    private_key = load_private_key(PRIVATE_KEY_PEM)
    
    endpoints = [
        ("https://api.kalshi.com", "Production (api.kalshi.com)"),
        ("https://elections.kalshi.com", "Elections (elections.kalshi.com)"),
        ("https://api.elections.kalshi.com", "Elections API (api.elections.kalshi.com)"),
        ("https://demo-api.kalshi.co", "Demo (demo-api.kalshi.co)"),
    ]
    
    for url, name in endpoints:
        test_endpoint(url, private_key, name)

if __name__ == '__main__':
    main()
