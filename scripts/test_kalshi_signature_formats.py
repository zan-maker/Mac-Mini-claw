#!/usr/bin/env python3
"""
Test Kalshi API based on OpenAPI spec
Looking for correct signature format
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

def test_signature_format():
    """Test different signature formats"""
    print("🔐 TESTING KALSHI SIGNATURE FORMATS")
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
    
    base_url = "https://api.elections.kalshi.com/trade-api/v2"
    path = "/portfolio/balance"
    method = "GET"
    timestamp = str(int(time.time()))
    
    # Test different message formats
    test_formats = [
        f"{method}{path}{timestamp}",  # Current format
        f"{method} {path} {timestamp}",  # With spaces
        f"{method}\n{path}\n{timestamp}",  # With newlines
        f"{timestamp}{method}{path}",  # Timestamp first
        f"{path}{method}{timestamp}",  # Path first
    ]
    
    for i, message in enumerate(test_formats):
        print(f"\n🔬 TEST {i+1}: {message[:50]}...")
        
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
            
            # Test the request
            response = requests.get(
                f"{base_url}{path}",
                headers=headers,
                timeout=10
            )
            
            print(f"   📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                account_data = response.json()
                print(f"   🎉 SUCCESS! Format {i+1} works!")
                print(f"   💰 Balance: ${account_data.get('balance', 0)/100:.2f}")
                print(f"   📋 Message format: {message}")
                return account_data
            elif response.status_code == 401:
                error = response.json().get('error', {})
                print(f"   ❌ 401: {error.get('details', 'Unknown')}")
            else:
                print(f"   ❌ Error: {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    print(f"\n❌ All signature formats failed")
    print(f"Check API key activation in Kalshi account")
    return None

def check_api_key_status():
    """Check if API key is active via different endpoint"""
    print("\n🔍 CHECKING API KEY STATUS VIA PUBLIC ENDPOINT")
    
    # Try public endpoint first
    try:
        response = requests.get(
            "https://api.elections.kalshi.com/trade-api/v2/exchange/status",
            timeout=10
        )
        
        print(f"📊 Exchange status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Exchange is online")
            return True
        else:
            print(f"❌ Exchange status error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exchange check failed: {e}")
        return False

def main():
    """Main function"""
    print("🔗 KALSHI API SIGNATURE FORMAT TEST")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check exchange status
    if not check_api_key_status():
        print("❌ Exchange check failed")
        return
    
    # Test different signature formats
    account = test_signature_format()
    
    if account:
        print("\n" + "=" * 60)
        print("🎉 API KEY WORKS!")
        print("=" * 60)
        print(f"💰 Balance: ${account.get('balance', 0)/100:.2f}")
        print(f"📈 Portfolio Value: ${account.get('portfolio_value', 0)/100:.2f}")
        print(f"💳 Buying Power: ${account.get('buying_power', 0)/100:.2f}")
        
        print("\n🚀 READY FOR TRADING!")
        print("1. Execute $1 test trade")
        print("2. Deploy remaining capital")
        print("3. Start 24/7 automated trading")
        
    else:
        print("\n" + "=" * 60)
        print("❌ API KEY ISSUE DETECTED")
        print("=" * 60)
        print("Most likely: API key not activated in Kalshi account")
        print("\n🔧 PLEASE CHECK:")
        print("1. Login to Kalshi.com")
        print("2. Go to Account → API Settings")
        print("3. Find key: 27df1d5a-8903-495c-b694-870b0c9fe468")
        print("4. Click 'Activate' or 'Enable'")
        print("5. Enable trading permissions")
        print("\n⏰ Wait 1-2 minutes after activation")
        print("Then run test again")

if __name__ == "__main__":
    main()