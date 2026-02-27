
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
