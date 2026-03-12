#!/usr/bin/env python3
"""
Test Kalshi API with correct endpoints
Balance: /portfolio/balance
Markets: /markets
Orders: /orders
"""

import os
import json
import time
import base64
import requests
from datetime import datetime
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class KalshiAPITester:
    """Test Kalshi API with correct endpoints"""
    
    def __init__(self, execute_real_trade=False):
        self.config = self.load_config()
        self.base_url = "https://api.elections.kalshi.com/trade-api/v2"
        self.execute_real_trade = execute_real_trade  # Safety flag
        
    def load_config(self):
        """Load Kalshi configuration"""
        config_file = "/Users/cubiczan/.openclaw/workspace/secrets/kalshi_config.json"
        if not os.path.exists(config_file):
            print("❌ Config file not found")
            return None
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        print(f"✅ Credentials loaded")
        print(f"📋 Key ID: {config.get('key_id', '')}")
        print(f"🔑 Private Key: {len(config.get('private_key', ''))} chars")
        
        return config
    
    def generate_signature(self, method: str, path: str, body: str = ""):
        """Generate Kalshi API signature using RSA"""
        if not self.config:
            return None
        
        key_id = self.config.get("key_id", "")
        private_key_pem = self.config.get("private_key", "")
        
        if not key_id or not private_key_pem:
            print("❌ Missing credentials for signature")
            return None
        
        timestamp = str(int(time.time()))
        message = f"{method}{path}{timestamp}{body}"
        
        try:
            # Load private key
            private_key = serialization.load_pem_private_key(
                private_key_pem.encode(),
                password=None
            )
            
            # Sign the message
            signature = private_key.sign(
                message.encode(),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            
            # Base64 encode
            signature_b64 = base64.b64encode(signature).decode()
            
            headers = {
                "KALSHI-ACCESS-KEY": key_id,
                "KALSHI-ACCESS-SIGNATURE": signature_b64,
                "KALSHI-ACCESS-TIMESTAMP": timestamp,
                "Content-Type": "application/json"
            }
            
            return headers
            
        except Exception as e:
            print(f"❌ Error generating signature: {e}")
            return None
    
    def test_account_balance(self):
        """Test /portfolio/balance endpoint"""
        print("\n1. 📊 TESTING ACCOUNT BALANCE...")
        
        path = "/portfolio/balance"  # CORRECT PATH
        headers = self.generate_signature("GET", path)
        
        if not headers:
            print("   ❌ Failed to generate signature")
            return None
        
        try:
            response = requests.get(
                f"{self.base_url}{path}",
                headers=headers,
                timeout=10
            )
            
            print(f"   📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                account_data = response.json()
                print(f"   ✅ Account data received")
                print(f"   💰 Balance: ${account_data.get('balance', 0)/100:.2f}")
                print(f"   📈 Portfolio Value: ${account_data.get('portfolio_value', 0)/100:.2f}")
                print(f"   💳 Buying Power: ${account_data.get('buying_power', 0)/100:.2f}")
                print(f"   📊 Updated: {account_data.get('updated_ts', 'unknown')}")
                return account_data
            else:
                print(f"   ❌ Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
            return None
    
    def test_markets(self):
        """Test /markets endpoint"""
        print("\n2. 📈 TESTING MARKETS ENDPOINT...")
        
        path = "/markets"
        headers = self.generate_signature("GET", path)
        
        if not headers:
            print("   ❌ Failed to generate signature")
            return None
        
        try:
            response = requests.get(
                f"{self.base_url}{path}",
                headers=headers,
                timeout=10
            )
            
            print(f"   📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                markets_data = response.json()
                markets = markets_data.get('markets', [])
                print(f"   ✅ Markets loaded: {len(markets)}")
                
                # Find simple markets (not complex cross-category)
                simple_markets = []
                for market in markets:
                    ticker = market.get('ticker', '')
                    title = market.get('title', '').lower()
                    
                    # Look for simple yes/no markets
                    if 'crosscategory' not in ticker.lower() and 'yes' in title and 'no' in title:
                        simple_markets.append(market)
                
                if simple_markets:
                    market = simple_markets[0]
                    print(f"   📊 Simple market found: {market.get('ticker')}")
                    print(f"   📝 Title: {market.get('title')}")
                    print(f"   💰 YES price: ${market.get('yes_price', 0)/100:.2f}")
                    print(f"   💰 NO price: ${market.get('no_price', 0)/100:.2f}")
                    return market
                elif markets:
                    # Use first market if no simple ones
                    market = markets[0]
                    print(f"   📊 First market: {market.get('ticker')}")
                    print(f"   📝 Title: {market.get('title')}")
                    return market
                else:
                    print(f"   ℹ️  No markets found")
                    return None
            else:
                print(f"   ❌ Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
            return None
    
    def execute_test_trade(self, market_ticker: str):
        """Execute $1 test trade"""
        print(f"\n3. 💰 EXECUTING $1 TEST TRADE...")
        print(f"   Ticker: {market_ticker}")
        
        # Trade parameters for $1 test
        trade_data = {
            "ticker": market_ticker,
            "action": "buy",  # buy or sell
            "side": "yes",    # yes or no
            "count": 2,       # 2 shares at $0.50 each = $1.00
            "price": 50,      # 50 cents = $0.50
            "client_order_id": f"test_{int(time.time())}",
            "type": "limit"   # limit order
        }
        
        path = "/orders"
        body = json.dumps(trade_data)
        headers = self.generate_signature("POST", path, body)
        
        if not headers:
            print("   ❌ Failed to generate signature")
            return None
        
        print(f"   📋 Trade details:")
        print(f"      Action: {trade_data['action'].upper()}")
        print(f"      Side: {trade_data['side'].upper()}")
        print(f"      Shares: {trade_data['count']}")
        print(f"      Price: ${trade_data['price']/100:.2f}")
        print(f"      Total: ${trade_data['count'] * trade_data['price']/100:.2f}")
        print(f"      Order ID: {trade_data['client_order_id']}")
        
        if self.execute_real_trade:
            print(f"\n   ⚠️  WARNING: Executing REAL $1 trade!")
            print(f"   Check Kalshi dashboard for order confirmation")
            
            try:
                response = requests.post(
                    f"{self.base_url}{path}",
                    json=trade_data,
                    headers=headers,
                    timeout=10
                )
                
                print(f"   📊 Status: {response.status_code}")
                
                if response.status_code == 200:
                    order_data = response.json()
                    print(f"   ✅ Trade executed successfully!")
                    print(f"   📋 Order ID: {order_data.get('order_id')}")
                    print(f"   📊 Status: {order_data.get('status')}")
                    print(f"   💰 Cost: ${order_data.get('cost', 0)/100:.2f}")
                    return order_data
                else:
                    print(f"   ❌ Error: {response.text}")
                    return None
                    
            except Exception as e:
                print(f"   ❌ Request failed: {e}")
                return None
        else:
            print(f"\n   🔒 SAFE MODE: Trade NOT executed")
            print(f"   To execute real trade, set execute_real_trade=True")
            return {"simulated": True, "trade_data": trade_data}
    
    def run_tests(self):
        """Run all tests"""
        print("🔗 TESTING KALSHI API CONNECTIVITY")
        print("=" * 60)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 API Endpoint: {self.base_url}")
        print(f"🔐 Execute Real Trade: {self.execute_real_trade}")
        print("=" * 60)
        
        # Test 1: Account balance
        account = self.test_account_balance()
        if not account:
            print("   ❌ Account test failed - check API key permissions")
            return False
        
        # Test 2: Markets
        market = self.test_markets()
        if not market:
            print("   ❌ Markets test failed")
            return False
        
        # Test 3: Execute trade
        trade_result = self.execute_test_trade(market.get('ticker'))
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY:")
        print(f"   API Endpoint: {self.base_url}")
        print(f"   Account Balance: ${account.get('balance', 0)/100:.2f}")
        print(f"   Buying Power: ${account.get('buying_power', 0)/100:.2f}")
        print(f"   Markets Loaded: ✅")
        print(f"   Trade Execution: {'✅ REAL' if trade_result and not trade_result.get('simulated') else '🔒 SIMULATED'}")
        
        if trade_result and not trade_result.get('simulated'):
            print(f"\n🎯 REAL TRADE EXECUTED!")
            print(f"   Check Kalshi dashboard for order: {trade_result.get('order_id')}")
            print(f"   Monitor trade performance")
            print(f"   Scale up to larger positions")
        else:
            print(f"\n🎯 READY FOR REAL TRADING:")
            print(f"   Change execute_real_trade=True")
            print(f"   Run script again")
            print(f"   Check Kalshi dashboard for $1 test trade")
        
        return True

def main():
    """Main function"""
    # SAFETY FIRST - Set to True only when ready for real trades
    execute_real_trade = False  # CHANGE TO TRUE FOR REAL TRADES
    
    tester = KalshiAPITester(execute_real_trade=execute_real_trade)
    
    if not tester.config:
        print("❌ Failed to load configuration")
        return
    
    tester.run_tests()

if __name__ == "__main__":
    main()