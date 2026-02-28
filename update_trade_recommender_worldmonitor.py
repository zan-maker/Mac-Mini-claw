#!/usr/bin/env python3
"""
Update Trade Recommender with World Monitor integration
"""

import os
import shutil

def update_daily_analysis_script():
    """Update daily_reddit_analysis.py with World Monitor integration"""
    script_path = "/Users/cubiczan/mac-bot/skills/trade-recommender/daily_reddit_analysis.py"
    
    # Read current script
    with open(script_path, 'r') as f:
        content = f.read()
    
    # Find the imports section and add World Monitor import
    if "from optimized_browser_wrapper import" in content:
        # Add World Monitor import after optimized_browser_wrapper import
        new_import = """try:
    from worldmonitor_integration import WorldMonitorIntegration
    WORLD_MONITOR_AVAILABLE = True
except ImportError:
    print("⚠️  worldmonitor_integration not found. World Monitor signals unavailable.")
    WORLD_MONITOR_AVAILABLE = False
    # Mock class for testing
    class WorldMonitorIntegration:
        def __init__(self, **kwargs):
            pass
        def get_macro_signals(self, **kwargs):
            return {"verdict": "UNKNOWN", "bullish_count": 0, "total_count": 0}
        def analyze_kalshi_arbitrage(self, kalshi_data):
            return []
        def generate_daily_report(self, kalshi_data):
            return {"report_date": "2026-02-27", "macro_overview": {"verdict": "UNKNOWN"}}
"""
        
        # Insert after optimized_browser_wrapper import
        import_end = content.find("except ImportError:")
        if import_end != -1:
            # Find the line before "except ImportError:"
            lines = content[:import_end].split('\n')
            for i, line in enumerate(reversed(lines)):
                if line.strip() and not line.strip().startswith('#'):
                    insert_point = import_end - sum(len(l) + 1 for l in lines[-i:])
                    break
            
            content = content[:insert_point] + new_import + content[insert_point:]
    
    # Find the analyze_reddit_posts function and add World Monitor analysis
    if "def analyze_reddit_posts" in content:
        # We need to modify the function to include World Monitor signals
        # This is a bit complex, so let's create a new version
        pass
    
    # For now, let's create a separate script that combines everything
    return create_combined_script()

def create_combined_script():
    """Create a combined script with World Monitor integration"""
    combined_script = """#!/usr/bin/env python3
"""
Daily Reddit Penny Stock Analysis with World Monitor Integration
Uses Agent Browser + World Monitor for predictive signals + Kalshi arbitrage
"""

import os
import sys
import json
import re
from datetime import datetime
from typing import List, Dict, Any
import requests

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/Users/cubiczan/.openclaw/workspace")

try:
    from optimized_browser_wrapper import OptimizedBrowser, BrowserSnapshot, BrowserElement
    BROWSER_AVAILABLE = True
except ImportError:
    print("⚠️  optimized_browser_wrapper not found. Using mock data for testing.")
    BROWSER_AVAILABLE = False
    # Mock classes for testing
    class BrowserSnapshot:
        def __init__(self):
            self.elements = []
            self.token_count = 0
    class BrowserElement:
        def __init__(self, text=""):
            self.text = text
    class OptimizedBrowser:
        def __init__(self, **kwargs):
            pass
        def open(self, url):
            print(f"Mock: Opening {url}")
        def get_optimized_snapshot(self):
            return BrowserSnapshot()
        def close(self):
            pass

try:
    from worldmonitor_integration import WorldMonitorIntegration
    WORLD_MONITOR_AVAILABLE = True
except ImportError:
    print("⚠️  worldmonitor_integration not found. World Monitor signals unavailable.")
    WORLD_MONITOR_AVAILABLE = False
    # Mock class for testing
    class WorldMonitorIntegration:
        def __init__(self, **kwargs):
            pass
        def get_macro_signals(self, **kwargs):
            return {"verdict": "UNKNOWN", "bullish_count": 0, "total_count": 0}
        def analyze_kalshi_arbitrage(self, kalshi_data):
            return []
        def generate_daily_report(self, kalshi_data):
            return {"report_date": "2026-02-27", "macro_overview": {"verdict": "UNKNOWN"}}

try:
    from defeatbeta_integration import get_defeatbeta_data
    DEFEATBETA_AVAILABLE = True
except ImportError:
    print("⚠️  defeatbeta_integration not found. Using mock financial data.")
    DEFEATBETA_AVAILABLE = False
    def get_defeatbeta_data(ticker):
        return {"price": 1.23, "volume": 1000000, "volatility": 0.3}

try:
    from alphavantage_integration import AlphaVantageIntegration
    ALPHA_VANTAGE_AVAILABLE = True
except ImportError:
    print("⚠️  alphavantage_integration not found. Alpha Vantage data unavailable.")
    ALPHA_VANTAGE_AVAILABLE = False
    class AlphaVantageIntegration:
        def __init__(self):
            pass
        def get_stock_price(self, symbol):
            return 1.23
        def get_technical_indicators(self, symbol):
            return {"rsi": 50, "macd": 0, "sma": 1.2}

def extract_tickers_from_text(text: str) -> List[str]:
    \"\"\"Extract stock tickers from text (1-5 letters, all caps)\"\"\"
    ticker_pattern = r'\\$?([A-Z]{1,5})\\b'
    matches = re.findall(ticker_pattern, text)
    
    common_words = {'THE', 'AND', 'FOR', 'YOU', 'ARE', 'ALL', 'HAS', 'WAS', 
                    'HAD', 'BUT', 'NOT', 'CAN', 'OUT', 'NOW', 'GET', 'SEE'}
    return [ticker for ticker in matches if ticker not in common_words]

def get_kalshi_data() -> Dict[str, Any]:
    \"\"\"Get Kalshi prediction market data\"\"\"
    # TODO: Implement actual Kalshi API integration
    # For now, return mock data
    return {
        "markets": [
            {
                "id": "market_fed_rates",
                "title": "Will the Fed raise rates in Q1 2026?",
                "yes_price": 0.45,
                "no_price": 0.50,
                "volume": 15000,
                "category": "Economics"
            },
            {
                "id": "market_recession", 
                "title": "Will there be a recession in 2026?",
                "yes_price": 0.30,
                "no_price": 0.65,
                "volume": 25000,
                "category": "Economics"
            },
            {
                "id": "market_bitcoin",
                "title": "Will Bitcoin reach $100K in 2026?",
                "yes_price": 0.25,
                "no_price": 0.70,
                "volume": 50000,
                "category": "Crypto"
            },
            {
                "id": "market_election",
                "title": "Will the incumbent win the 2026 election?",
                "yes_price": 0.55,
                "no_price": 0.40,
                "volume": 30000,
                "category": "Politics"
            },
            {
                "id": "market_war",
                "title": "Will there be a new major conflict in 2026?",
                "yes_price": 0.35,
                "no_price": 0.60,
                "volume": 20000,
                "category": "Geopolitics"
            }
        ],
        "timestamp": datetime.now().isoformat()
    }

def analyze_with_world_monitor(reddit_tickers: List[Dict], kalshi_data: Dict) -> Dict[str, Any]:
    \"\"\"Analyze trading opportunities with World Monitor signals\"\"\"
    
    if not WORLD_MONITOR_AVAILABLE:
        return {
            "world_monitor_available": False,
            "macro_signals": {"verdict": "UNKNOWN"},
            "kalshi_opportunities": [],
            "combined_opportunities": []
        }
    
    wm = WorldMonitorIntegration()
    
    # Get World Monitor signals
    macro_signals = wm.get_macro_signals()
    
    # Analyze Kalshi arbitrage opportunities
    kalshi_opportunities = wm.analyze_kalshi_arbitrage(kalshi_data)
    
    # Combine Reddit tickers with World Monitor analysis
    combined_opportunities = []
    
    for ticker_info in reddit_tickers[:10]:  # Top 10 from Reddit
        ticker = ticker_info.get("ticker", "")
        
        # Get financial data
        if DEFEATBETA_AVAILABLE:
            financial_data = get_defeatbeta_data(ticker)
            price = financial_data.get("price", 0)
        else:
            price = 1.23  # Mock price
        
        # Skip large cap stocks (price >= $5)
        if price >= 5.0:
            continue
        
        # Calculate opportunity score
        mention_count = ticker_info.get("mention_count", 1)
        sentiment = ticker_info.get("sentiment", 0.5)
        
        # Base score from Reddit
        base_score = mention_count * (1 + abs(sentiment - 0.5))
        
        # Adjust based on World Monitor macro signals
        macro_verdict = macro_signals.get("verdict", "UNKNOWN")
        macro_score = macro_signals.get("bullish_count", 0) / max(macro_signals.get("total_count", 1), 1)
        
        if macro_verdict == "BUY" and macro_score > 0.6:
            base_score *= 1.3
        elif macro_verdict == "CASH" and macro_score < 0.4:
            base_score *= 0.7
        
        # Check if ticker relates to any Kalshi opportunities
        ticker_lower = ticker.lower()
        related_kalshi = []
        
        for opp in kalshi_opportunities:
            title = opp.get("market_title", "").lower()
            if ticker_lower in title or any(word in title for word in ["stock", "market", "economy", "finance"]):
                related_kalshi.append(opp)
        
        # If related to Kalshi opportunities, boost score
        if related_kalshi:
            best_kalshi_score = max([opp.get("opportunity_score", 0) for opp in related_kalshi], default=0)
            base_score *= (1 + best_kalshi_score / 100)
        
        opportunity = {
            "ticker": ticker,
            "company_name": ticker_info.get("company_name", "Unknown"),
            "price": price,
            "reddit_mentions": mention_count,
            "reddit_sentiment": sentiment,
            "world_monitor_macro": macro_verdict,
            "world_monitor_score": macro_score,
            "related_kalshi_opportunities": len(related_kalshi),
            "combined_score": round(base_score, 2),
            "analysis": self._generate_analysis(ticker_info, macro_signals, related_kalshi)
        }
        
        combined_opportunities.append(opportunity)
    
    # Sort by combined score
    combined_opportunities.sort(key=lambda x: x.get("combined_score", 0), reverse=True)
    
    return {
        "world_monitor_available": True,
        "macro_signals": macro_signals,
        "kalshi_opportunities": kalshi_opportunities[:5],  # Top 5
        "combined_opportunities": combined_opportunities[:10]  # Top 10
    }

def _generate_analysis(ticker_info: Dict, macro_signals: Dict, related_kalshi: List) -> str:
    \"\"\"Generate analysis text for opportunity\"\"\"
    ticker = ticker_info.get("ticker", "")
    sentiment = ticker_info.get("sentiment", 0.5)
    macro_verdict = macro_signals.get("verdict", "UNKNOWN")
    
    analysis_parts = []
    
    # Reddit analysis
    if sentiment > 0.6:
        analysis_parts.append(f"Bullish sentiment on Reddit ({sentiment:.1%} positive)")
    elif sentiment < 0.4:
        analysis_parts.append(f"Bearish sentiment on Reddit ({sentiment:.1%} positive)")
    else:
        analysis_parts.append(f"Neutral sentiment on Reddit ({sentiment:.1%} positive)")
    
    # World Monitor analysis
    if macro_verdict == "BUY":
        analysis_parts.append("World Monitor signals BULLISH macro environment")
    elif macro_verdict == "CASH":
        analysis_parts.append("World Monitor signals BEARISH macro environment (cash recommended)")
    else:
        analysis_parts.append("World Monitor signals UNKNOWN macro environment")
    
    # Kalshi analysis
    if related_kalshi:
        kalshi_count = len(related_kalshi)
        best_gap = max([opp.get("arbitrage_percentage", 0) for opp in related_kalshi], default=0)
        analysis_parts.append(f"Related to {kalshi_count} Kalshi arbitrage opportunities (best gap: {best_gap:.1f}%)")
    
    # Price analysis
    price = ticker_info.get("price", 0)
    if price < 1.0:
        analysis_parts.append("Ultra-low price (<$1) - high risk/reward")
    elif price < 2.0:
        analysis_parts.append("Low price ($1-$2) - moderate risk")
    else:
        analysis_parts.append(f"Price ${price:.2f} - typical penny stock range")
    
    return " | ".join(analysis_parts)

def generate_daily_report(analysis_results: Dict) -> str:
    \"\"\"Generate daily report in markdown format\"\"\"
    report = []
    
    # Header
    report.append("# Daily Trade Recommendations with World Monitor")
    report.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    report.append("")
    
    # World Monitor Status
    if analysis_results.get("world_monitor_available", False):
        macro_signals = analysis_results.get("macro_signals", {})
        verdict = macro_signals.get("verdict", "UNKNOWN")
        bullish = macro_signals.get("bullish_count", 0)
        total = macro_signals.get("total_count", 0)
        
        report.append("## 🌍 World Monitor Signals")
        report.append(f"- **Macro Verdict:** {verdict}")
        report.append(f"- **Bullish Signals:** {bullish}/{total} ({bullish/max(total,1)*100:.0f}%)")
        report.append("")
    else:
        report.append("## ⚠️ World Monitor Unavailable")
        report.append("Using fallback analysis only")
        report.append("")
    
    # Kalshi Arbitrage Opportunities
    kalshi_opps = analysis_results.get("kalshi_opportunities", [])
    if kalshi_opps:
        report.append("## 🎯 Kalshi Arbitrage Opportunities")
        report.append("")
        report.append("| Market | Arbitrage Gap | Type | Score | Action |")
        report.append("|--------|---------------|------|-------|--------|")
        
        for opp in kalshi_opps[:5]:
            market = opp.get("market_title", "Unknown")[:40]
            gap = opp.get("arbitrage_percentage", 0)
            opp_type = opp.get("opportunity_type", "UNKNOWN")
            score = opp.get("opportunity_score", 0)
            action = opp.get("recommended_action", "MONITOR")
            
            report.append(f"| {market}... | {gap:.1f}% | {opp_type} | {score:.1f} | {action} |")
        
        report.append("")
    
    # Combined Stock Opportunities
    combined_opps = analysis_results.get("combined_opportunities", [])
    if combined_opps:
        report.append("## 📈 Top Penny Stock Opportunities")
        report.append("")
        report.append("| Ticker | Price | Reddit Mentions | Sentiment | WM Macro | Combined Score |")
        report.append("|--------|-------|-----------------|-----------|----------|----------------|")
        
        for opp in combined_opps[:5]:
            ticker = opp.get("ticker", "UNKN")
            price = opp.get("price", 0)
            mentions = opp.get("reddit_mentions", 0)
            sentiment = opp.get("reddit_sentiment", 0.5)
            wm_macro = opp.get("world_monitor_macro", "UNKNOWN")
            score = opp.get("combined_score", 0)
            
            report.append(f"| **{ticker}** | ${price:.2f} | {mentions} | {sentiment:.0%} | {wm_macro} | {score:.1f} |")
        
        report.append("")
        
        # Detailed analysis for top 3
        report.append("## 🔍 Detailed Analysis")
        report.append("")
        
        for i, opp in enumerate(combined_opps[:3]):
            ticker = opp.get("ticker", "UNKN")
            analysis = opp.get("analysis", "