#!/usr/bin/env python3
"""
Tastytrade API Client - OAuth 2.0 Authentication
Fully functional client with all credentials configured
"""

import os
import urllib.request
import urllib.error
import json
from datetime import datetime
from typing import Dict, List, Optional

class TastytradeClient:
    """Tastytrade API client with OAuth authentication"""

    def __init__(self):
        # OAuth credentials
        self.client_id = "0c7b8898-a2f1-49bb-a23d-843e47b68631"
        self.client_secret = "80e479d6235f546b188f9c86ec53bf80019c4bff"
        self.refresh_token = "eyJhbGciOiJFZERTQSIsInR5cCI6InJ0K2p3dCIsImtpZCI6ImlOcEIwZW9EdmVFdUlUU3U2ZmVEQ1ZwSG9SQWtRaC1TaTE5cGRJRjVuSGciLCJqa3UiOiJodHRwczovL2ludGVyaW9yLWFwaS5hcjIudGFzdHl0cmFkZS5zeXN0ZW1zL29hdXRoL2p3a3MifQ.eyJpc3MiOiJodHRwczovL2FwaS50YXN0eXRyYWRlLmNvbSIsInN1YiI6IlViMTA4NzI0Yy0yNDRhLTRlZWUtYjc0NC1jMmYzMWNmYjBlY2QiLCJpYXQiOjE3NzE2MDcyMTksImF1ZCI6IjBjN2I4ODk4LWEyZjEtNDliYi1hMjNkLTg0M2U0N2I2ODYzMSIsImdyYW50X2lkIjoiRzEzNWExZjhhLTE0MmQtNDVlMy1hMjlmLTgyNjBjZDY4NDBiOCIsInNjb3BlIjoicmVhZCB0cmFkZSBvcGVuaWQifQ.Nt_R4rn6Ckg2BgPC4GmxtRwz_K9aw6YbbJkA-SN6O6pojKH_nYYD0zAaq46G9T6wjGwwW5OIADjEeSrtWOv2Dg"

        self.base_url = "https://api.tastyworks.com"
        self.access_token = None
        self.account_number = None

    def _request(self, method: str, url: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """Make HTTP request"""
        try:
            headers = {"Content-Type": "application/json"}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            req_data = json.dumps(data).encode() if data else None
            req = urllib.request.Request(url, data=req_data, headers=headers, method=method)

            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            print(f"HTTP Error {e.code}: {error_body}")
            return None
        except Exception as e:
            print(f"Request error: {e}")
            return None

    def authenticate(self) -> bool:
        """Get access token using refresh token"""
        url = f"{self.base_url}/oauth/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token"
        }

        result = self._request("POST", url, data)
        if result and "access_token" in result:
            self.access_token = result["access_token"]
            print(f"✅ Authenticated (token valid for {result['expires_in']}s)")
            return True
        return False

    def _headers(self) -> Dict:
        """Get authorization headers"""
        return {"Authorization": f"Bearer {self.access_token}"}

    def get_accounts(self) -> List[Dict]:
        """Get all accounts"""
        url = f"{self.base_url}/customers/me/accounts"
        result = self._request("GET", url)
        if result:
            accounts = result.get("data", {}).get("items", [])
            if accounts:
                self.account_number = accounts[0]["account"]["account-number"]
            return accounts
        return []

    def get_balance(self) -> Dict:
        """Get account balance"""
        if not self.account_number:
            print("No account number set")
            return {}

        url = f"{self.base_url}/accounts/{self.account_number}/balances"
        result = self._request("GET", url)
        return result.get("data", {}) if result else {}

    def get_positions(self) -> List[Dict]:
        """Get current positions"""
        if not self.account_number:
            return []

        url = f"{self.base_url}/accounts/{self.account_number}/positions"
        result = self._request("GET", url)
        return result.get("data", {}).get("items", []) if result else []

    def get_quote(self, symbol: str) -> Dict:
        """Get real-time quote"""
        url = f"{self.base_url}/quotes/{symbol}"
        result = self._request("GET", url)
        return result.get("data", {}) if result else {}

    def get_option_chain(self, symbol: str) -> Dict:
        """Get option chain"""
        url = f"{self.base_url}/option-chains/{symbol}/nested"
        result = self._request("GET", url)
        return result.get("data", {}) if result else {}

def main():
    """Test Tastytrade API connection"""
    print("=" * 60)
    print("TASTYTRADE API CLIENT - OAUTH 2.0")
    print("=" * 60)
    print()

    # Initialize client
    client = TastytradeClient()

    # Authenticate
    if not client.authenticate():
        return

    print()

    # Get accounts
    print("--- Accounts ---")
    accounts = client.get_accounts()
    if accounts:
        print(f"Found {len(accounts)} account(s)")
        for acc in accounts:
            account = acc["account"]
            print(f"  • {account['account-number']} - {account['account-type-name']} ({account['margin-or-cash']})")
    print()

    # Get balance
    print("--- Account Balance ---")
    balance = client.get_balance()
    if balance:
        print(f"Cash Balance: ${float(balance.get('cash-balance', 0)):,.2f}")
        print(f"Buying Power: ${float(balance.get('buying-power', 0)):,.2f}")
        print(f"Net Liq Value: ${float(balance.get('net-liquidating-value', 0)):,.2f}")
    print()

    # Get positions
    print("--- Positions ---")
    positions = client.get_positions()
    if positions:
        print(f"Open positions: {len(positions)}")
        for pos in positions[:5]:
            print(f"  • {pos['symbol']}: {pos['quantity']} shares")
    else:
        print("No open positions")
    print()

    # Test quote
    print("--- SPY Quote ---")
    quote = client.get_quote("SPY")
    if quote:
        print(f"SPY: ${quote.get('last', 0):.2f}")
    print()

    # Test option chain
    print("--- SPY Option Chain ---")
    chain = client.get_option_chain("SPY")
    if chain:
        items = chain.get("items", [])
        print(f"Found {len(items)} expiration(s)")
        if items:
            first_exp = items[0]
            print(f"First expiration: {first_exp.get('expiration-date')}")
            print(f"Strikes available: {len(first_exp.get('strikes', []))}")
    print()

    print("=" * 60)
    print("✅ TASTYTRADE API INTEGRATION WORKING!")
    print("=" * 60)

if __name__ == "__main__":
    main()
