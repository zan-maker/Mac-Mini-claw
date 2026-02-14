# Mac Mini Autonomous Architecture — v1.0

**Created:** 2026-02-13
**Status:** Active
**Cron Jobs:** 2 (Meditation + Autonomous Time)

---

## Overview

This is a self-governing system that allows OpenClaw to operate proactively, exploring, learning, and creating without constant human oversight. It combines project tracking (Trello-like), nightly meditation (internal growth), and autonomous exploration time.

---

## Core Components

### 1. Mental Loop

**Looking Back (Memory):**
- `MEMORY.md` — Historical record, curated knowledge
- `memory/YYYY-MM-DD.md` — Daily logs

**Looking Forward (Meditation):**
- `meditations.md` — Active topics tracker
- `reflections/*.md` — Individual reflection files
- `monuments.md` — Completed projects trophy case

**Operating Independently (Autonomous Time):**
- `prompts/autonomous-time-system.md` — System prompt
- `prompts/autonomous-architecture.md` — Decision framework
- `experiments/` — Sandbox for code experiments

### 2. Cron Jobs

| Name | Schedule | Purpose | Job ID |
|------|----------|---------|--------|
| Nightly Meditation | 1:00 AM EST | Process active topics, reflect, propose seeds | `b52ee6c8-d515-4b47-a762-b61235206164` |
| Autonomous Time | 2:00 AM EST | Explore, learn, create independently | `299c22a6-3b9a-4de6-b4e1-4e5b19f50342` |

### 3. Workflow Integration

```
1:00 AM — Meditation
  ├─ Ground in IDENTITY.md, SOUL.md
  ├─ Process active reflection topics
  ├─ Announce breakthroughs to #mac-mini1
  └─ Propose new seeds if needed

2:00 AM — Autonomous Time
  ├─ Sense opportunities from recent context
  ├─ Decide: serial or parallel exploration
  ├─ Spawn sub-agents if valuable
  ├─ Create, research, build
  └─ Write morning brief
```

---

## Decision Framework

### OODA Loop

1. **Observe:** Load memory, check pending, identify opportunities
2. **Orient:** Score opportunities, filter by value
3. **Decide:** Choose execution mode, allocate budget
4. **Act:** Execute with autonomy, spawn agents, create
5. **Reflect:** Validate outputs, assess worth, surface to human

### Sub-Agent Spawning Criteria

```
IF (topic_count >= 2 AND independence >= 0.7 AND budget >= $0.02):
    SPAWN_PARALLEL = True
    agent_count = MIN(topic_count, 3)
ELSE:
    EXECUTE_SERIAL = True
```

### Skill Selection

| Problem Type | Skill |
|--------------|-------|
| Stock analysis | `trade-recommender` |
| Coding tasks | `coding-agent` |
| GitHub work | `github` |
| Weather | `weather` |
| Notes | `apple-notes` |

---

## Budget Allocation

**Total:** $0.10 per autonomous session
**Reserve:** $0.01 (emergency)
**Available:** $0.09

- High-value exploration: $0.03-0.04
- Medium exploration: $0.02-0.03
- Quick validation: $0.01
- Sub-agent spawn: $0.01-0.02 per agent

---

## Safety Protocols

### ✅ Allowed
- Research, read, write, code
- Organize workspace and memory files
- Spawn sub-agents for parallel work
- Create MD files and commit to memory

### ❌ Forbidden
- Send messages (Discord, Telegram, email)
- Post to social media
- Modify system config without approval
- Spend beyond budget

### ⚠️ Queued for Approval
- External actions → `pending-approvals.md`
- Cron job changes
- Production deployments

---

## File Structure

```
/workspace/
├── prompts/
│   ├── autonomous-time-system.md      # System prompt
│   ├── autonomous-architecture.md     # Decision framework
│   └── autonomous-cron-template.md    # Cron config template
├── meditations.md                     # Active topics
├── monuments.md                       # Completed projects
├── morning-brief.md                   # Daily summary
├── pending-approvals.md               # Queued actions
├── experiments/                       # Sandbox
└── reflections/
    ├── <topic>.md                     # Active reflections
    ├── archive/                       # Completed
    └── README.md                      # Format guide
```

---

## Evolution Roadmap

### Phase 1 (Week 1-2): Foundation
- Establish rhythm
- Test autonomy boundaries
- Surface decisions for calibration
- Document what works

### Phase 2 (Week 3-4): Expansion
- Increase sub-agent spawning
- Parallel exploration patterns
- Validate with real data

### Phase 3 (Month 2+): Optimization
- Predict human needs
- Pre-validate outputs
- Propose explorations proactively

---

## Monitoring

- Check `morning-brief.md` daily
- Review `pending-approvals.md` for queued actions
- Monitor cron job execution via `/status`
- Track token usage and costs

---

*This architecture enables Mac Mini to be a proactive partner, not just a reactive assistant.*
