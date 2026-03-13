#!/usr/bin/env python3
"""
Defense Sector Lead Generation - Scrapling-First Approach
Runs daily search for defense companies and PE/VC funds
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add scrapling integration path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# Track timing
start_time = datetime.now()
scrapling_used = False
scrapling_results = 0
api_results = 0

async def try_scrapling():
    """Try Scrapling integration first."""
    global scrapling_used, scrapling_results
    
    try:
        from cron_integration import ScraplingCronIntegration
        
        print("🔧 Initializing Scrapling with stealth mode...")
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if success:
            print("✅ Scrapling initialized successfully")
            scrapling_used = True
            
            # Search for defense companies
            search_terms = [
                "defense technology companies US UK EU",
                "cybersecurity defense contractors",
                "counter-drone C-UAS systems",
                "space defense technology satellites",
                "military AI machine learning"
            ]
            
            companies = await scrapling.scrape_defense_companies(search_terms)
            scrapling_results = len(companies)
            
            return {
                "companies": companies,
                "investors": []  # Scrapling doesn't have investor search yet
            }
        else:
            print("⚠️ Scrapling initialization failed")
            return None
            
    except ImportError as e:
        print(f"⚠️ Scrapling not available: {e}")
        return None
    except Exception as e:
        print(f"❌ Scrapling error: {e}")
        return None

async def fallback_to_tavily():
    """Fall back to Tavily API if Scrapling fails."""
    global api_results
    
    print("\n📡 Falling back to Tavily API...")
    
    try:
        import aiohttp
        
        api_key = "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"
        
        # Search for defense companies
        company_queries = [
            "defense technology companies Series A B C funding US UK EU 2025 2026",
            "cybersecurity defense contractors startups US UK Europe",
            "counter-drone C-UAS anti-drone systems companies investment",
            "space defense satellite technology startups Series A-C",
            "military AI machine learning defense tech companies"
        ]
        
        # Search for PE/VC funds
        investor_queries = [
            "private equity defense technology investments India Singapore",
            "venture capital drone aerospace Asia investments",
            "PE fund defense autonomous systems Japan Korea",
            "defense tech investors Southeast Asia Middle East",
            "aerospace drone technology VC funds Taiwan India"
        ]
        
        companies = []
        investors = []
        
        async with aiohttp.ClientSession() as session:
            # Search for companies
            for query in company_queries:
                try:
                    url = "https://api.tavily.com/search"
                    payload = {
                        "api_key": api_key,
                        "query": query,
                        "search_depth": "advanced",
                        "max_results": 10
                    }
                    
                    async with session.post(url, json=payload) as response:
                        if response.status == 200:
                            data = await response.json()
                            results = data.get("results", [])
                            
                            for result in results:
                                company = {
                                    "name": result.get("title", "Unknown"),
                                    "url": result.get("url", ""),
                                    "description": result.get("content", ""),
                                    "sector": classify_defense_sector(result.get("content", "")),
                                    "source": "Tavily API",
                                    "score": score_defense_company(result)
                                }
                                companies.append(company)
                                api_results += 1
                                
                except Exception as e:
                    print(f"Error in Tavily query: {e}")
            
            # Search for investors
            for query in investor_queries:
                try:
                    url = "https://api.tavily.com/search"
                    payload = {
                        "api_key": api_key,
                        "query": query,
                        "search_depth": "advanced",
                        "max_results": 8
                    }
                    
                    async with session.post(url, json=payload) as response:
                        if response.status == 200:
                            data = await response.json()
                            results = data.get("results", [])
                            
                            for result in results:
                                investor = {
                                    "name": result.get("title", "Unknown"),
                                    "url": result.get("url", ""),
                                    "description": result.get("content", ""),
                                    "region": extract_region(result.get("content", "")),
                                    "focus": extract_focus(result.get("content", "")),
                                    "source": "Tavily API",
                                    "score": score_investor(result)
                                }
                                investors.append(investor)
                                api_results += 1
                                
                except Exception as e:
                    print(f"Error in Tavily investor query: {e}")
        
        print(f"✅ Tavily found {len(companies)} companies and {len(investors)} investors")
        return {
            "companies": companies,
            "investors": investors
        }
        
    except Exception as e:
        print(f"❌ Tavily error: {e}")
        return None

def classify_defense_sector(content):
    """Classify defense sector from content."""
    content_lower = content.lower()
    
    if "cyber" in content_lower or "cybersecurity" in content_lower:
        return "Cybersecurity"
    elif "drone" in content_lower or "uas" in content_lower or "uav" in content_lower:
        return "Counter-Drone (C-UAS)"
    elif "space" in content_lower or "satellite" in content_lower:
        return "Space-Based Defense"
    elif "ai" in content_lower or "machine learning" in content_lower:
        return "AI & Machine Learning"
    elif "data" in content_lower or "analytics" in content_lower or "isr" in content_lower:
        return "Defense Data Analytics"
    else:
        return "Defense Technology"

def extract_region(content):
    """Extract region from content."""
    regions = {
        "India": ["india", "indian"],
        "Singapore": ["singapore"],
        "Japan": ["japan", "japanese"],
        "South Korea": ["south korea", "korea", "korean"],
        "Taiwan": ["taiwan", "taiwanese"],
        "Southeast Asia": ["southeast asia", "asean", "vietnam", "thailand", "indonesia", "malaysia"],
        "Middle East": ["middle east", "uae", "saudi", "israel", "qatar"]
    }
    
    content_lower = content.lower()
    for region, keywords in regions.items():
        if any(keyword in content_lower for keyword in keywords):
            return region
    
    return "Asia/India"

def extract_focus(content):
    """Extract investment focus from content."""
    content_lower = content.lower()
    
    focus_areas = []
    if "defense" in content_lower:
        focus_areas.append("Defense Tech")
    if "drone" in content_lower or "uav" in content_lower:
        focus_areas.append("Drones/UAV")
    if "aerospace" in content_lower:
        focus_areas.append("Aerospace")
    if "autonomous" in content_lower:
        focus_areas.append("Autonomous Systems")
    if "security" in content_lower:
        focus_areas.append("Security")
    
    return ", ".join(focus_areas) if focus_areas else "General Technology"

def score_defense_company(result):
    """Score defense company 0-100."""
    score = 0
    content = result.get("content", "").lower()
    title = result.get("title", "").lower()
    
    # Sector fit (0-30)
    defense_keywords = ["defense", "military", "cyber", "drone", "space", "ai", "autonomous"]
    keyword_matches = sum(1 for kw in defense_keywords if kw in content or kw in title)
    score += min(keyword_matches * 5, 30)
    
    # Stage fit (0-20)
    if any(term in content for term in ["series a", "series b", "series c", "funding", "raised"]):
        score += 20
    elif any(term in content for term in ["startup", "early-stage", "growth"]):
        score += 15
    
    # Technical depth (0-20)
    tech_keywords = ["technology", "platform", "system", "software", "ai", "autonomous", "sensor"]
    tech_matches = sum(1 for kw in tech_keywords if kw in content)
    score += min(tech_matches * 4, 20)
    
    # Region match (0-10)
    if any(region in content for region in ["us", "uk", "europe", "united states", "britain"]):
        score += 10
    elif any(region in content for region in ["north america", "nato"]):
        score += 7
    
    # Integration potential (0-20)
    if any(term in content for term in ["government", "contract", "dod", "ministry", "defense"]):
        score += 20
    elif any(term in content for term in ["enterprise", "commercial", "partners"]):
        score += 10
    
    return min(score, 100)

def score_investor(result):
    """Score PE/VC investor 0-100."""
    score = 0
    content = result.get("content", "").lower()
    title = result.get("title", "").lower()
    
    # Defense/drone focus (0-40)
    if any(term in content for term in ["defense", "military", "aerospace"]):
        score += 20
    if any(term in content for term in ["drone", "uav", "autonomous"]):
        score += 20
    
    # Region match (0-20)
    regions = ["india", "singapore", "japan", "korea", "taiwan", "southeast asia", "middle east"]
    if any(region in content for region in regions):
        score += 20
    
    # Portfolio fit (0-20)
    if any(term in content for term in ["portfolio", "investment", "funded", "backed"]):
        score += 20
    
    # Fund size/stage (0-20)
    if any(term in content for term in ["series a", "series b", "growth", "venture"]):
        score += 15
    if any(term in content for term in ["private equity", "pe fund", "fund size"]):
        score += 5
    
    return min(score, 100)

def save_results(data, output_dir):
    """Save results to markdown files."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Save companies
    companies_file = output_dir / f"daily-companies-{today}.md"
    companies = data.get("companies", [])
    
    # Remove duplicates and sort by score
    seen = set()
    unique_companies = []
    for company in companies:
        name = company.get("name", "")
        if name not in seen and name != "Unknown":
            seen.add(name)
            unique_companies.append(company)
    
    unique_companies.sort(key=lambda x: x.get("score", 0), reverse=True)
    
    with open(companies_file, "w") as f:
        f.write(f"# Defense Companies - {today}\n\n")
        f.write(f"**Total Identified:** {len(unique_companies)}\n")
        high_priority = [c for c in unique_companies if c.get("score", 0) >= 70]
        f.write(f"**High Priority (70+):** {len(high_priority)}\n\n")
        f.write("---\n\n")
        
        for i, company in enumerate(unique_companies[:15], 1):
            score = company.get("score", 0)
            priority = "🔴 HIGH" if score >= 70 else "🟡 MEDIUM" if score >= 50 else "🟢 LOW"
            
            f.write(f"## {i}. {company.get('name', 'Unknown')}\n\n")
            f.write(f"**Score:** {score}/100 | **Priority:** {priority}\n\n")
            f.write(f"**Sector:** {company.get('sector', 'N/A')}\n")
            f.write(f"**Source:** {company.get('source', 'N/A')}\n")
            f.write(f"**URL:** {company.get('url', 'N/A')}\n\n")
            f.write(f"**Description:**\n{company.get('description', 'No description available')[:300]}...\n\n")
            f.write("---\n\n")
    
    # Save investors
    investors_file = output_dir / f"daily-investors-{today}.md"
    investors = data.get("investors", [])
    
    # Remove duplicates and sort by score
    seen = set()
    unique_investors = []
    for investor in investors:
        name = investor.get("name", "")
        if name not in seen and name != "Unknown":
            seen.add(name)
            unique_investors.append(investor)
    
    unique_investors.sort(key=lambda x: x.get("score", 0), reverse=True)
    
    with open(investors_file, "w") as f:
        f.write(f"# Defense Investors (Asia/India) - {today}\n\n")
        f.write(f"**Total Funds:** {len(unique_investors)}\n")
        defense_focused = [i for i in unique_investors if "defense" in i.get("focus", "").lower()]
        f.write(f"**Defense-Focused:** {len(defense_focused)}\n\n")
        f.write("---\n\n")
        
        for i, investor in enumerate(unique_investors[:10], 1):
            score = investor.get("score", 0)
            priority = "🔴 HIGH" if score >= 70 else "🟡 MEDIUM" if score >= 50 else "🟢 LOW"
            
            f.write(f"## {i}. {investor.get('name', 'Unknown')}\n\n")
            f.write(f"**Score:** {score}/100 | **Priority:** {priority}\n\n")
            f.write(f"**Region:** {investor.get('region', 'N/A')}\n")
            f.write(f"**Focus:** {investor.get('focus', 'N/A')}\n")
            f.write(f"**Source:** {investor.get('source', 'N/A')}\n")
            f.write(f"**URL:** {investor.get('url', 'N/A')}\n\n")
            f.write(f"**Description:**\n{investor.get('description', 'No description available')[:300]}...\n\n")
            f.write("---\n\n")
    
    return companies_file, investors_file, len(unique_companies), len(unique_investors)

async def main():
    """Main execution."""
    print("🛡️ Defense Sector Lead Generation - Scrapling-First")
    print("=" * 60)
    
    # Try Scrapling first
    data = await try_scrapling()
    
    # Fall back to Tavily if Scrapling failed or returned no results
    if not data or (len(data.get("companies", [])) == 0 and len(data.get("investors", [])) == 0):
        data = await fallback_to_tavily()
    
    if not data:
        print("❌ All data sources failed")
        return
    
    # Create output directory
    output_dir = Path("/Users/cubiczan/.openclaw/workspace/defense-leads")
    output_dir.mkdir(exist_ok=True)
    
    # Save results
    companies_file, investors_file, company_count, investor_count = save_results(data, output_dir)
    
    # Calculate processing time
    end_time = datetime.now()
    processing_time = (end_time - start_time).total_seconds()
    
    # Generate report
    high_priority_companies = [c for c in data.get("companies", []) if c.get("score", 0) >= 70]
    defense_investors = [i for i in data.get("investors", []) if "defense" in i.get("focus", "").lower()]
    
    top_companies = sorted(data.get("companies", []), key=lambda x: x.get("score", 0), reverse=True)[:3]
    top_investors = sorted(data.get("investors", []), key=lambda x: x.get("score", 0), reverse=True)[:3]
    
    report = f"""🛡️ **Defense Sector Report (Scrapling-Enhanced)**

## Companies (US/UK/EU)
- Identified: {company_count}
- High priority (70+): {len(high_priority_companies)}
- Top 3:
{chr(10).join([f"  {i+1}. {c.get('name', 'Unknown')} - {c.get('sector', 'N/A')} - Score: {c.get('score', 0)}" for i, c in enumerate(top_companies)])}

## Investors (Asia/India)
- PE/VC funds: {investor_count}
- Defense-focused: {len(defense_investors)}
- Top 3:
{chr(10).join([f"  {i+1}. {i_f.get('name', 'Unknown')} - {i_f.get('region', 'N/A')} - {i_f.get('focus', 'N/A')}" for i, i_f in enumerate(top_investors)])}

🔍 **Data Source:**
- Scrapling Used: {'✅ Yes' if scrapling_used else '❌ No'}
- Scrapling Results: {scrapling_results}
- Traditional API Results: {api_results}
- Processing Time: {processing_time:.1f} seconds

📁 **Files Saved:**
- Companies: `{companies_file.name}`
- Investors: `{investors_file.name}`"""
    
    print("\n" + report)
    
    # Save report for Discord
    report_file = output_dir / f"report-{datetime.now().strftime('%Y-%m-%d')}.txt"
    with open(report_file, "w") as f:
        f.write(report)
    
    print(f"\n✅ Report saved to: {report_file}")

if __name__ == "__main__":
    asyncio.run(main())
