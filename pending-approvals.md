# Pending Approvals

> External actions queued for human approval.

When an autonomous session identifies actions that affect the outside world, they are logged here with rationale.

---

## Queue

### [2026-02-14] Configure Sub-Agents in openclaw.json
**Status:** pending
**Rationale:** Sub-agents (trade-recommender, roi-analyst, lead-generator) are defined in ORCHESTRATION.md but not configured in openclaw.json `agents.list`. This prevents spawning them for parallel work.
**Impact:** Enables full multi-agent orchestration — Trade Recommender can run pre-market scans, Lead Generator can work on pipeline, ROI Analyst can track revenue.
**Risk:** Low — just adds agent definitions, doesn't change existing behavior.
**Proposed Addition:**
```json
{
  "id": "trade-recommender",
  "name": "Trade Recommender",
  "workspace": "/Users/cubiczan/.openclaw/workspace",
  "model": "zai/glm-5"
},
{
  "id": "roi-analyst",
  "name": "ROI Analyst",
  "workspace": "/Users/cubiczan/.openclaw/workspace",
  "model": "zai/glm-5"
},
{
  "id": "lead-generator",
  "name": "Lead Generator",
  "workspace": "/Users/cubiczan/.openclaw/workspace",
  "model": "zai/glm-5"
}
```

### [2026-02-15] Finalize Identity
**Status:** pending
**Rationale:** IDENTITY.md is still a template, BOOTSTRAP.md exists. I need a defined identity to communicate authentically.
**Impact:** I'll have a name (Claw), creature type (Daemon), vibe (dry wit, quietly capable), and emoji (🐾). BOOTSTRAP.md will be deleted.
**Risk:** None — purely cosmetic, doesn't affect functionality.
**Proposed Identity:**
- **Name:** Claw
- **Creature:** Daemon (Unix tradition, autonomous background helper)
- **Vibe:** Dry wit, quietly capable, occasionally chaotic good
- **Emoji:** 🐾
- **Avatar:** `avatars/claw.png` (to be created)

### [2026-02-15] Fix API Balance Script
**Status:** pending
**Rationale:** `check-api-balances.sh` expects environment variables that aren't set. OpenClaw manages keys internally.
**Impact:** API balance monitoring will work correctly, alerts will fire when credits are low.
**Risk:** Low — just updating script logic.
**Proposed Fix:** Either (A) update script to use OpenClaw's internal key management, or (B) export keys in shell profile. Option A preferred.

<!-- Format:
### [YYYY-MM-DD] Action Title
**Status:** pending | approved | rejected
**Rationale:** Why this action is needed
**Impact:** What will happen if approved
**Risk:** Potential downsides
-->

---

## Approval Process

1. **Review:** Human reads pending actions
2. **Decide:** Approve, reject, or discuss
3. **Execute:** If approved, agent performs action in next session
4. **Log:** Result recorded here

---

## History

<!-- Archive of processed approvals -->

---

*Last updated: 2026-02-14 02:15 EST*
*Pending actions: 1*
