#!/usr/bin/env python3
"""
Integrate Agent Browser with ALL OpenClaw Agents
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path

def integrate_with_trade_recommender():
    """Add browser capabilities to Trade Recommender"""
    print("\n" + "="*60)
    print("INTEGRATING AGENT BROWSER: TRADE RECOMMENDER")
    print("="*60)
    
    skill_dir = "/Users/cubiczan/mac-bot/skills/trade-recommender"
    
    if not os.path.exists(skill_dir):
        print(f"❌ Skill directory not found: {skill_dir}")
        return False
    
    # Create browser integration file
    integration_file = os.path.join(skill_dir, "BROWSER_CAPABILITIES.md")
    
    integration_content = f"""# Agent Browser Capabilities - Trade Recommender

## 🚀 Browser Automation Enabled
**Integration Date:** {datetime.now().isoformat()}
**Status:** ✅ ACTIVE

## 📊 Trading-Specific Browser Use Cases

### 1. Market Data Collection
```python
from agent_browser_wrapper import AgentBrowser

# Real-time market data
browser = AgentBrowser(session="market-data")
browser.open("https://finance.yahoo.com")
browser.search_workflow("https://finance.yahoo.com", "AAPL stock")
# Extract price, charts, news
```

### 2. Earnings Calendar Scraping
```python
# Navigate to earnings calendar
browser.open("https://www.nasdaq.com/market-activity/earnings")
snapshot = browser.snapshot()
# Extract upcoming earnings dates
```

### 3. News Sentiment Analysis
```python
# Collect financial news
browser.open("https://www.bloomberg.com/markets")
# Extract headlines, sentiment indicators
```

### 4. SEC Filings Access
```python
# Access EDGAR database
browser.open("https://www.sec.gov/edgar/searchedgar/companysearch.html")
browser.fill("@e1", "AAPL")  # Company search
browser.click("@e2")  # Search button
# Extract 10-Q, 10-K filings
```

### 5. Options Chain Analysis
```python
# Options data from CBOE or brokers
browser.open("https://www.cboe.com/delayed_quotes/aapl/quote_table")
# Extract options chains, IV, Greeks
```

## 🔧 Installation & Setup

### Prerequisites:
```bash
# Install Agent Browser globally
npm install -g agent-browser

# Download Chromium (first time)
agent-browser install
```

### Python Wrapper:
```python
# The wrapper is available at:
# /Users/cubiczan/.openclaw/workspace/agent_browser_wrapper.py

# Import in your trading scripts:
from agent_browser_wrapper import AgentBrowser, BrowserSnapshot
```

## 🎯 Example: Real-Time Stock Analysis

```python
import json
from agent_browser_wrapper import AgentBrowser

class TradingBrowser:
    def __init__(self):
        self.browser = AgentBrowser(
            session="trading-analysis",
            verbose=True
        )
    
    def get_stock_data(self, symbol: str):
        """Get real-time stock data from Yahoo Finance"""
        
        # Navigate to Yahoo Finance
        if not self.browser.open(f"https://finance.yahoo.com/quote/{symbol}"):
            return None
        
        # Wait for page load
        self.browser.wait(timeout=10000)
        
        # Get snapshot
        snapshot = self.browser.snapshot()
        if not snapshot:
            return None
        
        # Extract key data points
        data = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "price": self._extract_price(snapshot),
            "change": self._extract_change(snapshot),
            "volume": self._extract_volume(snapshot),
            "market_cap": self._extract_market_cap(snapshot),
            "pe_ratio": self._extract_pe_ratio(snapshot)
        }
        
        # Take screenshot for visual confirmation
        screenshot = self.browser.screenshot(annotate=True)
        if screenshot:
            data["screenshot"] = screenshot
        
        return data
    
    def _extract_price(self, snapshot):
        """Extract current price from snapshot"""
        # Look for price elements
        for element in snapshot.elements:
            if element.role in ["heading", "text"] and "$" in element.name:
                # Parse price
                return element.name
        return None
    
    def _extract_change(self, snapshot):
        """Extract price change"""
        for element in snapshot.elements:
            if element.role == "text" and ("+" in element.name or "-" in element.name):
                return element.name
        return None
    
    def _extract_volume(self, snapshot):
        """Extract trading volume"""
        for element in snapshot.elements:
            if element.role == "text" and "Volume" in element.name:
                return element.name
        return None
    
    def _extract_market_cap(self, snapshot):
        """Extract market capitalization"""
        for element in snapshot.elements:
            if element.role == "text" and "Market Cap" in element.name:
                return element.name
        return None
    
    def _extract_pe_ratio(self, snapshot):
        """Extract P/E ratio"""
        for element in snapshot.elements:
            if element.role == "text" and "P/E Ratio" in element.name:
                return element.name
        return None
    
    def close(self):
        """Close browser"""
        self.browser.close()

# Usage
trading_browser = TradingBrowser()
aapl_data = trading_browser.get_stock_data("AAPL")
if aapl_data:
    print(f"AAPL Data: {json.dumps(aapl_data, indent=2)}")
trading_browser.close()
```

## 📈 Advanced Trading Scenarios

### Scenario 1: Multi-Source Data Aggregation
```python
def aggregate_market_data(symbol):
    """Aggregate data from multiple sources"""
    sources = [
        ("Yahoo Finance", f"https://finance.yahoo.com/quote/{symbol}"),
        ("MarketWatch", f"https://www.marketwatch.com/investing/stock/{symbol}"),
        ("NASDAQ", f"https://www.nasdaq.com/market-activity/stocks/{symbol}")
    ]
    
    aggregated = {}
    for source_name, url in sources:
        browser = AgentBrowser(session=f"source-{source_name}")
        if browser.open(url):
            snapshot = browser.snapshot()
            if snapshot:
                aggregated[source_name] = extract_key_metrics(snapshot)
        browser.close()
    
    return aggregated
```

### Scenario 2: Options Chain Analysis
```python
def analyze_options_chain(symbol, expiration):
    """Analyze options chain for given expiration"""
    browser = AgentBrowser(session="options-analysis")
    
    # Navigate to options page
    url = f"https://www.nasdaq.com/market-activity/stocks/{symbol}/option-chain"
    if browser.open(url):
        # Select expiration date
        browser.find_and_click("combobox", "Expiration Date")
        browser.find_and_click("option", expiration)
        
        # Extract options data
        snapshot = browser.snapshot()
        options_data = extract_options_data(snapshot)
        
        browser.close()
        return options_data
    
    return None
```

### Scenario 3: News Sentiment Pipeline
```python
def collect_financial_news(symbol, days=7):
    """Collect and analyze financial news"""
    browser = AgentBrowser(session="news-collection")
    
    # Google News search
    query = f"{symbol} stock news last {days} days"
    if browser.search_workflow("https://news.google.com", query):
        snapshot = browser.snapshot()
        
        # Extract news articles
        articles = []
        for element in snapshot.elements:
            if element.role == "link" and "article" in element.attributes.get("class", ""):
                articles.append({
                    "title": element.name,
                    "url": element.attributes.get("href", ""),
                    "source": extract_source(element)
                })
        
        browser.close()
        return articles
    
    return None
```

## 🔒 Security & Best Practices

### 1. Session Isolation
```python
# Use different sessions for different tasks
market_data_session = AgentBrowser(session="market-data")
news_session = AgentBrowser(session="news-collection")
options_session = AgentBrowser(session="options-analysis")
```

### 2. Rate Limiting
```python
import time

def rate_limited_browse(urls, delay=2):
    """Browse with rate limiting"""
    for url in urls:
        browser = AgentBrowser()
        browser.open(url)
        # Do work...
        browser.close()
        time.sleep(delay)  # Rate limit
```

### 3. Error Handling
```python
try:
    browser = AgentBrowser()
    if not browser.open(url):
        print(f"Failed to open {url}")
        # Fallback to alternative source
        fallback_url = get_fallback_url(url)
        browser.open(fallback_url)
except Exception as e:
    print(f"Browser error: {e}")
    # Log error and continue
finally:
    browser.close()
```

### 4. Data Validation
```python
def validate_stock_data(data):
    """Validate extracted stock data"""
    required_fields = ["symbol", "price", "timestamp"]
    for field in required_fields:
        if field not in data or not data[field]:
            return False
    
    # Price validation
    try:
        price = float(data["price"].replace("$", "").replace(",", ""))
        if price <= 0 or price > 1000000:  # Sanity check
            return False
    except:
        return False
    
    return True
```

## 🚀 Integration with Trade Recommender

### Update Your Trade Analysis Scripts:
```python
# Before: Static data sources
# After: Dynamic web data collection

from agent_browser_wrapper import AgentBrowser

class EnhancedTradeAnalyzer:
    def analyze_with_web_data(self, symbol):
        # 1. Get real-time web data
        browser = AgentBrowser()
        web_data = self.collect_web_data(browser, symbol)
        
        # 2. Combine with existing analysis
        analysis = self.technical_analysis(symbol)
        analysis["web_data"] = web_data
        
        # 3. Enhanced recommendation
        recommendation = self.generate_recommendation(analysis)
        
        return recommendation
```

### New Capabilities Added:
1. **Real-time price verification** - Cross-check against web sources
2. **News sentiment integration** - Incorporate breaking news
3. **Options market analysis** - Live options chain data
4. **Competitor analysis** - Compare with sector peers
5. **Regulatory filings** - Access SEC documents

## 📊 Performance Monitoring

### Browser Performance Metrics:
```python
class BrowserPerformance:
    def __init__(self):
        self.metrics = {
            "page_load_times": [],
            "extraction_success_rate": 0,
            "error_count": 0
        }
    
    def track_performance(self, url, success, load_time):
        self.metrics["page_load_times"].append(load_time)
        if success:
            self.metrics["extraction_success_rate"] += 1
        else:
            self.metrics["error_count"] += 1
        
        # Log to file
        with open("browser_performance.log", "a") as f:
            f.write(f"{datetime.now()},{url},{success},{load_time}\\n")
```

## 🎯 Quick Start Commands

```bash
# Test browser installation
agent-browser --version

# Test with Yahoo Finance
agent-browser open https://finance.yahoo.com
agent-browser snapshot -i --json

# Test with your trading script
python3 /Users/cubiczan/.openclaw/workspace/test_trading_browser.py
```

## 🔗 Resources

- **Agent Browser Docs**: https://agent-browser.vercel.app
- **Wrapper Code**: `/Users/cubiczan/.openclaw/workspace/agent_browser_wrapper.py`
- **Trading Data Sources**:
  - Yahoo Finance: https://finance.yahoo.com
  - MarketWatch: https://www.marketwatch.com
  - NASDAQ: https://www.nasdaq.com
  - SEC EDGAR: https://www.sec.gov/edgar

## ✅ Next Steps

1. **Test Installation**: Run the test commands above
2. **Integrate**: Add browser calls to your trading scripts
3. **Monitor**: Check browser performance logs
4. **Optimize**: Adjust timeouts and error handling

**Your Trade Recommender now has real-time web data capabilities!** 📈🌐
"""
    
    with open(integration_file, 'w') as f:
        f.write(integration_content)
    
    print(f"✅ Created: {integration_file}")
    
    # Copy wrapper to skill directory
    wrapper_src = "/Users/cubiczan/.openclaw/workspace/agent_browser_wrapper.py"
    wrapper_dst = os.path.join(skill_dir, "agent_browser_wrapper.py")
    
    if os.path.exists(wrapper_src):
        shutil.copy2(wrapper_src, wrapper_dst)
        print(f"✅ Copied wrapper: {wrapper_dst}")
    
    return True

def integrate_with_roi_analyst():
    """Add browser capabilities to ROI Analyst"""
    print("\n" + "="*60)
    print("INTEGRATING AGENT BROWSER: ROI ANALYST")
    print("="*60)
    
    skill_dir = "/Users/cubiczan/mac-bot/skills/roi-analyst"
    
    if not os.path.exists(skill_dir):
        print(f"❌ Skill directory not found: {skill_dir}")
        return False
    
    # Create browser integration file
    integration_file = os.path.join(skill_dir, "BROWSER_CAPABILITIES.md")
    
    integration_content = f"""# Agent Browser Capabilities - ROI Analyst

## 🚀 Browser Automation Enabled
**Integration Date:** {datetime.now().isoformat()}
**Status:** ✅ ACTIVE

## 📊 Financial Analysis Browser Use Cases

### 1. Company Financials Research
```python
from agent_browser_wrapper import AgentBrowser

# Research company financials
browser = AgentBrowser(session="financial-research")
browser.open("https://www.sec.gov/edgar/searchedgar/companysearch.html")
browser.fill("@e1", "AAPL")  # Company search
# Extract 10-K, 10-Q, 8-K filings
```

### 2. Market Research & Competitor Analysis
```python
# Analyze competitors
competitors = ["MSFT", "GOOGL", "AMZN"]
for symbol in competitors:
    browser.open(f"https://finance.yahoo.com/quote/{symbol}")
    snapshot = browser.snapshot()
    # Extract financial metrics, ratios
```

### 3. Economic Indicators
```python
# Access economic data
browser.open("https://fred.stlouisfed.org")
browser.search_workflow("https://fred.stlouisfed.org", "GDP")
# Extract economic time series data
```

### 4. Industry Reports
```python
# Access industry research
browser.open("https://www.ibisworld.com")
# Extract industry growth rates, trends
```

### 5. Investment Research Platforms
```python
# Access professional research
browser.open("https://www.bloomberg.com/markets")
# Extract analyst reports, ratings
```

## 🔧 Installation & Setup

### Prerequisites:
```bash
# Install Agent Browser globally
npm install -g agent-browser

# Download Chromium (first time)
agent-browser install
```

### Python Wrapper:
```python
# The wrapper is available at:
# /Users/cubiczan/.openclaw/workspace/agent_browser_wrapper.py

# Import in your analysis scripts:
from agent_browser_wrapper import AgentBrowser, BrowserSnapshot
```

## 🎯 Example: Financial Statement Analysis

```python
import json
from datetime import datetime
from agent_browser_wrapper import AgentBrowser

class FinancialBrowser:
    def __init__(self):
        self.browser = AgentBrowser(
            session="financial-analysis",
            verbose=True
        )
    
    def get_company_filings(self, symbol: str, filing_type: str = "10-K"):
        """Get SEC filings for company"""
        
        # Navigate to SEC EDGAR
        if not self.browser.open("https://www.sec.gov/edgar/searchedgar/companysearch.html"):
            return None
        
        # Search for company
        if not self.browser.find_and_fill("textbox", symbol):
            return None
        
        # Click search
        if not self.browser.find_and_click("button", "Search"):
            return None
        
        # Wait for results
        self.browser.wait(timeout=10000)
        
        # Get snapshot
        snapshot = self.browser.snapshot()
        if not snapshot:
            return None
        
        # Extract filings
        filings = []
        for element in snapshot.elements:
            if element.role == "link" and filing_type in element.name:
                filings.append({
                    "type": filing_type,
                    "date": extract_date(element.name),
                    "url": element.attributes.get("href", ""),
                    "symbol": symbol
                })
        
        return filings
    
    def analyze_financial_ratios(self, symbol: str):
        """Analyze financial ratios from multiple sources"""
        
        ratios = {}
        
        # Source 1: Yahoo Finance Key Statistics
        if self.browser.open(f"https://finance.yahoo.com/quote/{symbol}/key-statistics"):
            snapshot = self.browser.snapshot()
            if snapshot:
                ratios["yahoo"] = extract_yahoo_ratios(snapshot)
        
        # Source 2: MarketWatch Financials
        if self.browser.open(f"https://www.marketwatch.com/investing/stock/{symbol}/financials"):
            snapshot = self.browser.snapshot()
            if snapshot:
                ratios["marketwatch"] = extract_marketwatch_ratios(snapshot)
