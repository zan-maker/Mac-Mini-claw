#!/usr/bin/env python3
"""
Simple script to update cron jobs with Scrapling-first approach.
"""

import json
import sys
import os

# Scrapling-first message template
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
from scrapling_integration.cron_integration import ScraplingCronIntegration

async def run_with_scrapling():
    # Initialize Scrapling with stealth mode
    scrapling = ScraplingCronIntegration(stealth_mode=True)
    success = await scrapling.initialize()
    
    if success:
        print("✅ Scrapling initialized successfully")
        # Use Scrapling for data extraction
        # [Add job-specific Scrapling code here]
        results = await scrapling.{scrapling_method}()
        return results
    else:
        print("⚠️ Scrapling initialization failed, falling back to traditional APIs")
        return []
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
1. Scrapling is installed in: `/Users/cubiczan/.openclaw/workspace/scrapling-integration/`
2. Activate virtual environment: `source /Users/cubiczan/.openclaw/workspace/scrapling-venv/bin/activate`
3. Import: `from scrapling_integration.cron_integration import ScraplingCronIntegration`
4. Always try Scrapling first, fall back to APIs only if needed

Run the job now using Scrapling-first approach and report results."""

# Job-specific configurations
JOB_CONFIGS = {
    "Expense Reduction Lead Gen": {
        "scrapling_method": "generate_expense_reduction_leads",
        "description": "Generate 15-20 expense reduction leads"
    },
    "Defense Sector Lead Gen": {
        "scrapling_method": "scrape_defense_companies", 
        "description": "Find defense companies and investors"
    },
    "Deal Origination - Sellers": {
        "scrapling_method": "find_seller_leads",
        "description": "Find 10-15 off-market business sellers"
    },
    "Enhanced Lead Gen v2": {
        "scrapling_method": "generate_expense_reduction_leads",
        "description": "Generate 20-30 leads quickly"
    },
    "Deal Origination - Buyers": {
        "scrapling_method": "find_pe_buyers",
        "description": "Find 3-4 PE buyers accepting finder fees"
    }
}

def create_scrapling_message(job_name, original_message):
    """Create Scrapling-first message for a cron job."""
    config = JOB_CONFIGS.get(job_name, {
        "scrapling_method": "generate_expense_reduction_leads",
        "description": "Generate leads using Scrapling"
    })
    
    # Extract original instructions (everything after the first heading)
    lines = original_message.split('\n')
    original_instructions = ""
    in_instructions = False
    
    for line in lines:
        if line.startswith('#') and 'Your Task:' in line:
            in_instructions = True
        if in_instructions:
            original_instructions += line + '\n'
    
    if not original_instructions:
        original_instructions = original_message
    
    # Create Scrapling-first message
    scrapling_message = SCRAPLING_FIRST_TEMPLATE.format(
        job_name=job_name,
        scrapling_method=config["scrapling_method"],
        original_instructions=original_instructions
    )
    
    return scrapling_message

def main():
    """Main function to update cron jobs."""
    print("🔄 Updating cron jobs with Scrapling-first approach...")
    print("="*60)
    
    # List of cron jobs to update (from earlier analysis)
    cron_jobs = [
        {
            "name": "Expense Reduction Lead Gen",
            "id": "21f22635-5622-41f1-88d4-af1b43965e61",
            "original_file": "/Users/cubiczan/.openclaw/workspace/memory/2026-02-20.md"  # We'll extract from memory
        },
        {
            "name": "Defense Sector Lead Gen", 
            "id": "5eb89608-b94d-4908-8bef-5f5264cb17ce",
            "original_file": "/Users/cubiczan/.openclaw/workspace/memory/2026-02-20.md"
        },
        {
            "name": "Deal Origination - Sellers",
            "id": "ad9ea923-d3bb-465b-a2eb-233203b7c90e",
            "original_file": "/Users/cubiczan/.openclaw/workspace/memory/2026-02-20.md"
        },
        {
            "name": "Enhanced Lead Gen v2",
            "id": "583a120a-dfb9-4529-b228-67bfa60734bd",
            "original_file": "/Users/cubiczan/.openclaw/workspace/memory/2026-02-20.md"
        },
        {
            "name": "Deal Origination - Buyers",
            "id": "9c2fe9b1-12e5-4561-ac8a-4d5a8da1c7dd",
            "original_file": "/Users/cubiczan/.openclaw/workspace/memory/2026-02-20.md"
        }
    ]
    
    # Create example updated messages
    print("\n📋 Example Scrapling-first messages:")
    print("="*60)
    
    for job in cron_jobs[:2]:  # Show first 2 as examples
        print(f"\n🎯 {job['name']}:")
        print("-"*40)
        
        # Create example original message
        original_message = f"""# {job['name']}

## Your Task:

Generate leads for {job['name'].split('-')[0].strip()}.

### Step 1: Search
Use web search to find companies.

### Step 2: Process
Extract company information.

### Step 3: Save
Save results to file.

### Step 4: Report
Send summary to Discord."""
        
        scrapling_message = create_scrapling_message(job['name'], original_message)
        
        # Show preview
        preview = scrapling_message[:500] + "..." if len(scrapling_message) > 500 else scrapling_message
        print(preview)
        print(f"\n📏 Length: {len(scrapling_message)} characters")
    
    print("\n" + "="*60)
    print("✅ Scrapling-first template created successfully!")
    print("\n📋 Next steps:")
    print("1. Update each cron job via OpenClaw cron tool")
    print("2. Use the Scrapling-first message template")
    print("3. Test the updated cron jobs")
    print("4. Monitor performance improvements")
    
    # Create a ready-to-use update script
    update_script = """#!/usr/bin/env python3
# Script to update cron jobs with Scrapling-first approach
# Run this in OpenClaw session

import subprocess
import json

# Update Expense Reduction Lead Gen
expense_reduction_msg = '''{expense_msg}'''

# Update Defense Sector Lead Gen  
defense_sector_msg = '''{defense_msg}'''

print("Ready to update cron jobs with Scrapling-first approach!")
print("Copy the messages above and update each cron job via:")
print("1. cron update --jobId <id> --patch '{{\"payload\": {{\"message\": \"<message>\"}}}}'")
print("2. Or use the OpenClaw web interface")
""".format(
        expense_msg=create_scrapling_message(
            "Expense Reduction Lead Gen",
            "# Original message would be here"
        )[:1000] + "...",
        defense_msg=create_scrapling_message(
            "Defense Sector Lead Gen",
            "# Original message would be here"
        )[:1000] + "..."
    )
    
    # Save update script
    script_path = "/Users/cubiczan/.openclaw/workspace/scrapling-integration/update_cron_jobs_ready.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(update_script)
    
    print(f"\n💾 Update script saved to: {script_path}")
    print("\n🚀 To update cron jobs:")
    print("1. Read the current cron job messages")
    print("2. Create Scrapling-first versions using create_scrapling_message()")
    print("3. Update each cron job via OpenClaw cron update command")

if __name__ == "__main__":
    main()