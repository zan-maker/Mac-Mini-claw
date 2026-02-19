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

### ~~[2026-02-15] Finalize Identity~~
**Status:** ✅ COMPLETED (2026-02-16)
**Outcome:** Identity finalized as Claw (daemon, 🐾). BOOTSTRAP.md deleted.

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

### [2026-02-18] Investigate Discord Delivery Failures
**Status:** pending
**Rationale:** Three cron jobs are failing with "cron announce delivery failed" error. Jobs execute but results don't reach Discord.
**Impact:** Token Limit Monitor, Critical API Alert Check, and Nightly Meditation results are not being delivered.
**Risk:** Medium — critical alerts could be missed.
**Proposed Investigation:**
1. Check Discord bot permissions in target channels
2. Verify channel IDs are correct in cron job configs
3. Test Discord API connectivity
4. Check if Discord rate limiting is occurring

### [2026-02-19] Fix Cron Job Timeouts
**Status:** pending
**Rationale:** Multiple lead gen and outreach cron jobs are timing out (5-10 min limits). Miami Hotels Wave 1/3, Expense Lead Gen affected.
**Impact:** Outreach campaigns not executing, leads not being generated.
**Risk:** Medium — lost business opportunities.
**Proposed Fix:**
1. Increase timeout for lead gen jobs from 300s to 600s
2. Or split large jobs into smaller batches
3. Consider staggering 9 AM jobs to reduce concurrent load

### [2026-02-19] Resolve zai/glm-5 Rate Limiting
**Status:** pending
**Rationale:** Deal Origination - Sellers job hit rate limit: "Provider zai is in cooldown (all profiles unavailable)"
**Impact:** Seller lead generation paused during rate limit windows.
**Risk:** Low — job will retry automatically.
**Proposed Fix:**
1. Stagger 9 AM jobs to reduce burst load
2. Consider fallback model for lead gen jobs
3. Monitor zai API usage patterns

---

*Last updated: 2026-02-18 02:15 EST*
*Pending actions: 3*
