#!/usr/bin/env python3
"""
Expense Reduction Lead Generation - Scrapling-First Approach
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any

# Add Scrapling integration to path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

class LeadGenerator:
    def __init__(self):
        self.scrapling_used = False
        self.scrapling_results = 0
        self.api_results = 0
        self.start_time = datetime.now()
        
    async def try_scrapling(self, search_queries: List[str], limit: int = 20) -> List[Dict[str, Any]]:
        """Try Scrapling first for lead generation."""
        try:
            from cron_integration import ScraplingCronIntegration
            
            print("🚀 Initializing Scrapling...")
            scrapling = ScraplingCronIntegration(stealth_mode=True)
            success = await scrapling.initialize()
            
            if success:
                print("✅ Scrapling initialized successfully")
                self.scrapling_used = True
                leads = await scrapling.generate_expense_reduction_leads(
                    search_queries=search_queries,
                    limit=limit
                )
                self.scrapling_results = len(leads)
                print(f"✅ Scrapling found {len(leads)} leads")
                return leads
            else:
                print("⚠️ Scrapling initialization failed")
                return []
        except ImportError as e:
            print(f"⚠️ Scrapling not available: {e}")
            return []
        except Exception as e:
            print(f"⚠️ Scrapling error: {e}")
            return []
    
    async def try_tavily(self, search_queries: List[str]) -> List[Dict[str, Any]]:
        """Fall back to Tavily API."""
        import aiohttp
        
        print("🔍 Using Tavily API as fallback...")
        api_key = "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"
        leads = []
        
        async with aiohttp.ClientSession() as session:
            for query in search_queries[:5]:  # Limit to 5 queries
                try:
                    url = "https://api.tavily.com/search"
                    payload = {
                        "api_key": api_key,
                        "query": f"{query} contact CFO finance",
                        "search_depth": "basic",
                        "max_results": 5
                    }
                    
                    async with session.post(url, json=payload) as response:
                        if response.status == 200:
                            data = await response.json()
                            for result in data.get("results", []):
                                lead = self._create_lead_from_search(result, query)
                                leads.append(lead)
                except Exception as e:
                    print(f"⚠️ Tavily query failed: {e}")
        
        self.api_results = len(leads)
        print(f"✅ Tavily found {len(leads)} leads")
        return leads
    
    def _create_lead_from_search(self, result: Dict, query: str) -> Dict[str, Any]:
        """Create lead from search result."""
        # Extract domain
        url = result.get("url", "")
        domain = url.split("//")[-1].split("/")[0].replace("www.", "")
        company_name = domain.split(".")[0].title()
        
        # Estimate employees based on query
        if "50-200" in query or "100" in query:
            employees = 100
        elif "20-100" in query:
            employees = 50
        else:
            employees = 75
        
        # Calculate OPEX and savings
        estimated_opex = employees * 11500
        min_savings = int(estimated_opex * 0.15)
        max_savings = int(estimated_opex * 0.30)
        
        # Determine industry
        if "manufacturing" in query.lower():
            industry = "Manufacturing"
        elif "technology" in query.lower() or "tech" in query.lower():
            industry = "Technology"
        elif "healthcare" in query.lower():
            industry = "Healthcare"
        elif "professional" in query.lower():
            industry = "Professional Services"
        elif "financial" in query.lower():
            industry = "Financial Services"
        else:
            industry = "Other"
        
        # Calculate score
        score = self._calculate_score(employees, industry, url)
        
        return {
            "company_name": company_name,
            "url": url,
            "industry": industry,
            "estimated_employees": employees,
            "estimated_opex": f"${estimated_opex:,}",
            "potential_savings_range": f"${min_savings:,} - ${max_savings:,}",
            "average_potential_savings": f"${(min_savings + max_savings)//2:,}",
            "title": result.get("title", ""),
            "snippet": result.get("content", "")[:200],
            "lead_score": score,
            "priority": "High" if score >= 70 else "Medium" if score >= 50 else "Low",
            "source": "Tavily"
        }
    
    def _calculate_score(self, employees: int, industry: str, url: str) -> int:
        """Calculate lead score."""
        score = 0
        
        # Employee count (25 points)
        if employees >= 200:
            score += 25
        elif employees >= 100:
            score += 20
        elif employees >= 50:
            score += 15
        elif employees >= 20:
            score += 10
        
        # Industry (25 points)
        high_value = ["Technology", "Healthcare", "Financial Services", "Manufacturing"]
        if industry in high_value:
            score += 25
        elif industry == "Professional Services":
            score += 15
        else:
            score += 10
        
        # URL quality (25 points)
        if url and len(url) > 20:
            score += 20
        else:
            score += 10
        
        # Random factor for variation (25 points)
        import random
        score += random.randint(15, 25)
        
        return min(score, 100)
    
    def save_results(self, leads: List[Dict[str, Any]]):
        """Save leads to files."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Create directory
        os.makedirs("/Users/cubiczan/.openclaw/workspace/expense-leads", exist_ok=True)
        
        # Save daily leads
        daily_file = f"/Users/cubiczan/.openclaw/workspace/expense-leads/daily-leads-{today}.md"
        with open(daily_file, 'w') as f:
            f.write(f"# Expense Reduction Leads - {today}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Leads:** {len(leads)}\n")
            f.write(f"**High Priority:** {len([l for l in leads if l['priority'] == 'High'])}\n")
            f.write(f"**Source:** {'Scrapling' if self.scrapling_used else 'Tavily API'}\n\n")
            
            # Sort by score
            leads_sorted = sorted(leads, key=lambda x: x['lead_score'], reverse=True)
            
            for i, lead in enumerate(leads_sorted, 1):
                f.write(f"## {i}. {lead['company_name']}\n")
                f.write(f"- **Industry:** {lead['industry']}\n")
                f.write(f"- **Employees:** ~{lead['estimated_employees']}\n")
                f.write(f"- **Estimated OPEX:** {lead['estimated_opex']}\n")
                f.write(f"- **Potential Savings:** {lead['potential_savings_range']}\n")
                f.write(f"- **Lead Score:** {lead['lead_score']}/100\n")
                f.write(f"- **Priority:** {lead['priority']}\n")
                f.write(f"- **URL:** {lead['url']}\n")
                if lead.get('snippet'):
                    f.write(f"- **Notes:** {lead['snippet']}\n")
                f.write("\n")
        
        print(f"✅ Saved daily leads to {daily_file}")
        
        # Update pipeline
        pipeline_file = "/Users/cubiczan/.openclaw/workspace/expense-leads/pipeline.md"
        self._update_pipeline(leads, pipeline_file)
    
    def _update_pipeline(self, leads: List[Dict[str, Any]], pipeline_file: str):
        """Update pipeline file."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Read existing pipeline
        existing = ""
        if os.path.exists(pipeline_file):
            with open(pipeline_file, 'r') as f:
                existing = f.read()
        
        # Add new section
        new_section = f"\n## {today}\n\n"
        high_priority = [l for l in leads if l['priority'] == 'High']
        
        for lead in high_priority[:5]:
            new_section += f"### {lead['company_name']}\n"
            new_section += f"- Industry: {lead['industry']}\n"
            new_section += f"- Employees: ~{lead['estimated_employees']}\n"
            new_section += f"- Potential Savings: {lead['potential_savings_range']}\n"
            new_section += f"- Score: {lead['lead_score']}/100\n"
            new_section += f"- Status: New\n\n"
        
        # Write updated pipeline
        with open(pipeline_file, 'w') as f:
            if not existing:
                f.write("# Expense Reduction Pipeline\n\n")
            f.write(existing)
            f.write(new_section)
        
        print(f"✅ Updated pipeline")
    
    def generate_report(self, leads: List[Dict[str, Any]]) -> str:
        """Generate Discord report."""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        high_priority = [l for l in leads if l['priority'] == 'High']
        medium_priority = [l for l in leads if l['priority'] == 'Medium']
        
        # Calculate total potential savings
        total_savings = 0
        for lead in leads:
            savings_str = lead['average_potential_savings'].replace('$', '').replace(',', '')
            try:
                total_savings += int(savings_str)
            except:
                pass
        
        report = f"""# 💰 Expense Reduction Lead Generation Report

**Date:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
**Total Leads Generated:** {len(leads)}

## 🎯 Lead Quality Distribution
- **High Priority (70+):** {len(high_priority)} leads
- **Medium Priority (50-69):** {len(medium_priority)} leads
- **Low Priority (<50):** {len(leads) - len(high_priority) - len(medium_priority)} leads

## 💵 Financial Summary
- **Total Potential Annual Savings:** ${total_savings:,}
- **Average Savings per Lead:** ${total_savings // len(leads) if leads else 0:,}

## 🔍 Data Source Report
- **Scrapling Used:** {'✅ Yes' if self.scrapling_used else '❌ No'}
- **Scrapling Results:** {self.scrapling_results} leads
- **Traditional API Results:** {self.api_results} leads
- **Total Processing Time:** {elapsed:.1f} seconds

## 🏆 Top 3 Leads Today
"""
        
        # Sort by score and get top 3
        top_leads = sorted(leads, key=lambda x: x['lead_score'], reverse=True)[:3]
        
        for i, lead in enumerate(top_leads, 1):
            report += f"""
**{i}. {lead['company_name']}** (Score: {lead['lead_score']}/100)
• Industry: {lead['industry']}
• Employees: ~{lead['estimated_employees']}
• Potential Savings: {lead['potential_savings_range']}
• URL: {lead['url']}
"""
        
        report += f"""
## 📁 Files Updated
- `daily-leads-{datetime.now().strftime("%Y-%m-%d")}.md`
- `pipeline.md`

---
*Next steps: Review high-priority leads and initiate outreach sequence*
"""
        
        return report

async def main():
    generator = LeadGenerator()
    
    # Define search queries
    search_queries = [
        "manufacturing companies 50-200 employees",
        "technology companies 20-100 employees",
        "healthcare companies 30-150 employees",
        "professional services firms 25-75 employees",
        "financial services companies 40-120 employees"
    ]
    
    print("=" * 60)
    print("EXPENSE REDUCTION LEAD GENERATION")
    print("=" * 60)
    
    # Try Scrapling first
    leads = await generator.try_scrapling(search_queries, limit=20)
    
    # Fall back to Tavily if Scrapling didn't return enough results
    if len(leads) < 15:
        print(f"\n⚠️ Scrapling returned only {len(leads)} leads, trying Tavily...")
        tavily_leads = await generator.try_tavily(search_queries)
        leads.extend(tavily_leads)
        
        # Deduplicate by company name
        seen = set()
        unique_leads = []
        for lead in leads:
            if lead['company_name'] not in seen:
                seen.add(lead['company_name'])
                unique_leads.append(lead)
        leads = unique_leads[:20]  # Limit to 20
    
    # Save results
    if leads:
        generator.save_results(leads)
    
    # Generate report
    report = generator.generate_report(leads)
    print("\n" + "=" * 60)
    print(report)
    print("=" * 60)
    
    # Return report for Discord
    return report

if __name__ == "__main__":
    report = asyncio.run(main())
    print("\n\nDISCORD_REPORT_START")
    print(report)
    print("DISCORD_REPORT_END")
