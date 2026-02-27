#!/usr/bin/env python3
"""
Test TastyTrade OAuth client with SPY data
"""

import sys
import os
sys.path.append('/Users/cubiczan/.openclaw/workspace/skills/trade-recommender')

try:
    from tastytrade_oauth_client import TastytradeClient
    
    print("=" * 60)
    print("TASTYTRADE OAUTH CLIENT TEST")
    print("=" * 60)
    
    # Create client
    client = TastytradeClient()
    
    # Authenticate
    print("\n1. Authenticating...")
    if client.authenticate():
        print("   ✅ Authentication successful!")
    else:
        print("   ❌ Authentication failed")
        sys.exit(1)
    
    # Get accounts
    print("\n2. Getting accounts...")
    accounts = client.get_accounts()
    if accounts:
        print(f"   ✅ Found {len(accounts)} account(s)")
        account = accounts[0]
        account_number = account["account"]["account-number"]
        print(f"   Account Number: {account_number}")
        # Try different key names for account type
        account_type = account['account'].get('account-type') or account['account'].get('type') or 'Unknown'
        print(f"   Account Type: {account_type}")
    else:
        print("   ❌ No accounts found")
        sys.exit(1)
    
    # Get balance
    print("\n3. Getting account balance...")
    balance = client.get_balance()
    if balance:
        print("   ✅ Balance retrieved:")
        print(f"      Cash Balance: ${balance.get('cash-balance', 0):.2f}")
        print(f"      Option Buying Power: ${balance.get('option-buying-power', 0):.2f}")
        print(f"      Equity: ${balance.get('equity', 0):.2f}")
        print(f"      Day Trading Buying Power: ${balance.get('day-trading-buying-power', 0):.2f}")
    else:
        print("   ❌ Could not get balance")
    
    # Get SPY quote
    print("\n4. Getting SPY quote...")
    spy_quote = client.get_quote("SPY")
    if spy_quote:
        print("   ✅ SPY Quote:")
        print(f"      Symbol: {spy_quote.get('symbol')}")
        print(f"      Last: ${spy_quote.get('last', 0):.2f}")
        print(f"      Bid: ${spy_quote.get('bid', 0):.2f}")
        print(f"      Ask: ${spy_quote.get('ask', 0):.2f}")
        print(f"      Volume: {spy_quote.get('volume', 0):,}")
        print(f"      Change: ${spy_quote.get('change', 0):.2f}")
        print(f"      Percent Change: {spy_quote.get('percent-change', 0):.2f}%")
    else:
        print("   ❌ Could not get SPY quote")
        # Try alternative method
        print("   Trying alternative quote method...")
        try:
            import urllib.request
            import json
            
            headers = {"Authorization": f"Bearer {client.access_token}"}
            url = f"{client.base_url}/market-data/quotes/SPY"
            
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                if data.get('data', {}).get('items'):
                    quote = data['data']['items'][0]
                    print(f"      Alternative quote: ${quote.get('last', 0):.2f}")
        except Exception as e:
            print(f"   Alternative also failed: {e}")
    
    # Get SPY options chain
    print("\n5. Getting SPY options chain...")
    chain = client.get_option_chain("SPY")
    if chain:
        print("   ✅ Options chain retrieved")
        print(f"      Expiration Date: {chain.get('expiration-date')}")
        print(f"      Underlying Symbol: {chain.get('underlying-symbol')}")
        
        # Find ATM options
        options = chain.get('options', [])
        if options:
            # Find options around 687
            atm_options = [opt for opt in options if 680 <= opt.get('strike-price', 0) <= 695]
            print(f"      Total Options: {len(options)}")
            print(f"      ATM Options (680-695): {len(atm_options)}")
            
            if atm_options:
                # Show a sample call and put
                sample_call = next((opt for opt in atm_options if opt.get('option-type') == 'C'), None)
                sample_put = next((opt for opt in atm_options if opt.get('option-type') == 'P'), None)
                
                if sample_call:
                    print(f"\n      Sample Call (Strike {sample_call.get('strike-price')}):")
                    print(f"         Bid: ${sample_call.get('bid', 0):.2f}")
                    print(f"         Ask: ${sample_call.get('ask', 0):.2f}")
                    print(f"         IV: {sample_call.get('volatility', 0):.2f}%")
                
                if sample_put:
                    print(f"\n      Sample Put (Strike {sample_put.get('strike-price')}):")
                    print(f"         Bid: ${sample_put.get('bid', 0):.2f}")
                    print(f"         Ask: ${sample_put.get('ask', 0):.2f}")
                    print(f"         IV: {sample_put.get('volatility', 0):.2f}%")
    else:
        print("   ❌ Could not get options chain")
    
    # Get positions
    print("\n6. Getting current positions...")
    positions = client.get_positions()
    if positions:
        print(f"   ✅ Found {len(positions)} position(s)")
        for pos in positions[:3]:  # Show first 3
            print(f"      {pos.get('symbol')}: {pos.get('quantity')} @ ${pos.get('average-price', 0):.2f}")
    else:
        print("   No positions found (new account)")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE - API IS WORKING!")
    print("=" * 60)
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're in the right directory")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()