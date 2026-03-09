#!/usr/bin/env python3
"""
Defense Sector Lead Generation - Scrapling-First Approach
Generates leads for defense companies and PE/VC investors
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Add scrapling integration path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# Output directory
OUTPUT_DIR = Path('/Users/cubiczan/.openclaw/workspace/defense-leads')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Date string for filenames
DATE_STR = datetime.now().strftime('%Y-%m-%d')

# Results tracking
results = {
    "scrapling_used": False,
    "scrapling_companies": 0,
    "scrapling_investors": 0,
    "traditional_companies": 0,
    "traditional_investors": 0,
    "start_time": datetime.now().isoformat(),
    "end_time": None,
    "companies": [],
    "investors": []
}

async def try_scrapling():
    """Try to use Scrapling for data extraction."""
    print("🔍 Attempting Scrapling integration...")
    
    try:
        from cron_integration import ScraplingCronIntegration
        
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if not success:
            print("⚠️ Scrapling initialization failed")
            return False
        
        print("✅ Scrapling initialized successfully")
        
        # Search for defense companies
        search_terms = [
            "defense technology companies",
            "cybersecurity companies military",
            "drone technology defense",
            "space defense technology",
            "military AI companies"
        ]
        
        companies = await scrapling.scrape_defense_companies(search_terms)
        
        if companies:
            results["scrapling_used"] = True
            results["scrapling_companies"] = len(companies)
            results["companies"].extend(companies)
            print(f"✅ Scrapling found {len(companies)} companies")
            return True
        else:
            print("⚠️ Scrapling returned no results")
            return False
            
    except ImportError as e:
        print(f"⚠️ Scrapling not available: {e}")
        return False
    except Exception as e:
        print(f"❌ Scrapling error: {e}")
        return False

async def fallback_to_tavily():
    """Fall back to Tavily API for search."""
    print("\n📡 Falling back to Tavily API...")
    
    import aiohttp
    
    api_key = "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"
    
    # Defense company searches
    defense_queries = [
        "defense technology startups US UK EU Series A B C funding",
        "cybersecurity defense contractors early stage investment",
        "counter-drone C-UAS technology companies venture capital",
        "space defense satellite technology startups",
        "military AI machine learning defense companies investment"
    ]
    
    # PE/VC fund searches
    investor_queries = [
        "private equity defense technology fund India Singapore",
        "venture capital drone aerospace investment Asia",
        "defense tech PE fund Japan South Korea Taiwan",
        "aerospace defense investment firm Middle East Southeast Asia"
    ]
    
    companies = []
    investors = []
    
    async with aiohttp.ClientSession() as session:
        # Search for defense companies
        for query in defense_queries:
            try:
                payload = {
                    "api_key": api_key,
                    "query": query,
                    "search_depth": "advanced",
                    "max_results": 5
                }
                
                async with session.post("https://api.tavily.com/search", json=payload) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        for result in data.get("results", []):
                            companies.append({
                                "name": result.get("title", ""),
                                "url": result.get("url", ""),
                                "description": result.get("content", "")[:500],
                                "source": "Tavily"
                            })
                        print(f"  ✅ Found {len(data.get('results', []))} results for: {query[:50]}...")
                    else:
                        print(f"  ❌ Tavily error: {resp.status}")
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        # Search for investors
        for query in investor_queries:
            try:
                payload = {
                    "api_key": api_key,
                    "query": query,
                    "search_depth": "advanced",
                    "max_results": 5
                }
                
                async with session.post("https://api.tavily.com/search", json=payload) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        for result in data.get("results", []):
                            investors.append({
                                "name": result.get("title", ""),
                                "url": result.get("url", ""),
                                "description": result.get("content", "")[:500],
                                "source": "Tavily"
                            })
                        print(f"  ✅ Found {len(data.get('results', []))} results for: {query[:50]}...")
            except Exception as e:
                print(f"  ❌ Error: {e}")
    
    results["traditional_companies"] = len(companies)
    results["traditional_investors"] = len(investors)
    results["companies"].extend(companies)
    results["investors"].extend(investors)
    
    return len(companies) > 0 or len(investors) > 0

def score_defense_company(company):
    """Score a defense company (0-100)."""
    score = 0
    name = company.get("name", "").lower()
    desc = company.get("description", "").lower()
    url = company.get("url", "").lower()
    
    # Sector fit (0-30 pts)
    defense_keywords = ["defense", "military", "cyber", "security", "drone", "uas", "space", "satellite", "ai", "autonomous"]
    sector_score = sum(3 for kw in defense_keywords if kw in name or kw in desc)
    score += min(sector_score, 30)
    
    # Stage fit (0-20 pts) - look for funding stage indicators
    stage_keywords = ["series a", "series b", "series c", "seed", "early stage", "growth"]
    if any(kw in desc for kw in stage_keywords):
        score += 20
    elif "startup" in desc or "venture" in desc:
        score += 15
    
    # Technical depth (0-20 pts)
    tech_keywords = ["ai", "ml", "machine learning", "sensor", "encryption", "autonomous", "quantum", "edge computing"]
    tech_score = sum(4 for kw in tech_keywords if kw in desc)
    score += min(tech_score, 20)
    
    # Region match (0-10 pts)
    region_keywords = ["us", "united states", "uk", "united kingdom", "eu", "europe", "germany", "france", "uk"]
    if any(kw in desc or kw in url for kw in region_keywords):
        score += 10
    
    # Integration potential (0-20 pts) - dual-use potential
    if "dual-use" in desc or "commercial" in desc or "enterprise" in desc:
        score += 20
    elif "platform" in desc or "api" in desc:
        score += 15
    
    return min(score, 100)

def score_investor(investor):
    """Score a PE/VC fund (0-100)."""
    score = 0
    name = investor.get("name", "").lower()
    desc = investor.get("description", "").lower()
    
    # Defense/drone focus (0-40 pts)
    defense_keywords = ["defense", "military", "drone", "uav", "aerospace", "security", "surveillance", "autonomous"]
    defense_score = sum(5 for kw in defense_keywords if kw in name or kw in desc)
    score += min(defense_score, 40)
    
    # Region match (0-20 pts) - Asia/India focus
    region_keywords = ["india", "singapore", "japan", "korea", "taiwan", "southeast asia", "middle east", "asia"]
    region_score = sum(4 for kw in region_keywords if kw in desc)
    score += min(region_score, 20)
    
    # Portfolio fit (0-20 pts)
    portfolio_keywords = ["portfolio", "investment", "fund", "venture", "pe", "private equity"]
    if any(kw in name or kw in desc for kw in portfolio_keywords):
        score += 20
    
    # Fund size/stage (0-20 pts)
    if "growth" in desc or "series" in desc:
        score += 20
    elif "early" in desc or "seed" in desc:
        score += 15
    
    return min(score, 100)

def deduplicate_and_score():
    """Remove duplicates and score all results."""
    # Deduplicate companies by name
    seen_companies = set()
    unique_companies = []
    for company in results["companies"]:
        name = company.get("name", "").lower().strip()
        if name and name not in seen_companies:
            seen_companies.add(name)
            company["score"] = score_defense_company(company)
            unique_companies.append(company)
    
    # Deduplicate investors by name
    seen_investors = set()
    unique_investors = []
    for investor in results["investors"]:
        name = investor.get("name", "").lower().strip()
        if name and name not in seen_investors:
            seen_investors.add(name)
            investor["score"] = score_investor(investor)
            unique_investors.append(investor)
    
    # Sort by score
    unique_companies.sort(key=lambda x: x.get("score", 0), reverse=True)
    unique_investors.sort(key=lambda x: x.get("score", 0), reverse=True)
    
    results["companies"] = unique_companies
    results["investors"] = unique_investors

def save_results():
    """Save results to markdown files."""
    # Save companies
    companies_file = OUTPUT_DIR / f"daily-companies-{DATE_STR}.md"
    with open(companies_file, 'w') as f:
        f.write(f"# Defense Companies - {DATE_STR}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Leads:** {len(results['companies'])}\n")
        f.write(f"**High Priority (70+):** {sum(1 for c in results['companies'] if c.get('score', 0) >= 70)}\n\n")
        
        for i, company in enumerate(results["companies"][:15], 1):  # Top 15
            score = company.get("score", 0)
            priority = "🟢 High" if score >= 70 else "🟡 Medium" if score >= 50 else "⚪ Low"
            
            f.write(f"## {i}. {company.get('name', 'Unknown')}\n")
            f.write(f"**Score:** {score}/100 | **Priority:** {priority}\n\n")
            f.write(f"**URL:** {company.get('url', 'N/A')}\n\n")
            f.write(f"**Description:**\n{company.get('description', 'N/A')[:300]}...\n\n")
            f.write(f"**Source:** {company.get('source', 'Unknown')}\n\n")
            f.write("---\n\n")
    
    # Save investors
    investors_file = OUTPUT_DIR / f"daily-investors-{DATE_STR}.md"
    with open(investors_file, 'w') as f:
        f.write(f"# PE/VC Investors (Asia/India) - {DATE_STR}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Funds:** {len(results['investors'])}\n")
        f.write(f"**Defense-Focused:** {sum(1 for i in results['investors'] if i.get('score', 0) >= 50)}\n\n")
        
        for i, investor in enumerate(results["investors"][:10], 1):  # Top 10
            score = investor.get("score", 0)
            priority = "🟢 High" if score >= 60 else "🟡 Medium" if score >= 40 else "⚪ Low"
            
            f.write(f"## {i}. {investor.get('name', 'Unknown')}\n")
            f.write(f"**Score:** {score}/100 | **Priority:** {priority}\n\n")
            f.write(f"**URL:** {investor.get('url', 'N/A')}\n\n")
            f.write(f"**Description:**\n{investor.get('description', 'N/A')[:300]}...\n\n")
            f.write(f"**Source:** {investor.get('source', 'Unknown')}\n\n")
            f.write("---\n\n")
    
    print(f"\n✅ Results saved to:")
    print(f"   - {companies_file}")
    print(f"   - {investors_file}")

def generate_report():
    """Generate Discord report."""
    results["end_time"] = datetime.now().isoformat()
    
    start = datetime.fromisoformat(results["start_time"])
    end = datetime.fromisoformat(results["end_time"])
    processing_time = (end - start).total_seconds()
    
    high_priority = sum(1 for c in results["companies"] if c.get("score", 0) >= 70)
    defense_focused = sum(1 for i in results["investors"] if i.get("score", 0) >= 50)
    
    # Top 3 companies
    top_companies = results["companies"][:3]
    top_company_str = "\n".join([
        f"- {c.get('name', 'Unknown')[:40]} - Score: {c.get('score', 0)}"
        for c in top_companies
    ]) if top_companies else "- No companies found"
    
    # Top 3 investors
    top_investors = results["investors"][:3]
    top_investor_str = "\n".join([
        f"- {i.get('name', 'Unknown')[:40]} - Score: {i.get('score', 0)}"
        for i in top_investors
    ]) if top_investors else "- No investors found"
    
    report = f"""🛡️ **Defense Sector Report (Scrapling-Enhanced)**

## Companies (US/UK/EU)
- Identified: {len(results['companies'])}
- High priority (70+): {high_priority}
- Top 3:
{top_company_str}

## Investors (Asia/India)
- PE/VC funds: {len(results['investors'])}
- Defense-focused: {defense_focused}
- Top 3:
{top_investor_str}

🔍 **Data Source:**
- Scrapling Used: {'✅ Yes' if results['scrapling_used'] else '❌ No'}
- Scrapling Results: {results['scrapling_companies']} companies, {results['scrapling_investors']} investors
- Traditional API Results: {results['traditional_companies']} companies, {results['traditional_investors']} investors
- Processing Time: {processing_time:.1f} seconds"""
    
    return report

async def main():
    print("=" * 60)
    print("🛡️ Defense Sector Lead Generation - Scrapling-First")
    print("=" * 60)
    print(f"📅 Date: {DATE_STR}")
    print(f"⏰ Started: {results['start_time']}")
    print()
    
    # Step 1: Try Scrapling first
    scrapling_success = await try_scrapling()
    
    # Step 2: Fall back to Tavily if needed
    if not scrapling_success or len(results["companies"]) < 5:
        await fallback_to_tavily()
    
    # Step 3: Process and score results
    print("\n📊 Processing and scoring results...")
    deduplicate_and_score()
    
    # Step 4: Save to files
    save_results()
    
    # Step 5: Generate report
    print("\n" + "=" * 60)
    print("📋 DISCORD REPORT")
    print("=" * 60)
    report = generate_report()
    print(report)
    
    # Save report to file for delivery
    report_file = OUTPUT_DIR / f"report-{DATE_STR}.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"\n✅ Report saved to: {report_file}")

if __name__ == "__main__":
    asyncio.run(main())
