#!/usr/bin/env python3
"""
Defense Sector Lead Generation - Scrapling-First Enhanced v2
Fixed to use correct Scrapling methods and better search queries
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

# Defense company database - known active companies
DEFENSE_COMPANIES = [
    {"name": "Anduril Industries", "sector": "Defense AI & Autonomy", "url": "https://www.anduril.com", "region": "US", "stage": "Series E"},
    {"name": "Palantir Technologies", "sector": "Defense Data Analytics", "url": "https://www.palantir.com", "region": "US", "stage": "Public"},
    {"name": "Shield AI", "sector": "AI & Drones", "url": "https://shield.ai", "region": "US", "stage": "Series F"},
    {"name": "Skydio", "sector": "Autonomous Drones", "url": "https://www.skydio.com", "region": "US", "stage": "Series E"},
    {"name": "Epirus", "sector": "Counter-Drone (C-UAS)", "url": "https://www.epirusinc.com", "region": "US", "stage": "Series C"},
    {"name": "Dedrone", "sector": "Counter-Drone", "url": "https://www.dedrone.com", "region": "US", "stage": "Acquired"},
    {"name": "AEVEX Aerospace", "sector": "Space & ISR", "url": "https://www.aevex.com", "region": "US", "stage": "Private"},
    {"name": "BlackSky", "sector": "Space-Based ISR", "url": "https://www.blacksky.com", "region": "US", "stage": "Public"},
    {"name": "Planet Labs", "sector": "Space & Satellite", "url": "https://www.planet.com", "region": "US", "stage": "Public"},
    {"name": "Rebellion Defense", "sector": "Defense AI", "url": "https://www.rebelliondefense.com", "region": "US", "stage": "Series B"},
    {"name": "Hidden Level", "sector": "Counter-Drone", "url": "https://www.hiddenlevel.com", "region": "US", "stage": "Series A"},
    {"name": "AeroVironment", "sector": "Military Drones", "url": "https://www.avinc.com", "region": "US", "stage": "Public"},
    {"name": "Kratos Defense", "sector": "Defense Systems", "url": "https://www.kratosdefense.com", "region": "US", "stage": "Public"},
    {"name": "Fortem Technologies", "sector": "Counter-Drone", "url": "https://fortemtech.com", "region": "US", "stage": "Series C"},
    {"name": "Improbable", "sector": "Defense Simulation", "url": "https://improbable.io", "region": "UK", "stage": "Series D"},
    {"name": "Helsing", "sector": "Defense AI", "url": "https://www.helsing.ai", "region": "EU", "stage": "Series C"},
    {"name": "Quantum Systems", "sector": "Drone Systems", "url": "https://quantum-systems.com", "region": "EU", "stage": "Series B"},
    {"name": "Tekever", "sector": "UAV Systems", "url": "https://www.tekever.com", "region": "EU", "stage": "Private"},
    {"name": "Marlinspike", "sector": "Cybersecurity", "url": "https://marlinspike.com", "region": "US", "stage": "Series B"},
    {"name": "Dragos", "sector": "Industrial Cybersecurity", "url": "https://www.dragos.com", "region": "US", "stage": "Series D"},
]

# PE/VC funds in Asia/India focused on defense/drones
ASIA_INVESTORS = [
    {"name": "Speciale Invest", "region": "India", "focus": "Deep Tech, Defense, Drones", "url": "https://www.specialeinvest.com", "stage": "Early"},
    {"name": "Bluehill.VC", "region": "India", "focus": "Defense Tech, AI", "url": "https://bluehill.vc", "stage": "Early"},
    {"name": "Pi Ventures", "region": "India", "focus": "AI, Deep Tech", "url": "https://pi-ventures.com", "stage": "Early"},
    {"name": "Blume Ventures", "region": "India", "focus": "Deep Tech, Aerospace", "url": "https://blume.vc", "stage": "All"},
    {"name": "Sequoia India", "region": "India/Singapore", "focus": "AI, Security", "url": "https://www.sequoiacap.com/india", "stage": "All"},
    {"name": "Vertex Holdings", "region": "Singapore", "focus": "Deep Tech", "url": "https://www.vertexholdings.com", "stage": "All"},
    {"name": "Temasek Holdings", "region": "Singapore", "focus": "Defense, Tech", "url": "https://www.temasek.com.sg", "stage": "Growth"},
    {"name": "GIC", "region": "Singapore", "focus": "Technology", "url": "https://www.gic.com.sg", "stage": "All"},
    {"name": "JAFCO Asia", "region": "Japan/Singapore", "focus": "Tech, Industrial", "url": "https://www.jafco.co.jp", "stage": "All"},
    {"name": "SoftBank Vision", "region": "Japan", "focus": "AI, Robotics", "url": "https://visionfund.softbank", "stage": "Growth"},
    {"name": "Global Brain", "region": "Japan", "focus": "Deep Tech, AI", "url": "https://globalbrain.co.jp", "stage": "All"},
    {"name": "DCM Ventures Japan", "region": "Japan", "focus": "Tech", "url": "https://www.dcm.com", "stage": "Early"},
    {"name": "KIP (Korea Investment Partners)", "region": "Korea", "focus": "Tech, Industrial", "url": "https://www.kipvc.com", "stage": "All"},
    {"name": "Altos Ventures", "region": "Korea", "focus": "Tech", "url": "https://www.altos.vc", "stage": "All"},
    {"name": "FuturePlay", "region": "Korea", "focus": "Deep Tech", "url": "https://www.futureplay.co.kr", "stage": "Early"},
    {"name": "AppWorks", "region": "Taiwan", "focus": "AI, Deep Tech", "url": "https://appworks.tw", "stage": "Early"},
    {"name": "Taiwan Startup Stadium", "region": "Taiwan", "focus": "Hardware, Tech", "url": "https://startupstadium.tw", "stage": "Early"},
    {"name": " monk's hill ventures", "region": "Southeast Asia", "focus": "Tech", "url": "https://www.monkshill.com", "stage": "Early"},
    {"name": "Insignia Ventures", "region": "Southeast Asia", "focus": "Deep Tech", "url": "https://www.insignia.vc", "stage": "Early"},
    {"name": "East Ventures", "region": "Southeast Asia", "focus": "Tech", "url": "https://east.vc", "stage": "All"},
    {"name": "Mubadala Investment", "region": "UAE", "focus": "Defense, Tech", "url": "https://www.mubadala.com", "stage": "Growth"},
    {"name": "G42", "region": "UAE", "focus": "AI, Defense Tech", "url": "https://g42.ai", "stage": "All"},
]

# Scoring functions
def score_company(company):
    """Score defense company (0-100)"""
    score = 0
    
    # Sector fit (0-30)
    sector = company.get('sector', '').lower()
    high_value_sectors = ['counter-drone', 'ai & drones', 'defense ai', 'cybersecurity']
    if any(s in sector for s in high_value_sectors):
        score += 30
    elif any(s in sector for s in ['defense', 'drone', 'space', 'military']):
        score += 25
    elif 'autonomous' in sector:
        score += 20
    else:
        score += 10
    
    # Stage fit (0-20)
    stage = company.get('stage', '').lower()
    if 'series a' in stage or 'series b' in stage or 'series c' in stage:
        score += 20
    elif 'series d' in stage or 'series e' in stage:
        score += 15
    elif 'private' in stage:
        score += 12
    elif 'seed' in stage:
        score += 10
    elif 'public' in stage:
        score += 5
    
    # Region match (0-10)
    region = company.get('region', '').lower()
    if region in ['us', 'usa', 'uk', 'eu', 'europe']:
        score += 10
    elif 'united states' in region:
        score += 10
    
    # Technical depth bonus (0-20)
    name = company.get('name', '').lower()
    if any(kw in name for kw in ['ai', 'quantum', 'cyber', 'autonomous']):
        score += 20
    elif any(kw in name for kw in ['systems', 'tech', 'labs']):
        score += 10
    
    # Integration potential (0-20)
    sector_lower = company.get('sector', '').lower()
    if any(kw in sector_lower for kw in ['platform', 'ai', 'data', 'analytics']):
        score += 20
    elif any(kw in sector_lower for kw in ['systems', 'software']):
        score += 15
    
    return min(100, score)

def score_investor(fund):
    """Score PE/VC fund (0-100)"""
    score = 0
    
    focus = fund.get('focus', '').lower()
    name = fund.get('name', '').lower()
    
    # Defense/drone focus (0-40)
    if any(kw in focus for kw in ['defense', 'drone', 'aerospace']):
        score += 40
    elif any(kw in focus for kw in ['deep tech', 'autonomous', 'ai', 'security']):
        score += 30
    elif 'tech' in focus:
        score += 20
    else:
        score += 10
    
    # Region match (0-20) - Asia/India focused
    region = fund.get('region', '').lower()
    if any(r in region for r in ['india', 'singapore', 'japan', 'korea', 'taiwan', 'uae']):
        score += 20
    elif any(r in region for r in ['southeast asia', 'middle east', 'asia']):
        score += 15
    
    # Portfolio/stage fit (0-20)
    stage = fund.get('stage', '').lower()
    if 'early' in stage:
        score += 15
    elif 'all' in stage:
        score += 12
    elif 'growth' in stage:
        score += 10
    
    # Fund type bonus (0-20)
    if any(kw in name for kw in ['defense', 'aerospace', 'security']):
        score += 20
    elif 'deep tech' in focus or 'ai' in focus:
        score += 15
    
    return min(100, score)

def search_with_tavily(query, api_key):
    """Fallback search using Tavily API"""
    import urllib.request
    import urllib.parse
    
    url = "https://api.tavily.com/search"
    data = json.dumps({
        "api_key": api_key,
        "query": query,
        "search_depth": "advanced",
        "max_results": 10,
        "include_domains": []  # All domains
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('results', [])
    except Exception as e:
        print(f"Tavily error: {e}")
        return []

def parse_api_result(result, result_type='company'):
    """Parse API result into structured format"""
    if result_type == 'company':
        return {
            'name': result.get('title', 'Unknown'),
            'description': result.get('content', result.get('description', '')),
            'url': result.get('url', ''),
            'stage': 'Unknown',
            'region': 'Unknown',
            'sector': 'Unknown',
            'source': 'api'
        }
    else:
        return {
            'name': result.get('title', 'Unknown'),
            'focus': result.get('content', result.get('description', '')),
            'description': result.get('content', result.get('description', '')),
            'url': result.get('url', ''),
            'region': 'Unknown',
            'stage': 'Unknown',
            'source': 'api'
        }

async def main():
    start_time = time.time()
    
    tavily_key = "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"
    
    # Track data sources
    scrapling_used = False
    scrapling_results = 0
    api_results = 0
    
    companies = []
    investors = []
    
    print("=" * 60)
    print("🛡️ Defense Sector Lead Generation - Scrapling-First v2")
    print("=" * 60)
    
    # Try Scrapling for defense companies
    print("\n🔍 Attempting Scrapling search for defense companies...")
    try:
        from cron_integration import ScraplingCronIntegration
        
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if success:
            # Use the correct method - scrape_defense_companies
            search_terms = [
                "defense technology startups",
                "cybersecurity military",
                "drone technology",
                "space defense",
                "military AI"
            ]
            
            scrapling_companies = await scrapling.scrape_defense_companies(search_terms)
            
            if scrapling_companies and len(scrapling_companies) > 0:
                scrapling_used = True
                scrapling_results = len(scrapling_companies)
                print(f"✅ Scrapling returned {scrapling_results} defense companies")
                for c in scrapling_companies:
                    companies.append({
                        'name': c.get('company_name', 'Unknown'),
                        'description': c.get('description', ''),
                        'url': c.get('url', ''),
                        'sector': c.get('sector', 'Defense'),
                        'stage': 'Unknown',
                        'region': 'Unknown',
                        'source': 'scrapling'
                    })
            else:
                print("⚠️ Scrapling returned no results")
        else:
            print("⚠️ Scrapling initialization failed")
    except Exception as e:
        print(f"⚠️ Scrapling error: {e}")
    
    # Use known defense companies database as primary source
    print("\n📊 Loading defense companies database...")
    for c in DEFENSE_COMPANIES:
        companies.append({
            'name': c['name'],
            'description': f"{c['sector']} company",
            'url': c['url'],
            'sector': c['sector'],
            'stage': c['stage'],
            'region': c['region'],
            'source': 'database'
        })
    
    # Supplement with Tavily API search for recent news/developments
    print("\n📡 Supplementing with Tavily API search...")
    
    # Better search queries for actual companies
    company_queries = [
        "site:crunchbase.com defense technology startup Series A 2024 2025",
        "site:techcrunch.com defense drone startup funding",
        "counter-drone C-UAS startup company website",
        "defense AI startup raises funding 2025",
        "space defense technology startup Series B"
    ]
    
    for query in company_queries:
        results = search_with_tavily(query, tavily_key)
        if results:
            api_results += len(results)
            for r in results:
                parsed = parse_api_result(r, 'company')
                # Filter out article/list pages
                if not any(x in parsed['name'].lower() for x in ['list of', 'top 10', 'best', 'article']):
                    companies.append(parsed)
    
    # Load Asia/India investors database
    print("\n📊 Loading Asia/India investors database...")
    for i in ASIA_INVESTORS:
        investors.append({
            'name': i['name'],
            'focus': i['focus'],
            'description': f"VC/PE fund focused on {i['focus']}",
            'url': i['url'],
            'region': i['region'],
            'stage': i['stage'],
            'source': 'database'
        })
    
    # Supplement investors with API search
    investor_queries = [
        "venture capital fund defense technology India Singapore",
        "private equity drone aerospace investment Asia",
        "VC fund deep tech Japan Korea 2024 2025"
    ]
    
    for query in investor_queries:
        results = search_with_tavily(query, tavily_key)
        if results:
            api_results += len(results)
            for r in results:
                parsed = parse_api_result(r, 'investor')
                # Filter out article pages and China
                if 'china' not in parsed['name'].lower() and 'china' not in parsed.get('region', '').lower():
                    if not any(x in parsed['name'].lower() for x in ['list of', 'top 10', 'best', 'article']):
                        investors.append(parsed)
    
    # Deduplicate and score companies
    print("\n🎯 Scoring and ranking companies...")
    seen_companies = set()
    scored_companies = []
    for c in companies:
        name_lower = c['name'].lower().strip()
        if name_lower not in seen_companies and len(name_lower) > 3:
            seen_companies.add(name_lower)
            c['score'] = score_company(c)
            scored_companies.append(c)
    
    # Deduplicate and score investors
    print("🎯 Scoring and ranking investors...")
    seen_investors = set()
    scored_investors = []
    for i in investors:
        name_lower = i['name'].lower().strip()
        if name_lower not in seen_investors and len(name_lower) > 3:
            seen_investors.add(name_lower)
            i['score'] = score_investor(i)
            scored_investors.append(i)
    
    # Sort by score
    scored_companies.sort(key=lambda x: x['score'], reverse=True)
    scored_investors.sort(key=lambda x: x['score'], reverse=True)
    
    # Take top results
    top_companies = scored_companies[:10]
    top_investors = scored_investors[:5]
    
    high_priority_companies = [c for c in scored_companies if c['score'] >= 70]
    defense_focused_investors = [i for i in scored_investors if i['score'] >= 50]
    
    # Save company results
    company_file = output_dir / f"daily-companies-{today}.md"
    with open(company_file, 'w') as f:
        f.write(f"# Defense Companies - {today}\n\n")
        f.write(f"**Total Identified:** {len(scored_companies)}\n")
        f.write(f"**High Priority (70+):** {len(high_priority_companies)}\n\n")
        
        for i, c in enumerate(top_companies, 1):
            f.write(f"## {i}. {c['name']} (Score: {c['score']})\n\n")
            f.write(f"**Sector:** {c.get('sector', 'Unknown')}\n\n")
            f.write(f"**Stage:** {c.get('stage', 'Unknown')}\n\n")
            f.write(f"**Region:** {c.get('region', 'Unknown')}\n\n")
            f.write(f"**Description:** {c.get('description', 'N/A')}\n\n")
            f.write(f"**URL:** {c['url']}\n\n")
            f.write(f"**Source:** {c.get('source', 'unknown')}\n\n")
            f.write("---\n\n")
    
    # Save investor results
    investor_file = output_dir / f"daily-investors-{today}.md"
    with open(investor_file, 'w') as f:
        f.write(f"# PE/VC Funds (Asia/India) - {today}\n\n")
        f.write(f"**Total Identified:** {len(scored_investors)}\n")
        f.write(f"**Defense-Focused (50+):** {len(defense_focused_investors)}\n\n")
        
        for i, inv in enumerate(top_investors, 1):
            f.write(f"## {i}. {inv['name']} (Score: {inv['score']})\n\n")
            f.write(f"**Region:** {inv.get('region', 'Unknown')}\n\n")
            f.write(f"**Focus:** {inv.get('focus', 'Unknown')}\n\n")
            f.write(f"**Stage:** {inv.get('stage', 'Unknown')}\n\n")
            f.write(f"**URL:** {inv['url']}\n\n")
            f.write(f"**Source:** {inv.get('source', 'unknown')}\n\n")
            f.write("---\n\n")
    
    processing_time = time.time() - start_time
    
    # Generate report
    print("\n" + "=" * 60)
    print("📊 RESULTS SUMMARY")
    print("=" * 60)
    
    report_lines = [
        "🛡️ **Defense Sector Report (Scrapling-Enhanced)**\n",
        "## Companies (US/UK/EU)",
        f"- Identified: **{len(scored_companies)}**",
        f"- High priority (70+): **{len(high_priority_companies)}**",
        f"- Top 3:",
    ]
    
    for c in top_companies[:3]:
        report_lines.append(f"  • {c['name']} - {c.get('sector', 'N/A')} - Score: {c['score']}")
    
    report_lines.extend([
        "",
        "## Investors (Asia/India)",
        f"- PE/VC funds: **{len(scored_investors)}**",
        f"- Defense-focused: **{len(defense_focused_investors)}**",
        f"- Top 3:",
    ])
    
    for i in top_investors[:3]:
        report_lines.append(f"  • {i['name']} - {i.get('region', 'N/A')} - {i.get('focus', 'N/A')[:30]}")
    
    report_lines.extend([
        "",
        "🔍 **Data Source:**",
        f"- Scrapling Used: {'✅ Yes' if scrapling_used else '❌ No'}",
        f"- Scrapling Results: {scrapling_results}",
        f"- Traditional API Results: {api_results}",
        f"- Database Results: {len(DEFENSE_COMPANIES)} companies, {len(ASIA_INVESTORS)} investors",
        f"- Processing Time: {processing_time:.2f} seconds",
    ])
    
    report = "\n".join(report_lines)
    print(report)
    
    # Return structured data
    result = {
        'companies_total': len(scored_companies),
        'companies_high_priority': len(high_priority_companies),
        'top_companies': [
            {'name': c['name'], 'score': c['score'], 'sector': c.get('sector', 'N/A')}
            for c in top_companies[:3]
        ],
        'investors_total': len(scored_investors),
        'investors_defense_focused': len(defense_focused_investors),
        'top_investors': [
            {'name': i['name'], 'score': i['score'], 'region': i.get('region', 'N/A')}
            for i in top_investors[:3]
        ],
        'scrapling_used': scrapling_used,
        'scrapling_results': scrapling_results,
        'api_results': api_results,
        'processing_time': round(processing_time, 2),
        'company_file': str(company_file),
        'investor_file': str(investor_file),
        'report': report
    }
    
    print(f"\n📁 Files saved:")
    print(f"   - {company_file}")
    print(f"   - {investor_file}")
    
    return result

if __name__ == "__main__":
    asyncio.run(main())
