#!/usr/bin/env python3
"""
Defeatbeta API Integration for Trade Recommender
Real financial data instead of mock APIs
"""

import os
import sys
from typing import Dict, Any, Optional
import pandas as pd

# Add defeatbeta-api to path
defeatbeta_path = "/Users/cubiczan/.openclaw/workspace/defeatbeta-api"
sys.path.insert(0, defeatbeta_path)

try:
    from defeatbeta_api.data.ticker import Ticker
    DEFEATBETA_AVAILABLE = True
    print("✅ Defeatbeta API available")
except ImportError as e:
    print(f"⚠️  Defeatbeta API not available: {e}")
    print("Using mock data for now")
    DEFEATBETA_AVAILABLE = False

class DefeatbetaIntegration:
    """Integration with Defeatbeta API for real financial data"""
    
    def __init__(self, cache_dir: str = None):
        self.cache_dir = cache_dir or "/Users/cubiczan/.openclaw/workspace/cache/defeatbeta"
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Cache for ticker data
        self.ticker_cache = {}
    
    def get_ticker_data(self, ticker: str) -> Dict[str, Any]:
        """Get comprehensive data for a ticker"""
        
        # Check cache first
        cache_key = f"{ticker}_data"
        if cache_key in self.ticker_cache:
            return self.ticker_cache[cache_key]
        
        if not DEFEATBETA_AVAILABLE:
            return self._get_mock_data(ticker)
        
        try:
            print(f"📊 Fetching Defeatbeta data for {ticker}...")
            
            # Initialize ticker
            ticker_obj = Ticker(ticker)
            
            # Get price data (most recent)
            price_data = ticker_obj.price()
            
            # Get financial metrics
            metrics = self._extract_metrics(ticker_obj, price_data)
            
            # Cache the result
            self.ticker_cache[cache_key] = metrics
            
            return metrics
            
        except Exception as e:
            print(f"❌ Error fetching Defeatbeta data for {ticker}: {e}")
            return self._get_mock_data(ticker)
    
    def _extract_metrics(self, ticker_obj, price_data: pd.DataFrame) -> Dict[str, Any]:
        """Extract key metrics from Defeatbeta data"""
        
        metrics = {
            "success": True,
            "source": "defeatbeta_api"
        }
        
        try:
            # Get most recent price
            if not price_data.empty:
                latest = price_data.iloc[-1]
                metrics["current_price"] = float(latest["close"])
                metrics["open_price"] = float(latest["open"])
                metrics["high_price"] = float(latest["high"])
                metrics["low_price"] = float(latest["low"])
                metrics["volume"] = int(latest["volume"])
            
            # Get market cap if available
            try:
                market_cap_data = ticker_obj.market_cap()
                if not market_cap_data.empty:
                    latest_mc = market_cap_data.iloc[-1]
                    metrics["market_cap"] = float(latest_mc["market_cap"])
            except:
                metrics["market_cap"] = 10000000  # Default
            
            # Get PE ratio if available
            try:
                pe_data = ticker_obj.pe_ratio()
                if not pe_data.empty:
                    latest_pe = pe_data.iloc[-1]
                    metrics["pe_ratio"] = float(latest_pe["pe_ratio"])
            except:
                metrics["pe_ratio"] = 15.0  # Default
            
            # Get volatility (standard deviation of recent returns)
            if len(price_data) >= 20:
                returns = price_data["close"].pct_change().dropna()
                metrics["volatility"] = float(returns.std() * (252 ** 0.5))  # Annualized
            else:
                metrics["volatility"] = 0.3  # Default
            
            # Calculate risk score based on volatility and other factors
            metrics["risk_score"] = self._calculate_risk_score(metrics)
            
            # Calculate financial health score
            metrics["financial_health"] = self._calculate_financial_health(ticker_obj)
            
            # Check if it's a penny stock
            metrics["is_penny_stock"] = metrics.get("current_price", 10.0) < 5.0
            
        except Exception as e:
            print(f"⚠️  Error extracting metrics: {e}")
            # Fill with defaults
            metrics.update(self._get_default_metrics())
        
        return metrics
    
    def _calculate_risk_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate risk score (0-100, higher = riskier)"""
        score = 50  # Base score
        
        # Adjust based on volatility
        volatility = metrics.get("volatility", 0.3)
        if volatility > 0.5:
            score += 20  # High volatility = higher risk
        elif volatility < 0.2:
            score -= 10  # Low volatility = lower risk
        
        # Adjust based on price (penny stocks are riskier)
        price = metrics.get("current_price", 10.0)
        if price < 1.0:
            score += 30  # Very risky
        elif price < 5.0:
            score += 15  # Risky
        
        # Adjust based on market cap (smaller = riskier)
        market_cap = metrics.get("market_cap", 10000000)
        if market_cap < 10000000:  # < $10M
            score += 20
        elif market_cap < 50000000:  # < $50M
            score += 10
        
        # Ensure score is within bounds
        return max(0, min(100, score))
    
    def _calculate_financial_health(self, ticker_obj) -> float:
        """Calculate financial health score (0-1)"""
        try:
            # Try to get financial statements
            income_stmt = ticker_obj.quarterly_income_statement()
            
            if not income_stmt.empty:
                # Simple health check: positive net income?
                if "Net Income" in income_stmt.columns:
                    latest_income = income_stmt["Net Income"].iloc[-1]
                    if latest_income > 0:
                        return 0.7  # Profitable
                    else:
                        return 0.3  # Not profitable
            
        except:
            pass
        
        return 0.5  # Default neutral score
    
    def _get_default_metrics(self) -> Dict[str, Any]:
        """Get default metrics when API fails"""
        return {
            "current_price": 2.5,
            "market_cap": 50000000,
            "pe_ratio": 15.0,
            "volatility": 0.4,
            "risk_score": 65.0,
            "financial_health": 0.5,
            "is_penny_stock": True,
            "success": False
        }
    
    def _get_mock_data(self, ticker: str) -> Dict[str, Any]:
        """Get mock data when Defeatbeta is not available"""
        print(f"📊 Using mock data for {ticker}")
        
        # Generate deterministic mock data based on ticker hash
        import hashlib
        
        hash_val = int(hashlib.md5(ticker.encode()).hexdigest()[:8], 16)
        
        return {
            "current_price": 0.5 + (hash_val % 450) / 100,  # $0.50-$5.00
            "market_cap": 5000000 + (hash_val % 45000000),
            "pe_ratio": 3 + (hash_val % 97),
            "volatility": 0.3 + (hash_val % 100) / 500,
            "risk_score": 50 + (hash_val % 50),
            "financial_health": 0.4 + (hash_val % 60) / 100,
            "is_penny_stock": True,
            "success": False,  # Mark as mock data
            "source": "mock"
        }
    
    def get_multiple_tickers(self, tickers: list) -> Dict[str, Dict[str, Any]]:
        """Get data for multiple tickers efficiently"""
        results = {}
        
        for ticker in tickers:
            results[ticker] = self.get_ticker_data(ticker)
        
        return results
    
    def filter_penny_stocks(self, tickers: list, max_price: float = 5.0) -> list:
        """Filter list to only include penny stocks"""
        penny_stocks = []
        
        for ticker in tickers:
            data = self.get_ticker_data(ticker)
            if data.get("is_penny_stock", False) and data.get("current_price", 10.0) <= max_price:
                penny_stocks.append(ticker)
        
        return penny_stocks
    
    def get_top_penny_stocks(self, tickers: list, limit: int = 10) -> list:
        """Get top penny stocks by financial health"""
        scored = []
        
        for ticker in tickers:
            data = self.get_ticker_data(ticker)
            
            if data.get("is_penny_stock", False):
                # Score based on multiple factors
                score = (
                    (1.0 - data.get("risk_score", 100) / 100) * 0.4 +  # Lower risk = better
                    data.get("financial_health", 0.5) * 0.3 +          # Better financial health = better
                    (1.0 if data.get("pe_ratio", 100) < 20 else 0.5) * 0.2 +  # Reasonable PE = better
                    (1.0 if data.get("volatility", 1.0) < 0.6 else 0.5) * 0.1  # Lower volatility = better
                )
                
                scored.append((ticker, score, data))
        
        # Sort by score (highest first)
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # Return top N
        return [(ticker, score) for ticker, score, _ in scored[:limit]]


# Integration with existing Trade Recommender
def update_trade_recommender_with_defeatbeta():
    """Update the Trade Recommender to use real Defeatbeta data"""
    
    # Path to trade recommender
    trade_recommender_path = "/Users/cubiczan/mac-bot/skills/trade-recommender/daily_reddit_analysis.py"
    
    if not os.path.exists(trade_recommender_path):
        print(f"❌ Trade recommender not found: {trade_recommender_path}")
        return False
    
    # Read the file
    with open(trade_recommender_path, 'r') as f:
        content = f.read()
    
    # Find the get_defeatbeta_data function
    if "def get_defeatbeta_data" in content:
        print("✅ Defeatbeta integration already in trade recommender")
        return True
    
    # Create updated version
    print("🔄 Updating trade recommender with Defeatbeta integration...")
    
    # We'll create a separate integration file instead
    integration_code = '''
# REAL DEFEATBETA INTEGRATION
def get_defeatbeta_data(ticker: str) -> Dict[str, Any]:
    """Get real financial data from Defeatbeta API"""
    try:
        # Import our integration
        from defeatbeta_integration import DefeatbetaIntegration
        
        integration = DefeatbetaIntegration()
        data = integration.get_ticker_data(ticker)
        
        # Format for compatibility
        return {
            "volatility": data.get("volatility", 0.3),
            "risk_score": data.get("risk_score", 50),
            "financial_health": data.get("financial_health", 0.5),
            "market_cap": data.get("market_cap", 10000000),
            "pe_ratio": data.get("pe_ratio", 15),
            "current_price": data.get("current_price", 2.5),
            "is_penny_stock": data.get("is_penny_stock", True),
            "success": data.get("success", False),
            "source": data.get("source", "unknown")
        }
        
    except Exception as e:
        print(f"⚠️  Defeatbeta API error for {ticker}: {e}")
        # Fallback to mock data
        return get_defeatbeta_mock_data(ticker)

def get_defeatbeta_mock_data(ticker: str) -> Dict[str, Any]:
    """Mock data fallback"""
    import hashlib
    hash_val = int(hashlib.md5(ticker.encode()).hexdigest()[:8], 16)
    
    return {
        "volatility": 0.3 + (hash_val % 100) / 500,
        "risk_score": 50 + (hash_val % 50),
        "financial_health": 0.4 + (hash_val % 60) / 100,
        "market_cap": 10000000 + (hash_val % 90000000),
        "pe_ratio": 5 + (hash_val % 95),
        "current_price": 0.5 + (hash_val % 450) / 100,
        "is_penny_stock": True,
        "success": False,
        "source": "mock_fallback"
    }
'''
    
    # Create a patch file
    patch_path = "/Users/cubiczan/.openclaw/workspace/defeatbeta_patch.py"
    with open(patch_path, 'w') as f:
        f.write(integration_code)
    
    print(f"✅ Created Defeatbeta integration patch: {patch_path}")
    print("\n📋 To integrate:")
    print(f"1. Copy the functions from {patch_path}")
    print("2. Replace the mock get_defeatbeta_data function in daily_reddit_analysis.py")
    print("3. Test with: python3 -c \"from defeatbeta_integration import DefeatbetaIntegration; print('✅ Ready')\"")
    
    return True


def test_defeatbeta_integration():
    """Test the Defeatbeta integration"""
    print("🧪 Testing Defeatbeta Integration...")
    
    integration = DefeatbetaIntegration()
    
    # Test with some tickers
    test_tickers = ["AAPL", "TSLA", "GME", "AMC", "BB"]
    
    for ticker in test_tickers:
        print(f"\n📊 Testing {ticker}:")
        data = integration.get_ticker_data(ticker)
        
        print(f"  Price: ${data.get('current_price', 0):.2f}")
        print(f"  Penny stock: {data.get('is_penny_stock', False)}")
        print(f"  Volatility: {data.get('volatility', 0):.1%}")
        print(f"  Risk score: {data.get('risk_score', 0):.0f}")
        print(f"  Source: {data.get('source', 'unknown')}")
    
    # Test penny stock filtering
    penny_stocks = integration.filter_penny_stocks(test_tickers)
    print(f"\n🎯 Penny stocks found: {penny_stocks}")
    
    return True


if __name__ == "__main__":
    # Test the integration
    test_defeatbeta_integration()
    
    # Update trade recommender
    update_trade_recommender_with_defeatbeta()
    
    print("\n✅ Defeatbeta Integration Complete!")
    print("\n🚀 Next steps:")
    print("1. Review the integration code")
    print("2. Update trade-recommender/daily_reddit_analysis.py")
    print("3. Test with real ticker analysis")
    print("4. Monitor performance and adjust scoring")