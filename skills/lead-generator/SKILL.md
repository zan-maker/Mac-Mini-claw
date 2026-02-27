---
name: lead-generator
description: "B2B lead generation and outreach automation for Wellness 125 Cafeteria Plan. Identifies small to mid-sized businesses (20+ employees), enriches company data, finds decision-maker contacts, and manages outreach sequences. Use for: (1) daily lead identification, (2) company enrichment, (3) email finding, (4) outreach automation, (5) lead scoring and qualification."
---

# Lead Generator - Wellness 125 Cafeteria Plan

Automated B2B lead generation system targeting businesses with 20+ employees for the Wellness 125 Cafeteria Plan.

## Target Customer Profile

### Ideal Customer (20+ employees)
- Healthcare organizations (hospice, senior living, medical transport)
- Hospitality (hotels, restaurants, franchises)
- Manufacturing facilities
- Transportation companies
- Multi-location franchises
- Professional services firms

### Target Decision Makers
- CEO/Owner (companies <50 employees)
- HR Director/Manager
- CFO/Controller
- Benefits Manager
- Operations Director

## Value Proposition

**Employer Benefits:**
- Save $681/year per enrolled employee (FICA)
- 30-60% workers' comp premium reduction
- Zero cost to implement
- 30-60 day implementation

**Employee Benefits:**
- $50-$400/month take-home pay increase
- Free virtual healthcare (24/7)
- Free generic medications
- Dental discounts up to 60%

## Data Sources

### Hunter.io (Email Finding)
- **API Key:** `f701d171cf7decf7e730a6b1c6e9b74f29f39b6e`
- **Base URL:** `https://api.hunter.io/v2/`
- **Usage:** Find decision-maker emails

### Abstract API (Company Enrichment)
- **API Key:** `38aeec02e6f6469983e0856dfd147b10`
- **Base URL:** `https://companyenrichment.abstractapi.com/v1/`
- **Usage:** Get company data (size, revenue, industry)

### Zyte (Web Scraping)
- **API Key:** `8d3e9c7af6e948b088e96ad15ca21719`
- **Usage:** Scrape business directories, company websites

## Lead Sources

### Primary Sources
1. **LinkedIn** - Company pages, employee counts
2. **Google Maps** - Business listings by location
3. **Industry Directories:**
   - Healthcare: Definitive Healthcare, Healthgrades
   - Hospitality: Hotel Management, Restaurant Business
   - Manufacturing: ThomasNet, MFG.com
   - Transportation: Transport Topics, FleetOwner

### Search Patterns
```
"company name" + "20 employees" + industry
"company name" + "50 employees" + healthcare
"company name" + site:linkedin.com/company
```

## Lead Scoring

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
- Other: 10 points

**Decision Maker Found (0-25 points)**
- CEO/Owner: 25 points
- HR Director: 20 points
- CFO: 20 points
- Other: 10 points

**Contact Quality (0-25 points)**
- Email verified: 20 points
- Direct dial: +5 points
- LinkedIn profile: +5 points

### Qualification Threshold
- **High Priority:** Score 70-100
- **Medium Priority:** Score 50-69
- **Low Priority:** Score 30-49
- **Disqualify:** Score <30

## Outreach Sequence

### Day 1: Initial Email
**Subject:** $140K annual savings for [Company Name] (zero cost to implement)

Hi [First Name],

I noticed [Company Name] has about [employee_count] employees, which positions you for significant annual savings through a compliant Section 125 wellness program.

Organizations your size are typically saving:
- $681 per employee annually in FICA savings
- 30-60% reduction in workers' comp premiums
- Total savings: [calculated_amount]

One medical transportation company with 66 employees saved over $140,000 last year.

The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.

Would you be open to a 10-minute call this week to see the numbers for [Company Name]?

Best,
Zane

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info

### Day 4: Follow-up #1
**Subject:** Re: $140K annual savings for [Company Name]

Hi [First Name],

Just following up on my note about the Wellness 125 program. Happy to run a quick savings analysis based on your actual payroll data - takes about 5 minutes to share, shows exact savings broken down by employee count and wage bands.

No cost, no commitment. Just a clear view of what you could save.

Worth a quick call?

Best,
Zane

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info

### Day 7: Follow-up #2
**Subject:** Quick question about [Company Name]'s benefits strategy

Hi [First Name],

I'll keep this brief. We've helped similar organizations in [industry] achieve:
- [Case study savings amount]
- [Employee pay increase]
- [Implementation timeline]

The program is fully compliant, with legal opinions from ERISA counsel and independent accounting review.

Open to seeing how this would work for your team?

Best,
Zane

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info

### Day 14: Break-up Email
**Subject:** Last note re: [Company Name] savings

Hi [First Name],

I'll stop reaching out after this, but wanted to leave the door open.

If employee benefits costs or payroll taxes become a priority down the road, the Wellness 125 program is worth a look. Zero implementation cost, 30-60 day rollout, and most organizations see six-figure annual savings.

Here if you need it.

Best,
Zane

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info

## Lead Pipeline Tracking

### Pipeline Stages
1. **Identified** - Company found, basic info gathered
2. **Enriched** - Full company data collected
3. **Contacted** - Initial outreach sent
4. **Engaged** - Response received
5. **Qualified** - Meeting scheduled/proposal sent
6. **Closed** - Deal signed
7. **Disqualified** - Not a fit

### Tracking Files
- `/workspace/leads/daily-leads-YYYY-MM-DD.md` - Daily lead lists
- `/workspace/leads/pipeline.md` - Active pipeline
- `/workspace/leads/contacts.md` - Contact database
- `/workspace/leads/analytics.md` - Performance metrics

## Daily Workflow (Automated)

### Morning (9 AM)
1. Generate 15-20 new leads
2. Enrich company data
3. Find decision-maker emails
4. Score and qualify
5. Add to pipeline

### Afternoon (2 PM)
1. Send initial outreach to high-priority leads
2. Send follow-ups based on sequence timing
3. Log all activity

### Evening (5 PM)
1. Update pipeline status
2. Track response rates
3. Generate daily report

## Metrics to Track

### Daily
- New leads identified
- Leads enriched
- Emails sent
- Response rate

### Weekly
- Lead-to-response rate
- Response-to-meeting rate
- Average lead score
- Pipeline value

### Monthly
- Meetings booked
- Proposals sent
- Deals closed
- Revenue generated

## API Integration

### AgentMail (Email Sending)
**From:** Zane@agentmail.to
**CC:** sam@impactquadrant.info (on all emails)

```python
from agentmail_integration import send_email, send_initial_outreach

# Send initial outreach
result = send_initial_outreach(lead_data)

# Send custom email
result = send_email(
    to_email="hr@company.com",
    subject="Subject line",
    text_content="Plain text version",
    html_content="<p>HTML version</p>",
    cc="sam@impactquadrant.info"
)
```

### Hunter.io Email Search
```bash
curl "https://api.hunter.io/v2/domain-search?domain=company.com&api_key=f701d171cf7decf7e730a6b1c6e9b74f29f39b6e"
```

### Abstract Company Enrichment
```bash
curl "https://companyenrichment.abstractapi.com/v1/?api_key=38aeec02e6f6469983e0856dfd147b10&domain=company.com"
```

## Compliance Notes

- All emails include unsubscribe option
- Honor opt-out requests immediately
- Follow CAN-SPAM requirements
- Track consent and opt-outs
