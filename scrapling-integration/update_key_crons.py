#!/usr/bin/env python3
"""
Update key cron jobs with Scrapling-first approach.
"""

import json

# Scrapling-first template
SCRAPLING_FIRST_TEMPLATE = """# {job_name} - Scrapling-First Enhanced

## 🚀 NEW: Scrapling Integration Activated

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
            # Use Scrapling for data extraction
            # [Job-specific Scrapling code will go here]
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
   - Scrapling Results: X leads
   - Traditional API Results: Y leads
   - Total Processing Time: Z seconds
   ```

## 🎯 Performance Benefits
- **Speed:** 774x faster than BeautifulSoup
- **Reliability:** Bypasses Cloudflare and anti-bot systems
- **Stealth:** No bot detection
- **Maintenance:** Zero selector maintenance
- **Cost:** Reduces API calls to Serper/Tavily

## 📊 Report Format
Always include Scrapling status in your Discord report.

{original_instructions}

## 💡 Implementation Notes
1. Scrapling is installed and ready to use
2. Always try Scrapling first, fall back to APIs only if needed
3. Report Scrapling usage status in Discord

Run the job now using Scrapling-first approach and report results."""

# Job configurations
JOB_CONFIGS = {
    "Expense Reduction Lead Gen": {
        "id": "21f22635-5622-41f1-88d4-af1b43965e61",
        "scrapling_method": "generate_expense_reduction_leads",
        "description": "Generate 15-20 expense reduction leads"
    },
    "Defense Sector Lead Gen": {
        "id": "5eb89608-b94d-4908-8bef-5f5264cb17ce",
        "scrapling_method": "scrape_defense_companies",
        "description": "Find defense companies and investors"
    },
    "Enhanced Lead Gen v2": {
        "id": "583a120a-dfb9-4529-b228-67bfa60734bd",
        "scrapling_method": "generate_expense_reduction_leads",
        "description": "Generate 20-30 leads quickly"
    }
}

def create_scrapling_message(job_name, original_message):
    """Create Scrapling-first message."""
    config = JOB_CONFIGS.get(job_name, {
        "scrapling_method": "generate_expense_reduction_leads",
        "description": "Generate leads using Scrapling"
    })
    
    # Create Scrapling-first message
    scrapling_message = SCRAPLING_FIRST_TEMPLATE.format(
        job_name=job_name,
        scrapling_method=config["scrapling_method"],
        original_instructions=original_message
    )
    
    return scrapling_message

def main():
    """Main function to create updated cron job messages."""
    print("🔄 Creating Scrapling-first cron job messages...")
    print("="*60)
    
    # Example original messages (from the cron list)
    original_messages = {
        "Expense Reduction Lead Gen": """# Daily Lead Generation - Expense Reduction Services

You are running the daily lead generation process for expense reduction services.

## Your Task:

1. **Generate 15-20 New Leads:**
   - Target companies with 20-500 employees
   - Focus on: Technology/SaaS, Manufacturing, Healthcare, Professional Services, Financial Services
   - Look for companies with high OPEX indicators (SaaS spend, logistics, vendors)
   - Use web search to find companies in target industries

2. **Enrich Company Data:**
   - Get employee count, industry, location
   - Find company website/domain
   - Estimate OPEX: $8K-$15K per employee annually
   - Calculate potential savings: 15-30% of estimated OPEX

3. **Find Decision Makers:**
   - CFO/Controller (primary target)
   - VP Finance / Finance Director
   - Director of Operations / Procurement
   - Use Hunter.io API if domain found

4. **Score Leads (0-100):**
   - Company size: 0-25 points
   - Spend indicators: 0-25 points (tech=25, manufacturing=20, etc)
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

## Target:
- 15-20 qualified leads daily
- Focus on companies with significant OPEX
- Track all activity in pipeline

Generate leads now and report results to #mac-mini1.""",
        
        "Defense Sector Lead Gen": """# Defense Sector Lead Generation - ENHANCED

Two-part daily search: (1) Defense companies in US/UK/EU, (2) PE/VC funds in Asia/India.

## Part 1: Defense Companies (5-10 leads)

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

### Score (0-100)
- Sector fit: 0-30 pts
- Stage fit: 0-20 pts
- Technical depth: 0-20 pts
- Integration potential: 0-20 pts
- Region match: 0-10 pts

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

### Search Queries
- "defense technology PE fund India"
- "drone technology investors Asia"
- "aerospace venture capital Singapore Japan"
- "autonomous systems PE fund Korea Taiwan"
- "UAV drone investors Middle East"

### Score PE Funds (0-100)
- Defense/dron focus: 0-40 pts
- Region match: 0-20 pts
- Portfolio fit: 0-20 pts
- Fund size/stage: 0-20 pts

## Save Results

Create TWO files:
1. `/workspace/defense-leads/daily-companies-YYYY-MM-DD.md`
2. `/workspace/defense-leads/daily-investors-YYYY-MM-DD.md`

## Report to Discord

```
🛡️ **Defense Sector Report**

## Companies (US/UK/EU)
- Identified: X
- High priority (70+): X
- Top 3: [Company] - [Sector] - [Score]

## Investors (Asia/India)
- PE/VC funds: X
- Defense-focused: X
- Top 3: [Fund] - [Region] - [Focus]
```

Target: 5-10 companies + 3-5 investors daily.""",
        
        "Enhanced Lead Gen v2": """# Enhanced Lead Generation - FOCUSED

Generate 20-30 leads quickly. Keep it simple.

## APIs
- Serper: `BSA4VYA3FjSPQmTjZeKjsq5CqWvFy2u`
- ZeroBounce: `fd0105c8c98340e0a2b63e2fbe39d7a4`

## Step 1: Search (5 mins)

```bash
curl -X POST "https://google.serper.dev/search" \
  -H "X-API-KEY: BSA4VYA3FjSPQmTjZeKjsq5CqWvFy2u" \
  -d '{"q":"manufacturing companies 50-200 employees Texas"}'
```

Search for 3-4 different queries.

## Step 2: Quick Score (0-100)

- Size fit (50-200 employees): 25 pts
- Industry match: 25 pts
- Contact found: 25 pts
- Intent signal: 25 pts

## Step 3: Save

Create `/workspace/leads/daily-leads-YYYY-MM-DD.md`

## Step 4: Report

- Total found: X
- High priority (70+): X
- Top 3 companies

STOP after 15 minutes. Report progress."""
    }
    
    # Create updated messages
    print("\n📋 Updated Cron Job Messages:")
    print("="*60)
    
    for job_name, original_msg in original_messages.items():
        config = JOB_CONFIGS.get(job_name)
        if not config:
            continue
            
        print(f"\n🎯 {job_name} (ID: {config['id']}):")
        print("-"*40)
        
        updated_msg = create_scrapling_message(job_name, original_msg)
        
        # Show preview
        preview = updated_msg[:800] + "..." if len(updated_msg) > 800 else updated_msg
        print(preview)
        print(f"\n📏 Length: {len(updated_msg)} characters")
        
        # Save to file
        filename = f"/Users/cubiczan/.openclaw/workspace/scrapling-integration/cron_{job_name.lower().replace(' ', '_')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(updated_msg)
        
        print(f"💾 Saved to: {filename}")
    
    print("\n" + "="*60)
    print("✅ Scrapling-first messages created successfully!")
    print("\n🚀 To update cron jobs:")
    print("1. Copy the message from the saved .txt file")
    print("2. Update the cron job via:")
    print("   cron update --jobId <id> --patch '{\"payload\": {\"message\": \"<message>\"}}'")
    print("3. Or use the OpenClaw web interface")
    print("\n📋 Jobs to update:")
    for job_name, config in JOB_CONFIGS.items():
        print(f"   • {job_name}: ID {config['id']}")

if __name__ == "__main__":
    main()