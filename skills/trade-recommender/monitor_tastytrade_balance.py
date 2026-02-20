#!/usr/bin/env python3
"""
Tastytrade Balance Monitor
Checks account balance and alerts when funding appears
"""

import time
from datetime import datetime
from tastytrade_oauth_client import TastytradeClient

def check_balance():
    """Check Tastytrade account balance"""
    client = TastytradeClient()

    if not client.authenticate():
        return None

    accounts = client.get_accounts()
    if not accounts:
        return None

    balance = client.get_balance()
    if balance:
        return {
            "cash": float(balance.get('cash-balance', 0)),
            "buying_power": float(balance.get('buying-power', 0)),
            "net_liq": float(balance.get('net-liquidating-value', 0))
        }
    return None

def main():
    print("=" * 60)
    print("TASTYTRADE BALANCE MONITOR")
    print("=" * 60)
    print()
    print("Checking for $100 funding...")
    print()

    # Check once immediately
    balance = check_balance()
    if balance:
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Cash: ${balance['cash']:,.2f}")
        print(f"  Buying Power: ${balance['buying_power']:,.2f}")
        print(f"  Net Liq: ${balance['net_liq']:,.2f}")
        print()

        if balance['buying_power'] >= 100:
            print("✅ FUNDING DETECTED!")
            print(f"   Account is ready for trading with ${balance['buying_power']:,.2f}")
            return
        else:
            print("⏳ Funding not yet reflected in API")
            print("   This is normal - can take 5-15 minutes for ACH/funding to appear")
            print()
            print("   To check manually:")
            print("   1. Visit: https://my.tastytrade.com/")
            print("   2. Check account balance")
            print("   3. If showing there but not in API, wait a few more minutes")
    else:
        print("❌ Unable to check balance")

    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
