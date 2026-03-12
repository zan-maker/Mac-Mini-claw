#!/usr/bin/env python3
"""
Test Kalshi API using official Python SDK
"""

import os
import json
from datetime import datetime
from kalshi_python import Configuration, KalshiClient

def test_with_official_sdk():
    """Test using official Kalshi Python SDK"""
    print("🔗 TESTING WITH OFFICIAL KALSHI PYTHON SDK")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Load credentials
    config_file = "/Users/cubiczan/.openclaw/workspace/secrets/kalshi_config.json"
    if not os.path.exists(config_file):
        print("❌ Config file not found")
        return False
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    key_id = config.get("key_id", "")
    private_key_pem = config.get("private_key", "")
    
    print(f"✅ Credentials loaded")
    print(f"📋 Key ID: {key_id}")
    
    try:
        # Configure the client
        api_config = Configuration(
            host="https://api.elections.kalshi.com/trade-api/v2"
        )
        
        # Set API credentials
        api_config.api_key_id = key_id
        api_config.private_key_pem = private_key_pem
        
        # Initialize client
        client = KalshiClient(api_config)
        
        print(f"✅ Kalshi client initialized")
        
        # Test 1: Get balance
        print(f"\n1. 📊 GETTING ACCOUNT BALANCE...")
        try:
            balance = client.get_balance()
            print(f"   ✅ Balance: ${balance.balance / 100:.2f}")
            print(f"   💰 Buying Power: ${balance.buying_power / 100:.2f}")
            print(f"   📈 Portfolio Value: ${balance.portfolio_value / 100:.2f}")
        except Exception as e:
            print(f"   ❌ Balance error: {e}")
            return False
        
        # Test 2: Get markets
        print(f"\n2. 📈 GETTING MARKETS...")
        try:
            markets = client.get_markets(limit=5)
            print(f"   ✅ Markets loaded: {len(markets.markets)}")
            
            if markets.markets:
                market = markets.markets[0]
                print(f"   📊 Sample market: {market.ticker}")
                print(f"   📝 Title: {market.title}")
                print(f"   💰 YES price: ${market.yes_price / 100:.2f}")
                print(f"   💰 NO price: ${market.no_price / 100:.2f}")
                
                # Return market for potential trading
                return {
                    "balance": balance,
                    "market": market,
                    "client": client
                }
        except Exception as e:
            print(f"   ❌ Markets error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ SDK initialization error: {e}")
        return False

def execute_test_trade_sdk(client, market_ticker):
    """Execute $1 test trade using SDK"""
    print(f"\n3. 💰 EXECUTING $1 TEST TRADE (SDK)...")
    print(f"   Ticker: {market_ticker}")
    
    # SAFETY FIRST - Simulated mode
    print(f"   🔒 SAFE MODE: Trade will be SIMULATED")
    print(f"   To execute real trade, change simulated=False")
    
    simulated = True  # SAFETY FIRST
    
    if not simulated:
        try:
            # Create order
            order = client.create_order(
                ticker=market_ticker,
                action="buy",
                side="yes",
                count=2,  # 2 shares at $0.50 each = $1.00
                price=50,  # 50 cents = $0.50
                client_order_id=f"test_sdk_{int(datetime.now().timestamp())}",
                type="limit"
            )
            
            print(f"   ✅ Trade executed successfully!")
            print(f"   📋 Order ID: {order.order_id}")
            print(f"   📊 Status: {order.status}")
            print(f"   💰 Cost: ${order.cost / 100:.2f}")
            return order
            
        except Exception as e:
            print(f"   ❌ Trade error: {e}")
            return None
    else:
        print(f"   🔒 SIMULATED: Trade NOT executed")
        print(f"   Ready for real trading with SDK")
        return {"simulated": True, "ticker": market_ticker}

def main():
    """Main function"""
    # Test with official SDK
    result = test_with_official_sdk()
    
    if result:
        print("\n" + "=" * 60)
        print("🎉 OFFICIAL SDK WORKS!")
        print("=" * 60)
        
        balance = result["balance"]
        market = result["market"]
        client = result["client"]
        
        print(f"📊 ACCOUNT STATUS:")
        print(f"   Balance: ${balance.balance / 100:.2f}")
        print(f"   Buying Power: ${balance.buying_power / 100:.2f}")
        print(f"   Portfolio Value: ${balance.portfolio_value / 100:.2f}")
        
        print(f"\n📈 MARKET READY:")
        print(f"   Ticker: {market.ticker}")
        print(f"   Title: {market.title}")
        print(f"   YES price: ${market.yes_price / 100:.2f}")
        print(f"   NO price: ${market.no_price / 100:.2f}")
        
        # Test trade (simulated)
        trade_result = execute_test_trade_sdk(client, market.ticker)
        
        print("\n" + "=" * 60)
        print("🚀 READY FOR REAL TRADING:")
        print("1. Change simulated=False in line 86")
        print("2. Run script again")
        print("3. Check Kalshi dashboard for $1 test trade")
        print("4. Scale up to larger positions")
        print("=" * 60)
        
    else:
        print("\n❌ SDK TEST FAILED")
        print("Possible issues:")
        print("1. API key not activated in Kalshi account")
        print("2. Key doesn't have trading permissions")
        print("3. Need to enable API access in account settings")
        print("4. Check Kalshi dashboard for API key status")

if __name__ == "__main__":
    main()