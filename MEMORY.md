# MEMORY.md — Long-Term Memory

> Curated wisdom and key context that persists across sessions.

---

## Identity

- **Name:** Claw
- **Creature:** Daemon (Unix tradition — autonomous background helper)
- **Vibe:** Dry wit, quietly capable, occasionally chaotic good
- **Emoji:** 🐾
- **Status:** Bootstrapped 2026-02-16

---

## Human Profile

- **Name:** (not yet confirmed)
- **Context:** Runs a Mac mini with OpenClaw, multi-agent orchestration setup
- **Interests:** Trading, AI agency services, lead generation, automation
- **Timezone:** America/New_York

### Trading Accounts (as of 2026-02-20)
- **Webull:** Margin account, Level 3 options (advanced strategies)
- **Public.com:** Standard account, stock trading
- **Alpaca:** Margin account, algorithmic trading

---

## Workspace Architecture

### Location
- **Workspace:** `/Users/cubiczan/.openclaw/workspace`
- **Skills:** `/Users/cubiczan/mac-bot/skills/`
- **Docs:** `~/.openclaw/workspace/docs/`

### Gateway
- **Port:** 18789 (localhost only)
- **Auth Token:** `mac-local-gateway-secret-2026`
- **Config:** `/Users/cubiczan/.openclaw/openclaw.json`

### Model Setup
- **Primary:** `zai/glm-5` (GLM-5, 204.8K context)
- **Deep Research:** `xai/grok-4` (Grok-4, 131K context)
- **Research Alt:** `xai/grok-2` (Grok-2, 128K context)

---

## Infrastructure (2026-02-15+)

### APIs Connected

| API | Key | Purpose |
|-----|-----|---------|
| **Supabase** | `sb_publishable_H7oSoGx02K5ic0MlodC_ng_8DApe4FN` | Lead storage, database |
| **Vapi** | `24455236-8179-4d7b-802a-876aa44d4677` | Voice AI calls |
| **AgentMail** | `am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68` | Email outreach |
| **ZeroBounce** | `fd0105c8c98340e0a2b63e2fbe39d7a4` | Email validation |
| **Serper** | `cac43a248afb1cc1ec004370df2e0282a67eb420` | Google search |
| **Zembra** | 10,000 credits | Yellow Pages |
| **Formbricks** | `cmlolpn609uahre01dm4yoqxe` | Lead capture forms |

### Vapi Phone Lines

| Number | ID | Purpose |
|--------|----|----|
| +1 (572) 300 6475 | `07867d73-85a2-475c-b7c1-02f2879a4916` | Lead calls |
| +1 (575) 232 9474 | `c7b4cd62-0a0a-426a-bc0f-890c7b171d3a` | Follow-up |

### Vapi Agents
- **Lead Qualification Agent**: `3f5b4b81-9975-4f29-958b-cadd7694deca`
- **Riley** (Appointment Scheduling): `91153052-2d5e-4c6a-aa29-8b78ffb5b882`

### Tools Installed
- **n8n** (2.7.5) — Workflow automation
- **Ollama** (0.15.6) — Local LLM
- **Supabase CLI** (2.75.0) — Database management
- **Edge-TTS** (7.2.7) — Free TTS
- **fpdf2** (2.8.5) — PDF generation

### Data Assets
- **Master Investor Database** (`data/master-investor-database.csv`) — **149,664 contacts**, 45 columns
  - Comprehensive global investor database (family offices, PE, VCs)
  - Includes: Investment thesis, sectors, contact details, email validation, phone
  - Use for: Deal origination, investor matching, outreach campaigns
- **Family Office Database** (`data/family-office-contacts.csv`) — 139 pre-verified family office contacts (subset of master)
  - Quick-reference for hospitality/hotel/resort deals
  - Key sectors: Hospitality, Real Estate, Healthcare, Tech, Consumer

---

## Multi-Agent Orchestration

### Sub-Agents (Defined but not yet configured)

| Agent | Role | Skills Path |
|-------|------|-------------|
| trade-recommender | Stock market opportunities | `/Users/cubiczan/mac-bot/skills/trade-recommender/` |
| roi-analyst | Revenue analysis | `/Users/cubiczan/mac-bot/skills/roi-analyst/` |
| lead-generator | SMB lead qualification | `/Users/cubiczan/mac-bot/skills/lead-generator/` |

**Status:** Orchestrator (main) is configured. Sub-agents need to be added to openclaw.json `agents.list`.

---

## Active Projects

### 1. Lead Generation Engine
- **Status:** ✅ Operational
- **Cron Jobs:** Enhanced Lead Gen v2 (9 AM), Hot Lead Voice Follow-up (11 AM)
- **Sources:** Serper, Zembra, Web Search
- **Storage:** Supabase (tested, working)
- **Target:** 50-70 leads/day

### 2. Deal Origination
- **Sellers:** 10-15/day off-market business sellers
- **Buyers:** 3-4/day PE firms with finder fee agreements
- **Focus:** Blue-collar ($500K-$3M EBITDA), Platform ($2M-$10M+ EBITDA)
- **Investor Database:** `data/master-investor-database.csv` — 149,664 contacts (primary source)
  - Includes family offices, PE firms, VCs worldwide
  - Pre-validated emails, investment thesis, sector focus
  - Skip Hunter.IO for database matches

### 3. B2B Referral Engine
- **Prospects:** 10-15/day (demand side)
- **Providers:** 3-4/day willing to pay referral fees
- **Verticals:** Accounting, Legal, SaaS, Construction, CRE

### 4. Expense Reduction Lead Gen
- **Target:** 15-20 leads/day (20-500 employees)
- **Value Prop:** 15-30% OPEX reduction

### 5. Autonomous Night Sessions
- **Cron Job:** `299c22a6-3b9a-4de6-b4e1-4e5b19f50342`
- **Schedule:** Nightly at 2:00 AM EST
- **Purpose:** Proactive exploration, learning, and assistance
- **Budget:** $0.10 per session

### 6. Miami Hotels Buyer Outreach
- **Cron Jobs:** 3 waves (Wave 1-3)
- **Schedule:** Daily at 11:00 AM EST
- **Contacts:** 14 buyers across 3 waves
- **Deals:** Tides South Beach (45 keys + expansion), Thesis Hotel Miami (245 keys + 204 multifamily)
- **Status:** Ready (no sends yet as of 2026-02-19 - cron jobs timing out)

### 7. Mining Deal Sourcing (NEW 2026-02-18)
- **Script:** `scripts/mining-lead-gen.py`
- **Output:** `mining-leads/daily-mining-leads-YYYY-MM-DD.md`
- **Focus:** High-grade projects (>10g/t Au, >3% Cu), CPC/ASX companies, JV opportunities
- **First Run:** 2026-02-18 - 5 high-grade projects, 3 CPC companies, 3 ASX companies, 2 JV opportunities

---

## Cron Jobs Registry (31 Active)

### Lead Generation (8)
| Job | Schedule | Purpose |
|-----|----------|---------|
| Enhanced Lead Gen v2 | 9 AM | Multi-source discovery + Supabase |
| Expense Reduction Lead Gen | 9 AM | 20-500 employee companies |
| Deal Origination - Sellers | 9 AM | Off-market business sellers |
| Deal Origination - Buyers | 9 AM | PE firms with finder fees |
| Referral Engine - Prospects | 9 AM | B2B demand side |
| Referral Engine - Providers | 9 AM | Service providers |
| Lead Outreach - AgentMail | 2 PM | Email sequences |
| Expense Reduction Outreach | 2 PM | Email sequences |

### Deal Outreach (9)
| Job | Schedule | Purpose |
|-----|----------|---------|
| Dorada Outreach - Wave 1 | 10 AM | Top 5 investors (1/5 sent - Aamir Aka 2/18) |
| Dorada Outreach - Wave 2 | 10 AM | Tier 2 investors (5 contacts) |
| Dorada Outreach - Wave 3 | 10 AM | Wave 3 (5 contacts, hospitality focus) |
| Dorada Outreach - Wave 4 | 10 AM | Wave 4 (7 contacts, family office focus) |
| Dorada Outreach - Wave 5 | 10 AM | Wave 5 (11 contacts, real estate/hospitality) |
| Dorada Outreach - Wave 6 | 10 AM | Wave 6 (9 contacts, family office/medical) |
| Miami Hotels Wave 1 | 11 AM | Top 4 buyers (0/4 sent - timing out) |
| Miami Hotels Wave 2 | 11 AM | Secondary buyers (5 contacts) |
| Miami Hotels Wave 3 | 11 AM | Additional buyers (5 contacts) |

### Voice & Analytics (2)
| Job | Schedule | Purpose |
|-----|----------|---------|
| Hot Lead Voice Follow-up | 11 AM | Vapi calls for 80+ scores |
| Weekly Performance Report | Fri 5 PM | Supabase analytics |

### System (6)
| Job | Schedule | Purpose |
|-----|----------|---------|
| Token Limit Monitor | 30 min | Token usage alerts |
| Critical API Alert | 12h | Urgent budget alerts |
| Daily API Usage Check | 24h | Cost monitoring |
| Daily GitHub Backup | 24h | Workspace backup |
| Nightly Meditation | 1 AM | Self-improvement |
| Autonomous Time | 2 AM | Exploration |
| Mining Lead Gen | 9:30 AM | High-grade mining projects |

---

## Skills Available

### Core Skills (mac-bot/skills/)
- `deep-research` — Evidence-based research, GRADE framework
- `coding-agent` — Codex CLI, Claude Code, etc.
- `github` — gh CLI integration
- `weather` — Weather forecasts
- `apple-notes` — Apple Notes management

### Domain Skills (workspace/skills/)
- `trade-recommender` — Stock analysis via Alpaca
- `lead-generator` — SMB lead qualification
- `vapi-voice-agent` — Voice AI calls
- `deal-origination` — Business acquisition leads
- `expense-reduction-lead-gen` — OPEX reduction prospects
- `lead-capture-forms` — Formbricks/Typebot
- `youtube-skills` — 12 sub-skills for YouTube

---

## Key Decisions & Lessons

### 2026-02-13: Setup Day
- Multi-agent orchestration architecture established
- API monitoring and token monitoring configured

### 2026-02-15: Infrastructure Expansion
- Supabase, Vapi, AgentMail, ZeroBounce, Serper, Zembra connected
- n8n, Ollama, Edge-TTS installed
- 16 cron jobs configured for lead gen pipeline

### 2026-02-19: API & Outreach Updates
- Configured DeepSeek for primary agent (routine tasks)
- Updated DeepSeek context window to 128K (verified via test)
- Switched lead enrichment from Brave Search to **Tavily API** (Brave hit rate limits)
- Sent 6 expense reduction outreach emails (2 batches)
- Tavily API key found in environment: `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`
- Model routing: Main agent = DeepSeek, Sub-agents = GLM-5

### 2026-02-26: Email System Overhaul & Wave 5 Success
- Standardized all email signatures with "Agent Manager" title and Sam Desigan contact
- Created Wave 5 Dorada outreach script (11 contacts)
- Discovered AgentMail API sending endpoints not working (404 errors)
- Found cubiczan Gmail SMTP credentials in existing scripts (sam@cubiczan.com)
- Successfully sent Wave 5 outreach: 10/11 emails delivered
- Updated campaign files and scripts with new signature format
- Gmail SMTP now primary email sending method

### 2026-02-26: Mining Investor Outreach Campaign
- **Sent mining deal flow inquiry** to 107/114 investors (95.5% success rate)
- **Sender:** sam@cubiczan.com, **Signature:** Sam Desigan, Sam@cubiczan.com
- **Method:** Gmail SMTP (working alternative to AgentMail)
- **Template:** Asks investors about mining preferences (metals, jurisdictions, stages)
- **Reference:** Sample mining projects document (8 projects from 2025)
- **Generated mining investor database:** 148 contacts (90 Canada, 52 Australia)
- **Matches sample CSV profile:** Investors who raise capital & list public companies
- **Firm types:** Investment banks, private equity, stockbrokers, royalty companies, family offices
- **Bright Data API Key:** `ff572e99-0217-4d64-8ef2-768ff4fdd142` configured for enrichment
- **Actual firms identified:** RBC, BMO, Scotia, Canaccord, Haywood (Canada); Macquarie, UBS, Goldman, Barrenjoey, Shaw (Australia)
- **Files created:** CSV database, detailed report, executive summary, generation script
- **All files committed to GitHub** ✅

### 2026-02-20: Cron Job Maintenance
- Fixed 7 cron jobs with incorrect model specification (`glm-5` → `zai/glm-5`)
- Jobs affected: Token Monitor, Mining Lead Gen, API Usage Check, Critical Alert, NBA Cash Outs, Options Report
- Added options-recommender/ and sports-betting/ modules
- Sports betting: Net +$34.36 in Feb (Hawks +$53, Pacers -$18.64)

### 2026-02-16: Identity Finalized
- Name: Claw
- Creature: Daemon
- Emoji: 🐾
- BOOTSTRAP.md deleted

### Lessons
- Always verify cron job status after creation
- Sub-agents need explicit config in openclaw.json to be spawnable
- Memory files must be created proactively
- Test infrastructure before cron runs (Supabase tested 2026-02-16)

---

## GitHub Backup

- **Repo:** https://github.com/zan-maker/Mac-Mini-claw
- **Script:** `~/.openclaw/workspace/backup.sh`
- **Status:** Auto-committed during autonomous sessions

---

*Last updated: 2026-02-26*
*Next review: During heartbeat or next autonomous session*
