#!/usr/bin/env python3
"""
Defense Sector Lead Generation - Complete Implementation
Uses Tavily API (primary) with Brave Search fallback
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

# API Keys
TAVILY_API_KEY = "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"
BRAVE_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"

class DefenseLeadGenerator:
    """Generate defense sector leads using Tavily/Brave Search APIs."""
    
    def __init__(self):
        self.tavily_used = False
        self.brave_used = False
        self.start_time = datetime.now()
        self.session = None
        
    async def init_session(self):
        """Initialize aiohttp session."""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def close_session(self):
        """Close aiohttp session."""
        if self.session:
            await self.session.close()
    
    async def search_tavily(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search using Tavily API."""
        await self.init_session()
        
        url = "https://api.tavily.com/search"
        headers = {"Content-Type": "application/json"}
        data = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
            "include_raw_content": False,
            "include_images": False
        }
        
        try:
            async with self.session.post(url, json=data, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    result = await response.json()
                    self.tavily_used = True
                    return result.get("results", [])
                else:
                    print(f"⚠️ Tavily API error: {response.status}")
                    return []
        except Exception as e:
            print(f"❌ Tavily error: {e}")
            return []
    
    async def search_brave(self, query: str, count: int = 10) -> List[Dict[str, Any]]:
        """Search using Brave Search API."""
        await self.init_session()
        
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": BRAVE_API_KEY
        }
        params = {
            "q": query,
            "count": count
        }
        
        try:
            async with self.session.get(url, headers=headers, params=params, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    result = await response.json()
                    self.brave_used = True
                    web_results = result.get("web", {}).get("results", [])
                    # Convert to Tavily-like format
                    return [{
                        "title": r.get("title", ""),
                        "url": r.get("url", ""),
                        "content": r.get("description", ""),
                        "score": 1.0
                    } for r in web_results]
                else:
                    print(f"⚠️ Brave API error: {response.status}")
                    return []
        except Exception as e:
            print(f"❌ Brave error: {e}")
            return []
    
    async def search_with_fallback(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Try Tavily first, fall back to Brave."""
        results = await self.search_tavily(query, max_results)
        
        if not results:
            print(f"  ⚠️ Tavily failed for '{query}', trying Brave...")
            results = await self.search_brave(query, max_results)
        
        return results
    
    def score_defense_company(self, company: Dict[str, Any]) -> int:
        """Score defense company (0-100)."""
        score = 0
        
        title = company.get("title", "").lower()
        content = company.get("content", "").lower()
        url = company.get("url", "").lower()
        combined = f"{title} {content} {url}"
        
        # Sector fit (0-30 points)
        defense_keywords = ["defense", "military", "cybersecurity", "drone", "uav", 
                          "space", "satellite", "surveillance", "autonomous", "ai"]
        sector_score = sum(3 for kw in defense_keywords if kw in combined)
        score += min(sector_score, 30)
        
        # Stage fit (0-20 points) - Look for Series A-C indicators
        stage_keywords = ["series a", "series b", "series c", "funding", "raised",
                        "startup", "early-stage", "growth"]
        if any(kw in combined for kw in stage_keywords):
            score += 20
        elif "venture" in combined or "investment" in combined:
            score += 15
        else:
            score += 10
        
        # Technical depth (0-20 points)
        tech_keywords = ["ai", "machine learning", "autonomous", "sensor", "encryption",
                        "satellite", "platform", "technology", "software"]
        tech_score = sum(2 for kw in tech_keywords if kw in combined)
        score += min(tech_score, 20)
        
        # Integration potential (0-20 points)
        integration_keywords = ["platform", "api", "integration", "solution", "system"]
        if any(kw in combined for kw in integration_keywords):
            score += 20
        else:
            score += 10
        
        # Region match (0-10 points)
        region_keywords = ["usa", "us", "united states", "uk", "united kingdom",
                         "europe", "eu", "germany", "france", "uk"]
        if any(kw in combined for kw in region_keywords):
            score += 10
        else:
            score += 5
        
        return min(score, 100)
    
    def score_pe_vc_fund(self, fund: Dict[str, Any]) -> int:
        """Score PE/VC fund (0-100)."""
        score = 0
        
        title = fund.get("title", "").lower()
        content = fund.get("content", "").lower()
        url = fund.get("url", "").lower()
        combined = f"{title} {content} {url}"
        
        # Defense/drone focus (0-40 points)
        focus_keywords = ["defense", "drone", "aerospace", "autonomous", "security",
                        "surveillance", "military", "uav", "dual-use"]
        focus_score = sum(4 for kw in focus_keywords if kw in combined)
        score += min(focus_score, 40)
        
        # Region match (0-20 points) - Asia/India focus
        region_keywords = ["india", "singapore", "japan", "korea", "taiwan",
                         "southeast asia", "middle east", "dubai", "abu dhabi"]
        if any(kw in combined for kw in region_keywords):
            score += 20
        else:
            score += 5
        
        # Portfolio fit (0-20 points)
        portfolio_keywords = ["portfolio", "investment", "fund", "capital", "ventures"]
        if any(kw in combined for kw in portfolio_keywords):
            score += 20
        else:
            score += 10
        
        # Fund size/stage (0-20 points)
        stage_keywords = ["early stage", "growth", "series a", "series b", "venture"]
        if any(kw in combined for kw in stage_keywords):
            score += 20
        elif "pe" in combined or "private equity" in combined:
            score += 15
        else:
            score += 10
        
        # Exclude China
        if "china" in combined or "chinese" in combined:
            score = 0
        
        return min(score, 100)
    
    async def find_defense_companies(self) -> List[Dict[str, Any]]:
        """Find defense companies in US/UK/EU."""
        print("📋 Part 1: Searching for Defense Companies (US/UK/EU)")
        print("-" * 60)
        
        search_queries = [
            "defense technology companies Series A Series B funding US UK EU",
            "cybersecurity defense military contracts startups",
            "drone UAV anti-drone technology companies funding",
            "space defense satellite technology companies investment",
            "AI machine learning military defense applications companies",
            "autonomous systems defense companies Series A",
            "counter-UAS C-UAS technology companies funding"
        ]
        
        all_companies = []
        seen_urls = set()
        
        for query in search_queries:
            print(f"🔍 Searching: {query[:60]}...")
            results = await self.search_with_fallback(query, max_results=8)
            
            for result in results:
                url = result.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    
                    # Score the company
                    score = self.score_defense_company(result)
                    
                    if score > 0:  # Exclude China-related
                        company = {
                            "title": result.get("title", ""),
                            "url": url,
                            "description": result.get("content", ""),
                            "score": score,
                            "priority": "High" if score >= 70 else "Medium" if score >= 50 else "Low",
                            "source": "Tavily" if self.tavily_used else "Brave"
                        }
                        all_companies.append(company)
        
        # Sort by score
        all_companies.sort(key=lambda x: x["score"], reverse=True)
        
        # Take top 10
        top_companies = all_companies[:10]
        
        print(f"✅ Found {len(all_companies)} companies, keeping top {len(top_companies)}")
        return top_companies
    
    async def find_pe_vc_funds(self) -> List[Dict[str, Any]]:
        """Find PE/VC funds in Asia/India."""
        print("\n📋 Part 2: Searching for PE/VC Funds (Asia/India)")
        print("-" * 60)
        
        search_queries = [
            "venture capital defense technology India Singapore",
            "private equity drone aerospace investment Asia",
            "VC fund autonomous systems security Japan Korea",
            "defense tech investors Southeast Asia Middle East",
            "drone technology investment fund Taiwan India"
        ]
        
        all_funds = []
        seen_urls = set()
        
        for query in search_queries:
            print(f"🔍 Searching: {query[:60]}...")
            results = await self.search_with_fallback(query, max_results=8)
            
            for result in results:
                url = result.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    
                    # Score the fund
                    score = self.score_pe_vc_fund(result)
                    
                    if score > 0:  # Exclude China-related
                        fund = {
                            "title": result.get("title", ""),
                            "url": url,
                            "description": result.get("content", ""),
                            "score": score,
                            "priority": "High" if score >= 70 else "Medium" if score >= 50 else "Low",
                            "source": "Tavily" if self.tavily_used else "Brave"
                        }
                        all_funds.append(fund)
        
        # Sort by score
        all_funds.sort(key=lambda x: x["score"], reverse=True)
        
        # Take top 5
        top_funds = all_funds[:5]
        
        print(f"✅ Found {len(all_funds)} funds, keeping top {len(top_funds)}")
        return top_funds
    
    def save_results(self, companies: List[Dict[str, Any]], funds: List[Dict[str, Any]]):
        """Save results to files."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Create directory
        output_dir = Path("/Users/cubiczan/.openclaw/workspace/defense-leads")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save companies
        companies_file = output_dir / f"daily-companies-{today}.md"
        with open(companies_file, "w") as f:
            f.write(f"# Defense Companies - {today}\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            for i, company in enumerate(companies, 1):
                f.write(f"## {i}. {company['title']}\n\n")
                f.write(f"**Score:** {company['score']}/100 ({company['priority']} Priority)\n\n")
                f.write(f"**URL:** {company['url']}\n\n")
                f.write(f"**Description:** {company['description'][:300]}...\n\n")
                f.write(f"**Source:** {company['source']}\n\n")
                f.write("---\n\n")
        
        print(f"✅ Saved companies to: {companies_file}")
        
        # Save investors
        investors_file = output_dir / f"daily-investors-{today}.md"
        with open(investors_file, "w") as f:
            f.write(f"# PE/VC Investors (Asia/India) - {today}\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            for i, fund in enumerate(funds, 1):
                f.write(f"## {i}. {fund['title']}\n\n")
                f.write(f"**Score:** {fund['score']}/100 ({fund['priority']} Priority)\n\n")
                f.write(f"**URL:** {fund['url']}\n\n")
                f.write(f"**Description:** {fund['description'][:300]}...\n\n")
                f.write(f"**Source:** {fund['source']}\n\n")
                f.write("---\n\n")
        
        print(f"✅ Saved investors to: {investors_file}")
    
    def get_processing_time(self) -> str:
        """Get processing time in seconds."""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        return f"{elapsed:.1f}"
    
    async def run(self):
        """Run the complete lead generation process."""
        print("=" * 60)
        print("🛡️ Defense Sector Lead Generation")
        print("=" * 60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        try:
            # Find defense companies
            companies = await self.find_defense_companies()
            
            # Reset API flags for funds search
            self.tavily_used = False
            self.brave_used = False
            
            # Find PE/VC funds
            funds = await self.find_pe_vc_funds()
            
            # Save results
            print("\n💾 Saving Results...")
            print("-" * 60)
            self.save_results(companies, funds)
            
            # Generate summary
            print("\n" + "=" * 60)
            print("📊 Results Summary")
            print("=" * 60)
            
            high_priority_companies = len([c for c in companies if c["priority"] == "High"])
            defense_focused_funds = len([f for f in funds if f["score"] >= 60])
            
            summary = {
                "companies": {
                    "total": len(companies),
                    "high_priority": high_priority_companies,
                    "top_3": [
                        {"name": c["title"][:50], "score": c["score"]}
                        for c in companies[:3]
                    ]
                },
                "investors": {
                    "total": len(funds),
                    "defense_focused": defense_focused_funds,
                    "top_3": [
                        {"name": f["title"][:50], "score": f["score"]}
                        for f in funds[:3]
                    ]
                },
                "data_source": {
                    "scrapling_used": False,
                    "scrapling_results": 0,
                    "tavily_used": self.tavily_used,
                    "brave_used": self.brave_used,
                    "processing_time": self.get_processing_time()
                }
            }
            
            print(json.dumps(summary, indent=2))
            
            return {
                "companies": companies,
                "funds": funds,
                "summary": summary
            }
            
        finally:
            await self.close_session()

async def main():
    """Main entry point."""
    generator = DefenseLeadGenerator()
    results = await generator.run()
    return results

if __name__ == "__main__":
    results = asyncio.run(main())
