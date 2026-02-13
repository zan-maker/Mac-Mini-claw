# Bregman-Frank-Wolfe Market Maker Arbitrage

Advanced prediction market arbitrage strategy using Bregman projections and Frank-Wolfe optimization.

---

## Overview

The Kroer–Dudík "Frank‑Wolfe market maker" shows how to use Frank‑Wolfe as a Bregman projection to remove arbitrage in prediction markets: compute the Bregman projection of current prices onto the set of coherent distributions, and the divergence equals max arbitrage profit.

**Strategy:** "Run a light‑weight version client‑side and trade up to that bound."

---

## Mathematical Framework

### For a Single Market with Prices p∈R^n

**1. Normalize to the simplex:**
```
p_i = orderbook mid / sum
```

**2. Define feasible set M:**
All μ in the simplex consistent with no‑arb:
- For simple Polymarket markets: just the simplex
- For cross‑market constraints: add linear equalities/inequalities

**3. Bregman projection:**
```
μ* = argmin_{μ∈M} D(μ∥θ)
```
Where:
- D is KL divergence
- θ is current price vector

**4. Frank‑Wolfe:**
Use conditional gradient iterations over M to approximate μ*

**5. Trade:**
Move the market from θ towards μ* up to max position and slippage constraints
- **Guaranteed profit:** D(μ*∥θ) minus fees

---

## OpenClaw + PolyClaw Integration

### Environment Setup

**Required Environment Variables:**
- `CHAINSTACK_NODE` (Polygon RPC)
- `POLYCLAW_PRIVATE_KEY` (funded arb wallet)
- `OPENROUTER_API_KEY` (for LLM‑assisted monitoring)

### New Skill: bregman_fw_arb

**Components:**

**1. Markets Scan:**
Call existing market listing endpoints and cache:
- Outcome set
- Current bid/ask/mid for each YES/NO or multi‑outcome line

**2. Arbitrage Detection:**
For each market (and defined bundles for cross‑market constraints):
- Run Bregman/Frank‑Wolfe routine
- Return opportunities: `market_id, type, expected_profit, size, legs`

**3. Scheduling:**
Wire into OpenClaw's scheduler → runs every 30 seconds

---

## Algorithmic Details

### 3.1 Simple and Multi‑Outcome Arbitrage

**Simple Binary Arb:**
```
If best YES price + best NO price < 1 − fees − MIN_PROFIT_PCT:
    Buy both legs sized to MAX_POSITION_SIZE and orderbook depth
```

**Multi‑Outcome:**
```
If sum of "complete cover" < 1 − margin:
    It's arb
    Bregman projection refines optimal weights
```

**Unified Metric:**
```
Let p be normalized prices

If ∑p_i ≠ 1, or any constraint is violated:
    Compute mispricing score
    Use KL divergence D(μ*∥θ) from FW projection as unified arb metric

Only act when:
    D(μ*∥θ) ≥ MIN_PROFIT_PCT + fees + slippage buffer
```

### 3.2 Frank‑Wolfe Loop (Pseudocode)

```typescript
let current = initializeOnSimplex(marketPrices); // θ

for (let iter = 0; iter < MAX_ITERATIONS; iter++) {
  const gradient = computeGradient(current, marketPrices);   // ∇D(µ||θ)
  const vertex   = argminOverSimplex(gradient);              // e_k with smallest gradient
  const stepSize = 2 / (iter + 2);                           // standard FW schedule
  const previous = current;
  current = blend(current, vertex, stepSize);                // convex combo

  if (converged(current, previous)) break;
}

const muStar = current;
const divergence = klDivergence(muStar, marketPrices);
```

**Implementation Notes:**
- Gradient for KL D(μ∥θ) w.r.t. μ is `log(μ_i / θ_i) + 1`
- Keep numerics stable via small eps clamps
- `argminOverSimplex` = pick coordinate with lowest gradient (simplex vertex)
- Use standard step size; adaptive fully‑corrective FW is overkill at current scale

### 3.3 Execution Sizing and Guards

**Hard Constraints:**

| Parameter | Value | Description |
|-----------|-------|-------------|
| MIN_PROFIT_PCT | 0.5% | Minimum profit percentage |
| MIN_PROFIT_USDC | $0.50 | Minimum absolute profit |
| MAX_SLIPPAGE | 5% | Maximum acceptable slippage |
| MAX_POSITION_SIZE | 10% | Max position vs portfolio equity |

**Pre-Execution Checks:**
1. Build order plan using live orderbook (not mid) for each leg
2. Compute executed price vs theoretical arb price
3. Calculate expected P&L under worst‑case resolution
4. If both pct and absolute thresholds pass → proceed; else skip

---

## OpenClaw Orchestration

### Trading Engine Integration

**Strategy Module:**
```
strategy_id: "bregman_projection_arb"

Hooks:
  - on_scan_cycle(): Run detection, generate candidate trades
  - risk_check(order_bundle): Enforce position/PNL limits
  - execute(order_bundle): Call PolyClaw buy/sell helpers
```

### Dashboard and Alerts

**Vercel Dashboard (Next.js 14):**
- Markets scanned per cycle
- Divergence histogram (KL or other Bregman)
- Executed arb trades with realized vs theoretical P&L

**Telegram Alerts:**
- Each executed arb: market name, type, size, locked-in profit, current PnL
- Warning when failed leg occurs and hedge kicks in

---

## Execution Safeguards

**Beyond the basics** (earlier strategies lost ~38% on Reddit):

### 1. Orderbook Integrity Checks
- Ignore markets with clear spoofing
- Large best quotes but almost no depth behind top level
- Quotes that vanish repeatedly right before expected fill window

### 2. Latency & Execution Risk
- Measure time between taking leg A and placing leg B
- If latency or rejection rates spike → auto‑throttle or pause strategy

### 3. Protocol / Contract Risk Filter
- Maintain whitelist of Polymarket markets and categories
- Avoid obscure contracts with settlement/edge‑case ambiguity

### 4. Outcome‑Definition Sanity
- For cross‑market arbitrage, encode logical constraints with small DSL
- Test against historical data or known events before trusting in size

---

## Rollout Plan

### Phase 1: Paper Mode (Current)
- Run every 30s
- Store: divergence, theoretical arb P&L, "would‑be" fills based on book

### Phase 2: Dry‑Run with Tiny Capital
- 50–100 USDC
- Enable "max notional per day"
- "Max loss per day = 2–3% of bankroll"

### Phase 3: Parameter Tuning
- Adjust MIN_PROFIT_PCT, slippage, FW iteration count
- Based on realized slippage and failed‑leg frequency

### Phase 4: Scale Slowly
- Every time realized P&L over 1–2 weeks < theoretical P&L:
  - Diagnose: fees, slippage, liquidity, or logical/latency issues?

---

## Key Metrics to Track

| Metric | Target | Measurement |
|--------|--------|-------------|
| Win rate | >60% | Executed arbs |
| Theoretical vs Realized P&L | <5% gap | Per cycle |
| Failed leg rate | <2% | Per execution |
| Average divergence | >1.5% | Before entry |
| Max drawdown | <5% | Rolling 7-day |

---

## Implementation Next Steps

1. Draft `bregman_fw_arb.py` skeleton (Python pseudo‑code)
2. Wire to PolyClaw's existing CLI
3. Drop into repo and iterate
4. Run paper mode for 2 weeks minimum
5. Analyze divergence vs realized P&L gap
6. Gradually increase capital if metrics hold

---

**Version:** 1.0
**Integration:** PolyClaw + OpenClaw
**Frequency:** 30-second scan cycles
