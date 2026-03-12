#!/usr/bin/env python3
"""
Test actual Kalshi API connectivity with real $1 trade
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
    """Test Kalshi API with real connectivity"""
    
    def __init__(self):
        self.config = self.load_config()
        self.base_url = "https://trading-api.kalshi.com/v1"
        
    def load_config(self):
        """Load Kalshi configuration"""
        config_file = "/Users/cubiczan/.openclaw/workspace/secrets/kalshi_config.json"
        if not os.path.exists(config_file):
            print("❌ Config file not found")
            return None
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        print(f"✅ Credentials loaded")
        print(f"📋 Key ID: {config.get('key_id', '')[:8]}...")
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
    
    def test_account_endpoint(self):
        """Test /account endpoint"""
        print("\n1. 📊 TESTING ACCOUNT ENDPOINT...")
        
        path = "/account"
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
                print(f"   💰 Balance: ${account_data.get('balance_cents', 0)/100:.2f}")
                print(f"   💳 Buying Power: ${account_data.get('buying_power_cents', 0)/100:.2f}")
                return account_data
            else:
                print(f"   ❌ Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
            return None
    
    def test_markets_endpoint(self):
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
                
                # Find gas market
                gas_markets = [m for m in markets if 'gas' in m.get('title', '').lower()]
                if gas_markets:
                    market = gas_markets[0]
                    print(f"   📊 Gas market found: {market.get('ticker')}")
                    print(f"   📝 Title: {market.get('title')}")
                    print(f"   💰 YES ask: ${market.get('yes_ask', 0)/100:.2f}")
                    print(f"   💰 NO ask: ${market.get('no_ask', 0)/100:.2f}")
                    return market
                else:
                    print("   ℹ️  No gas markets found")
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
        
        # Trade parameters for $1 test (2 shares at ~$0.50 each)
        trade_data = {
            "ticker": market_ticker,
            "side": "yes",  # Start with YES
            "count": 2,     # 2 shares
            "price": 50,    # 50 cents = $0.50
            "client_order_id": f"test_{int(time.time())}"
        }
        
        path = "/orders"
        body = json.dumps(trade_data)
        headers = self.generate_signature("POST", path, body)
        
        if not headers:
            print("   ❌ Failed to generate signature")
            return None
        
        print(f"   📋 Trade details:")
        print(f"      Side: {trade_data['side'].upper()}")
        print(f"      Shares: {trade_data['count']}")
        print(f"      Price: ${trade_data['price']/100:.2f}")
        print(f"      Total: ${trade_data['count'] * trade_data['price']/100:.2f}")
        print(f"      Order ID: {trade_data['client_order_id']}")
        
        # Ask for confirmation
        print(f"\n   ⚠️  WARNING: This will execute a REAL $1 trade")
        print(f"   Do you want to proceed? (y/n): ", end="")
        
        # For safety, we'll simulate unless explicitly enabled
        # In production, you would read user input here
        proceed = False  # Default to safe mode
        
        if proceed:
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
                    return order_data
                else:
                    print(f"   ❌ Error: {response.text}")
                    return None
                    
            except Exception as e:
                print(f"   ❌ Request failed: {e}")
                return None
        else:
            print(f"   🔒 SAFE MODE: Trade NOT executed")
            print(f"   To execute real trade, set proceed=True")
            return {"simulated": True, "trade_data": trade_data}
    
    def run_tests(self):
        """Run all tests"""
        print("🔗 TESTING KALSHI API CONNECTIVITY")
        print("=" * 60)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Test 1: Account endpoint
        account = self.test_account_endpoint()
        if not account:
            print("   ❌ Account test failed - stopping")
            return False
        
        # Test 2: Markets endpoint
        market = self.test_markets_endpoint()
        if not market:
            print("   ⚠️  Markets test issues - continuing")
        
        # Test 3: Execute trade (if we have a market)
        if market:
            trade_result = self.execute_test_trade(market.get('ticker'))
        else:
            # Use a known ticker for testing
            trade_result = self.execute_test_trade("GASMONTH-3.50")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY:")
        print(f"   Account test: {'✅' if account else '❌'}")
        print(f"   Markets test: {'✅' if market else '⚠️'}")
        print(f"   Trade test: {'✅ Simulated' if trade_result and trade_result.get('simulated') else '⚠️ Not executed'}")
        
        print("\n🎯 NEXT STEPS:")
        print("1. Check Kalshi dashboard for API key status")
        print("2. Verify the $1 test trade appears (if executed)")
        print("3. Monitor trade performance")
        print("4. Scale up to larger positions")
        
        return True

def main():
    """Main function"""
    tester = KalshiAPITester()
    
    if not tester.config:
        print("❌ Failed to load configuration")
        return
    
    tester.run_tests()

if __name__ == "__main__":
    main()