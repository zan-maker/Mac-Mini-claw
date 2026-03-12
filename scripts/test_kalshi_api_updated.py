#!/usr/bin/env python3
"""
Test actual Kalshi API connectivity with real $1 trade
UPDATED: Correct API endpoint
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
        self.base_url = "https://api.elections.kalshi.com/v1"  # UPDATED ENDPOINT
        
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
        """Test basic connectivity to new endpoint"""
        print("\n🌐 TESTING CONNECTIVITY TO NEW ENDPOINT...")
        
        try:
            response = requests.get(self.base_url, timeout=10)
            print(f"   📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Connected to new API endpoint")
                return True
            else:
                print(f"   ❌ Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"   ❌ Connection failed: {e}")
            return False
    
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
                print(f"   📊 Open Positions: {account_data.get('open_positions_count', 0)}")
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
        
        # Try different market endpoints
        endpoints = [
            "/markets",
            "/events"  # Some APIs use events instead of markets
        ]
        
        for path in endpoints:
            print(f"   Trying: {path}")
            headers = self.generate_signature("GET", path)
            
            if not headers:
                print("   ❌ Failed to generate signature")
                continue
            
            try:
                response = requests.get(
                    f"{self.base_url}{path}",
                    headers=headers,
                    timeout=10
                )
                
                print(f"   📊 Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Data received from {path}")
                    
                    # Try to parse markets/events
                    if 'markets' in data:
                        markets = data['markets']
                        print(f"   📊 Markets found: {len(markets)}")
                        return markets
                    elif 'events' in data:
                        events = data['events']
                        print(f"   📊 Events found: {len(events)}")
                        return events
                    else:
                        print(f"   📊 Response keys: {list(data.keys())}")
                        return data
                else:
                    print(f"   ❌ Error: {response.text}")
                    
            except Exception as e:
                print(f"   ❌ Request failed: {e}")
        
        return None
    
    def execute_test_trade(self, market_data):
        """Execute $1 test trade"""
        print(f"\n3. 💰 PREPARING $1 TEST TRADE...")
        
        # Extract ticker from market data
        if isinstance(market_data, dict) and 'ticker' in market_data:
            ticker = market_data['ticker']
        elif isinstance(market_data, list) and len(market_data) > 0:
            # Use first market
            ticker = market_data[0].get('ticker', 'TEST-1.00')
        else:
            ticker = "TEST-1.00"  # Fallback
        
        print(f"   Ticker: {ticker}")
        
        # Trade parameters for $1 test (2 shares at ~$0.50 each)
        trade_data = {
            "ticker": ticker,
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
        
        # SAFETY FIRST - Simulated mode
        print(f"\n   🔒 SAFETY MODE: Trade will be SIMULATED")
        print(f"   To execute real trade, change simulated=False")
        
        simulated = True  # SAFETY FIRST
        
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
            print(f"   🔒 SIMULATED: Trade NOT executed")
            print(f"   Check Kalshi dashboard for actual trading")
            return {"simulated": True, "trade_data": trade_data}
    
    def run_tests(self):
        """Run all tests"""
        print("🔗 TESTING KALSHI API CONNECTIVITY")
        print("=" * 60)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 API Endpoint: {self.base_url}")
        print("=" * 60)
        
        # Test connectivity
        if not self.test_connectivity():
            print("   ❌ Connectivity test failed")
            return False
        
        # Test 1: Account endpoint
        account = self.test_account_endpoint()
        if not account:
            print("   ⚠️  Account test issues - check API key permissions")
            # Continue anyway for testing
        
        # Test 2: Markets endpoint
        markets = self.test_markets_endpoint()
        
        # Test 3: Execute trade (simulated)
        if markets:
            trade_result = self.execute_test_trade(markets)
        else:
            trade_result = self.execute_test_trade({"ticker": "TEST-1.00"})
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY:")
        print(f"   API Endpoint: {self.base_url}")
        print(f"   Connectivity: ✅")
        print(f"   Account test: {'✅' if account else '⚠️'}")
        print(f"   Markets test: {'✅' if markets else '⚠️'}")
        print(f"   Trade test: 🔒 SIMULATED")
        
        print("\n🎯 NEXT STEPS FOR REAL TRADING:")
        print("1. Check Kalshi dashboard → API Settings")
        print("2. Verify API key has trading permissions")
        print("3. Test with curl command:")
        print(f"   curl -X GET {self.base_url}/account \\")
        print(f"     -H 'KALSHI-ACCESS-KEY: YOUR_KEY' \\")
        print(f"     -H 'KALSHI-ACCESS-SIGNATURE: ...' \\")
        print(f"     -H 'KALSHI-ACCESS-TIMESTAMP: $(date +%s)'")
        print("4. Once working, change simulated=False in script")
        print("5. Start with $1 test trades")
        
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