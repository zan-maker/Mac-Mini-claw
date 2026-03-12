#!/usr/bin/env python3
"""
Kalshi API Test - Real connectivity check
"""

import os
import sys
import json
import time
import requests
from datetime import datetime

def check_kalshi_connectivity():
    """Check if we can connect to Kalshi API"""
    print("🔗 CHECKING KALSHI API CONNECTIVITY")
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
    
    print(f"✅ Credentials loaded")
    print(f"📋 Key ID: {key_id}")
    print(f"🔑 Private Key: {len(private_key)} chars")
    
    # Test basic connectivity
    print("\n🌐 TESTING BASIC CONNECTIVITY...")
    try:
        # Test if we can reach Kalshi
        response = requests.get("https://trading-api.kalshi.com/v1", timeout=10)
        print(f"   ✅ Can reach Kalshi API")
        print(f"   📊 Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Cannot reach Kalshi API: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🎯 KALSHI API CONNECTIVITY CHECK")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check connectivity
    connected = check_kalshi_connectivity()
    
    if connected:
        print("\n✅ BASIC CONNECTIVITY: OK")
        print("\n🔧 WHAT'S NEEDED FOR REAL TRADES:")
        print("1. Proper RSA signing implementation")
        print("2. Test account balance endpoint")
        print("3. Test markets endpoint")
        print("4. Execute $1 test trade")
        
        print("\n📋 IMMEDIATE ACTION PLAN:")
        print("1. Check Kalshi dashboard for API key status")
        print("2. Verify key has trading permissions")
        print("3. Test with curl command first:")
        print("   curl -X GET https://trading-api.kalshi.com/v1/account \\")
        print("     -H 'KALSHI-ACCESS-KEY: YOUR_KEY_ID' \\")
        print("     -H 'KALSHI-ACCESS-SIGNATURE: GENERATED_SIGNATURE' \\")
        print("     -H 'KALSHI-ACCESS-TIMESTAMP: $(date +%s)'")
        
    else:
        print("\n❌ CONNECTIVITY ISSUES")
    
    print("\n" + "=" * 60)
    print("💡 WHY NO ORDERS ON KALSHI:")
    print("1. My previous trades were SIMULATED only")
    print("2. Need proper RSA signing for API authentication")
    print("3. Need to test with real API calls")
    print("4. Start with $1 test trades")
    print("=" * 60)
    
    print("\n🚀 ACTION 1 COMPLETE: Kalshi API connectivity checked")
    print("   Next: Action 2 - Create Pinchtab LinkedIn profiles")

if __name__ == "__main__":
    main()