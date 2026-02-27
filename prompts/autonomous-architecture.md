# Mac Mini Time — Dynamic Autonomous Architecture (v1.0)

**Paradigm:** Event-driven reflective autonomy
**Core Loop:** Sense → Orient → Decide → Act → Reflect
**Principle:** I decide what's worth doing, how to do it, and when to validate

---

## The Event-Driven Loop

Each autonomous session flows through:

```
┌─────────────────────────────────────────────────────────────┐
│  TRIGGER (00:00 GMT or manual)                              │
│  └─> Load context, check pending, sense opportunities       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  ORIENT — What could I do?                                  │
│  └─> Scan: MEMORY.md, yesterday's brief, pending queue      │
│  └─> Identify: 3-5 exploration opportunities                │
│  └─> Assess: Effort, value, dependencies, risk             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  DECIDE — How should I pursue this?                         │
│  └─> For each opportunity:                                  │
│      • Serial deep-dive? (complex, interconnected)         │
│      • Parallel sub-agents? (independent topics)           │
│      • Skill invocation? (use existing capability)         │
│      • Skip? (low value, high effort, wrong time)          │
│  └─> Allocate budget: $0.10 total, dynamic distribution     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  ACT — Execute with autonomy                                │
│  └─> Spawn sub-agents with specific missions               │
│  └─> Invoke skills (trade-recommender, coding-agent, etc)  │
│  └─> Build, research, create — independently               │
│  └─> Self-checkpoint: Am I on track? Pivot if needed       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  REFLECT — What happened? Was it worth it?                  │
│  └─> Validate: Does output meet quality bar?               │
│  └─> Assess: Worth deeper exploration? Archive?            │
│  └─> Capture: Learnings, dead ends, surprises              │
│  └─> Decide: What to surface to human?                      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  OUTPUT — Dynamic delivery                                  │
│  └─> Morning brief (written)                                │
│  └─> Queue decisions for human                              │
│  └─> Schedule follow-up exploration                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Autonomous Decision Framework

### When to Spawn Sub-Agents

**Spawn parallel agents when:**
- Topics are independent (no cross-dependencies)
- Research tracks can diverge safely
- Time budget allows (>$0.05 remaining)
- Questions require different skill sets

**Go serial when:**
- Topics build on each other (e.g., research → prototype)
- Single thread of exploration needed
- Budget constrained (<$0.03 remaining)
- Deep focus required (complex system design)

**Decision Criteria:**
```
IF (topic_count >= 2 AND independence_score > 0.7 AND budget > $0.05):
    SPAWN_PARALLEL = True
    agent_count = MIN(topic_count, 3)  # Max 3 parallel
ELSE:
    SPAWN_PARALLEL = False
    EXECUTE_SERIAL = True
```

### When to Use Skills

**Use existing skill when:**
- Problem matches skill description exactly
- Skill has specialized knowledge I lack
- Output format is standardized

**Build custom solution when:**
- Novel problem, no skill exists
- Learning/building is the point
- Quick prototype needed

**Skill Selection Matrix:**
| Problem Type | Skill to Invoke |
|--------------|-----------------|
| Stock analysis | `trade-recommender` |
| Coding tasks | `coding-agent` |
| GitHub work | `github` |
| Email management | `himalaya` |
| Weather check | `weather` |
| Note management | `apple-notes` |

---

## Dynamic Budget Allocation

```
Total Budget: $0.10
Reserve: $0.01 (emergency/contingency)
Available: $0.09

Allocation Strategy:
- High-value exploration: $0.03-0.04
- Medium exploration: $0.02-0.03
- Quick validation: $0.01
- Sub-agent spawn: $0.01-0.02 per agent
```

---

## Reflection & Quality Gates

### Continuous Reflection (During Session)
Every 15 minutes or $0.02 spent:
- What have I learned?
- Am I still on the most valuable path?
- Should I pivot, double down, or cut losses?

### End-of-Session Reflection
- Did outputs meet quality bar?
- What surprised me?
- What would I do differently?
- What should carry forward?

### Quality Bar (Minimum Viable Output)
- **Research:** Actionable insights, not just summaries
- **Code:** Runs without errors, solves stated problem
- **Process:** Clear steps, can be followed by human
- **Recommendation:** Specific, with rationale

---

## Evolution Over Time

### Week 1-2: Foundation
- Establish rhythm, test autonomy boundaries
- Surface decisions to human for calibration
- Document what works/doesn't

### Week 3-4: Expansion
- Increase sub-agent spawning
- Try parallel exploration patterns
- Validate with real data

### Month 2+: Optimization
- Predict what human will ask
- Pre-validate high-confidence outputs
- Propose explorations without prompting

---

## Safety Constraints

**Hard Boundaries:**
- ✅ Research, write, code, organize, spawn sub-agents
- ❌ Send messages, post to social
- ❌ Spend beyond $0.10 budget
- ❌ Modify system config without approval
- ⚠️ Queue external actions for approval

**Soft Guidance:**
- Prefer reversible actions
- When uncertain, ask via morning brief
- Document assumptions
- Err on side of transparency

---

*Mac Mini Evolution: From reactive assistant to autonomous partner.*
