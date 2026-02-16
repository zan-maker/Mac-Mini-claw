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
| **AgentMail** | `am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f` | Email outreach |
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

---

## Cron Jobs Registry (16 Active)

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

*Last updated: 2026-02-16*
*Next review: During heartbeat or next autonomous session*
