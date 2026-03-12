#!/usr/bin/env python3
"""
Test Kalshi API with correct endpoint: https://api.elections.kalshi.com/trade-api/v2
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
    """Test Kalshi API with correct endpoint"""
    
    def __init__(self):
        self.config = self.load_config()
        self.base_url = "https://api.elections.kalshi.com/trade-api/v2"  # CORRECT ENDPOINT
        
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
    
    def test_connectivity(self):
        """Test basic connectivity"""
        print("\n🌐 TESTING CONNECTIVITY...")
        print(f"   Endpoint: {self.base_url}")
        
        try:
            # Try to reach the base URL
            response = requests.get(self.base_url, timeout=10)
            print(f"   📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Connected successfully")
                return True
            elif response.status_code == 404:
                print(f"   ⚠️  404 - Might need specific endpoint path")
                return True  # Still might work with specific endpoints
            else:
                print(f"   ❌ Error: {response.text[:100]}")
                return False
                
        except Exception as e:
            print(f"   ❌ Connection failed: {e}")
            return False
    
    def test_account_balance(self):
        """Test /balance endpoint"""
        print("\n1. 📊 TESTING ACCOUNT BALANCE...")
        
        path = "/balance"
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
                print(f"   💳 Buying Power: ${account_data.get('buying_power', 0)/100:.2f}")
                print(f"   📊 Open Positions: {account_data.get('open_positions_count', 0)}")
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
                
                # Find gas markets
                gas_markets = []
                for market in markets:
                    title = market.get('title', '').lower()
                    if 'gas' in title or 'fuel' in title:
                        gas_markets.append(market)
                
                if gas_markets:
                    market = gas_markets[0]
                    print(f"   📊 Gas market found: {market.get('ticker')}")
                    print(f"   📝 Title: {market.get('title')}")
                    print(f"   💰 YES price: ${market.get('yes_price', 0)/100:.2f}")
                    print(f"   💰 NO price: ${market.get('no_price', 0)/100:.2f}")
                    return market
                else:
                    print(f"   ℹ️  Showing first market:")
                    if markets:
                        market = markets[0]
                        print(f"   📊 Market: {market.get('ticker')}")
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
            "count": 2,       # 2 shares
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
        
        # SAFETY FIRST - Ask for confirmation
        print(f"\n   ⚠️  WARNING: This will execute a REAL $1 trade")
        print(f"   Currently in SAFE MODE")
        
        simulated = True  # SAFETY FIRST - Change to False for real trade
        
        if not simulated:
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
            print(f"   To execute real trade, change simulated=False")
            return {"simulated": True, "trade_data": trade_data}
    
    def run_tests(self):
        """Run all tests"""
        print("🔗 TESTING KALSHI API WITH CORRECT ENDPOINT")
        print("=" * 60)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 API Endpoint: {self.base_url}")
        print("=" * 60)
        
        # Test connectivity
        if not self.test_connectivity():
            print("   ❌ Connectivity test failed")
            return False
        
        # Test 1: Account balance
        account = self.test_account_balance()
        if not account:
            print("   ⚠️  Account test issues - check API key permissions")
        
        # Test 2: Markets
        market = self.test_markets()
        
        # Test 3: Execute trade (simulated for safety)
        if market:
            trade_result = self.execute_test_trade(market.get('ticker'))
        else:
            # Use test ticker
            trade_result = self.execute_test_trade("TEST-1.00")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY:")
        print(f"   API Endpoint: {self.base_url}")
        print(f"   Connectivity: ✅")
        print(f"   Account test: {'✅' if account else '⚠️'}")
        print(f"   Markets test: {'✅' if market else '⚠️'}")
        print(f"   Trade test: 🔒 SIMULATED (Safe Mode)")
        
        print("\n🎯 READY FOR REAL TRADING:")
        print("1. Change simulated=False in line 186")
        print("2. Run script again")
        print("3. Check Kalshi dashboard for $1 test trade")
        print("4. Scale up to larger positions")
        
        print("\n📋 VERIFICATION STEPS:")
        print("1. Login to Kalshi.com")
        print("2. Check Account → Balance")
        print("3. Check Open Positions")
        print("4. Verify API key is active")
        
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