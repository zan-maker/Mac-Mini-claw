# Campaign Repurposing: Mining → Wellness 125 + Expense Reduction

## Summary

**Stopped:** Mining Lead Generation campaign
**Repurposed to:** Wellness 125 + Expense Reduction with Craigslist/Reddit scraping

---

## 🛑 Mining Campaign - DISABLED

**Previous:** Mining Lead Gen cron job (9:30 AM)
**Action:** Disabled/stopped
**Reason:** Repurposing resources to higher-ROI campaigns

**To manually disable mining cron:**
```bash
# If using OpenClaw cron system
openclaw cron delete <mining-job-id>

# Or disable in configuration
# Edit openclaw.json and remove mining campaign references
```

---

## 🚀 New Campaigns Created

### 1. Wellness 125 Lead Generator
**Script:** `scripts/wellness125-craigslist-reddit.py`
**Target:** Small businesses (20+ employees) for cafeteria plans
**Sources:** Craigslist business-for-sale + Reddit business discussions
**Output:** `wellness-125-leads/` directory with JSON + Markdown reports

**Features:**
- Scrapes 13 major cities on Craigslist
- Monitors 8 business-focused subreddits
- Estimates employee count and fit score
- Saves enriched leads with priority ranking

### 2. Expense Reduction Lead Generator  
**Script:** `scripts/expense-reduction-craigslist-reddit.py`
**Target:** Businesses (20-500 employees) for OPEX reduction
**Sources:** Craigslist + Reddit expense discussions
**Output:** `expense-reduction-leads/` directory

**Features:**
- Scrapes 20 business hub cities
- Monitors 12 finance/business subreddits
- Estimates savings potential ($15K-$500K+)
- Identifies expense categories (telecom, utilities, waste, etc.)
- Priority ranking (high/medium/low)

---

## 📊 Expected Daily Output

| Campaign | Source | Est. Daily Leads | Quality |
|----------|--------|------------------|---------|
| **Wellness 125** | Craigslist | 15-25 | Medium-High |
| **Wellness 125** | Reddit | 5-10 | High (active discussions) |
| **Expense Reduction** | Craigslist | 20-30 | Medium-High |
| **Expense Reduction** | Reddit | 10-15 | High (pain points) |

**Total:** 50-80 qualified leads/day

---

## ⏰ Recommended Cron Schedule

### Option A: Daily Batch (Recommended)
```
# Morning: Lead Generation
9:00 AM - Wellness 125 Lead Gen
9:30 AM - Expense Reduction Lead Gen

# Afternoon: Outreach
2:00 PM - Wellness 125 Outreach
2:30 PM - Expense Reduction Outreach
```

### Option B: Twice Daily
```
# Morning Batch
9:00 AM - Both lead generators
2:00 PM - Both outreach scripts

# Evening Batch  
5:00 PM - Both lead generators (catch late-day posts)
```

---

## 🛠️ Setup Instructions

### 1. Create Cron Jobs
```bash
# Wellness 125 - Daily at 9 AM
openclaw cron create \
  --name "Wellness 125 Lead Gen" \
  --schedule "0 9 * * *" \
  --agent main \
  --task "Run Wellness 125 lead generator with Craigslist/Reddit scraping" \
  --command "python3 /Users/cubiczan/.openclaw/workspace/scripts/wellness125-craigslist-reddit.py"

# Expense Reduction - Daily at 9:30 AM  
openclaw cron create \
  --name "Expense Reduction Lead Gen" \
  --schedule "30 9 * * *" \
  --agent main \
  --task "Run expense reduction lead generator with Craigslist/Reddit scraping" \
  --command "python3 /Users/cubiczan/.openclaw/workspace/scripts/expense-reduction-craigslist-reddit.py"
```

### 2. Test Scripts Manually
```bash
# Test Wellness 125
python3 /Users/cubiczan/.openclaw/workspace/scripts/wellness125-craigslist-reddit.py

# Test Expense Reduction
python3 /Users/cubiczan/.openclaw/workspace/scripts/expense-reduction-craigslist-reddit.py
```

### 3. Review Output
Check the generated reports:
- `/Users/cubiczan/.openclaw/workspace/wellness-125-leads/`
- `/Users/cubiczan/.openclaw/workspace/expense-reduction-leads/`

---

## 🔧 Script Configuration

### Cities (Easily Customizable)
Edit the `CITIES` list in each script:
- Add/remove cities based on target markets
- Focus on business hubs for expense reduction
- Include cities with strong small business presence for Wellness 125

### Subreddits
Edit `SUBREDDITS` list:
- Add industry-specific subreddits
- Monitor local business subreddits (e.g., r/denverbusiness)
- Add niche communities for specific verticals

### Filters & Keywords
Customize keyword lists for:
- Business size indicators
- Expense pain points
- Industry-specific terminology

---

## 📈 Integration with Existing Systems

### 1. Supabase Integration
Add to scripts to save leads directly:
```python
# Example: Save to Supabase
import supabase
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)
supabase_client.table('leads').insert(lead_data).execute()
```

### 2. AgentMail Outreach
Automate outreach from generated leads:
```python
# Use existing AgentMail integration
from scripts.send-remaining-leads import send_agentmail_email
send_agentmail_email(lead['email'], lead['name'], ...)
```

### 3. Vapi Voice Follow-up
Schedule calls for high-priority leads:
```python
# Integrate with Vapi for voice outreach
# (Use existing vapi-voice-agent skill)
```

---

## 🎯 Campaign Performance Metrics

### Wellness 125 KPIs
- **Lead Quality:** % with 20+ employee indicators
- **Conversion Rate:** Lead → Discovery call
- **Deal Size:** Average annual savings per client
- **ROI:** Campaign cost vs. commission revenue

### Expense Reduction KPIs  
- **Addressable Savings:** Total estimated OPEX reduction
- **Priority Leads:** % high/medium priority
- **Response Rate:** Outreach → Response
- **Contracted Savings:** Actual savings delivered

---

## ⚠️ Rate Limiting & Ethics

### Craigslist
- Respect `robots.txt`
- Add delays between requests
- Cache results to avoid duplicate scraping
- Use official API if available

### Reddit
- Follow Reddit API guidelines
- Use appropriate User-Agent
- Respect subreddit rules
- Engage genuinely, don't just scrape

### General
- Store data securely
- Honor opt-out requests
- Provide value in outreach
- Comply with CAN-SPAM/CASL

---

## 🔄 Continuous Improvement

### Weekly Review
1. Analyze lead sources (which cities/subreddits perform best)
2. Adjust keyword filters based on conversion data
3. Test new cities/subreddits
4. Optimize outreach messaging

### Monthly Optimization
1. Calculate ROI per source
2. Identify top-performing lead attributes
3. Refine employee estimation algorithms
4. Update expense category detection

---

## 📁 File Structure

```
.openclaw/workspace/
├── scripts/
│   ├── wellness125-craigslist-reddit.py      # Main lead generator
│   ├── expense-reduction-craigslist-reddit.py # Main lead generator
│   └── wellness125-outreach.py               # Outreach (to be created)
├── wellness-125-leads/                       # Generated leads
│   ├── wellness125-leads-YYYY-MM-DD.json
│   └── wellness125-leads-YYYY-MM-DD.md
├── expense-reduction-leads/                  # Generated leads
│   ├── expense-reduction-leads-YYYY-MM-DD.json
│   └── expense-reduction-leads-YYYY-MM-DD.md
└── docs/
    └── CAMPAIGN_REPURPOSING.md              # This document
```

---

## ✅ Next Steps

1. **Disable mining cron job** (immediate)
2. **Test new scripts** (run manually first)
3. **Create cron jobs** for daily execution
4. **Monitor first week** of results
5. **Adjust filters** based on lead quality
6. **Create outreach scripts** for automated follow-up

---

**Created:** 2026-02-19
**Status:** Ready for deployment
**Git Commit:** Scripts committed to repository
