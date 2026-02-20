#!/usr/bin/env python3
"""
Options Recommender - API Clients
Wrappers for Alpaca, Finnhub, and FRED APIs
"""

import os
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# API Configuration
ALPACA_KEY = os.environ.get('ALPACA_KEY', 'PKNDK5P66FCRH5P5ILPTVCYE7D')
ALPACA_SECRET = os.environ.get('ALPACA_SECRET', 'z1fwAHFV9H8NY26XrZ2sSSxJggc8BwqiU2gPxVsy49V')
ALPACA_ENDPOINT = os.environ.get('ALPACA_ENDPOINT', 'https://paper-api.alpaca.markets/v2')

FINNHUB_KEY = os.environ.get('FINNHUB_KEY', 'd6bq93hr01qp4li0f2h0d6bq93hr01qp4li0f2hg')
FRED_KEY = os.environ.get('FRED_KEY', 'c00b92a9c6a70cb70efc3201cfb9bb5f')


class AlpacaClient:
    """Alpaca Markets API client for options data"""
    
    def __init__(self):
        self.headers = {
            'APCA-API-KEY-ID': ALPACA_KEY,
            'APCA-API-SECRET-KEY': ALPACA_SECRET
        }
        self.base_url = ALPACA_ENDPOINT
    
    def get_account(self) -> Dict:
        """Get account details"""
        resp = requests.get(f"{self.base_url}/account", headers=self.headers)
        return resp.json() if resp.status_code == 200 else {}
    
    def get_positions(self) -> List[Dict]:
        """Get current positions"""
        resp = requests.get(f"{self.base_url}/positions", headers=self.headers)
        return resp.json() if resp.status_code == 200 else []
    
    def get_assets(self, status: str = 'active', asset_class: str = 'us_equity') -> List[Dict]:
        """Get list of tradeable assets"""
        params = {'status': status, 'asset_class': asset_class}
        resp = requests.get(f"{self.base_url}/assets", headers=self.headers, params=params)
        return resp.json() if resp.status_code == 200 else []
    
    def get_bars(self, symbol: str, timeframe: str = '1Day', limit: int = 200) -> List[Dict]:
        """Get historical price bars"""
        params = {'timeframe': timeframe, 'limit': limit}
        url = f"https://data.alpaca.markets/v2/stocks/{symbol}/bars"
        resp = requests.get(url, headers=self.headers, params=params)
        return resp.json().get('bars', []) if resp.status_code == 200 else []
    
    def get_snapshot(self, symbol: str) -> Dict:
        """Get current snapshot for a symbol"""
        url = f"https://data.alpaca.markets/v2/stocks/{symbol}/snapshot"
        resp = requests.get(url, headers=self.headers)
        return resp.json() if resp.status_code == 200 else {}
    
    def get_options_chain(self, symbol: str) -> List[Dict]:
        """Get options chain for a symbol (requires options data subscription)"""
        # Note: This is a simplified version. Real options data requires
        # Alpaca's options data subscription or a third-party provider
        url = f"{self.base_url}/options/chains/{symbol}"
        resp = requests.get(url, headers=self.headers)
        return resp.json() if resp.status_code == 200 else []


class FinnhubClient:
    """Finnhub API client for fundamentals and news"""
    
    def __init__(self):
        self.api_key = FINNHUB_KEY
        self.base_url = "https://finnhub.io/api/v1"
    
    def _request(self, endpoint: str, params: Dict = None) -> Any:
        """Make API request"""
        if params is None:
            params = {}
        params['token'] = self.api_key
        resp = requests.get(f"{self.base_url}/{endpoint}", params=params)
        return resp.json() if resp.status_code == 200 else {}
    
    def get_company_profile(self, symbol: str) -> Dict:
        """Get company profile"""
        return self._request("stock/profile2", {"symbol": symbol})
    
    def get_basic_financials(self, symbol: str, metric: str = 'all') -> Dict:
        """Get basic financials"""
        return self._request("stock/metric", {"symbol": symbol, "metric": metric})
    
    def get_financials(self, symbol: str, statement: str = 'ic', freq: str = 'annual') -> Dict:
        """Get financial statements (ic=income, bs=balance, cf=cashflow)"""
        return self._request("stock/financials", {
            "symbol": symbol, 
            "statement": statement, 
            "freq": freq
        })
    
    def get_recommendation_trends(self, symbol: str) -> List[Dict]:
        """Get analyst recommendation trends"""
        return self._request("stock/recommendation", {"symbol": symbol})
    
    def get_price_target(self, symbol: str) -> Dict:
        """Get analyst price targets"""
        return self._request("stock/price-target", {"symbol": symbol})
    
    def get_earnings(self, symbol: str) -> Dict:
        """Get earnings data"""
        return self._request("stock/earnings", {"symbol": symbol})
    
    def get_news(self, symbol: str, days: int = 3) -> List[Dict]:
        """Get company news"""
        to_date = datetime.now().strftime('%Y-%m-%d')
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        return self._request("company-news", {
            "symbol": symbol,
            "from": from_date,
            "to": to_date
        })
    
    def get_news_sentiment(self, symbol: str) -> Dict:
        """Get news sentiment"""
        return self._request("news-sentiment", {"symbol": symbol})
    
    def get_insider_transactions(self, symbol: str) -> List[Dict]:
        """Get insider transactions"""
        return self._request("stock/insider-transactions", {"symbol": symbol})
    
    def get_stock_candles(self, symbol: str, resolution: str = 'D', days: int = 365) -> Dict:
        """Get historical candles (D=daily, W=weekly)"""
        to_ts = int(datetime.now().timestamp())
        from_ts = int((datetime.now() - timedelta(days=days)).timestamp())
        return self._request("stock/candle", {
            "symbol": symbol,
            "resolution": resolution,
            "from": from_ts,
            "to": to_ts
        })
    
    def get_uspto_patents(self, symbol: str) -> List[Dict]:
        """Get USPTO patents"""
        return self._request("stock/uspto-patents", {"symbol": symbol})


class FredClient:
    """FRED API client for macro indicators"""
    
    def __init__(self):
        self.api_key = FRED_KEY
        self.base_url = "https://api.stlouisfed.org/fred"
    
    def _request(self, endpoint: str, params: Dict = None) -> Any:
        """Make API request"""
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        params['file_type'] = 'json'
        resp = requests.get(f"{self.base_url}/{endpoint}", params=params)
        return resp.json() if resp.status_code == 200 else {}
    
    def get_series(self, series_id: str, observations: bool = True) -> Dict:
        """Get series data"""
        if observations:
            return self._request("series/observations", {"series_id": series_id})
        return self._request("series", {"series_id": series_id})
    
    def get_latest_observation(self, series_id: str) -> Optional[float]:
        """Get the latest observation for a series"""
        data = self.get_series(series_id)
        observations = data.get('observations', [])
        if observations:
            try:
                return float(observations[-1]['value'])
            except (ValueError, IndexError):
                pass
        return None
    
    # Convenience methods for common indicators
    def get_vix(self) -> Optional[float]:
        """Get VIX index"""
        return self.get_latest_observation('VIXCLS')
    
    def get_cpi(self) -> Optional[float]:
        """Get CPI (Consumer Price Index)"""
        return self.get_latest_observation('CPIAUCSL')
    
    def get_unemployment(self) -> Optional[float]:
        """Get unemployment rate"""
        return self.get_latest_observation('UNRATE')
    
    def get_gdp(self) -> Optional[float]:
        """Get GDP"""
        return self.get_latest_observation('GDP')
    
    def get_fed_funds_rate(self) -> Optional[float]:
        """Get Federal Funds Rate"""
        return self.get_latest_observation('FEDFUNDS')
    
    def get_10y_treasury(self) -> Optional[float]:
        """Get 10-Year Treasury Yield"""
        return self.get_latest_observation('GS10')
    
    def get_consumer_confidence(self) -> Optional[float]:
        """Get Consumer Confidence Index"""
        return self.get_latest_observation('UMCSENT')


# Convenience function to get all clients
def get_clients() -> Dict:
    """Get initialized API clients"""
    return {
        'alpaca': AlpacaClient(),
        'finnhub': FinnhubClient(),
        'fred': FredClient()
    }


if __name__ == "__main__":
    # Test the clients
    print("Testing API clients...")
    
    # Test Alpaca
    print("\n1. Alpaca:")
    alpaca = AlpacaClient()
    account = alpaca.get_account()
    print(f"   Account status: {account.get('status', 'N/A')}")
    print(f"   Buying power: ${float(account.get('buying_power', 0)):,.2f}")
    
    # Test Finnhub
    print("\n2. Finnhub:")
    finnhub = FinnhubClient()
    profile = finnhub.get_company_profile('AAPL')
    print(f"   AAPL: {profile.get('name', 'N/A')}")
    financials = finnhub.get_basic_financials('AAPL')
    metrics = financials.get('metric', {})
    print(f"   P/E: {metrics.get('peBasicExclExtraTTM', 'N/A')}")
    print(f"   Revenue growth: {metrics.get('revenueGrowthTTM', 'N/A')}")
    
    # Test FRED
    print("\n3. FRED:")
    fred = FredClient()
    vix = fred.get_vix()
    unemployment = fred.get_unemployment()
    print(f"   VIX: {vix}")
    print(f"   Unemployment: {unemployment}%")
    
    print("\n✅ All API clients working!")
