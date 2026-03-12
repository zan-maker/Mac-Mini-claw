#!/usr/bin/env python3
"""
Enhanced Lead Gen v2 - Better Search Queries
Focuses on finding actual companies, not directory pages.
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from pathlib import Path
import aiohttp
import time
import re

# API Keys
TAVILY_API_KEY = "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"
SERPER_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"

# Stats
stats = {
    "scrapling_used": False,
    "scrapling_results": 0,
    "tavily_results": 0,
    "brave_results": 0,
    "total_time": 0,
    "start_time": time.time()
}


async def search_tavily(query: str):
    """Search using Tavily API."""
    print(f"\n🔍 Searching: {query}")
    
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "max_results": 10,
        "include_domains": [],  # Include all domains
        "exclude_domains": ["linkedin.com", "facebook.com", "twitter.com", "instagram.com", "crunchbase.com", "zoominfo.com", "glassdoor.com", "indeed.com"]
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=15)) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get("results", [])
                    # Filter out directory pages
                    filtered = [r for r in results if not any(x in r.get("url", "").lower() for x in ["top", "list", "best", "directory"])]
                    print(f"✅ Found {len(filtered)} relevant results (filtered from {len(results)})")
                    return filtered
                else:
                    print(f"❌ Error: {response.status}")
                    return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


def extract_company_info(result: dict) -> dict:
    """Extract company information from search result."""
    title = result.get("title", "")
    url = result.get("url", "")
    snippet = result.get("content", "") or result.get("snippet", "")
    
    # Extract company name (usually first part before dash or pipe)
    company_name = title.split(" - ")[0].split(" | ")[0].split(" · ")[0].strip()
    
    # Clean up common suffixes
    for suffix in ["Inc", "LLC", "Corp", "Company", "Ltd", "Co"]:
        if company_name.endswith(f" {suffix}"):
            company_name = company_name[:-len(f" {suffix}")].strip()
    
    return {
        "company_name": company_name,
        "url": url,
        "snippet": snippet,
        "title": title
    }


def score_lead(company: dict) -> int:
    """Score lead 0-100."""
    score = 0
    text = f"{company.get('title', '')} {company.get('snippet', '')}".lower()
    url = company.get("url", "").lower()
    
    # Size indicators (25 pts)
    size_keywords = {
        "50-200": 25,
        "100+": 25,
        "150+": 25,
        "200": 20,
        "100": 15,
        "50": 15,
        "75": 15,
        "medium": 15,
        "mid-size": 15,
        "growing": 20
    }
    for keyword, points in size_keywords.items():
        if keyword in text:
            score += points
            break
    
    # Industry match (25 pts)
    industry_keywords = {
        "manufacturing": 25,
        "technology": 25,
        "software": 25,
        "healthcare": 25,
        "medical": 25,
        "professional services": 25,
        "consulting": 20,
        "engineering": 20,
        "industrial": 20
    }
    for keyword, points in industry_keywords.items():
        if keyword in text:
            score += points
            break
    
    # Valid company URL (25 pts)
    if url and not any(x in url for x in ["linkedin", "facebook", "twitter", "crunchbase", "zoominfo", "glassdoor", "indeed", "yelp", "yellowpages"]):
        # Check if it looks like a real company site
        if any(x in url for x in [".com", ".io", ".net", ".org"]):
            score += 25
    
    # Intent signals (25 pts)
    intent_keywords = ["hiring", "expanding", "growing", "new location", "new facility", "investment", "funding"]
    for keyword in intent_keywords:
        if keyword in text:
            score += 25
            break
    
    return min(score, 100)


async def generate_leads():
    """Generate leads with better search queries."""
    print("=" * 60)
    print("🚀 Enhanced Lead Gen v2 - Better Search Strategy")
    print("=" * 60)
    
    all_leads = []
    
    # Better search queries - specific company types
    queries = [
        # Manufacturing - specific types
        "precision manufacturing company Texas site:.com",
        "industrial equipment manufacturer California site:.com",
        "metal fabrication company Florida site:.com",
        "plastics manufacturing New York site:.com",
        
        # Technology - specific types
        "enterprise software company Texas employees site:.com",
        "SaaS company California 100 employees site:.com",
        "IT services company Florida site:.com",
        "cloud computing company New York site:.com",
        
        # Healthcare - specific types
        "medical devices company Texas site:.com",
        "healthcare technology Florida site:.com",
        "biotech company California site:.com",
        "pharmaceutical company New York site:.com",
        
        # Professional services
        "consulting firm Texas employees site:.com",
        "engineering services California site:.com",
        "professional services firm Florida site:.com"
    ]
    
    seen_urls = set()
    
    for query in queries[:6]:  # Limit to first 6 to stay under 15 min
        if len(all_leads) >= 30:
            break
        
        results = await search_tavily(query)
        
        for result in results:
            url = result.get("url", "")
            
            # Skip duplicates
            if url in seen_urls:
                continue
            seen_urls.add(url)
            
            # Extract company info
            company = extract_company_info(result)
            
            # Score the lead
            score = score_lead({**company, "url": url})
            
            lead = {
                **company,
                "url": url,
                "lead_score": score,
                "priority": "High" if score >= 70 else "Medium" if score >= 50 else "Low",
                "source": "Tavily"
            }
            
            stats["tavily_results"] += 1
            all_leads.append(lead)
            
            if len(all_leads) >= 30:
                break
        
        # Small delay between requests
        await asyncio.sleep(0.5)
    
    return all_leads


async def save_leads(leads: list):
    """Save leads to daily file."""
    if not leads:
        return None
    
    leads_dir = Path("/Users/cubiczan/.openclaw/workspace/leads")
    leads_dir.mkdir(exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    filename = leads_dir / f"daily-leads-{today}.md"
    
    leads_sorted = sorted(leads, key=lambda x: x.get("lead_score", 0), reverse=True)
    
    high_priority = [l for l in leads_sorted if l.get("lead_score", 0) >= 70]
    medium_priority = [l for l in leads_sorted if 50 <= l.get("lead_score", 0) < 70]
    
    content = f"""# Daily Leads - {today}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Total Leads: {len(leads)}
High Priority (70+): {len(high_priority)}
Medium Priority (50-69): {len(medium_priority)}

## 🔍 Data Source Report
- Scrapling Used: {"✅ Yes" if stats["scrapling_used"] else "❌ No"}
- Scrapling Results: {stats["scrapling_results"]}
- Tavily API Results: {stats["tavily_results"]}
- Brave Search Results: {stats["brave_results"]}
- Total Processing Time: {time.time() - stats["start_time"]:.1f} seconds

---
"""
    
    if high_priority:
        content += "\n## 🔥 High Priority Leads\n\n"
        for i, lead in enumerate(high_priority, 1):
            content += f"### {i}. {lead.get('company_name', 'Unknown')}\n"
            content += f"- **Score:** {lead.get('lead_score', 0)}/100\n"
            content += f"- **Priority:** {lead.get('priority', 'Medium')}\n"
            content += f"- **URL:** {lead.get('url', 'N/A')}\n"
            content += f"- **Source:** {lead.get('source', 'Unknown')}\n"
            if lead.get('snippet'):
                content += f"- **Details:** {lead.get('snippet')[:200]}\n"
            content += "\n"
    
    if medium_priority:
        content += "\n## 📊 Medium Priority Leads\n\n"
        for i, lead in enumerate(medium_priority, 1):
            content += f"### {i}. {lead.get('company_name', 'Unknown')}\n"
            content += f"- **Score:** {lead.get('lead_score', 0)}/100\n"
            content += f"- **URL:** {lead.get('url', 'N/A')}\n"
            if lead.get('snippet'):
                content += f"- **Details:** {lead.get('snippet')[:150]}\n"
            content += "\n"
    
    content += f"\n## 📋 All Leads ({len(leads)} total)\n\n"
    for i, lead in enumerate(leads_sorted, 1):
        content += f"{i}. **{lead.get('company_name', 'Unknown')}** - Score: {lead.get('lead_score', 0)} - [{lead.get('url', 'N/A')}]({lead.get('url', '')})\n"
    
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"\n✅ Saved {len(leads)} leads to {filename}")
    return filename


async def main():
    """Main execution."""
    leads = await generate_leads()
    
    if leads:
        filename = await save_leads(leads)
        
        stats["total_time"] = time.time() - stats["start_time"]
        
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
            summary += f"\n{i}. **{lead.get('company_name', 'Unknown')}** (Score: {lead.get('lead_score', 0)})\n   {lead.get('url', '')}"
        
        summary += f"\n\n📁 **Saved to:** `{filename}`"
        
        print(summary)
        return summary
    else:
        return "❌ No leads generated"


if __name__ == "__main__":
    result = asyncio.run(main())
    print(result)
