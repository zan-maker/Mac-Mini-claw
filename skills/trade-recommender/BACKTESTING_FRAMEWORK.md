# Backtesting Framework

**Purpose:** Test trading strategies against historical data using Twelve Data API

---

## Overview

The backtesting framework allows you to:

1. **Test strategies** against historical price data
2. **Calculate technical indicators** (RSI, SMA, MACD, Bollinger Bands)
3. **Simulate option trades** with realistic P&L
4. **Generate performance metrics** (win rate, profit factor, ROI)

---

## Quick Start

```bash
cd ~/.openclaw/workspace/skills/trade-recommender
python3 backtesting_framework.py
```

---

## Strategies Available

### 1. RSI Reversal
**Logic:**
- Buy calls when RSI < 30 (oversold)
- Buy puts when RSI > 70 (overbought)
- Hold 5 days

**Best for:** Mean-reverting markets

---

### 2. Trend Following
**Logic:**
- Buy calls when technical score >= 50
- Buy puts when technical score <= -50
- Hold 5 days

**Best for:** Trending markets

---

## API Integration

### Data Source: Twelve Data
```python
from twelve_data_client import TwelveDataClient

client = TwelveDataClient()

# Get historical data
data = client.get_time_series("SPY", "1day", 252)

# Get technical indicators
rsi = client.get_technical_indicators("SPY", "1day", "rsi", period=14)
sma = client.get_technical_indicators("SPY", "1day", "sma", period=50)
```

---

## Technical Indicators

### RSI (Relative Strength Index)
```python
rsi = engine.calculate_rsi(prices, period=14)
```

### SMA (Simple Moving Average)
```python
sma_50 = engine.calculate_sma(prices, 50)
sma_200 = engine.calculate_sma(prices, 200)
```

### MACD
```python
macd, signal, histogram = engine.calculate_macd(prices)
```

---

## Signal Generation

The framework generates signals based on:

| Indicator | Weight | Bullish Signal |
|-----------|--------|----------------|
| RSI | 25 pts | RSI < 30 (oversold) |
| SMA Trend | 25 pts | Price > SMA50 > SMA200 |
| MACD | 25 pts | Histogram positive |
| Price Position | 25 pts | Near lower Bollinger Band |

**Total Score: 0-100**

- **75-100:** Strong signal, increase position
- **50-74:** Moderate signal, standard position
- **25-49:** Weak signal, reduce position
- **0-24:** Conflicting signals, avoid trade

---

## Performance Metrics

| Metric | Description |
|--------|-------------|
| **Total Return** | Overall portfolio return % |
| **Win Rate** | Percentage of winning trades |
| **Profit Factor** | Avg Win / Avg Loss |
| **Average Win** | Mean profit on winning trades |
| **Average Loss** | Mean loss on losing trades |

---

## Example Output

```
============================================================
BACKTEST: SPY | Strategy: rsi_reversal
============================================================

Initial Capital: $10,000.00
Final Capital: $11,234.56
Total Return: 12.35%

Total Trades: 45
Win Rate: 62.2%
Average Win: $156.78
Average Loss: $89.23
Profit Factor: 1.76

============================================================
```

---

## Custom Strategies

Create your own strategy:

```python
class MyStrategy:
    def __init__(self, engine):
        self.engine = engine
    
    def generate_signal(self, prices):
        # Your logic here
        signals = self.engine.generate_signals(prices)
        
        # Custom entry logic
        if signals['rsi'] < 35 and signals['trend'] == 'bullish':
            return 'buy_call'
        elif signals['rsi'] > 65 and signals['trend'] == 'bearish':
            return 'buy_put'
        else:
            return 'hold'
```

---

## Configuration

### Position Sizing
```python
engine.run_backtest(
    symbol="SPY",
    strategy="rsi_reversal",
    days=252,
    position_size=0.02  # 2% of capital per trade
)
```

### Initial Capital
```python
engine = BacktestEngine(initial_capital=10000)
```

---

## Output Files

**Location:** `~/.openclaw/workspace/trades/`

**Format:** `backtest-results-YYYYMMDD-HHMMSS.json`

**Contents:**
- All trades executed
- Equity curve
- Performance metrics
- Signal history

---

## Integration with Daily Recommendations

The backtesting framework integrates with the daily trade recommendations:

1. **Technical analysis** from Twelve Data
2. **Signal generation** using same indicators
3. **Position sizing** based on backtested performance
4. **Risk management** informed by historical win rates

---

## Future Enhancements

- [ ] Add more strategies (momentum, breakout, mean reversion)
- [ ] Support for multi-leg strategies (spreads, iron condors)
- [ ] Greeks-based entry/exit rules
- [ ] Monte Carlo simulation
- [ ] Walk-forward optimization
- [ ] Real-time paper trading mode

---

**Version:** 1.0
**Status:** ✅ Operational
**API:** Twelve Data (26b639a38e124248ba08958bcd72566f)
