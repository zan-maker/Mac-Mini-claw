# Twelve Data API Integration

**API Key:** `26b639a38e124248ba08958bcd72566f`
**Status:** ✅ **FULLY OPERATIONAL**
**Added:** 2026-02-20

---

## 📊 Capabilities

### Market Data
- ✅ **Real-time prices** - Stocks, ETFs, Forex, Crypto
- ✅ **Historical data** - Time series with multiple intervals
- ✅ **Market quotes** - Full quote data (OHLCV, volume, change)
- ✅ **Technical indicators** - RSI, MACD, SMA, EMA, etc.

### Coverage
- **Stocks:** 50+ countries, 1M+ instruments
- **Forex:** Major and minor pairs
- **Crypto:** Top cryptocurrencies
- **ETFs:** Global ETF coverage
- **Indices:** Major world indices

---

## 🔧 Integration File

**Python Client:** `skills/trade-recommender/twelve_data_client.py`

**Usage:**
```python
from twelve_data_client import TwelveDataClient

client = TwelveDataClient()

# Get real-time price
price = client.get_price("AAPL")

# Get full quote
quote = client.get_quote("SPY")

# Get historical data
history = client.get_time_series("SPY", "1day", 30)

# Get technical indicators
rsi = client.get_technical_indicators("SPY", "1day", "rsi", period=14)
```

---

## 📡 Available Endpoints

### Core Endpoints
| Endpoint | Description | Status |
|----------|-------------|--------|
| `/price` | Latest price | ✅ Working |
| `/quote` | Full quote data | ✅ Working |
| `/time_series` | Historical OHLCV | ✅ Working |
| `/indicators` | Technical analysis | ✅ Available |

### Data Types
| Type | Available | Examples |
|------|-----------|----------|
| **Stocks** | ✅ | AAPL, MSFT, NVDA |
| **ETFs** | ✅ | SPY, QQQ, IWM |
| **Forex** | ✅ | EUR/USD, GBP/USD |
| **Crypto** | ✅ | BTC/USD, ETH/USD |
| **Indices** | ✅ | SPX, NDX, DJI |

---

## ⏰ Intervals Supported

**Intraday:**
- 1min, 5min, 15min, 30min, 45min
- 1h, 2h, 4h, 8h

**Daily+:**
- 1day, 1week, 1month

---

## 🎯 Use Cases for Trade Recommender

### 1. Real-time Price Feeds
- Get current prices for any symbol
- Replace or supplement Public.com quotes
- Faster, more reliable data

### 2. Technical Analysis
- Calculate RSI, MACD, moving averages
- Identify support/resistance levels
- Generate entry/exit signals

### 3. Historical Backtesting
- Fetch historical data for backtesting
- Validate trading strategies
- Analyze past performance

### 4. Market Scanning
- Scan multiple symbols quickly
- Find opportunities across sectors
- Track market movers

---

## 🔄 Integration Points

### Daily Trade Recommendations
**Current Flow:**
1. Public.com → Stock quotes
2. Kalshi → Event markets
3. The Odds API → Sportsbook odds

**Enhanced Flow:**
1. **Twelve Data** → Real-time quotes
2. **Twelve Data** → Technical indicators
3. Kalshi → Event markets
4. The Odds API → Sportsbook odds

---

## 📊 Example Data

### Real-time Quote
```json
{
  "symbol": "SPY",
  "name": "SPDR S&P 500 ETF Trust",
  "exchange": "NYSE",
  "close": "685.88",
  "change": "1.40",
  "percent_change": "0.20453769",
  "volume": 1185306
}
```

### Time Series
```json
[
  {
    "datetime": "2026-02-20",
    "open": "682.23",
    "high": "689.32",
    "low": "681.81",
    "close": "685.88",
    "volume": "1185306"
  }
]
```

---

## 🚦 Rate Limits

**Free Tier:**
- 800 API credits per day
- 8 calls per minute
- Real-time data (15-min delay for some endpoints)

**Note:** Monitor usage to avoid hitting limits

---

## 📈 Comparison with Other Data Sources

| Feature | Twelve Data | Public.com | Alpaca |
|---------|-------------|------------|--------|
| **Real-time** | ✅ | ✅ | ✅ |
| **Historical** | ✅ | ❌ | ✅ |
| **Technical Indicators** | ✅ | ❌ | ❌ |
| **Forex** | ✅ | ❌ | ❌ |
| **Crypto** | ✅ | ❌ | ❌ |
| **Options Chains** | ❌ | ❌ | ✅ |

---

## 🔗 Quick Links

**Twelve Data Portal:**
- Dashboard: https://twelvedata.com/account
- API Keys: https://twelvedata.com/account/api-keys
- Documentation: https://twelvedata.com/docs
- Pricing: https://twelvedata.com/pricing

**Python SDK:**
- GitHub: https://github.com/twelvedata/twelvedata-python
- Install: `pip install twelvedata`

---

## 💡 Best Practices

1. **Cache responses** - Reduce API calls
2. **Handle errors gracefully** - Implement retry logic
3. **Monitor rate limits** - Track daily usage
4. **Use appropriate intervals** - Don't request 1min data for swing trading
5. **Validate data** - Check for null values

---

## 🎯 Next Steps

1. ✅ Integration file created
2. ✅ API tested and working
3. ⏳ Integrate with daily trade recommendations
4. ⏳ Add technical indicators to analysis
5. ⏳ Enable backtesting capabilities

---

**Version:** 1.0
**Status:** ✅ Operational
**Integration Point:** Trade Recommender skill
**Purpose:** Real-time market data, technical analysis, backtesting
