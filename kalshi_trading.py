#!/usr/bin/env python3
"""
Kalshi Trading Module - Read/Write API
Can place orders, check balance, get positions
"""

import requests
import datetime
import base64
import json
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

# API Configuration
API_KEY_ID = '4dd243e0-5d05-4e63-841a-be980f08b43a'
BASE_URL = 'https://api.elections.kalshi.com'

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

# Load private key
_pk = serialization.load_pem_private_key(PRIVATE_KEY_PEM.encode(), password=None, backend=default_backend())


def _sign_request(method, path):
    """Create request signature."""
    ts = str(int(datetime.datetime.now().timestamp() * 1000))
    path_only = path.split('?')[0]
    msg = f"{ts}{method}{path_only}".encode()
    sig = _pk.sign(msg, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.DIGEST_LENGTH), hashes.SHA256())
    return ts, base64.b64encode(sig).decode()


def _request(method, path, body=None):
    """Make authenticated request to Kalshi API."""
    ts, sig = _sign_request(method, path)
    headers = {
        'KALSHI-ACCESS-KEY': API_KEY_ID,
        'KALSHI-ACCESS-SIGNATURE': sig,
        'KALSHI-ACCESS-TIMESTAMP': ts,
        'Content-Type': 'application/json'
    }
    url = BASE_URL + path
    
    if method == 'GET':
        resp = requests.get(url, headers=headers)
    elif method == 'POST':
        resp = requests.post(url, headers=headers, json=body)
    elif method == 'DELETE':
        resp = requests.delete(url, headers=headers)
    else:
        resp = requests.request(method, url, headers=headers, json=body)
    
    return resp


# ============ PUBLIC API ============

def get_balance():
    """Get account balance."""
    resp = _request('GET', '/trade-api/v2/portfolio/balance')
    if resp.status_code == 200:
        data = resp.json()
        return {
            'balance': data.get('balance', 0) / 100,
            'balance_cents': data.get('balance', 0)
        }
    return None


def get_positions():
    """Get open positions."""
    resp = _request('GET', '/trade-api/v2/portfolio/positions')
    if resp.status_code == 200:
        return resp.json().get('positions', [])
    return []


def get_orders():
    """Get open orders."""
    resp = _request('GET', '/trade-api/v2/portfolio/orders')
    if resp.status_code == 200:
        return resp.json().get('orders', [])
    return []


def get_markets(limit=50, event_ticker=None):
    """Get available markets."""
    path = f'/trade-api/v2/markets?limit={limit}'
    if event_ticker:
        path += f'&event_ticker={event_ticker}'
    resp = _request('GET', path)
    if resp.status_code == 200:
        return resp.json().get('markets', [])
    return []


def get_events(limit=50):
    """Get available events."""
    resp = _request('GET', f'/trade-api/v2/events?limit={limit}')
    if resp.status_code == 200:
        return resp.json().get('events', [])
    return []


def place_order(ticker, side, price_cents, count, order_type='limit'):
    """
    Place an order.
    
    Args:
        ticker: Market ticker (e.g., 'KXCPIYOY-26FEB-T2.4')
        side: 'yes' or 'no'
        price_cents: Price in cents (e.g., 50 for 50 cents)
        count: Number of contracts
        order_type: 'limit' or 'market'
    
    Returns:
        Order response or None if failed
    """
    order = {
        'ticker': ticker,
        'side': side,
        'action': 'buy',
        'type': order_type,
        'yes_price': price_cents,
        'count': count
    }
    
    resp = _request('POST', '/trade-api/v2/portfolio/orders', order)
    
    if resp.status_code in [200, 201]:
        return resp.json()
    else:
        return {'error': resp.text, 'status': resp.status_code}


def cancel_order(order_id):
    """Cancel an order by ID."""
    resp = _request('DELETE', f'/trade-api/v2/portfolio/orders/{order_id}')
    return resp.status_code in [200, 204]


def cancel_all_orders():
    """Cancel all open orders."""
    orders = get_orders()
    cancelled = []
    for o in orders:
        if o.get('status') == 'resting':
            # Try to cancel by ticker
            ticker = o.get('ticker')
            resp = _request('DELETE', f'/trade-api/v2/portfolio/orders?ticker={ticker}')
            cancelled.append({'ticker': ticker, 'status': resp.status_code})
    return cancelled


# ============ CLI ============

if __name__ == '__main__':
    import sys
    
    print("=" * 55)
    print("📊 KALSHI TRADING MODULE")
    print("=" * 55)
    
    # Show balance
    bal = get_balance()
    print(f"\n💰 Balance: ${bal['balance']:.2f}")
    
    # Show positions
    positions = get_positions()
    print(f"\n📈 Positions: {len(positions)}")
    for p in positions:
        print(f"  {p.get('ticker')}: {p.get('side')} x{p.get('count')}")
    
    # Show orders
    orders = get_orders()
    print(f"\n📋 Open Orders: {len([o for o in orders if o.get('status') == 'resting'])}")
    for o in orders:
        if o.get('status') == 'resting':
            print(f"  {o.get('ticker')}: {o.get('side')} x{o.get('count')} @ {o.get('yes_price')}¢")
    
    print("\n✅ Ready to trade!")
    print("\nUsage:")
    print("  place_order(ticker, side, price_cents, count)")
    print("  Example: place_order('KXCPIYOY-26FEB-T2.4', 'yes', 50, 10)")
