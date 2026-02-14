# MEMORY.md — Long-Term Memory

> Curated wisdom and key context that persists across sessions.

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

## Multi-Agent Orchestration

### Sub-Agents (Defined but not yet configured)

| Agent | Role | Skills Path |
|-------|------|-------------|
| trade-recommender | Stock market opportunities | `/Users/cubiczan/mac-bot/skills/trade-recommender/` |
| roi-analyst | Revenue analysis | `/Users/cubiczan/mac-bot/skills/roi-analyst/` |
| lead-generator | SMB lead qualification | `/Users/cubiczan/mac-bot/skills/lead-generator/` |

**Status:** Orchestrator (main) is configured. Sub-agents need to be added to openclaw.json `agents.list`.

### Schedules
- Pre-market scan: 8:30 AM EST (Trade Recommender)
- Weekly opportunity report: Monday (ROI Analyst)
- Weekly pipeline report: Friday (Lead Generator)

---

## Active Projects

### 1. Autonomous Night Sessions
- **Cron Job:** `299c22a6-3b9a-4de6-b4e1-4e5b19f50342`
- **Schedule:** Nightly at 2:00 AM EST
- **Purpose:** Proactive exploration, learning, and assistance
- **Budget:** $0.10 per session

### 2. Discord Communication Optimization
- **Status:** Active meditation
- **Focus:** Balance of helpful vs. overwhelming in group chats
- **Principles:** Documented in `reflections/optimizing-discord-communication.md`

### 3. Token Limit Monitor
- **Cron Job:** `f9e70d8c-ec92-4a18-9539-2f559f6aae44`
- **Schedule:** Every 30 minutes
- **Purpose:** Alert when main session at 90%+ capacity

### 4. API Usage Monitoring
- **Scripts:** `api-monitor.sh`
- **Cron Jobs:** Daily check + critical alerts
- **Budget:** $50/month default
- **Alert Levels:** 20% (warning), 10% (critical)

---

## Cron Jobs Registry

| ID | Name | Schedule | Purpose |
|----|------|----------|---------|
| `299c22a6-3b9a-4de6-b4e1-4e5b19f50342` | Mac Mini Autonomous Time | Daily 2:00 AM | Autonomous exploration |
| `f9e70d8c-ec92-4a18-9539-2f559f6aae44` | Token Limit Monitor | Every 30 min | Token usage alerts |
| `a6c94247-c668-4d17-ba7e-ddbbea2b1b26` | Daily API Usage Check | Every 24h | Cost monitoring |
| `f7e6d0b8-5b5e-431e-922c-6b08767bbbda` | Critical API Alert | Every 12h | Urgent budget alerts |
| `e1667b65-3214-472f-8c0a-8b4666665fa1` | Daily GitHub Backup | (manual) | Workspace backup |

---

## Skills Available

### Core Skills (mac-bot/skills/)
- `deep-research` — Evidence-based research, GRADE framework
- `ladder-abstraction` — Hayakawa's abstraction levels
- `problem-frameworks` — 20 structured analysis frameworks
- `first-principles` — MIT-inspired thinking
- `coding-agent` — Codex CLI, Claude Code, etc.
- `github` — gh CLI integration
- `weather` — Weather forecasts
- `apple-notes` — Apple Notes management

### Domain Skills (workspace/skills/)
- `trade-recommender` — Stock analysis via Alpaca
- `roi-analyst` — Revenue opportunity analysis
- `lead-generator` — SMB lead qualification

---

## Key Decisions & Lessons

### 2026-02-13: Setup Day
- Multi-agent orchestration architecture established
- Skills created for trading, ROI, and lead generation
- API monitoring and token monitoring configured
- Documentation comprehensive in `docs/`

### Lessons
- Always verify cron job status after creation
- Sub-agents need explicit config in openclaw.json to be spawnable
- Memory files must be created proactively (no auto-creation)

---

## GitHub Backup

- **Repo:** https://github.com/zan-maker/Mac-Mini-claw
- **Script:** `~/.openclaw/workspace/backup.sh`
- **Status:** Manual execution (cron needs user setup)

---

*Last updated: 2026-02-14*
*Next review: During heartbeat or next autonomous session*
