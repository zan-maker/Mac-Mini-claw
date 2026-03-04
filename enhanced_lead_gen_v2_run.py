#!/usr/bin/env python3
"""
Enhanced Lead Gen v2 - Scrapling-First Approach
Cron job execution script
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from pathlib import Path
import aiohttp

# Add scrapling integration to path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# API Keys
SERPER_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"
TAVILY_API_KEY = "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"

class EnhancedLeadGenerator:
    def __init__(self):
        self.scrapling_used = False
        self.scrapling_leads = 0
        self.api_leads = 0
        self.start_time = datetime.now()
        self.leads = []
        
    async def try_scrapling(self):
        """Try Scrapling integration first."""
        print("\n🔍 Attempting Scrapling integration...")
        
        try:
            from cron_integration import ScraplingCronIntegration
            
            scrapling = ScraplingCronIntegration(stealth_mode=True)
            success = await scrapling.initialize()
            
            if success:
                print("✅ Scrapling initialized successfully")
                
                search_queries = [
                    "manufacturing companies 50-200 employees Texas",
                    "technology companies 20-100 employees California",
                    "healthcare companies 30-150 employees Florida",
                    "professional services firms 25-75 employees New York"
                ]
                
                leads = await scrapling.generate_expense_reduction_leads(
                    search_queries=search_queries,
                    limit=30,
                    fast_mode=True
                )
                
                if leads:
                    self.scrapling_used = True
                    self.scrapling_leads = len(leads)
                    self.leads.extend(leads)
                    print(f"✅ Scrapling found {len(leads)} leads")
                    return True
                else:
                    print("⚠️ Scrapling returned no leads")
                    return False
            else:
                print("⚠️ Scrapling initialization failed")
                return False
                
        except ImportError as e:
            print(f"⚠️ Scrapling not available: {e}")
            return False
        except Exception as e:
            print(f"❌ Scrapling error: {e}")
            return False
    
    async def search_tavily(self, query):
        """Search using Tavily API."""
        print(f"\n🔍 Searching Tavily: {query}")
        
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "basic",
            "max_results": 10
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("results", [])
                    else:
                        print(f"⚠️ Tavily error: {response.status}")
                        return []
        except Exception as e:
            print(f"❌ Tavily error: {e}")
            return []
    
    async def search_brave(self, query):
        """Search using Brave Search API (fallback)."""
        print(f"\n🔍 Searching Brave: {query}")
        
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": SERPER_API_KEY}
        payload = {"q": query}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("organic", [])
                    else:
                        print(f"⚠️ Brave error: {response.status}")
                        return []
        except Exception as e:
            print(f"❌ Brave error: {e}")
            return []
    
    async def fallback_to_apis(self):
        """Fall back to Tavily and Brave Search APIs."""
        print("\n🔄 Falling back to traditional APIs...")
        
        queries = [
            "manufacturing companies 50-200 employees Texas",
            "technology companies 20-100 employees California",
            "healthcare companies 30-150 employees Florida"
        ]
        
        for query in queries:
            # Try Tavily first
            results = await self.search_tavily(query)
            
            # If Tavily fails, try Brave
            if not results:
                results = await self.search_brave(query)
            
            # Process results
            for result in results[:8]:  # Limit to 8 per query
                lead = self.process_search_result(result, query)
                if lead:
                    self.leads.append(lead)
                    self.api_leads += 1
        
        print(f"✅ APIs found {self.api_leads} leads")
    
    def process_search_result(self, result, query):
        """Process a search result into a lead."""
        try:
            # Extract basic info
            title = result.get("title", "")
            url = result.get("url", result.get("link", ""))
            snippet = result.get("snippet", result.get("description", ""))
            
            if not title or not url:
                return None
            
            # Extract company name from title
            company_name = title.split(" - ")[0].split(" | ")[0].strip()
            
            # Estimate employee count from query
            if "50-200" in query:
                estimated_employees = 125
            elif "20-100" in query:
                estimated_employees = 60
            elif "30-150" in query:
                estimated_employees = 90
            else:
                estimated_employees = 75
            
            # Estimate OPEX
            avg_opex_per_employee = 11500
            estimated_opex = estimated_employees * avg_opex_per_employee
            
            # Calculate potential savings
            min_savings = estimated_opex * 0.15
            max_savings = estimated_opex * 0.30
            avg_savings = (min_savings + max_savings) / 2
            
            # Classify industry from query
            if "manufacturing" in query.lower():
                industry = "Manufacturing"
            elif "technology" in query.lower():
                industry = "Technology"
            elif "healthcare" in query.lower():
                industry = "Healthcare"
            else:
                industry = "Professional Services"
            
            # Calculate lead score
            lead_score = 50  # Base score
            if 50 <= estimated_employees <= 200:
                lead_score += 25  # Size fit
            if industry in ["Manufacturing", "Technology", "Healthcare"]:
                lead_score += 15  # Industry match
            
            return {
                "company_name": company_name,
                "url": url,
                "industry": industry,
                "estimated_employees": estimated_employees,
                "estimated_opex": f"${estimated_opex:,.0f}",
                "potential_savings_range": f"${min_savings:,.0f} - ${max_savings:,.0f}",
                "average_potential_savings": f"${avg_savings:,.0f}",
                "emails": [],
                "phones": [],
                "lead_score": min(lead_score, 100),
                "priority": "High" if lead_score >= 70 else "Medium" if lead_score >= 50 else "Low",
                "source": "API",
                "snippet": snippet[:200] if snippet else ""
            }
            
        except Exception as e:
            print(f"⚠️ Error processing result: {e}")
            return None
    
    def save_leads(self):
        """Save leads to daily file."""
        if not self.leads:
            print("⚠️ No leads to save")
            return None
        
        # Sort by lead score
        self.leads.sort(key=lambda x: x.get("lead_score", 0), reverse=True)
        
        # Create leads directory
        leads_dir = Path("/Users/cubiczan/.openclaw/workspace/leads")
        leads_dir.mkdir(exist_ok=True)
        
        # Create filename
        today = datetime.now().strftime("%Y-%m-%d")
        filename = leads_dir / f"daily-leads-{today}.md"
        
        # Generate markdown content
        content = f"# Daily Leads - {today}\n\n"
        content += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += f"**Total Leads:** {len(self.leads)}\n"
        content += f"**High Priority (70+):** {sum(1 for l in self.leads if l.get('lead_score', 0) >= 70)}\n\n"
        
        content += "---\n\n"
        
        for i, lead in enumerate(self.leads, 1):
            content += f"## {i}. {lead.get('company_name', 'Unknown')}\n\n"
            content += f"- **Industry:** {lead.get('industry', 'N/A')}\n"
            content += f"- **URL:** {lead.get('url', 'N/A')}\n"
            content += f"- **Estimated Employees:** {lead.get('estimated_employees', 'N/A')}\n"
            content += f"- **Estimated OPEX:** {lead.get('estimated_opex', 'N/A')}\n"
            content += f"- **Potential Savings:** {lead.get('potential_savings_range', 'N/A')}\n"
            content += f"- **Average Savings:** {lead.get('average_potential_savings', 'N/A')}\n"
            content += f"- **Lead Score:** {lead.get('lead_score', 0)}/100\n"
            content += f"- **Priority:** {lead.get('priority', 'Low')}\n"
            content += f"- **Source:** {lead.get('source', 'Unknown')}\n"
            
            if lead.get('emails'):
                content += f"- **Emails:** {', '.join(lead['emails'])}\n"
            if lead.get('phones'):
                content += f"- **Phones:** {', '.join(lead['phones'])}\n"
            if lead.get('snippet'):
                content += f"\n**Snippet:** {lead['snippet']}\n"
            
            content += "\n---\n\n"
        
        # Write file
        with open(filename, 'w') as f:
            f.write(content)
        
        print(f"✅ Saved {len(self.leads)} leads to {filename}")
        return filename
    
    def generate_report(self):
        """Generate summary report."""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        high_priority = sum(1 for l in self.leads if l.get('lead_score', 0) >= 70)
        medium_priority = sum(1 for l in self.leads if 50 <= l.get('lead_score', 0) < 70)
        
        # Get top 3 leads
        top_leads = sorted(self.leads, key=lambda x: x.get('lead_score', 0), reverse=True)[:3]
        
        report = {
            "total_leads": len(self.leads),
            "high_priority": high_priority,
            "medium_priority": medium_priority,
            "scrapling_used": self.scrapling_used,
            "scrapling_leads": self.scrapling_leads,
            "api_leads": self.api_leads,
            "processing_time_seconds": round(elapsed, 2),
            "top_3_leads": [
                {
                    "company": l.get('company_name'),
                    "score": l.get('lead_score'),
                    "savings": l.get('average_potential_savings')
                }
                for l in top_leads
            ]
        }
        
        return report

async def main():
    print("=" * 60)
    print("Enhanced Lead Gen v2 - Scrapling-First")
    print("=" * 60)
    
    generator = EnhancedLeadGenerator()
    
    # Step 1: Try Scrapling
    scrapling_success = await generator.try_scrapling()
    
    # Step 2: Fall back to APIs if needed
    if not scrapling_success or len(generator.leads) < 20:
        await generator.fallback_to_apis()
    
    # Step 3: Save leads
    filename = generator.save_leads()
    
    # Step 4: Generate report
    report = generator.generate_report()
    
    print("\n" + "=" * 60)
    print("SUMMARY REPORT")
    print("=" * 60)
    print(json.dumps(report, indent=2))
    
    # Save report for Discord
    report_file = Path("/Users/cubiczan/.openclaw/workspace/leads/report-latest.json")
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Report saved to {report_file}")
    
    return report

if __name__ == "__main__":
    asyncio.run(main())
