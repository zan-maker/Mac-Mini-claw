# Trading Accounts

**Last Updated:** 2026-02-20

---

## Active Brokerage Accounts

### 1. Webull (NEW - 2026-02-20)
**Account Type:** Margin
**Options Level:** Level 3 ✅
**Status:** Approved and Active

**Level 3 Allows:**
- All Level 1 & 2 strategies
- Long calls and puts
- Covered calls
- Cash-secured puts
- Bull/bear spreads
- Calendar spreads
- Straddles and strangles
- Iron condors
- Butterflies
- Complex multi-leg strategies

**API Status:** TBD (check Webull API documentation)
**Use Case:** Options trading, advanced strategies

---

### 2. Tastytrade (NEW - 2026-02-20)
**Account Type:** Margin
**Account Number:** `5WI41087` ✅
**Options Focus:** Advanced options execution
**Status:** ✅ **API OPERATIONAL**

**OAuth Credentials:**
- Client ID: `0c7b8898-a2f1-49bb-a23d-843e47b68631`
- Client Secret: Configured
- Refresh Token: Configured (never expires)

**Integration:** `/workspace/skills/trade-recommender/tastytrade_oauth_client.py`

**Features:**
- ✅ OAuth 2.0 authentication working
- ✅ Account access verified
- ✅ Balance endpoint accessible
- ✅ Full option chains with Greeks
- ✅ Real-time quotes
- ✅ Advanced order types
- ✅ Spread trading
- ✅ Low commissions

**Account Status:**
- Created: 2026-02-20
- **Funded: $100.00** (2026-02-20 12:10 PM)
- Balance: ⏳ Pending API sync (5-15 min)
- Positions: None
- **Status:** ✅ **READY FOR TRADING**

**Use Case:** Primary options execution platform

---

### 3. Public.com
**API Key:** `uHdIMj7dBcttYdNlqFbk67woyC4YR04N`
**Account Type:** Standard
**Features:** Stock trading, fractional shares

**Scripts:** `/workspace/skills/claw-skill-public-dot-com/scripts/`
- `get_quotes.py` - Real-time quotes
- `get_portfolio.py` - Portfolio holdings
- `place_trade.py` - Execute trades

**Use Case:** Stock recommendations, portfolio tracking

---

### 4. Alpaca (via Trade Recommender)
**Status:** Configured in trade-recommender skill
**Account Type:** Margin
**Features:** Commission-free stock trading, paper trading

**Skill:** `/workspace/skills/trade-recommender/`
**Use Case:** Algorithmic trading, backtesting

---

## Trading Strategy Integration

### Stock Recommendations
- **Primary:** Public.com API
- **Backup:** Alpaca API
- **Cron Job:** Daily Trade Recommendations (8 AM EST)

### Options Strategies
- **Primary:** Webull (Level 3 - Advanced)
- **Strategies:** Iron condors, butterflies, spreads, straddles/strangles
- **Framework:** OPTIONS_RESEARCH.md in trade-recommender skill

### Sportsbook / Event Markets
- **Kalshi:** Event contracts API
- **The Odds API:** Sportsbook odds comparison
- **Use Case:** Arbitrage opportunities

---

## API Configuration

| Data Source | API Key | Status | Use Case |
|-------------|---------|--------|----------|
| **Twelve Data** | `26b639a38e124248ba08958bcd72566f` | ✅ Active | Real-time quotes, technical analysis |
| **Tastytrade** | OAuth 2.0 | ✅ Active | Options execution (primary) |
| **Public.com** | `uHdIMj7dBcttYdNlqFbk67woyC4YR04N` | ✅ Active | Stock quotes, portfolio |
| **Webull** | TBD | 🔄 New | Options strategies (backup) |
| **Alpaca** | Configured | ✅ Active | Algorithmic trading |
| **Kalshi** | `fb109d35-efc3-42b1-bdba-0ee2a1e90ef8` | ✅ Active | Event markets |
| **The Odds API** | `a2584115f9fd3d4520f34449495a9d4f` | ✅ Active | Sportsbook odds |

---

## Next Steps for Webull Integration

1. **Check API availability:** Review Webull API documentation
2. **Generate API keys:** If available, create API credentials
3. **Test connection:** Verify API access with scripts
4. **Integrate with Trade Recommender:** Add Webull as options execution platform
5. **Update daily cron job:** Include Webull options recommendations

---

## Options Strategy Framework

**Available in Trade Recommender:**
- `OPTIONS_RESEARCH.md` - Systematic selection criteria
- 7 data categories for analysis
- Hard filters (POP ≥0.65, quote age ≤10 min)
- 5-trade daily selection with thesis
- Risk management protocols

**Webull Level 3 Strategies Ready:**
- ✅ Iron condors (neutral outlook)
- ✅ Butterflies (pin risk strategies)
- ✅ Calendar spreads (term structure plays)
- ✅ Straddles/strangles (volatility plays)
- ✅ Complex spreads (multi-leg income strategies)

---

## Cron Jobs Using Trading APIs

| Job | Schedule | APIs Used |
|-----|----------|-----------|
| Daily Trade Recommendations | 8 AM | Public.com, Kalshi, The Odds API |
| Options Performance Report | 4 PM | TBD (Webull integration) |
| NBA Cash Out Checks | Game time | Brave Search (live scores) |

---

**Version:** 1.1
**Latest Addition:** Webull (Level 3 Options) - 2026-02-20
