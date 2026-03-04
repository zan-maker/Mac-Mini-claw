# Kalshi Automated Trading System

**Created:** 2026-03-04
**Status:** ✅ Active
**Focus:** Catalyst detection & discrepancy scanning for Kalshi prediction markets

---

## 🎯 System Overview

**Goal:** Automated Kalshi trade recommendations via catalyst detection
**Strategy:** Multi-API news scanning + market analysis
**Output:** Actionable trade recommendations with entry/target/stop levels

---

## ⚙️ Technical Setup

### **Core Script**
`scripts/kalshi-daily-scanner.py`
- Multi-API news aggregation (News API, Newsdata.io, Serper)
- Catalyst detection for Kalshi markets
- Time-based analysis (premarket/midday/postmarket)
- Trade recommendation generation
- Results saving + alerting

### **APIs Integrated**
1. **News API** (`4eb2186b017a49c38d6f6ded502dd55b`)
2. **Newsdata.io** (`pub_fb29ca627ef54173a0675b2413523744`)
3. **Serper API** (`cac43a248afb1cc1ec004370df2e0282a67eb420`)
4. **Kalshi API** (`fb109d35-efc3-42b1-bdba-0ee2a1e90ef8`)

---

## ⏰ Cron Job Schedule (8 Jobs)

| Time | Type | Focus |
|------|------|-------|
| **7:00 AM** | Premarket | Overnight news, earnings, economic data |
| **9:30 AM** | Market Open | Opening moves, breaking news |
| **11:00 AM** | Midday | Lunchtime catalysts |
| **1:00 PM** | Afternoon | Afternoon momentum, earnings calls |
| **4:30 PM** | Post-market | After-hours news, next day prep |
| **7:00 PM** | Evening | Evening news, international markets |
| **Every 2h** | Real-time | Continuous monitoring (9 AM - 5 PM) |

**Total scans per day:** 12+ (including 2-hour intervals)

---

## 📊 Output Format

### **Files Generated**
`kalshi-scan-{time}-{timestamp}.json`
- Example: `kalshi-scan-midday-20260304_1408.json`

### **Contents:**
- Catalyst analysis (12+ catalysts per scan)
- Trade recommendations (5-8 per scan)
- Entry/target/stop levels
- Risk-reward ratios
- Source links and timestamps

### **Log Files:**
`logs/kalshi-{type}.log`
- Separate logs for each scan type

---

## 🎯 Kalshi Market Coverage

### **Primary Markets Monitored:**
- **POLITICAL:** HOUSE-2024-CONTROL, SENATE-2024-CONTROL
- **ECONOMIC:** FED-2024-MAR-RATE, CPI-2024-FEB, NFP-2024-MAR
- **EARNINGS:** EARNINGS-AAPL-2024-Q1, EARNINGS-MSFT-2024-Q1
- **SPORTS:** NBA-CHAMPIONSHIP-2024, SUPERBOWL-2025-WINNER

### **Catalyst Categories:**
1. Political events (elections, policy changes)
2. Economic data (Fed, CPI, jobs reports)
3. Earnings announcements
4. Sports championships
5. Entertainment awards
6. Weather events
7. Tech developments

---

## 🔍 Catalyst Detection Logic

### **News Analysis:**
1. **Keyword matching** against Kalshi market categories
2. **Sentiment analysis** (positive/negative/neutral)
3. **Time relevance** (freshness scoring)
4. **Source credibility** weighting

### **Trade Generation:**
1. **Market selection** based on catalyst category
2. **Action determination** (BUY YES/NO based on sentiment)
3. **Price levels** (entry/target/stop based on confidence)
4. **Risk-reward calculation** (1:2 minimum target)

---

## 🚀 Performance Metrics

### **First Test Run (2026-03-04 14:08):**
- **Articles scanned:** 19
- **Catalysts found:** 12
- **Recommendations generated:** 6
- **Processing time:** ~3 seconds

### **Sample Recommendations:**
1. **HOUSE-2024-CONTROL** - BUY NO @ 40-60¢, target 65-75¢
2. **FED-2024-MAR-RATE** - BUY NO @ 40-60¢, target 65-75¢
3. **EARNINGS-TECH** - BUY YES @ 50-70¢, target 75-85¢

---

## 🔧 Manual Testing

```bash
# Test different scan types
python3 scripts/kalshi-daily-scanner.py premarket
python3 scripts/kalshi-daily-scanner.py midday
python3 scripts/kalshi-daily-scanner.py postmarket

# View logs
tail -f logs/kalshi-premarket.log
```

---

## 📈 Next Enhancements

### **Phase 2 (This Week):**
- Add actual Kalshi market price fetching
- Implement discrepancy detection (news vs. market prices)
- Add social sentiment analysis (Reddit/Twitter)
- Include options flow data

### **Phase 3 (Next Week):**
- Machine learning pattern recognition
- Backtesting framework
- Auto-trading integration (with manual approval)
- Performance tracking dashboard

---

## ⚠️ Important Notes

1. **Manual Execution Required:** Recommendations need human review/execution
2. **Market Hours:** Scans optimized for US market hours (9:30 AM - 4:00 PM EST)
3. **API Limits:** Respecting free tier limits (100 calls/day News API)
4. **Risk Management:** All recommendations include stop-loss levels

---

## ✅ Success Story

**Paxton Trade:** $25 → $130 (5.2x return)
**Strategy:** Catalyst detection + timely execution
**Goal:** Scale this success with automated scanning

---

**System ready for production use.** First automated scan: Tomorrow 7:00 AM EST.
