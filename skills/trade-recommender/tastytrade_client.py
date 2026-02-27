#!/usr/bin/env python3
"""
Tastytrade API Integration for Trade Recommender
Provides options chain data, account info, and order execution capabilities
"""

import os
import sys
from typing import Optional, Dict, List
import json

# Try to import tastytrade SDK
try:
    from tastytrade_sdk import Tastytrade
    from tastytrade_sdk.account import Account
    from tastytrade_sdk.instruments import Instrument, OptionChain
    from tastytrade_sdk.orders import Order
    from tastytrade_sdk.quote import Quote
except ImportError:
    print("ERROR: tastytrade-sdk not installed")
    print("Install with: pip3 install tastytrade-sdk")
    sys.exit(1)

class TastytradeAPI:
    """Tastytrade API client for trade recommender"""

    def __init__(self, api_key: str):
        """Initialize Tastytrade client with API key"""
        self.api_key = api_key
        self.client = None
        self.account = None

    def connect(self) -> bool:
        """Connect to Tastytrade API"""
        try:
            self.client = Tastytrade(api_key=self.api_key)
            # Get first account
            accounts = self.client.get_accounts()
            if accounts:
                self.account = accounts[0]
                print(f"✅ Connected to Tastytrade account: {self.account.account_number}")
                return True
            else:
                print("❌ No accounts found")
                return False
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    def get_account_balance(self) -> Dict:
        """Get account balance and buying power"""
        try:
            balances = self.account.get_balances()
            return {
                "cash": balances.cash_balance,
                "buying_power": balances.buying_power,
                "net_liquidating_value": balances.net_liquidating_value,
                "equity_buying_power": balances.equity_buying_power,
                "options_buying_power": balances.options_buying_power
            }
        except Exception as e:
            print(f"Error getting balance: {e}")
            return {}

    def get_positions(self) -> List[Dict]:
        """Get current positions"""
        try:
            positions = self.account.get_positions()
            return [
                {
                    "symbol": pos.symbol,
                    "quantity": pos.quantity,
                    "average_price": pos.average_price,
                    "market_value": pos.market_value,
                    "unrealized_pnl": pos.unrealized_pnl,
                    "realized_pnl": pos.realized_pnl
                }
                for pos in positions
            ]
        except Exception as e:
            print(f"Error getting positions: {e}")
            return []

    def get_option_chain(self, symbol: str) -> List[Dict]:
        """Get option chain for a symbol"""
        try:
            chain = OptionChain.get(self.client, symbol)
            options = []

            for expiration in chain.expirations:
                for strike in expiration.strikes:
                    if strike.call:
                        options.append({
                            "type": "call",
                            "strike": strike.strike_price,
                            "expiration": expiration.expiration_date,
                            "symbol": strike.call.symbol,
                            "bid": strike.call.bid,
                            "ask": strike.call.ask,
                            "delta": strike.call.delta,
                            "gamma": strike.call.gamma,
                            "theta": strike.call.theta,
                            "vega": strike.call.vega,
                            "implied_volatility": strike.call.implied_volatility,
                            "open_interest": strike.call.open_interest,
                            "volume": strike.call.volume
                        })
                    if strike.put:
                        options.append({
                            "type": "put",
                            "strike": strike.strike_price,
                            "expiration": expiration.expiration_date,
                            "symbol": strike.put.symbol,
                            "bid": strike.put.bid,
                            "ask": strike.put.ask,
                            "delta": strike.put.delta,
                            "gamma": strike.put.gamma,
                            "theta": strike.put.theta,
                            "vega": strike.put.vega,
                            "implied_volatility": strike.put.implied_volatility,
                            "open_interest": strike.put.open_interest,
                            "volume": strike.put.volume
                        })

            return options
        except Exception as e:
            print(f"Error getting option chain: {e}")
            return []

    def get_quote(self, symbol: str) -> Dict:
        """Get real-time quote for a symbol"""
        try:
            quote = Quote.get(self.client, symbol)
            return {
                "symbol": quote.symbol,
                "bid": quote.bid,
                "ask": quote.ask,
                "last": quote.last,
                "volume": quote.volume,
                "high": quote.high,
                "low": quote.low,
                "open": quote.open,
                "close": quote.close
            }
        except Exception as e:
            print(f"Error getting quote: {e}")
            return {}

    def place_order(self, order_data: Dict) -> Dict:
        """Place an order (for paper trading or live)"""
        try:
            # This is a simplified example - you'll need to build proper Order objects
            order = Order(
                account=self.account,
                symbol=order_data["symbol"],
                quantity=order_data["quantity"],
                order_type=order_data.get("order_type", "limit"),
                price=order_data.get("price"),
                side=order_data["side"]  # "buy" or "sell"
            )

            result = self.account.place_order(order)
            return {
                "success": True,
                "order_id": result.id,
                "status": result.status
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

def main():
    """Test Tastytrade API connection"""
    api_key = os.environ.get("TASTYTRADE_API_KEY", "80e479d6235f546b188f9c86ec53bf80019c4bff")

    print("============================================================")
    print("TASTYTRADE API TEST")
    print("============================================================\n")

    # Initialize client
    tasty = TastytradeAPI(api_key)

    # Connect
    if not tasty.connect():
        sys.exit(1)

    print("\n--- Account Balance ---")
    balance = tasty.get_account_balance()
    for key, value in balance.items():
        print(f"{key}: ${value:,.2f}")

    print("\n--- SPY Option Chain (first 5 calls) ---")
    chain = tasty.get_option_chain("SPY")
    for opt in chain[:5]:
        if opt["type"] == "call":
            print(f"{opt['symbol']}: Strike ${opt['strike']:.2f} | "
                  f"Bid ${opt['bid']:.2f} Ask ${opt['ask']:.2f} | "
                  f"Delta {opt['delta']:.2f}")

    print("\n--- SPY Quote ---")
    quote = tasty.get_quote("SPY")
    print(f"SPY: ${quote['last']:.2f} | "
          f"Bid ${quote['bid']:.2f} Ask ${quote['ask']:.2f}")

    print("\n✅ Tastytrade API test complete!")

if __name__ == "__main__":
    main()
