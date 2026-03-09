# Prediction Market Bot - Mathematical Formulas

## Core Formulas for Prediction Market Trading

### 1. Expected Value (EV)
**Formula:** `EV = p · b − (1 − p)`

**Where:**
- `p` = Model probability (our estimate)
- `b` = Decimal odds - 1
- `(1 - p)` = Probability of losing

**Example:**
- Model probability: 0.75 (75%)
- Market odds: 2.0x (market probability = 1/2.0 = 0.50)
- `b` = 2.0 - 1 = 1.0
- `EV` = 0.75 × 1.0 - (1 - 0.75) = 0.75 - 0.25 = 0.50

**Interpretation:** Positive EV means favorable bet.

### 2. Market Edge
**Formula:** `edge = p_model − p_market`

**Where:**
- `p_model` = Our model probability
- `p_market` = Market implied probability (1/decimal_odds)

**Threshold:** Trade only when `edge > 0.04` (4% edge)

**Example:**
- Model: 0.75, Market: 0.50
- Edge = 0.75 - 0.50 = 0.25 (25% edge) ✅

### 3. Kelly Criterion
**Formula:** `f* = (p · b − q) / b`

**Where:**
- `p` = Win probability
- `q` = Loss probability = 1 - p
- `b` = Decimal odds - 1

**Fractional Kelly:** `f = α · f*` (use α = 0.25–0.5 for reduced variance)

**Example:**
- p = 0.75, b = 1.0
- f* = (0.75 × 1.0 - 0.25) / 1.0 = 0.50
- Fractional (α=0.25): f = 0.25 × 0.50 = 0.125

**Position Size:** `position = f × bankroll`

### 4. Value at Risk (VaR)
**Formula:** `VaR = μ − z · σ`

**Where:**
- `μ` = Mean return
- `σ` = Standard deviation of returns
- `z` = Z-score for confidence level (1.645 for 95%)

**Interpretation:** Maximum expected loss over a given period at 95% confidence.

### 5. Sharpe Ratio
**Formula:** `SR = (E[R] − Rf) / σ(R)`

**Where:**
- `E[R]` = Expected return
- `Rf` = Risk-free rate
- `σ(R)` = Standard deviation of returns

**Annualized:** Multiply by √252 (trading days)

**Target:** SR > 2.0

### 6. Mispricing Score
**Formula:** `δ = (p_model − p_market) / σ`

**Where:**
- `σ` = Standard deviation of probability estimates

**Interpretation:** Z-score of model vs market divergence.

### 7. Brier Score (Calibration)
**Formula:** `BS = (1/n) · Σ(pᵢ − oᵢ)²`

**Where:**
- `pᵢ` = Predicted probability
- `oᵢ` = Actual outcome (1 for win, 0 for loss)

**Interpretation:** Lower score = better calibrated model.

### 8. Profit Factor
**Formula:** `PF = gross_profit / gross_loss`

**Target:** PF > 1.5

### 9. Max Drawdown
**Formula:** `MDD = (Peak − Trough) / Peak`

**Rule:** Block new trades if MDD > 8%

## Bayesian Updating

**Formula:** `P(H|E) = P(E|H) · P(H) / P(E)`

**Where:**
- `P(H|E)` = Updated probability after evidence
- `P(E|H)` = Probability of evidence given hypothesis
- `P(H)` = Prior probability
- `P(E)` = Probability of evidence

**Use:** Update model probabilities with new information.

## Arbitrage Detection

**Condition:** `Σ (1/oddsᵢ) < 1`

**Where:** Sum of reciprocal odds across all outcomes < 1 indicates arbitrage opportunity.

## Practical Implementation Notes

### 1. Probability Conversion
- **Decimal odds to probability:** `p = 1 / decimal_odds`
- **American odds to probability:** 
  - Positive: `p = 100 / (odds + 100)`
  - Negative: `p = |odds| / (|odds| + 100)`

### 2. Bankroll Management
- **Initial bankroll:** Start with risk capital only
- **Position sizing:** Never exceed Kelly fraction
- **Compounding:** Reinvest profits according to updated bankroll

### 3. Risk Limits
- **Single trade max:** 5% of bankroll
- **Total exposure:** 10% of bankroll
- **Daily loss limit:** 2% of bankroll
- **Weekly loss limit:** 5% of bankroll

### 4. Performance Tracking
Track these metrics daily:
1. Win rate
2. Average edge
3. Sharpe ratio
4. Max drawdown
5. Profit factor
6. Number of trades

## Python Implementation Examples

```python
import numpy as np
from scipy import stats

def calculate_ev(p_model, decimal_odds):
    b = decimal_odds - 1
    ev = p_model * b - (1 - p_model)
    return ev

def kelly_criterion(p_model, decimal_odds):
    b = decimal_odds - 1
    q = 1 - p_model
    f_star = (p_model * b - q) / b if b > 0 else 0
    return max(0, f_star)

def calculate_sharpe(returns, risk_free_rate=0.02):
    excess_returns = np.array(returns) - risk_free_rate/252
    sharpe = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
    return sharpe

def calculate_var(returns, confidence=0.95):
    mu = np.mean(returns)
    sigma = np.std(returns)
    z_score = stats.norm.ppf(1 - confidence)
    var = mu - z_score * sigma
    return var
```

## Common Pitfalls to Avoid

1. **Overestimating edge** - Be conservative with probability estimates
2. **Ignoring transaction costs** - Include fees in calculations
3. **Chasing losses** - Stick to the system, don't increase size after losses
4. **Underestimating variance** - Use fractional Kelly (α=0.25)
5. **Not tracking performance** - Log every trade for analysis

## Optimal Parameters (Based on Backtesting)

- **Minimum edge:** 4%
- **Fractional Kelly α:** 0.25 (conservative)
- **Max drawdown limit:** 8%
- **VaR confidence:** 95%
- **Minimum confidence:** 55%
- **Target Sharpe:** >2.0
- **Target win rate:** >65%

---

*These formulas form the mathematical foundation of the prediction market trading bot. All trading decisions should be based on these calculations.*