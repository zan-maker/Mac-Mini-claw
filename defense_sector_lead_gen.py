#!/usr/bin/env python3
"""
Defense Sector Lead Generation - Scrapling-First Enhanced
Cron Job: Daily defense company and PE/VC fund identification
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any
import aiohttp

# Try Scrapling first
SCRAPLING_AVAILABLE = False
try:
    sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')
    from cron_integration import ScraplingCronIntegration
    SCRAPLING_AVAILABLE = True
    print("✅ Scrapling integration available")
except ImportError as e:
    print(f"⚠️ Scrapling not available: {e}")

# API Keys
TAVILY_API_KEY = "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"
BRAVE_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"

class DefenseSectorLeadGen:
    """Generate defense sector leads using Scrapling-first approach."""
    
    def __init__(self):
        self.scrapling = None
        self.scrapling_used = False
        self.scrapling_results = 0
        self.api_results = 0
        self.start_time = datetime.now()
        
    async def run(self):
        """Main execution."""
        print("🚀 Defense Sector Lead Generation - Scrapling-First")
        print(f"⏰ Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Step 1: Try Scrapling first
        companies = await self.try_scrapling_first()
        
        # Step 2: Get PE/VC funds (using APIs - Scrapling doesn't have search capability yet)
        investors = await self.find_pe_vc_funds()
        
        # Step 3: Save results
        await self.save_results(companies, investors)
        
        # Step 4: Report to Discord
        await self.report_to_discord(companies, investors)
        
        # Summary
        elapsed = (datetime.now() - self.start_time).total_seconds()
        print(f"\n✅ Complete in {elapsed:.1f} seconds")
        print(f"   Companies: {len(companies)}")
        print(f"   Investors: {len(investors)}")
        
    async def try_scrapling_first(self) -> List[Dict[str, Any]]:
        """Try Scrapling integration first, fall back to APIs."""
        print("\n📡 Step 1: Trying Scrapling Integration...")
        
        if not SCRAPLING_AVAILABLE:
            print("   ⚠️ Scrapling not available, using APIs")
            return await self.find_defense_companies_with_apis()
        
        try:
            # Initialize Scrapling
            self.scrapling = ScraplingCronIntegration(stealth_mode=True)
            success = await self.scrapling.initialize()
            
            if not success:
                print("   ⚠️ Scrapling initialization failed, using APIs")
                return await self.find_defense_companies_with_apis()
            
            print("   ✅ Scrapling initialized successfully")
            
            # Search for defense companies
            search_terms = [
                "defense technology companies Series A B C funding",
                "cybersecurity defense contractors early stage",
                "drone technology anti-UAS military startups",
                "space defense satellites surveillance companies",
                "military AI machine learning defense startups"
            ]
            
            companies = await self.scrapling.scrape_defense_companies(search_terms)
            
            if companies and len(companies) > 0:
                self.scrapling_used = True
                self.scrapling_results = len(companies)
                print(f"   ✅ Scrapling found {len(companies)} companies")
                
                # Enrich with additional data from APIs
                print("   🔍 Enriching with API data...")
                enriched = await self.enrich_with_apis(companies)
                return enriched
            else:
                print("   ⚠️ Scrapling returned no results, using APIs")
                return await self.find_defense_companies_with_apis()
                
        except Exception as e:
            print(f"   ❌ Scrapling error: {e}")
            return await self.find_defense_companies_with_apis()
    
    async def enrich_with_apis(self, companies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrich Scrapling results with API data."""
        # For now, return Scrapling results as-is
        # In production, we'd enrich each company with additional data
        return companies
    
    async def find_defense_companies_with_apis(self) -> List[Dict[str, Any]]:
        """Find defense companies using Tavily/Brave APIs."""
        print("\n📡 Step 2: Using Traditional APIs...")
        
        all_companies = []
        
        # Search queries for different defense sectors
        queries = [
            "defense technology companies US UK EU Series A B C funding 2024 2025",
            "cybersecurity defense military startups early stage investment",
            "counter-drone C-UAS anti-drone technology companies",
            "space defense satellite surveillance companies funding",
            "military AI machine learning ISR defense startups"
        ]
        
        # Try Tavily first
        print("\n🔍 Searching with Tavily API (primary)...")
        for query in queries:
            try:
                results = await self.search_tavily(query)
                if results:
                    companies = self.parse_defense_companies(results)
                    all_companies.extend(companies)
                    print(f"   ✅ Found {len(companies)} companies for: {query[:50]}...")
                await asyncio.sleep(0.5)  # Rate limiting
            except Exception as e:
                print(f"   ❌ Tavily error: {e}")
        
        # If Tavily failed or returned few results, try Brave
        if len(all_companies) < 5:
            print("\n🔍 Supplementing with Brave Search API (fallback)...")
            for query in queries[:2]:  # Only top 2 queries
                try:
                    results = await self.search_brave(query)
                    if results:
                        companies = self.parse_defense_companies(results)
                        all_companies.extend(companies)
                        print(f"   ✅ Found {len(companies)} additional companies")
                    await asyncio.sleep(0.5)
                except Exception as e:
                    print(f"   ❌ Brave error: {e}")
        
        # Deduplicate and score
        unique_companies = self.deduplicate_companies(all_companies)
        scored_companies = [self.score_defense_company(c) for c in unique_companies]
        sorted_companies = sorted(scored_companies, key=lambda x: x['score'], reverse=True)
        
        self.api_results = len(sorted_companies)
        
        return sorted_companies[:10]  # Return top 10
    
    async def search_tavily(self, query: str) -> List[Dict[str, Any]]:
        """Search using Tavily API."""
        url = "https://api.tavily.com/search"
        
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "include_answer": False,
            "include_raw_content": False,
            "max_results": 10
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("results", [])
                else:
                    raise Exception(f"Tavily API error: {response.status}")
    
    async def search_brave(self, query: str) -> List[Dict[str, Any]]:
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
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("web", {}).get("results", [])
                else:
                    raise Exception(f"Brave API error: {response.status}")
    
    def parse_defense_companies(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse search results into company data."""
        companies = []
        
        for result in results:
            # Extract company info from search result
            company = {
                "name": result.get("title", "").split(" - ")[0].split(" | ")[0],
                "url": result.get("url", ""),
                "description": result.get("description", ""),
                "source": result.get("source", "unknown"),
                "found_date": datetime.now().strftime("%Y-%m-%d")
            }
            
            # Basic validation
            if company["name"] and company["url"]:
                companies.append(company)
        
        return companies
    
    def deduplicate_companies(self, companies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate companies."""
        seen = set()
        unique = []
        
        for company in companies:
            # Use URL as unique identifier
            url = company.get("url", "")
            if url and url not in seen:
                seen.add(url)
                unique.append(company)
        
        return unique
    
    def score_defense_company(self, company: Dict[str, Any]) -> Dict[str, Any]:
        """Score defense company (0-100)."""
        score = 0
        
        # Sector fit (0-30 points)
        text = f"{company.get('name', '')} {company.get('description', '')}".lower()
        defense_keywords = {
            "defense": 5, "military": 5, "cyber": 4, "security": 4,
            "drone": 5, "uas": 5, "space": 4, "satellite": 4,
            "ai": 3, "autonomous": 4, "surveillance": 4, "isr": 5
        }
        
        sector_score = sum(points for keyword, points in defense_keywords.items() 
                          if keyword in text)
        score += min(sector_score, 30)
        
        # Stage fit (0-20 points) - looking for early-mid stage
        stage_keywords = ["series a", "series b", "series c", "funding", "startup", "early stage"]
        stage_score = sum(4 for keyword in stage_keywords if keyword in text)
        score += min(stage_score, 20)
        
        # Technical depth (0-20 points)
        tech_keywords = ["ai", "machine learning", "autonomous", "sensor", "encryption", 
                        "satellite", "drone", "cyber", "platform"]
        tech_score = sum(2 for keyword in tech_keywords if keyword in text)
        score += min(tech_score, 20)
        
        # Integration potential (0-20 points)
        integration_keywords = ["platform", "api", "integration", "system", "solution"]
        integration_score = sum(4 for keyword in integration_keywords if keyword in text)
        score += min(integration_score, 20)
        
        # Region match (0-10 points)
        region_keywords = ["us", "usa", "united states", "uk", "united kingdom", 
                          "europe", "eu", "germany", "france", "uk"]
        if any(keyword in text for keyword in region_keywords):
            score += 10
        
        company["score"] = min(score, 100)
        company["priority"] = "High" if score >= 70 else "Medium" if score >= 50 else "Low"
        
        return company
    
    async def find_pe_vc_funds(self) -> List[Dict[str, Any]]:
        """Find PE/VC funds in Asia/India focusing on defense."""
        print("\n📡 Step 3: Finding PE/VC Funds in Asia/India...")
        
        all_funds = []
        
        # Search queries for PE/VC funds
        queries = [
            "private equity venture capital defense technology India Singapore",
            "VC fund drone aerospace investment Asia Japan Korea",
            "defense tech investor autonomous systems Southeast Asia",
            "aerospace defense fund Middle East UAE Saudi Arabia",
            "dual-use technology investor Taiwan India venture capital"
        ]
        
        # Try Tavily first
        print("\n🔍 Searching with Tavily API...")
        for query in queries:
            try:
                results = await self.search_tavily(query)
                if results:
                    funds = self.parse_funds(results)
                    all_funds.extend(funds)
                    print(f"   ✅ Found {len(funds)} funds")
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        # Deduplicate and score
        unique_funds = self.deduplicate_funds(all_funds)
        scored_funds = [self.score_fund(f) for f in unique_funds]
        sorted_funds = sorted(scored_funds, key=lambda x: x['score'], reverse=True)
        
        return sorted_funds[:5]  # Return top 5
    
    def parse_funds(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse search results into fund data."""
        funds = []
        
        for result in results:
            fund = {
                "name": result.get("title", "").split(" - ")[0].split(" | ")[0],
                "url": result.get("url", ""),
                "description": result.get("description", ""),
                "source": "Tavily",
                "found_date": datetime.now().strftime("%Y-%m-%d")
            }
            
            if fund["name"] and fund["url"]:
                funds.append(fund)
        
        return funds
    
    def deduplicate_funds(self, funds: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate funds."""
        seen = set()
        unique = []
        
        for fund in funds:
            url = fund.get("url", "")
            if url and url not in seen:
                seen.add(url)
                unique.append(fund)
        
        return unique
    
    def score_fund(self, fund: Dict[str, Any]) -> Dict[str, Any]:
        """Score PE/VC fund (0-100)."""
        score = 0
        
        text = f"{fund.get('name', '')} {fund.get('description', '')}".lower()
        
        # Defense/drone focus (0-40 points)
        defense_keywords = ["defense", "military", "aerospace", "drone", "uav", 
                          "autonomous", "security", "surveillance", "dual-use"]
        defense_score = sum(5 for keyword in defense_keywords if keyword in text)
        score += min(defense_score, 40)
        
        # Region match (0-20 points)
        region_keywords = ["india", "singapore", "japan", "korea", "taiwan", 
                          "southeast asia", "middle east", "uae", "saudi"]
        if any(keyword in text for keyword in region_keywords):
            score += 20
        
        # Portfolio fit (0-20 points)
        portfolio_keywords = ["portfolio", "investment", "startup", "technology", 
                            "innovation", "growth"]
        portfolio_score = sum(3 for keyword in portfolio_keywords if keyword in text)
        score += min(portfolio_score, 20)
        
        # Fund size/stage (0-20 points)
        stage_keywords = ["series a", "series b", "early stage", "growth", 
                         "venture", "private equity"]
        stage_score = sum(4 for keyword in stage_keywords if keyword in text)
        score += min(stage_score, 20)
        
        # Exclude China
        if "china" in text or "chinese" in text:
            score = 0
        
        fund["score"] = min(score, 100)
        fund["priority"] = "High" if score >= 70 else "Medium" if score >= 50 else "Low"
        
        return fund
    
    async def save_results(self, companies: List[Dict[str, Any]], funds: List[Dict[str, Any]]):
        """Save results to files."""
        print("\n💾 Saving results...")
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Create directory if needed
        os.makedirs("/Users/cubiczan/.openclaw/workspace/defense-leads", exist_ok=True)
        
        # Save companies
        companies_file = f"/Users/cubiczan/.openclaw/workspace/defense-leads/daily-companies-{today}.md"
        with open(companies_file, 'w') as f:
            f.write(f"# Defense Companies - {today}\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Leads: {len(companies)}\n")
            f.write(f"High Priority: {len([c for c in companies if c.get('priority') == 'High'])}\n\n")
            f.write("---\n\n")
            
            for i, company in enumerate(companies, 1):
                f.write(f"## {i}. {company.get('name', 'Unknown')}\n\n")
                f.write(f"**Score:** {company.get('score', 0)}/100\n")
                f.write(f"**Priority:** {company.get('priority', 'Low')}\n")
                f.write(f"**URL:** {company.get('url', 'N/A')}\n")
                f.write(f"**Description:** {company.get('description', 'N/A')}\n\n")
                f.write("---\n\n")
        
        print(f"   ✅ Saved {len(companies)} companies to {companies_file}")
        
        # Save investors
        investors_file = f"/Users/cubiczan/.openclaw/workspace/defense-leads/daily-investors-{today}.md"
        with open(investors_file, 'w') as f:
            f.write(f"# PE/VC Investors - {today}\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Funds: {len(funds)}\n")
            f.write(f"High Priority: {len([f for f in funds if f.get('priority') == 'High'])}\n\n")
            f.write("---\n\n")
            
            for i, fund in enumerate(funds, 1):
                f.write(f"## {i}. {fund.get('name', 'Unknown')}\n\n")
                f.write(f"**Score:** {fund.get('score', 0)}/100\n")
                f.write(f"**Priority:** {fund.get('priority', 'Low')}\n")
                f.write(f"**URL:** {fund.get('url', 'N/A')}\n")
                f.write(f"**Description:** {fund.get('description', 'N/A')}\n\n")
                f.write("---\n\n")
        
        print(f"   ✅ Saved {len(funds)} investors to {investors_file}")
    
    async def report_to_discord(self, companies: List[Dict[str, Any]], funds: List[Dict[str, Any]]):
        """Report results to Discord."""
        print("\n📤 Preparing Discord report...")
        
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        # Count priorities
        high_priority_companies = [c for c in companies if c.get('priority') == 'High']
        high_priority_funds = [f for f in funds if f.get('priority') == 'High']
        
        # Top 3 companies
        top_companies = companies[:3]
        top_company_lines = []
        for c in top_companies:
            name = c.get('name', 'Unknown')[:30]
            score = c.get('score', 0)
            desc = c.get('description', '')[:50]
            top_company_lines.append(f"• {name} - Score: {score}")
        
        # Top 3 funds
        top_funds = funds[:3]
        top_fund_lines = []
        for f in top_funds:
            name = f.get('name', 'Unknown')[:30]
            score = f.get('score', 0)
            region = "Asia" if any(r in f.get('description', '').lower() 
                                  for r in ['india', 'singapore', 'japan', 'korea']) else "Other"
            top_fund_lines.append(f"• {name} - {region} - Score: {score}")
        
        # Build report
        report = f"""🛡️ **Defense Sector Report (Scrapling-Enhanced)**

## Companies (US/UK/EU)
• Identified: {len(companies)}
• High priority (70+): {len(high_priority_companies)}
• Top 3:
{chr(10).join(top_company_lines) if top_company_lines else '• No companies found'}

## Investors (Asia/India)
• PE/VC funds: {len(funds)}
• Defense-focused: {len(high_priority_funds)}
• Top 3:
{chr(10).join(top_fund_lines) if top_fund_lines else '• No funds found'}

🔍 **Data Source:**
• Scrapling Used: {'✅ Yes' if self.scrapling_used else '❌ No'}
• Scrapling Results: {self.scrapling_results}
• Traditional API Results: {self.api_results}
• Processing Time: {elapsed:.1f} seconds

---
📁 Full reports saved to `/workspace/defense-leads/`"""
        
        # Save report for Discord delivery
        report_file = "/Users/cubiczan/.openclaw/workspace/defense-leads/discord-report.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"   ✅ Discord report saved to {report_file}")
        print("\n" + "="*60)
        print(report)
        print("="*60)


async def main():
    """Run defense sector lead generation."""
    gen = DefenseSectorLeadGen()
    await gen.run()


if __name__ == "__main__":
    asyncio.run(main())
