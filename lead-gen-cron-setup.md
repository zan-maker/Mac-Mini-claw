# Lead Gen Cron Jobs - Setup Guide

**Issue Fixed:** Lead gen scripts were failing due to missing Python dependencies (requests module not found).

**Solution:** Created a wrapper script that activates the virtual environment before running each script.

---

## Fixed Files

1. **Wrapper Script:** `/Users/cubiczan/.openclaw/workspace/scripts/run-lead-gen.sh`
   - Activates the correct Python virtual environment
   - Runs lead gen scripts with proper environment
   - Logs output to `/Users/cubiczan/.openclaw/workspace/logs/lead-gen.log`

---

## Running Lead Gen Jobs Manually

```bash
# Run ALL lead gen scripts
~/.openclaw/workspace/scripts/run-lead-gen.sh

# Run a specific script
~/.openclaw/workspace/scripts/run-lead-gen.sh expense-reduction-lead-gen.py
~/.openclaw/workspace/scripts/run-lead-gen.sh buyer-lead-gen.py
~/.openclaw/workspace/scripts/run-lead-gen.sh seller-lead-gen.py
~/.openclaw/workspace/scripts/run-lead-gen.sh referral-engine-prospects.py
~/.openclaw/workspace/scripts/run-lead-gen.sh referral-engine-providers.py
```

---

## System Cron Setup (Alternative)

If OpenClaw's internal scheduler isn't working, you can set up system cron:

```bash
# Edit crontab
crontab -e

# Add these lines:
# Lead Gen - 9 AM weekdays
0 9 * * 1-5 /Users/cubiczan/.openclaw/workspace/scripts/run-lead-gen.sh >> /Users/cubiczan/.openclaw/workspace/logs/cron.log 2>&1

# Or run individual scripts at different times:
0 9 * * 1-5 /Users/cubiczan/.openclaw/workspace/scripts/run-lead-gen.sh expense-reduction-lead-gen.py >> /Users/cubiczan/.openclaw/workspace/logs/cron.log 2>&1
5 9 * * 1-5 /Users/cubiczan/.openclaw/workspace/scripts/run-lead-gen.sh buyer-lead-gen.py >> /Users/cubiczan/.openclaw/workspace/logs/cron.log 2>&1
10 9 * * 1-5 /Users/cubiczan/.openclaw/workspace/scripts/run-lead-gen.sh seller-lead-gen.py >> /Users/cubiczan/.openclaw/workspace/logs/cron.log 2>&1
15 9 * * 1-5 /Users/cubiczan/.openclaw/workspace/scripts/run-lead-gen.sh referral-engine-prospects.py >> /Users/cubiczan/.openclaw/workspace/logs/cron.log 2>&1
20 9 * * 1-5 /Users/cubiczan/.openclaw/workspace/scripts/run-lead-gen.sh referral-engine-providers.py >> /Users/cubiczan/.openclaw/workspace/logs/cron.log 2>&1
```

---

## Today's Lead Gen Results (Feb 18, 2026)

| Script | Status | Leads Generated | High Priority |
|--------|--------|-----------------|---------------|
| expense-reduction-lead-gen.py | ✅ | 5 | 4 |
| buyer-lead-gen.py | ✅ | 8 | 3 |
| seller-lead-gen.py | ✅ | 12 | 10 |
| referral-engine-prospects.py | ✅ | 12 | 9 |
| **TOTAL** | ✅ | **37** | **26** |

**Total Potential Value:** $5.3M+ in finder fees/savings

---

## Output Files

- `/Users/cubiczan/.openclaw/workspace/expense-leads/daily-leads-2026-02-18.md`
- `/Users/cubiczan/.openclaw/workspace/deals/buyers/daily-buyers-2026-02-18.md`
- `/Users/cubiczan/.openclaw/workspace/deals/sellers/daily-sellers-2026-02-18.md`
- `/Users/cubiczan/.openclaw/workspace/referral-engine/prospects/daily-prospects-2026-02-18.md`

---

*Updated: 2026-02-18 19:11 EST*
