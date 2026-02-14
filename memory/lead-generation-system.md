# Lead Generation System - Wellness 125 Cafeteria Plan

**Created:** 2026-02-13
**Status:** Active
**Cron Jobs:** 2 (Lead Generation + Outreach)

---

## System Overview

Automated B2B lead generation and outreach system targeting businesses with 20-500 employees for the Wellness 125 Cafeteria Plan.

### Email Configuration
- **From:** Zane@agentmail.to
- **CC:** sam@impactquadrant.info (on all emails)
- **AgentMail API:** Configured and ready

### Target Customer Profile
- **Company Size:** 20-500 employees
- **Industries:** Healthcare, Hospitality, Manufacturing, Transportation
- **Decision Makers:** CEO/Owner, HR Director, CFO, Benefits Manager

### Value Proposition
- **Employer:** $681/employee annual savings, 30-60% workers' comp reduction
- **Employee:** $50-$400/month take-home increase, free virtual healthcare
- **Implementation:** Zero cost, 30-60 days

---

## Components

### 1. Skill: Lead Generator
**Location:** `/workspace/skills/lead-generator/SKILL.md`

**Capabilities:**
- Lead identification and scoring
- Company enrichment
- Decision-maker finding
- Outreach sequence templates
- Pipeline tracking

**APIs Used:**
- Hunter.io (email finding)
- Abstract API (company enrichment)
- Zyte (web scraping - optional)

### 2. Script: Lead Generator
**Location:** `/workspace/scripts/lead-generator.py`

**Functions:**
- `search_companies()` - Find target companies
- `enrich_company()` - Get company data
- `find_decision_maker_email()` - Find contacts
- `score_lead()` - Score 0-100
- `calculate_potential_savings()` - Estimate value
- `save_daily_leads()` - Export results

### 3. Cron Jobs

**Daily Lead Generation**
- **ID:** `82ce5735-8a39-4cfe-bf13-f1b5c247eb47`
- **Schedule:** 9:00 AM EST, Monday-Friday
- **Target:** 15-20 leads/day
- **Output:** `/workspace/leads/daily-leads-YYYY-MM-DD.md`

**Lead Outreach**
- **ID:** `5cc16603-fbad-4105-9446-67721b5e11bd`
- **Schedule:** 2:00 PM EST, Monday-Friday
- **Action:** Queue personalized outreach
- **Output:** `/workspace/leads/pending-outreach.md`

---

## Lead Scoring System

### Score Criteria (0-100)

**Company Size (0-25 points)**
- 20-50 employees: 15 points
- 51-100 employees: 20 points
- 101-500 employees: 25 points

**Industry Fit (0-25 points)**
- Healthcare: 25 points
- Hospitality: 20 points
- Manufacturing: 20 points
- Transportation: 20 points

**Decision Maker Found (0-25 points)**
- CEO/Owner: 25 points
- HR Director: 20 points
- CFO: 20 points

**Contact Quality (0-25 points)**
- Email verified: 20 points
- Phone number: +5 points

### Priority Thresholds
- **High Priority:** 70-100 points
- **Medium Priority:** 50-69 points
- **Low Priority:** 30-49 points
- **Disqualify:** <30 points

---

## Outreach Sequence

### Day 1: Initial Email
- Subject: "$[amount] annual savings for [Company]"
- Personalized value prop
- CTA: 10-minute call

### Day 4: Follow-up #1
- Subject: "Re: $[amount] annual savings"
- Offer savings analysis
- Low commitment

### Day 7: Follow-up #2
- Subject: "Quick question about [Company] benefits"
- Social proof (case studies)
- Compliance credentials

### Day 14: Break-up
- Subject: "Last note re: [Company] savings"
- Keep door open
- No pressure

---

## File Structure

```
/workspace/
├── skills/
│   └── lead-generator/
│       └── SKILL.md                    # Lead gen skill
├── scripts/
│   └── lead-generator.py               # Automation script
└── leads/
    ├── daily-leads-YYYY-MM-DD.md       # Daily lead lists
    ├── pipeline.md                      # Active pipeline
    ├── pending-outreach.md              # Queued emails
    └── contacts.md                      # Contact database
```

---

## Metrics Tracking

### Daily
- New leads identified
- Leads enriched
- Emails queued
- High priority count

### Weekly
- Lead-to-response rate
- Average lead score
- Total pipeline value

### Monthly
- Meetings booked
- Proposals sent
- Deals closed
- Revenue generated

---

## Sample Lead

**Company:** Sunrise Senior Living - Phoenix
**Industry:** Healthcare - Senior Living
**Employees:** 85
**Score:** 85/100 (HIGH PRIORITY)

**Potential Savings:**
- FICA: $57,885
- Workers Comp: $12,750
- **Total: $70,635/year**

**Decision Maker:**
- Name: Sarah Johnson
- Title: HR Director
- Email: sjohnson@sunriseseniorliving.com

---

## Execution Plan

### Phase 1: Setup (Complete ✅)
- Skill created
- Script developed
- Cron jobs scheduled
- File structure built

### Phase 2: Daily Operations
- 9 AM: Generate 15-20 leads
- 2 PM: Queue outreach for high-priority leads
- 5 PM: Update pipeline, track metrics

### Phase 3: Optimization (Ongoing)
- A/B test subject lines
- Track response rates by industry
- Refine scoring algorithm
- Improve targeting

---

## Safety Protocols

- **No automatic email sending** - All outreach queued for human review
- **CAN-SPAM compliant** - Unsubscribe option in all emails
- **Consent tracking** - Log all opt-outs
- **Data privacy** - Secure API key storage

---

## Next Steps

1. **Monitor first week** - Track lead quality and response rates
2. **Refine targeting** - Adjust industry focus based on results
3. **Add automation** - Integrate with actual email sending (with approval)
4. **Scale up** - Increase lead volume once system proven

---

*System operational and ready for daily execution.*
