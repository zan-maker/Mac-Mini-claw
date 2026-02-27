# API Usage Monitoring Configuration

**Purpose:** Daily monitoring of API token usage and budget alerts

---

## Monitored APIs

| Provider | Models | Use Case | Est. Cost/1M Tokens |
|----------|--------|----------|---------------------|
| **Z.AI** | GLM-5, GLM-4.7 variants | Primary daily driver | $0.40 input / $1.50 output |
| **xAI** | Grok-4, Grok-2 | Deep research | ~$2.00 input / ~$10.00 output |

---

## Monitoring Setup

### Scripts

**`api-monitor.sh`** — Main monitoring script
- Tracks daily token usage
- Calculates costs based on pricing
- Updates monthly usage totals
- Generates alerts at threshold levels

**`api-usage.json`** — Usage tracking database
- Stores monthly usage totals
- Tracks budget allocation
- Records last check timestamp

---

## Alert Thresholds

| Level | Threshold | Action |
|-------|-----------|--------|
| ✅ **Healthy** | >20% budget remaining | No action |
| ⚠️ **Low** | 10-20% budget remaining | Daily reminder to top up |
| 🚨 **Critical** | <10% budget remaining | Immediate alert every 12 hours |

---

## Cron Jobs

### 1. Daily API Usage Check
**ID:** `a6c94247-c668-4d17-ba7e-ddbbea2b1b26`
**Schedule:** Every 24 hours
**Actions:**
- Run `api-monitor.sh`
- Check for alert files
- Send Discord notification with status
- Delete alert files after sending

### 2. Critical API Alert Check
**ID:** [created above]
**Schedule:** Every 12 hours
**Actions:**
- Check for critical alert file
- If exists, send URGENT Discord message
- Delete file after sending
- If no critical alerts, do nothing (NO_REPLY)

---

## Monthly Budget

**Current Setting:** $50 USD/month

**To adjust:**
Edit `api-monitor.sh` and change:
```bash
MONTHLY_BUDGET=50  # Change this value
```

---

## Usage Tracking

**File:** `~/.openclaw/workspace/api-usage.json`

**Structure:**
```json
{
  "monthly": {
    "2026-02": {
      "zai_tokens": {"input": 0, "output": 0},
      "xai_tokens": {"input": 0, "output": 0},
      "cost_usd": 0
    }
  },
  "budget": 50,
  "last_check": "2026-02-13"
}
```

---

## Manual Check

**To manually run usage check:**
```bash
~/.openclaw/workspace/api-monitor.sh
```

**To view current usage:**
```bash
cat ~/.openclaw/workspace/api-usage.json
```

**To view alert history:**
```bash
cat ~/.openclaw/workspace/api-alerts.log
```

---

## Alert Format

### Low Budget Warning
```
⚠️ WARNING: API budget at XX% ($YY.YY spent of $ZZ). 
Consider topping up soon.
```

### Critical Budget Alert
```
🚨 CRITICAL: API budget at XX% ($YY.YY spent of $ZZ). 
Top up immediately!
```

---

## How It Works

1. **Daily Check (24h):**
   - Runs `api-monitor.sh`
   - Estimates token usage from session activity
   - Calculates costs against budget
   - Generates alert files if thresholds crossed
   - Sends status to Discord

2. **Critical Check (12h):**
   - Monitors for critical alerts
   - Sends immediate notification if budget critical
   - Ensures you don't miss urgent top-ups

3. **Tracking:**
   - All usage stored in `api-usage.json`
   - Monthly totals rolled over each month
   - Historical data preserved for analysis

---

## Important Notes

⚠️ **Usage Estimation:** Currently uses estimated daily usage. For exact tracking, would need:
- OpenAI API usage endpoints (if available)
- Provider-specific billing APIs
- Direct integration with OpenClaw session tracking

💡 **To Improve Accuracy:**
- Update pricing in `api-monitor.sh` to match actual plan
- Add provider-specific balance checking if APIs available
- Integrate with actual OpenClaw session status

---

## Provider Balance Check (Manual)

**Z.AI:**
- Dashboard: https://open.bigmodel.cn
- Check: Account balance and usage

**xAI:**
- Dashboard: https://console.x.ai
- Check: API usage and billing

---

**Version:** 1.0
**Created:** 2026-02-13
**Next Steps:** Verify actual API pricing and integrate provider balance APIs if available
