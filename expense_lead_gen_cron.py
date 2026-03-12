#!/usr/bin/env python3
"""
Expense Reduction Lead Generation Cron Job
Scrapling-First Approach with API Fallbacks
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any

# Add Scrapling integration to path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# API Keys
TAVILY_API_KEY = "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"
BRAVE_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"

class ExpenseLeadGenerator:
    def __init__(self):
        self.scrapling_used = False
        self.scrapling_results = 0
        self.api_results = 0
        self.start_time = datetime.now()
        self.leads = []
        
    async def try_scrapling(self, search_queries: List[str], limit: int = 20) -> List[Dict[str, Any]]:
        """Try Scrapling integration first."""
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
                    self.scrapling_used = True
                    self.scrapling_results = len(leads)
                    print(f"✅ Scrapling found {len(leads)} leads")
                    return leads
                else:
                    print("⚠️ Scrapling returned no results, falling back to APIs")
                    return []
            else:
                print("⚠️ Scrapling initialization failed")
                return []
                
        except ImportError as e:
            print(f"⚠️ Scrapling not available: {e}")
            return []
        except Exception as e:
            print(f"❌ Scrapling error: {e}")
            return []
    
    async def search_with_tavily(self, query: str) -> List[Dict[str, Any]]:
        """Search using Tavily API."""
        import aiohttp
        
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "max_results": 10,
            "include_domains": [],
            "exclude_domains": ["linkedin.com", "facebook.com", "twitter.com"]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("results", [])
                    else:
                        print(f"⚠️ Tavily API error: {response.status}")
                        return []
        except Exception as e:
            print(f"❌ Tavily error: {e}")
            return []
    
    async def search_with_brave(self, query: str) -> List[Dict[str, Any]]:
        """Search using Brave Search API."""
        import aiohttp
        
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": BRAVE_API_KEY
        }
        params = {
            "q": query,
            "count": 10
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("web", {}).get("results", [])
                    else:
                        print(f"⚠️ Brave API error: {response.status}")
                        return []
        except Exception as e:
            print(f"❌ Brave error: {e}")
            return []
    
    def extract_company_from_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract company data from search result."""
        # Extract domain
        url = result.get("url", "")
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc.replace("www.", "")
        company_name = domain.split(".")[0].title()
        
        # Estimate size based on search result
        title = result.get("title", "").lower()
        description = result.get("description", "").lower()
        text = title + " " + description
        
        # Estimate employees
        if any(x in text for x in ["enterprise", "global", "fortune", "fortune 500"]):
            estimated_employees = 500
        elif any(x in text for x in ["inc. 5000", "fast-growing", "rapidly expanding"]):
            estimated_employees = 150
        else:
            estimated_employees = 50
        
        # Classify industry
        industry_keywords = {
            "Technology": ["software", "saas", "tech", "api", "cloud", "platform", "digital"],
            "Manufacturing": ["manufacturing", "industrial", "production", "factory", "machinery"],
            "Healthcare": ["healthcare", "medical", "health", "hospital", "clinic", "pharma"],
            "Professional Services": ["consulting", "services", "agency", "advisory", "solutions"],
            "Financial Services": ["finance", "banking", "investment", "insurance", "fintech"],
            "Retail": ["retail", "ecommerce", "e-commerce", "store", "shop"]
        }
        
        industry = "Other"
        for ind, keywords in industry_keywords.items():
            if any(keyword in text for keyword in keywords):
                industry = ind
                break
        
        # Estimate OPEX
        avg_opex_per_employee = 11500
        estimated_opex = estimated_employees * avg_opex_per_employee
        min_savings = estimated_opex * 0.15
        max_savings = estimated_opex * 0.30
        
        # Calculate lead score
        score = 0
        if estimated_employees >= 200:
            score += 25
        elif estimated_employees >= 100:
            score += 20
        elif estimated_employees >= 50:
            score += 15
        elif estimated_employees >= 20:
            score += 10
        
        high_value_industries = ["Technology", "Healthcare", "Financial Services", "Manufacturing"]
        if industry in high_value_industries:
            score += 25
        elif industry != "Other":
            score += 15
        
        # Add points for having contact info
        if "contact" in text or "about" in text:
            score += 15
        
        return {
            "company_name": company_name,
            "url": url,
            "domain": domain,
            "industry": industry,
            "estimated_employees": estimated_employees,
            "estimated_opex": f"${estimated_opex:,.0f}",
            "potential_savings_range": f"${min_savings:,.0f} - ${max_savings:,.0f}",
            "average_potential_savings": f"${(min_savings + max_savings) / 2:,.0f}",
            "lead_score": min(score, 100),
            "priority": "High" if score >= 70 else "Medium" if score >= 50 else "Low",
            "source": result.get("source", "API"),
            "title": result.get("title", ""),
            "description": result.get("description", "")[:200]
        }
    
    async def generate_leads_with_apis(self, search_queries: List[str], limit: int = 20) -> List[Dict[str, Any]]:
        """Generate leads using Tavily and Brave APIs."""
        print("🔄 Using traditional APIs for lead generation...")
        
        all_leads = []
        seen_domains = set()
        
        for query in search_queries:
            if len(all_leads) >= limit:
                break
            
            print(f"🔍 Searching: {query}")
            
            # Try Tavily first
            results = await self.search_with_tavily(query)
            
            # If Tavily fails, try Brave
            if not results:
                print("⚠️ Tavily failed, trying Brave Search...")
                results = await self.search_with_brave(query)
            
            # Process results
            for result in results:
                if len(all_leads) >= limit:
                    break
                
                url = result.get("url", "")
                from urllib.parse import urlparse
                domain = urlparse(url).netloc
                
                # Skip duplicates and low-quality results
                if domain in seen_domains:
                    continue
                if any(x in domain for x in ["linkedin", "facebook", "twitter", "youtube", "wikipedia"]):
                    continue
                
                lead = self.extract_company_from_result(result)
                
                if lead["lead_score"] >= 30:  # Only include qualified leads
                    all_leads.append(lead)
                    seen_domains.add(domain)
                    print(f"  ✅ {lead['company_name']} (Score: {lead['lead_score']}, Priority: {lead['priority']})")
        
        self.api_results = len(all_leads)
        return all_leads
    
    async def run(self):
        """Main execution."""
        print("="*60)
        print("EXPENSE REDUCTION LEAD GENERATION - SCRAPLING-FIRST")
        print("="*60)
        print(f"Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        search_queries = [
            "growing manufacturing companies 50-200 employees",
            "technology companies series B funding 20-100 employees",
            "healthcare companies expansion 30-150 employees",
            "professional services firms growth 25-75 employees",
            "financial services companies scaling 40-120 employees",
            "SaaS companies rapid growth 20-500 employees",
            "mid-size enterprises high operating expenses",
            "companies with multiple software subscriptions",
            "businesses with logistics and vendor spend"
        ]
        
        # Step 1: Try Scrapling
        leads = await self.try_scrapling(search_queries, limit=20)
        
        # Step 2: Fall back to APIs if needed
        if not leads or len(leads) < 15:
            api_leads = await self.generate_leads_with_apis(search_queries, limit=20)
            leads.extend(api_leads)
            leads = leads[:20]  # Cap at 20
        
        self.leads = leads
        
        # Calculate processing time
        processing_time = (datetime.now() - self.start_time).total_seconds()
        
        print()
        print("="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Total Leads Generated: {len(leads)}")
        print(f"Scrapling Used: {'✅ Yes' if self.scrapling_used else '❌ No'}")
        print(f"Scrapling Results: {self.scrapling_results}")
        print(f"API Results: {self.api_results}")
        print(f"Processing Time: {processing_time:.2f} seconds")
        print()
        
        # Save results
        self.save_results(leads, processing_time)
        
        # Generate Discord report
        discord_report = self.generate_discord_report(leads, processing_time)
        
        return leads, discord_report
    
    def save_results(self, leads: List[Dict[str, Any]], processing_time: float):
        """Save results to files."""
        import os
        
        # Create directory if needed
        os.makedirs("/Users/cubiczan/.openclaw/workspace/expense-leads", exist_ok=True)
        
        # Save daily leads
        today = datetime.now().strftime("%Y-%m-%d")
        daily_file = f"/Users/cubiczan/.openclaw/workspace/expense-leads/daily-leads-{today}.md"
        
        with open(daily_file, "w") as f:
            f.write(f"# Expense Reduction Leads - {today}\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Leads: {len(leads)}\n")
            f.write(f"Processing Time: {processing_time:.2f}s\n\n")
            
            # Sort by lead score
            sorted_leads = sorted(leads, key=lambda x: x["lead_score"], reverse=True)
            
            for i, lead in enumerate(sorted_leads, 1):
                f.write(f"## {i}. {lead['company_name']}\n")
                f.write(f"- **URL:** {lead['url']}\n")
                f.write(f"- **Industry:** {lead['industry']}\n")
                f.write(f"- **Estimated Employees:** {lead['estimated_employees']}\n")
                f.write(f"- **Estimated OPEX:** {lead['estimated_opex']}\n")
                f.write(f"- **Potential Savings:** {lead['potential_savings_range']}\n")
                f.write(f"- **Lead Score:** {lead['lead_score']}/100\n")
                f.write(f"- **Priority:** {lead['priority']}\n")
                f.write(f"- **Source:** {lead.get('source', 'API')}\n")
                if lead.get('description'):
                    f.write(f"- **Description:** {lead['description']}\n")
                f.write("\n")
        
        print(f"✅ Saved daily leads to: {daily_file}")
        
        # Update pipeline
        pipeline_file = "/Users/cubiczan/.openclaw/workspace/expense-leads/pipeline.md"
        
        # Read existing pipeline or create new
        existing_content = ""
        if os.path.exists(pipeline_file):
            with open(pipeline_file, "r") as f:
                existing_content = f.read()
        
        # Prepend new leads
        with open(pipeline_file, "w") as f:
            f.write(f"# Expense Reduction Lead Pipeline\n\n")
            f.write(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Leads Today: {len(leads)}\n\n")
            
            # Summary stats
            high_priority = sum(1 for l in leads if l["priority"] == "High")
            medium_priority = sum(1 for l in leads if l["priority"] == "Medium")
            
            f.write(f"## Today's Summary\n")
            f.write(f"- High Priority: {high_priority}\n")
            f.write(f"- Medium Priority: {medium_priority}\n")
            f.write(f"- Low Priority: {len(leads) - high_priority - medium_priority}\n\n")
            
            # Top leads
            f.write(f"## Top Leads Today\n\n")
            top_leads = sorted(leads, key=lambda x: x["lead_score"], reverse=True)[:5]
            for lead in top_leads:
                f.write(f"- **{lead['company_name']}** ({lead['industry']}) - Score: {lead['lead_score']} - {lead['potential_savings_range']}\n")
            
            f.write("\n---\n\n")
            
            # Keep last 7 days of existing content
            if existing_content:
                lines = existing_content.split("\n")
                # Keep header and recent entries
                f.write("## Previous Entries\n\n")
                f.write("\n".join(lines[:100]))  # Keep first 100 lines
        
        print(f"✅ Updated pipeline: {pipeline_file}")
    
    def generate_discord_report(self, leads: List[Dict[str, Any]], processing_time: float) -> str:
        """Generate Discord summary report."""
        if not leads:
            return "❌ No leads generated today"
        
        # Calculate stats
        high_priority = sum(1 for l in leads if l["priority"] == "High")
        medium_priority = sum(1 for l in leads if l["priority"] == "Medium")
        low_priority = len(leads) - high_priority - medium_priority
        
        # Calculate total potential savings
        total_min_savings = 0
        total_max_savings = 0
        
        for lead in leads:
            savings_range = lead.get("potential_savings_range", "$0 - $0")
            # Parse savings range
            import re
            matches = re.findall(r'\$([\d,]+)', savings_range)
            if len(matches) >= 2:
                min_s = int(matches[0].replace(",", ""))
                max_s = int(matches[1].replace(",", ""))
                total_min_savings += min_s
                total_max_savings += max_s
        
        # Get top 3 leads
        top_leads = sorted(leads, key=lambda x: x["lead_score"], reverse=True)[:3]
        
        report = f"""📊 **Expense Reduction Lead Generation - Daily Report**

**Summary:**
• Total Leads Generated: **{len(leads)}**
• High Priority: **{high_priority}** 🔥
• Medium Priority: **{medium_priority}**
• Low Priority: **{low_priority}**

**Potential Impact:**
• Total Potential Savings: **${total_min_savings:,} - ${total_max_savings:,}**
• Average Savings per Lead: **${(total_min_savings + total_max_savings) // 2 // len(leads):,}**

**Top 3 Leads Today:**

"""
        
        for i, lead in enumerate(top_leads, 1):
            report += f"**{i}. {lead['company_name']}**\n"
            report += f"   • Industry: {lead['industry']}\n"
            report += f"   • Size: ~{lead['estimated_employees']} employees\n"
            report += f"   • Potential Savings: {lead['potential_savings_range']}\n"
            report += f"   • Lead Score: {lead['lead_score']}/100\n"
            report += f"   • Priority: {lead['priority']}\n\n"
        
        report += f"""**🔍 Data Source Report:**
• Scrapling Used: {'✅ Yes' if self.scrapling_used else '❌ No'}
• Scrapling Results: {self.scrapling_results}
• Traditional API Results: {self.api_results}
• Total Processing Time: {processing_time:.2f} seconds

---
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"""
        
        return report


async def main():
    generator = ExpenseLeadGenerator()
    leads, report = await generator.run()
    
    print("\n" + "="*60)
    print("DISCORD REPORT")
    print("="*60)
    print(report)
    
    return report


if __name__ == "__main__":
    report = asyncio.run(main())
