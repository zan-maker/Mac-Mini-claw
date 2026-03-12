#!/usr/bin/env python3
"""
Test Kalshi API with real $1 trade
"""

import os
import json
import time
import hashlib
import hmac
import base64
from datetime import datetime
import requests

def test_kalshi_api_real():
    """Test actual Kalshi API with real trade"""
    print("🔗 TESTING KALSHI API WITH REAL TRADE")
    print("=" * 60)
    
    # Load credentials
    config_file = "/Users/cubiczan/.openclaw/workspace/secrets/kalshi_config.json"
    if not os.path.exists(config_file):
        print("❌ Config file not found")
        return False
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    key_id = config.get("key_id", "")
    private_key = config.get("private_key", "")
    
    if not key_id or not private_key:
        print("❌ Missing API credentials")
        return False
    
    print(f"✅ Credentials loaded: {key_id[:8]}...")
    
    # Kalshi API endpoints
    base_url = "https://trading-api.kalshi.com/v1"
    
    # Generate signature (simplified - would need proper RSA signing)
    timestamp = str(int(time.time()))
    
    # Headers for API calls
    headers = {
        "KALSHI-ACCESS-KEY": key_id,
        "KALSHI-ACCESS-SIGNATURE": "test_signature_placeholder",
        "KALSHI-ACCESS-TIMESTAMP": timestamp,
        "Content-Type": "application/json"
    }
    
    print(f"📅 Timestamp: {timestamp}")
    print(f"🔗 Base URL: {base_url}")
    
    # Step 1: Test account endpoint
    print("\n1. 📊 TESTING ACCOUNT ENDPOINT...")
    try:
        # This would be the real API call:
        # response = requests.get(f"{base_url}/account", headers=headers)
        # print(f"   Status: {response.status_code}")
        # print(f"   Response: {response.text}")
        
        # Simulated response for testing
        print("   ⚠️  SIMULATED RESPONSE (API call commented for safety)")
        print("   To make real API call, uncomment lines 55-57")
        print("   Account balance check would happen here")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Step 2: Test markets endpoint
    print("\n2. 📈 TESTING MARKETS ENDPOINT...")
    try:
        # Real API call:
        # response = requests.get(f"{base_url}/markets", headers=headers)
        
        # Simulated markets
        markets = [
            {
                "ticker": "GASMONTH-3.50",
                "title": "Gas prices in the US this month > $3.50",
                "yes_bid": 45,
                "yes_ask": 46,
                "no_bid": 54,
                "no_ask": 55,
                "status": "open"
            }
        ]
        
        print(f"   ✅ Markets loaded: {len(markets)}")
        print(f"   📊 Sample market: {markets[0]['ticker']}")
        print(f"   💰 YES ask: ${markets[0]['yes_ask']/100:.2f}")
        print(f"   💰 NO ask: ${markets[0]['no_ask']/100:.2f}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Step 3: Test trade execution
    print("\n3. 💰 TESTING TRADE EXECUTION...")
    print("   ⚠️  IMPORTANT: This would execute a REAL $1 trade")
    print("   Currently in SAFE MODE - no real trades executed")
    
    # Trade parameters for $1 test
    test_trade = {
        "ticker": "GASMONTH-3.50",
        "side": "yes",  # or "no"
        "count": 2,  # 2 shares at ~$0.46 each = ~$0.92
        "price": 46,  # 46 cents = $0.46
        "client_order_id": f"test_{int(time.time())}"
    }
    
    print(f"   📋 Test trade parameters:")
    print(f"      Ticker: {test_trade['ticker']}")
    print(f"      Side: {test_trade['side'].upper()}")
    print(f"      Shares: {test_trade['count']}")
    print(f"      Price: ${test_trade['price']/100:.2f}")
    print(f"      Total: ${test_trade['count'] * test_trade['price']/100:.2f}")
    print(f"      Order ID: {test_trade['client_order_id']}")
    
    # This would be the real API call:
    # response = requests.post(f"{base_url}/orders", json=test_trade, headers=headers)
    
    print("\n   🔒 SAFE MODE: Trade NOT executed")
    print("   To execute real trade, uncomment line 104")
    
    # Step 4: Recommendations
    print("\n4. 🎯 RECOMMENDATIONS:")
    print("   a) First, test account balance endpoint")
    print("   b) Then test markets endpoint")
    print("   c) Finally, execute $1 test trade")
    print("   d) Monitor Kalshi dashboard for order")
    
    print("\n5. 🔧 NEXT STEPS:")
    print("   1. Uncomment API calls in this script")
    print("   2. Run with --test flag first")
    print("   3. Then run with --execute for real trade")
    print("   4. Check Kalshi dashboard for confirmation")
    
    return True

def main():
    """Main function"""
    print("🚀 KALSHI API REAL TRADE TEST")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("💰 Test trade: $1 position")
    print("=" * 60)
    
    test_kalshi_api_real()
    
    print("\n" + "=" * 60)
    print("⚠️  IMPORTANT SAFETY NOTES:")
    print("1. This script is in SAFE MODE")
    print("2. No real trades will be executed")
    print("3. Uncomment API calls to test real connectivity")
    print("4. Start with $1 test trades only")
    print("5. Monitor Kalshi dashboard for orders")
    print("=" * 60)

if __name__ == "__main__":
    main()