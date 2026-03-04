#!/usr/bin/env python3
"""
Mining Lead Generator - Daily Deal Sourcing
Finds high-grade mining projects, CPC companies, and ASX companies seeking JVs
"""

import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Any

# Configuration
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "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")
OUTPUT_DIR = "/Users/cubiczan/.openclaw/workspace/mining-leads"

# Grade thresholds for "high-grade"
GRADE_THRESHOLDS = {
    "gold": "5 g/t",           # Underground: >5g/t is high-grade
    "copper": "1.5%",          # >1.5% Cu is high-grade
    "silver": "200 g/t",       # >200 g/t Ag is high-grade
    "lithium": "1.2% Li2O",    # Hard rock lithium
    "zinc": "8%",              # Zinc
    "rare_earths": "1.5% TREO" # Total rare earth oxides
}

# Search queries for finding opportunities
SEARCH_QUERIES = {
    "high_grade_projects": [
        "high grade gold discovery 2026 drilling results 10 g/t",
        "copper porphyry high grade 2% drilling results 2026",
        "silver epithermal high grade 300 g/t discovery",
        "lithium spodumene 1.5% Li2O drill results 2026",
        "zinc VMS high grade 10% drilling intercepts",
        "rare earth carbonatite 2% TREO drill results"
    ],
    "cpc_companies": [
        "TSXV CPC capital pool company mining seeking acquisition 2026",
        "Canadian Capital Pool Company mining target qualifying transaction",
        "TSX Venture CPC mining exploration looking for project"
    ],
    "asx_seekers": [
        "ASX mining company cashed up seeking joint venture 2026",
        "ASX junior mining cash runway seeking earn-in partner",
        "Australian mining company farm-out joint venture opportunity",
        "ASX exploration company seeking strategic partner investment"
    ],
    "private_projects": [
        "private mining project seeking joint venture partner",
        "family owned mining property farm-out agreement",
        "private mineral exploration earn-in opportunity"
    ]
}

def search_tavily(query: str, max_results: int = 5) -> List[Dict]:
    """Search using Tavily API"""
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            headers={"Content-Type": "application/json"},
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "search_depth": "advanced",
                "max_results": max_results,
                "include_raw_content": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            print(f"  ⚠️ Tavily error: {response.status_code}")
            return []
    except Exception as e:
        print(f"  ⚠️ Search error: {e}")
        return []

def extract_project_info(result: Dict) -> Dict:
    """Extract project information from search result"""
    content = result.get("content", "")
    title = result.get("title", "")
    url = result.get("url", "")
    
    # Extract commodity
    commodity = "Unknown"
    for c in ["Gold", "Copper", "Silver", "Lithium", "Zinc", "Rare Earth", "Nickel", "Cobalt"]:
        if c.lower() in content.lower() or c.lower() in title.lower():
            commodity = c
            break
    
    # Extract location
    location = "Unknown"
    locations = ["Nevada", "Western Australia", "Queensland", "Ontario", "British Columbia", 
                 "Chile", "Peru", "Mexico", "Quebec", "Yukon", "Arizona", "Africa", "Canada", "USA", "Australia"]
    for loc in locations:
        if loc.lower() in content.lower() or loc.lower() in title.lower():
            location = loc
            break
    
    # Extract grade mentions
    import re
    grade_info = "Not specified"
    
    # Gold grades (g/t)
    gold_match = re.search(r'(\d+\.?\d*)\s*g/t\s*(?:Au|gold)', content, re.IGNORECASE)
    if gold_match:
        grade_info = f"{gold_match.group(1)} g/t Au"
    
    # Copper grades (%)
    copper_match = re.search(r'(\d+\.?\d*)\s*%\s*(?:Cu|copper)', content, re.IGNORECASE)
    if copper_match:
        grade_info = f"{copper_match.group(1)}% Cu"
    
    # Silver grades (g/t)
    silver_match = re.search(r'(\d+)\s*g/t\s*(?:Ag|silver)', content, re.IGNORECASE)
    if silver_match:
        grade_info = f"{silver_match.group(1)} g/t Ag"
    
    # Lithium grades (% Li2O)
    lithium_match = re.search(r'(\d+\.?\d*)\s*%\s*Li2O', content, re.IGNORECASE)
    if lithium_match:
        grade_info = f"{lithium_match.group(1)}% Li2O"
    
    return {
        "title": title,
        "commodity": commodity,
        "location": location,
        "grade": grade_info,
        "source": url,
        "snippet": content[:300] + "..." if len(content) > 300 else content
    }

def extract_company_info(result: Dict, company_type: str) -> Dict:
    """Extract company information from search result"""
    content = result.get("content", "")
    title = result.get("title", "")
    url = result.get("url", "")
    
    # Extract ticker if present
    import re
    ticker = ""
    ticker_match = re.search(r'\(([A-Z]{2,4}\.[A-Z]{1,3})\)', title + " " + content)
    if ticker_match:
        ticker = ticker_match.group(1)
    
    # Extract company name (usually first part of title)
    company_name = title.split(" - ")[0].split(" | ")[0].strip()
    if len(company_name) > 50:
        company_name = company_name[:50]
    
    # Look for cash/runway mentions
    cash_info = "Not specified"
    cash_match = re.search(r'\$?(\d+\.?\d*)\s*[MB]?\s*(?:million|M)\s*(?:cash|CAD|AUD|USD)', content, re.IGNORECASE)
    if cash_match:
        cash_info = f"${cash_match.group(1)}M"
    
    # Look for what they're seeking
    seeking = "JV/Partner"
    if "earn-in" in content.lower():
        seeking = "Earn-in partner"
    elif "strategic" in content.lower():
        seeking = "Strategic investor"
    elif "acquisition" in content.lower():
        seeking = "Acquisition target"
    elif "farm-out" in content.lower():
        seeking = "Farm-out agreement"
    
    return {
        "name": company_name,
        "ticker": ticker,
        "type": company_type,
        "cash": cash_info,
        "seeking": seeking,
        "source": url,
        "snippet": content[:200] + "..." if len(content) > 200 else content
    }

def score_project(project: Dict) -> int:
    """Score a project (0-100)"""
    score = 50  # Base score
    
    # Bonus for high grades
    grade = project.get("grade", "")
    if "g/t Au" in grade:
        try:
            gpt = float(grade.split()[0])
            if gpt >= 10:
                score += 25
            elif gpt >= 5:
                score += 15
            elif gpt >= 3:
                score += 5
        except:
            pass
    elif "% Cu" in grade:
        try:
            pct = float(grade.split()[0])
            if pct >= 2:
                score += 25
            elif pct >= 1:
                score += 15
        except:
            pass
    elif "g/t Ag" in grade:
        try:
            gpt = float(grade.split()[0])
            if gpt >= 300:
                score += 25
            elif gpt >= 200:
                score += 15
        except:
            pass
    
    # Bonus for good jurisdictions
    location = project.get("location", "")
    if location in ["Nevada", "Western Australia", "Quebec", "British Columbia"]:
        score += 10
    
    # Bonus for specific commodities
    commodity = project.get("commodity", "")
    if commodity in ["Gold", "Copper", "Lithium"]:
        score += 5
    
    return min(100, score)

def main():
    print("=" * 70)
    print("⛏️ MINING LEAD GENERATOR - DAILY DEAL SOURCING")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    results = {
        "generated_at": datetime.now().isoformat(),
        "high_grade_projects": [],
        "cpc_companies": [],
        "asx_seekers": [],
        "private_opportunities": []
    }
    
    # 1. Find high-grade projects
    print("🔍 Searching for high-grade projects...")
    projects = []
    seen_titles = set()
    
    for query in SEARCH_QUERIES["high_grade_projects"]:
        print(f"  Query: {query[:50]}...")
        search_results = search_tavily(query, max_results=3)
        
        for result in search_results:
            project = extract_project_info(result)
            if project["title"] not in seen_titles:
                project["score"] = score_project(project)
                projects.append(project)
                seen_titles.add(project["title"])
    
    # Sort by score and take top 10
    projects.sort(key=lambda x: x.get("score", 0), reverse=True)
    results["high_grade_projects"] = projects[:10]
    print(f"  ✅ Found {len(results['high_grade_projects'])} high-grade projects")
    print()
    
    # 2. Find CPC companies
    print("🔍 Searching for CPC companies...")
    cpc_companies = []
    seen_names = set()
    
    for query in SEARCH_QUERIES["cpc_companies"]:
        print(f"  Query: {query[:50]}...")
        search_results = search_tavily(query, max_results=3)
        
        for result in search_results:
            company = extract_company_info(result, "CPC")
            if company["name"] and company["name"] not in seen_names:
                cpc_companies.append(company)
                seen_names.add(company["name"])
    
    results["cpc_companies"] = cpc_companies[:8]
    print(f"  ✅ Found {len(results['cpc_companies'])} CPC companies")
    print()
    
    # 3. Find ASX companies seeking JVs
    print("🔍 Searching for ASX companies seeking JVs...")
    asx_companies = []
    seen_names = set()
    
    for query in SEARCH_QUERIES["asx_seekers"]:
        print(f"  Query: {query[:50]}...")
        search_results = search_tavily(query, max_results=3)
        
        for result in search_results:
            company = extract_company_info(result, "ASX")
            if company["name"] and company["name"] not in seen_names:
                asx_companies.append(company)
                seen_names.add(company["name"])
    
    results["asx_seekers"] = asx_companies[:8]
    print(f"  ✅ Found {len(results['asx_seekers'])} ASX companies")
    print()
    
    # 4. Find private opportunities
    print("🔍 Searching for private JV opportunities...")
    private_opps = []
    seen_titles = set()
    
    for query in SEARCH_QUERIES["private_projects"]:
        print(f"  Query: {query[:50]}...")
        search_results = search_tavily(query, max_results=3)
        
        for result in search_results:
            project = extract_project_info(result)
            project["type"] = "Private"
            if project["title"] not in seen_titles:
                project["score"] = score_project(project)
                private_opps.append(project)
                seen_titles.add(project["title"])
    
    results["private_opportunities"] = private_opps[:5]
    print(f"  ✅ Found {len(results['private_opportunities'])} private opportunities")
    print()
    
    # Save results
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    date_str = datetime.now().strftime('%Y-%m-%d')
    json_file = f"{OUTPUT_DIR}/daily-mining-leads-{date_str}.json"
    md_file = f"{OUTPUT_DIR}/daily-mining-leads-{date_str}.md"
    
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Generate markdown report
    md_content = generate_markdown_report(results)
    with open(md_file, 'w') as f:
        f.write(md_content)
    
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"High-Grade Projects: {len(results['high_grade_projects'])}")
    print(f"CPC Companies: {len(results['cpc_companies'])}")
    print(f"ASX Companies Seeking JVs: {len(results['asx_seekers'])}")
    print(f"Private Opportunities: {len(results['private_opportunities'])}")
    print()
    print(f"📁 Results saved to:")
    print(f"   {json_file}")
    print(f"   {md_file}")
    print("=" * 70)
    
    return results

def generate_markdown_report(results: Dict) -> str:
    """Generate a markdown report"""
    date = datetime.now().strftime('%Y-%m-%d')
    
    md = f"""# Mining Deal Sourcing - {date}

**Generated:** {results['generated_at']}

## 🔥 High-Grade Projects

"""
    
    for i, project in enumerate(results['high_grade_projects'], 1):
        score_emoji = "🔥" if project.get('score', 0) >= 75 else "⭐" if project.get('score', 0) >= 60 else "📍"
        md += f"""### {i}. {project['title'][:60]}
- **Commodity:** {project['commodity']}
- **Grade:** {project['grade']}
- **Location:** {project['location']}
- **Score:** {project.get('score', 'N/A')}
- **Source:** [{project['source'][:50]}...]({project['source']})

"""
    
    md += """## 🇨🇦 CPC Companies (Canadian Juniors)

"""
    
    if results['cpc_companies']:
        for company in results['cpc_companies']:
            md += f"""### {company['name']}
- **Ticker:** {company['ticker'] or 'N/A'}
- **Cash:** {company['cash']}
- **Seeking:** {company['seeking']}
- **Source:** [{company['source'][:40]}...]({company['source']})

"""
    else:
        md += "*No CPC companies found in this search.*\n\n"
    
    md += """## 🇦🇺 ASX Companies Seeking JVs

"""
    
    if results['asx_seekers']:
        for company in results['asx_seekers']:
            md += f"""### {company['name']}
- **Ticker:** {company['ticker'] or 'N/A'}
- **Cash:** {company['cash']}
- **Seeking:** {company['seeking']}
- **Source:** [{company['source'][:40]}...]({company['source']})

"""
    else:
        md += "*No ASX companies found in this search.*\n\n"
    
    md += """## 🤝 Private JV Opportunities

"""
    
    if results['private_opportunities']:
        for project in results['private_opportunities']:
            md += f"""### {project['title'][:50]}
- **Commodity:** {project['commodity']}
- **Location:** {project['location']}
- **Source:** [{project['source'][:40]}...]({project['source']})

"""
    else:
        md += "*No private opportunities found in this search.*\n\n"
    
    md += """---

## Grade Thresholds

| Commodity | High-Grade Threshold |
|-----------|---------------------|
| Gold | >5 g/t (underground) |
| Copper | >1.5% Cu |
| Silver | >200 g/t Ag |
| Lithium | >1.2% Li2O |
| Zinc | >8% Zn |
| Rare Earths | >1.5% TREO |

"""
    
    return md

if __name__ == "__main__":
    main()
