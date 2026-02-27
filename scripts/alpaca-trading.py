#!/usr/bin/env python3
"""
Alpaca Paper Trading Integration for Trade Recommender
"""

import requests
import json
from datetime import datetime

# Alpaca Paper Trading Credentials
ALPACA_ENDPOINT = "https://paper-api.alpaca.markets/v2"
ALPACA_KEY = "PKNDK5P66FCRH5P5ILPTVCYE7D"
ALPACA_SECRET = "z1fwAHFV9H8NY26XrZ2sSSxJggc8BwqiU2gPxVsy49V"

HEADERS = {
    "APCA-API-KEY-ID": ALPACA_KEY,
    "APCA-API-SECRET-KEY": ALPACA_SECRET
}

def get_account():
    """Get account information"""
    response = requests.get(f"{ALPACA_ENDPOINT}/account", headers=HEADERS)
    return response.json()

def get_positions():
    """Get current positions"""
    response = requests.get(f"{ALPACA_ENDPOINT}/positions", headers=HEADERS)
    return response.json()

def get_orders(status="open"):
    """Get orders by status"""
    response = requests.get(f"{ALPACA_ENDPOINT}/orders?status={status}", headers=HEADERS)
    return response.json()

def place_order(symbol, qty, side, order_type="market", time_in_force="gtc"):
    """Place an order
    
    Args:
        symbol: Stock symbol (e.g., "AAPL")
        qty: Number of shares
        side: "buy" or "sell"
        order_type: "market", "limit", "stop", "stop_limit"
        time_in_force: "day", "gtc", "opg", "cls", "ioc", "fok"
    """
    data = {
        "symbol": symbol,
        "qty": str(qty),
        "side": side,
        "type": order_type,
        "time_in_force": time_in_force
    }
    response = requests.post(f"{ALPACA_ENDPOINT}/orders", headers=HEADERS, json=data)
    return response.json()

def place_limit_order(symbol, qty, side, limit_price, time_in_force="gtc"):
    """Place a limit order"""
    data = {
        "symbol": symbol,
        "qty": str(qty),
        "side": side,
        "type": "limit",
        "limit_price": str(limit_price),
        "time_in_force": time_in_force
    }
    response = requests.post(f"{ALPACA_ENDPOINT}/orders", headers=HEADERS, json=data)
    return response.json()

def cancel_order(order_id):
    """Cancel an order"""
    response = requests.delete(f"{ALPACA_ENDPOINT}/orders/{order_id}", headers=HEADERS)
    return response.status_code == 204

def get_portfolio_history(period="1M", timeframe="1D"):
    """Get portfolio history"""
    params = {"period": period, "timeframe": timeframe}
    response = requests.get(f"{ALPACA_ENDPOINT}/account/portfolio/history", 
                           headers=HEADERS, params=params)
    return response.json()

def get_assets(status="active", asset_class="us_equity"):
    """Get list of assets"""
    params = {"status": status, "asset_class": asset_class}
    response = requests.get(f"{ALPACA_ENDPOINT}/assets", headers=HEADERS, params=params)
    return response.json()

def get_quote(symbol):
    """Get real-time quote"""
    # Note: This requires market data subscription
    # For paper trading, may return delayed data
    response = requests.get(f"https://data.alpaca.markets/v2/stocks/{symbol}/quotes/latest",
                           headers=HEADERS)
    return response.json()

def get_bars(symbol, timeframe="1D", limit=100):
    """Get historical price bars"""
    params = {"limit": limit}
    response = requests.get(
        f"https://data.alpaca.markets/v2/stocks/{symbol}/bars?timeframe={timeframe}",
        headers=HEADERS,
        params=params
    )
    return response.json()

def execute_recommendation(recommendation, symbol, confidence, current_price):
    """Execute a trade based on recommendation
    
    Args:
        recommendation: "STRONG_BUY", "BUY", "HOLD", "SELL", "STRONG_SELL"
        symbol: Stock symbol
        confidence: 0-100 confidence score
        current_price: Current stock price
    """
    account = get_account()
    buying_power = float(account.get("buying_power", 0))
    
    # Get current positions
    positions = get_positions()
    current_position = next((p for p in positions if p["symbol"] == symbol), None)
    
    result = {
        "action": "none",
        "reason": "",
        "order": None
    }
    
    if recommendation in ["STRONG_BUY", "BUY"]:
        # Calculate position size based on confidence and buying power
        max_position = buying_power * 0.1  # Max 10% of portfolio per trade
        position_size = max_position * (confidence / 100)
        qty = int(position_size / current_price)
        
        if qty > 0:
            result["action"] = "buy"
            result["reason"] = f"Recommendation: {recommendation}, Confidence: {confidence}%"
            result["order"] = place_order(symbol, qty, "buy")
            
    elif recommendation in ["SELL", "STRONG_SELL"]:
        if current_position:
            qty = int(current_position["qty"])
            if qty > 0:
                result["action"] = "sell"
                result["reason"] = f"Recommendation: {recommendation}, Confidence: {confidence}%"
                result["order"] = place_order(symbol, qty, "sell")
        else:
            result["reason"] = "No position to sell"
    
    return result

if __name__ == "__main__":
    print("\n" + "="*50)
    print("Alpaca Paper Trading Account Status")
    print("="*50 + "\n")
    
    # Get account info
    account = get_account()
    print(f"Account Status: {account.get('status', 'N/A')}")
    print(f"Buying Power: ${float(account.get('buying_power', 0)):,.2f}")
    print(f"Cash: ${float(account.get('cash', 0)):,.2f}")
    print(f"Portfolio Value: ${float(account.get('portfolio_value', 0)):,.2f}")
    
    # Get positions
    positions = get_positions()
    print(f"\nOpen Positions: {len(positions)}")
    for pos in positions:
        print(f"  - {pos['symbol']}: {pos['qty']} shares @ ${float(pos['avg_entry_price']):.2f}")
    
    # Get open orders
    orders = get_orders("open")
    print(f"\nOpen Orders: {len(orders)}")
    for order in orders:
        print(f"  - {order['symbol']}: {order['side']} {order['qty']} @ ${order.get('limit_price', 'market')}")
    
    print("\n" + "="*50 + "\n")
