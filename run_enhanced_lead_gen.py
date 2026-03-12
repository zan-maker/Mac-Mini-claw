#!/usr/bin/env python3
"""
Enhanced Lead Gen v2 - Scrapling-First Approach
Generates 20-30 leads quickly using Scrapling, with fallback to Tavily/Brave APIs.
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from pathlib import Path
import aiohttp
import time

# Add Scrapling integration to path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# API Keys
SERPER_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"
TAVILY_API_KEY = "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"
ZEROBOUNCE_API_KEY = "fd0105c8c98340e0a2b63e2fbe39d7a4"

# Stats tracking
stats = {
    "scrapling_used": False,
    "scrapling_results": 0,
    "tavily_results": 0,
    "brave_results": 0,
    "total_time": 0,
    "start_time": time.time()
}


async def try_scrapling_first():
    """Try Scrapling integration first."""
    print("\n🔍 ATTEMPTING SCRAPLING INTEGRATION...")
    
    try:
        from cron_integration import ScraplingCronIntegration
        
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if success:
            print("✅ Scrapling initialized successfully")
            stats["scrapling_used"] = True
            
            # Search queries for different industries and regions
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
                stats["scrapling_results"] = len(leads)
                print(f"✅ Scrapling found {len(leads)} leads")
                return leads
            else:
                print("⚠️ Scrapling returned no results, falling back to APIs")
                return []
        else:
            print("⚠️ Scrapling initialization failed, falling back to APIs")
            return []
            
    except ImportError as e:
        print(f"⚠️ Scrapling not available: {e}")
        print("⚠️ Falling back to traditional APIs")
        return []
    except Exception as e:
        print(f"❌ Scrapling error: {e}")
        return []


async def search_tavily(query: str):
    """Search using Tavily API (preferred fallback)."""
    print(f"\n🔍 Searching Tavily: {query}")
    
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "max_results": 10
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=15)) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get("results", [])
                    print(f"✅ Tavily found {len(results)} results")
                    return results
                else:
                    print(f"❌ Tavily error: {response.status}")
                    return []
    except Exception as e:
        print(f"❌ Tavily error: {e}")
        return []


async def search_brave(query: str):
    """Search using Brave Search API (second fallback)."""
    print(f"\n🔍 Searching Brave: {query}")
    
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY}
    payload = {"q": query}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as response:
                if response.status == 200:
                    data = await response.json()
                    organic = data.get("organic", [])
                    print(f"✅ Brave found {len(organic)} results")
                    return organic
                else:
                    print(f"❌ Brave error: {response.status}")
                    return []
    except Exception as e:
        print(f"❌ Brave error: {e}")
        return []


def score_lead(company: dict) -> int:
    """Quick lead scoring (0-100)."""
    score = 0
    
    # Size fit (50-200 employees): 25 pts
    size = str(company.get("snippet", "") + company.get("title", "")).lower()
    if any(x in size for x in ["50-200", "100+", "150+", "200"]):
        score += 25
    elif any(x in size for x in ["50", "75", "100"]):
        score += 20
    elif any(x in size for x in ["20", "30", "40"]):
        score += 15
    
    # Industry match: 25 pts
    if any(x in size for x in ["manufacturing", "technology", "healthcare", "professional services"]):
        score += 25
    elif any(x in size for x in ["services", "company", "inc", "corp"]):
        score += 15
    
    # Contact found: 25 pts (check if domain looks valid)
    link = company.get("link", "")
    if link and not any(x in link for x in ["linkedin", "facebook", "twitter"]):
        score += 25
    
    # Intent signal: 25 pts
    if any(x in size for x in ["growing", "hiring", "expanding", "new"]):
        score += 25
    
    return min(score, 100)


async def generate_leads_with_apis():
    """Generate leads using traditional APIs."""
    print("\n🔄 FALLING BACK TO TRADITIONAL APIs...")
    
    all_leads = []
    
    # Search queries
    queries = [
        "manufacturing companies 50-200 employees Texas",
        "technology companies 20-100 employees California",
        "healthcare companies 30-150 employees Florida",
        "professional services firms 25-75 employees New York"
    ]
    
    # Try Tavily first
    for query in queries:
        if len(all_leads) >= 30:
            break
        
        results = await search_tavily(query)
        
        if not results:
            # Fallback to Brave
            results = await search_brave(query)
            stats["brave_results"] += len(results)
        else:
            stats["tavily_results"] += len(results)
        
        # Process results
        for result in results:
            if len(all_leads) >= 30:
                break
            
            lead = {
                "company_name": result.get("title", "").split(" - ")[0].split(" | ")[0],
                "url": result.get("link", ""),
                "snippet": result.get("snippet", ""),
                "lead_score": score_lead(result),
                "source": "Tavily" if result in results else "Brave"
            }
            
            # Determine priority
            lead["priority"] = "High" if lead["lead_score"] >= 70 else "Medium" if lead["lead_score"] >= 50 else "Low"
            
            all_leads.append(lead)
    
    return all_leads


async def save_leads(leads: list):
    """Save leads to daily file."""
    if not leads:
        print("⚠️ No leads to save")
        return None
    
    # Create leads directory
    leads_dir = Path("/Users/cubiczan/.openclaw/workspace/leads")
    leads_dir.mkdir(exist_ok=True)
    
    # Create daily file
    today = datetime.now().strftime("%Y-%m-%d")
    filename = leads_dir / f"daily-leads-{today}.md"
    
    # Sort by score
    leads_sorted = sorted(leads, key=lambda x: x.get("lead_score", 0), reverse=True)
    
    # Generate markdown
    content = f"""# Daily Leads - {today}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Total Leads: {len(leads)}
High Priority (70+): {sum(1 for l in leads if l.get("lead_score", 0) >= 70)}

## 🔍 Data Source Report
- Scrapling Used: {"✅ Yes" if stats["scrapling_used"] else "❌ No"}
- Scrapling Results: {stats["scrapling_results"]}
- Tavily API Results: {stats["tavily_results"]}
- Brave Search Results: {stats["brave_results"]}
- Total Processing Time: {time.time() - stats["start_time"]:.1f} seconds

---

"""
    
    # Add high priority leads first
    high_priority = [l for l in leads_sorted if l.get("lead_score", 0) >= 70]
    if high_priority:
        content += "## 🔥 High Priority Leads\n\n"
        for i, lead in enumerate(high_priority[:10], 1):
            content += f"### {i}. {lead.get('company_name', 'Unknown')}\n"
            content += f"- **Score:** {lead.get('lead_score', 0)}/100\n"
            content += f"- **Priority:** {lead.get('priority', 'Medium')}\n"
            content += f"- **URL:** {lead.get('url', 'N/A')}\n"
            content += f"- **Source:** {lead.get('source', 'Unknown')}\n"
            if lead.get('snippet'):
                content += f"- **Details:** {lead.get('snippet')[:200]}\n"
            content += "\n"
    
    # Add all leads
    content += f"\n## 📋 All Leads ({len(leads)} total)\n\n"
    for i, lead in enumerate(leads_sorted, 1):
        content += f"{i}. **{lead.get('company_name', 'Unknown')}** (Score: {lead.get('lead_score', 0)})\n"
    
    # Write file
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"✅ Saved {len(leads)} leads to {filename}")
    return filename


async def main():
    """Main execution."""
    print("=" * 60)
    print("🚀 Enhanced Lead Gen v2 - Scrapling-First Approach")
    print("=" * 60)
    
    # Step 1: Try Scrapling first
    leads = await try_scrapling_first()
    
    # Step 2: Fall back to APIs if needed
    if not leads or len(leads) < 20:
        print(f"\n⚠️ Scrapling returned {len(leads)} leads, trying APIs...")
        api_leads = await generate_leads_with_apis()
        leads.extend(api_leads)
    
    # Step 3: Process and save
    if leads:
        filename = await save_leads(leads)
        
        # Calculate final stats
        stats["total_time"] = time.time() - stats["start_time"]
        
        # Prepare summary
        high_priority = sum(1 for l in leads if l.get("lead_score", 0) >= 70)
        top_3 = sorted(leads, key=lambda x: x.get("lead_score", 0), reverse=True)[:3]
        
        summary = f"""
✅ **Lead Generation Complete**

**Results:**
- Total Found: {len(leads)}
- High Priority (70+): {high_priority}
- Processing Time: {stats["total_time"]:.1f}s

**🔍 Data Source Report:**
- Scrapling Used: {"✅ Yes" if stats["scrapling_used"] else "❌ No"}
- Scrapling Results: {stats["scrapling_results"]}
- Tavily API Results: {stats["tavily_results"]}
- Brave Search Results: {stats["brave_results"]}

**🏆 Top 3 Companies:**
"""
        
        for i, lead in enumerate(top_3, 1):
            summary += f"\n{i}. **{lead.get('company_name', 'Unknown')}** (Score: {lead.get('lead_score', 0)})"
        
        summary += f"\n\n📁 **Saved to:** `{filename}`"
        
        print(summary)
        return summary
    else:
        return "❌ No leads generated"


if __name__ == "__main__":
    result = asyncio.run(main())
    print(result)
