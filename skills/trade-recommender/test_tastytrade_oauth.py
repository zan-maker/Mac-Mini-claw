#!/usr/bin/env python3
"""
Tastytrade OAuth Integration - Updated for OAuth 2.0
Requires: client_secret and refresh_token
"""

import os
import sys
from datetime import datetime

# Install instructions
print("=" * 60)
print("TASTYTRADE OAUTH INTEGRATION")
print("=" * 60)
print()
print("Client ID: 0c7b8898-a2f1-49bb-a23d-843e47b68631 ✅")
print()
print("⚠️  Additional credentials needed:")
print("    1. Client Secret (from OAuth app settings)")
print("    2. Refresh Token (generated via 'Create Grant')")
print()
print("See: TASTYTRADE_OAUTH_SETUP.md for instructions")
print()
print("=" * 60)
print()

# Try to import tastytrade SDK
try:
    from tastytrade import Session, Account
    SDK_AVAILABLE = True
    print("✅ tastytrade SDK installed")
except ImportError:
    SDK_AVAILABLE = False
    print("❌ tastytrade SDK not installed")
    print("   Install with: pip3 install --user tastytrade")
    print()

def test_oauth_connection(client_secret: str, refresh_token: str):
    """Test OAuth connection with provided credentials"""

    print("\n--- Testing Connection ---")

    try:
        # Create OAuth session
        session = Session(client_secret, refresh_token)
        print("✅ OAuth session created")

        # Get accounts
        accounts = Account.get(session)
        print(f"✅ Found {len(accounts)} account(s)")

        # Get account details
        if accounts:
            account = accounts[0]
            print(f"\n--- Account: {account.account_number} ---")

            # Get balances
            balances = account.get_balances()
            print(f"Cash Balance: ${balances.cash_balance:,.2f}")
            print(f"Buying Power: ${balances.buying_power:,.2f}")
            print(f"Net Liq Value: ${balances.net_liquidating_value:,.2f}")

            # Get positions
            positions = account.get_positions()
            print(f"\nPositions: {len(positions)}")

            print("\n✅ All tests passed!")
            return True
        else:
            print("⚠️  No accounts found")
            return False

    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    # Check for credentials
    client_secret = os.environ.get("TASTYTRADE_CLIENT_SECRET")
    refresh_token = os.environ.get("TASTYTRADE_REFRESH_TOKEN")

    if not client_secret or not refresh_token:
        print("\n⚠️  Credentials not found in environment")
        print("\nSet environment variables:")
        print("  export TASTYTRADE_CLIENT_SECRET='your-client-secret'")
        print("  export TASTYTRADE_REFRESH_TOKEN='your-refresh-token'")
        print("\nOr provide directly:")
        print("  client_secret = input('Client Secret: ')")
        print("  refresh_token = input('Refresh Token: ')")
        sys.exit(1)

    if not SDK_AVAILABLE:
        print("\n❌ Cannot test - SDK not installed")
        sys.exit(1)

    # Test connection
    success = test_oauth_connection(client_secret, refresh_token)
    sys.exit(0 if success else 1)
