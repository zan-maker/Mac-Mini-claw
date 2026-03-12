#!/usr/bin/env python3
"""
Enhanced Lead Gen v2 - Scrapling-First Approach
Tries Scrapling first, falls back to Tavily, then Brave Search
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Try Scrapling first
SCRAPLING_AVAILABLE = False
try:
    sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')
    from cron_integration import ScraplingCronIntegration
    SCRAPLING_AVAILABLE = True
    print("✅ Scrapling module available")
except ImportError as e:
    print(f"⚠️ Scrapling not available: {e}")

async def try_scrapling():
    """Try to generate leads using Scrapling."""
    if not SCRAPLING_AVAILABLE:
        return None, "Scrapling module not available"
    
    try:
        print("\n🔍 Attempting Scrapling integration...")
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if not success:
            return None, "Scrapling initialization failed"
        
        print("✅ Scrapling initialized successfully")
        
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
        
        if leads and len(leads) > 0:
            print(f"✅ Scrapling found {len(leads)} leads")
            return leads, "Scrapling"
        else:
            return None, "Scrapling returned no results"
            
    except Exception as e:
        return None, f"Scrapling error: {str(e)}"

async def try_tavily():
    """Fall back to Tavily API."""
    import aiohttp
    
    print("\n🔄 Falling back to Tavily API...")
    
    api_key = "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"
    
    search_queries = [
        "manufacturing companies 50-200 employees Texas",
        "technology companies 20-100 employees California",
        "healthcare companies 30-150 employees Florida",
        "professional services firms 25-75 employees New York"
    ]
    
    leads = []
    
    async with aiohttp.ClientSession() as session:
        for query in search_queries:
            try:
                url = "https://api.tavily.com/search"
                payload = {
                    "api_key": api_key,
                    "query": query,
                    "search_depth": "basic",
                    "max_results": 10
                }
                
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = data.get("results", [])
                        
                        for result in results:
                            lead = {
                                "company_name": result.get("title", "Unknown"),
                                "url": result.get("url", ""),
                                "description": result.get("content", ""),
                                "source": "Tavily",
                                "lead_score": 0
                            }
                            leads.append(lead)
                    else:
                        print(f"⚠️ Tavily error: {response.status}")
                        
            except Exception as e:
                print(f"⚠️ Tavily query error: {e}")
    
    if leads:
        print(f"✅ Tavily found {len(leads)} leads")
        return leads, "Tavily"
    return None, "Tavily returned no results"

async def try_brave_search():
    """Fall back to Brave Search API (Serper)."""
    import aiohttp
    
    print("\n🔄 Falling back to Brave Search (Serper)...")
    
    api_key = "cac43a248afb1cc1ec004370df2e0282a67eb420"
    
    search_queries = [
        "manufacturing companies 50-200 employees Texas",
        "technology companies 20-100 employees California",
        "healthcare companies 30-150 employees Florida",
        "professional services firms 25-75 employees New York"
    ]
    
    leads = []
    
    async with aiohttp.ClientSession() as session:
        for query in search_queries:
            try:
                url = "https://google.serper.dev/search"
                headers = {"X-API-KEY": api_key}
                payload = {"q": query}
                
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        organic = data.get("organic", [])
                        
                        for result in organic:
                            lead = {
                                "company_name": result.get("title", "Unknown"),
                                "url": result.get("link", ""),
                                "description": result.get("snippet", ""),
                                "source": "Brave Search",
                                "lead_score": 0
                            }
                            leads.append(lead)
                    else:
                        print(f"⚠️ Brave Search error: {response.status}")
                        
            except Exception as e:
                print(f"⚠️ Brave Search query error: {e}")
    
    if leads:
        print(f"✅ Brave Search found {len(leads)} leads")
        return leads, "Brave Search"
    return None, "Brave Search returned no results"

def score_lead(lead):
    """Score lead from 0-100 for expense reduction fit."""
    score = 0
    
    # Size fit (25 points) - look for employee indicators
    description = lead.get("description", "").lower()
    title = lead.get("company_name", "").lower()
    text = description + " " + title
    
    if any(x in text for x in ["50-200", "100+", "mid-size", "medium"]):
        score += 25
    elif any(x in text for x in ["20-100", "small", "growing"]):
        score += 20
    elif any(x in text for x in ["enterprise", "large"]):
        score += 10
    
    # Industry match (25 points)
    industries = {
        "manufacturing": ["manufacturing", "industrial", "factory", "production"],
        "technology": ["technology", "software", "saas", "tech", "it"],
        "healthcare": ["healthcare", "medical", "hospital", "health"],
        "professional": ["professional", "services", "consulting", "agency"]
    }
    
    for industry, keywords in industries.items():
        if any(kw in text for kw in keywords):
            score += 25
            lead["industry"] = industry.title()
            break
    else:
        score += 10
        lead["industry"] = "Other"
    
    # Contact found (25 points) - check URL structure
    url = lead.get("url", "")
    if "contact" in url or "about" in url:
        score += 25
    elif url:
        score += 15
    
    # Intent signal (25 points)
    if any(x in text for x in ["growing", "expanding", "hiring", "new location"]):
        score += 25
    elif any(x in text for x in ["services", "solutions", "provider"]):
        score += 15
    
    lead["lead_score"] = min(score, 100)
    lead["priority"] = "High" if score >= 70 else "Medium" if score >= 50 else "Low"
    
    return lead

async def main():
    """Main execution - try Scrapling, then Tavily, then Brave Search."""
    start_time = datetime.now()
    
    print("=" * 60)
    print("Enhanced Lead Gen v2 - Scrapling-First")
    print("=" * 60)
    print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Try each source in order
    leads = None
    source_used = None
    
    # 1. Try Scrapling
    leads, source_used = await try_scrapling()
    
    # 2. Fall back to Tavily
    if not leads:
        leads, source_used = await try_tavily()
    
    # 3. Fall back to Brave Search
    if not leads:
        leads, source_used = await try_brave_search()
    
    # Process results
    if not leads:
        print("\n❌ No leads found from any source")
        return {
            "success": False,
            "leads": [],
            "source": "None",
            "message": "All sources failed"
        }
    
    print(f"\n📊 Processing {len(leads)} leads from {source_used}...")
    
    # Score leads
    scored_leads = [score_lead(lead) for lead in leads]
    
    # Sort by score
    scored_leads.sort(key=lambda x: x["lead_score"], reverse=True)
    
    # Limit to top 30
    top_leads = scored_leads[:30]
    
    # Calculate stats
    high_priority = len([l for l in top_leads if l["priority"] == "High"])
    medium_priority = len([l for l in top_leads if l["priority"] == "Medium"])
    low_priority = len([l for l in top_leads if l["priority"] == "Low"])
    avg_score = sum(l["lead_score"] for l in top_leads) / len(top_leads) if top_leads else 0
    
    # Save to file
    output_dir = Path("/Users/cubiczan/.openclaw/workspace/leads")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"daily-leads-{datetime.now().strftime('%Y-%m-%d')}.md"
    
    with open(output_file, "w") as f:
        f.write(f"# Daily Leads - {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(f"**Source:** {source_used}\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Leads:** {len(top_leads)}\n")
        f.write(f"**High Priority:** {high_priority}\n")
        f.write(f"**Average Score:** {avg_score:.1f}\n\n")
        
        f.write("## Summary\n\n")
        f.write(f"- High Priority (70+): {high_priority}\n")
        f.write(f"- Medium Priority (50-69): {medium_priority}\n")
        f.write(f"- Low Priority (<50): {low_priority}\n\n")
        
        f.write("## Top 3 Leads\n\n")
        for i, lead in enumerate(top_leads[:3], 1):
            f.write(f"### {i}. {lead['company_name']}\n")
            f.write(f"- **Score:** {lead['lead_score']}/100\n")
            f.write(f"- **Priority:** {lead['priority']}\n")
            f.write(f"- **Industry:** {lead.get('industry', 'N/A')}\n")
            f.write(f"- **URL:** {lead['url']}\n")
            f.write(f"- **Description:** {lead['description'][:150]}...\n\n")
        
        f.write("## All Leads\n\n")
        for i, lead in enumerate(top_leads, 1):
            f.write(f"{i}. **{lead['company_name']}** (Score: {lead['lead_score']}, Priority: {lead['priority']})\n")
            f.write(f"   - Industry: {lead.get('industry', 'N/A')}\n")
            f.write(f"   - URL: {lead['url']}\n\n")
    
    print(f"✅ Leads saved to: {output_file}")
    
    # Calculate processing time
    end_time = datetime.now()
    processing_time = (end_time - start_time).total_seconds()
    
    # Prepare result
    result = {
        "success": True,
        "source": source_used,
        "scrapling_used": source_used == "Scrapling",
        "total_leads": len(top_leads),
        "high_priority": high_priority,
        "medium_priority": medium_priority,
        "low_priority": low_priority,
        "average_score": round(avg_score, 1),
        "processing_time_seconds": round(processing_time, 1),
        "top_leads": [
            {
                "name": l["company_name"],
                "score": l["lead_score"],
                "priority": l["priority"],
                "industry": l.get("industry", "N/A")
            }
            for l in top_leads[:3]
        ],
        "output_file": str(output_file)
    }
    
    print("\n" + "=" * 60)
    print("RESULT SUMMARY")
    print("=" * 60)
    print(json.dumps(result, indent=2))
    
    return result

if __name__ == "__main__":
    result = asyncio.run(main())
