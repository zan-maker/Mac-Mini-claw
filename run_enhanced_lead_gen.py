#!/usr/bin/env python3
"""
Enhanced Lead Gen v2 - Scrapling-First Approach
Runs lead generation using Scrapling first, falls back to Tavily/Brave Search
"""

import asyncio
import json
import sys
import os
import time
from datetime import datetime
from pathlib import Path
import aiohttp

# Configuration
WORKSPACE = Path("/Users/cubiczan/.openclaw/workspace")
LEADS_DIR = WORKSPACE / "leads"
SCRAPLING_VENV = "/Users/cubiczan/.openclaw/workspace/scrapling-venv/bin/activate"
SCRAPLING_INTEGRATION = "/Users/cubiczan/.openclaw/workspace/scrapling-integration"

# API Keys
TAVILY_API_KEY = "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"
BRAVE_API_KEY = "BSA4VYA3FjSPQmTjZeKjsq5CqWvFy2u"
ZEROBOUNCE_API_KEY = "fd0105c8c98340e0a2b63e2fbe39d7a4"

# Metrics tracking
metrics = {
    "start_time": time.time(),
    "scrapling_used": False,
    "scrapling_results": 0,
    "tavily_results": 0,
    "brave_results": 0,
    "total_leads": 0
}

async def try_scrapling():
    """Try Scrapling first for fast, reliable data extraction."""
    print("🚀 Attempting Scrapling integration...")
    
    try:
        # Add Scrapling to path
        sys.path.insert(0, SCRAPLING_INTEGRATION)
        from cron_integration import ScraplingCronIntegration
        
        # Initialize Scrapling
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if not success:
            print("⚠️ Scrapling initialization failed")
            return []
        
        print("✅ Scrapling initialized successfully")
        metrics["scrapling_used"] = True
        
        # Generate leads with Scrapling
        search_queries = [
            "manufacturing companies 50-200 employees Texas",
            "technology companies 20-100 employees California",
            "healthcare companies 30-150 employees Florida",
            "professional services firms 25-75 employees New York"
        ]
        
        leads = await scrapling.generate_expense_reduction_leads(
            search_queries=search_queries,
            limit=30,
            fast_mode=True
        )
        
        if leads:
            metrics["scrapling_results"] = len(leads)
            print(f"✅ Scrapling found {len(leads)} leads")
            return leads
        else:
            print("⚠️ Scrapling returned no results, falling back to APIs")
            return []
            
    except ImportError as e:
        print(f"⚠️ Scrapling not available: {e}")
        return []
    except Exception as e:
        print(f"❌ Scrapling error: {e}")
        return []

async def search_tavily(query: str):
    """Search using Tavily API (preferred fallback)."""
    print(f"🔍 Searching Tavily: {query}")
    
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    data = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "max_results": 10
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers, timeout=15) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("results", [])
                else:
                    print(f"⚠️ Tavily error: {response.status}")
                    return []
    except Exception as e:
        print(f"❌ Tavily error: {e}")
        return []

async def search_brave(query: str):
    """Search using Brave Search API (secondary fallback)."""
    print(f"🔍 Searching Brave: {query}")
    
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": BRAVE_API_KEY
    }
    params = {"q": query, "count": 10}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params, timeout=15) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("web", {}).get("results", [])
                else:
                    print(f"⚠️ Brave error: {response.status}")
                    return []
    except Exception as e:
        print(f"❌ Brave error: {e}")
        return []

def calculate_lead_score(company: dict, source: str) -> int:
    """Calculate lead score (0-100)."""
    score = 0
    
    # Size fit (25 points)
    size_text = str(company).lower()
    if any(x in size_text for x in ["100-200", "150+", "100+ employees"]):
        score += 25
    elif any(x in size_text for x in ["50-100", "50-200", "50+ employees"]):
        score += 20
    elif any(x in size_text for x in ["20-50", "25-75"]):
        score += 15
    else:
        score += 10
    
    # Industry match (25 points)
    high_value = ["manufacturing", "technology", "healthcare", "professional services", "finance"]
    if any(ind in size_text for ind in high_value):
        score += 25
    else:
        score += 10
    
    # Contact potential (25 points)
    if "contact" in size_text or "email" in size_text or "phone" in size_text:
        score += 25
    elif "about" in size_text:
        score += 15
    else:
        score += 10
    
    # Source quality (25 points)
    if source == "scrapling":
        score += 25
    elif source == "tavily":
        score += 20
    else:
        score += 15
    
    return min(score, 100)

async def generate_leads_with_apis():
    """Generate leads using traditional APIs (Tavily first, then Brave)."""
    print("🔄 Using traditional APIs for lead generation...")
    
    queries = [
        "manufacturing companies 50-200 employees Texas site:linkedin.com OR site:bloomberg.com",
        "technology companies 20-100 employees California contact",
        "healthcare companies 30-150 employees Florida",
        "professional services firms 25-75 employees New York",
        "mid-sized companies 50-200 employees contact email"
    ]
    
    leads = []
    
    # Try Tavily first
    for query in queries[:3]:
        results = await search_tavily(query)
        
        for result in results:
            lead = {
                "company_name": result.get("title", "").split(" - ")[0].split(" | ")[0],
                "url": result.get("url"),
                "description": result.get("content", "")[:200],
                "source": "Tavily",
                "found_at": datetime.now().isoformat()
            }
            
            # Calculate score
            lead["lead_score"] = calculate_lead_score(lead, "tavily")
            lead["priority"] = "High" if lead["lead_score"] >= 70 else "Medium" if lead["lead_score"] >= 50 else "Low"
            
            leads.append(lead)
    
    metrics["tavily_results"] = len(leads)
    
    # If Tavily didn't return enough, try Brave
    if len(leads) < 20:
        print(f"⚠️ Tavily only returned {len(leads)} results, trying Brave Search...")
        
        for query in queries[3:]:
            results = await search_brave(query)
            
            for result in results:
                lead = {
                    "company_name": result.get("title", "").split(" - ")[0].split(" | ")[0],
                    "url": result.get("url"),
                    "description": result.get("description", "")[:200],
                    "source": "Brave Search",
                    "found_at": datetime.now().isoformat()
                }
                
                # Calculate score
                lead["lead_score"] = calculate_lead_score(lead, "brave")
                lead["priority"] = "High" if lead["lead_score"] >= 70 else "Medium" if lead["lead_score"] >= 50 else "Low"
                
                leads.append(lead)
        
        metrics["brave_results"] = len(leads) - metrics["tavily_results"]
    
    return leads[:30]  # Return max 30 leads

def save_leads(leads: list):
    """Save leads to markdown file."""
    LEADS_DIR.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    filename = LEADS_DIR / f"daily-leads-{today}.md"
    
    # Calculate stats
    high_priority = [l for l in leads if l.get("lead_score", 0) >= 70]
    
    content = f"""# Daily Lead Report - {today}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📊 Summary

- **Total Leads:** {len(leads)}
- **High Priority (70+):** {len(high_priority)}
- **Data Source:** {"Scrapling ✅" if metrics["scrapling_used"] else "Traditional APIs"}

### Source Breakdown
- Scrapling: {metrics["scrapling_results"]} leads
- Tavily: {metrics["tavily_results"]} leads
- Brave Search: {metrics["brave_results"]} leads

## 🔍 Top 3 High-Priority Leads

"""
    
    # Add top 3
    sorted_leads = sorted(leads, key=lambda x: x.get("lead_score", 0), reverse=True)
    for i, lead in enumerate(sorted_leads[:3], 1):
        content += f"""
### {i}. {lead.get('company_name', 'Unknown')}

- **Score:** {lead.get('lead_score', 0)}/100
- **Priority:** {lead.get('priority', 'Medium')}
- **URL:** {lead.get('url', 'N/A')}
- **Source:** {lead.get('source', 'Unknown')}
- **Description:** {lead.get('description', 'N/A')[:150]}...

"""
    
    # Add all leads
    content += "\n## 📋 All Leads\n\n"
    
    for lead in sorted_leads:
        emoji = "🟢" if lead.get("lead_score", 0) >= 70 else "🟡" if lead.get("lead_score", 0) >= 50 else "🔴"
        content += f"""
{emoji} **{lead.get('company_name', 'Unknown')}** (Score: {lead.get('lead_score', 0)})
   - URL: {lead.get('url', 'N/A')}
   - Source: {lead.get('source', 'Unknown')}
   - Description: {lead.get('description', 'N/A')[:100]}...

"""
    
    # Add metrics report
    elapsed_time = time.time() - metrics["start_time"]
    content += f"""
## 📈 Performance Metrics

- **Processing Time:** {elapsed_time:.1f} seconds
- **Scrapling Used:** {"✅ Yes" if metrics["scrapling_used"] else "❌ No"}
- **API Calls:**
  - Tavily: {"Yes" if metrics["tavily_results"] > 0 else "No"}
  - Brave Search: {"Yes" if metrics["brave_results"] > 0 else "No"}

---
Generated by Enhanced Lead Gen v2 (Scrapling-First)
"""
    
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"✅ Saved {len(leads)} leads to {filename}")
    return filename

async def main():
    """Main execution."""
    print("=" * 60)
    print("Enhanced Lead Gen v2 - Scrapling-First")
    print("=" * 60)
    
    # Step 1: Try Scrapling first
    leads = await try_scrapling()
    
    # Step 2: Fall back to APIs if needed
    if not leads:
        print("\n⚠️ Scrapling returned no results, falling back to APIs...")
        leads = await generate_leads_with_apis()
    
    # Step 3: Process and save
    if leads:
        metrics["total_leads"] = len(leads)
        filename = save_leads(leads)
        
        # Prepare summary for Discord
        elapsed_time = time.time() - metrics["start_time"]
        high_priority = len([l for l in leads if l.get("lead_score", 0) >= 70])
        
        summary = f"""# Enhanced Lead Gen v2 Complete

## Results
- **Total Leads:** {len(leads)}
- **High Priority (70+):** {high_priority}
- **Processing Time:** {elapsed_time:.1f} seconds

## Data Source Report
- **Scrapling Used:** {"✅ Yes" if metrics["scrapling_used"] else "❌ No"}
- **Scrapling Results:** {metrics["scrapling_results"]} leads
- **Tavily Results:** {metrics["tavily_results"]} leads
- **Brave Search Results:** {metrics["brave_results"]} leads

## Top 3 Companies
"""
        
        sorted_leads = sorted(leads, key=lambda x: x.get("lead_score", 0), reverse=True)
        for i, lead in enumerate(sorted_leads[:3], 1):
            summary += f"\n{i}. **{lead.get('company_name', 'Unknown')}** (Score: {lead.get('lead_score', 0)}) - {lead.get('source')}"
        
        summary += f"\n\n📁 **Full Report:** `{filename}`"
        
        print("\n" + "=" * 60)
        print(summary)
        print("=" * 60)
        
        return summary
    else:
        return "❌ No leads generated"

if __name__ == "__main__":
    result = asyncio.run(main())
    print(result)
