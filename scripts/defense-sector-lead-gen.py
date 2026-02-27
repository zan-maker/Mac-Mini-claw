#!/usr/bin/env python3
"""
Defense Sector Lead Gen - Scrapling-First Enhanced
Two-part daily search: (1) Defense companies in US/UK/EU, (2) PE/VC funds in Asia/India
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Add scrapling integration to path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# Track data sources
data_sources = {
    "scrapling_used": False,
    "scrapling_results": 0,
    "tavily_results": 0,
    "brave_results": 0,
    "start_time": datetime.now()
}

async def try_scrapling_defense():
    """Try Scrapling for defense company discovery."""
    global data_sources
    
    try:
        from cron_integration import ScraplingCronIntegration
        
        print("🔍 Attempting Scrapling integration...")
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if success:
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
                data_sources["scrapling_used"] = True
                data_sources["scrapling_results"] = len(companies)
                print(f"✅ Scrapling found {len(companies)} companies")
                return companies
        else:
            print("⚠️ Scrapling initialization failed")
            return []
    except ImportError as e:
        print(f"⚠️ Scrapling not available: {e}")
        return []
    except Exception as e:
        print(f"⚠️ Scrapling error: {e}")
        return []
    
    return []

async def try_scrapling_investors():
    """Try Scrapling for PE/VC fund discovery."""
    global data_sources
    
    try:
        from cron_integration import ScraplingCronIntegration
        
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if success:
            regions = ["India", "Singapore", "Japan", "South Korea", "Taiwan", "Southeast Asia", "Middle East"]
            funds = await scrapling.scrape_pe_vc_funds(regions, focus="defense")
            
            if funds:
                data_sources["scrapling_results"] += len(funds)
                print(f"✅ Scrapling found {len(funds)} PE/VC funds")
                return funds
        return []
    except:
        return []

async def search_tavily(query: str, api_key: str):
    """Search using Tavily API."""
    import aiohttp
    
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "advanced",
        "max_results": 10
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("results", [])
    except Exception as e:
        print(f"⚠️ Tavily API error: {e}")
    
    return []

async def search_brave(query: str, api_key: str):
    """Search using Brave Search API."""
    import aiohttp
    
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {"X-Subscription-Token": api_key}
    params = {"q": query, "count": 10}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("web", {}).get("results", [])
    except Exception as e:
        print(f"⚠️ Brave Search API error: {e}")
    
    return []

async def fallback_defense_search():
    """Fall back to Tavily/Brave for defense companies."""
    global data_sources
    
    tavily_key = "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"
    brave_key = "BSA4VYA3FjSPQmTjZeKjsq5CqWvFy2u"
    
    companies = []
    
    # Defense company searches
    queries = [
        "defense technology companies Series A B C funding US UK EU",
        "cybersecurity military defense companies early stage",
        "counter-drone C-UAS anti-drone systems companies",
        "space defense satellite technology startups",
        "military AI machine learning defense companies"
    ]
    
    print("🔍 Using Tavily API for defense company search...")
    
    for query in queries:
        results = await search_tavily(query, tavily_key)
        
        if results:
            data_sources["tavily_results"] += len(results)
            for result in results:
                company = {
                    "company_name": result.get("title", "").split(" - ")[0].split(" | ")[0],
                    "url": result.get("url", ""),
                    "description": result.get("content", ""),
                    "source": "Tavily"
                }
                companies.append(company)
        else:
            # Fall back to Brave if Tavily fails
            print(f"⚠️ Tavily failed for query, trying Brave...")
            results = await search_brave(query, brave_key)
            if results:
                data_sources["brave_results"] += len(results)
                for result in results:
                    company = {
                        "company_name": result.get("title", "").split(" - ")[0].split(" | ")[0],
                        "url": result.get("url", ""),
                        "description": result.get("description", ""),
                        "source": "Brave"
                    }
                    companies.append(company)
    
    return companies

async def fallback_investor_search():
    """Fall back to Tavily/Brave for PE/VC funds."""
    global data_sources
    
    tavily_key = "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"
    brave_key = "BSA4VYA3FjSPQmTjZeKjsq5CqWvFy2u"
    
    funds = []
    
    # PE/VC searches (EXCLUDING CHINA)
    queries = [
        "private equity defense drone aerospace investment Asia India Singapore",
        "venture capital military technology autonomous systems Japan Korea",
        "PE fund dual-use technology surveillance India Middle East",
        "defense tech investor UAV drone funding Taiwan Southeast Asia"
    ]
    
    print("🔍 Using Tavily API for PE/VC fund search...")
    
    for query in queries:
        results = await search_tavily(query, tavily_key)
        
        if results:
            data_sources["tavily_results"] += len(results)
            for result in results:
                # Exclude China
                url = result.get("url", "")
                description = result.get("content", "").lower()
                if "china" not in url.lower() and "china" not in description:
                    fund = {
                        "fund_name": result.get("title", "").split(" - ")[0].split(" | ")[0],
                        "url": url,
                        "description": result.get("content", ""),
                        "source": "Tavily"
                    }
                    funds.append(fund)
        else:
            # Fall back to Brave
            print(f"⚠️ Tavily failed for query, trying Brave...")
            results = await search_brave(query, brave_key)
            if results:
                data_sources["brave_results"] += len(results)
                for result in results:
                    url = result.get("url", "")
                    description = result.get("description", "").lower()
                    if "china" not in url.lower() and "china" not in description:
                        fund = {
                            "fund_name": result.get("title", "").split(" - ")[0].split(" | ")[0],
                            "url": url,
                            "description": result.get("description", ""),
                            "source": "Brave"
                        }
                        funds.append(fund)
    
    return funds

def score_defense_company(company: dict) -> int:
    """Score defense company (0-100)."""
    score = 0
    
    # Sector fit (30 points)
    desc = company.get("description", "").lower()
    sector_keywords = {
        "cybersecurity": 30,
        "drone": 30,
        "counter-drone": 30,
        "c-uas": 30,
        "defense": 25,
        "military": 25,
        "space": 20,
        "satellite": 20,
        "ai": 15,
        "machine learning": 15,
        "autonomous": 15,
        "surveillance": 20,
        "security": 15,
        "technology": 10
    }
    
    for keyword, points in sector_keywords.items():
        if keyword in desc:
            score = max(score, min(score + points, 30))
            break
    
    # Stage fit (20 points)
    stage_keywords = ["series a", "series b", "series c", "early stage", "growth stage", "funding", "raised"]
    if any(kw in desc for kw in stage_keywords):
        score += 20
    
    # Technical depth (20 points)
    tech_keywords = ["ai", "ml", "autonomous", "sensor", "satellite", "encryption", "quantum", "edge computing"]
    tech_count = sum(1 for kw in tech_keywords if kw in desc)
    score += min(tech_count * 5, 20)
    
    # Integration potential (20 points)
    integration_keywords = ["platform", "api", "integration", "modular", "interoperable"]
    if any(kw in desc for kw in integration_keywords):
        score += 20
    
    # Region match (10 points)
    region_keywords = ["us", "united states", "uk", "united kingdom", "europe", "eu", "germany", "france", "uk"]
    if any(kw in desc for kw in region_keywords):
        score += 10
    
    return min(score, 100)

def score_pe_fund(fund: dict) -> int:
    """Score PE/VC fund (0-100)."""
    score = 0
    
    desc = fund.get("description", "").lower()
    
    # Defense/drone focus (40 points)
    defense_keywords = ["defense", "military", "drone", "uav", "aerospace", "autonomous", "surveillance", "security"]
    defense_count = sum(1 for kw in defense_keywords if kw in desc)
    score += min(defense_count * 8, 40)
    
    # Region match (20 points)
    region_keywords = ["india", "singapore", "japan", "korea", "taiwan", "southeast asia", "middle east", "dubai", "abu dhabi"]
    if any(kw in desc for kw in region_keywords):
        score += 20
    
    # Portfolio fit (20 points)
    portfolio_keywords = ["portfolio", "investment", "backed", "funded", "capital"]
    if any(kw in desc for kw in portfolio_keywords):
        score += 20
    
    # Fund size/stage (20 points)
    stage_keywords = ["early stage", "growth", "venture", "series", "seed"]
    if any(kw in desc for kw in stage_keywords):
        score += 20
    
    return min(score, 100)

def deduplicate(items: list, key: str) -> list:
    """Remove duplicates based on key."""
    seen = set()
    unique = []
    for item in items:
        identifier = item.get(key, "").lower()
        if identifier and identifier not in seen:
            seen.add(identifier)
            unique.append(item)
    return unique

async def main():
    """Main execution."""
    print("=" * 60)
    print("🛡️  Defense Sector Lead Gen - Scrapling-First Enhanced")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Part 1: Defense Companies
    print("📍 Part 1: Defense Companies (US/UK/EU)")
    print("-" * 60)
    
    # Try Scrapling first
    defense_companies = await try_scrapling_defense()
    
    # Fall back to traditional APIs if Scrapling fails
    if not defense_companies:
        print("⚠️ Scrapling returned no results, using traditional APIs...")
        defense_companies = await fallback_defense_search()
    
    # Process and score
    if defense_companies:
        for company in defense_companies:
            company["defense_score"] = score_defense_company(company)
        
        # Deduplicate
        defense_companies = deduplicate(defense_companies, "company_name")
        
        # Sort by score
        defense_companies.sort(key=lambda x: x.get("defense_score", 0), reverse=True)
        
        # Take top 10
        defense_companies = defense_companies[:10]
    
    print(f"✅ Found {len(defense_companies)} defense companies")
    
    # Part 2: PE/VC Funds
    print()
    print("📍 Part 2: PE/VC Funds (Asia/India)")
    print("-" * 60)
    
    # Try Scrapling first
    pe_vc_funds = await try_scrapling_investors()
    
    # Fall back to traditional APIs
    if not pe_vc_funds:
        print("⚠️ Scrapling returned no results, using traditional APIs...")
        pe_vc_funds = await fallback_investor_search()
    
    # Process and score
    if pe_vc_funds:
        for fund in pe_vc_funds:
            fund["fund_score"] = score_pe_fund(fund)
        
        # Deduplicate
        pe_vc_funds = deduplicate(pe_vc_funds, "fund_name")
        
        # Sort by score
        pe_vc_funds.sort(key=lambda x: x.get("fund_score", 0), reverse=True)
        
        # Take top 5
        pe_vc_funds = pe_vc_funds[:5]
    
    print(f"✅ Found {len(pe_vc_funds)} PE/VC funds")
    
    # Save results
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = Path("/Users/cubiczan/.openclaw/workspace/defense-leads")
    output_dir.mkdir(exist_ok=True)
    
    # Save companies
    companies_file = output_dir / f"daily-companies-{today}.md"
    with open(companies_file, "w") as f:
        f.write(f"# Defense Companies - {today}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Leads:** {len(defense_companies)}\n\n")
        
        for i, company in enumerate(defense_companies, 1):
            score = company.get("defense_score", 0)
            priority = "🟢 HIGH" if score >= 70 else "🟡 MEDIUM" if score >= 50 else "🔴 LOW"
            
            f.write(f"## {i}. {company.get('company_name', 'Unknown')}\n")
            f.write(f"**Score:** {score}/100 {priority}\n")
            f.write(f"**URL:** {company.get('url', 'N/A')}\n")
            f.write(f"**Description:** {company.get('description', 'N/A')[:200]}...\n")
            f.write(f"**Source:** {company.get('source', 'Unknown')}\n\n")
    
    # Save investors
    investors_file = output_dir / f"daily-investors-{today}.md"
    with open(investors_file, "w") as f:
        f.write(f"# PE/VC Investors (Asia/India) - {today}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Funds:** {len(pe_vc_funds)}\n\n")
        
        for i, fund in enumerate(pe_vc_funds, 1):
            score = fund.get("fund_score", 0)
            priority = "🟢 HIGH" if score >= 70 else "🟡 MEDIUM" if score >= 50 else "🔴 LOW"
            
            f.write(f"## {i}. {fund.get('fund_name', 'Unknown')}\n")
            f.write(f"**Score:** {score}/100 {priority}\n")
            f.write(f"**URL:** {fund.get('url', 'N/A')}\n")
            f.write(f"**Description:** {fund.get('description', 'N/A')[:200]}...\n")
            f.write(f"**Source:** {fund.get('source', 'Unknown')}\n\n")
    
    print()
    print("=" * 60)
    print("✅ Results saved to:")
    print(f"   - {companies_file}")
    print(f"   - {investors_file}")
    
    # Calculate processing time
    processing_time = (datetime.now() - data_sources["start_time"]).total_seconds()
    
    # Print summary
    print()
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Defense Companies: {len(defense_companies)}")
    print(f"  - High Priority (70+): {sum(1 for c in defense_companies if c.get('defense_score', 0) >= 70)}")
    print(f"  - Medium Priority (50-69): {sum(1 for c in defense_companies if 50 <= c.get('defense_score', 0) < 70)}")
    print()
    print(f"PE/VC Funds: {len(pe_vc_funds)}")
    print(f"  - High Priority (70+): {sum(1 for f in pe_vc_funds if f.get('fund_score', 0) >= 70)}")
    print()
    print("🔍 Data Sources:")
    print(f"  - Scrapling Used: {'✅ Yes' if data_sources['scrapling_used'] else '❌ No'}")
    print(f"  - Scrapling Results: {data_sources['scrapling_results']}")
    print(f"  - Tavily Results: {data_sources['tavily_results']}")
    print(f"  - Brave Results: {data_sources['brave_results']}")
    print(f"  - Processing Time: {processing_time:.1f} seconds")
    
    # Generate Discord report
    discord_report = f"""🛡️ **Defense Sector Report (Scrapling-Enhanced)**

## Companies (US/UK/EU)
- Identified: {len(defense_companies)}
- High priority (70+): {sum(1 for c in defense_companies if c.get('defense_score', 0) >= 70)}
- Top 3: """

    top_3_companies = defense_companies[:3]
    if top_3_companies:
        discord_report += ", ".join([f"{c.get('company_name', 'Unknown')} ({c.get('defense_score', 0)})" for c in top_3_companies])
    else:
        discord_report += "None found"
    
    discord_report += f"""

## Investors (Asia/India)
- PE/VC funds: {len(pe_vc_funds)}
- Defense-focused: {sum(1 for f in pe_vc_funds if f.get('fund_score', 0) >= 60)}
- Top 3: """
    
    top_3_funds = pe_vc_funds[:3]
    if top_3_funds:
        discord_report += ", ".join([f"{f.get('fund_name', 'Unknown')} ({f.get('fund_score', 0)})" for f in top_3_funds])
    else:
        discord_report += "None found"
    
    discord_report += f"""

🔍 **Data Source:**
- Scrapling Used: {'✅ Yes' if data_sources['scrapling_used'] else '❌ No'}
- Scrapling Results: {data_sources['scrapling_results']}
- Traditional API Results: {data_sources['tavily_results'] + data_sources['brave_results']}
- Processing Time: {processing_time:.1f} seconds"""
    
    # Save Discord report
    report_file = output_dir / f"discord-report-{today}.txt"
    with open(report_file, "w") as f:
        f.write(discord_report)
    
    print()
    print("=" * 60)
    print("💬 Discord Report:")
    print("=" * 60)
    print(discord_report)
    print()
    print(f"Discord report saved to: {report_file}")

if __name__ == "__main__":
    asyncio.run(main())
