#!/usr/bin/env python3
"""
Defense Sector Lead Generation - Scrapling-First Approach
"""

import sys
import os
import asyncio
import json
from datetime import datetime
from pathlib import Path

# Add scrapling integration to path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# Output directory
OUTPUT_DIR = Path('/Users/cubiczan/.openclaw/workspace/defense-leads')
OUTPUT_DIR.mkdir(exist_ok=True)

# Today's date
TODAY = datetime.now().strftime('%Y-%m-%d')

# Track data sources
data_sources = {
    'scrapling_used': False,
    'scrapling_results': 0,
    'tavily_results': 0,
    'brave_results': 0,
    'processing_time': 0
}

async def try_scrapling():
    """Try to use Scrapling for data extraction"""
    try:
        from cron_integration import ScraplingCronIntegration
        
        print("🔍 Initializing Scrapling with stealth mode...")
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if success:
            print("✅ Scrapling initialized successfully")
            data_sources['scrapling_used'] = True
            
            # Search for defense companies
            search_terms = [
                "defense technology companies Series A B C funding 2024 2025",
                "cybersecurity defense military companies US UK EU",
                "counter-drone C-UAS anti-drone systems companies",
                "space defense technology satellite companies",
                "military AI machine learning defense companies"
            ]
            
            companies = await scrapling.scrape_defense_companies(search_terms)
            
            if companies:
                data_sources['scrapling_results'] = len(companies)
                print(f"✅ Scrapling found {len(companies)} companies")
                return companies
            else:
                print("⚠️ Scrapling returned no results")
                return []
        else:
            print("⚠️ Scrapling initialization failed")
            return []
    except Exception as e:
        print(f"⚠️ Scrapling error: {e}")
        return []

async def try_tavily():
    """Fallback to Tavily API"""
    import aiohttp
    
    print("🔍 Using Tavily API as fallback...")
    
    api_key = "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"
    
    search_queries = [
        "defense technology companies Series A B C funding 2024 2025 US UK EU",
        "cybersecurity military defense companies early stage funding",
        "counter-drone anti-drone C-UAS companies investment",
        "space defense technology satellite companies startup",
        "military AI machine learning defense contractors startup"
    ]
    
    companies = []
    
    async with aiohttp.ClientSession() as session:
        for query in search_queries:
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
                        results = data.get('results', [])
                        
                        for result in results:
                            companies.append({
                                'name': result.get('title', 'Unknown'),
                                'url': result.get('url', ''),
                                'description': result.get('content', ''),
                                'source': 'tavily'
                            })
                
                await asyncio.sleep(0.5)  # Rate limiting
                
            except Exception as e:
                print(f"⚠️ Tavily query error: {e}")
    
    data_sources['tavily_results'] = len(companies)
    print(f"✅ Tavily found {len(companies)} results")
    return companies

async def try_brave_search():
    """Second fallback to Brave Search API"""
    import aiohttp
    
    print("🔍 Using Brave Search API as fallback...")
    
    api_key = "cac43a248afb1cc1ec004370df2e0282a67eb420"
    
    search_queries = [
        "defense technology companies startup funding 2024 2025",
        "cybersecurity military defense companies Series A",
        "counter-drone anti-drone systems startup",
        "space defense technology satellite companies",
        "military AI companies early stage"
    ]
    
    companies = []
    
    async with aiohttp.ClientSession() as session:
        for query in search_queries:
            try:
                headers = {
                    "X-Subscription-Token": api_key,
                    "Accept": "application/json"
                }
                
                params = {
                    "q": query,
                    "count": 5
                }
                
                async with session.get("https://api.search.brave.com/res/v1/web/search", 
                                      headers=headers, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        results = data.get('web', {}).get('results', [])
                        
                        for result in results:
                            companies.append({
                                'name': result.get('title', 'Unknown'),
                                'url': result.get('url', ''),
                                'description': result.get('description', ''),
                                'source': 'brave'
                            })
                
                await asyncio.sleep(0.5)  # Rate limiting
                
            except Exception as e:
                print(f"⚠️ Brave Search query error: {e}")
    
    data_sources['brave_results'] = len(companies)
    print(f"✅ Brave Search found {len(companies)} results")
    return companies

async def search_asian_investors():
    """Search for PE/VC funds in Asia/India"""
    import aiohttp
    
    print("🔍 Searching for Asian PE/VC funds...")
    
    # Use Tavily for investor search
    api_key = "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"
    
    search_queries = [
        "private equity venture capital defense technology India Singapore",
        "VC funds drone aerospace technology Asia Japan Korea",
        "defense tech investors Taiwan Southeast Asia",
        "autonomous systems drone technology investors India",
        "aerospace defense fund Middle East Singapore"
    ]
    
    investors = []
    
    async with aiohttp.ClientSession() as session:
        for query in search_queries:
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
                        results = data.get('results', [])
                        
                        for result in results:
                            investors.append({
                                'name': result.get('title', 'Unknown'),
                                'url': result.get('url', ''),
                                'description': result.get('content', ''),
                                'source': 'tavily'
                            })
                
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"⚠️ Investor search error: {e}")
    
    print(f"✅ Found {len(investors)} investor leads")
    return investors

def score_company(company):
    """Score a defense company (0-100)"""
    score = 0
    
    # Sector fit (0-30)
    sectors = ['cybersecurity', 'ai', 'machine learning', 'drone', 'counter-drone', 
               'c-uas', 'space', 'satellite', 'defense', 'military', 'autonomous']
    desc_lower = company.get('description', '').lower()
    name_lower = company.get('name', '').lower()
    
    sector_matches = sum(1 for s in sectors if s in desc_lower or s in name_lower)
    score += min(30, sector_matches * 10)
    
    # Stage fit (0-20)
    stages = ['series a', 'series b', 'series c', 'early stage', 'startup', 'funding']
    stage_matches = sum(1 for s in stages if s in desc_lower)
    score += min(20, stage_matches * 10)
    
    # Technical depth (0-20)
    tech_terms = ['ai', 'ml', 'autonomous', 'quantum', 'encryption', 'satellite', 
                  'sensor', 'radar', 'platform', 'system']
    tech_matches = sum(1 for t in tech_terms if t in desc_lower)
    score += min(20, tech_matches * 4)
    
    # Integration potential (0-20)
    integration_terms = ['platform', 'api', 'integration', 'software', 'dual-use']
    int_matches = sum(1 for i in integration_terms if i in desc_lower)
    score += min(20, int_matches * 5)
    
    # Region match (0-10)
    regions = ['us', 'usa', 'uk', 'united kingdom', 'eu', 'europe', 'germany', 
               'france', 'netherlands', 'sweden', 'israel']
    region_matches = sum(1 for r in regions if r in desc_lower or r in name_lower)
    score += min(10, region_matches * 5)
    
    return score

def score_investor(investor):
    """Score a PE/VC fund (0-100)"""
    score = 0
    
    desc_lower = investor.get('description', '').lower()
    name_lower = investor.get('name', '').lower()
    
    # Defense/drone focus (0-40)
    defense_terms = ['defense', 'military', 'drone', 'aerospace', 'autonomous', 
                     'security', 'surveillance', 'uav', 'dual-use']
    defense_matches = sum(1 for d in defense_terms if d in desc_lower or d in name_lower)
    score += min(40, defense_matches * 8)
    
    # Region match (0-20)
    regions = ['india', 'singapore', 'japan', 'korea', 'taiwan', 'southeast asia', 
               'middle east', 'dubai', 'abu dhabi']
    region_matches = sum(1 for r in regions if r in desc_lower or r in name_lower)
    score += min(20, region_matches * 5)
    
    # Portfolio fit (0-20)
    portfolio_terms = ['portfolio', 'investment', 'startup', 'technology', 'series']
    portfolio_matches = sum(1 for p in portfolio_terms if p in desc_lower)
    score += min(20, portfolio_matches * 5)
    
    # Fund size/stage (0-20)
    fund_terms = ['fund', 'capital', 'ventures', 'pe', 'private equity', 'vc']
    fund_matches = sum(1 for f in fund_terms if f in desc_lower or f in name_lower)
    score += min(20, fund_matches * 5)
    
    return score

def save_companies(companies):
    """Save company leads to markdown file"""
    filepath = OUTPUT_DIR / f'daily-companies-{TODAY}.md'
    
    # Score and deduplicate
    scored_companies = []
    seen_names = set()
    
    for company in companies:
        name = company.get('name', '')
        if name and name not in seen_names:
            company['score'] = score_company(company)
            scored_companies.append(company)
            seen_names.add(name)
    
    # Sort by score
    scored_companies.sort(key=lambda x: x['score'], reverse=True)
    
    # Generate markdown
    content = f"""# Defense Company Leads - {TODAY}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- Total Leads: {len(scored_companies)}
- High Priority (70+): {len([c for c in scored_companies if c['score'] >= 70])}
- Data Sources: Scrapling={data_sources['scrapling_results']}, Tavily={data_sources['tavily_results']}, Brave={data_sources['brave_results']}

## Top Leads

"""
    
    for i, company in enumerate(scored_companies[:10], 1):
        content += f"""### {i}. {company['name']} (Score: {company['score']})

**URL:** {company.get('url', 'N/A')}

**Description:** {company.get('description', 'N/A')[:300]}

**Source:** {company.get('source', 'unknown')}

---

"""
    
    # Write file
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"✅ Saved {len(scored_companies)} companies to {filepath}")
    return scored_companies

def save_investors(investors):
    """Save investor leads to markdown file"""
    filepath = OUTPUT_DIR / f'daily-investors-{TODAY}.md'
    
    # Score and deduplicate
    scored_investors = []
    seen_names = set()
    
    for investor in investors:
        name = investor.get('name', '')
        # Filter out China
        if name and 'china' not in name.lower() and 'chinese' not in name.lower():
            if name not in seen_names:
                investor['score'] = score_investor(investor)
                scored_investors.append(investor)
                seen_names.add(name)
    
    # Sort by score
    scored_investors.sort(key=lambda x: x['score'], reverse=True)
    
    # Generate markdown
    content = f"""# Defense Investor Leads (Asia/India) - {TODAY}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- Total Funds: {len(scored_investors)}
- Defense-Focused (60+): {len([i for i in scored_investors if i['score'] >= 60])}
- Regions: India, Singapore, Japan, Korea, Taiwan, SE Asia, Middle East

## Top Funds

"""
    
    for i, investor in enumerate(scored_investors[:5], 1):
        content += f"""### {i}. {investor['name']} (Score: {investor['score']})

**URL:** {investor.get('url', 'N/A')}

**Description:** {investor.get('description', 'N/A')[:300]}

**Source:** {investor.get('source', 'unknown')}

---

"""
    
    # Write file
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"✅ Saved {len(scored_investors)} investors to {filepath}")
    return scored_investors

async def main():
    """Main execution"""
    import time
    start_time = time.time()
    
    print("=" * 60)
    print("🛡️ Defense Sector Lead Generation - Scrapling-First")
    print("=" * 60)
    
    # Step 1: Try Scrapling first
    companies = await try_scrapling()
    
    # Step 2: Fallback to Tavily if needed
    if len(companies) < 5:
        print("\n⚠️ Insufficient Scrapling results, using Tavily API...")
        tavily_companies = await try_tavily()
        companies.extend(tavily_companies)
    
    # Step 3: Fallback to Brave if still insufficient
    if len(companies) < 5:
        print("\n⚠️ Insufficient results, using Brave Search API...")
        brave_companies = await try_brave_search()
        companies.extend(brave_companies)
    
    # Step 4: Search for Asian investors
    investors = await search_asian_investors()
    
    # Calculate processing time
    data_sources['processing_time'] = round(time.time() - start_time, 2)
    
    # Step 5: Save results
    scored_companies = save_companies(companies)
    scored_investors = save_investors(investors)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Companies Identified: {len(scored_companies)}")
    print(f"High Priority (70+): {len([c for c in scored_companies if c['score'] >= 70])}")
    print(f"Investor Funds: {len(scored_investors)}")
    print(f"Defense-Focused (60+): {len([i for i in scored_investors if i['score'] >= 60])}")
    print(f"\n🔍 Data Sources:")
    print(f"  - Scrapling Used: {'✅ Yes' if data_sources['scrapling_used'] else '❌ No'}")
    print(f"  - Scrapling Results: {data_sources['scrapling_results']}")
    print(f"  - Tavily Results: {data_sources['tavily_results']}")
    print(f"  - Brave Results: {data_sources['brave_results']}")
    print(f"  - Processing Time: {data_sources['processing_time']}s")
    print("=" * 60)
    
    # Return results for Discord reporting
    return {
        'companies': scored_companies,
        'investors': scored_investors,
        'data_sources': data_sources
    }

if __name__ == "__main__":
    results = asyncio.run(main())
    
    # Output JSON for processing
    print("\n__RESULTS_JSON__")
    print(json.dumps({
        'companies_count': len(results['companies']),
        'high_priority_companies': len([c for c in results['companies'] if c['score'] >= 70]),
        'investors_count': len(results['investors']),
        'defense_focused_investors': len([i for i in results['investors'] if i['score'] >= 60]),
        'top_3_companies': [
            {'name': c['name'], 'score': c['score'], 'sector': 'Defense Tech'} 
            for c in results['companies'][:3]
        ],
        'top_3_investors': [
            {'name': i['name'], 'score': i['score'], 'region': 'Asia/India'} 
            for i in results['investors'][:3]
        ],
        'data_sources': results['data_sources']
    }))
