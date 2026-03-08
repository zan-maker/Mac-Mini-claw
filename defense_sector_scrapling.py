#!/usr/bin/env python3
"""
Defense Sector Lead Gen - Scrapling-First Enhanced Approach
Runs daily defense company and PE/VC fund searches using Scrapling first, then falls back to APIs.
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import List, Dict, Any

# Add Scrapling integration to path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# Try importing Scrapling
try:
    from cron_integration import ScraplingCronIntegration
    SCRAPLING_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Scrapling import failed: {e}")
    SCRAPLING_AVAILABLE = False

# API Keys
TAVILY_API_KEY = "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"
BRAVE_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"

class DefenseSectorLeadGen:
    """Defense sector lead generation with Scrapling-first approach."""
    
    def __init__(self):
        self.scrapling = None
        self.scrapling_used = False
        self.scrapling_results = 0
        self.api_results = 0
        self.start_time = datetime.now()
        
    async def initialize_scrapling(self):
        """Try to initialize Scrapling."""
        if not SCRAPLING_AVAILABLE:
            print("❌ Scrapling not available in environment")
            return False
        
        try:
            self.scrapling = ScraplingCronIntegration(stealth_mode=True)
            success = await self.scrapling.initialize()
            if success:
                print("✅ Scrapling initialized successfully")
                return True
            else:
                print("⚠️ Scrapling initialization returned False")
                return False
        except Exception as e:
            print(f"❌ Scrapling initialization failed: {e}")
            return False
    
    async def search_defense_companies_scrapling(self) -> List[Dict]:
        """Search for defense companies using Scrapling."""
        if not self.scrapling:
            return []
        
        print("\n🔍 Attempting Scrapling search for defense companies...")
        
        search_terms = [
            "defense technology companies US UK EU",
            "cybersecurity military contractors",
            "counter-drone technology C-UAS",
            "space defense technology startups",
            "military AI machine learning defense",
            "autonomous systems defense",
            "defense data analytics ISR"
        ]
        
        try:
            companies = await self.scrapling.scrape_defense_companies(search_terms)
            if companies:
                self.scrapling_used = True
                self.scrapling_results = len(companies)
                print(f"✅ Scrapling found {len(companies)} defense companies")
                return companies
            else:
                print("⚠️ Scrapling returned no results")
                return []
        except Exception as e:
            print(f"❌ Scrapling search failed: {e}")
            return []
    
    async def search_defense_companies_api(self) -> List[Dict]:
        """Search for defense companies using Tavily/Brave APIs."""
        print("\n🔍 Using API search for defense companies...")
        
        # Try Tavily first
        companies = await self._search_tavily_defense()
        
        if not companies:
            print("⚠️ Tavily returned no results, trying Brave Search...")
            companies = await self._search_brave_defense()
        
        self.api_results = len(companies)
        return companies
    
    async def _search_tavily_defense(self) -> List[Dict]:
        """Search using Tavily API."""
        import aiohttp
        
        queries = [
            "defense technology companies Series A B C funding US UK EU",
            "cybersecurity defense contractors early stage startups",
            "counter-drone C-UAS technology companies Series A",
            "space defense satellite technology startups",
            "military AI machine learning defense companies funding"
        ]
        
        companies = []
        
        try:
            async with aiohttp.ClientSession() as session:
                for query in queries:
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
                            results = data.get("results", [])
                            
                            for result in results:
                                company = {
                                    "name": result.get("title", "Unknown"),
                                    "url": result.get("url", ""),
                                    "description": result.get("content", ""),
                                    "source": "Tavily",
                                    "score": 0
                                }
                                company["score"] = self._score_defense_company(company)
                                companies.append(company)
                        else:
                            print(f"⚠️ Tavily API error: {response.status}")
            
            print(f"✅ Tavily found {len(companies)} results")
            return companies
            
        except Exception as e:
            print(f"❌ Tavily search failed: {e}")
            return []
    
    async def _search_brave_defense(self) -> List[Dict]:
        """Search using Brave Search API."""
        import aiohttp
        
        queries = [
            "defense technology startups Series A B C US UK EU 2024 2025",
            "cybersecurity military contractors funding",
            "counter-drone technology C-UAS startups",
            "space defense technology companies investment",
            "AI defense military machine learning startups"
        ]
        
        companies = []
        
        try:
            async with aiohttp.ClientSession() as session:
                for query in queries:
                    headers = {
                        "X-Subscription-Token": BRAVE_API_KEY,
                        "Accept": "application/json"
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
                            results = data.get("web", {}).get("results", [])
                            
                            for result in results:
                                company = {
                                    "name": result.get("title", "Unknown"),
                                    "url": result.get("url", ""),
                                    "description": result.get("description", ""),
                                    "source": "Brave Search",
                                    "score": 0
                                }
                                company["score"] = self._score_defense_company(company)
                                companies.append(company)
                        else:
                            print(f"⚠️ Brave API error: {response.status}")
            
            print(f"✅ Brave Search found {len(companies)} results")
            return companies
            
        except Exception as e:
            print(f"❌ Brave search failed: {e}")
            return []
    
    def _score_defense_company(self, company: Dict) -> int:
        """Score defense company 0-100."""
        score = 0
        
        # Sector fit (30 pts)
        text = f"{company.get('name', '')} {company.get('description', '')}".lower()
        defense_keywords = {
            "defense": 6, "military": 6, "cyber": 5, "security": 5,
            "drone": 5, "uav": 5, "c-uas": 6, "space": 4, "satellite": 4,
            "autonomous": 4, "ai": 3, "machine learning": 3, "sensor": 3,
            "isr": 5, "surveillance": 4, "encryption": 4
        }
        
        for keyword, points in defense_keywords.items():
            if keyword in text:
                score += points
        
        score = min(score, 30)  # Cap at 30
        
        # Stage indicators (20 pts)
        stage_keywords = ["series a", "series b", "series c", "funding", "raised", "investment", "startup"]
        stage_score = sum(4 for keyword in stage_keywords if keyword in text)
        score += min(stage_score, 20)
        
        # Technical depth (20 pts)
        tech_keywords = ["ai", "ml", "autonomous", "sensor", "satellite", "encryption", "platform", "system"]
        tech_score = sum(3 for keyword in tech_keywords if keyword in text)
        score += min(tech_score, 20)
        
        # Region match (10 pts)
        region_keywords = ["us", "united states", "uk", "united kingdom", "europe", "eu", "germany", "france", "uk"]
        if any(keyword in text for keyword in region_keywords):
            score += 10
        
        # Integration potential (20 pts)
        integration_keywords = ["platform", "api", "integration", "system", "solution"]
        integration_score = sum(4 for keyword in integration_keywords if keyword in text)
        score += min(integration_score, 20)
        
        return min(score, 100)
    
    async def search_pe_vc_funds(self) -> List[Dict]:
        """Search for PE/VC funds in Asia/India."""
        print("\n🔍 Searching for PE/VC funds in Asia/India...")
        
        # Use API search (Scrapling not set up for this yet)
        funds = await self._search_funds_api()
        self.api_results += len(funds)
        return funds
    
    async def _search_funds_api(self) -> List[Dict]:
        """Search for PE/VC funds using APIs."""
        import aiohttp
        
        queries = [
            "private equity defense technology Asia India Singapore",
            "venture capital drone aerospace investment Japan Korea",
            "defense tech fund Southeast Asia Middle East",
            "military technology investment fund Taiwan India",
            "dual-use technology PE VC fund Asia"
        ]
        
        funds = []
        
        try:
            async with aiohttp.ClientSession() as session:
                for query in queries:
                    # Try Tavily first
                    payload = {
                        "api_key": TAVILY_API_KEY,
                        "query": query,
                        "search_depth": "advanced",
                        "max_results": 3
                    }
                    
                    async with session.post(
                        "https://api.tavily.com/search",
                        json=payload
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            results = data.get("results", [])
                            
                            for result in results:
                                fund = {
                                    "name": result.get("title", "Unknown"),
                                    "url": result.get("url", ""),
                                    "description": result.get("content", ""),
                                    "source": "Tavily",
                                    "score": 0
                                }
                                fund["score"] = self._score_pe_fund(fund)
                                funds.append(fund)
            
            # Deduplicate by name
            seen = set()
            unique_funds = []
            for fund in funds:
                if fund["name"] not in seen:
                    seen.add(fund["name"])
                    unique_funds.append(fund)
            
            print(f"✅ Found {len(unique_funds)} PE/VC funds")
            return unique_funds
            
        except Exception as e:
            print(f"❌ Fund search failed: {e}")
            return []
    
    def _score_pe_fund(self, fund: Dict) -> int:
        """Score PE/VC fund 0-100."""
        score = 0
        
        text = f"{fund.get('name', '')} {fund.get('description', '')}".lower()
        
        # Defense/drone focus (40 pts)
        defense_keywords = {
            "defense": 10, "military": 8, "drone": 8, "uav": 8,
            "aerospace": 7, "security": 6, "surveillance": 6,
            "autonomous": 5, "dual-use": 10
        }
        
        for keyword, points in defense_keywords.items():
            if keyword in text:
                score += points
        
        score = min(score, 40)
        
        # Region match (20 pts)
        region_keywords = {
            "india": 5, "singapore": 5, "japan": 5, "korea": 5,
            "taiwan": 5, "southeast asia": 5, "middle east": 4
        }
        
        for keyword, points in region_keywords.items():
            if keyword in text:
                score += points
        
        score = min(score, 20)
        
        # Portfolio fit (20 pts)
        portfolio_keywords = ["portfolio", "investment", "startup", "technology", "innovation"]
        portfolio_score = sum(4 for keyword in portfolio_keywords if keyword in text)
        score += min(portfolio_score, 20)
        
        # Fund size/stage (20 pts)
        fund_keywords = ["fund", "capital", "venture", "private equity", "growth", "series"]
        fund_score = sum(4 for keyword in fund_keywords if keyword in text)
        score += min(fund_score, 20)
        
        return min(score, 100)
    
    def save_results(self, companies: List[Dict], funds: List[Dict]):
        """Save results to files."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        # Create directory if needed
        os.makedirs("/Users/cubiczan/.openclaw/workspace/defense-leads", exist_ok=True)
        
        # Save companies
        companies_file = f"/Users/cubiczan/.openclaw/workspace/defense-leads/daily-companies-{date_str}.md"
        with open(companies_file, "w") as f:
            f.write(f"# Defense Companies - {date_str}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Leads:** {len(companies)}\n")
            f.write(f"**High Priority (70+):** {len([c for c in companies if c['score'] >= 70])}\n\n")
            
            # Sort by score
            sorted_companies = sorted(companies, key=lambda x: x['score'], reverse=True)
            
            for i, company in enumerate(sorted_companies, 1):
                priority = "🟢 High" if company['score'] >= 70 else "🟡 Medium" if company['score'] >= 50 else "🔴 Low"
                f.write(f"## {i}. {company['name']}\n")
                f.write(f"**Score:** {company['score']}/100 {priority}\n")
                f.write(f"**URL:** {company['url']}\n")
                f.write(f"**Source:** {company.get('source', 'Unknown')}\n")
                f.write(f"**Description:** {company['description'][:300]}...\n\n")
        
        print(f"✅ Saved companies to {companies_file}")
        
        # Save funds
        funds_file = f"/Users/cubiczan/.openclaw/workspace/defense-leads/daily-investors-{date_str}.md"
        with open(funds_file, "w") as f:
            f.write(f"# PE/VC Funds (Asia/India) - {date_str}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Funds:** {len(funds)}\n")
            f.write(f"**Defense-Focused (70+):** {len([f for f in funds if f['score'] >= 70])}\n\n")
            
            # Sort by score
            sorted_funds = sorted(funds, key=lambda x: x['score'], reverse=True)
            
            for i, fund in enumerate(sorted_funds, 1):
                priority = "🟢 High" if fund['score'] >= 70 else "🟡 Medium" if fund['score'] >= 50 else "🔴 Low"
                f.write(f"## {i}. {fund['name']}\n")
                f.write(f"**Score:** {fund['score']}/100 {priority}\n")
                f.write(f"**URL:** {fund['url']}\n")
                f.write(f"**Source:** {fund.get('source', 'Unknown')}\n")
                f.write(f"**Description:** {fund['description'][:300]}...\n\n")
        
        print(f"✅ Saved funds to {funds_file}")
    
    def generate_discord_report(self, companies: List[Dict], funds: List[Dict]) -> str:
        """Generate Discord report."""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        # Sort and get top companies
        sorted_companies = sorted(companies, key=lambda x: x['score'], reverse=True)
        top_companies = sorted_companies[:3]
        
        # Sort and get top funds
        sorted_funds = sorted(funds, key=lambda x: x['score'], reverse=True)
        top_funds = sorted_funds[:3]
        
        report = f"""🛡️ **Defense Sector Report (Scrapling-Enhanced)**

## Companies (US/UK/EU)
- **Identified:** {len(companies)}
- **High Priority (70+):** {len([c for c in companies if c['score'] >= 70])}
- **Top 3:**
"""
        
        for company in top_companies:
            name = company['name'][:40] + "..." if len(company['name']) > 40 else company['name']
            report += f"  • {name} - Score: {company['score']}\n"
        
        report += f"""
## Investors (Asia/India)
- **PE/VC funds:** {len(funds)}
- **Defense-focused:** {len([f for f in funds if f['score'] >= 70])}
- **Top 3:**
"""
        
        for fund in top_funds:
            name = fund['name'][:40] + "..." if len(fund['name']) > 40 else fund['name']
            report += f"  • {name} - Score: {fund['score']}\n"
        
        report += f"""
🔍 **Data Source:**
- Scrapling Used: {'✅ Yes' if self.scrapling_used else '❌ No'}
- Scrapling Results: {self.scrapling_results}
- Traditional API Results: {self.api_results}
- Processing Time: {elapsed:.1f} seconds

📊 Files saved to `/workspace/defense-leads/`
"""
        
        return report

async def main():
    """Main execution."""
    print("=" * 60)
    print("Defense Sector Lead Generation - Scrapling-First Enhanced")
    print("=" * 60)
    
    lead_gen = DefenseSectorLeadGen()
    
    # Step 1: Try Scrapling first
    scrapling_initialized = await lead_gen.initialize_scrapling()
    
    companies = []
    
    if scrapling_initialized:
        # Try Scrapling for defense companies
        companies = await lead_gen.search_defense_companies_scrapling()
    
    # Step 2: Fall back to APIs if needed
    if not companies:
        print("\n⚠️ Falling back to traditional APIs...")
        companies = await lead_gen.search_defense_companies_api()
    
    # Step 3: Search for PE/VC funds
    funds = await lead_gen.search_pe_vc_funds()
    
    # Step 4: Save results
    if companies or funds:
        lead_gen.save_results(companies, funds)
    
    # Step 5: Generate Discord report
    report = lead_gen.generate_discord_report(companies, funds)
    
    print("\n" + "=" * 60)
    print("DISCORD REPORT:")
    print("=" * 60)
    print(report)
    
    # Save report to file for delivery
    with open("/Users/cubiczan/.openclaw/workspace/defense_report.txt", "w") as f:
        f.write(report)
    
    print("\n✅ Report saved to defense_report.txt")

if __name__ == "__main__":
    asyncio.run(main())
