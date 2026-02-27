# Tastytrade API Integration

**Status:** ⚠️ API Key Invalid/Expired
**Date Added:** 2026-02-20
**API Key:** `80e479d6235f546b188f9c86ec53bf80019c4bff`

---

## ⚠️ Issue Detected

The provided API key returned:
```
{"error":{"code":"token_invalid","message":"This token is invalid or has expired"}}
```

**Action Required:**
1. Log in to Tastytrade Developer Portal
2. Generate a new API key
3. Update the key in this integration

---

## Setup Instructions

### 1. Install SDK

```bash
pip3 install --user tastytrade-sdk
```

Or with venv:
```bash
python3 -m venv ~/.openclaw/workspace/skills/trade-recommender/venv
source ~/.openclaw/workspace/skills/trade-recommender/venv/bin/activate
pip install tastytrade-sdk
```

### 2. Get API Key

1. Visit: https://developer.tastytrade.com/
2. Log in with your Tastytrade credentials
3. Create a new application
4. Generate an API key
5. Copy the API key

### 3. Configure

Update the API key in:
- `tastytrade_client.py` - Line 6
- `test_tastytrade.sh` - Line 5
- Or set environment variable: `TASTYTRADE_API_KEY`

---

## Integration Features

### Tastytrade Client (`tastytrade_client.py`)

**Capabilities:**
- ✅ Account balance and buying power
- ✅ Current positions
- ✅ Real-time quotes
- ✅ Full option chains with Greeks
- ✅ Order placement (paper or live)

**Usage:**
```python
from tastytrade_client import TastytradeAPI

api = TastytradeAPI("your-api-key")
api.connect()

# Get balance
balance = api.get_account_balance()

# Get option chain
chain = api.get_option_chain("SPY")

# Get quote
quote = api.get_quote("AAPL")
```

---

## Why Tastytrade?

**Perfect for Options Trading:**
- Specialized options platform
- Advanced order types
- Greeks and IV data built-in
- Low commissions
- Excellent for Level 3 strategies

**Complements Your Brokerage Setup:**
- Webull (Level 3) - Options strategies
- Public.com - Stock quotes
- Tastytrade - Advanced options execution

---

## Integration with Trade Recommender

### Current Framework Support

Your `OPTIONS_RESEARCH.md` framework includes:
- 7 data categories
- Hard filters (POP ≥0.65)
- 5-trade daily selection
- Risk management

**Tastytrade Enhances:**
1. **Real-time Greeks:** Delta, Gamma, Theta, Vega for all options
2. **IV Data:** Implied volatility for pricing
3. **Open Interest:** Liquidity verification
4. **Spread Pricing:** Multi-leg strategies with proper pricing

### Workflow

```
1. Trade Recommender generates recommendations
   ↓
2. Tastytrade API fetches live option chains
   ↓
3. Calculate Greeks, POP, and pricing
   ↓
4. Present 5 trades with full analysis
   ↓
5. User executes via Tastytrade platform
```

---

## API Endpoints (for reference)

**Base URL:** `https://api.tastyworks.com`

**Key Endpoints:**
- `/customers/me` - User info
- `/customers/me/accounts` - Account list
- `/accounts/{account-id}/balances` - Balance
- `/accounts/{account-id}/positions` - Positions
- `/accounts/{account-id}/orders` - Orders
- `/instruments/equities/{symbol}` - Stock info
- `/option-chains/{symbol}/nest` - Option chains
- `/quotes/{symbol}` - Real-time quotes

**Authentication:**
```bash
curl -H "Authorization: YOUR_API_KEY" \
  https://api.tastyworks.com/customers/me
```

---

## Testing

### Quick Test (Bash)
```bash
./test_tastytrade.sh
```

### Python Test
```bash
python3 tastytrade_client.py
```

Expected output:
```
✅ Connected to Tastytrade account: [account-number]

--- Account Balance ---
cash: $XX,XXX.XX
buying_power: $XX,XXX.XX
net_liquidating_value: $XX,XXX.XX

--- SPY Option Chain ---
[Option details...]

✅ Tastytrade API test complete!
```

---

## Documentation

- **Official SDK:** https://github.com/tastytrade/tastytrade-sdk-python
- **API Reference:** https://developer.tastytrade.com/
- **Python Docs:** https://tastytrade.github.io/tastytrade-sdk-python/

---

## Next Steps

1. ✅ SDK integration code created
2. ✅ Test script created
3. ⚠️ **Generate new API key** (current key invalid)
4. Test connection with valid key
5. Integrate with daily trade recommendations cron
6. Start generating options recommendations

---

**Version:** 1.0
**Status:** Ready (awaiting valid API key)
**Integration Point:** Trade Recommender skill
