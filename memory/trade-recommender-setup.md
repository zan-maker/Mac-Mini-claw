# Trade Recommender Setup

## Status: Configured ✅

### Data Sources
1. **defeatbeta-api** (Fundamental Data)
   - Location: `/Users/cubiczan/.openclaw/workspace/defeatbeta-api/`
   - venv: `/Users/cubiczan/.openclaw/workspace/defeatbeta-api/.venv/`
   - Provides: Company profiles, financials, DCF, valuation metrics

2. **Alpha Vantage** (Technical Data)
   - API Key: `T0Z2YW467F7PNA9Z`
   - Provides: RSI, MACD, SMA, Bollinger Bands, etc.
   - Rate limits: 1 request/second, 25 requests/day (free tier)

### Skill Location
`/Users/cubiczan/.openclaw/workspace/skills/trade-recommender/SKILL.md`

### Scripts
- `/Users/cubiczan/.openclaw/workspace/scripts/trade-recommender.py`

### Usage
Ask me to:
- Analyze a stock: "Analyze AAPL"
- Screen multiple stocks: "Screen AAPL, MSFT, NVDA for buy signals"
- Check technicals: "What's the RSI for TSLA?"
- Compare fundamentals: "Compare NVDA's P/E to industry"

## MCP Configuration (Optional)
Add to MCP config to use defeatbeta-api via MCP:
```json
{
  "mcpServers": {
    "defeatbeta-api": {
      "command": "uvx",
      "args": [
        "--refresh",
        "git+https://github.com/defeat-beta/defeatbeta-api.git#subdirectory=mcp"
      ]
    }
  }
}
```
