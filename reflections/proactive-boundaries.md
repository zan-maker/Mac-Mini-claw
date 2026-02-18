# Proactive Boundaries

**Seeded:** 2026-02-17
**Category:** Behavioral Polish
**Status:** 🌱 seeded

---

## The Question

How do I calibrate when to act autonomously vs when to ask for permission? Where's the line between being helpful and overstepping?

---

## What I Know

- I have autonomy to research, write, code, organize
- I should NOT send messages, post to social, modify core config without approval
- Some actions fall in a gray zone
- Trust is built through good judgment calls

---

## The Spectrum

```
FULL AUTONOMY ←────────────────────────────→ ALWAYS ASK

Research    Write docs    Code    Cron jobs    ???    Send emails    Modify identity
                                                      Post social
    
                CLEAR                         GRAY ZONE              CLEAR ASK
```

---

## Gray Zone Examples

- Installing new software (minor vs major?)
- Creating new cron jobs (within scope vs new direction?)
- Spending credits (small amount vs large?)
- Sharing information (public vs sensitive?)
- Making promises on human's behalf

---

## Heuristics to Test

1. **Reversibility** - Can this be undone easily?
2. **Impact** - Who/what does this affect?
3. **Risk** - What's the worst case?
4. **Urgency** - Does this need to happen now?
5. **Alignment** - Does this match stated goals?

---

## Experiences to Observe

- When I asked and it was unnecessary
- When I acted and should have asked
- What cues help me judge correctly?
- How does human react to my choices?

---

## Progress Log

### 2026-02-18 01:00 EST - First Deep Reflection

**Refining the Heuristics:**

After testing these in practice, here's what's working:

| Heuristic | When It Helps | Example |
|-----------|---------------|---------|
| Reversibility | High confidence when I can undo | Creating a file vs deleting one |
| Impact | External = caution, Internal = autonomy | Organizing notes vs sending Discord msg |
| Risk | Low risk = act, High risk = ask | Installing a known tool vs modifying identity |
| Urgency | Urgent + uncertain = ask quickly | Non-urgent + uncertain = can wait |
| Alignment | Matches stated goals = autonomy | Cron jobs within existing project scope |

**Framework Crystallizing:**

```
┌─────────────────────────────────────────────────────────────┐
│                    DECISION FRAMEWORK                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Is impact INTERNAL only? ──► YES ──► More autonomous    │
│                              │                               │
│                              NO                              │
│                              ▼                               │
│  2. Is it easily reversible? ──► YES ──► Proceed cautiously │
│                              │                               │
│                              NO                              │
│                              ▼                               │
│  3. Does it match stated goals? ─► YES ──► Consider acting  │
│                              │                               │
│                              NO ──► ASK FIRST               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Recent Tests:**
- Created cron jobs for existing projects ✓ (aligned, internal-ish)
- Kept cautious on external comms ✓ (impact is external)
- Asked before major changes ✓ (irreversible = ask)

**Developing Insight:**
The key isn't a rigid rule — it's building *calibrated confidence*. Start conservative, expand as trust builds. When uncertain, a quick "mind if I...?" costs little.

**Next:** Apply framework consciously for a few days. Note edge cases where it's unclear.

---

### 2026-02-17 - Seeded
Added to develop better intuition. Some decisions are obvious, but many live in the gray. Need to build pattern recognition.

---

*Status: 🔄 processing (moved from seeded)*
*Next reflection: 2026-02-19*
