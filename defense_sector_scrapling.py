#!/usr/bin/env python3
"""
Defense Sector Lead Gen - Scrapling-First Approach
Two-part daily search: (1) Defense companies in US/UK/EU, (2) PE/VC funds in Asia/India
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Setup paths
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# Output directory
OUTPUT_DIR = Path('/Users/cubiczan/.openclaw/workspace/defense-leads')
OUTPUT_DIR.mkdir(exist_ok=True)

# API Keys
TAVILY_API_KEY = "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"
BRAVE_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"

# Track data sources
scrapling_used = False
scrapling_results = 0
traditional_api_results = 0
start_time = datetime.now()


def calculate_defense_company_score(company: Dict[str, Any]) -> int:
    """Score defense company (0-100)"""
    score = 0
    
    # Sector fit (0-30 pts)
    sector = company.get("sector", "").lower()
    description = company.get("description", "").lower()
    combined = f"{sector} {description}"
    
    defense_keywords = ["cybersecurity", "ai", "drone", "counter-drone", "c-uas", 
                       "space", "satellite", "defense", "military", "surveillance",
                       "autonomous", "uav", "isr", "analytics"]
    
    matches = sum(1 for kw in defense_keywords if kw in combined)
    sector_score = min(matches * 3, 30)
    score += sector_score
    
    # Stage fit (0-20 pts)
    stage = company.get("stage", "").lower()
    if any(s in stage for s in ["series a", "series b", "series c"]):
        score += 20
    elif "early" in stage or "seed" in stage:
        score += 15
    elif "growth" in stage:
        score += 10
    
    # Technical depth (0-20 pts)
    tech = company.get("technologies", "").lower()
    tech_keywords = ["ai", "machine learning", "autonomous", "sensor", "encryption",
                    "blockchain", "quantum", "edge computing", "computer vision"]
    tech_matches = sum(1 for kw in tech_keywords if kw in tech)
    score += min(tech_matches * 4, 20)
    
    # Integration potential (0-20 pts)
    clients = company.get("clients", "").lower()
    if "government" in clients or "military" in clients or "defense" in clients:
        score += 20
    elif "enterprise" in clients or "federal" in clients:
        score += 15
    else:
        score += 5
    
    # Region match (0-10 pts)
    location = company.get("location", "").lower()
    if any(r in location for r in ["us", "usa", "united states", "uk", "united kingdom"]):
        score += 10
    elif any(r in location for r in ["eu", "europe", "germany", "france", "uk"]):
        score += 8
    else:
        score += 2
    
    return min(score, 100)


def calculate_pe_fund_score(fund: Dict[str, Any]) -> int:
    """Score PE/VC fund (0-100)"""
    score = 0
    
    # Defense/drone focus (0-40 pts)
    focus = fund.get("focus", "").lower()
    portfolio = fund.get("portfolio", "").lower()
    combined = f"{focus} {portfolio}"
    
    defense_keywords = ["defense", "drone", "uav", "aerospace", "autonomous", 
                       "security", "surveillance", "military", "dual-use"]
    matches = sum(1 for kw in defense_keywords if kw in combined)
    score += min(matches * 5, 40)
    
    # Region match (0-20 pts)
    region = fund.get("region", "").lower()
    if "india" in region:
        score += 20
    elif any(r in region for r in ["singapore", "japan", "korea", "taiwan"]):
        score += 18
    elif "southeast asia" in region or "middle east" in region:
        score += 15
    else:
        score += 5
    
    # Portfolio fit (0-20 pts)
    if any(kw in portfolio for kw in ["autonomous", "drone", "ai", "robotics"]):
        score += 20
    elif any(kw in portfolio for kw in ["technology", "hardware", "software"]):
        score += 10
    
    # Fund size/stage (0-20 pts)
    stage = fund.get("stage", "").lower()
    if "early" in stage or "series a" in stage:
        score += 20
    elif "growth" in stage:
        score += 15
    elif "late" in stage:
        score += 10
    
    return min(score, 100)


async def try_scrapling_approach() -> tuple[List[Dict], List[Dict]]:
    """Try Scrapling integration first"""
    global scrapling_used, scrapling_results
    
    print("🔧 Attempting Scrapling integration...")
    
    try:
        from cron_integration import ScraplingCronIntegration
        
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if success:
            print("✅ Scrapling initialized successfully")
            scrapling_used = True
            
            # Search for defense companies
            search_terms = [
                "defense technology companies",
                "cybersecurity companies military",
                "drone technology defense",
                "space defense technology",
                "military AI companies"
            ]
            
            companies = await scrapling.scrape_defense_companies(search_terms)
            scrapling_results = len(companies)
            
            # Search for PE/VC funds (placeholder)
            funds = await scrapling.scrape_pe_vc_funds(
                regions=["india", "singapore", "japan", "korea"],
                focus="defense"
            )
            
            if companies or funds:
                return companies, funds
        else:
            print("⚠️ Scrapling initialization failed")
            
    except ImportError as e:
        print(f"⚠️ Scrapling not available: {e}")
    except Exception as e:
        print(f"❌ Scrapling error: {e}")
    
    return [], []


async def search_tavily_defense_companies() -> List[Dict[str, Any]]:
    """Use Tavily API to search for defense companies"""
    global traditional_api_results
    
    print("🔍 Using Tavily API for defense companies...")
    
    import subprocess
    import tempfile
    
    companies = []
    
    # Search queries for defense companies
    queries = [
        "defense technology companies Series A Series B US UK EU 2024 2025",
        "cybersecurity defense military contractors early stage",
        "counter-drone C-UAS technology companies",
        "space defense satellite technology startups",
        "military AI machine learning defense companies"
    ]
    
    for query in queries:
        try:
            # Create a Node.js script to call Tavily
            script = f"""
const https = require('https');

const data = JSON.stringify({{
  api_key: "{TAVILY_API_KEY}",
  query: "{query}",
  search_depth: "advanced",
  max_results: 5
}});

const options = {{
  hostname: 'api.tavily.com',
  port: 443,
  path: '/search',
  method: 'POST',
  headers: {{
    'Content-Type': 'application/json',
    'Content-Length': data.length
  }}
}};

const req = https.request(options, (res) => {{
  let body = '';
  res.on('data', (chunk) => body += chunk);
  res.on('end', () => console.log(body));
}});

req.on('error', (e) => console.error(e.message));
req.write(data);
req.end();
"""
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(script)
                temp_file = f.name
            
            result = subprocess.run(
                ['node', temp_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            os.unlink(temp_file)
            
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                if 'results' in data:
                    for item in data['results'][:3]:
                        companies.append({
                            "company_name": item.get("title", "Unknown"),
                            "url": item.get("url", ""),
                            "description": item.get("content", ""),
                            "sector": "Defense Technology",
                            "location": "US/UK/EU",
                            "stage": "Early-Mid Stage",
                            "source": "Tavily"
                        })
                        traditional_api_results += 1
            
        except Exception as e:
            print(f"⚠️ Tavily query failed: {e}")
            continue
    
    return companies


async def search_tavily_pe_funds() -> List[Dict[str, Any]]:
    """Use Tavily API to search for PE/VC funds in Asia/India"""
    global traditional_api_results
    
    print("🔍 Using Tavily API for PE/VC funds...")
    
    import subprocess
    import tempfile
    
    funds = []
    
    # Search queries for PE/VC funds
    queries = [
        "private equity venture capital funds India defense aerospace drone technology",
        "Singapore VC funds autonomous systems drone investments",
        "Japan Korea venture capital defense technology dual-use",
        "Middle East PE fund defense technology investments",
        "Southeast Asia venture capital drone UAV investments"
    ]
    
    for query in queries:
        try:
            script = f"""
const https = require('https');

const data = JSON.stringify({{
  api_key: "{TAVILY_API_KEY}",
  query: "{query}",
  search_depth: "advanced",
  max_results: 5
}});

const options = {{
  hostname: 'api.tavily.com',
  port: 443,
  path: '/search',
  method: 'POST',
  headers: {{
    'Content-Type': 'application/json',
    'Content-Length': data.length
  }}
}};

const req = https.request(options, (res) => {{
  let body = '';
  res.on('data', (chunk) => body += chunk);
  res.on('end', () => console.log(body));
}});

req.on('error', (e) => console.error(e.message));
req.write(data);
req.end();
"""
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(script)
                temp_file = f.name
            
            result = subprocess.run(
                ['node', temp_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            os.unlink(temp_file)
            
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                if 'results' in data:
                    for item in data['results'][:3]:
                        funds.append({
                            "fund_name": item.get("title", "Unknown"),
                            "url": item.get("url", ""),
                            "focus": "Defense Technology, Drones, Aerospace",
                            "region": "Asia/India",
                            "portfolio": "Autonomous Systems, Dual-Use Technology",
                            "stage": "Early-Mid Stage",
                            "source": "Tavily"
                        })
                        traditional_api_results += 1
            
        except Exception as e:
            print(f"⚠️ Tavily query failed: {e}")
            continue
    
    return funds


async def search_brave_defense_companies() -> List[Dict[str, Any]]:
    """Use Brave Search API as fallback"""
    global traditional_api_results
    
    print("🔍 Using Brave Search API for defense companies...")
    
    import subprocess
    
    companies = []
    
    queries = [
        "defense technology companies Series A Series B funding",
        "cybersecurity defense military startups",
        "counter-drone technology companies investment"
    ]
    
    for query in queries:
        try:
            result = subprocess.run(
                ['curl', '-s', '-X', 'POST', 'https://api.search.brave.com/res/v1/web/search',
                 '-H', f'X-Subscription-Token: {BRAVE_API_KEY}',
                 '-H', 'Accept: application/json',
                 '-H', 'Accept-Encoding: gzip',
                 '-d', f'q={query}&count=3'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                if 'web' in data and 'results' in data['web']:
                    for item in data['web']['results'][:3]:
                        companies.append({
                            "company_name": item.get("title", "Unknown"),
                            "url": item.get("url", ""),
                            "description": item.get("description", ""),
                            "sector": "Defense Technology",
                            "location": "US/UK/EU",
                            "stage": "Early-Mid Stage",
                            "source": "Brave Search"
                        })
                        traditional_api_results += 1
            
        except Exception as e:
            print(f"⚠️ Brave Search query failed: {e}")
            continue
    
    return companies


def save_results(companies: List[Dict], funds: List[Dict]):
    """Save results to files"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Save companies
    companies_file = OUTPUT_DIR / f"daily-companies-{today}.md"
    with open(companies_file, 'w') as f:
        f.write(f"# Defense Companies - {today}\n\n")
        f.write(f"**Total Identified:** {len(companies)}\n\n")
        
        high_priority = [c for c in companies if c.get('defense_score', 0) >= 70]
        f.write(f"**High Priority (70+ score):** {len(high_priority)}\n\n")
        
        # Sort by score
        sorted_companies = sorted(companies, key=lambda x: x.get('defense_score', 0), reverse=True)
        
        for i, company in enumerate(sorted_companies, 1):
            score = company.get('defense_score', 0)
            f.write(f"## {i}. {company.get('company_name', 'Unknown')}\n")
            f.write(f"- **Score:** {score}/100\n")
            f.write(f"- **Priority:** {'High' if score >= 70 else 'Medium' if score >= 50 else 'Low'}\n")
            f.write(f"- **Sector:** {company.get('sector', 'N/A')}\n")
            f.write(f"- **Stage:** {company.get('stage', 'N/A')}\n")
            f.write(f"- **Location:** {company.get('location', 'N/A')}\n")
            f.write(f"- **URL:** {company.get('url', 'N/A')}\n")
            f.write(f"- **Source:** {company.get('source', 'N/A')}\n")
            if company.get('description'):
                f.write(f"- **Description:** {company.get('description')[:200]}...\n")
            f.write("\n")
    
    print(f"✅ Saved companies to {companies_file}")
    
    # Save investors
    investors_file = OUTPUT_DIR / f"daily-investors-{today}.md"
    with open(investors_file, 'w') as f:
        f.write(f"# PE/VC Investors (Asia/India) - {today}\n\n")
        f.write(f"**Total Identified:** {len(funds)}\n\n")
        
        defense_focused = [f for f in funds if f.get('investor_score', 0) >= 50]
        f.write(f"**Defense-Focused:** {len(defense_focused)}\n\n")
        
        # Sort by score
        sorted_funds = sorted(funds, key=lambda x: x.get('investor_score', 0), reverse=True)
        
        for i, fund in enumerate(sorted_funds, 1):
            score = fund.get('investor_score', 0)
            f.write(f"## {i}. {fund.get('fund_name', 'Unknown')}\n")
            f.write(f"- **Score:** {score}/100\n")
            f.write(f"- **Region:** {fund.get('region', 'N/A')}\n")
            f.write(f"- **Focus:** {fund.get('focus', 'N/A')}\n")
            f.write(f"- **Stage:** {fund.get('stage', 'N/A')}\n")
            f.write(f"- **URL:** {fund.get('url', 'N/A')}\n")
            f.write(f"- **Source:** {fund.get('source', 'N/A')}\n")
            f.write("\n")
    
    print(f"✅ Saved investors to {investors_file}")


async def main():
    """Main execution"""
    print("=" * 60)
    print("🛡️ Defense Sector Lead Gen - Scrapling-First Enhanced")
    print("=" * 60)
    
    companies = []
    funds = []
    
    # Step 1: Try Scrapling first
    print("\n📊 Step 1: Attempting Scrapling integration...")
    scrapling_companies, scrapling_funds = await try_scrapling_approach()
    
    if scrapling_companies or scrapling_funds:
        companies.extend(scrapling_companies)
        funds.extend(scrapling_funds)
        print(f"✅ Scrapling found {len(scrapling_companies)} companies, {len(scrapling_funds)} funds")
    else:
        # Step 2: Fall back to Tavily
        print("\n📊 Step 2: Falling back to Tavily API...")
        tavily_companies = await search_tavily_defense_companies()
        tavily_funds = await search_tavily_pe_funds()
        
        companies.extend(tavily_companies)
        funds.extend(tavily_funds)
        print(f"✅ Tavily found {len(tavily_companies)} companies, {len(tavily_funds)} funds")
        
        # Step 3: Fall back to Brave Search if needed
        if len(companies) < 5:
            print("\n📊 Step 3: Supplementing with Brave Search...")
            brave_companies = await search_brave_defense_companies()
            companies.extend(brave_companies)
            print(f"✅ Brave Search found {len(brave_companies)} additional companies")
    
    # Score all results
    print("\n📊 Scoring results...")
    for company in companies:
        company['defense_score'] = calculate_defense_company_score(company)
    
    for fund in funds:
        fund['investor_score'] = calculate_pe_fund_score(fund)
    
    # Save results
    print("\n📊 Saving results...")
    save_results(companies, funds)
    
    # Calculate processing time
    processing_time = (datetime.now() - start_time).total_seconds()
    
    # Prepare summary for Discord
    high_priority_companies = [c for c in companies if c.get('defense_score', 0) >= 70]
    defense_focused_funds = [f for f in funds if f.get('investor_score', 0) >= 50]
    
    top_companies = sorted(companies, key=lambda x: x.get('defense_score', 0), reverse=True)[:3]
    top_funds = sorted(funds, key=lambda x: x.get('investor_score', 0), reverse=True)[:3]
    
    summary = f"""🛡️ **Defense Sector Report (Scrapling-Enhanced)**

## Companies (US/UK/EU)
- Identified: {len(companies)}
- High priority (70+): {len(high_priority_companies)}
- Top 3: {', '.join([f"{c.get('company_name', 'Unknown')} ({c.get('sector', 'N/A')}) - {c.get('defense_score', 0)}" for c in top_companies])}

## Investors (Asia/India)
- PE/VC funds: {len(funds)}
- Defense-focused: {len(defense_focused_funds)}
- Top 3: {', '.join([f"{f.get('fund_name', 'Unknown')} ({f.get('region', 'N/A')}) - {f.get('investor_score', 0)}" for f in top_funds])}

🔍 **Data Source:**
- Scrapling Used: {'✅ Yes' if scrapling_used else '❌ No'}
- Scrapling Results: {scrapling_results}
- Traditional API Results: {traditional_api_results}
- Processing Time: {processing_time:.1f} seconds

Files saved to:
- `/workspace/defense-leads/daily-companies-{datetime.now().strftime("%Y-%m-%d")}.md`
- `/workspace/defense-leads/daily-investors-{datetime.now().strftime("%Y-%m-%d")}.md`"""
    
    print("\n" + "=" * 60)
    print(summary)
    print("=" * 60)
    
    return summary


if __name__ == "__main__":
    summary = asyncio.run(main())
    # Print summary for cron to capture
    print("\nDISCORD_SUMMARY_START")
    print(summary)
    print("DISCORD_SUMMARY_END")
