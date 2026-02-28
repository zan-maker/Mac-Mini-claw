# Cron Job Management - Disable & Repurpose

**Date:** 2026-02-28
**Request:** Disable failing Dorada cron job and repurpose Mining analyst

---

## Cron Jobs to Modify

### 1. Dorada Outreach Cron Job (DISABLE)
**Issue:** Execution failed with SIGTERM (2026-02-28 06:55:38 EST)
**Job ID:** Unknown (one of Dorada Waves 1-6)
**Schedule:** 10:00 AM daily
**Action:** **DISABLE** the failing Dorada cron job

### 2. Mining Lead Gen Cron Job (REPURPOSE)
**Current:** Mining Lead Gen (9:30 AM daily)
**Script:** `scripts/mining-lead-gen.py`
**Output:** `mining-leads/daily-mining-leads-YYYY-MM-DD.md`
**Action:** **REPURPOSE** for new use case

---

## Recommended Actions

### A. Disable Dorada Cron Job
1. Identify which Dorada wave is failing (check logs for "quiet-bl")
2. Run: `openclaw cron disable <job_id>`
3. Or delete from cron configuration

### B. Repurpose Mining Analyst
**Current Purpose:** High-grade mining project sourcing
- Targets: >10g/t Au, >3% Cu projects
- Sources: CPC/ASX companies, JV opportunities
- Output: Daily mining leads report

**Repurpose Options:**

#### Option 1: Enhanced Expense Reduction Lead Gen
- **Use:** Expand expense reduction outreach
- **Schedule:** Keep 9:30 AM daily
- **Target:** Additional 10-15 companies/day
- **Integration:** Use existing AgentMail + Tavily workflow

#### Option 2: Defense Sector Outreach
- **Use:** Defense contractor expense reduction
- **Target:** Defense contractors (20+ employees)
- **Value Prop:** 15-25% OPEX reduction
- **Sources:** SAM.gov, defense contractor databases

#### Option 3: Healthcare Provider Outreach
- **Use:** Medical practice expense reduction
- **Target:** Medical practices, clinics, hospitals
- **Value Prop:** 20-30% savings on medical supplies, telecom, waste
- **Sources:** CMS data, medical directories

#### Option 4: Real Estate Investor Outreach
- **Use:** Real estate investor expense reduction
- **Target:** Property managers, REITs, multifamily owners
- **Value Prop:** 15-25% savings on utilities, maintenance, insurance
- **Sources:** CoStar, real estate databases

---

## Implementation Steps

### Step 1: Identify & Disable Failing Cron Job
```bash
# List all cron jobs
openclaw cron list

# Find the Dorada job with issues (look for "quiet-bl" or recent failures)
# Disable it
openclaw cron disable <job_id>
```

### Step 2: Repurpose Mining Analyst
```bash
# 1. Backup current mining script
cp scripts/mining-lead-gen.py scripts/mining-lead-gen-backup.py

# 2. Choose repurpose option and create new script
# Example: Enhanced Expense Reduction
cp scripts/expense-reduction-agentmail.py scripts/enhanced-expense-reduction.py

# 3. Update cron job configuration
openclaw cron update <mining_job_id> --script scripts/enhanced-expense-reduction.py
```

### Step 3: Update Documentation
- Update MEMORY.md cron job registry
- Document changes in memory/2026-02-28.md
- Update skill documentation if needed

---

## Quick Fix (If Job ID Unknown)

If you can't identify the specific failing Dorada job, consider:

1. **Disable all Dorada waves temporarily:**
   ```bash
   # Disable Waves 1-6
   openclaw cron disable <dorada_wave1_id>
   openclaw cron disable <dorada_wave2_id>
   # ... etc
   ```

2. **Enable one at a time** to identify which is failing

3. **Keep only working waves** enabled

---

## Impact Assessment

### Before Changes:
- **Dorada Outreach:** 6 waves (60+ investors)
- **Mining Analyst:** 5-10 mining leads/day
- **Total Active Cron Jobs:** 31

### After Changes:
- **Dorada Outreach:** 5 waves (disable failing one)
- **Mining Repurposed:** New outreach channel
- **Total Active Cron Jobs:** 31 (replaced, not reduced)

---

## Recommended Choice: Option 1 (Enhanced Expense Reduction)

**Why:**
- Leverages existing successful workflow
- Uses proven Tavily + AgentMail integration
- Expands highest-performing campaign
- Immediate ROI potential

**New Script:** `scripts/enhanced-expense-reduction.py`
**Schedule:** 9:30 AM daily (same as mining)
**Target:** Additional 10-15 companies/day
**Integration:** Supabase + Tavily + AgentMail

---

**Next Steps:**
1. Identify failing Dorada job ID
2. Disable it via `openclaw cron disable`
3. Choose repurpose option for Mining analyst
4. Update scripts and cron configuration
5. Test new workflow
