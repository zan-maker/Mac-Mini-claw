#!/usr/bin/env python3
"""
Expense Reduction Lead Generation - Scrapling-First Approach
Generates 15-20 leads daily using Scrapling integration with fallback to Tavily/Brave Search.
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Add scrapling integration to path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# Import after adding to path
try:
    from cron_integration import ScraplingCronIntegration
    SCRAPLING_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Scrapling not available: {e}")
    SCRAPLING_AVAILABLE = False

# API Keys
TAVILY_API_KEY = "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"
BRAVE_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"

# Directories
WORKSPACE_DIR = Path("/Users/cubiczan/.openclaw/workspace")
LEADS_DIR = WORKSPACE_DIR / "expense-leads"
LEADS_DIR.mkdir(exist_ok=True)


class ExpenseReductionLeadGen:
    """Expense reduction lead generator with Scrapling-first approach."""
    
    def __init__(self):
        self.scrapling = None
        self.scrapling_initialized = False
        self.scrapling_leads = []
        self.api_leads = []
        self.total_processing_time = 0
        self.start_time = datetime.now()
    
    async def try_scrapling_first(self) -> List[Dict[str, Any]]:
        """Try to generate leads using Scrapling integration."""
        if not SCRAPLING_AVAILABLE:
            print("⚠️ Scrapling not available, skipping...")
            return []
        
        try:
            print("🚀 Attempting Scrapling integration...")
            self.scrapling = ScraplingCronIntegration(stealth_mode=True)
            self.scrapling_initialized = await self.scrapling.initialize()
            
            if not self.scrapling_initialized:
                print("❌ Scrapling initialization failed")
                return []
            
            print("✅ Scrapling initialized successfully")
            
            # Define search queries for expense reduction leads
            search_queries = [
                "manufacturing companies 50-200 employees",
                "technology companies 20-100 employees",
                "healthcare companies 30-150 employees",
                "professional services firms 25-75 employees",
                "financial services companies 40-120 employees",
                "SaaS companies Series A-C funding",
                "logistics companies 100-300 employees",
                "retail companies 50-150 employees"
            ]
            
            # Generate leads using Scrapling
            leads = await self.scrapling.generate_expense_reduction_leads(
                search_queries=search_queries,
                limit=20
            )
            
            print(f"✅ Scrapling found {len(leads)} leads")
            return leads
            
        except Exception as e:
            print(f"❌ Scrapling error: {e}")
            return []
    
    async def fallback_to_tavily(self) -> List[Dict[str, Any]]:
        """Fall back to Tavily API for lead generation."""
        print("🔄 Falling back to Tavily API...")
        
        try:
            import aiohttp
            
            # Tavily search queries
            queries = [
                "CFO manufacturing companies 50-200 employees",
                "VP Finance technology companies Series A",
                "Controller healthcare companies 100+ employees",
                "Director Operations professional services firms",
                "Procurement Manager financial services companies"
            ]
            
            leads = []
            
            async with aiohttp.ClientSession() as session:
                for query in queries:
                    try:
                        payload = {
                            "api_key": TAVILY_API_KEY,
                            "query": query,
                            "search_depth": "advanced",
                            "max_results": 5
                        }
                        
                        async with session.post(
                            "https://api.tavily.com/search",
                            json=payload
                        ) as response:
                            if response.status == 200:
                                data = await response.json()
                                # Process results
                                for result in data.get("results", []):
                                    lead = self._process_api_result(result, "Tavily")
                                    if lead:
                                        leads.append(lead)
                            else:
                                print(f"⚠️ Tavily API error: {response.status}")
                    except Exception as e:
                        print(f"⚠️ Tavily query error: {e}")
            
            print(f"✅ Tavily found {len(leads)} leads")
            return leads
            
        except Exception as e:
            print(f"❌ Tavily error: {e}")
            return []
    
    async def fallback_to_brave(self) -> List[Dict[str, Any]]:
        """Final fallback to Brave Search API."""
        print("🔄 Falling back to Brave Search API...")
        
        try:
            import aiohttp
            
            queries = [
                "manufacturing companies CFO contact",
                "technology startups VP Finance",
                "healthcare organizations Controller",
                "professional services firms operations director"
            ]
            
            leads = []
            
            async with aiohttp.ClientSession() as session:
                for query in queries:
                    try:
                        headers = {
                            "Accept": "application/json",
                            "X-Subscription-Token": BRAVE_API_KEY
                        }
                        
                        params = {
                            "q": query,
                            "count": 5
                        }
                        
                        async with session.get(
                            "https://api.search.brave.com/res/v1/web/search",
                            headers=headers,
                            params=params
                        ) as response:
                            if response.status == 200:
                                data = await response.json()
                                # Process results
                                for result in data.get("web", {}).get("results", []):
                                    lead = self._process_api_result(result, "Brave")
                                    if lead:
                                        leads.append(lead)
                            else:
                                print(f"⚠️ Brave API error: {response.status}")
                    except Exception as e:
                        print(f"⚠️ Brave query error: {e}")
            
            print(f"✅ Brave Search found {len(leads)} leads")
            return leads
            
        except Exception as e:
            print(f"❌ Brave Search error: {e}")
            return []
    
    def _process_api_result(self, result: Dict[str, Any], source: str) -> Dict[str, Any]:
        """Process API search result into lead format."""
        try:
            # Extract basic info
            url = result.get("url", "")
            title = result.get("title", "")
            description = result.get("description", "")
            
            if not url:
                return None
            
            # Extract company name
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc.replace("www.", "")
            company_name = domain.split(".")[0].title()
            
            # Estimate company size based on industry keywords
            industry = self._classify_industry_from_text(f"{title} {description}")
            
            # Estimate employees (conservative estimate for API results)
            estimated_employees = 75  # Default mid-range
            
            # Calculate OPEX and savings
            avg_opex_per_employee = 11500
            estimated_opex = estimated_employees * avg_opex_per_employee
            min_savings = int(estimated_opex * 0.15)
            max_savings = int(estimated_opex * 0.30)
            avg_savings = (min_savings + max_savings) // 2
            
            # Calculate lead score
            lead_score = self._calculate_lead_score(
                estimated_employees,
                industry,
                0,  # No email count from API
                5000  # Assume medium website quality
            )
            
            return {
                "company_name": company_name,
                "url": url,
                "title": title,
                "description": description[:200],
                "industry": industry,
                "estimated_employees": estimated_employees,
                "estimated_opex": f"${estimated_opex:,}",
                "potential_savings_range": f"${min_savings:,} - ${max_savings:,}",
                "average_potential_savings": f"${avg_savings:,}",
                "emails": [],
                "phones": [],
                "lead_score": lead_score,
                "priority": "High" if lead_score >= 70 else "Medium" if lead_score >= 50 else "Low",
                "source": source,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"⚠️ Error processing API result: {e}")
            return None
    
    def _classify_industry_from_text(self, text: str) -> str:
        """Classify industry from text."""
        text = text.lower()
        
        industry_keywords = {
            "Technology": ["tech", "software", "saas", "platform", "api", "cloud", "ai"],
            "Manufacturing": ["manufacturing", "factory", "production", "industrial"],
            "Healthcare": ["health", "medical", "hospital", "clinic", "pharma"],
            "Professional Services": ["consulting", "services", "agency", "advisory"],
            "Financial Services": ["finance", "bank", "investment", "insurance", "fintech"],
            "Retail/E-commerce": ["shop", "store", "marketplace", "retail"],
            "Logistics": ["logistics", "supply chain", "shipping", "warehouse"],
            "Construction": ["construction", "building", "contractor"]
        }
        
        for industry, keywords in industry_keywords.items():
            if any(keyword in text for keyword in keywords):
                return industry
        
        return "Other"
    
    def _calculate_lead_score(self, employees: int, industry: str, 
                             email_count: int, html_size: int) -> int:
        """Calculate lead score (0-100)."""
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
        else:
            score += 5
        
        # Industry (25 points)
        high_opex_industries = ["Technology", "Healthcare", "Financial Services", "Manufacturing"]
        if industry in high_opex_industries:
            score += 25
        elif industry in ["Professional Services", "Logistics", "Construction"]:
            score += 15
        elif industry != "Other":
            score += 10
        
        # Contact information (25 points)
        if email_count >= 3:
            score += 25
        elif email_count >= 2:
            score += 20
        elif email_count >= 1:
            score += 15
        else:
            score += 5  # API results still have potential
        
        # Website quality (25 points)
        if html_size > 10000:
            score += 25
        elif html_size > 5000:
            score += 20
        elif html_size > 2000:
            score += 15
        else:
            score += 10
        
        return min(score, 100)
    
    async def generate_leads(self) -> List[Dict[str, Any]]:
        """Generate leads using Scrapling-first approach with fallbacks."""
        all_leads = []
        
        # Try Scrapling first
        self.scrapling_leads = await self.try_scrapling_first()
        all_leads.extend(self.scrapling_leads)
        
        # If Scrapling didn't return enough leads, fall back to Tavily
        if len(all_leads) < 15:
            self.api_leads = await self.fallback_to_tavily()
            all_leads.extend(self.api_leads)
        
        # If still not enough, fall back to Brave Search
        if len(all_leads) < 15:
            brave_leads = await self.fallback_to_brave()
            all_leads.extend(brave_leads)
        
        # Deduplicate by company name
        seen = set()
        unique_leads = []
        for lead in all_leads:
            company = lead.get("company_name", "").lower()
            if company not in seen:
                seen.add(company)
                unique_leads.append(lead)
        
        # Sort by lead score (highest first)
        unique_leads.sort(key=lambda x: x.get("lead_score", 0), reverse=True)
        
        # Limit to 20 leads
        final_leads = unique_leads[:20]
        
        # Calculate processing time
        self.total_processing_time = (datetime.now() - self.start_time).total_seconds()
        
        print(f"\n✅ Total leads generated: {len(final_leads)}")
        print(f"   - Scrapling: {len(self.scrapling_leads)}")
        print(f"   - Traditional APIs: {len(self.api_leads)}")
        print(f"   - Processing time: {self.total_processing_time:.1f}s")
        
        return final_leads
    
    def save_results(self, leads: List[Dict[str, Any]]):
        """Save leads to files."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Save daily leads
        daily_file = LEADS_DIR / f"daily-leads-{today}.md"
        with open(daily_file, "w") as f:
            f.write(f"# Expense Reduction Leads - {today}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Leads:** {len(leads)}\n")
            f.write(f"**High Priority:** {sum(1 for l in leads if l.get('priority') == 'High')}\n")
            f.write(f"**Data Source:** Scrapling ({len(self.scrapling_leads)}) + APIs ({len(self.api_leads)})\n\n")
            
            f.write("## Lead Summary\n\n")
            for i, lead in enumerate(leads, 1):
                f.write(f"### {i}. {lead.get('company_name', 'Unknown')}\n")
                f.write(f"- **Industry:** {lead.get('industry', 'N/A')}\n")
                f.write(f"- **Employees:** ~{lead.get('estimated_employees', 'N/A')}\n")
                f.write(f"- **Estimated OPEX:** {lead.get('estimated_opex', 'N/A')}\n")
                f.write(f"- **Potential Savings:** {lead.get('potential_savings_range', 'N/A')}\n")
                f.write(f"- **Lead Score:** {lead.get('lead_score', 0)}/100\n")
                f.write(f"- **Priority:** {lead.get('priority', 'Low')}\n")
                f.write(f"- **Source:** {lead.get('source', 'Unknown')}\n")
                if lead.get("url"):
                    f.write(f"- **Website:** {lead.get('url')}\n")
                if lead.get("emails"):
                    f.write(f"- **Emails:** {', '.join(lead.get('emails', []))}\n")
                f.write("\n")
        
        print(f"✅ Saved daily leads to: {daily_file}")
        
        # Update pipeline
        pipeline_file = LEADS_DIR / "pipeline.md"
        
        # Read existing pipeline if it exists
        existing_content = ""
        if pipeline_file.exists():
            with open(pipeline_file, "r") as f:
                existing_content = f.read()
        
        # Add new leads to pipeline
        with open(pipeline_file, "w") as f:
            f.write("# Expense Reduction Lead Pipeline\n\n")
            f.write(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Add today's leads
            f.write(f"## Today's Leads ({today})\n\n")
            
            high_priority = [l for l in leads if l.get('priority') == 'High']
            medium_priority = [l for l in leads if l.get('priority') == 'Medium']
            
            if high_priority:
                f.write("### High Priority\n\n")
                for lead in high_priority:
                    f.write(f"- **{lead.get('company_name')}** ({lead.get('industry')}) - ")
                    f.write(f"Potential Savings: {lead.get('average_potential_savings')}\n")
                f.write("\n")
            
            if medium_priority:
                f.write("### Medium Priority\n\n")
                for lead in medium_priority:
                    f.write(f"- **{lead.get('company_name')}** ({lead.get('industry')}) - ")
                    f.write(f"Potential Savings: {lead.get('average_potential_savings')}\n")
                f.write("\n")
            
            # Add historical data if exists
            if existing_content and "## Historical" not in existing_content:
                f.write("\n---\n\n## Historical Leads\n\n")
                f.write(existing_content)
        
        print(f"✅ Updated pipeline: {pipeline_file}")
    
    def generate_summary(self, leads: List[Dict[str, Any]]) -> str:
        """Generate summary for Discord."""
        high_priority = [l for l in leads if l.get('priority') == 'High']
        medium_priority = [l for l in leads if l.get('priority') == 'Medium']
        
        # Calculate total potential savings
        total_min = 0
        total_max = 0
        for lead in leads:
            savings_range = lead.get('potential_savings_range', '$0 - $0')
            # Parse savings range
            import re
            matches = re.findall(r'\$([\d,]+)', savings_range)
            if len(matches) >= 2:
                total_min += int(matches[0].replace(',', ''))
                total_max += int(matches[1].replace(',', ''))
        
        # Top 3 leads
        top_3 = leads[:3]
        
        summary = f"""📊 **Expense Reduction Lead Gen - {datetime.now().strftime('%B %d, %Y')}**

**Total Leads Generated:** {len(leads)}

**Priority Breakdown:**
• High Priority: {len(high_priority)}
• Medium Priority: {len(medium_priority)}
• Low Priority: {len(leads) - len(high_priority) - len(medium_priority)}

**Total Potential Savings:** ${total_min:,} - ${total_max:,}

**🔍 Data Source Report:**
• Scrapling Used: {'✅ Yes' if self.scrapling_leads else '❌ No'}
• Scrapling Results: {len(self.scrapling_leads)} leads
• Traditional API Results: {len(self.api_leads)} leads
• Total Processing Time: {self.total_processing_time:.1f} seconds

**🏆 Top 3 Leads:**
"""
        
        for i, lead in enumerate(top_3, 1):
            summary += f"\n{i}. **{lead.get('company_name')}** ({lead.get('industry')})"
            summary += f"\n   • Employees: ~{lead.get('estimated_employees')}"
            summary += f"\n   • Potential Savings: {lead.get('potential_savings_range')}"
            summary += f"\n   • Score: {lead.get('lead_score')}/100"
            summary += f"\n   • Source: {lead.get('source')}"
        
        summary += f"\n\n📁 Full report saved to: `/workspace/expense-leads/daily-leads-{datetime.now().strftime('%Y-%m-%d')}.md`"
        
        return summary


async def main():
    """Main execution."""
    print("=" * 80)
    print("EXPENSE REDUCTION LEAD GENERATION - SCRAPLING-FIRST APPROACH")
    print("=" * 80)
    print()
    
    # Initialize lead generator
    generator = ExpenseReductionLeadGen()
    
    # Generate leads
    leads = await generator.generate_leads()
    
    if not leads:
        print("❌ No leads generated")
        return
    
    # Save results
    generator.save_results(leads)
    
    # Generate summary
    summary = generator.generate_summary(leads)
    
    print("\n" + "=" * 80)
    print("SUMMARY FOR DISCORD")
    print("=" * 80)
    print(summary)
    
    # Save summary for Discord delivery
    summary_file = WORKSPACE_DIR / "expense-reduction-summary.txt"
    with open(summary_file, "w") as f:
        f.write(summary)
    
    print(f"\n✅ Summary saved to: {summary_file}")
    print("\nNOTE: Summary will be delivered automatically to Discord channel #mac-mini1")


if __name__ == "__main__":
    asyncio.run(main())
