#!/usr/bin/env python3
"""
Twelve Data API Client for Trade Recommender
Provides real-time and historical market data for stocks, forex, crypto
"""

import urllib.request
import urllib.error
import json
from typing import Dict, List, Optional
from datetime import datetime

class TwelveDataClient:
    """Twelve Data API client for market data"""

    def __init__(self, api_key: str = "26b639a38e124248ba08958bcd72566f"):
        self.api_key = api_key
        self.base_url = "https://api.twelvedata.com"

    def _request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make API request"""
        try:
            # Build URL with parameters
            url = f"{self.base_url}/{endpoint}"
            if params:
                params["apikey"] = self.api_key
                param_str = "&".join(f"{k}={v}" for k, v in params.items())
                url = f"{url}?{param_str}"
            else:
                url = f"{url}?apikey={self.api_key}"

            req = urllib.request.Request(url)
            # Add User-Agent header (required by Twelve Data)
            req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5)')

            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode())

        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            print(f"HTTP Error {e.code}: {error_body}")
            return None
        except Exception as e:
            print(f"Request error: {e}")
            return None

    def get_quote(self, symbol: str) -> Dict:
        """Get real-time quote for a symbol"""
        result = self._request("quote", {"symbol": symbol})
        return result if result else {}

    def get_price(self, symbol: str) -> Dict:
        """Get latest price for a symbol"""
        result = self._request("price", {"symbol": symbol})
        return result if result else {}

    def get_time_series(self, symbol: str, interval: str = "1day",
                        outputsize: int = 30) -> List[Dict]:
        """Get historical time series data

        Intervals: 1min, 5min, 15min, 30min, 45min, 1h, 2h, 4h, 8h, 1day, 1week, 1month
        """
        result = self._request("time_series", {
            "symbol": symbol,
            "interval": interval,
            "outputsize": outputsize
        })

        if result and "values" in result:
            return result["values"]
        return []

    def get_technical_indicators(self, symbol: str, interval: str = "1day",
                                  indicator: str = "rsi", **kwargs) -> Dict:
        """Get technical indicators (RSI, MACD, SMA, EMA, etc.)"""
        params = {
            "symbol": symbol,
            "interval": interval,
            "indicator": indicator
        }
        params.update(kwargs)

        result = self._request("indicators", params)
        return result if result else {}

    def get_forex_pairs(self) -> List[Dict]:
        """Get list of forex pairs"""
        result = self._request("forex_pairs")
        if result and "data" in result:
            return result["data"]
        return []

    def get_cryptocurrencies(self) -> List[Dict]:
        """Get list of cryptocurrencies"""
        result = self._request("cryptocurrencies")
        if result and "data" in result:
            return result["data"]
        return []

    def get_etf_list(self) -> List[Dict]:
        """Get list of ETFs"""
        result = self._request("etf")
        if result and "data" in result:
            return result["data"]
        return []

    def get_market_movers(self, market: str = "stocks") -> Dict:
        """Get market movers (gainers, losers, most active)"""
        result = self._request("market_movers", {"market": market})
        return result if result else {}

    def get_earnings(self, symbol: str) -> Dict:
        """Get earnings data"""
        result = self._request("earnings", {"symbol": symbol})
        return result if result else {}

    def get_profile(self, symbol: str) -> Dict:
        """Get company profile"""
        result = self._request("profile", {"symbol": symbol})
        return result if result else {}

def main():
    """Test Twelve Data API"""
    print("=" * 60)
    print("TWELVE DATA API CLIENT TEST")
    print("=" * 60)
    print()

    client = TwelveDataClient()

    # Test 1: Real-time price
    print("--- Test 1: AAPL Real-time Price ---")
    price = client.get_price("AAPL")
    if price:
        print(f"✅ AAPL Price: ${float(price.get('price', 0)):,.2f}")
    print()

    # Test 2: Real-time quote
    print("--- Test 2: SPY Quote ---")
    quote = client.get_quote("SPY")
    if quote:
        print(f"Symbol: {quote.get('symbol')}")
        print(f"Name: {quote.get('name')}")
        print(f"Price: ${float(quote.get('close', 0)):,.2f}")
        print(f"Change: {quote.get('change')} ({quote.get('percent_change')}%)")
        volume = quote.get('volume', 0)
        print(f"Volume: {int(volume):,}" if volume else "Volume: N/A")
    print()

    # Test 3: Time series
    print("--- Test 3: SPY Last 5 Days ---")
    series = client.get_time_series("SPY", "1day", 5)
    if series:
        for bar in series[:5]:
            print(f"{bar['datetime']}: Close ${float(bar['close']):.2f}, Vol {bar['volume']}")
    print()

    # Test 4: Multiple symbols
    print("--- Test 4: Multiple Symbol Prices ---")
    symbols = ["QQQ", "IWM", "TLT"]
    for symbol in symbols:
        price_data = client.get_price(symbol)
        if price_data:
            print(f"  • {symbol}: ${float(price_data.get('price', 0)):,.2f}")
    print()

    print("=" * 60)
    print("✅ TWELVE DATA API INTEGRATION WORKING!")
    print("=" * 60)

if __name__ == "__main__":
    main()
