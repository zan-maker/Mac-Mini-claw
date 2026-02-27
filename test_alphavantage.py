#!/usr/bin/env python3
"""Test Alpha Vantage integration with rate limiting"""

from alphavantage_integration import AlphaVantageIntegration

def main():
    print("🧪 Testing Alpha Vantage Integration with Rate Limiting...")
    
    # Initialize with API key
    integration = AlphaVantageIntegration(api_key="T0Z2YW467F7PNA9Z")
    
    print(f"📊 Starting API calls: {integration.daily_call_count}/{integration.max_daily_calls}")
    
    # Test with a penny stock
    print("\n📈 Testing AMC (penny stock):")
    data = integration.get_ticker_data("AMC")
    
    print(f"  Price: ${data.get('current_price', 0):.2f}")
    print(f"  Penny stock: {data.get('is_penny_stock', False)}")
    print(f"  RSI: {data.get('rsi', 0):.1f}")
    print(f"  Source: {data.get('source', 'unknown')}")
    print(f"  Success: {data.get('success', False)}")
    
    # Test with a large cap (should be filtered)
    print("\n📈 Testing AAPL (large cap):")
    data = integration.get_ticker_data("AAPL")
    
    print(f"  Price: ${data.get('current_price', 0):.2f}")
    print(f"  Penny stock: {data.get('is_penny_stock', False)}")
    print(f"  Source: {data.get('source', 'unknown')}")
    
    print(f"\n📊 Final API calls: {integration.daily_call_count}/{integration.max_daily_calls}")
    
    # Test mock data fallback
    print("\n🧪 Testing mock data fallback:")
    data = integration._get_mock_data("TEST")
    print(f"  Mock price: ${data.get('current_price', 0):.2f}")
    print(f"  Mock RSI: {data.get('rsi', 0):.1f}")
    
    print("\n✅ Alpha Vantage Integration Test Complete!")

if __name__ == "__main__":
    main()