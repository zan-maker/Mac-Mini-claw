#!/bin/bash
# Penny Stock Scanner - OpenClaw Gateway Integration
# Spawns trade-recommender agent for penny stock analysis

GATEWAY_URL="http://localhost:18789"
GATEWAY_TOKEN="mac-local-gateway-secret-2026"
AGENT_ID="trade-recommender"
CHANNEL_ID="1471852327978795091"  # Discord #general

# Create task file
TASK_FILE="/Users/cubiczan/.openclaw/workspace/tasks/penny-stock-$(date +%Y%m%d).txt"
mkdir -p "$(dirname "$TASK_FILE")"

cat > "$TASK_FILE" << 'TASK_EOF'
Analyze penny stocks ($0.10-$5.00) for today's trading opportunities on Tasty Trade.

**SCREENING CRITERIA:**
- Price: $0.10 - $5.00
- Volume: >500,000 shares daily
- Market Cap: $50M - $500M
- RSI (14): 30-70 (avoid extremes)
- Volume spike: >150% of 20-day average
- Float: < 50M shares (squeeze potential)
- Short Interest: > 10% (optional catalyst)

**PATTERNS TO IDENTIFY:**
1. Breakouts above key resistance
2. Oversold bounces (RSI < 30 recovering)
3. Momentum continuations (3+ green days)
4. News catalysts (FDA approvals, contracts, earnings)
5. Technical patterns (cup & handle, bull flags)

**FOR EACH STOCK (TOP 3-5):**
- Ticker and company name
- Current price and daily change
- Volume vs average
- Technical setup (pattern, RSI, key levels)
- News catalyst (if any)
- Entry price and strategy
- Target price (20-30% upside)
- Stop loss (10-15% risk)
- Risk/Reward ratio (minimum 1:2)

**TASTY TRADE EXECUTION:**
- Position size: 2% of portfolio maximum
- Order type: Market or limit based on volatility
- Stop loss: Hard stop immediately after entry
- Take profit: Scale out (50% at target 1, 50% at target 2)
- Timeframe: 1-5 day swing trades

**DISCORD ALERT FORMAT (use exactly):**
```
🎯 PENNY STOCK ALERT - [TICKER]

**Stock:** [TICKER] - [COMPANY NAME]
**Price:** $[PRICE] ([CHANGE]% today)
**Volume:** [VOLUME] shares ([%] of average)

**Setup:** [PATTERN: BREAKOUT/BOUNCE/MOMENTUM]
**Catalyst:** [NEWS/EVENT OR "Technical only"]

**Target:** $[TARGET] ([%] upside)
**Stop:** $[STOP] ([%] risk)
**R/R:** 1:[RISK_REWARD]

**Entry:** [MARKET/LIMIT] @ $[PRICE]
**Timeframe:** 1-5 days
**Risk Level:** High (penny stock)

**Chart:** [BRIEF CHART ANALYSIS]
```

**DATA SOURCES TO USE:**
- Yahoo Finance for real-time prices/volume
- Finviz for screening and fundamentals
- TradingView for chart patterns
- News APIs for catalysts
- Social sentiment (StockTwits/Twitter)

Provide 3-5 actionable penny stock recommendations ready for immediate execution on Tasty Trade. Focus on stocks with clear technical setups and catalysts.
TASK_EOF

echo "=========================================="
echo "PENNY STOCK SCANNER - $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo
echo "Gateway: $GATEWAY_URL"
echo "Agent: $AGENT_ID"
echo "Task file: $TASK_FILE"
echo

# Check if gateway is running
if ! curl -s "$GATEWAY_URL/status" > /dev/null 2>&1; then
    echo "❌ Gateway not running at $GATEWAY_URL"
    echo "Starting gateway..."
    openclaw gateway start > /dev/null 2>&1
    sleep 5
fi

echo "✅ Task saved to: $TASK_FILE"
echo
echo "To execute manually via OpenClaw API:"
echo "curl -X POST \\"
echo "  -H \"Authorization: Bearer $GATEWAY_TOKEN\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"agentId\":\"$AGENT_ID\",\"task\":\"$(cat "$TASK_FILE" | jq -Rs .)\"}' \\"
echo "  $GATEWAY_URL/api/v1/sessions/spawn"
echo
echo "Or use sessions_spawn tool from main agent."
echo
echo "Sample alert would be sent to Discord channel: $CHANNEL_ID"
echo
echo "=========================================="
echo "SETUP COMPLETE"
echo "=========================================="
echo
echo "System cron job runs: 8:30 AM EST Mon-Fri"
echo "Script: /Users/cubiczan/.openclaw/workspace/scripts/penny-stock-cron.sh"
echo "Logs: /Users/cubiczan/.openclaw/workspace/logs/penny-cron.log"
echo
echo "Next: Test with manual execution"
