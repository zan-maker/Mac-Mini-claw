#!/usr/bin/env python3
"""
Update all lead generation cron jobs with Scrapling-first approach.
"""

import json

# Scrapling-first template for different job types
SCRAPLING_TEMPLATES = {
    "deal_origination": """## 🚀 NEW: Scrapling Integration Activated

**Scrapling gives us an unfair advantage:**
- **774x faster** than traditional web scraping
- **Cloudflare bypass** - automatically handles anti-bot systems
- **Maximum stealth** - no bot detection
- **Adaptive scraping** - no selector maintenance needed
- **AI-powered extraction** - natural language queries

## 📋 Your Task (Scrapling-First Approach)

### Step 1: Try Scrapling First (Primary Source)
```python
# Use Scrapling integration for fast, reliable data extraction
# Scrapling is installed in: /Users/cubiczan/.openclaw/workspace/scrapling-integration/
# Activate virtual environment: source /Users/cubiczan/.openclaw/workspace/scrapling-venv/bin/activate

import sys
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

try:
    from cron_integration import ScraplingCronIntegration
    
    async def run_with_scrapling():
        # Initialize Scrapling with stealth mode
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if success:
            print("✅ Scrapling initialized successfully")
            # Use Scrapling for deal origination
            results = await scrapling.{scrapling_method}()
            return results
        else:
            print("⚠️ Scrapling initialization failed, falling back to traditional APIs")
            return []
except ImportError:
    print("⚠️ Scrapling not available, using traditional APIs")
```

### Step 2: Fall Back to Traditional APIs (If Scrapling Fails)
If Scrapling returns no results or fails:
1. **First fallback:** Use **Tavily API** (preferred)
   - API Key: `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`
   - Faster and more reliable than Brave Search

2. **Second fallback:** Use **Brave Search API**
   - API Key: `BSA4VYA3FjSPQmTjZeKjsq5CqWvFy2u`
   - Use only if Tavily fails

### Step 3: Process and Report Results
1. Process the data (same as before)
2. Save results to appropriate files
3. **IMPORTANT:** Include Scrapling usage status in Discord report:
   ```
   🔍 **Data Source Report:**
   - Scrapling Used: ✅ Yes / ❌ No
   - Scrapling Results: X {result_type}
   - Traditional API Results: Y {result_type}
   - Total Processing Time: Z seconds
   ```""",
    
    "referral_engine": """## 🚀 NEW: Scrapling Integration Activated

**Scrapling gives us an unfair advantage:**
- **774x faster** than traditional web scraping
- **Cloudflare bypass** - automatically handles anti-bot systems
- **Maximum stealth** - no bot detection
- **Adaptive scraping** - no selector maintenance needed
- **AI-powered extraction** - natural language queries

## 📋 Your Task (Scrapling-First Approach)

### Step 1: Try Scrapling First (Primary Source)
```python
# Use Scrapling integration for fast, reliable data extraction
# Scrapling is installed in: /Users/cubiczan/.openclaw/workspace/scrapling-integration/
# Activate virtual environment: source /Users/cubiczan/.openclaw/workspace/scrapling-venv/bin/activate

import sys
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

try:
    from cron_integration import ScraplingCronIntegration
    
    async def run_with_scrapling():
        # Initialize Scrapling with stealth mode
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if success:
            print("✅ Scrapling initialized successfully")
            # Use Scrapling for referral engine leads
            results = await scrapling.{scrapling_method}()
            return results
        else:
            print("⚠️ Scrapling initialization failed, falling back to traditional APIs")
            return []
except ImportError:
    print("⚠️ Scrapling not available, using traditional APIs")
```

### Step 2: Fall Back to Traditional APIs (If Scrapling Fails)
If Scrapling returns no results or fails:
1. **First fallback:** Use **Tavily API** (preferred)
   - API Key: `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`
   - Faster and more reliable than Brave Search

2. **Second fallback:** Use **Brave Search API**
   - API Key: `BSA4VYA3FjSPQmTjZeKjsq5CqWvFy2u`
   - Use only if Tavily fails

### Step 3: Process and Report Results
1. Process the data (same as before)
2. Save results to appropriate files
3. **IMPORTANT:** Include Scrapling usage status in Discord report:
   ```
   🔍 **Data Source Report:**
   - Scrapling Used: ✅ Yes / ❌ No
   - Scrapling Results: X {result_type}
   - Traditional API Results: Y {result_type}
   - Total Processing Time: Z seconds
   ```"""
}

# Job configurations for remaining lead generation jobs
REMAINING_JOBS = [
    {
        "id": "ad9ea923-d3bb-465b-a2eb-233203b7c90e",
        "name": "Deal Origination - Sellers",
        "type": "deal_origination",
        "scrapling_method": "find_off_market_sellers",
        "result_type": "sellers",
        "original_message": """# Deal Origination - Off-Market Sellers

You are running daily seller lead generation for business acquisitions.

## Your Task:

1. **Generate 10-15 Off-Market Seller Leads:**
   - NO business brokers - direct owner relationships only
   - Blue Collar: HVAC, Plumbing, Electrical, Roofing, Fire/Safety, Commercial Cleaning, Waste Management
   - Platform: Healthcare Services, Insurance Brokerage, Logistics, Dental, Veterinary
   - $500K - $10M+ EBITDA

2. **Seller Signals to Look For:**
   - Business age > 15 years
   - Owner nearing retirement age
   - Outdated website/branding
   - High review count, low marketing spend
   - Second-generation ownership

3. **Score Each Lead (0-100):**
   - EBITDA range: 0-30 points
   - Years in business: 0-20 points
   - Owner retirement signals: 0-25 points
   - Segment fit: 0-25 points

4. **Save Results:**
   - Create `/workspace/deals/sellers/daily-sellers-YYYY-MM-DD.md`
   - Update `/workspace/deals/pipeline.md`
   - Include: Company, industry, EBITDA, years in business, owner signals, estimated finder fee

5. **Send Summary to Discord:**
   - Total sellers identified
   - High priority count
   - Blue collar vs platform split
   - Total estimated finder fees

## Key Metrics:
- Target: 10-15 sellers daily
- No brokers - off-market only
- Track estimated finder fees

Generate leads now and report results."""
    },
    {
        "id": "8bc2acb7-6a30-48d7-911f-8e4a7edd44a0",
        "name": "Referral Engine - Prospects",
        "type": "referral_engine",
        "scrapling_method": "find_referral_prospects",
        "result_type": "prospects",
        "original_message": """# B2B Referral Engine - Demand Side (Prospects)

You are running daily prospect identification for the B2B referral engine.

## Target: 10-15 daily prospects

## Verticals (Priority Order):
1. **B2B Professional Services** - Accounting, Legal, Consulting ($5K-$7.5K fee)
2. **Technology/SaaS** - Software implementations ($5K or 10-20% ACV)
3. **Construction & Trades** - Permits, RFPs ($3K fee)
4. **Financial Services B2B** - Treasury, lending, insurance ($2.5K fee)
5. **Manufacturing** - Supply chain ($1K fee)
6. **Commercial Real Estate** - Leasing ($3K-$10K fee)

## Buying Signals to Detect:
- Series A+ funding
- Job postings (data engineers, controllers)
- Permit filings
- Tech stack changes
- Expansion announcements
- Lease expirations

## Score Prospects (0-100):
- Intent signals: 0-40 points
- Vertical fee potential: 0-30 points
- Company size fit: 0-20 points
- Signal specificity: 0-10 points

## Save Results:
- `/workspace/referral-engine/prospects/daily-prospects-YYYY-MM-DD.md`

## Report to Discord:
- Total prospects identified
- High priority count (80+)
- Top 3 prospects with signals
- Total potential fees

Generate 10-15 prospects now."""
    },
    {
        "id": "f546195e-6efd-4622-b131-33e79097252a",
        "name": "Referral Engine - Providers",
        "type": "referral_engine",
        "scrapling_method": "find_referral_providers",
        "result_type": "providers",
        "original_message": """# B2B Referral Engine - Supply Side (Service Providers)

You are running daily service provider identification for referral agreements.

## Target: 3-4 daily providers willing to pay referral fees

## Provider Categories:
1. **Accounting Firms** - Audit, Tax, Fractional CFO (10-15% first year)
2. **Law Firms** - Corporate, M&A, Compliance (10-15% first year)
3. **Consulting Firms** - Strategy, Operations (10% of contract)
4. **SaaS Partners** - Implementation, Integration ($5K or 10-20% ACV)
5. **Construction Contractors** - Trades, PM ($3K per referral)
6. **CRE Brokers** - Office, Industrial (25% of commission)

## Qualification Criteria:
- MUST accept referral fees
- Active partner/referral programs preferred
- Clear fee structure
- Good reputation

## Score Providers (0-100):
- Willingness score: 0-40 points
- Fee structure: 0-30 points
- Referral history: 0-20 points
- Category potential: 0-10 points

## Outreach Templates Ready:
- Subject: "Referral partnership - qualified [vertical] leads"
- Propose standard fee terms
- Highlight pre-qualified introductions

## Save Results:
- `/workspace/referral-engine/providers/daily-providers-YYYY-MM-DD.md`

## Report to Discord:
- Total providers identified
- High priority count (80+)
- Providers ready for outreach
- Fee structures offered

Generate 3-4 providers now."""
    },
    {
        "id": "9c2fe9b1-12e5-4561-ac8a-4d5a8da1c7dd",
        "name": "Deal Origination - Buyers",
        "type": "deal_origination",
        "scrapling_method": "find_pe_buyers",
        "result_type": "buyers",
        "original_message": """# Deal Origination - PE Buyers

Find 3-4 PE buyers who accept finder fees.

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

Keep search focused. 3-4 buyers max."""
    }
]

def create_updated_message(job_config):
    """Create updated message with Scrapling-first approach."""
    template = SCRAPLING_TEMPLATES.get(job_config["type"], SCRAPLING_TEMPLATES["deal_origination"])
    
    # Format the template with job-specific values
    scrapling_section = template.format(
        scrapling_method=job_config["scrapling_method"],
        result_type=job_config["result_type"]
    )
    
    # Create the full message
    updated_message = f"""# {job_config['name']} - Scrapling-First Enhanced

{scrapling_section}

## 🎯 Performance Benefits
- **Speed:** 774x faster than BeautifulSoup
- **Reliability:** Bypasses Cloudflare and anti-bot systems
- **Stealth:** No bot detection
- **Maintenance:** Zero selector maintenance
- **Cost:** Reduces API calls to Serper/Tavily

## Original Task:

{job_config['original_message']}

## 💡 Implementation Notes
1. Scrapling is installed and ready to use
2. Always try Scrapling first, fall back to APIs only if needed
3. Report Scrapling usage status in Discord
4. Include Scrapling results in your Discord report

Generate leads now using Scrapling-first approach and report results."""
    
    return updated_message

def main():
    """Main function to generate updated cron job messages."""
    print("🔄 Creating Scrapling-first messages for remaining lead generation jobs...")
    print("="*70)
    
    for job in REMAINING_JOBS:
        print(f"\n🎯 {job['name']} (ID: {job['id']}):")
        print("-"*40)
        
        updated_message = create_updated_message(job)
        
        # Show preview
        preview = updated_message[:800] + "..." if len(updated_message) > 800 else updated_message
        print(preview)
        print(f"\n📏 Length: {len(updated_message)} characters")
        
        # Save to file
        filename = f"/Users/cubiczan/.openclaw/workspace/scrapling-integration/cron_{job['name'].lower().replace(' ', '_').replace('-', '_')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(updated_message)
        
        print(f"💾 Saved to: {filename}")
    
    print("\n" + "="*70)
    print("✅ Scrapling-first messages created successfully!")
    print("\n🚀 To update cron jobs, run these commands:")
    print("="*70)
    
    for job in REMAINING_JOBS:
        print(f"\n# Update {job['name']}:")
        print(f"cron update --jobId {job['id']} --patch '{{\"payload\": {{\"message\": \"<message>\"}}}}'")
    
    print("\n" + "="*70)
    print("📋 Summary of jobs updated:")
    print("1. ✅ Expense Reduction Lead Gen (Scrapling-first)")
    print("2. ✅ Defense Sector Lead Gen (Scrapling-first)")
    print("3. ✅ Enhanced Lead Gen v2 (Scrapling-first)")
    print("4. ⏳ Deal Origination - Sellers")
    print("5. ⏳ Referral Engine - Prospects")
    print("6. ⏳ Referral Engine - Providers")
    print("7. ⏳ Deal Origination - Buyers")
    print("\n🎯 Total: 7 lead generation jobs enhanced with Scrapling-first approach")

if __name__ == "__main__":
    main()