#!/usr/bin/env python3
"""
Enhanced Lead Gen v2 - Scrapling-First Approach

This script tries Scrapling first, then falls back to Tavily/Brave Search APIs.
Generates 20-30 expense reduction leads quickly.
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from pathlib import Path
import aiohttp
import re

# Add Scrapling integration path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# Configuration
TAVILY_API_KEY = "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"
BRAVE_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"
ZBOUNCE_API_KEY = "fd0105c8c98340e0a2b63e2fbe39d7a4"

class EnhancedLeadGenV2:
    def __init__(self):
        self.scrapling_available = False
        self.scrapling_client = None
        self.scrapling_results = 0
        self.api_results = 0
        self.start_time = datetime.now()
        
    async def try_scrapling(self):
        """Try to initialize and use Scrapling."""
        try:
            from cron_integration import ScraplingCronIntegration
            
            print("🔧 Attempting to initialize Scrapling...")
            self.scrapling_client = ScraplingCronIntegration(stealth_mode=True)
            success = await self.scrapling_client.initialize()
            
            if success:
                self.scrapling_available = True
                print("✅ Scrapling initialized successfully")
                return True
            else:
                print("⚠️ Scrapling initialization failed")
                return False
        except ImportError as e:
            print(f"⚠️ Scrapling not available: {e}")
            return False
        except Exception as e:
            print(f"❌ Scrapling error: {e}")
            return False
    
    async def search_tavily(self, query: str) -> list:
        """Search using Tavily API."""
        url = "https://api.tavily.com/search"
        
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "basic",
            "max_results": 10,
            "include_raw_content": False,
            "include_domains": [],
            "exclude_domains": ["linkedin.com", "facebook.com", "twitter.com", "instagram.com"]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("results", [])
                    else:
                        print(f"⚠️ Tavily API error: {response.status}")
                        return []
        except Exception as e:
            print(f"❌ Tavily search error: {e}")
            return []
    
    async def search_brave(self, query: str) -> list:
        """Search using Brave Search API."""
        url = "https://api.search.brave.com/res/v1/web/search"
        
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": BRAVE_API_KEY
        }
        
        params = {
            "q": query,
            "count": 10,
            "search_lang": "en",
            "country": "us"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("web", {}).get("results", [])
                    else:
                        print(f"⚠️ Brave API error: {response.status}")
                        return []
        except Exception as e:
            print(f"❌ Brave search error: {e}")
            return []
    
    def extract_company_info(self, result: dict) -> dict:
        """Extract company information from search result."""
        # Extract company name from title
        title = result.get("title", "")
        company_name = title.split(" - ")[0].split(" | ")[0].strip()
        
        # Clean up company name
        company_name = re.sub(r'\s+(Inc|LLC|Corp|Company|Co|Ltd|PC|PLLC)\.?$', '', company_name, flags=re.IGNORECASE)
        
        # Get URL
        url = result.get("url", "")
        
        # Get description
        description = result.get("content", result.get("description", ""))
        
        return {
            "company_name": company_name,
            "url": url,
            "description": description,
            "source": "API"
        }
    
    def estimate_employees(self, description: str, title: str) -> int:
        """Estimate employee count from description."""
        text = f"{title} {description}".lower()
        
        # Look for explicit employee counts
        patterns = [
            r'(\d+)\+?\s*employees?',
            r'(\d+)\s*-\s*\d+\s*employees?',
            r'team of (\d+)',
            r'staff of (\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                count = int(match.group(1))
                if 20 <= count <= 500:
                    return count
        
        # Estimate based on keywords
        if any(word in text for word in ["enterprise", "large", "fortune 500"]):
            return 250
        elif any(word in text for word in ["mid-sized", "midsize", "growing"]):
            return 100
        elif any(word in text for word in ["small", "startup", "boutique"]):
            return 30
        else:
            return 75  # Default mid-range
    
    def classify_industry(self, text: str) -> str:
        """Classify industry from text."""
        text = text.lower()
        
        if any(word in text for word in ["manufacturing", "factory", "production", "industrial"]):
            return "Manufacturing"
        elif any(word in text for word in ["technology", "software", "tech", "it", "digital", "saas"]):
            return "Technology"
        elif any(word in text for word in ["healthcare", "medical", "hospital", "health", "clinic"]):
            return "Healthcare"
        elif any(word in text for word in ["financial", "finance", "bank", "investment", "insurance"]):
            return "Financial Services"
        elif any(word in text for word in ["professional", "consulting", "services", "agency", "law", "accounting"]):
            return "Professional Services"
        elif any(word in text for word in ["retail", "ecommerce", "e-commerce", "store"]):
            return "Retail/E-commerce"
        elif any(word in text for word in ["construction", "building", "contractor", "engineering"]):
            return "Construction"
        elif any(word in text for word in ["education", "school", "university", "training", "learning"]):
            return "Education"
        else:
            return "Other"
    
    def calculate_lead_score(self, employees: int, industry: str, has_contact: bool) -> int:
        """Calculate lead score (0-100)."""
        score = 0
        
        # Employee fit (25 points)
        if 50 <= employees <= 200:
            score += 25
        elif 20 <= employees < 50:
            score += 20
        elif 200 < employees <= 300:
            score += 20
        else:
            score += 10
        
        # Industry match (25 points)
        high_value = ["Manufacturing", "Technology", "Healthcare", "Financial Services"]
        medium_value = ["Professional Services", "Construction", "Retail/E-commerce"]
        
        if industry in high_value:
            score += 25
        elif industry in medium_value:
            score += 20
        else:
            score += 10
        
        # Contact info (25 points)
        if has_contact:
            score += 25
        else:
            score += 10
        
        # Random factor for variety (25 points)
        import random
        score += random.randint(15, 25)
        
        return min(score, 100)
    
    def calculate_savings(self, employees: int) -> dict:
        """Calculate potential expense reduction savings."""
        # Average OPEX per employee: $8K-$15K annually
        avg_opex_per_employee = 11500
        estimated_opex = employees * avg_opex_per_employee
        
        # Potential savings: 15-30% of OPEX
        min_savings = int(estimated_opex * 0.15)
        max_savings = int(estimated_opex * 0.30)
        
        return {
            "estimated_opex": f"${estimated_opex:,.0f}",
            "min_savings": f"${min_savings:,.0f}",
            "max_savings": f"${max_savings:,.0f}",
            "avg_savings": f"${(min_savings + max_savings) // 2:,.0f}"
        }
    
    async def generate_leads(self) -> list:
        """Generate leads using Scrapling-first approach."""
        leads = []
        
        # Search queries for different industries and regions
        queries = [
            "manufacturing companies 50-200 employees Texas",
            "technology companies 20-100 employees California",
            "healthcare companies 30-150 employees Florida",
            "professional services firms 25-75 employees New York",
            "construction companies 40-200 employees Georgia",
            "financial services firms 30-100 employees Illinois"
        ]
        
        print(f"\n🔍 Starting lead generation with {len(queries)} search queries...")
        
        # Step 1: Try Scrapling first (if available)
        if self.scrapling_available and self.scrapling_client:
            print("\n📊 Step 1: Using Scrapling for enhanced scraping...")
            try:
                scrapling_leads = await self.scrapling_client.generate_expense_reduction_leads(
                    search_queries=queries[:2],  # Try first 2 queries with Scrapling
                    limit=10
                )
                if scrapling_leads:
                    leads.extend(scrapling_leads)
                    self.scrapling_results = len(scrapling_leads)
                    print(f"✅ Scrapling found {len(scrapling_leads)} leads")
            except Exception as e:
                print(f"⚠️ Scrapling lead generation failed: {e}")
        
        # Step 2: Use Tavily API (primary fallback)
        if len(leads) < 20:
            print(f"\n📊 Step 2: Using Tavily API for additional leads ({20 - len(leads)} needed)...")
            
            for query in queries:
                if len(leads) >= 30:
                    break
                
                print(f"  🔍 Searching: {query}")
                results = await self.search_tavily(query)
                
                for result in results:
                    if len(leads) >= 30:
                        break
                    
                    # Extract basic info
                    company_info = self.extract_company_info(result)
                    
                    # Skip if no URL or already exists
                    if not company_info["url"] or any(l.get("url") == company_info["url"] for l in leads):
                        continue
                    
                    # Estimate employees
                    employees = self.estimate_employees(
                        company_info["description"],
                        result.get("title", "")
                    )
                    
                    # Classify industry
                    industry = self.classify_industry(
                        f"{company_info['company_name']} {company_info['description']}"
                    )
                    
                    # Calculate savings
                    savings = self.calculate_savings(employees)
                    
                    # Calculate lead score
                    lead_score = self.calculate_lead_score(employees, industry, True)
                    
                    # Create lead entry
                    lead = {
                        "company_name": company_info["company_name"],
                        "url": company_info["url"],
                        "industry": industry,
                        "estimated_employees": employees,
                        "estimated_opex": savings["estimated_opex"],
                        "potential_savings_range": f"{savings['min_savings']} - {savings['max_savings']}",
                        "average_potential_savings": savings["avg_savings"],
                        "description": company_info["description"][:200] + "..." if len(company_info["description"]) > 200 else company_info["description"],
                        "lead_score": lead_score,
                        "priority": "High" if lead_score >= 70 else "Medium" if lead_score >= 50 else "Low",
                        "source": "Tavily API",
                        "found_at": datetime.now().isoformat()
                    }
                    
                    leads.append(lead)
                    self.api_results += 1
                
                # Small delay between searches
                await asyncio.sleep(0.5)
        
        # Step 3: Use Brave Search API (secondary fallback if needed)
        if len(leads) < 20:
            print(f"\n📊 Step 3: Using Brave Search API for additional leads ({20 - len(leads)} needed)...")
            
            for query in queries[2:]:  # Use different queries
                if len(leads) >= 25:
                    break
                
                print(f"  🔍 Searching: {query}")
                results = await self.search_brave(query)
                
                for result in results:
                    if len(leads) >= 25:
                        break
                    
                    # Extract basic info
                    company_info = self.extract_company_info(result)
                    
                    # Skip if no URL or already exists
                    if not company_info["url"] or any(l.get("url") == company_info["url"] for l in leads):
                        continue
                    
                    # Estimate employees
                    employees = self.estimate_employees(
                        company_info["description"],
                        result.get("title", "")
                    )
                    
                    # Classify industry
                    industry = self.classify_industry(
                        f"{company_info['company_name']} {company_info['description']}"
                    )
                    
                    # Calculate savings
                    savings = self.calculate_savings(employees)
                    
                    # Calculate lead score
                    lead_score = self.calculate_lead_score(employees, industry, True)
                    
                    # Create lead entry
                    lead = {
                        "company_name": company_info["company_name"],
                        "url": company_info["url"],
                        "industry": industry,
                        "estimated_employees": employees,
                        "estimated_opex": savings["estimated_opex"],
                        "potential_savings_range": f"{savings['min_savings']} - {savings['max_savings']}",
                        "average_potential_savings": savings["avg_savings"],
                        "description": company_info["description"][:200] + "..." if len(company_info["description"]) > 200 else company_info["description"],
                        "lead_score": lead_score,
                        "priority": "High" if lead_score >= 70 else "Medium" if lead_score >= 50 else "Low",
                        "source": "Brave Search API",
                        "found_at": datetime.now().isoformat()
                    }
                    
                    leads.append(lead)
                    self.api_results += 1
                
                # Small delay between searches
                await asyncio.sleep(0.5)
        
        return leads
    
    def save_leads(self, leads: list) -> str:
        """Save leads to markdown file."""
        # Create leads directory
        leads_dir = Path("/Users/cubiczan/.openclaw/workspace/leads")
        leads_dir.mkdir(exist_ok=True)
        
        # Generate filename with today's date
        today = datetime.now().strftime("%Y-%m-%d")
        filename = leads_dir / f"daily-leads-{today}.md"
        
        # Sort leads by score
        sorted_leads = sorted(leads, key=lambda x: x["lead_score"], reverse=True)
        
        # Generate markdown content
        content = f"""# Daily Lead Report - {today}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Total Leads: {len(leads)}
High Priority (70+): {sum(1 for l in leads if l["lead_score"] >= 70)}
Medium Priority (50-69): {sum(1 for l in leads if 50 <= l["lead_score"] < 70)}
Low Priority (<50): {sum(1 for l in leads if l["lead_score"] < 50)}

---

## 🔍 Data Source Report

- **Scrapling Used:** {"✅ Yes" if self.scrapling_available else "❌ No"}
- **Scrapling Results:** {self.scrapling_results} leads
- **Traditional API Results:** {self.api_results} leads
- **Total Processing Time:** {(datetime.now() - self.start_time).total_seconds():.1f} seconds

---

## 📊 Top 3 High-Priority Leads

"""
        
        # Add top 3 leads
        for i, lead in enumerate(sorted_leads[:3], 1):
            content += f"""### {i}. {lead["company_name"]}

- **Industry:** {lead["industry"]}
- **Estimated Employees:** {lead["estimated_employees"]}
- **Estimated OPEX:** {lead["estimated_opex"]}
- **Potential Savings:** {lead["potential_savings_range"]}
- **Lead Score:** {lead["lead_score"]}/100
- **Priority:** {lead["priority"]}
- **URL:** {lead["url"]}
- **Source:** {lead["source"]}

"""
        
        content += "---\n\n## 📋 All Leads (Sorted by Score)\n\n"
        
        # Add all leads
        for i, lead in enumerate(sorted_leads, 1):
            content += f"""### {i}. {lead["company_name"]}

- **Industry:** {lead["industry"]}
- **Employees:** {lead["estimated_employees"]}
- **OPEX:** {lead["estimated_opex"]}
- **Savings Potential:** {lead["average_potential_savings"]}
- **Score:** {lead["lead_score"]}/100 ({lead["priority"]})
- **URL:** {lead["url"]}
- **Source:** {lead["source"]}
- **Description:** {lead["description"]}

---
"""
        
        # Write file
        with open(filename, "w") as f:
            f.write(content)
        
        return str(filename)
    
    def generate_discord_report(self, leads: list) -> str:
        """Generate Discord-friendly report."""
        high_priority = [l for l in leads if l["lead_score"] >= 70]
        medium_priority = [l for l in leads if 50 <= l["lead_score"] < 70]
        
        # Sort by score
        sorted_leads = sorted(leads, key=lambda x: x["lead_score"], reverse=True)
        
        processing_time = (datetime.now() - self.start_time).total_seconds()
        
        report = f"""🎯 **Enhanced Lead Gen v2 Complete**

**Results:**
• Total Found: {len(leads)}
• High Priority (70+): {len(high_priority)}
• Medium Priority (50-69): {len(medium_priority)}

**🔍 Data Source Report:**
• Scrapling Used: {"✅ Yes" if self.scrapling_available else "❌ No"}
• Scrapling Results: {self.scrapling_results} leads
• Traditional API Results: {self.api_results} leads
• Processing Time: {processing_time:.1f}s

**🏆 Top 3 Leads:**

"""
        
        for i, lead in enumerate(sorted_leads[:3], 1):
            report += f"""**{i}. {lead["company_name"]}**
• Industry: {lead["industry"]}
• Employees: {lead["estimated_employees"]}
• Potential Savings: {lead["average_potential_savings"]}
• Score: {lead["lead_score"]}/100
• Source: {lead["source"]}

"""
        
        report += f"💾 Full report saved to: `leads/daily-leads-{datetime.now().strftime('%Y-%m-%d')}.md`"
        
        return report


async def main():
    """Main execution."""
    print("=" * 60)
    print("Enhanced Lead Gen v2 - Scrapling-First Approach")
    print("=" * 60)
    
    generator = EnhancedLeadGenV2()
    
    # Try Scrapling first
    await generator.try_scrapling()
    
    # Generate leads
    leads = await generator.generate_leads()
    
    if not leads:
        print("\n❌ No leads generated!")
        return
    
    # Save leads
    filename = generator.save_leads(leads)
    print(f"\n💾 Leads saved to: {filename}")
    
    # Generate Discord report
    discord_report = generator.generate_discord_report(leads)
    print("\n" + "=" * 60)
    print("Discord Report:")
    print("=" * 60)
    print(discord_report)
    
    # Save Discord report for delivery
    report_file = Path("/Users/cubiczan/.openclaw/workspace/discord_report.txt")
    with open(report_file, "w") as f:
        f.write(discord_report)
    
    print(f"\n✅ Discord report saved to: {report_file}")


if __name__ == "__main__":
    asyncio.run(main())
