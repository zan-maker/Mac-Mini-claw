# API Keys & Web Access Configuration

**Last Updated:** 2026-02-13

## Web Search APIs

### Brave Search API (Primary)
- **API Key:** `BSAqx7g5ob7ymEOAUfRduTetIOWPalN`
- **Usage:** Primary web search for all agents
- **Base URL:** `https://api.search.brave.com/res/v1/web/search`

### Tavily API (Fallback)
- **API Key:** `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`
- **Usage:** When Brave limits reached
- **Base URL:** `https://api.tavily.com/search`

---

## Data Enrichment APIs

### Hunter.io (Email/Company Discovery)
- **API Key:** `f701d171cf7decf7e730a6b1c6e9b74f29f39b6e`
- **Usage:** Find emails, company data
- **Base URL:** `https://api.hunter.io/v2/`

### Zyte Web Scraper API
- **API Key:** `8d3e9c7af6e948b088e96ad15ca21719`
- **Usage:** Build target lists, scrape websites
- **Base URL:** `https://app.zyte.com/api/`

### Abstract API (Company Enrichment)
- **API Key:** `38aeec02e6f6469983e0856dfd147b10`
- **Usage:** Enrich company data
- **Base URL:** `https://companyenrichment.abstractapi.com/v1/`
- **Docs:** https://app.abstractapi.com/api/company-enrichment

---

## Financial Data APIs

### Alpha Vantage (Technical Indicators)
- **API Key:** `T0Z2YW467F7PNA9Z`
- **Usage:** RSI, MACD, SMA, price data
- **Base URL:** `https://www.alphavantage.co/query`

### NewsAPI (Financial News)
- **API Key:** `fe52ac365edf464c9dca774544a40da3`
- **Usage:** Trade recommender news feed
- **Base URL:** `https://newsapi.org/v2/`

### AgentMail (Email Sending)
- **Email:** `Zane@agentmail.to`
- **API Key:** `am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68`
- **Usage:** Automated outreach emails
- **Base URL:** `https://api.agentmail.to/v0`
- **CC:** `sam@impactquadrant.info` (on all emails)

### Alpaca API (Paper Trading)
- **Endpoint:** `https://paper-api.alpaca.markets/v2`
- **API Key:** `PKNDK5P66FCRH5P5ILPTVCYE7D`
- **Secret Key:** `z1fwAHFV9H8NY26XrZ2sSSxJggc8BwqiU2gPxVsy49V`
- **Usage:** Paper trading, account management, orders
- **Mode:** Paper trading (sandbox)

### defeatbeta-api (Fundamental Data)
- **Status:** Already connected
- **Location:** `/Users/cubiczan/.openclaw/workspace/defeatbeta-api/`
- **Python venv:** `.venv/`

---

## AI/Crawling Tools

### crawl4ai (Web Crawling)
- **Status:** ✅ Installed
- **Location:** `/Users/cubiczan/.openclaw/workspace/defeatbeta-api/.venv/`
- **Python:** `.venv/bin/python`
- **Usage:** LLM-powered web crawling and scraping

---

## Model APIs (Already Configured)

### xAI (Grok)
- **Provider:** xai
- **Models:** grok-2, grok-4
- **Status:** ✅ Configured

### Zhipu AI (GLM)
- **Provider:** zai
- **Models:** glm-5, glm-4.7
- **Status:** ✅ Configured

### OpenAI
- **API Key:** In environment
- **Status:** ✅ Configured

### DeepSeek
- **API Key:** In environment
- **Status:** ✅ Configured

### Qwen
- **API Key:** In environment
- **Status:** ✅ Configured

---

## Rate Limits

| API | Limit | Notes |
|-----|-------|-------|
| Brave Search | 2000 req/month | Free tier |
| Tavily | 1000 req/month | Free tier |
| Alpha Vantage | 25 req/day | Free tier |
| NewsAPI | 100 req/day | Free tier |
| Hunter.io | 25 req/month | Free tier |
| Zyte | Pay per request | Credits-based |

---

## Usage Priority

1. **Web Search:** Brave → Tavily (fallback)
2. **Company Data:** Hunter.io → Abstract API → Zyte scraping
3. **Financial Data:** defeatbeta (fundamentals) + Alpha Vantage (technicals) + NewsAPI (news)
4. **Crawling:** crawl4ai with LLM extraction
