#!/usr/bin/env python3
"""Simple Alpha Vantage test"""

import time
from alphavantage_integration import AlphaVantageIntegration

print("🧪 Fresh Alpha Vantage test...")
integration = AlphaVantageIntegration(api_key="T0Z2YW467F7PNA9Z")

print("Testing AMC...")
data1 = integration.get_ticker_data("AMC")
print(f"AMC: Price ${data1.get('current_price', 0):.2f}, Source: {data1.get('source')}")

time.sleep(2)  # Wait for rate limit

print("Testing AAPL...")
data2 = integration.get_ticker_data("AAPL")
print(f"AAPL: Price ${data2.get('current_price', 0):.2f}, Source: {data2.get('source')}")

print(f"Total calls: {integration.daily_call_count}")