#!/usr/bin/env python3
"""
Enhanced Lead Gen v2 - Scrapling-First Approach
Generates 20-30 leads quickly with Scrapling, falls back to APIs
"""

import asyncio
import sys
import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import aiohttp

# Add Scrapling integration to path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# Configuration
SERPER_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"
TAVILY_API_KEY = "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"
ZEROBOUNCE_API_KEY = "fd0105c8c98340e0a2b63e2fbe39d7a4"

class EnhancedLeadGen:
    def __init__(self):
        self.scrapling_available = False
        self.scrapling_leads = []
        self.api_leads = []
        self.start_time = datetime.now()
        
    async def try_scrapling(self):
        """Try Scrapling integration first"""
        print("🔍 Attempting Scrapling integration...")
        
        try:
            from cron_integration import ScraplingCronIntegration
            
            scrapling = ScraplingCronIntegration(stealth_mode=True)
            success = await scrapling.initialize()
            
            if success:
                print("✅ Scrapling initialized successfully")
                
                # Search queries for expense reduction leads
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
                    self.scrapling_leads = leads
                    self.scrapling_available = True
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
    
    async def search_tavily(self, query: str) -> List[Dict]:
        """Search using Tavily API"""
        print(f"🔍 Searching Tavily: {query}")
        
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.tavily.com/search"
                payload = {
                    "api_key": TAVILY_API_KEY,
                    "query": query,
                    "search_depth": "basic",
                    "max_results": 10
                }
                
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("results", [])
                    else:
                        print(f"⚠️ Tavily API error: {response.status}")
                        return []
        except Exception as e:
            print(f"❌ Tavily error: {e}")
            return []
    
    async def search_brave(self, query: str) -> List[Dict]:
        """Search using Brave Search API (Serper)"""
        print(f"🔍 Searching Brave/Serper: {query}")
        
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://google.serper.dev/search"
                headers = {"X-API-KEY": SERPER_API_KEY}
                payload = {"q": query}
                
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Extract organic results
                        return data.get("organic", [])
                    else:
                        print(f"⚠️ Brave API error: {response.status}")
                        return []
        except Exception as e:
            print(f"❌ Brave error: {e}")
            return []
    
    async def generate_leads_with_apis(self):
        """Generate leads using traditional APIs"""
        print("\n🔄 Falling back to traditional APIs...")
        
        queries = [
            "manufacturing companies 50-200 employees Texas",
            "technology companies 20-100 employees California",
            "healthcare companies 30-150 employees Florida",
            "professional services firms 25-75 employees New York"
        ]
        
        all_results = []
        
        # Try Tavily first
        print("\n📡 Trying Tavily API...")
        for query in queries[:2]:  # Try first 2 queries with Tavily
            results = await self.search_tavily(query)
            all_results.extend(results)
        
        if all_results:
            print(f"✅ Tavily found {len(all_results)} results")
        else:
            # Fall back to Brave Search
            print("\n📡 Tavily failed, trying Brave Search...")
            for query in queries:
                results = await self.search_brave(query)
                all_results.extend(results)
            
            if all_results:
                print(f"✅ Brave Search found {len(all_results)} results")
        
        # Process results into leads
        self.api_leads = await self.process_results(all_results)
        
    async def process_results(self, results: List[Dict]) -> List[Dict]:
        """Process search results into lead format"""
        leads = []
        
        for result in results[:30]:  # Limit to 30
            # Extract company info
            title = result.get("title", "")
            link = result.get("link", result.get("url", ""))
            snippet = result.get("snippet", result.get("content", ""))
            
            # Parse company name from title
            company_name = title.split(" - ")[0].split(" | ")[0] if title else "Unknown"
            
            # Extract employee count from snippet
            employee_match = re.search(r'(\d+)-(\d+)\s*employees?', snippet, re.I)
            if employee_match:
                emp_min = int(employee_match.group(1))
                emp_max = int(employee_match.group(2))
                estimated_employees = (emp_min + emp_max) // 2
            else:
                # Estimate based on query match
                estimated_employees = 100  # Default mid-range
            
            # Calculate OPEX and savings
            avg_opex_per_employee = 11500
            estimated_opex = estimated_employees * avg_opex_per_employee
            min_savings = estimated_opex * 0.15
            max_savings = estimated_opex * 0.30
            
            # Classify industry
            industry = self.classify_industry(title + " " + snippet)
            
            # Calculate lead score
            lead_score = self.calculate_lead_score(estimated_employees, industry, link)
            
            lead = {
                "company_name": company_name,
                "url": link,
                "industry": industry,
                "estimated_employees": estimated_employees,
                "estimated_opex": f"${estimated_opex:,.0f}",
                "potential_savings_range": f"${min_savings:,.0f} - ${max_savings:,.0f}",
                "average_potential_savings": f"${(min_savings + max_savings) / 2:,.0f}",
                "emails": [],  # Would need email enrichment
                "phones": [],
                "lead_score": lead_score,
                "priority": "High" if lead_score >= 70 else "Medium" if lead_score >= 50 else "Low",
                "snippet": snippet[:200] if snippet else "",
                "source": "Traditional API"
            }
            
            leads.append(lead)
        
        return leads
    
    def classify_industry(self, text: str) -> str:
        """Classify industry from text"""
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in ["manufacturing", "factory", "industrial"]):
            return "Manufacturing"
        elif any(kw in text_lower for kw in ["technology", "software", "it", "tech", "saas"]):
            return "Technology"
        elif any(kw in text_lower for kw in ["healthcare", "medical", "hospital", "health"]):
            return "Healthcare"
        elif any(kw in text_lower for kw in ["professional services", "consulting", "services"]):
            return "Professional Services"
        else:
            return "Other"
    
    def calculate_lead_score(self, employees: int, industry: str, url: str) -> int:
        """Calculate lead score 0-100"""
        score = 0
        
        # Employee count (25 pts)
        if 50 <= employees <= 200:
            score += 25
        elif 20 <= employees < 50 or 200 < employees <= 300:
            score += 20
        elif employees >= 10:
            score += 15
        
        # Industry (25 pts)
        high_value = ["Technology", "Healthcare", "Manufacturing"]
        if industry in high_value:
            score += 25
        elif industry == "Professional Services":
            score += 20
        elif industry != "Other":
            score += 15
        
        # URL quality (25 pts)
        if url and "http" in url:
            score += 25
        else:
            score += 10
        
        # Size estimate (25 pts)
        if employees >= 100:
            score += 25
        elif employees >= 50:
            score += 20
        else:
            score += 15
        
        return min(score, 100)
    
    def save_results(self):
        """Save leads to daily file"""
        all_leads = self.scrapling_leads + self.api_leads
        
        if not all_leads:
            print("⚠️ No leads to save")
            return None
        
        # Sort by lead score
        all_leads.sort(key=lambda x: x.get("lead_score", 0), reverse=True)
        
        # Create leads directory
        leads_dir = Path("/Users/cubiczan/.openclaw/workspace/leads")
        leads_dir.mkdir(exist_ok=True)
        
        # Generate filename
        today = datetime.now().strftime("%Y-%m-%d")
        filename = leads_dir / f"daily-leads-{today}.md"
        
        # Generate markdown content
        md_content = f"""# Daily Lead Report - {today}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📊 Summary

- **Total Leads:** {len(all_leads)}
- **High Priority (70+):** {sum(1 for l in all_leads if l.get("lead_score", 0) >= 70)}
- **Medium Priority (50-69):** {sum(1 for l in all_leads if 50 <= l.get("lead_score", 0) < 70)}
- **Low Priority (<50):** {sum(1 for l in all_leads if l.get("lead_score", 0) < 50)}

## 🔍 Data Source Report

- **Scrapling Used:** {"✅ Yes" if self.scrapling_available else "❌ No"}
- **Scrapling Results:** {len(self.scrapling_leads)} leads
- **Traditional API Results:** {len(self.api_leads)} leads
- **Total Processing Time:** {(datetime.now() - self.start_time).total_seconds():.1f} seconds

## 🎯 Top 3 High-Priority Leads

"""
        
        # Add top 3 leads
        for i, lead in enumerate(all_leads[:3], 1):
            md_content += f"""### {i}. {lead.get("company_name", "Unknown")}

- **Industry:** {lead.get("industry", "N/A")}
- **Estimated Employees:** {lead.get("estimated_employees", "N/A")}
- **Estimated OPEX:** {lead.get("estimated_opex", "N/A")}
- **Potential Savings:** {lead.get("potential_savings_range", "N/A")}
- **Lead Score:** {lead.get("lead_score", 0)}/100
- **Priority:** {lead.get("priority", "N/A")}
- **URL:** {lead.get("url", "N/A")}
- **Source:** {lead.get("source", "N/A")}

"""
        
        # Add all leads table
        md_content += "\n## 📋 All Leads\n\n"
        md_content += "| Company | Industry | Employees | Est. OPEX | Savings Range | Score | Priority |\n"
        md_content += "|---------|----------|-----------|-----------|---------------|-------|----------|\n"
        
        for lead in all_leads:
            md_content += f"| {lead.get('company_name', 'N/A')[:30]} | {lead.get('industry', 'N/A')} | {lead.get('estimated_employees', 'N/A')} | {lead.get('estimated_opex', 'N/A')} | {lead.get('potential_savings_range', 'N/A')} | {lead.get('lead_score', 0)} | {lead.get('priority', 'N/A')} |\n"
        
        # Write file
        with open(filename, 'w') as f:
            f.write(md_content)
        
        print(f"✅ Saved {len(all_leads)} leads to {filename}")
        return filename
    
    async def run(self):
        """Run the complete lead generation process"""
        print("=" * 60)
        print("🚀 Enhanced Lead Gen v2 - Scrapling-First")
        print("=" * 60)
        
        # Step 1: Try Scrapling
        scrapling_success = await self.try_scrapling()
        
        # Step 2: Use APIs if needed
        if not scrapling_success or len(self.scrapling_leads) < 20:
            await self.generate_leads_with_apis()
        
        # Step 3: Save results
        filename = self.save_results()
        
        # Step 4: Generate report
        all_leads = self.scrapling_leads + self.api_leads
        processing_time = (datetime.now() - self.start_time).total_seconds()
        
        report = {
            "total_leads": len(all_leads),
            "high_priority": sum(1 for l in all_leads if l.get("lead_score", 0) >= 70),
            "medium_priority": sum(1 for l in all_leads if 50 <= l.get("lead_score", 0) < 70),
            "scrapling_used": self.scrapling_available,
            "scrapling_results": len(self.scrapling_leads),
            "api_results": len(self.api_leads),
            "processing_time_seconds": round(processing_time, 1),
            "filename": str(filename) if filename else None,
            "top_3": all_leads[:3] if all_leads else []
        }
        
        print("\n" + "=" * 60)
        print("✅ Lead Generation Complete!")
        print("=" * 60)
        print(f"Total Leads: {report['total_leads']}")
        print(f"High Priority: {report['high_priority']}")
        print(f"Scrapling Used: {'✅' if report['scrapling_used'] else '❌'}")
        print(f"Processing Time: {report['processing_time_seconds']}s")
        
        return report

if __name__ == "__main__":
    gen = EnhancedLeadGen()
    report = asyncio.run(gen.run())
    
    # Output JSON for parsing
    print("\n" + json.dumps(report, indent=2, default=str))
