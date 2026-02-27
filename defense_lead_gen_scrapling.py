#!/usr/bin/env python3
"""
Defense Sector Lead Generation - Scrapling-First Enhanced
"""
import sys
import os
import asyncio
import json
import time
from datetime import datetime
from pathlib import Path

# Add Scrapling to path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# Create output directory
output_dir = Path('/Users/cubiczan/.openclaw/workspace/defense-leads')
output_dir.mkdir(exist_ok=True)

today = datetime.now().strftime('%Y-%m-%d')

# Scoring functions
def score_company(company):
    """Score defense company (0-100)"""
    score = 0
    
    # Sector fit (0-30)
    sector_keywords = ['cybersecurity', 'ai', 'drone', 'counter-drone', 'c-uas', 
                       'space', 'satellite', 'defense', 'military', 'autonomous']
    name_desc = f"{company.get('name', '')} {company.get('description', '')}".lower()
    sector_matches = sum(1 for kw in sector_keywords if kw in name_desc)
    score += min(30, sector_matches * 10)
    
    # Stage fit (0-20)
    stage = company.get('stage', '').lower()
    if any(s in stage for s in ['series a', 'series b', 'series c', 'early', 'mid']):
        score += 20
    elif 'seed' in stage:
        score += 15
    
    # Technical depth (0-20)
    tech_keywords = ['ai', 'machine learning', 'autonomous', 'quantum', 'encryption', 
                     'radar', 'sensor', 'surveillance', 'intelligence']
    tech_matches = sum(1 for kw in tech_keywords if kw in name_desc)
    score += min(20, tech_matches * 5)
    
    # Region match (0-10)
    region = company.get('region', '').lower()
    if any(r in region for r in ['us', 'usa', 'uk', 'eu', 'europe', 'united states']):
        score += 10
    
    # Integration potential (0-20)
    if any(kw in name_desc for kw in ['platform', 'api', 'integration', 'sdk']):
        score += 20
    
    return min(100, score)

def score_investor(fund):
    """Score PE/VC fund (0-100)"""
    score = 0
    
    name_desc = f"{fund.get('name', '')} {fund.get('focus', '')} {fund.get('description', '')}".lower()
    
    # Defense/drone focus (0-40)
    defense_keywords = ['defense', 'drone', 'uav', 'aerospace', 'autonomous', 
                        'security', 'surveillance', 'military', 'dual-use']
    defense_matches = sum(1 for kw in defense_keywords if kw in name_desc)
    score += min(40, defense_matches * 10)
    
    # Region match (0-20) - Asia/India focused
    region = fund.get('region', '').lower()
    if any(r in region for r in ['india', 'singapore', 'japan', 'korea', 'taiwan', 
                                  'southeast asia', 'middle east', 'asia']):
        score += 20
    
    # Portfolio fit (0-20)
    portfolio_keywords = ['autonomous', 'robotics', 'ai', 'tech', 'hardware']
    portfolio_matches = sum(1 for kw in portfolio_keywords if kw in name_desc)
    score += min(20, portfolio_matches * 5)
    
    # Fund size/stage (0-20)
    size = fund.get('size', '').lower()
    if any(s in size for s in ['series a', 'series b', 'growth', 'venture']):
        score += 20
    elif 'early' in size:
        score += 15
    
    return min(100, score)

async def try_scrapling_search():
    """Attempt to use Scrapling for defense company search"""
    try:
        from cron_integration import ScraplingCronIntegration
        
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if not success:
            return None, "Initialization failed"
        
        search_terms = [
            "defense technology companies Series A B",
            "cybersecurity military defense startups",
            "counter-drone C-UAS companies Europe",
            "space defense technology startups UK",
            "military AI companies Series A funding"
        ]
        
        all_companies = []
        for term in search_terms:
            try:
                results = await scrapling.search_and_extract(term, max_results=5)
                if results:
                    all_companies.extend(results)
            except Exception as e:
                print(f"Scrapling search error for '{term}': {e}")
                continue
        
        return all_companies, "Success"
    except ImportError as e:
        return None, f"Import error: {e}"
    except Exception as e:
        return None, f"Error: {e}"

def search_with_tavily(query, api_key):
    """Fallback search using Tavily API"""
    import urllib.request
    import urllib.parse
    
    url = "https://api.tavily.com/search"
    data = json.dumps({
        "api_key": api_key,
        "query": query,
        "search_depth": "advanced",
        "max_results": 10
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('results', [])
    except Exception as e:
        print(f"Tavily error: {e}")
        return []

def search_with_brave(query, api_key):
    """Second fallback using Brave Search API"""
    import urllib.request
    import urllib.parse
    
    url = f"https://api.search.brave.com/res/v1/web/search?q={urllib.parse.quote(query)}&count=10"
    req = urllib.request.Request(url, headers={
        'Accept': 'application/json',
        'X-Subscription-Token': api_key
    })
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('web', {}).get('results', [])
    except Exception as e:
        print(f"Brave error: {e}")
        return []

def parse_company_result(result, source='api'):
    """Parse API result into company format"""
    return {
        'name': result.get('title', 'Unknown'),
        'description': result.get('description', result.get('snippet', '')),
        'url': result.get('url', result.get('link', '')),
        'stage': 'Unknown',
        'region': 'Unknown',
        'source': source
    }

def parse_investor_result(result, source='api'):
    """Parse API result into investor format"""
    return {
        'name': result.get('title', 'Unknown'),
        'focus': result.get('description', result.get('snippet', '')),
        'description': result.get('description', result.get('snippet', '')),
        'url': result.get('url', result.get('link', '')),
        'region': 'Unknown',
        'size': 'Unknown',
        'source': source
    }

async def main():
    start_time = time.time()
    
    tavily_key = "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"
    brave_key = "cac43a248afb1cc1ec004370df2e0282a67eb420"
    
    # Track data sources
    scrapling_used = False
    scrapling_results = 0
    api_results = 0
    
    companies = []
    investors = []
    
    print("🔍 Attempting Scrapling search...")
    scrapling_data, scrapling_status = await try_scrapling_search()
    
    if scrapling_data and len(scrapling_data) > 0:
        print(f"✅ Scrapling returned {len(scrapling_data)} results")
        scrapling_used = True
        scrapling_results = len(scrapling_data)
        for item in scrapling_data:
            companies.append(parse_company_result(item, 'scrapling'))
    else:
        print(f"⚠️ Scrapling failed: {scrapling_status}")
        print("📡 Falling back to Tavily API...")
        
        # Defense company searches
        company_queries = [
            "defense technology companies Series A B funding 2024 2025",
            "cybersecurity defense military startups US UK EU",
            "counter-drone anti-drone C-UAS companies Europe",
            "space defense satellite technology startups",
            "military AI artificial intelligence defense companies"
        ]
        
        for query in company_queries:
            results = search_with_tavily(query, tavily_key)
            if results:
                api_results += len(results)
                for r in results:
                    companies.append(parse_company_result(r, 'tavily'))
            else:
                # Try Brave as second fallback
                brave_results = search_with_brave(query, brave_key)
                if brave_results:
                    api_results += len(brave_results)
                    for r in brave_results:
                        companies.append(parse_company_result(r, 'brave'))
    
    # Search for PE/VC funds in Asia/India (using APIs)
    print("📡 Searching for PE/VC funds in Asia/India...")
    
    investor_queries = [
        "venture capital defense technology India Singapore",
        "private equity drone aerospace Asia investments",
        "VC fund autonomous systems Japan Korea Taiwan",
        "defense tech investor Southeast Asia Middle East",
        "aerospace drone technology venture capital India"
    ]
    
    for query in investor_queries:
        results = search_with_tavily(query, tavily_key)
        if results:
            for r in results:
                investors.append(parse_investor_result(r, 'tavily'))
        else:
            brave_results = search_with_brave(query, brave_key)
            if brave_results:
                for r in brave_results:
                    investors.append(parse_investor_result(r, 'brave'))
    
    # Deduplicate and score companies
    seen_companies = set()
    scored_companies = []
    for c in companies:
        name_lower = c['name'].lower()
        if name_lower not in seen_companies and len(name_lower) > 3:
            seen_companies.add(name_lower)
            c['score'] = score_company(c)
            scored_companies.append(c)
    
    # Deduplicate and score investors
    seen_investors = set()
    scored_investors = []
    for i in investors:
        name_lower = i['name'].lower()
        if name_lower not in seen_investors and len(name_lower) > 3:
            # Exclude China
            if 'china' not in name_lower and 'china' not in i.get('region', '').lower():
                seen_investors.add(name_lower)
                i['score'] = score_investor(i)
                scored_investors.append(i)
    
    # Sort by score
    scored_companies.sort(key=lambda x: x['score'], reverse=True)
    scored_investors.sort(key=lambda x: x['score'], reverse=True)
    
    # Take top results
    top_companies = scored_companies[:10]
    top_investors = scored_investors[:5]
    
    high_priority_companies = [c for c in top_companies if c['score'] >= 70]
    defense_focused_investors = [i for i in top_investors if i['score'] >= 50]
    
    # Save company results
    company_file = output_dir / f"daily-companies-{today}.md"
    with open(company_file, 'w') as f:
        f.write(f"# Defense Companies - {today}\n\n")
        f.write(f"**Total Identified:** {len(scored_companies)}\n")
        f.write(f"**High Priority (70+):** {len(high_priority_companies)}\n\n")
        
        for i, c in enumerate(top_companies, 1):
            f.write(f"## {i}. {c['name']} (Score: {c['score']})\n\n")
            f.write(f"**Description:** {c['description']}\n\n")
            f.write(f"**URL:** {c['url']}\n\n")
            f.write(f"**Source:** {c.get('source', 'unknown')}\n\n")
            f.write("---\n\n")
    
    # Save investor results
    investor_file = output_dir / f"daily-investors-{today}.md"
    with open(investor_file, 'w') as f:
        f.write(f"# PE/VC Funds (Asia/India) - {today}\n\n")
        f.write(f"**Total Identified:** {len(scored_investors)}\n")
        f.write(f"**Defense-Focused:** {len(defense_focused_investors)}\n\n")
        
        for i, inv in enumerate(top_investors, 1):
            f.write(f"## {i}. {inv['name']} (Score: {inv['score']})\n\n")
            f.write(f"**Focus:** {inv['focus']}\n\n")
            f.write(f"**URL:** {inv['url']}\n\n")
            f.write(f"**Source:** {inv.get('source', 'unknown')}\n\n")
            f.write("---\n\n")
    
    processing_time = time.time() - start_time
    
    # Generate report
    report = {
        'companies_total': len(scored_companies),
        'companies_high_priority': len(high_priority_companies),
        'top_companies': [
            {'name': c['name'], 'score': c['score'], 'description': c['description'][:100]}
            for c in top_companies[:3]
        ],
        'investors_total': len(scored_investors),
        'investors_defense_focused': len(defense_focused_investors),
        'top_investors': [
            {'name': i['name'], 'score': i['score'], 'focus': i['focus'][:100]}
            for i in top_investors[:3]
        ],
        'scrapling_used': scrapling_used,
        'scrapling_results': scrapling_results,
        'api_results': api_results,
        'processing_time': round(processing_time, 2),
        'company_file': str(company_file),
        'investor_file': str(investor_file)
    }
    
    print(json.dumps(report, indent=2))
    return report

if __name__ == "__main__":
    asyncio.run(main())
