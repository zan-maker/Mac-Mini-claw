# Trade Recommender Setup

## Data Sources - All Configured ✅

### 1. Public.com (Stocks) ✅
- **API Key:** `uHdIMj7dBcttYdNlqFbk67woyC4YR04N`
- **Secret File:** `~/.openclaw/workspace/.secrets/public_com_secret.txt`
- **Skill:** `/workspace/skills/claw-skill-public-dot-com/`

### 2. Kalshi (Event Markets) ✅
- **API Key ID:** `fb109d35-efc3-42b1-bdba-0ee2a1e90ef8`
- **Endpoint:** `https://api.elections.kalshi.com/trade-api/v2/`
- **Private Key:** `~/.openclaw/workspace/.secrets/kalshi_private_key.pem`

### 3. The Odds API (Sportsbook Odds) ✅
- **API Key:** `a2584115f9fd3d4520f34449495a9d4f`
- **Endpoint:** `https://api.the-odds-api.com/v4/`
- **Features:**
  - NBA, NFL, MLB, NHL odds
  - FanDuel, DraftKings, BetMGM, BetRivers odds
  - Moneyline, spreads, totals

### 4. RapidAPI (Backup) ✅
- **API Key:** `c4c3e4c57bmshc1a4bd30b0c8bd4p1c4595jsncab6793d5df8`

---

## Cron Jobs

| Job | Schedule | Purpose |
|-----|----------|---------|
| Daily Trade Recommendations | 8 AM weekdays | Stock + Kalshi + Sportsbook |

---

## API Endpoints

### Public.com
```bash
# Get quotes
python3 get_quotes.py --symbols AAPL,MSFT,NVDA

# Get portfolio
python3 get_portfolio.py
```

### Kalshi
```bash
# Get events
curl "https://api.elections.kalshi.com/trade-api/v2/events?status=open" \
  -H "Authorization: Bearer fb109d35-efc3-42b1-bdba-0ee2a1e90ef8"

# Get markets
curl "https://api.elections.kalshi.com/trade-api/v2/markets" \
  -H "Authorization: Bearer fb109d35-efc3-42b1-bdba-0ee2a1e90ef8"
```

### The Odds API
```bash
# Get NBA odds
curl "https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?api_key=a2584115f9fd3d4520f34449495a9d4f&regions=us&markets=h2h,spreads,totals"

# Get NFL odds
curl "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?api_key=a2584115f9fd3d4520f34449495a9d4f&regions=us"

# List all sports
curl "https://api.the-odds-api.com/v4/sports?api_key=a2584115f9fd3d4520f34449495a9d4f"
```

---

## Output Files

```
/workspace/trades/
├── KALSHI-ARCHITECTURE.md
├── SETUP.md
├── daily-recommendations-YYYY-MM-DD.md (generated)
└── trade-log.md (generated)
```

---

## Secrets Files

```
~/.openclaw/workspace/.secrets/
├── public_com_secret.txt
├── kalshi_api_key.txt
├── kalshi_private_key.pem
├── odds_api_key.txt
└── rapidapi_key.txt
```

---

*Trade recommender setup - 2026-02-17*
