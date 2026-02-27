#!/usr/bin/env python3
"""
Quick TastyTrade test to see data structure
"""

import sys
import os
import json
sys.path.append('/Users/cubiczan/.openclaw/workspace/skills/trade-recommender')

from tastytrade_oauth_client import TastytradeClient

client = TastytradeClient()

if client.authenticate():
    print("✅ Authenticated")
    
    # Get accounts
    accounts = client.get_accounts()
    print(f"\nAccounts: {json.dumps(accounts, indent=2)[:500]}...")
    
    if accounts:
        account = accounts[0]
        print(f"\nAccount keys: {list(account.keys())}")
        print(f"Account data: {json.dumps(account['account'], indent=2)}")
        
        # Get balance
        balance = client.get_balance()
        print(f"\nBalance keys: {list(balance.keys()) if balance else 'None'}")
        print(f"Balance data: {json.dumps(balance, indent=2) if balance else 'None'}")
        
        # Try to get SPY quote
        try:
            import urllib.request
            headers = {"Authorization": f"Bearer {client.access_token}"}
            url = f"{client.base_url}/market-data/quotes/SPY"
            
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                print(f"\nSPY Quote structure: {json.dumps(data, indent=2)[:500]}...")
        except Exception as e:
            print(f"\nSPY quote error: {e}")
else:
    print("❌ Authentication failed")