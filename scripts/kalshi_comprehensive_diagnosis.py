#!/usr/bin/env python3
"""
Comprehensive Kalshi API test
Check public endpoints and diagnose authentication issues
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

def test_public_endpoints():
    """Test endpoints that don't require authentication"""
    print("🌐 TESTING PUBLIC ENDPOINTS")
    print("=" * 60)
    
    base_url = "https://api.elections.kalshi.com/trade-api/v2"
    
    endpoints = [
        ("/historical/cutoff", "Historical cutoff"),
        ("/exchange/status", "Exchange status"),
        ("/exchange/schedule", "Exchange schedule"),
    ]
    
    for path, description in endpoints:
        try:
            response = requests.get(f"{base_url}{path}", timeout=10)
            print(f"📊 {description}: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Public endpoint accessible")
            else:
                print(f"   ❌ Error: {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    return True

def diagnose_authentication():
    """Diagnose authentication issues"""
    print("\n🔐 DIAGNOSING AUTHENTICATION ISSUES")
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
    print(f"🔑 Private Key length: {len(private_key_pem)} chars")
    
    # Check private key format
    print(f"\n🔑 CHECKING PRIVATE KEY FORMAT...")
    try:
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode(),
            password=None
        )
        print(f"   ✅ Private key is valid PEM format")
        
        # Check key size
        key_size = private_key.key_size
        print(f"   📏 Key size: {key_size} bits")
        
        # Test signing a simple message
        test_message = b"test"
        signature = private_key.sign(
            test_message,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        print(f"   ✅ Can sign messages ({len(signature)} bytes)")
        
    except Exception as e:
        print(f"   ❌ Private key error: {e}")
        return False
    
    # Try to get balance with detailed error
    print(f"\n🌐 TESTING AUTHENTICATED ENDPOINT...")
    base_url = "https://api.elections.kalshi.com/trade-api/v2"
    path = "/portfolio/balance"
    method = "GET"
    timestamp = str(int(time.time()))
    message = f"{method}{path}{timestamp}"
    
    try:
        # Generate signature
        signature = private_key.sign(
            message.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        
        signature_b64 = base64.b64encode(signature).decode()
        
        headers = {
            "KALSHI-ACCESS-KEY": key_id,
            "KALSHI-ACCESS-SIGNATURE": signature_b64,
            "KALSHI-ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }
        
        print(f"   📅 Timestamp: {timestamp}")
        print(f"   🔑 Signature generated: {len(signature_b64)} chars")
        
        # Make request
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
            return account_data
        else:
            error_data = response.json()
            error_details = error_data.get('error', {})
            print(f"\n❌ AUTHENTICATION FAILED")
            print(f"   Code: {error_details.get('code')}")
            print(f"   Message: {error_details.get('message')}")
            print(f"   Details: {error_details.get('details')}")
            
            # Specific diagnosis
            if error_details.get('details') == "INCORRECT_API_KEY_SIGNATURE":
                print(f"\n🔍 DIAGNOSIS: API KEY NOT ACTIVATED")
                print(f"   The key exists but is not active in your Kalshi account")
                print(f"   Please login to Kalshi.com → Account → API Settings")
                print(f"   Find key: {key_id}")
                print(f"   Click 'Activate' or 'Enable'")
                
            return None
            
    except Exception as e:
        print(f"   ❌ Request failed: {e}")
        return None

def main():
    """Main function"""
    print("🔗 COMPREHENSIVE KALSHI API DIAGNOSIS")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Test public endpoints
    test_public_endpoints()
    
    # Diagnose authentication
    account = diagnose_authentication()
    
    if account:
        print("\n" + "=" * 60)
        print("🚀 READY FOR TRADING!")
        print("=" * 60)
        print(f"💰 Balance: ${account.get('balance', 0)/100:.2f}")
        print(f"💳 Buying Power: ${account.get('buying_power', 0)/100:.2f}")
        
        print("\n🎯 IMMEDIATE ACTIONS:")
        print("1. Execute $1 test trade")
        print("2. Deploy remaining capital")
        print("3. Start 24/7 automated trading")
        
    else:
        print("\n" + "=" * 60)
        print("🔧 ACTION REQUIRED")
        print("=" * 60)
        print("Your API key needs activation in Kalshi account")
        print("\n📋 STEPS TO FIX:")
        print("1. Login to Kalshi.com")
        print("2. Go to Account → API Settings")
        print("3. Find key: 27df1d5a-8903-495c-b694-870b0c9fe468")
        print("4. Click 'Activate' or 'Enable'")
        print("5. Enable trading permissions")
        print("6. Wait 1-2 minutes")
        print("\n⏰ Then run this test again")

if __name__ == "__main__":
    main()