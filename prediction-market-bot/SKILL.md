---
name: prediction-market-bot
description: Advanced prediction market trading with Kelly Criterion, risk metrics, and automated analysis. Use when: "analyze trade", "calculate position", "check risk", "prediction market", "kelly sizing".
metadata:
  version: 1.0.0
  pattern: context-aware
  tags: [prediction-market, kelly, risk, trading, kalshi]
---

# Prediction Market Bot Skill

## When to Use This Skill

Use this skill when you need to:
- Analyze prediction market opportunities (Kalshi, etc.)
- Calculate optimal position sizes using Kelly Criterion
- Validate trades against risk rules
- Track performance metrics (Sharpe, VaR, Max Drawdown)
- Execute mathematically-sound trading strategies

## Core Formulas Implemented

### Edge Detection
- **Expected Value**: `EV = p · b − (1 − p)`
- **Market Edge**: `edge = p_model − p_mkt` (trade when > 0.04)
- **Mispricing Score**: `δ = (p_model − p_mkt) / σ`

### Position Sizing
- **Kelly Criterion**: `f* = (p · b − q) / b`
- **Fractional Kelly**: `f = α · f*` (α = 0.25–0.5)
- **Bankroll Management**: Position ≤ f × Bankroll

### Risk Metrics
- **Value at Risk (95%)**: `VaR = μ − 1.645 · σ`
- **Max Drawdown**: `MDD = (Peak − Trough) / Peak` (block if > 8%)
- **Sharpe Ratio**: `SR = (E[R] − Rf) / σ(R)` (target > 2.0)

## Critical Pre-Execution Rules

Before any trade execution, ALL rules must pass:

1. **Minimum Edge**: `edge > 0.04` (4% edge required)
2. **Positive EV**: `EV > 0` (positive expected value)
3. **Kelly Compliance**: `position ≤ kelly_fraction × bankroll`
4. **Exposure Limit**: `current_exposure + new_position ≤ 10%`
5. **Minimum Confidence**: `p_model > 0.55` (55% minimum)

## Usage Examples

### 1. Analyze a Trade Opportunity
```bash
cd /Users/cubiczan/.openclaw/workspace
python3 scripts/prediction-market-bot.py --analyze --market "WTI >$98" --p_model 0.95 --p_market 0.75
```

### 2. Calculate Position Size
```bash
python3 scripts/kelly-calculator.py --bankroll 1000 --p_model 0.75 --p_market 0.50 --multiplier 2.0
```

### 3. Validate Trade Against Rules
```bash
python3 scripts/validate-trade.py --p_model 0.80 --p_market 0.60 --current_exposure 0.05
```

### 4. Track Performance
```bash
python3 scripts/performance-tracker.py --days 90 --calculate-sharpe --calculate-var
```

## Integration with Existing Systems

### Works With:
1. **War Crude Monitor** - For crude/gasoline opportunities
2. **Kalshi Profit Scanner** - For general prediction markets
3. **Gas Trading Monitor** - For existing position management
4. **Cron Job System** - For automated scanning

### Data Flow:
1. **Scanner** detects opportunity → passes to **Prediction Bot**
2. **Prediction Bot** analyzes → calculates position size
3. **Risk Validator** checks rules → approves or rejects
4. **If approved** → Execute trade on Kalshi
5. **Performance Tracker** logs results → updates metrics

## Configuration

### Bankroll Settings
Default: $1000
- Can be adjusted in `.env`: `PREDICTION_BANKROLL=5000`
- Position sizes scale with bankroll

### Risk Parameters
- **Max Drawdown**: 8% (blocks new trades if exceeded)
- **VaR Confidence**: 95%
- **Minimum Edge**: 4%
- **Fractional Kelly Alpha**: 0.25 (conservative)

### Exposure Limits
- **Single Trade Max**: 5% of bankroll
- **Total Exposure Max**: 10% of bankroll
- **Daily Loss Limit**: 2% of bankroll

## Files Structure

```
prediction-market-bot/
├── SKILL.md                          # This file
├── scripts/
│   ├── prediction-market-bot.py      # Main analysis script
│   ├── kelly-calculator.py          # Position sizing
│   ├── validate-trade.py            # Risk validation
│   ├── performance-tracker.py       # Metrics tracking
│   └── trade-executor.py           # Auto-execution (future)
└── references/
    ├── formulas.md                  # Mathematical reference
    ├── risk-parameters.md          # Risk configuration
    └── performance-metrics.md      # Tracking metrics
```

## Performance Targets

Based on simulated backtesting:
- **Win Rate**: >65%
- **Sharpe Ratio**: >2.0
- **Max Drawdown**: <8%
- **Profit Factor**: >1.5
- **Annual Return**: >40%

## Safety Notes

1. **Never override risk rules** - The math is deterministic
2. **Start small** - Test with small bankroll first
3. **Monitor daily** - Check performance metrics regularly
4. **Adjust conservatively** - Use fractional Kelly (α=0.25)
5. **Keep logs** - All trades and analyses are logged

## Next Development Phases

### Phase 2 (Multi-Agent Research)
- Twitter/Reddit sentiment analysis
- News aggregation with NLP
- Bayesian probability updates
- Parallel sub-agent research

### Phase 3 (Full Automation)
- Kalshi API auto-trading
- Real-time performance dashboard
- Auto-hedging mechanisms
- Machine learning from past trades

---

*This skill implements mathematically-sound prediction market trading based on the framework from "Chapter 3 — Predict & Execute".*