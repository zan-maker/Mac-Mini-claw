#!/usr/bin/env python3
"""
Defense Sector Lead Generation - Scrapling-First Approach
"""
import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add scrapling integration
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# API Keys
TAVILY_API_KEY = "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"
BRAVE_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"

# Results tracking
results = {
    "scrapling_used": False,
    "scrapling_results": 0,
    "tavily_results": 0,
    "brave_results": 0,
    "companies": [],
    "investors": [],
    "start_time": datetime.now(),
    "errors": []
}

async def try_scrapling():
    """Try Scrapling integration first."""
    try:
        from cron_integration import ScraplingCronIntegration, SCRAPLING_AVAILABLE
        
        if not SCRAPLING_AVAILABLE:
            print("⚠️ Scrapling not available")
            return False
        
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if not success:
            print("⚠️ Scrapling initialization failed")
            return False
        
        print("✅ Scrapling initialized successfully")
        results["scrapling_used"] = True
        
        # Search for defense companies
        search_terms = [
            "defense technology companies Series A B C funding",
            "cybersecurity military dual-use technology",
            "counter-drone C-UAS anti-drone systems startup",
            "space defense satellite technology companies",
            "military AI autonomous systems defense"
        ]
        
        companies = await scrapling.scrape_defense_companies(search_terms)
        results["scrapling_results"] = len(companies)
        results["companies"].extend(companies)
        
        return len(companies) > 0
        
    except Exception as e:
        print(f"❌ Scrapling error: {e}")
        results["errors"].append(f"Scrapling: {str(e)}")
        return False

async def try_tavily():
    """Fallback to Tavily API."""
    import urllib.request
    import urllib.error
    
    print("🔄 Trying Tavily API...")
    
    try:
        queries = [
            "defense technology companies US UK EU Series A B C funding 2024 2025",
            "cybersecurity defense military startups funding",
            "counter-drone C-UAS anti-drone technology companies",
            "space defense satellite startups venture capital",
            "military AI autonomous defense systems companies"
        ]
        
        companies = []
        
        for query in queries:
            try:
                url = "https://api.tavily.com/search"
                data = json.dumps({
                    "api_key": TAVILY_API_KEY,
                    "query": query,
                    "search_depth": "advanced",
                    "max_results": 10,
                    "include_raw_content": False
                }).encode('utf-8')
                
                req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    
                    for item in result.get('results', []):
                        company = {
                            "name": item.get('title', 'Unknown'),
                            "url": item.get('url', ''),
                            "description": item.get('content', ''),
                            "source": "Tavily",
                            "query": query,
                            "defense_score": score_defense_company(item.get('content', '') + " " + item.get('title', ''))
                        }
                        if company["defense_score"] >= 30:
                            companies.append(company)
                            
            except Exception as e:
                print(f"Tavily query error: {e}")
                continue
        
        results["tavily_results"] = len(companies)
        results["companies"].extend(companies)
        print(f"✅ Tavily found {len(companies)} companies")
        return len(companies) > 0
        
    except Exception as e:
        print(f"❌ Tavily error: {e}")
        results["errors"].append(f"Tavily: {str(e)}")
        return False

async def try_brave():
    """Fallback to Brave Search API."""
    import urllib.request
    import urllib.error
    
    print("🔄 Trying Brave Search API...")
    
    try:
        queries = [
            "defense technology startup funding Series A B C",
            "cybersecurity military companies US UK EU",
            "anti-drone counter-UAS technology companies",
            "space defense satellite startups",
            "AI military autonomous defense systems"
        ]
        
        companies = []
        
        for query in queries:
            try:
                url = f"https://api.search.brave.com/res/v1/web/search?q={query}&count=10"
                req = urllib.request.Request(url, headers={
                    'Accept': 'application/json',
                    'X-Subscription-Token': BRAVE_API_KEY
                })
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    
                    for item in result.get('web', {}).get('results', []):
                        company = {
                            "name": item.get('title', 'Unknown').replace(' - ', ' | ').split('|')[0].strip(),
                            "url": item.get('url', ''),
                            "description": item.get('description', ''),
                            "source": "Brave",
                            "query": query,
                            "defense_score": score_defense_company(item.get('description', '') + " " + item.get('title', ''))
                        }
                        if company["defense_score"] >= 30:
                            companies.append(company)
                            
            except Exception as e:
                print(f"Brave query error: {e}")
                continue
        
        results["brave_results"] = len(companies)
        results["companies"].extend(companies)
        print(f"✅ Brave found {len(companies)} companies")
        return len(companies) > 0
        
    except Exception as e:
        print(f"❌ Brave error: {e}")
        results["errors"].append(f"Brave: {str(e)}")
        return False

def score_defense_company(text):
    """Score a defense company based on text content (0-100)."""
    score = 0
    text_lower = text.lower()
    
    # Sector fit (0-30)
    sector_keywords = {
        "defense": 10, "military": 10, "cybersecurity": 8, "cyber": 6,
        "drone": 8, "uav": 6, "space": 6, "satellite": 6,
        "autonomous": 5, "ai": 5, "security": 4, "surveillance": 5,
        "isr": 6, "radar": 5, "sensor": 4, "encryption": 4
    }
    for keyword, points in sector_keywords.items():
        if keyword in text_lower:
            score += points
    score = min(score, 30)
    
    # Stage fit (0-20)
    if "series a" in text_lower or "series b" in text_lower or "series c" in text_lower:
        score += 15
    elif "seed" in text_lower or "funding" in text_lower or "raised" in text_lower:
        score += 10
    elif "startup" in text_lower:
        score += 8
    
    # Region (0-10)
    if "united states" in text_lower or "us" in text_lower or "usa" in text_lower:
        score += 4
    if "uk" in text_lower or "united kingdom" in text_lower or "britain" in text_lower:
        score += 3
    if "eu" in text_lower or "europe" in text_lower or "germany" in text_lower or "france" in text_lower:
        score += 3
    
    # Technical depth (0-20)
    tech_keywords = ["machine learning", "deep learning", "autonomous", "edge computing",
                     "computer vision", "signal processing", "quantum", "hypersonic"]
    for keyword in tech_keywords:
        if keyword in text_lower:
            score += 5
    score = min(score + 20, 40)
    
    return min(score, 100)

async def search_investors():
    """Search for PE/VC funds in Asia/India."""
    import urllib.request
    import urllib.error
    
    print("🔍 Searching for investors...")
    
    investors = []
    
    # Try Tavily first for investors
    queries = [
        "private equity venture capital defense technology India Singapore",
        "VC fund drone aerospace investment Asia Japan Korea",
        "defense tech investor Southeast Asia Middle East",
        "aerospace drone fund Taiwan Singapore venture capital",
        "dual-use technology investor India Japan funding"
    ]
    
    for query in queries:
        try:
            url = "https://api.tavily.com/search"
            data = json.dumps({
                "api_key": TAVILY_API_KEY,
                "query": query,
                "search_depth": "advanced",
                "max_results": 8
            }).encode('utf-8')
            
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                for item in result.get('results', []):
                    investor = {
                        "name": item.get('title', 'Unknown').replace(' - ', ' | ').split('|')[0].strip(),
                        "url": item.get('url', ''),
                        "description": item.get('content', ''),
                        "source": "Tavily",
                        "score": score_investor(item.get('content', '') + " " + item.get('title', ''))
                    }
                    if investor["score"] >= 30 and "china" not in investor["name"].lower():
                        investors.append(investor)
                        
        except Exception as e:
            print(f"Investor search error: {e}")
            continue
    
    # Remove duplicates by name
    seen = set()
    unique_investors = []
    for inv in investors:
        name_lower = inv["name"].lower()
        if name_lower not in seen:
            seen.add(name_lower)
            unique_investors.append(inv)
    
    results["investors"] = unique_investors[:10]  # Limit to 10
    print(f"✅ Found {len(unique_investors)} investors")
    return len(unique_investors) > 0

def score_investor(text):
    """Score investor based on defense/region focus (0-100)."""
    score = 0
    text_lower = text.lower()
    
    # Defense/drone focus (0-40)
    if "defense" in text_lower:
        score += 15
    if "drone" in text_lower or "uav" in text_lower:
        score += 10
    if "aerospace" in text_lower:
        score += 10
    if "security" in text_lower or "surveillance" in text_lower:
        score += 5
    
    # Region (0-20) - EXCLUDE CHINA
    regions = ["india", "singapore", "japan", "korea", "taiwan", "southeast asia", "middle east", "dubai", "abu dhabi"]
    for region in regions:
        if region in text_lower:
            score += 5
    score = min(score, 20)
    
    # Fund type (0-20)
    if "private equity" in text_lower or "pe" in text_lower:
        score += 10
    if "venture capital" in text_lower or "vc" in text_lower:
        score += 10
    
    # Portfolio fit (0-20)
    if "portfolio" in text_lower:
        score += 5
    if "autonomous" in text_lower or "technology" in text_lower:
        score += 5
    
    return min(score, 100)

def deduplicate_companies():
    """Remove duplicate companies."""
    seen = set()
    unique = []
    for company in results["companies"]:
        name = company.get("name", "").lower()
        # Normalize name
        name = name.replace(" - ", " ").replace(" | ", " ").strip()
        if name not in seen and len(name) > 3:
            seen.add(name)
            unique.append(company)
    results["companies"] = unique

def save_results():
    """Save results to files."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Save companies
    companies_file = Path(f"defense-leads/daily-companies-{today}.md")
    companies_content = f"# Defense Companies - {today}\n\n"
    companies_content += f"Generated: {datetime.now().isoformat()}\n\n"
    
    # Sort by score
    sorted_companies = sorted(results["companies"], key=lambda x: x.get("defense_score", 0), reverse=True)
    
    for i, company in enumerate(sorted_companies[:15], 1):
        score = company.get("defense_score", 0)
        priority = "🟢 High" if score >= 70 else "🟡 Medium" if score >= 50 else "🔴 Low"
        companies_content += f"## {i}. {company.get('name', 'Unknown')}\n"
        companies_content += f"**Score:** {score}/100 | **Priority:** {priority}\n\n"
        companies_content += f"**URL:** {company.get('url', 'N/A')}\n\n"
        companies_content += f"**Description:** {company.get('description', 'N/A')[:500]}\n\n"
        companies_content += f"**Source:** {company.get('source', 'Unknown')}\n\n"
        companies_content += "---\n\n"
    
    companies_file.write_text(companies_content)
    print(f"✅ Saved companies to {companies_file}")
    
    # Save investors
    investors_file = Path(f"defense-leads/daily-investors-{today}.md")
    investors_content = f"# Defense Investors (Asia/India) - {today}\n\n"
    investors_content += f"Generated: {datetime.now().isoformat()}\n\n"
    
    sorted_investors = sorted(results["investors"], key=lambda x: x.get("score", 0), reverse=True)
    
    for i, investor in enumerate(sorted_investors[:10], 1):
        score = investor.get("score", 0)
        priority = "🟢 High" if score >= 60 else "🟡 Medium" if score >= 40 else "🔴 Low"
        investors_content += f"## {i}. {investor.get('name', 'Unknown')}\n"
        investors_content += f"**Score:** {score}/100 | **Priority:** {priority}\n\n"
        investors_content += f"**URL:** {investor.get('url', 'N/A')}\n\n"
        investors_content += f"**Description:** {investor.get('description', 'N/A')[:500]}\n\n"
        investors_content += "---\n\n"
    
    investors_file.write_text(investors_content)
    print(f"✅ Saved investors to {investors_file}")

def generate_report():
    """Generate Discord report."""
    elapsed = (datetime.now() - results["start_time"]).total_seconds()
    
    # Sort companies by score
    sorted_companies = sorted(results["companies"], key=lambda x: x.get("defense_score", 0), reverse=True)
    high_priority = [c for c in sorted_companies if c.get("defense_score", 0) >= 70]
    
    # Sort investors by score
    sorted_investors = sorted(results["investors"], key=lambda x: x.get("score", 0), reverse=True)
    defense_focused = [i for i in sorted_investors if i.get("score", 0) >= 50]
    
    report = f"""🛡️ **Defense Sector Report (Scrapling-Enhanced)**

## Companies (US/UK/EU)
- Identified: {len(results["companies"])}
- High priority (70+): {len(high_priority)}
- Top 3: """
    
    for c in sorted_companies[:3]:
        name = c.get("name", "Unknown")[:30]
        score = c.get("defense_score", 0)
        report += f"\n  • {name} - Score: {score}"
    
    report += f"""

## Investors (Asia/India)
- PE/VC funds: {len(results["investors"])}
- Defense-focused: {len(defense_focused)}
- Top 3: """
    
    for i in sorted_investors[:3]:
        name = i.get("name", "Unknown")[:30]
        score = i.get("score", 0)
        report += f"\n  • {name} - Score: {score}"
    
    report += f"""

🔍 **Data Source:**
- Scrapling Used: {'✅ Yes' if results['scrapling_used'] else '❌ No'}
- Scrapling Results: {results['scrapling_results']}
- Tavily Results: {results['tavily_results']}
- Brave Results: {results['brave_results']}
- Processing Time: {elapsed:.1f} seconds"""
    
    return report

async def main():
    print("🚀 Starting Defense Sector Lead Generation")
    print("=" * 50)
    
    # Try Scrapling first
    scrapling_success = await try_scrapling()
    
    # If Scrapling didn't return enough results, try Tavily
    if results["scrapling_results"] < 5:
        await try_tavily()
    
    # If still not enough, try Brave
    if len(results["companies"]) < 5:
        await try_brave()
    
    # Deduplicate
    deduplicate_companies()
    
    # Search for investors
    await search_investors()
    
    # Save results
    save_results()
    
    # Generate report
    report = generate_report()
    print("\n" + "=" * 50)
    print(report)
    
    return report

if __name__ == "__main__":
    report = asyncio.run(main())
