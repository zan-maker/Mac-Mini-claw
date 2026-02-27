---
name: trade-recommender
description: "AI-powered trade recommendations using defeatbeta-api for financial data, Alpha Vantage for technical indicators, and NewsAPI for market sentiment. Use for: (1) stock analysis and recommendations, (2) technical + fundamental analysis, (3) entry/exit signals, (4) portfolio screening, (5) news sentiment analysis."
---

# Trade Recommender

Comprehensive trade recommendation system combining fundamental analysis from defeatbeta-api, technical indicators from Alpha Vantage, and news sentiment from NewsAPI.

## Data Sources

### defeatbeta-api (Fundamental Data)
- Company profiles, financials, valuation metrics
- DCF modeling, earnings transcripts
- Industry benchmarking
- 60+ financial data endpoints
- **Location:** `/Users/cubiczan/.openclaw/workspace/defeatbeta-api/`
- **Python:** `.venv/bin/python`

### Alpha Vantage (Technical Data)
- **API Key:** `T0Z2YW467F7PNA9Z`
- Real-time and historical prices
- Technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands, etc.)
- Rate limit: 1 request/second, 25 requests/day (free tier)

### NewsAPI (Financial News & Sentiment)
- **API Key:** `fe52ac365edf464c9dca774544a40da3`
- **Base URL:** `https://newsapi.org/v2/`
- Real-time financial news
- Company-specific news search
- Market sentiment analysis
- Rate limit: 100 requests/day (free tier)

### Alpaca API (Paper Trading)
- **Endpoint:** `https://paper-api.alpaca.markets/v2`
- **API Key:** `PKNDK5P66FCRH5P5ILPTVCYE7D`
- **Secret Key:** `z1fwAHFV9H8NY26XrZ2sSSxJggc8BwqiU2gPxVsy49V`
- **Mode:** Paper trading (no real money)
- Account info, orders, positions, portfolio
- Real-time market data
- Rate limit: 200 requests/minute

## API Endpoints

### Alpha Vantage Base URL
```
https://www.alphavantage.co/query
```

### Available Alpha Vantage Functions

#### Price Data
- `TIME_SERIES_DAILY` - Daily OHLCV data
- `TIME_SERIES_INTRADAY` - Intraday data (1min, 5min, 15min, 30min, 60min)
- `GLOBAL_QUOTE` - Real-time quote

#### Technical Indicators
- `SMA` - Simple Moving Average
- `EMA` - Exponential Moving Average
- `RSI` - Relative Strength Index
- `MACD` - Moving Average Convergence Divergence
- `BBANDS` - Bollinger Bands
- `STOCH` - Stochastic Oscillator
- `ADX` - Average Directional Index
- `CCI` - Commodity Channel Index
- `ATR` - Average True Range
- `OBV` - On-Balance Volume

#### Fundamental Data
- `OVERVIEW` - Company overview
- `EARNINGS` - Earnings data
- `INCOME_STATEMENT` - Income statement
- `BALANCE_SHEET` - Balance sheet
- `CASH_FLOW` - Cash flow statement

## Trade Recommendation Workflow

### 1. Fundamental Analysis (defeatbeta-api)
```python
from defeatbeta_api.data.ticker import Ticker

ticker = Ticker('AAPL')

# Get company profile
profile = ticker.profile()

# Get valuation metrics
pe_ratio = ticker.pe_ratio()
pb_ratio = ticker.pb_ratio()

# Get financial statements
income = ticker.quarterly_income_statement()
balance = ticker.quarterly_balance_sheet()
cashflow = ticker.quarterly_cashflow()

# Get DCF valuation
dcf = ticker.dcf()
```

### 2. Technical Analysis (Alpha Vantage)
```bash
# Get RSI
curl "https://www.alphavantage.co/query?function=RSI&symbol=AAPL&interval=daily&time_period=14&apikey=T0Z2YW467F7PNA9Z"

# Get MACD
curl "https://www.alphavantage.co/query?function=MACD&symbol=AAPL&interval=daily&apikey=T0Z2YW467F7PNA9Z"

# Get SMA 50 and 200
curl "https://www.alphavantage.co/query?function=SMA&symbol=AAPL&interval=daily&time_period=50&apikey=T0Z2YW467F7PNA9Z"
curl "https://www.alphavantage.co/query?function=SMA&symbol=AAPL&interval=daily&time_period=200&apikey=T0Z2YW467F7PNA9Z"
```

### 3. News Sentiment (NewsAPI)
```bash
# Get company news
curl "https://newsapi.org/v2/everything?q=AAPL&sortBy=publishedAt&apiKey=fe52ac365edf464c9dca774544a40da3"

# Get top business headlines
curl "https://newsapi.org/v2/top-headlines?category=business&country=us&apiKey=fe52ac365edf464c9dca774544a40da3"
```

### 4. News Sentiment (NewsAPI)
```bash
# Get company news
curl "https://newsapi.org/v2/everything?q=AAPL&sortBy=publishedAt&apiKey=fe52ac365edf464c9dca774544a40da3"

# Get top business headlines
curl "https://newsapi.org/v2/top-headlines?category=business&country=us&apiKey=fe52ac365edf464c9dca774544a40da3"
```

### 5. Paper Trading (Alpaca API)
```python
# Using scripts/alpaca-trading.py
from alpaca-trading import get_account, place_order, execute_recommendation

# Get account info
account = get_account()

# Execute trade based on recommendation
result = execute_recommendation(
    recommendation="BUY",
    symbol="AAPL",
    confidence=75,
    current_price=261.73
)
```

### 6. Generate Recommendation

#### Scoring System

**Fundamental Score (0-100)**
- P/E vs Industry (0-20)
- Revenue Growth (0-20)
- Profit Margins (0-20)
- ROE/ROIC (0-20)
- DCF Fair Value vs Price (0-20)

**Technical Score (0-100)**
- RSI (0-20): Oversold = bullish, Overbought = bearish
- MACD (0-20): Bullish crossover = positive
- Price vs SMA50/SMA200 (0-20): Golden cross = bullish
- Volume trends (0-20)
- Bollinger Band position (0-20)

**Sentiment Score (0-100)**
- News sentiment analysis (0-50)
- Recent news volume (0-25)
- Market events impact (0-25)

**Combined Score = (Fundamental × 0.4) + (Technical × 0.3) + (Sentiment × 0.3)**

#### Recommendation Thresholds
- **Strong Buy**: Combined Score ≥ 80
- **Buy**: Combined Score 60-79
- **Hold**: Combined Score 40-59
- **Sell**: Combined Score 20-39
- **Strong Sell**: Combined Score < 20

## Usage Examples

### Quick Analysis
```
Analyze AAPL and give me a trade recommendation
```

### Portfolio Screening
```
Screen these stocks for buy signals: AAPL, MSFT, GOOGL, NVDA
```

### Technical Check
```
What's the RSI and MACD for TSLA?
```

### Fundamental Check
```
Compare NVDA's P/E and growth to industry average
```

## MCP Integration

To use defeatbeta-api via MCP, add to your MCP config:

```json
{
  "mcpServers": {
    "defeatbeta-api": {
      "command": "uvx",
      "args": [
        "--refresh",
        "git+https://github.com/defeat-beta/defeatbeta-api.git#subdirectory=mcp"
      ]
    }
  }
}
```

## Paper Trading

The trade recommender can execute trades on Alpaca's paper trading platform:

**Account:** $200,000 buying power (paper money)
**Script:** `/workspace/scripts/alpaca-trading.py`

### Available Functions
- `get_account()` - Account info and buying power
- `get_positions()` - Current open positions
- `get_orders(status)` - Open/closed orders
- `place_order(symbol, qty, side)` - Execute market order
- `place_limit_order(symbol, qty, side, price)` - Execute limit order
- `execute_recommendation(rec, symbol, conf, price)` - Auto-execute based on recommendation

### Execution Rules
- **STRONG_BUY/BUY:** Buy up to 10% of portfolio per trade
- **SELL/STRONG_SELL:** Sell entire position if held
- **HOLD:** No action
- Position size scales with confidence score

## Rate Limits

- **Alpha Vantage**: 5 calls/minute, 25 calls/day (free tier)
- **defeatbeta-api**: No rate limits (uses cached Hugging Face data)
- **NewsAPI**: 100 requests/day (free tier)
- **Alpaca API**: 200 requests/minute

## Notes

- Alpha Vantage free tier has rate limits - cache results when possible
- defeatbeta-api data is updated daily from Hugging Face
- Always check the data update date with `get_latest_data_update_date`
- For intraday trading, use Alpha Vantage intraday endpoints
