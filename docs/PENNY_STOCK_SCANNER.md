# Penny Stock Scanner Cron Job

**Purpose:** Daily penny stock recommendations for Tasty Trade execution

---

## Job Configuration

**Schedule:** Daily at 8:30 AM EST (before market open)
**Agent:** trade-recommender (specialized for trading)
**Model:** GLM-5 (needs large context for analysis)
**Output:** Discord alerts with actionable recommendations

---

## Workflow

### **1. Pre-market Scan (8:30 AM)**
- Screen 50+ active penny stocks
- Apply technical/fundamental filters
- Identify top 3-5 opportunities
- Generate trade setups

### **2. Alert Format**
```
🎯 PENNY STOCK ALERT - [DATE]

**Stock:** [TICKER] - [COMPANY]
**Price:** $[PRICE] ([CHANGE]%)
**Setup:** [PATTERN/BREAKOUT/BOUNCE]

**Target:** $[TARGET] ([%] upside)
**Stop:** $[STOP] ([%] risk)
**R/R:** 1:[RISK_REWARD]

**Entry:** Market/limit @ $[PRICE]
**Timeframe:** 1-5 days
**Risk Level:** High (penny stock)

**Chart:** [LINK]
**News:** [LINK]
```

### **3. Tasty Trade Execution**
- **Order Type:** Market or limit
- **Position Size:** 2% of portfolio max
- **Stop Loss:** Hard stop @ $[STOP]
- **Take Profit:** Scale out @ targets

---

## Penny Stock Criteria

### **Price:** $0.10 - $5.00
### **Volume:** >500K shares daily
### **Market Cap:** $50M - $500M
### **Technical:**
- RSI: 30-70 (avoid extremes)
- Volume spike: >150% of average
- Pattern: Breakout/bounce/trend
- ATR: >5% (swing potential)

### **Risk Management:**
- Max 15% stop loss
- Min 1:2 risk/reward
- Max 3 positions at once
- Sector diversification

---

## Data Sources

### **Primary:**
- Yahoo Finance (free API)
- Finviz screening
- TradingView charts

### **Alternative:**
- Social sentiment
- News volume
- Options flow

---

## Integration

### **With Trade Recommender:**
- Extends existing trading framework
- Specialized penny stock filters
- Higher risk parameters
- Real-time Discord alerts

### **With Tasty Trade:**
- Direct execution recommendations
- Position sizing guidance
- Risk management rules

---

## Success Metrics

### **Daily:**
- 3-5 actionable recommendations
- >60% win rate target
- 20-30% average return
- <15% max drawdown

### **Monthly:**
- 60-100 trade ideas
- 35-60 profitable trades
- 20-30% monthly return
- <10% monthly drawdown

---

## Files

**Skill:** `/Users/cubiczan/mac-bot/skills/penny-stock-scanner/SKILL.md`
**Script:** `/Users/cubiczan/.openclaw/workspace/scripts/penny-stock-scanner.py`
**Cron Job:** Configured via OpenClaw gateway

---

## Testing

**Manual Test:**
```bash
python3 /Users/cubiczan/.openclaw/workspace/scripts/penny-stock-scanner.py
```

**Expected Output:**
- Top 3-5 penny stock picks
- Detailed analysis for each
- Discord-style alert format
- JSON output file

---

**Version:** 1.0
**Status:** Ready for cron job creation
**Next:** Test script and create cron job
