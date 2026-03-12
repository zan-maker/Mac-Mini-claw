#!/usr/bin/env python3
"""
Quick test of new Kalshi API key
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

def test_new_api_key():
    """Test the newly regenerated API key"""
    print("🔑 TESTING NEW KALSHI API KEY")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Load new credentials
    config_file = "/Users/cubiczan/.openclaw/workspace/secrets/kalshi_config.json"
    if not os.path.exists(config_file):
        print("❌ Config file not found")
        return False
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    key_id = config.get("key_id", "")
    private_key_pem = config.get("private_key", "")
    
    print(f"✅ New credentials loaded")
    print(f"📋 Key ID: {key_id}")
    print(f"🔑 Private Key: {len(private_key_pem)} chars")
    
    # Generate signature
    print("\n🔐 GENERATING SIGNATURE...")
    base_url = "https://api.elections.kalshi.com/trade-api/v2"
    path = "/portfolio/balance"
    method = "GET"
    timestamp = str(int(time.time()))
    message = f"{method}{path}{timestamp}"
    
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
        
        print(f"   ✅ Signature generated successfully")
        print(f"   📅 Timestamp: {timestamp}")
        print(f"   🔑 Signature (first 50 chars): {signature_b64[:50]}...")
        
        headers = {
            "KALSHI-ACCESS-KEY": key_id,
            "KALSHI-ACCESS-SIGNATURE": signature_b64,
            "KALSHI-ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }
        
        # Test the request
        print(f"\n🌐 TESTING API REQUEST...")
        print(f"   URL: {base_url}{path}")
        
        response = requests.get(
            f"{base_url}{path}",
            headers=headers,
            timeout=10
        )
        
        print(f"   📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            account_data = response.json()
            print(f"\n🎉 SUCCESS! API KEY WORKS!")
            print(f"   💰 Balance: ${account_data.get('balance', 0)/100:.2f}")
            print(f"   📈 Portfolio Value: ${account_data.get('portfolio_value', 0)/100:.2f}")
            print(f"   💳 Buying Power: ${account_data.get('buying_power', 0)/100:.2f}")
            print(f"   📊 Updated: {account_data.get('updated_ts', 'unknown')}")
            
            # Ready for trading
            print(f"\n🚀 READY FOR TRADING!")
            print(f"   Available capital: ${account_data.get('buying_power', 0)/100:.2f}")
            print(f"   Next: Execute $1 test trade")
            
            return account_data
            
        else:
            print(f"   ❌ Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def execute_immediate_test_trade():
    """Execute immediate $1 test trade if API works"""
    print("\n" + "=" * 60)
    print("💰 EXECUTE IMMEDIATE $1 TEST TRADE?")
    print("=" * 60)
    
    # Ask for confirmation (simulated for now)
    print("   ⚠️  Would execute $1 test trade now")
    print("   🔒 Currently in SAFE MODE")
    print("   Change to execute_real_trade=True for real trade")
    
    return {"simulated": True, "note": "Ready for real trading"}

def main():
    """Main function"""
    # Test the new API key
    account = test_new_api_key()
    
    if account:
        # Ready to execute test trade
        trade_result = execute_immediate_test_trade()
        
        print("\n" + "=" * 60)
        print("🎯 NEXT STEPS:")
        print("1. Change execute_real_trade=True in script")
        print("2. Run trading system")
        print("3. Check Kalshi dashboard for $1 test trade")
        print("4. Scale up to larger positions")
        print("=" * 60)
        
        print(f"\n📊 YOUR ACCOUNT STATUS:")
        print(f"   Balance: ${account.get('balance', 0)/100:.2f}")
        print(f"   Buying Power: ${account.get('buying_power', 0)/100:.2f}")
        print(f"   Ready for trading: ✅")
        
    else:
        print("\n❌ API KEY TEST FAILED")
        print("Check:")
        print("1. API key activated in Kalshi account")
        print("2. Key has trading permissions")
        print("3. Internet connectivity")
        print("4. Signature generation")

if __name__ == "__main__":
    main()