#!/usr/bin/env python3
"""
Update OpenClaw cron jobs to use Scrapling-first approach.

This script updates all lead generation cron jobs to:
1. Use Scrapling for web scraping first
2. Fall back to Brave Search/Tavily APIs if Scrapling fails
3. Maintain existing functionality with enhanced performance
"""

import json
import sys
import os
from datetime import datetime

# List of cron jobs to update with Scrapling-first approach
CRON_JOBS_TO_UPDATE = [
    # Lead Generation Jobs
    {
        "id": "21f22635-5622-41f1-88d4-af1b43965e61",
        "name": "Expense Reduction Lead Gen",
        "type": "expense_reduction"
    },
    {
        "id": "ad9ea923-d3bb-465b-a2eb-233203b7c90e",
        "name": "Deal Origination - Sellers",
        "type": "deal_sellers"
    },
    {
        "id": "8bc2acb7-6a30-48d7-911f-8e4a7edd44a0",
        "name": "Referral Engine - Prospects",
        "type": "referral_prospects"
    },
    {
        "id": "f546195e-6efd-4622-b131-33e79097252a",
        "name": "Referral Engine - Providers",
        "type": "referral_providers"
    },
    {
        "id": "583a120a-dfb9-4529-b228-67bfa60734bd",
        "name": "Enhanced Lead Gen v2",
        "type": "enhanced_lead_gen"
    },
    {
        "id": "9c2fe9b1-12e5-4561-ac8a-4d5a8da1c7dd",
        "name": "Deal Origination - Buyers",
        "type": "deal_buyers"
    },
    {
        "id": "5eb89608-b94d-4908-8bef-5f5264cb17ce",
        "name": "Defense Sector Lead Gen",
        "type": "defense_sector"
    }
]

# Scrapling-first message templates for each job type
SCRAPLING_MESSAGES = {
    "expense_reduction": """# Daily Lead Generation - Expense Reduction Services (Scrapling-Enhanced)

You are running the daily lead generation process for expense reduction services with SCRAPLING-FIRST approach.

## NEW: Scrapling Integration
Scrapling gives us an unfair advantage:
- **774x faster** than traditional scraping
- **Cloudflare bypass** - automatically handles anti-bot systems
- **Maximum stealth** - no bot detection
- **Adaptive scraping** - no selector maintenance needed

## Your Task (Scrapling-First):

### Step 1: Try Scrapling First (Primary Source)
```python
# Use Scrapling integration for fast, reliable data extraction
from scrapling_integration.cron_integration import ScraplingCronIntegration

async def generate_leads_with_scrapling():
    scrapling = ScraplingCronIntegration(stealth_mode=True)
    await scrapling.initialize()
    
    # Generate expense reduction leads
    search_queries = [
        "manufacturing companies 50-200 employees",
        "technology companies 20-100 employees",
        "healthcare companies 30-150 employees",
        "professional services firms 25-75 employees",
        "financial services companies 40-120 employees"
    ]
    
    leads = await scrapling.generate_expense_reduction_leads(
        search_queries=search_queries,
        limit=20
    )
    
    return leads
```

### Step 2: Fall Back to Traditional APIs (If Scrapling Fails)
If Scrapling returns no results or fails:
- Use **Tavily API** (preferred): `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`
- Fall back to **Brave Search**: `BSA4VYA3FjSPQmTjZeKjsq5CqWvFy2u`

### Step 3: Process Results
1. **Generate 15-20 New Leads:**
   - Target companies with 20-500 employees
   - Focus on: Technology/SaaS, Manufacturing, Healthcare, Professional Services, Financial Services
   - Look for companies with high OPEX indicators

2. **Enrich Company Data:**
   - Get employee count, industry, location
   - Find company website/domain
   - Estimate OPEX: $8K-$15K per employee annually
   - Calculate potential savings: 15-30% of estimated OPEX

3. **Find Decision Makers:**
   - CFO/Controller (primary target)
   - VP Finance / Finance Director
   - Director of Operations / Procurement

4. **Score Leads (0-100):**
   - Company size: 0-25 points
   - Spend indicators: 0-25 points
   - Decision maker found: 0-25 points
   - Contact quality: 0-25 points
   - High Priority: 70+, Medium: 50-69, Low: 30-49

5. **Save Results:**
   - Create `/workspace/expense-leads/daily-leads-YYYY-MM-DD.md`
   - Update `/workspace/expense-leads/pipeline.md`
   - Include: Company, industry, size, estimated OPEX, potential savings range

6. **Send Summary to Discord:**
   - Total leads generated
   - High priority count
   - Total potential savings
   - Top 3 leads of the day
   - **Note if Scrapling was used successfully**

## Performance Benefits:
- **Speed:** 774x faster than traditional scraping
- **Reliability:** Bypasses Cloudflare and anti-bot systems
- **Stealth:** No bot detection
- **Maintenance:** Zero selector maintenance

## Target:
- 15-20 qualified leads daily
- Focus on companies with significant OPEX
- Track all activity in pipeline

Generate leads now using Scrapling-first approach and report results to #mac-mini1.""",

    "defense_sector": """# Defense Sector Lead Generation - ENHANCED (Scrapling-First)

Two-part daily search with SCRAPLING-FIRST approach.

## NEW: Scrapling Integration
Scrapling gives us:
- **Maximum stealth** for sensitive defense sites
- **Cloudflare bypass** for protected sites
- **Adaptive scraping** for complex defense company websites

## Part 1: Defense Companies (5-10 leads) - Scrapling First

### Step 1: Try Scrapling
```python
from scrapling_integration.cron_integration import ScraplingCronIntegration

async def find_defense_companies():
    scrapling = ScraplingCronIntegration(stealth_mode=True)
    await scrapling.initialize()
    
    search_terms = [
        "defense technology companies",
        "cybersecurity companies military",
        "drone technology defense",
        "space defense technology",
        "military AI companies"
    ]
    
    companies = await scrapling.scrape_defense_companies(search_terms)
    return companies
```

### Step 2: Fall Back to Traditional APIs
If Scrapling fails or returns no results:
- Use **Tavily API**: `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`
- Search for defense companies in US/UK/EU

### Target Sectors
1. Cybersecurity - Defense-grade security
2. AI & Machine Learning - Military applications
3. Counter-Drone (C-UAS) - Anti-drone systems
4. Space-Based Defense - Satellites, space tech
5. Defense Data Analytics - ISR, decision systems

### Company Criteria
- Stage: Early to mid-stage (Series A-C)
- Region: US, UK, EU
- Focus: Defense or dual-use technology
- IP ownership important

## Part 2: PE/VC Funds in Asia/India (3-5 leads)

### Target Regions
- India
- Singapore
- Japan
- South Korea
- Taiwan
- Southeast Asia
- Middle East
- **EXCLUDE: China**

### Fund Criteria
- Focus: Defense tech, drones, aerospace, dual-use
- Active investments in autonomous systems
- Interest in drone/UAV technology
- Portfolio includes security or surveillance

## Save Results

Create TWO files:
1. `/workspace/defense-leads/daily-companies-YYYY-MM-DD.md`
2. `/workspace/defense-leads/daily-investors-YYYY-MM-DD.md`

## Report to Discord

```
🛡️ **Defense Sector Report (Scrapling-Enhanced)**

## Companies (US/UK/EU) - Scrapling Used: [Yes/No]
- Identified: X
- High priority (70+): X
- Top 3: [Company] - [Sector] - [Score]

## Investors (Asia/India)
- PE/VC funds: X
- Defense-focused: X
- Top 3: [Fund] - [Region] - [Focus]

## Performance Notes:
- Scrapling success: [Yes/No]
- Traditional APIs used: [Yes/No]
- Total processing time: X seconds
```

Target: 5-10 companies + 3-5 investors daily.""",

    "deal_sellers": """# Deal Origination - Off-Market Sellers (Scrapling-Enhanced)

You are running daily seller lead generation for business acquisitions with SCRAPLING-FIRST approach.

## NEW: Scrapling Integration
Scrapling helps find off-market sellers by:
- **Stealth mode** for sensitive business websites
- **Adaptive scraping** for outdated websites (common with older businesses)
- **Email extraction** from contact pages

## Your Task (Scrapling-First):

### Step 1: Try Scrapling First
```python
from scrapling_integration.cron_integration import ScraplingCronIntegration

async def find_seller_leads():
    scrapling = ScraplingCronIntegration(stealth_mode=True)
    await scrapling.initialize()
    
    # Search for business websites in target industries
    industries = [
        "HVAC companies",
        "plumbing businesses", 
        "electrical contractors",
        "roofing companies",
        "commercial cleaning",
        "waste management",
        "healthcare services",
        "insurance brokerage"
    ]
    
    # Scrapling will find and analyze business websites
    sellers = await scrapling.find_seller_leads(industries)
    return sellers
```

### Step 2: Fall Back to Traditional APIs
If Scrapling fails:
- Use **Tavily API**: `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`
- Search for business directories and listings

### Step 3: Generate 10-15 Off-Market Seller Leads:
- NO business brokers - direct owner relationships only
- Blue Collar: HVAC, Plumbing, Electrical, Roofing, Fire/Safety, Commercial Cleaning, Waste Management
- Platform: Healthcare Services, Insurance Brokerage, Logistics, Dental, Veterinary
- $500K - $10M+ EBITDA

### Seller Signals to Look For:
- Business age > 15 years
- Owner nearing retirement age
- Outdated website/branding
- High review count, low marketing spend
- Second-generation ownership

### Score Each Lead (0-100):
- EBITDA range: 0-30 points
- Years in business: 0-20 points
- Owner retirement signals: 0-25 points
- Segment fit: 0-25 points

### Save Results:
- Create `/workspace/deals/sellers/daily-sellers-YYYY-MM-DD.md`
- Update `/workspace/deals/pipeline.md`
- Include: Company, industry, EBITDA, years in business, owner signals, estimated finder fee

### Send Summary to Discord:
- Total sellers identified
- High priority count
- Blue collar vs platform split
- Total estimated finder fees
- **Scrapling usage status**

## Key Metrics:
- Target: 10-15 sellers daily
- No brokers - off-market only
- Track estimated finder fees

Generate leads now using Scrapling-first approach and report results.""",

    "enhanced_lead_gen": """# Enhanced Lead Generation - FOCUSED (Scrapling-First)

Generate 20-30 leads quickly using SCRAPLING-FIRST approach.

## NEW: Scrapling Integration
Scrapling provides:
- **774x faster** data extraction
- **Zero maintenance** - adaptive to website changes
- **Maximum stealth** - bypasses all anti-bot systems

## Step 1: Try Scrapling First (5 mins)

```python
from scrapling_integration.cron_integration import ScraplingCronIntegration

async def generate_leads_fast():
    scrapling = ScraplingCronIntegration(stealth_mode=True)
    await scrapling.initialize()
    
    # Fast parallel scraping
    leads = await scrapling.generate_expense_reduction_leads(
        search_queries=[
            "manufacturing companies 50-200 employees Texas",
            "technology companies 20-100 employees California",
            "healthcare companies 30-150 employees Florida",
            "professional services 25-75 employees New York"
        ],
        limit=30
    )
    
    return leads
```

## Step 2: Fall Back to Traditional APIs (If Needed)

If Scrapling fails or needs supplementation:
- **Serper API**: `BSA4VYA3FjSPQmTjZeKjsq5CqWvFy2u`
- **ZeroBounce**: `fd0105c8c98340e0a2b63e2fbe39d7a4`

## Step 3: Quick Score (0-100)

- Size fit (50-200 employees): 25 pts
- Industry match: 25 pts
- Contact found: 25 pts
- Intent signal: 25 pts

## Step 4: Save

Create `/workspace/leads/daily-leads-YYYY-MM-DD.md`

## Step 5: Report

- Total found: X
- High priority (70+): X
- Top 3 companies
- **Scrapling success: Yes/No**
- **Processing time: X seconds**

STOP after 15 minutes. Report progress.

## Performance Benefits:
- **Speed:** Process 100+ URLs in parallel
- **Reliability:** Adaptive to website changes
- **Stealth:** No bot detection
- **Cost:** Reduces API calls to Serper/Tavily""",

    "deal_buyers": """# Deal Origination - PE Buyers (Scrapling-Enhanced)

Find 3-4 PE buyers who accept finder fees using SCRAPLING-FIRST approach.

## NEW: Scrapling Integration
Scrapling helps:
- **Extract contact info** from PE firm websites
- **Analyze investment focus** from portfolio pages
- **Find fee policies** from partnership pages

## Step 1: Try Scrapling First

```python
from scrapling_integration.cron_integration import ScraplingCronIntegration

async def find_pe_buyers():
    scrapling = ScraplingCronIntegration(stealth_mode=True)
    await scrapling.initialize()
    
    # Search for PE firm websites
    buyers = await scrapling.find_pe_buyers(
        focus_areas=["blue-collar", "healthcare", "logistics", "insurance"],
        regions=["US", "Canada", "Europe"]
    )
    
    return buyers
```

## Step 2: Fall Back to Traditional APIs

If Scrapling fails:
- Use **Tavily API**: `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`
- Search for PE firm directories

## Target Buyers
- Private Equity firms
- Independent sponsors
- Family offices
- Search funds

## Criteria
- MUST accept finder fees
- Active in blue-collar OR platform targets
- Blue Collar: HVAC, Plumbing, Electrical, Roofing
- Platform: Healthcare, Insurance, Logistics
- Check size: $1M - $75M

## Score (0-100)
- Finder fee history: 40 pts (most important)
- Buyer type: 25 pts
- Focus match: 20 pts
- Industry coverage: 15 pts

## Save

Create `/workspace/deals/buyers/daily-buyers-YYYY-MM-DD.md`

## Report to Discord

- Buyers identified: X
- High priority: X
- Finder fee willing: X
- **Scrapling used: Yes/No**

Keep search focused. 3-4 buyers max.""",

    "referral_prospects": """# B2B Referral Engine - Demand Side (Prospects) - Scrapling-Enhanced

You are running daily prospect identification for the B2B referral engine with SCRAPLING-FIRST approach.

## NEW: Scrapling Integration
Scrapling detects buying signals by:
- **Monitoring job postings** for intent signals
- **Tracking permit filings** for expansion
- **Analyzing tech stack changes** for SaaS needs
- **Finding funding announcements** for Series A+ companies

## Target: 10-15 daily prospects

## Step 1: Try Scrapling First

```python
from scrapling_integration.cron_integration import ScraplingCronIntegration

async def find_referral_prospects():
    scrapling = ScraplingCronIntegration(stealth_mode=True)
    await scrapling.initialize()
    
    # Scrapling will monitor for buying signals
    prospects = await scrapling.find_referral_prospects(
        verticals=["B2B Professional Services", "Technology/SaaS", "Construction", "Financial Services"],
        signal_types=["job_postings", "funding_announcements", "permit_filings", "tech_stack_changes"]
    )
    
    return prospects
```

## Step 2: Fall Back to Traditional APIs

If Scrapling fails:
- Use **Tavily API**: `tvly-dev-rvV85j53kZTDW1J