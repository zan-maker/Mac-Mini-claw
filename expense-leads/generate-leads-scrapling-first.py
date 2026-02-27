#!/usr/bin/env python3
"""
Expense Reduction Lead Generation - Scrapling-First Approach
Tries Scrapling first, falls back to Tavily API if needed.
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import List, Dict, Any

# Add Scrapling integration path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# Tavily API
import requests

# Configuration
TAVILY_API_KEY = "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"
BRAVE_API_KEY = "BSA4VYA3FjSPQmTjZeKjsq5CqWvFy2u"
OUTPUT_DIR = "/Users/cubiczan/.openclaw/workspace/expense-leads"

class ExpenseLeadGenerator:
    def __init__(self):
        self.scrapling_used = False
        self.scrapling_results = 0
        self.api_results = 0
        self.processing_start = datetime.now()
        
    async def try_scrapling_first(self, limit=20) -> List[Dict[str, Any]]:
        """Try Scrapling integration first."""
        print("=" * 60)
        print("🔍 ATTEMPTING SCRAPLING INTEGRATION")
        print("=" * 60)
        
        try:
            from cron_integration import ScraplingCronIntegration
            
            # Initialize Scrapling
            scrapling = ScraplingCronIntegration(stealth_mode=True)
            success = await scrapling.initialize()
            
            if success:
                print("✅ Scrapling initialized successfully")
                
                # Search queries for expense reduction leads
                search_queries = [
                    "manufacturing companies 50-200 employees",
                    "technology companies 20-100 employees",
                    "healthcare companies 30-150 employees",
                    "professional services firms 25-75 employees",
                    "financial services companies 40-120 employees"
                ]
                
                leads = await scrapling.generate_expense_reduction_leads(
                    search_queries=search_queries,
                    limit=limit
                )
                
                if leads and len(leads) > 0:
                    self.scrapling_used = True
                    self.scrapling_results = len(leads)
                    print(f"✅ Scrapling found {len(leads)} leads")
                    return leads
                else:
                    print("⚠️ Scrapling returned no leads, falling back to Tavily")
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
    
    def search_tavily(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search using Tavily API."""
        print(f"🔍 Searching Tavily: {query}")
        
        url = "https://api.tavily.com/search"
        
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
            "include_domains": [],
            "exclude_domains": ["linkedin.com", "facebook.com", "twitter.com", "instagram.com"],
            "include_answer": True,
            "include_raw_content": False
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            results = data.get("results", [])
            print(f"✅ Tavily found {len(results)} results")
            return results
            
        except Exception as e:
            print(f"❌ Tavily error: {e}")
            return []
    
    def search_brave(self, query: str, count: int = 10) -> List[Dict[str, Any]]:
        """Search using Brave Search API (fallback)."""
        print(f"🔍 Searching Brave (fallback): {query}")
        
        url = "https://api.search.brave.com/res/v1/web/search"
        
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": BRAVE_API_KEY
        }
        
        params = {
            "q": query,
            "count": count,
            "search_lang": "en",
            "country": "us"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            results = data.get("web", {}).get("results", [])
            print(f"✅ Brave found {len(results)} results")
            return results
            
        except Exception as e:
            print(f"❌ Brave error: {e}")
            return []
    
    def extract_company_from_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract company information from search result."""
        url = result.get("url", "")
        title = result.get("title", "")
        description = result.get("description", result.get("content", ""))
        
        # Extract company name from title
        company_name = title.split("-")[0].split("|")[0].strip()
        
        # Estimate employee count from description
        estimated_employees = self._estimate_employees(description)
        
        # Classify industry
        industry = self._classify_industry(title + " " + description)
        
        # Estimate OPEX
        estimated_opex = estimated_employees * 11500  # $11,500 per employee
        
        # Calculate potential savings (15-30%)
        min_savings = int(estimated_opex * 0.15)
        max_savings = int(estimated_opex * 0.30)
        avg_savings = int((min_savings + max_savings) / 2)
        
        # Calculate lead score
        lead_score = self._calculate_lead_score(
            estimated_employees,
            industry,
            url
        )
        
        return {
            "company_name": company_name,
            "url": url,
            "title": title,
            "description": description[:200] if description else "",
            "industry": industry,
            "estimated_employees": estimated_employees,
            "estimated_opex": f"${estimated_opex:,.0f}",
            "potential_savings_range": f"${min_savings:,.0f} - ${max_savings:,.0f}",
            "average_potential_savings": f"${avg_savings:,.0f}",
            "lead_score": lead_score,
            "priority": "High" if lead_score >= 70 else "Medium" if lead_score >= 50 else "Low",
            "source": "Tavily API",
            "found_at": datetime.now().isoformat()
        }
    
    def _estimate_employees(self, text: str) -> int:
        """Estimate employee count from text."""
        text = text.lower()
        
        # Look for employee count indicators
        if "fortune 500" in text or "enterprise" in text:
            return 500
        elif "mid-sized" in text or "midsize" in text:
            return 150
        elif "growing" in text or "expanding" in text:
            return 100
        elif "startup" in text or "seed" in text:
            return 20
        elif "small business" in text or "smb" in text:
            return 30
        else:
            # Default based on industry keywords
            return 75
    
    def _classify_industry(self, text: str) -> str:
        """Classify industry from text."""
        text = text.lower()
        
        industry_keywords = {
            "Technology/SaaS": ["software", "saas", "platform", "api", "cloud", "ai", "tech", "digital"],
            "Manufacturing": ["manufacturing", "factory", "production", "industrial", "machinery", "fabrication"],
            "Healthcare": ["healthcare", "medical", "hospital", "clinic", "pharma", "biotech", "health"],
            "Professional Services": ["consulting", "services", "agency", "advisory", "solutions", "firm"],
            "Financial Services": ["finance", "bank", "investment", "insurance", "fintech", "capital"],
            "Retail/E-commerce": ["retail", "ecommerce", "shop", "store", "marketplace", "consumer"],
            "Construction": ["construction", "building", "contractor", "engineering", "infrastructure"],
            "Education": ["education", "learning", "school", "university", "training", "edtech"],
            "Logistics": ["logistics", "supply chain", "shipping", "distribution", "warehouse", "freight"],
            "Energy": ["energy", "renewable", "solar", "wind", "utilities", "power"]
        }
        
        best_industry = "Other"
        best_score = 0
        
        for industry, keywords in industry_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > best_score:
                best_score = score
                best_industry = industry
        
        return best_industry
    
    def _calculate_lead_score(self, employees: int, industry: str, url: str) -> int:
        """Calculate lead score (0-100)."""
        score = 0
        
        # Employee count (25 points)
        if 100 <= employees <= 300:
            score += 25  # Sweet spot
        elif 50 <= employees < 100:
            score += 20
        elif 300 < employees <= 500:
            score += 20
        elif 20 <= employees < 50:
            score += 15
        else:
            score += 10
        
        # Industry (25 points)
        high_opex = ["Technology/SaaS", "Healthcare", "Financial Services", "Manufacturing"]
        medium_opex = ["Professional Services", "Logistics", "Energy", "Construction"]
        
        if industry in high_opex:
            score += 25
        elif industry in medium_opex:
            score += 20
        elif industry != "Other":
            score += 15
        else:
            score += 5
        
        # URL quality (25 points)
        if ".com" in url:
            score += 20
        if "https://" in url:
            score += 5
        
        # Estimated OPEX indicator (25 points)
        if employees >= 200:
            score += 25
        elif employees >= 100:
            score += 20
        elif employees >= 50:
            score += 15
        else:
            score += 10
        
        return min(score, 100)
    
    async def generate_leads_with_api(self, limit=20) -> List[Dict[str, Any]]:
        """Generate leads using Tavily API (fallback)."""
        print("=" * 60)
        print("🔍 USING TAVILY API (FALLBACK)")
        print("=" * 60)
        
        leads = []
        
        # Search queries targeting companies with high OPEX
        search_queries = [
            "growing manufacturing companies 50-200 employees USA",
            "mid-sized technology companies 20-100 employees",
            "healthcare technology companies 30-150 employees",
            "professional services firms 25-75 employees",
            "financial services companies 40-120 employees",
            "logistics and supply chain companies 50-200 employees",
            "SaaS companies series B funding",
            "expanding retail companies 100+ employees",
            "construction companies commercial projects",
            "energy and utilities companies mid-sized"
        ]
        
        seen_companies = set()
        
        for query in search_queries:
            if len(leads) >= limit:
                break
            
            results = self.search_tavily(query, max_results=5)
            
            for result in results:
                if len(leads) >= limit:
                    break
                
                company = self.extract_company_from_result(result)
                company_key = company["company_name"].lower().strip()
                
                # Avoid duplicates
                if company_key not in seen_companies:
                    seen_companies.add(company_key)
                    leads.append(company)
                    print(f"✅ Found lead: {company['company_name']} - {company['industry']} - Score: {company['lead_score']}")
        
        self.api_results = len(leads)
        return leads
    
    def save_results(self, leads: List[Dict[str, Any]]):
        """Save leads to files."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Save daily leads
        daily_file = f"{OUTPUT_DIR}/daily-leads-{today}.md"
        with open(daily_file, 'w') as f:
            f.write(f"# Expense Reduction Leads - {today}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Leads:** {len(leads)}\n\n")
            
            # Group by priority
            high_priority = [l for l in leads if l['priority'] == 'High']
            medium_priority = [l for l in leads if l['priority'] == 'Medium']
            low_priority = [l for l in leads if l['priority'] == 'Low']
            
            f.write(f"**High Priority:** {len(high_priority)}\n")
            f.write(f"**Medium Priority:** {len(medium_priority)}\n")
            f.write(f"**Low Priority:** {len(low_priority)}\n\n")
            
            # High Priority Leads
            if high_priority:
                f.write("## 🔴 High Priority Leads\n\n")
                for lead in sorted(high_priority, key=lambda x: x['lead_score'], reverse=True):
                    f.write(f"### {lead['company_name']}\n")
                    f.write(f"- **Industry:** {lead['industry']}\n")
                    f.write(f"- **Estimated Employees:** {lead['estimated_employees']}\n")
                    f.write(f"- **Estimated OPEX:** {lead['estimated_opex']}\n")
                    f.write(f"- **Potential Savings:** {lead['potential_savings_range']}\n")
                    f.write(f"- **Lead Score:** {lead['lead_score']}/100\n")
                    f.write(f"- **URL:** {lead['url']}\n")
                    f.write(f"- **Source:** {lead['source']}\n")
                    if lead.get('description'):
                        f.write(f"- **Description:** {lead['description']}\n")
                    f.write("\n")
            
            # Medium Priority Leads
            if medium_priority:
                f.write("## 🟡 Medium Priority Leads\n\n")
                for lead in sorted(medium_priority, key=lambda x: x['lead_score'], reverse=True):
                    f.write(f"### {lead['company_name']}\n")
                    f.write(f"- **Industry:** {lead['industry']}\n")
                    f.write(f"- **Estimated Employees:** {lead['estimated_employees']}\n")
                    f.write(f"- **Estimated OPEX:** {lead['estimated_opex']}\n")
                    f.write(f"- **Potential Savings:** {lead['potential_savings_range']}\n")
                    f.write(f"- **Lead Score:** {lead['lead_score']}/100\n")
                    f.write(f"- **URL:** {lead['url']}\n\n")
            
            # Low Priority Leads
            if low_priority:
                f.write("## 🟢 Low Priority Leads\n\n")
                for lead in sorted(low_priority, key=lambda x: x['lead_score'], reverse=True):
                    f.write(f"- **{lead['company_name']}** ({lead['industry']}) - Score: {lead['lead_score']}\n")
        
        print(f"✅ Saved daily leads to: {daily_file}")
        
        # Update pipeline
        pipeline_file = f"{OUTPUT_DIR}/pipeline.md"
        self._update_pipeline(leads, pipeline_file)
    
    def _update_pipeline(self, leads: List[Dict[str, Any]], pipeline_file: str):
        """Update pipeline file."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Read existing pipeline if it exists
        existing_content = ""
        if os.path.exists(pipeline_file):
            with open(pipeline_file, 'r') as f:
                existing_content = f.read()
        
        # Calculate totals
        high_priority = len([l for l in leads if l['priority'] == 'High'])
        medium_priority = len([l for l in leads if l['priority'] == 'Medium'])
        
        total_potential_savings = sum(
            int(l['average_potential_savings'].replace('$', '').replace(',', ''))
            for l in leads
        )
        
        # Append new entry
        with open(pipeline_file, 'a') as f:
            if not existing_content:
                f.write("# Expense Reduction Pipeline\n\n")
            
            f.write(f"\n## {today}\n\n")
            f.write(f"**Leads Generated:** {len(leads)}\n")
            f.write(f"**High Priority:** {high_priority}\n")
            f.write(f"**Medium Priority:** {medium_priority}\n")
            f.write(f"**Total Potential Savings:** ${total_potential_savings:,.0f}\n\n")
            
            # Top 3 leads
            top_leads = sorted(leads, key=lambda x: x['lead_score'], reverse=True)[:3]
            f.write("**Top 3 Leads:**\n\n")
            for i, lead in enumerate(top_leads, 1):
                f.write(f"{i}. **{lead['company_name']}** ({lead['industry']})\n")
                f.write(f"   - Employees: {lead['estimated_employees']}\n")
                f.write(f"   - Potential Savings: {lead['potential_savings_range']}\n")
                f.write(f"   - Score: {lead['lead_score']}/100\n\n")
            
            f.write("---\n")
        
        print(f"✅ Updated pipeline: {pipeline_file}")
    
    def generate_discord_summary(self, leads: List[Dict[str, Any]]) -> str:
        """Generate Discord summary."""
        processing_time = (datetime.now() - self.processing_start).total_seconds()
        
        high_priority = [l for l in leads if l['priority'] == 'High']
        medium_priority = [l for l in leads if l['priority'] == 'Medium']
        
        total_savings = sum(
            int(l['average_potential_savings'].replace('$', '').replace(',', ''))
            for l in leads
        )
        
        top_3 = sorted(leads, key=lambda x: x['lead_score'], reverse=True)[:3]
        
        summary = f"""📊 **Expense Reduction Lead Gen Report**
📅 {datetime.now().strftime('%A, %B %d, %Y - %I:%M %p')}

🔍 **Data Source Report:**
• Scrapling Used: {'✅ Yes' if self.scrapling_used else '❌ No'}
• Scrapling Results: {self.scrapling_results} leads
• Traditional API Results: {self.api_results} leads
• Total Processing Time: {processing_time:.1f} seconds

📈 **Lead Statistics:**
• Total Leads Generated: **{len(leads)}**
• 🔴 High Priority: **{len(high_priority)}**
• 🟡 Medium Priority: **{len(medium_priority)}**
• 💰 Total Potential Savings: **${total_savings:,.0f}**

🏆 **Top 3 Leads:**
"""
        
        for i, lead in enumerate(top_3, 1):
            summary += f"\n**{i}. {lead['company_name']}**"
            summary += f"\n   • Industry: {lead['industry']}"
            summary += f"\n   • Employees: ~{lead['estimated_employees']}"
            summary += f"\n   • Potential Savings: {lead['potential_savings_range']}"
            summary += f"\n   • Score: {lead['lead_score']}/100\n"
        
        summary += "\n---\n✅ *Leads saved to workspace/expense-leads/*"
        
        return summary
    
    async def run(self, limit=20):
        """Main execution."""
        print("=" * 60)
        print("EXPENSE REDUCTION LEAD GENERATION - SCRAPLING-FIRST")
        print("=" * 60)
        print(f"Target: {limit} qualified leads")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Step 1: Try Scrapling first
        leads = await self.try_scrapling_first(limit)
        
        # Step 2: Fall back to Tavily if needed
        if not leads:
            leads = await self.generate_leads_with_api(limit)
        
        # Step 3: Process and save results
        if leads:
            self.save_results(leads)
            
            # Generate Discord summary
            summary = self.generate_discord_summary(leads)
            
            # Save summary to file for Discord delivery
            summary_file = f"{OUTPUT_DIR}/discord-summary-{datetime.now().strftime('%Y-%m-%d')}.txt"
            with open(summary_file, 'w') as f:
                f.write(summary)
            
            print("\n" + "=" * 60)
            print("DISCORD SUMMARY")
            print("=" * 60)
            print(summary)
            
            return summary
        else:
            print("❌ No leads generated")
            return None


async def main():
    generator = ExpenseLeadGenerator()
    summary = await generator.run(limit=20)
    
    if summary:
        print("\n✅ Lead generation complete!")
        print("📱 Summary ready for Discord delivery")
    else:
        print("\n❌ Lead generation failed")


if __name__ == "__main__":
    asyncio.run(main())
