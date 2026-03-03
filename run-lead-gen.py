#!/usr/bin/env python3
"""Enhanced Lead Gen v2 - Scrapling-First Approach"""
import sys
import os
import json
import asyncio
import aiohttp
from datetime import datetime
from pathlib import Path

# Add Scrapling to path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# API Keys
SERPER_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"
TAVILY_API_KEY = "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"

# Track data sources
data_source = {
    "scrapling_used": False,
    "scrapling_results": 0,
    "tavily_results": 0,
    "serper_results": 0,
    "start_time": datetime.now()
}

async def try_scrapling():
    """Try Scrapling integration first"""
    try:
        from cron_integration import ScraplingCronIntegration
        
        print("🔍 Attempting Scrapling integration...")
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if success:
            print("✅ Scrapling initialized successfully")
            data_source["scrapling_used"] = True
            
            # Search queries for expense reduction leads
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
                data_source["scrapling_results"] = len(leads)
                print(f"✅ Scrapling found {len(leads)} leads")
                return leads
            else:
                print("⚠️ Scrapling returned no results, falling back...")
                return []
        else:
            print("⚠️ Scrapling initialization failed")
            return []
    except Exception as e:
        print(f"⚠️ Scrapling error: {e}")
        return []

async def search_tavily(query):
    """Fallback to Tavily API"""
    print(f"🔍 Searching Tavily: {query}")
    
    async with aiohttp.ClientSession() as session:
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "basic",
            "max_results": 10
        }
        
        try:
            async with session.post("https://api.tavily.com/search", json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("results", [])
        except Exception as e:
            print(f"⚠️ Tavily error: {e}")
    return []

async def search_serper(query):
    """Second fallback to Serper API"""
    print(f"🔍 Searching Serper: {query}")
    
    async with aiohttp.ClientSession() as session:
        headers = {"X-API-KEY": SERPER_API_KEY}
        payload = {"q": query}
        
        try:
            async with session.post("https://google.serper.dev/search", 
                                   json=payload, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    # Extract organic results
                    results = data.get("organic", [])
                    return [{"title": r.get("title"), "link": r.get("link"), 
                            "snippet": r.get("snippet")} for r in results]
        except Exception as e:
            print(f"⚠️ Serper error: {e}")
    return []

def score_lead(company_data):
    """Quick scoring (0-100)"""
    score = 0
    
    # Size fit (50-200 employees): 25 pts
    size = company_data.get("employees", 0)
    if 50 <= size <= 200:
        score += 25
    elif 20 <= size <= 300:
        score += 15
    
    # Industry match: 25 pts
    industry = company_data.get("industry", "").lower()
    target_industries = ["manufacturing", "technology", "healthcare", "professional services", 
                        "logistics", "finance", "retail"]
    if any(ind in industry for ind in target_industries):
        score += 25
    
    # Contact found: 25 pts
    if company_data.get("contact_email") or company_data.get("contact_phone"):
        score += 25
    
    # Intent signal: 25 pts
    snippet = company_data.get("snippet", "").lower()
    intent_signals = ["hiring", "expanding", "growth", "new location", "funding", "investment"]
    if any(signal in snippet for signal in intent_signals):
        score += 25
    
    return min(score, 100)

async def generate_leads():
    """Main lead generation function"""
    print("🚀 Enhanced Lead Gen v2 - Scrapling-First")
    print("=" * 50)
    
    all_leads = []
    
    # Step 1: Try Scrapling first
    scrapling_leads = await try_scrapling()
    if scrapling_leads:
        all_leads.extend(scrapling_leads)
    
    # Step 2: Fallback to APIs if needed
    if len(all_leads) < 20:
        print("\n📊 Using traditional APIs as fallback...")
        
        search_queries = [
            "manufacturing companies 50-200 employees Texas",
            "technology companies 20-100 employees California",
            "healthcare companies 30-150 employees Florida",
            "professional services firms 25-75 employees New York"
        ]
        
        # Try Tavily first
        for query in search_queries[:2]:
            results = await search_tavily(query)
            if results:
                data_source["tavily_results"] += len(results)
                for r in results:
                    lead = {
                        "company": r.get("title", "Unknown"),
                        "snippet": r.get("content", r.get("snippet", "")),
                        "link": r.get("url", r.get("link", "")),
                        "industry": "unknown",
                        "employees": 0
                    }
                    lead["score"] = score_lead(lead)
                    all_leads.append(lead)
        
        # If still need more, try Serper
        if len(all_leads) < 20:
            for query in search_queries[2:]:
                results = await search_serper(query)
                if results:
                    data_source["serper_results"] += len(results)
                    for r in results:
                        lead = {
                            "company": r.get("title", "Unknown"),
                            "snippet": r.get("snippet", ""),
                            "link": r.get("link", ""),
                            "industry": "unknown",
                            "employees": 0
                        }
                        lead["score"] = score_lead(lead)
                        all_leads.append(lead)
    
    # Sort by score
    all_leads.sort(key=lambda x: x.get("score", 0), reverse=True)
    
    # Limit to top 30
    top_leads = all_leads[:30]
    
    # Calculate processing time
    data_source["processing_time"] = (datetime.now() - data_source["start_time"]).total_seconds()
    
    return top_leads

def save_leads(leads):
    """Save leads to markdown file"""
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = Path("/Users/cubiczan/.openclaw/workspace/leads")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"daily-leads-{today}.md"
    
    with open(output_file, "w") as f:
        f.write(f"# Daily Leads - {today}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Leads:** {len(leads)}\n")
        f.write(f"**High Priority (70+):** {sum(1 for l in leads if l.get('score', 0) >= 70)}\n\n")
        
        f.write("## 🔍 Data Source Report\n")
        f.write(f"- **Scrapling Used:** {'✅ Yes' if data_source['scrapling_used'] else '❌ No'}\n")
        f.write(f"- **Scrapling Results:** {data_source['scrapling_results']} leads\n")
        f.write(f"- **Tavily Results:** {data_source['tavily_results']} leads\n")
        f.write(f"- **Serper Results:** {data_source['serper_results']} leads\n")
        f.write(f"- **Total Processing Time:** {data_source['processing_time']:.2f} seconds\n\n")
        
        f.write("## 📊 Top 3 Priority Leads\n\n")
        for i, lead in enumerate(leads[:3], 1):
            f.write(f"### {i}. {lead.get('company', 'Unknown')}\n")
            f.write(f"**Score:** {lead.get('score', 0)}/100\n")
            f.write(f"**Link:** {lead.get('link', 'N/A')}\n")
            f.write(f"**Snippet:** {lead.get('snippet', 'N/A')[:200]}...\n\n")
        
        f.write("## 📋 All Leads\n\n")
        for i, lead in enumerate(leads, 1):
            score = lead.get('score', 0)
            priority = "🔥" if score >= 70 else "⭐" if score >= 50 else "📌"
            f.write(f"{i}. {priority} **{lead.get('company', 'Unknown')}** (Score: {score})\n")
            f.write(f"   - {lead.get('snippet', 'N/A')[:150]}...\n")
            f.write(f"   - Link: {lead.get('link', 'N/A')}\n\n")
    
    print(f"✅ Saved {len(leads)} leads to {output_file}")
    return output_file

async def main():
    """Main execution"""
    try:
        leads = await generate_leads()
        
        if leads:
            output_file = save_leads(leads)
            
            # Print summary
            print("\n" + "=" * 50)
            print("📊 LEAD GENERATION SUMMARY")
            print("=" * 50)
            print(f"✅ Total Found: {len(leads)}")
            print(f"🔥 High Priority (70+): {sum(1 for l in leads if l.get('score', 0) >= 70)}")
            print(f"⭐ Medium Priority (50-69): {sum(1 for l in leads if 50 <= l.get('score', 0) < 70)}")
            print(f"\n🔍 Data Source Report:")
            print(f"  - Scrapling Used: {'✅ Yes' if data_source['scrapling_used'] else '❌ No'}")
            print(f"  - Scrapling Results: {data_source['scrapling_results']}")
            print(f"  - Tavily Results: {data_source['tavily_results']}")
            print(f"  - Serper Results: {data_source['serper_results']}")
            print(f"  - Processing Time: {data_source['processing_time']:.2f}s")
            
            print(f"\n🏆 Top 3 Companies:")
            for i, lead in enumerate(leads[:3], 1):
                print(f"  {i}. {lead.get('company', 'Unknown')} (Score: {lead.get('score', 0)})")
            
            # Return data for Discord report
            return {
                "total": len(leads),
                "high_priority": sum(1 for l in leads if l.get('score', 0) >= 70),
                "top_3": leads[:3],
                "data_source": data_source,
                "output_file": str(output_file)
            }
        else:
            print("❌ No leads generated")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(main())
    if result:
        print("\n" + json.dumps(result, indent=2, default=str))
