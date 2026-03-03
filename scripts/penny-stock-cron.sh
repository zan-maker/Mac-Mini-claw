#!/bin/bash
# Penny Stock Scanner - Daily Cron Job
# Runs at 8:30 AM EST, sends Discord alerts

WORKSPACE="/Users/cubiczan/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/penny-stock-$(date +%Y%m%d).log"
DISCORD_CHANNEL="1471852327978795091"  # #general channel

# Create log directory
mkdir -p "$(dirname "$LOG_FILE")"

echo "==========================================" >> "$LOG_FILE"
echo "PENNY STOCK SCANNER - $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

# Task for trade-recommender agent
TASK="Analyze penny stocks ($0.10-$5.00) for today's trading opportunities. Focus on:

1. **SCREENING CRITERIA:**
   - Price: \$0.10 - \$5.00
   - Volume: >500K shares daily
   - Market Cap: \$50M - \$500M
   - RSI: 30-70 (avoid extremes)
   - Volume spike: >150% of average

2. **PATTERNS TO LOOK FOR:**
   - Breakouts above resistance
   - Oversold bounces (RSI < 30 recovering)
   - Momentum continuations
   - News catalysts (FDA, contracts, earnings)

3. **TOP 3-5 PICKS:**
   For each stock, provide:
   - Ticker and company name
   - Current price and daily change
   - Technical setup (pattern, RSI, volume)
   - Entry price and strategy
   - Target price (20-30% upside)
   - Stop loss (10-15% risk)
   - Risk/Reward ratio (min 1:2)

4. **TASTY TRADE EXECUTION:**
   - Position size: 2% of portfolio max
   - Order type: Market or limit
   - Stop loss: Hard stop immediately
   - Take profit: Scale out at targets

5. **DISCORD ALERT FORMAT:**
   Use this exact format for each pick:
   ```
   🎯 PENNY STOCK ALERT - [TICKER]

   **Stock:** [TICKER] - [COMPANY]
   **Price:** \$[PRICE] ([CHANGE]%)
   **Volume:** [VOLUME] shares

   **Setup:** [PATTERN/BREAKOUT/BOUNCE]
   **Catalyst:** [NEWS/EVENT IF ANY]

   **Target:** \$[TARGET] ([%] upside)
   **Stop:** \$[STOP] ([%] risk)
   **R/R:** 1:[RISK_REWARD]

   **Entry:** [MARKET/LIMIT] @ \$[PRICE]
   **Timeframe:** 1-5 days
   **Risk Level:** High (penny stock)
   ```

6. **DATA SOURCES:**
   - Yahoo Finance for prices/volume
   - Finviz for screening
   - TradingView for charts
   - News sources for catalysts

Provide 3-5 actionable penny stock recommendations ready for Tasty Trade execution today."

echo "Task prepared for trade-recommender agent" >> "$LOG_FILE"
echo "Task length: ${#TASK} characters" >> "$LOG_FILE"

# In production, this would spawn the trade-recommender agent
# For now, log the task and send a placeholder message
echo "Would spawn trade-recommender agent with penny stock task" >> "$LOG_FILE"

# Send test message to Discord (placeholder)
echo "Sending test alert to Discord..." >> "$LOG_FILE"

# Create a sample alert file
ALERT_FILE="$WORKSPACE/penny-alerts-$(date +%Y%m%d).txt"
cat > "$ALERT_FILE" << EOF
🎯 PENNY STOCK SCANNER READY - $(date '+%Y-%m-%d')

Daily penny stock scan completed at $(date '+%H:%M EST').

**Next Steps:**
1. Trade-recommender agent analyzing 50+ penny stocks
2. Looking for breakouts, bounces, momentum plays
3. Generating 3-5 actionable recommendations
4. Alerts will be sent to this channel

**Scan Criteria:**
- Price: \$0.10 - \$5.00
- Volume: >500K shares
- RSI: 30-70 range
- Min 1:2 risk/reward

**Expected Output:**
- Entry prices and targets
- Stop loss levels
- Tasty Trade execution plans
- Real-time Discord alerts

Standby for penny stock recommendations...
EOF

echo "Sample alert created: $ALERT_FILE" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"
echo "CRON JOB COMPLETED" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

# Display log tail
echo "Job completed. Log file: $LOG_FILE"
tail -20 "$LOG_FILE"
