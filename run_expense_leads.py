#!/usr/bin/env python3
"""
Expense Reduction Lead Generation - Scrapling-First Approach
Generates 15-20 qualified leads daily using Scrapling integration
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Add Scrapling integration to path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# API Keys
TAVILY_API_KEY = "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"
BRAVE_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"

# Track data sources
data_source_report = {
    "scrapling_used": False,
    "scrapling_results": 0,
    "tavily_results": 0,
    "brave_results": 0,
    "start_time": datetime.now()
}

async def try_scrapling_leads(search_queries: List[str], limit: int = 20) -> List[Dict[str, Any]]:
    """Try generating leads using Scrapling."""
    global data_source_report
    
    print("🔍 Attempting Scrapling integration...")
    
    try:
        from cron_integration import ScraplingCronIntegration
        
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if success:
            print("✅ Scrapling initialized successfully")
            leads = await scrapling.generate_expense_reduction_leads(
                search_queries=search_queries,
                limit=limit
            )
            
            if leads:
                data_source_report["scrapling_used"] = True
                data_source_report["scrapling_results"] = len(leads)
                print(f"✅ Scrapling generated {len(leads)} leads")
                return leads
            else:
                print("⚠️ Scrapling returned no results, falling back to APIs")
        else:
            print("⚠️ Scrapling initialization failed, falling back to APIs")
    
    except ImportError as e:
        print(f"⚠️ Scrapling not available: {e}")
    except Exception as e:
        print(f"⚠️ Scrapling error: {e}")
    
    return []

async def try_tavily_search(search_queries: List[str], limit: int = 20) -> List[Dict[str, Any]]:
    """Fall back to Tavily API for lead generation."""
    global data_source_report
    
    print("🔍 Using Tavily API as fallback...")
    
    leads = []
    
    try:
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            for query in search_queries:
                if len(leads) >= limit:
                    break
                
                # Tavily search API
                url = "https://api.tavily.com/search"
                payload = {
                    "api_key": TAVILY_API_KEY,
                    "query": query,
                    "search_depth": "advanced",
                    "max_results": 5,
                    "include_domains": ["linkedin.com", "crunchbase.com", "glassdoor.com", "zoominfo.com"]
                }
                
                try:
                    async with session.post(url, json=payload) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            for result in data.get("results", []):
                                if len(leads) >= limit:
                                    break
                                
                                # Extract company info from search result
                                lead = process_search_result(result, query)
                                if lead:
                                    leads.append(lead)
                
                except Exception as e:
                    print(f"⚠️ Tavily query failed: {e}")
                    continue
        
        if leads:
            data_source_report["tavily_results"] = len(leads)
            print(f"✅ Tavily generated {len(leads)} leads")
    
    except Exception as e:
        print(f"⚠️ Tavily API error: {e}")
    
    return leads

async def try_brave_search(search_queries: List[str], limit: int = 20) -> List[Dict[str, Any]]:
    """Fall back to Brave Search API."""
    global data_source_report
    
    print("🔍 Using Brave Search API as second fallback...")
    
    leads = []
    
    try:
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            for query in search_queries:
                if len(leads) >= limit:
                    break
                
                url = "https://api.search.brave.com/res/v1/web/search"
                headers = {
                    "Accept": "application/json",
                    "X-Subscription-Token": BRAVE_API_KEY
                }
                params = {
                    "q": query,
                    "count": 5
                }
                
                try:
                    async with session.get(url, headers=headers, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            for result in data.get("web", {}).get("results", []):
                                if len(leads) >= limit:
                                    break
                                
                                lead = process_search_result(result, query)
                                if lead:
                                    leads.append(lead)
                
                except Exception as e:
                    print(f"⚠️ Brave query failed: {e}")
                    continue
        
        if leads:
            data_source_report["brave_results"] = len(leads)
            print(f"✅ Brave Search generated {len(leads)} leads")
    
    except Exception as e:
        print(f"⚠️ Brave Search API error: {e}")
    
    return leads

def process_search_result(result: Dict[str, Any], query: str) -> Dict[str, Any]:
    """Process search result and create lead entry."""
    
    # Extract basic info
    title = result.get("title", "")
    url = result.get("url", "")
    description = result.get("description", result.get("snippet", ""))
    
    if not title or not url:
        return None
    
    # Estimate company size from query
    if "50-200" in query:
        estimated_employees = 125
    elif "20-100" in query:
        estimated_employees = 60
    elif "30-150" in query:
        estimated_employees = 90
    elif "25-75" in query:
        estimated_employees = 50
    elif "40-120" in query:
        estimated_employees = 80
    else:
        estimated_employees = 100
    
    # Determine industry from query
    if "manufacturing" in query.lower():
        industry = "Manufacturing"
    elif "technology" in query.lower():
        industry = "Technology"
    elif "healthcare" in query.lower():
        industry = "Healthcare"
    elif "professional services" in query.lower():
        industry = "Professional Services"
    elif "financial" in query.lower():
        industry = "Financial Services"
    else:
        industry = "Other"
    
    # Calculate OPEX and savings
    avg_opex_per_employee = 11500
    estimated_opex = estimated_employees * avg_opex_per_employee
    min_savings = int(estimated_opex * 0.15)
    max_savings = int(estimated_opex * 0.30)
    avg_savings = int((min_savings + max_savings) / 2)
    
    # Calculate lead score
    lead_score = calculate_lead_score(estimated_employees, industry, 1, len(description))
    
    return {
        "company_name": title.split(" - ")[0].split(" | ")[0],
        "url": url,
        "industry": industry,
        "estimated_employees": estimated_employees,
        "estimated_opex": f"${estimated_opex:,}",
        "potential_savings_range": f"${min_savings:,} - ${max_savings:,}",
        "average_potential_savings": f"${avg_savings:,}",
        "description": description[:200] if description else "",
        "lead_score": lead_score,
        "priority": "High" if lead_score >= 70 else "Medium" if lead_score >= 50 else "Low",
        "source": "API"
    }

def calculate_lead_score(employees: int, industry: str, email_count: int, content_size: int) -> int:
    """Calculate lead score (0-100)."""
    score = 0
    
    # Company size (25 points)
    if employees >= 200:
        score += 25
    elif employees >= 100:
        score += 20
    elif employees >= 50:
        score += 15
    elif employees >= 20:
        score += 10
    
    # Industry (25 points)
    high_opex_industries = ["Technology", "Healthcare", "Financial Services", "Manufacturing"]
    if industry in high_opex_industries:
        score += 25
    elif industry == "Professional Services":
        score += 15
    
    # Contact availability (25 points) - assume 1 email for API results
    score += 15
    
    # Content quality (25 points)
    if content_size > 200:
        score += 20
    elif content_size > 100:
        score += 15
    else:
        score += 10
    
    return min(score, 100)

def save_leads_to_files(leads: List[Dict[str, Any]]):
    """Save leads to daily file and update pipeline."""
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Create directory
    leads_dir = Path("/Users/cubiczan/.openclaw/workspace/expense-leads")
    leads_dir.mkdir(exist_ok=True)
    
    # Save daily leads
    daily_file = leads_dir / f"daily-leads-{today}.md"
    
    with open(daily_file, "w") as f:
        f.write(f"# Expense Reduction Leads - {today}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Leads:** {len(leads)}\n")
        f.write(f"**High Priority:** {len([l for l in leads if l['priority'] == 'High'])}\n")
        f.write(f"**Medium Priority:** {len([l for l in leads if l['priority'] == 'Medium'])}\n\n")
        
        # Sort by lead score
        leads_sorted = sorted(leads, key=lambda x: x['lead_score'], reverse=True)
        
        for i, lead in enumerate(leads_sorted, 1):
            f.write(f"## {i}. {lead['company_name']}\n\n")
            f.write(f"- **Industry:** {lead['industry']}\n")
            f.write(f"- **Employees:** ~{lead['estimated_employees']}\n")
            f.write(f"- **Estimated OPEX:** {lead['estimated_opex']}\n")
            f.write(f"- **Potential Savings:** {lead['potential_savings_range']}\n")
            f.write(f"- **Lead Score:** {lead['lead_score']}/100\n")
            f.write(f"- **Priority:** {lead['priority']}\n")
            f.write(f"- **Source:** {lead.get('source', 'Unknown')}\n")
            f.write(f"- **URL:** {lead['url']}\n")
            if lead.get('description'):
                f.write(f"- **Description:** {lead['description']}\n")
            f.write("\n---\n\n")
    
    print(f"✅ Saved daily leads to {daily_file}")
    
    # Update pipeline
    pipeline_file = leads_dir / "pipeline.md"
    
    # Read existing pipeline
    existing_content = ""
    if pipeline_file.exists():
        with open(pipeline_file, "r") as f:
            existing_content = f.read()
    
    # Prepend new leads
    with open(pipeline_file, "w") as f:
        f.write(f"# Expense Reduction Lead Pipeline\n\n")
        f.write(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Summary stats
        high_priority = len([l for l in leads if l['priority'] == 'High'])
        medium_priority = len([l for l in leads if l['priority'] == 'Medium'])
        
        total_potential_savings = sum(
            int(l['average_potential_savings'].replace('$', '').replace(',', ''))
            for l in leads
        )
        
        f.write(f"## Current Batch ({today})\n\n")
        f.write(f"- **Total Leads:** {len(leads)}\n")
        f.write(f"- **High Priority:** {high_priority}\n")
        f.write(f"- **Medium Priority:** {medium_priority}\n")
        f.write(f"- **Total Potential Savings:** ${total_potential_savings:,}\n\n")
        
        # Top 3 leads
        f.write(f"### Top 3 Leads Today\n\n")
        for i, lead in enumerate(leads_sorted[:3], 1):
            f.write(f"{i}. **{lead['company_name']}** ({lead['industry']})\n")
            f.write(f"   - Potential Savings: {lead['potential_savings_range']}\n")
            f.write(f"   - Score: {lead['lead_score']}/100\n\n")
        
        # Add existing content
        if existing_content and "# Expense Reduction Lead Pipeline" in existing_content:
            # Find where to append (after header section)
            lines = existing_content.split("\n")
            f.write("\n---\n\n")
            f.write("## Historical Data\n\n")
            # Add historical summary from existing content
            for line in lines:
                if "## Current Batch" in line or "### Top 3" in line:
                    break
            f.write(existing_content)
    
    print(f"✅ Updated pipeline at {pipeline_file}")

def generate_discord_report(leads: List[Dict[str, Any]]) -> str:
    """Generate Discord summary report."""
    
    global data_source_report
    
    high_priority = [l for l in leads if l['priority'] == 'High']
    medium_priority = [l for l in leads if l['priority'] == 'Medium']
    
    total_savings = sum(
        int(l['average_potential_savings'].replace('$', '').replace(',', ''))
        for l in leads
    )
    
    # Calculate processing time
    processing_time = (datetime.now() - data_source_report['start_time']).total_seconds()
    
    # Sort by score for top 3
    leads_sorted = sorted(leads, key=lambda x: x['lead_score'], reverse=True)
    
    report = f"""# 💰 Expense Reduction Lead Generation Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Summary

- **Total Leads:** {len(leads)}
- **High Priority:** {len(high_priority)} 🔥
- **Medium Priority:** {len(medium_priority)}
- **Total Potential Savings:** ${total_savings:,}

## 🔍 Data Source Report

- **Scrapling Used:** {'✅ Yes' if data_source_report['scrapling_used'] else '❌ No'}
- **Scrapling Results:** {data_source_report['scrapling_results']} leads
- **Tavily API Results:** {data_source_report['tavily_results']} leads
- **Brave Search Results:** {data_source_report['brave_results']} leads
- **Total Processing Time:** {processing_time:.1f} seconds

## 🏆 Top 3 Leads Today

"""
    
    for i, lead in enumerate(leads_sorted[:3], 1):
        report += f"""**{i}. {lead['company_name']}**
• Industry: {lead['industry']}
• Employees: ~{lead['estimated_employees']}
• Potential Savings: {lead['potential_savings_range']}
• Score: {lead['lead_score']}/100 ({lead['priority']} Priority)
• URL: {lead['url']}

"""
    
    report += f"""## 📁 Files Updated

- ✅ `/workspace/expense-leads/daily-leads-{datetime.now().strftime('%Y-%m-%d')}.md`
- ✅ `/workspace/expense-leads/pipeline.md`

---
*Powered by Scrapling + OpenClaw* 🐾"""
    
    return report

async def main():
    """Main execution."""
    
    print("=" * 60)
    print("💰 Expense Reduction Lead Generation - Scrapling-First")
    print("=" * 60)
    print()
    
    # Define search queries
    search_queries = [
        "manufacturing companies 50-200 employees",
        "technology companies 20-100 employees",
        "healthcare companies 30-150 employees",
        "professional services firms 25-75 employees",
        "financial services companies 40-120 employees"
    ]
    
    leads = []
    
    # Step 1: Try Scrapling first
    leads = await try_scrapling_leads(search_queries, limit=20)
    
    # Step 2: Fall back to Tavily if Scrapling fails or returns insufficient results
    if len(leads) < 15:
        print(f"\n⚠️ Insufficient leads from Scrapling ({len(leads)}), trying Tavily...")
        tavily_leads = await try_tavily_search(search_queries, limit=20 - len(leads))
        leads.extend(tavily_leads)
    
    # Step 3: Fall back to Brave Search if still insufficient
    if len(leads) < 15:
        print(f"\n⚠️ Still need more leads ({len(leads)}), trying Brave Search...")
        brave_leads = await try_brave_search(search_queries, limit=20 - len(leads))
        leads.extend(brave_leads)
    
    # Remove duplicates based on URL
    seen_urls = set()
    unique_leads = []
    for lead in leads:
        if lead['url'] not in seen_urls:
            seen_urls.add(lead['url'])
            unique_leads.append(lead)
    
    leads = unique_leads[:20]  # Cap at 20 leads
    
    print(f"\n✅ Total unique leads generated: {len(leads)}")
    
    if not leads:
        print("❌ No leads generated from any source!")
        return
    
    # Save to files
    save_leads_to_files(leads)
    
    # Generate Discord report
    discord_report = generate_discord_report(leads)
    
    # Save report for delivery
    report_file = Path("/Users/cubiczan/.openclaw/workspace/expense-leads/discord-report.txt")
    report_file.parent.mkdir(exist_ok=True)
    
    with open(report_file, "w") as f:
        f.write(discord_report)
    
    print(f"\n✅ Discord report saved to {report_file}")
    print("\n" + "=" * 60)
    print(discord_report)
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
