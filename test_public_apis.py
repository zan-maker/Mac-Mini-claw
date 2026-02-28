#!/usr/bin/env python3
"""Test Public APIs integration"""

from public_apis_integration import PublicAPIsIntegration

def main():
    print("🧪 Testing Public APIs Integration...")
    
    apis = PublicAPIsIntegration()
    
    print("\n📊 Testing available APIs...")
    
    # Test Alpha Vantage (already configured)
    print("\n💰 Testing Alpha Vantage...")
    stock_data = apis.get_stock_price("AAPL", api="alphavantage")
    print(f"  Success: {stock_data.get('success', False)}")
    print(f"  Source: {stock_data.get('source', 'unknown')}")
    if stock_data.get("success"):
        print(f"  Price: ${stock_data.get('price', 0):.2f}")
    
    # Test CoinGecko (no API key needed)
    print("\n🪙 Testing CoinGecko...")
    crypto_data = apis.get_crypto_price("bitcoin", "usd")
    print(f"  Success: {crypto_data.get('success', False)}")
    print(f"  Source: {crypto_data.get('source', 'unknown')}")
    if crypto_data.get("success"):
        print(f"  Bitcoin price: ${crypto_data.get('price', 0):,.2f}")
    
    # Test validation (mock since no API keys)
    print("\n✅ Testing validation (mock - needs API keys)...")
    print("  To enable:")
    print("  - Sign up for Numverify (phone validation)")
    print("  - Sign up for Mailboxlayer (email validation)")
    print("  - Sign up for Tomba (email finding)")
    print("  - Sign up for NewsAPI (news)")
    print("  - Get Marketstack key from APILayer")
    
    # Show call statistics
    print("\n📈 Call statistics:")
    stats = apis.get_call_stats()
    for api, calls in stats.items():
        if api != "date":
            print(f"  {api}: {calls} calls")
    
    print("\n✅ Public APIs Integration Ready!")
    print("\n🔑 Next: Sign up for free API keys to unlock full functionality!")

if __name__ == "__main__":
    main()