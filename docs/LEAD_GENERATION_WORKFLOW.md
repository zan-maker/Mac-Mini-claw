# Lead Generation System Workflow

## Overview
Unified workflow for all lead generation activities with proper error handling and monitoring.

## Daily Workflow

### 1. Master Workflow Script
**Script:** `scripts/master-lead-workflow.py`
**Schedule:** Daily at 9:00 AM
**Purpose:** Runs all lead generation steps sequentially

### 2. Workflow Steps
1. **Enhanced Lead Gen v2** (`lead-generator.py`)
   - Target: Wellness 125 Cafeteria Plan
   - Companies: 20+ employees
   - Sources: Abstract API, Hunter.io

2. **Expense Reduction Lead Gen** (`expense-reduction-lead-gen.py`)
   - Target: 20-500 employee companies
   - Value prop: 15-30% OPEX reduction
   - Sources: Tavily, Serper

3. **Deal Origination - Sellers** (`seller-lead-gen.py`)
   - Target: Off-market business sellers
   - Volume: 10-15/day
   - Focus: $500K-$3M EBITDA

4. **Deal Origination - Buyers** (`buyer-lead-gen.py`)
   - Target: PE firms with finder fee agreements
   - Volume: 3-4/day
   - Focus: Platform ($2M-$10M+ EBITDA)

5. **B2B Referral Engine**
   - Prospects: 10-15/day (demand side)
   - Providers: 3-4/day (service providers)
   - Verticals: Accounting, Legal, SaaS, Construction, CRE

6. **Lead Outreach** (`send-remaining-leads.sh`)
   - Method: AgentMail API
   - Timing: 2:00 PM daily
   - Follow-up: Sam Desigan (sam@impactquadrant.info)

7. **Expense Reduction Outreach**
   - Method: AgentMail API
   - Timing: 2:00 PM daily
   - Signature: "Agent Manager" + Sam Desigan contact

## API Configuration

### Environment Variables
All API keys stored in `.env` file:
- `HUNTER_IO_API_KEY`: Email enrichment
- `TAVILY_API_KEY`: Web search (alternative to Brave)
- `ABSTRACT_API_KEY`: Company data
- `SERPER_API_KEY`: Google search
- `AGENTMAIL_API_KEY`: Email sending
- `ZEROBOUNCE_API_KEY`: Email validation

### Rate Limits
- **Abstract API:** 1 request/second
- **Hunter.io:** 2000 credits/month
- **Tavily:** Varies by plan
- **AgentMail:** Check account limits

## Monitoring & Maintenance

### Daily Checks
1. **API Credits:** Monitor Hunter.io, ZeroBounce credits
2. **Script Outputs:** Check `outreach-results/` directory
3. **Error Logs:** Review workflow logs

### Weekly Maintenance (Sundays 2 AM)
1. **Diagnostics:** Run `diagnose-lead-system.py`
2. **Cleanup:** Archive old results
3. **Updates:** Check for script updates

### Monthly Tasks
1. **API Key Rotation:** Update expired keys
2. **Performance Review:** Analyze conversion rates
3. **Workflow Optimization:** Adjust search queries, thresholds

## Troubleshooting

### Common Issues

#### 1. API Rate Limits
**Symptoms:** Scripts failing with timeout or 429 errors
**Fix:** Implement rate limiting, switch to alternative APIs

#### 2. Missing Environment Variables
**Symptoms:** "API key not found" errors
**Fix:** Ensure `.env` file is sourced before running scripts

#### 3. Cron Job Failures
**Symptoms:** Jobs not running or timing out
**Fix:** Check OpenClaw cron configuration, increase timeouts

#### 4. Email Delivery Issues
**Symptoms:** Emails not sending, bouncebacks
**Fix:** Verify AgentMail API key, check email templates

### Diagnostic Tools
- `scripts/diagnose-lead-system.py`: Comprehensive system check
- `scripts/master-lead-workflow.py`: Unified workflow with logging
- `scripts/lead-system-maintenance.py`: Automated fixes

## Performance Metrics

### Key Metrics to Track
- **Leads Generated/Day:** Target 50-70
- **Email Send Rate:** Target 95%+ success
- **Response Rate:** Track for optimization
- **Cost/Lead:** Monitor API usage costs

### Reporting
- **Daily:** Workflow completion status
- **Weekly:** Performance summary
- **Monthly:** ROI analysis

## Version History

### 2026-03-04: Unified Workflow Implementation
- Created master workflow script
- Fixed environment variable configuration
- Disabled completed campaign cron jobs
- Created enhanced expense reduction script
- Added comprehensive documentation

---

**Last Updated:** 2026-03-04
**Status:** ✅ Operational
