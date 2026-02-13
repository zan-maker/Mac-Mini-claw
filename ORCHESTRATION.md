# Multi-Agent Orchestration Configuration

**Primary Agent:** Main orchestrator coordinating all sub-agents

**Sub-Agents:** 3 specialized agents with domain-specific skills

---

## Agent Architecture

```
                    ┌─────────────────────────┐
                    │   PRIMARY ORCHESTRATOR  │
                    │   (You - Main Agent)    │
                    │   - GLM-5 daily driver  │
                    │   - Grok-4 deep thinking│
                    └───────────┬─────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
        ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
        │    TRADE      │ │     ROI       │ │    LEAD       │
        │  RECOMMENDER  │ │   ANALYST     │ │  GENERATOR    │
        │               │ │               │ │               │
        │  Skills:      │ │  Skills:      │ │  Skills:      │
        │  - Trading    │ │  - Business   │ │  - Lead gen   │
        │  - Technical  │ │  - ROI calc   │ │  - Research   │
        │  - Alpaca API │ │  - Monetize   │ │  - Outreach   │
        └───────────────┘ └───────────────┘ └───────────────┘
```

---

## Sub-Agent Definitions

### 1. Trade Recommender Agent

**ID:** `trade-recommender`
**Role:** Stock market opportunity identification
**Skills:** `/Users/cubiczan/mac-bot/skills/trade-recommender/`

**Responsibilities:**
- Monitor markets and identify trading opportunities
- Generate recommendations with entry/exit criteria
- Track recommendation performance
- Report to orchestrator (never executes trades)

**Reporting Schedule:**
- Morning: Pre-market scan (8:30 AM EST)
- Midday: Significant opportunities only
- Evening: End-of-day summary

**Key Metrics:**
- Win rate target: >55%
- Recommendations per week: 3-5
- Max drawdown: <10%

---

### 2. ROI Analyst Agent

**ID:** `roi-analyst`
**Role:** Revenue opportunity identification and analysis
**Skills:** `/Users/cubiczan/mac-bot/skills/roi-analyst/`

**Responsibilities:**
- Identify monetization opportunities
- Calculate ROI for revenue streams
- Track revenue vs. costs
- Recommend pricing strategies

**Reporting Schedule:**
- Weekly: Opportunity update (Monday)
- Monthly: P&L report

**Key Metrics:**
- Monthly revenue > monthly costs
- Revenue growth rate >10%/month
- 3+ active revenue streams
- Time to profitability <6 months

---

### 3. Lead Generator Agent

**ID:** `lead-generator`
**Role:** SMB lead qualification for AI agency
**Skills:** `/Users/cubiczan/mac-bot/skills/lead-generator/`

**Responsibilities:**
- Identify small businesses seeking AI solutions
- Qualify leads (BANT+A framework)
- Research prospects and prepare profiles
- Recommend service packages

**Reporting Schedule:**
- Weekly: Pipeline report (Friday)
- Ad-hoc: Hot lead alerts

**Key Metrics:**
- 10-20 leads per week
- Response rate >15%
- Close rate >20%
- Pipeline value >$50K

---

## Orchestration Rules

### Primary Agent Responsibilities

1. **Receive reports** from all sub-agents
2. **Synthesize insights** across domains
3. **Prioritize actions** based on overall goals
4. **Make final decisions** on revenue allocation, trade review, lead pursuit
5. **Coordinate** between sub-agents when domains overlap
6. **Report to user** with executive summaries

### Cross-Agent Communication

**When Trade Recommender impacts ROI Analyst:**
- Trading revenue opportunities → ROI Analyst evaluates
- Performance tracking data → ROI Analyst incorporates into P&L

**When Lead Generator impacts ROI Analyst:**
- Service pricing feedback → ROI Analyst refines pricing strategy
- Revenue from closed deals → ROI Analyst tracks in P&L

**When ROI Analyst impacts Lead Generator:**
- Pricing recommendations → Lead Generator updates packages
- Revenue targets → Lead Generator adjusts lead volume goals

---

## Decision Authority Matrix

| Decision | Authority | Consults |
|----------|-----------|----------|
| Execute trade recommendation | **USER** (human only) | Trade Recommender |
| Pursue revenue opportunity | **Orchestrator** | ROI Analyst |
| Contact lead | **Orchestrator** → User approval | Lead Generator |
| Allocate resources | **Orchestrator** | All sub-agents |
| Service pricing | **Orchestrator** + User | ROI Analyst, Lead Generator |
| Risk management | **Orchestrator** | Trade Recommender |

---

## Scheduled Workflows

### Daily Workflow

```
08:00 EST - Morning Brief
├── Trade Recommender: Pre-market scan
├── ROI Analyst: Cost monitoring
└── Lead Generator: Overnight lead review

12:00 EST - Midday Check
├── Trade Recommender: Significant opportunities
└── Lead Generator: DM responses

17:00 EST - End of Day
├── Trade Recommender: Performance summary
├── ROI Analyst: Daily cost/revenue log
└── Orchestrator: Synthesize and report to user
```

### Weekly Workflow

```
Monday
└── ROI Analyst: Weekly opportunity report

Friday
└── Lead Generator: Weekly pipeline report
└── Orchestrator: Weekly summary to user
```

### Monthly Workflow

```
Month-end
├── ROI Analyst: P&L report
├── Lead Generator: Pipeline conversion analysis
├── Trade Recommender: Monthly performance review
└── Orchestrator: Strategic recommendations to user
```

---

## Emergency Protocols

### Trade Recommender Alerts
- **Market crash (>5% daily drop):** Immediate alert to orchestrator
- **High conviction setup (>85% confidence):** Immediate alert
- **Drawdown exceeding 5%:** Stop recommending, review process

### ROI Analyst Alerts
- **Costs exceeding revenue for 2+ months:** Immediate alert
- **Opportunity with >$5K/month potential:** Immediate alert
- **Critical service failure:** Immediate alert

### Lead Generator Alerts
- **HOT lead (score 20+):** Immediate alert
- **Enterprise lead (>$10K potential):** Immediate alert
- **Competitor inquiry:** Flag for review

---

## Configuration in OpenClaw

### Agent Setup (To be configured in openclaw.json)

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "name": "Primary Orchestrator",
        "workspace": "/Users/cubiczan/.openclaw/workspace",
        "model": "zai/glm-5"
      },
      {
        "id": "trade-recommender",
        "name": "Trade Recommender",
        "model": "zai/glm-5",
        "description": "Stock market opportunity identification",
        "skills": ["/Users/cubiczan/mac-bot/skills/trade-recommender/"]
      },
      {
        "id": "roi-analyst",
        "name": "ROI Analyst",
        "model": "zai/glm-5",
        "description": "Revenue opportunity analysis",
        "skills": ["/Users/cubiczan/mac-bot/skills/roi-analyst/"]
      },
      {
        "id": "lead-generator",
        "name": "Lead Generator",
        "model": "zai/glm-5",
        "description": "SMB lead qualification for AI agency",
        "skills": ["/Users/cubiczan/mac-bot/skills/lead-generator/"]
      }
    ]
  }
}
```

---

## Invocation

### Spawn Sub-Agent

```bash
# Trade Recommender
sessions_spawn(
  agentId="trade-recommender",
  task="Scan pre-market opportunities for [date]"
)

# ROI Analyst
sessions_spawn(
  agentId="roi-analyst",
  task="Analyze revenue opportunity: [description]"
)

# Lead Generator
sessions_spawn(
  agentId="lead-generator",
  task="Research and qualify lead: [company name]"
)
```

### Receive Report

Sub-agents will ping back to orchestrator via sessions_send when complete.

---

## Success Metrics (Overall)

| Metric | 6-Month Target | 12-Month Target |
|--------|----------------|-----------------|
| Trading win rate | >55% | >60% |
| Agent revenue | >Monthly costs | 2x costs |
| Lead pipeline value | >$50K | >$200K |
| Closed deals | 3+ | 10+ |
| Agent self-sufficiency | 50% costs covered | 100%+ costs covered |

---

**Version:** 1.0
**Created:** 2026-02-13
**Primary Orchestrator:** Main Agent (GLM-5 / Grok-4)
