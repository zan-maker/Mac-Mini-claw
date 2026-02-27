# Craigslist Referral Fee System - Cron Jobs

## Overview
Two daily cron jobs to find and process referral fee opportunities from Craigslist:

1. **Morning Scraper** (9:00 AM): Finds business-for-sale and service business opportunities
2. **Afternoon Processor** (2:00 PM): Processes leads and initiates outreach

## Revenue Streams

### 1. Business-for-Sale Referral Fees (Idea 1)
- **Target:** `biz` category listings
- **Fee:** 1% of business sale price
- **Range:** $5,000 - $50,000 per deal
- **Action:** Connect sellers with buyers from investor database

### 2. Service Business Expense Reduction (Idea 3)
- **Target:** `sks`, `cps`, `lbs` categories
- **Fee:** 15% of first-year savings
- **Range:** $1,000 - $10,000 per client
- **Action:** Pitch expense reduction services

## Cron Job Configuration

### Job 1: Daily Craigslist Scraper
- **Schedule:** 9:00 AM daily
- **Model:** zai/glm-5 (needs large context for analysis)
- **Task:** Run scraper, identify opportunities, save to database
- **Output:** JSON files + Discord report

### Job 2: Lead Processing & Outreach
- **Schedule:** 2:00 PM daily  
- **Model:** deepseek (routine tasks)
- **Task:** Process scraped leads, initiate outreach via AgentMail
- **Output:** Emails sent, follow-up scheduled

## File Structure

```
/Users/cubiczan/.openclaw/workspace/
├── scripts/
│   ├── craigslist_daily_scraper.py    # Main scraper
│   ├── run_craigslist_scraper.sh      # Shell wrapper
│   └── process_craigslist_leads.py    # Lead processor (to be created)
├── craigslist-leads/                  # Output directory
│   ├── daily_leads_YYYY-MM-DD.json    # Raw leads
│   ├── daily_summary_YYYY-MM-DD.json  # Summary
│   └── discord_report_YYYY-MM-DD.txt  # Discord report
└── craigslist-env/                    # Virtual environment
```

## Expected Output

### Daily Report Format (Discord):
```
📊 Daily Craigslist Referral Fee Report
2026-02-27

Total Opportunities: 42
Total Estimated Fees: $187,500
Avg Fee/Opportunity: $4,464

🏢 Business-for-Sale: 18 leads ($112,500)
🔧 Service Businesses: 24 leads ($75,000)

🎯 Top Opportunities:
1. $25,000 - Established Restaurant for Sale... (NYC, Biz Sale)
2. $18,000 - Commercial Cleaning Business... (LA, Service)
3. $15,000 - IT Consulting Firm for Sale... (Chicago, Biz Sale)
```

## Setup Instructions

1. **Virtual Environment:** Already created at `craigslist-env/`
2. **Dependencies:** Installed (craigslistscraper, beautifulsoup4, requests, pandas)
3. **Output Directory:** Created at `craigslist-leads/`
4. **Cron Jobs:** To be configured via OpenClaw

## Testing

Test the scraper manually:
```bash
cd /Users/cubiczan/.openclaw/workspace
./scripts/run_craigslist_scraper.sh
```

## Next Steps

1. Create lead processor script
2. Configure cron jobs in OpenClaw
3. Set up AgentMail integration for outreach
4. Add Supabase storage for lead tracking
5. Create dashboard for monitoring

## Revenue Projections

| Metric | Conservative | Realistic | Optimistic |
|--------|--------------|-----------|------------|
| Leads/Day | 20 | 50 | 100 |
| Conversion Rate | 2% | 5% | 10% |
| Avg Fee/Deal | $2,500 | $5,000 | $10,000 |
| **Monthly Revenue** | **$30,000** | **$375,000** | **$3,000,000** |

*Based on 30-day month, 2 cities initially, scaling to 10 cities*
