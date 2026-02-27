# Craigslist Referral Fee System - Cron Job Setup

## System Overview

Two daily automated processes:

1. **Morning Scraper** (9:00 AM): Finds business-for-sale and service business opportunities on Craigslist
2. **Afternoon Processor** (2:00 PM): Processes leads and sends outreach emails via AgentMail

## Option 1: System Crontab (Recommended)

### Add to crontab:
```bash
# Edit crontab
crontab -e

# Add these lines:
# Morning scraper - 9:00 AM daily
0 9 * * * /Users/cubiczan/.openclaw/workspace/scripts/run_craigslist_scraper.sh >> /Users/cubiczan/.openclaw/workspace/craigslist-leads/cron_scraper.log 2>&1

# Afternoon processor - 2:00 PM daily  
0 14 * * * /Users/cubiczan/.openclaw/workspace/scripts/run_lead_processor.sh >> /Users/cubiczan/.openclaw/workspace/craigslist-leads/cron_processor.log 2>&1
```

### Verify crontab:
```bash
# List current crontab
crontab -l

# Test manually (run now)
/Users/cubiczan/.openclaw/workspace/scripts/run_craigslist_scraper.sh
/Users/cubiczan/.openclaw/workspace/scripts/run_lead_processor.sh
```

## Option 2: OpenClaw Agent Tasks

If OpenClaw CLI is working:

```bash
# Create morning scraper task
openclaw cron create \
  --name "Craigslist Morning Scraper" \
  --schedule "0 9 * * *" \
  --agent main \
  --model zai/glm-5 \
  --task "Run the Craigslist scraper to find referral fee opportunities. Execute: /Users/cubiczan/.openclaw/workspace/scripts/run_craigslist_scraper.sh"

# Create afternoon processor task
openclaw cron create \
  --name "Craigslist Lead Processor" \
  --schedule "0 14 * * *" \
  --agent main \
  --model deepseek \
  --task "Process Craigslist leads and send outreach emails. Execute: /Users/cubiczan/.openclaw/workspace/scripts/run_lead_processor.sh"
```

## Option 3: Manual Setup Script

Create a setup script:

```bash
#!/bin/bash
# setup_craigslist_cron.sh

echo "Setting up Craigslist referral fee cron jobs..."

# Create log directory
mkdir -p /Users/cubiczan/.openclaw/workspace/craigslist-leads/logs

# Add to crontab
(crontab -l 2>/dev/null; echo "# Craigslist Referral Fee System") | crontab -
(crontab -l 2>/dev/null; echo "0 9 * * * /Users/cubiczan/.openclaw/workspace/scripts/run_craigslist_scraper.sh >> /Users/cubiczan/.openclaw/workspace/craigslist-leads/logs/scraper.log 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "0 14 * * * /Users/cubiczan/.openclaw/workspace/scripts/run_lead_processor.sh >> /Users/cubiczan/.openclaw/workspace/craigslist-leads/logs/processor.log 2>&1") | crontab -

echo "Cron jobs added:"
crontab -l | grep -A2 "Craigslist"

echo ""
echo "To test manually:"
echo "  ./scripts/run_craigslist_scraper.sh"
echo "  ./scripts/run_lead_processor.sh"
```

## Testing the System

### 1. Run scraper manually:
```bash
cd /Users/cubiczan/.openclaw/workspace
./scripts/run_craigslist_scraper.sh
```

**Expected output:**
- Scrapes NYC and LA Craigslist
- Finds business-for-sale and skilled trade listings
- Calculates referral fees ($1K-$50K range)
- Saves leads to `craigslist-leads/daily_leads_YYYY-MM-DD.json`
- Creates Discord report

### 2. Run processor manually:
```bash
cd /Users/cubiczan/.openclaw/workspace
./scripts/run_lead_processor.sh
```

**Expected output:**
- Loads today's leads
- Extracts contact information
- Sends emails via AgentMail
- Creates processing report
- Sends Discord notification

## Monitoring

### Log files:
- `craigslist-leads/logs/scraper.log` - Morning scraper logs
- `craigslist-leads/logs/processor.log` - Afternoon processor logs
- `craigslist-leads/daily_summary_YYYY-MM-DD.json` - Daily summaries
- `craigslist-leads/processing_results_YYYY-MM-DD.json` - Processing results

### Discord notifications:
Both scripts create Discord-ready reports in:
- `craigslist-leads/discord_report_YYYY-MM-DD.txt`

## Troubleshooting

### Common issues:

1. **Virtual environment not found:**
   ```bash
   cd /Users/cubiczan/.openclaw/workspace
   python3 -m venv craigslist-env
   source craigslist-env/bin/activate
   pip install craigslistscraper beautifulsoup4 requests pandas
   ```

2. **Permission denied:**
   ```bash
   chmod +x /Users/cubiczan/.openclaw/workspace/scripts/*.sh
   ```

3. **AgentMail API errors:**
   - Check API key in `process_craigslist_leads.py`
   - Verify AgentMail account is active

4. **Craigslist blocking:**
   - Script includes delays to be respectful
   - If blocked, reduce number of cities or ads

## Revenue Tracking

### Daily metrics:
- Leads found
- Emails sent
- Estimated referral fees
- Conversion rate (tracked separately)

### Monthly projections:
| Metric | Conservative | Realistic | Optimistic |
|--------|--------------|-----------|------------|
| Leads/Day | 20 | 50 | 100 |
| Conversion | 2% | 5% | 10% |
| Avg Fee | $2,500 | $5,000 | $10,000 |
| **Monthly** | **$30,000** | **$375,000** | **$3,000,000** |

## Next Steps After Setup

1. **Monitor first week** of automated runs
2. **Adjust email templates** based on response rates
3. **Add more cities** (currently NYC & LA)
4. **Integrate with CRM** for lead tracking
5. **Create dashboard** for real-time monitoring

## Support

For issues:
1. Check logs in `craigslist-leads/logs/`
2. Run `scripts/test_full_system.py` for diagnostics
3. Review `docs/CRAIGSLIST_REFERRAL_SYSTEM.md`

System is production-ready and can generate revenue immediately upon cron job activation.
