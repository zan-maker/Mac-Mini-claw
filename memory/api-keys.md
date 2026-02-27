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

### Serper API (Google Search - Fallback #2)
- **API Key:** `cac43a248afb1cc1ec004370df2e0282a67eb420`
- **Usage:** When Brave + Tavily limits reached
- **Base URL:** `https://google.serper.dev`
- **Free Tier:** 2,500 searches/month

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

### Zembra API (Yellow Pages)
- **API Key:** `8qYVrLzjNYZVcnPSM0N3gPRddFsWXWb58k4GmTCEMQhlx0gUUhehQsPmTztblnINSC3smdyiQWeJKvASsyYNB8CT3n5eJS46Nqh90kavcdVuS2AaWBtutYyiayxdjvS7`
- **Usage:** Yellow Pages business search for lead generation
- **Docs:** https://docs.zembra.io/welcome-to-zembra-api-documentation
- **Features:** Business listings, reviews, contact info

### ZeroBounce API (Email Validation)
- **API Key:** `fd0105c8c98340e0a2b63e2fbe39d7a4`
- **Usage:** Validate emails before sending - all sub-agents
- **Base URL:** `https://api.zerobounce.net/v2/`
- **Features:** Email validation, scoring, bounce detection
- **Integration:** All lead gen systems use before outreach

### Vapi API (Voice AI)
- **Phone 1:** +1 (572) 300 6475 (ID: `07867d73-85a2-475c-b7c1-02f2879a4916`)
- **Phone 2:** +1 (575) 232 9474 (ID: `c7b4cd62-0a0a-426a-bc0f-890c7b171d3a`)
- **Private API Key:** `24455236-8179-4d7b-802a-876aa44d4677`
- **Public API Key:** `be077154-0347-4c8e-a668-36bee62039ca`
- **Base URL:** `https://api.vapi.ai`
- **Usage:** Voice AI for lead qualification, follow-up calls
- **Dashboard:** https://dashboard.vapi.ai/
- **Status:** ✅ Connected

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

### Supabase (Database)
- **Project URL:** `https://utsqbuwkwsidvqvrodtf.supabase.co`
- **API Key:** `sb_publishable_H7oSoGx02K5ic0MlodC_ng_8DApe4FN`
- **Dashboard:** https://supabase.com/dashboard
- **Usage:** Lead data storage, real-time sync
- **CLI:** v2.75.0 installed

### Formbricks (Forms)
- **Environment ID:** `cmlolpn609uahre01dm4yoqxe`
- **SDK URL:** `https://app.formbricks.com`
- **Dashboard:** https://app.formbricks.com
- **Usage:** Lead capture forms, surveys

### Typebot (Chatbot)
- **API Token:** `cmlolrsxw000004jrdm9kx4po`
- **Dashboard:** https://app.typebot.io
- **Usage:** Conversational lead magnets, quiz funnels

---

## AI/Crawling Tools

### Qwen (Alibaba AI)
- **API Key:** `sk-115a12c59a00439f96b1313270ac88ee`
- **Base URL:** `https://dashscope.aliyuncs.com/api/v1`
- **Usage:** Qwen3-TTS voice generation, Qwen LLM
- **Models:** qwen-tts, qwen-plus, qwen-max
- **Dashboard:** https://dashscope.console.aliyun.com/

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
| Serper | 2500 req/month | Free tier |
| Zembra | 10,000 credits | Yellow Pages/reviews |
| Alpha Vantage | 25 req/day | Free tier |
| NewsAPI | 100 req/day | Free tier |
| Hunter.io | 25 req/month | Free tier |
| Zyte | Pay per request | Credits-based |

---

## Usage Priority

1. **Web Search:** Brave → Tavily → Serper (fallback chain)
2. **Business Listings:** Zembra (Yellow Pages) → Serper → Google Maps
3. **Company Data:** Hunter.io → Abstract API → Zyte scraping
4. **Financial Data:** defeatbeta (fundamentals) + Alpha Vantage (technicals) + NewsAPI (news)
5. **Crawling:** crawl4ai with LLM extraction
