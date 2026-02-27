#!/usr/bin/env python3
"""
Alpha Vantage API Integration for Trade Recommender and Other Agents
Real-time market data, technical indicators, and fundamental data
"""

import os
import sys
import json
import time
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import pandas as pd

try:
    from alpha_vantage.timeseries import TimeSeries
    from alpha_vantage.techindicators import TechIndicators
    from alpha_vantage.fundamentaldata import FundamentalData
    ALPHA_VANTAGE_AVAILABLE = True
    print("✅ Alpha Vantage API available")
except ImportError as e:
    print(f"⚠️  Alpha Vantage not available: {e}")
    ALPHA_VANTAGE_AVAILABLE = False

class AlphaVantageIntegration:
    """Integration with Alpha Vantage API for market data"""
    
    def __init__(self, api_key: str = None, cache_dir: str = None):
        self.api_key = api_key or "T0Z2YW467F7PNA9Z"
        self.cache_dir = cache_dir or "/Users/cubiczan/.openclaw/workspace/cache/alphavantage"
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Rate limiting
        self.last_call_time = 0
        self.min_call_interval = 1.2  # 1.2 seconds between calls (free tier: 1 call/sec)
        self.daily_call_count = 0
        self.max_daily_calls = 25  # Free tier limit
        
        # Initialize clients if available
        if ALPHA_VANTAGE_AVAILABLE:
            self.ts = TimeSeries(key=self.api_key, output_format='pandas')
            self.ti = TechIndicators(key=self.api_key, output_format='pandas')
            self.fd = FundamentalData(key=self.api_key, output_format='pandas')
        else:
            self.ts = None
            self.ti = None
            self.fd = None
        
        # Cache for API responses
        self.cache = {}
        
        # Load daily call count
        self._load_daily_stats()
    
    def get_ticker_data(self, ticker: str) -> Dict[str, Any]:
        """Get comprehensive data for a ticker from Alpha Vantage"""
        
        # Check cache first
        cache_key = f"{ticker}_full"
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            # Check if cache is fresh (less than 1 hour old)
            cache_time = datetime.fromisoformat(cached_data.get("timestamp", "2000-01-01"))
            if (datetime.now() - cache_time).total_seconds() < 3600:
                return cached_data
        
        # Check rate limits
        if not self._check_rate_limits():
            print(f"⚠️  Rate limit reached for {ticker}, using mock data")
            return self._get_mock_data(ticker)
        
        if not ALPHA_VANTAGE_AVAILABLE:
            return self._get_mock_data(ticker)
        
        try:
            print(f"📈 Fetching Alpha Vantage data for {ticker}...")
            
            data = {
                "success": True,
                "source": "alphavantage",
                "ticker": ticker,
                "timestamp": datetime.now().isoformat()
            }
            
            # 1. Get real-time quote (most important)
            quote_data = self._get_quote(ticker)
            data.update(quote_data)
            
            # 2. Get ONE technical indicator (to save API calls)
            if self.daily_call_count < self.max_daily_calls - 5:  # Save some calls
                tech_data = self._get_single_technical_indicator(ticker)
                data.update(tech_data)
            
            # 3. Skip fundamental data for now (saves API calls)
            # fund_data = self._get_fundamental_data(ticker)
            # data.update(fund_data)
            
            # 4. Calculate derived metrics
            derived = self._calculate_derived_metrics(data)
            data.update(derived)
            
            # Cache the result
            self.cache[cache_key] = data
            
            # Update rate limiting
            self._update_call_stats()
            
            return data
            
        except Exception as e:
            print(f"❌ Error fetching Alpha Vantage data for {ticker}: {e}")
            return self._get_mock_data(ticker)
    
    def _get_quote(self, ticker: str) -> Dict[str, Any]:
        """Get real-time quote data using free endpoints"""
        try:
            # Try daily adjusted data (free endpoint)
            data, meta_data = self.ts.get_daily_adjusted(symbol=ticker, outputsize='compact')
            
            if not data.empty:
                latest = data.iloc[0]
                return {
                    "current_price": float(latest['5. adjusted close']),  # Use adjusted close
                    "open_price": float(latest['1. open']),
                    "high_price": float(latest['2. high']),
                    "low_price": float(latest['3. low']),
                    "volume": int(latest['6. volume']),
                    "latest_timestamp": latest.name.isoformat(),
                    "dividend": float(latest['7. dividend amount']),
                    "split_coefficient": float(latest['8. split coefficient'])
                }
        except Exception as e:
            if "premium" not in str(e).lower():
                print(f"⚠️  Quote error for {ticker}: {e}")
        
        # Fallback to simple quote (free)
        try:
            data, meta_data = self.ts.get_quote_endpoint(symbol=ticker)
            if data is not None and not data.empty:
                return {
                    "current_price": float(data['05. price']),
                    "volume": int(data['06. volume']),
                    "latest_timestamp": data['07. latest trading day']
                }
        except Exception as e:
            if "premium" not in str(e).lower():
                print(f"⚠️  Quote endpoint error for {ticker}: {e}")
        
        return {}
    
    def _get_single_technical_indicator(self, ticker: str) -> Dict[str, Any]:
        """Get a single technical indicator (to save API calls)"""
        indicators = {}
        
        try:
            # Only get RSI (most useful for penny stocks)
            rsi_data, _ = self.ti.get_rsi(symbol=ticker, interval='daily', time_period=14, series_type='close')
            if not rsi_data.empty:
                indicators["rsi"] = float(rsi_data.iloc[0]['RSI'])
                print(f"  ✅ Got RSI: {indicators['rsi']:.1f}")
        
        except Exception as e:
            print(f"⚠️  RSI error for {ticker}: {e}")
        
        return indicators
    
    def _get_technical_indicators(self, ticker: str) -> Dict[str, Any]:
        """Get multiple technical indicators (for premium tier)"""
        indicators = {}
        
        try:
            # RSI (Relative Strength Index)
            rsi_data, _ = self.ti.get_rsi(symbol=ticker, interval='daily', time_period=14, series_type='close')
            if not rsi_data.empty:
                indicators["rsi"] = float(rsi_data.iloc[0]['RSI'])
        
        except Exception as e:
            print(f"⚠️  RSI error for {ticker}: {e}")
        
        # Only get more if we have API calls to spare
        if self.daily_call_count < self.max_daily_calls - 10:
            try:
                # SMA (Simple Moving Average)
                sma_data, _ = self.ti.get_sma(symbol=ticker, interval='daily', time_period=20, series_type='close')
                if not sma_data.empty:
                    indicators["sma_20"] = float(sma_data.iloc[0]['SMA'])
            
            except Exception as e:
                print(f"⚠️  SMA error for {ticker}: {e}")
        
        return indicators
    
    def _get_fundamental_data(self, ticker: str) -> Dict[str, Any]:
        """Get fundamental data (income statement, balance sheet)"""
        fundamentals = {}
        
        try:
            # Company Overview
            overview, _ = self.fd.get_company_overview(symbol=ticker)
            if not overview.empty:
                # Extract key metrics
                fundamentals["market_cap"] = float(overview.iloc[0]['MarketCapitalization']) if overview.iloc[0]['MarketCapitalization'] != 'None' else 0
                fundamentals["pe_ratio"] = float(overview.iloc[0]['PERatio']) if overview.iloc[0]['PERatio'] != 'None' else 0
                fundamentals["eps"] = float(overview.iloc[0]['EPS']) if overview.iloc[0]['EPS'] != 'None' else 0
                fundamentals["dividend_yield"] = float(overview.iloc[0]['DividendYield']) if overview.iloc[0]['DividendYield'] != 'None' else 0
                fundamentals["profit_margin"] = float(overview.iloc[0]['ProfitMargin']) if overview.iloc[0]['ProfitMargin'] != 'None' else 0
                fundamentals["operating_margin"] = float(overview.iloc[0]['OperatingMarginTTM']) if overview.iloc[0]['OperatingMarginTTM'] != 'None' else 0
                fundamentals["return_on_equity"] = float(overview.iloc[0]['ReturnOnEquityTTM']) if overview.iloc[0]['ReturnOnEquityTTM'] != 'None' else 0
                fundamentals["beta"] = float(overview.iloc[0]['Beta']) if overview.iloc[0]['Beta'] != 'None' else 1.0
        
        except Exception as e:
            print(f"⚠️  Fundamental data error for {ticker}: {e}")
        
        return fundamentals
    
    def _calculate_derived_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate derived metrics from raw data"""
        derived = {}
        
        # Calculate volatility (if we have historical data)
        price = data.get("current_price", 0)
        beta = data.get("beta", 1.0)
        
        # Simple volatility estimate
        if price > 0:
            # Base volatility on beta and price range
            if data.get("high_price") and data.get("low_price"):
                price_range = data["high_price"] - data["low_price"]
                volatility = (price_range / price) * beta * 10  # Rough annualized estimate
                derived["volatility"] = min(max(volatility, 0.1), 2.0)  # Cap at 200%
            else:
                derived["volatility"] = 0.3 * beta  # Default based on beta
        
        # Calculate risk score
        risk_score = 50  # Base
        
        # Adjust based on volatility
        volatility = derived.get("volatility", 0.3)
        if volatility > 0.5:
            risk_score += 20
        elif volatility < 0.2:
            risk_score -= 10
        
        # Adjust based on RSI
        rsi = data.get("rsi", 50)
        if rsi > 70:  # Overbought
            risk_score += 10
        elif rsi < 30:  # Oversold
            risk_score -= 5
        
        # Adjust based on price (penny stocks are riskier)
        if price < 1.0:
            risk_score += 30
        elif price < 5.0:
            risk_score += 15
        
        derived["risk_score"] = max(0, min(100, risk_score))
        
        # Calculate financial health
        financial_health = 0.5  # Base
        
        # Adjust based on fundamentals
        if data.get("profit_margin", 0) > 0.1:
            financial_health += 0.2
        if data.get("return_on_equity", 0) > 0.15:
            financial_health += 0.1
        if data.get("pe_ratio", 100) < 20 and data.get("pe_ratio", 0) > 0:
            financial_health += 0.1
        
        derived["financial_health"] = max(0.1, min(1.0, financial_health))
        
        # Check if penny stock
        derived["is_penny_stock"] = price < 5.0
        
        return derived
    
    def _get_mock_data(self, ticker: str) -> Dict[str, Any]:
        """Get mock data when Alpha Vantage is not available"""
        print(f"📈 Using mock Alpha Vantage data for {ticker}")
        
        import hashlib
        hash_val = int(hashlib.md5(ticker.encode()).hexdigest()[:8], 16)
        
        return {
            "current_price": 0.5 + (hash_val % 450) / 100,
            "rsi": 30 + (hash_val % 50),
            "macd": -0.5 + (hash_val % 100) / 100,
            "sma_20": 0.5 + (hash_val % 450) / 100,
            "volatility": 0.3 + (hash_val % 100) / 500,
            "risk_score": 50 + (hash_val % 50),
            "financial_health": 0.4 + (hash_val % 60) / 100,
            "is_penny_stock": True,
            "success": False,
            "source": "mock"
        }
    
    def get_technical_analysis(self, ticker: str) -> Dict[str, Any]:
        """Get comprehensive technical analysis"""
        data = self.get_ticker_data(ticker)
        
        analysis = {
            "ticker": ticker,
            "timestamp": datetime.now().isoformat(),
            "price_action": {
                "current": data.get("current_price", 0),
                "rsi": data.get("rsi", 50),
                "rsi_signal": "Neutral"
            },
            "trend": {
                "macd": data.get("macd", 0),
                "macd_signal": data.get("macd_signal", 0),
                "trend_direction": "Neutral"
            },
            "support_resistance": {
                "sma_20": data.get("sma_20", 0),
                "bb_upper": data.get("bb_upper", 0),
                "bb_lower": data.get("bb_lower", 0)
            },
            "momentum": {
                "volatility": data.get("volatility", 0.3),
                "risk_score": data.get("risk_score", 50)
            }
        }
        
        # Determine RSI signal
        rsi = data.get("rsi", 50)
        if rsi > 70:
            analysis["price_action"]["rsi_signal"] = "Overbought"
        elif rsi < 30:
            analysis["price_action"]["rsi_signal"] = "Oversold"
        
        # Determine trend direction
        macd = data.get("macd", 0)
        macd_signal = data.get("macd_signal", 0)
        if macd > macd_signal:
            analysis["trend"]["trend_direction"] = "Bullish"
        elif macd < macd_signal:
            analysis["trend"]["trend_direction"] = "Bearish"
        
        return analysis
    
    def get_multiple_tickers(self, tickers: List[str]) -> Dict[str, Dict[str, Any]]:
        """Get data for multiple tickers"""
        results = {}
        
        for ticker in tickers:
            results[ticker] = self.get_ticker_data(ticker)
        
        return results
    
    def filter_by_technical_signal(self, tickers: List[str], signal: str = "bullish") -> List[str]:
        """Filter tickers by technical signal"""
        filtered = []
        
        for ticker in tickers:
            data = self.get_ticker_data(ticker)
            
            if signal == "bullish":
                # Bullish conditions: RSI not overbought, MACD bullish, price above SMA
                rsi = data.get("rsi", 50)
                macd = data.get("macd", 0)
                macd_signal = data.get("macd_signal", 0)
                price = data.get("current_price", 0)
                sma = data.get("sma_20", price)
                
                if (rsi < 70 and  # Not overbought
                    macd > macd_signal and  # MACD bullish
                    price > sma * 0.95):  # Price near or above SMA
                    filtered.append(ticker)
            
            elif signal == "oversold":
                # Oversold conditions: RSI < 30
                rsi = data.get("rsi", 50)
                if rsi < 30:
                    filtered.append(ticker)
        
        return filtered
    
    def _check_rate_limits(self) -> bool:
        """Check if we can make another API call"""
        current_time = time.time()
        
        # Check minimum interval
        if current_time - self.last_call_time < self.min_call_interval:
            time_to_wait = self.min_call_interval - (current_time - self.last_call_time)
            print(f"⏳ Waiting {time_to_wait:.1f}s for rate limit...")
            time.sleep(time_to_wait)
        
        # Check daily limit
        if self.daily_call_count >= self.max_daily_calls:
            print(f"⚠️  Daily API limit reached ({self.max_daily_calls} calls)")
            return False
        
        return True
    
    def _update_call_stats(self):
        """Update call statistics"""
        self.last_call_time = time.time()
        self.daily_call_count += 1
        self._save_daily_stats()
        
        print(f"📊 API calls today: {self.daily_call_count}/{self.max_daily_calls}")
    
    def _load_daily_stats(self):
        """Load daily call statistics"""
        stats_file = os.path.join(self.cache_dir, "daily_stats.json")
        
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r') as f:
                    stats = json.load(f)
                
                # Check if stats are from today
                stats_date = stats.get("date", "2000-01-01")
                if stats_date == datetime.now().strftime("%Y-%m-%d"):
                    self.daily_call_count = stats.get("call_count", 0)
                else:
                    # Reset for new day
                    self.daily_call_count = 0
                    
            except Exception as e:
                print(f"⚠️  Error loading daily stats: {e}")
                self.daily_call_count = 0
        else:
            self.daily_call_count = 0
    
    def _save_daily_stats(self):
        """Save daily call statistics"""
        stats_file = os.path.join(self.cache_dir, "daily_stats.json")
        
        stats = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "call_count": self.daily_call_count,
            "last_updated": datetime.now().isoformat()
        }
        
        try:
            with open(stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving daily stats: {e}")


# Update TradeVantage integration in Trade Recommender
def update_tradevantage_with_alphavantage():
    """Update TradeVantage mock with real Alpha Vantage data"""
    
    integration_code = '''
# REAL ALPHA VANTAGE INTEGRATION
def get_tradevantage_data(ticker: str) -> Dict[str, Any]:
    """Get real technical data from Alpha Vantage API"""
    try:
        # Import our integration
        from alphavantage_integration import AlphaVantageIntegration
        
        integration = AlphaVantageIntegration(api_key="T0Z2YW467F7PNA9Z")
        data = integration.get_ticker_data(ticker)
        
        # Format for compatibility
        return {
            "rsi": data.get("rsi", 50),
            "volume": data.get("volume", 1000000),
            "price_change": data.get("price_change", 0),
            "support": data.get("bb_lower", 0.8),
            "resistance": data.get("bb_upper", 1.2),
            "trend": data.get("trend_direction", "neutral"),
            "is_penny": data.get("is_penny_stock", True),
            "success": data.get("success", False),
            "source": data.get("source", "unknown")
        }
        
    except Exception as e:
        print(f"⚠️  Alpha Vantage API error for {ticker}: {e}")
        # Fallback to mock data
        return get_tradevantage_mock_data(ticker)

def get_tradevantage_mock_data(ticker: str) -> Dict[str, Any]:
    """Mock data fallback"""
    import hashlib
    hash_val = int(hashlib.md5(ticker.encode()).hexdigest()[:8], 16)
    
    return {
        "rsi": 30 + (hash_val % 50),
        "volume": 500000 + (hash_val % 49500000),
        "price_change": -8 + (hash_val % 160) / 10,
        "support": 0.7 + (hash_val % 50) / 100,
        "resistance": 1.1 + (hash_val % 90) / 100,
        "trend": "bullish" if (hash_val % 3) != 0 else "bearish",
        "is_penny": True,
        "success": False,
        "source": "mock_fallback"
    }
'''

    # Create patch file
    patch_path = "/Users/cubiczan/.openclaw/workspace/alphavantage_patch.py"
    with open(patch_path, 'w') as f:
        f.write(integration_code)
    
    print(f"✅ Created Alpha Vantage integration patch: {patch_path}")
    return True


def test_alphavantage_integration():
    """Test the Alpha Vantage integration"""
    print("🧪 Testing Alpha Vantage Integration...")
    
    integration = AlphaVantageIntegration(api_key="T0Z2YW467F7PNA9Z")
    
    # Test with some tickers
    test_tickers = ["AAPL", "TSLA", "AMC", "BB"]
    
    for ticker in test_tickers:
        print(f"\n📈 Testing {ticker}:")
        data = integration.get_ticker_data(ticker)
        
        print(f"  Price: ${data.get('current_price', 0):.2f}")
        print(f"  Penny stock: {data.get('is_penny_stock', False)}")
        print(f"  RSI: {data.get('rsi', 0):.1f}")
        print(f"  Volatility: {data.get('volatility', 0):.1%}")
        print(f"  Risk score: {data.get('risk_score', 0):.0f}")
        print(f"  Source: {data.get('source', 'unknown')}")
        
        # Technical analysis
        if data.get("success", False):
            analysis = integration.get_technical_analysis(ticker)
            print(f"  Trend: {analysis['trend']['trend_direction']}")
            print(f"  RSI Signal: {analysis['price_action']['rsi_signal']}")
    
    # Test filtering
    bullish_tickers = integration.filter_by_technical_signal(test_tickers, "bullish")
    print(f"\n🎯 Bullish tickers: {bullish_tickers}")
    
    return True


if __name__ == "__main__":
    # Test the integration
    test_alphavantage_integration()
    
    # Update trade recommender
    update_tradevantage_with_alphavantage()
    
    print("\n✅ Alpha Vantage Integration Complete!")
    print("\n🚀 Next steps:")
    print("1. Review the integration code")
    print("2. Update trade-recommender/daily_reddit_analysis.py")
    print("3. Test with real technical analysis")
    print("4. Monitor API rate limits (5 calls/min, 500 calls/day free tier)")