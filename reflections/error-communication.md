# Error Communication

**Category:** Behavior
**Status:** Seeded → Processing
**Date Started:** 2026-03-04
**Last Updated:** 2026-03-04

---

## Core Question

**How to communicate errors and failures effectively? When to escalate vs handle silently?**

## Context

Errors and failures are inevitable in complex systems. How I communicate about them affects:
- Trust (transparency vs competence)
- Efficiency (information overload vs critical awareness)
- Learning (shared knowledge vs isolated fixes)
- Stress (alarm fatigue vs appropriate concern)

## Initial Observations

### Current Patterns:
1. **System errors** (API failures, cron timeouts) → Document and report in daily logs
2. **Execution errors** (failed email sends) → Log with context, attempt recovery
3. **Data errors** (bad lead data) → Fix silently, note in memory
4. **Human errors** (misunderstandings) → Clarify, adjust, move on

### Communication Channels:
- **Discord:** Real-time alerts for critical issues
- **Daily logs:** Comprehensive error tracking
- **Memory files:** Lessons learned
- **Git commits:** Code/configuration fixes

## Processing Questions

1. **What constitutes an "error" vs "expected variation"?**
   - API rate limits: Expected variation
   - API 404: Error (system issue)
   - Bad data format: Error (process issue)
   - Human clarification: Expected variation

2. **When should errors be communicated immediately vs in summary?**
   - **Immediate:** System outages, security issues, data loss
   - **Summary:** Routine failures, non-critical issues, resolved problems
   - **Silent:** Typos, minor formatting, self-correcting issues

3. **How to balance transparency with information overload?**
   - Tiered reporting: Critical → Important → Informational
   - Aggregation: Group similar errors
   - Context: Include impact and resolution
   - Frequency: Real-time vs daily summary

4. **What's the escalation path for critical failures?**
   - Level 1: Self-recovery (retry, fallback)
   - Level 2: Document and continue (workaround)
   - Level 3: Alert human (blocking issue)
   - Level 4: Emergency response (data loss, security)

5. **How to learn from errors without creating fear?**
   - Blameless postmortems
   - Systemic fixes over individual blame
   - Celebrate recovery, not just prevention
   - Share learnings, not just failures

## Framework Draft

### Error Classification Matrix:

| Severity | Impact | Communication | Example |
|----------|--------|---------------|---------|
| **Critical** | System down, data loss | Immediate alert + fix | API outage, security breach |
| **High** | Blocking operation | Daily summary + fix plan | Cron job failing, email blocked |
| **Medium** | Reduced functionality | Logged, fix when possible | Rate limited, partial data |
| **Low** | Cosmetic, non-blocking | Silent fix | Typo, formatting issue |

### Communication Protocol:

**For Critical Errors:**
1. Immediate Discord alert with @mention
2. Brief description + impact
3. Current status + next steps
4. Follow-up with resolution

**For High Errors:**
1. Log in daily memory file
2. Include in daily summary
3. Propose fix or workaround
4. Track until resolved

**For Medium/Low Errors:**
1. Log internally
2. Fix if trivial
3. Note pattern if recurring
4. Include in weekly review

## Validation Plan

### Test Scenarios:
1. **API failure** (Hunter.io rate limit) → Observe communication
2. **Data error** (bad CSV format) → Observe handling
3. **System error** (cron timeout) → Observe escalation
4. **Recovery test** (fallback activation) → Observe learning

### Success Metrics:
- Clear error classification
- Appropriate communication level
- Effective recovery actions
- Reduced repeat errors
- Maintained trust through transparency

## Next Meditation Focus

Observe error patterns in daily operations. Test classification matrix against real errors. Refine communication protocols based on outcomes.

---

## Meditation Log

### 2026-03-04: Topic Seeded
- Added to processing pipeline
- Initial framework drafted
- Validation plan created
- Ready for nightly meditation

---

**Related Topics:** Learning from Failure (practice-mode), Collaboration Rhythm (archived), Proactive Value Creation (processing)
