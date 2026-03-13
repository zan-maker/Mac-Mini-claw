#!/usr/bin/env python3
"""
Enhanced Lead Gen v2 - Scrapling-First Approach
Tries Scrapling first, falls back to Tavily, then Brave Search
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Setup paths
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# Try to import Scrapling
SCRAPLING_AVAILABLE = False
try:
    from cron_integration import ScraplingCronIntegration
    SCRAPLING_AVAILABLE = True
    print("✅ Scrapling module available")
except ImportError as e:
    print(f"⚠️ Scrapling not available: {e}")

class EnhancedLeadGenerator:
    def __init__(self):
        self.scrapling_used = False
        self.scrapling_results = 0
        self.api_results = 0
        self.start_time = datetime.now()
        self.leads = []
        
    async def try_scrapling(self):
        """Try Scrapling first for lead generation."""
        if not SCRAPLING_AVAILABLE:
            print("⚠️ Scrapling not available, skipping...")
            return []
        
        print("\n🔍 Attempting Scrapling integration...")
        
        try:
            scrapling = ScraplingCronIntegration(stealth_mode=True)
            success = await scrapling.initialize()
            
            if not success:
                print("❌ Scrapling initialization failed")
                return []
            
            print("✅ Scrapling initialized successfully")
            
            # Generate leads with Scrapling
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
                self.scrapling_results = len(leads)
                print(f"✅ Scrapling found {len(leads)} leads")
                return leads
            else:
                print("⚠️ Scrapling returned no results")
                return []
                
        except Exception as e:
            print(f"❌ Scrapling error: {e}")
            return []
    
    async def try_tavily(self):
        """Fall back to Tavily API."""
        print("\n🔄 Falling back to Tavily API...")
        
        import aiohttp
        
        api_key = "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"
        
        queries = [
            "manufacturing companies 50-200 employees Texas",
            "technology companies 20-100 employees California", 
            "healthcare companies 30-150 employees Florida",
            "professional services firms 25-75 employees New York"
        ]
        
        leads = []
        
        async with aiohttp.ClientSession() as session:
            for query in queries:
                try:
                    payload = {
                        "api_key": api_key,
                        "query": query,
                        "search_depth": "basic",
                        "max_results": 10
                    }
                    
                    async with session.post(
                        "https://api.tavily.com/search",
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=15)
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            results = data.get("results", [])
                            
                            for result in results[:8]:
                                lead = {
                                    "company_name": self._extract_company_name(result.get("url", "")),
                                    "url": result.get("url"),
                                    "title": result.get("title", ""),
                                    "description": result.get("content", "")[:200],
                                    "source": "Tavily",
                                    "lead_score": self._quick_score(result)
                                }
                                leads.append(lead)
                            
                            print(f"✅ Tavily: {len(results)} results for '{query[:50]}...'")
                        else:
                            print(f"⚠️ Tavily error: {response.status}")
                            
                except Exception as e:
                    print(f"⚠️ Tavily query failed: {e}")
        
        if leads:
            self.api_results = len(leads)
            print(f"✅ Tavily total: {len(leads)} leads")
        
        return leads
    
    async def try_brave_search(self):
        """Fall back to Brave Search API."""
        print("\n🔄 Falling back to Brave Search API...")
        
        import aiohttp
        
        api_key = "cac43a248afb1cc1ec004370df2e0282a67eb420"
        
        queries = [
            "manufacturing companies 50-200 employees Texas",
            "technology companies California medium business",
            "healthcare companies Florida 30-150 employees",
            "professional services firms New York small business"
        ]
        
        leads = []
        
        async with aiohttp.ClientSession() as session:
            for query in queries:
                try:
                    headers = {
                        "X-API-KEY": api_key,
                        "Content-Type": "application/json"
                    }
                    
                    payload = {"q": query}
                    
                    async with session.post(
                        "https://google.serper.dev/search",
                        headers=headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=15)
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            results = data.get("organic", [])
                            
                            for result in results[:7]:
                                lead = {
                                    "company_name": self._extract_company_name(result.get("link", "")),
                                    "url": result.get("link"),
                                    "title": result.get("title", ""),
                                    "description": result.get("snippet", "")[:200],
                                    "source": "Brave Search",
                                    "lead_score": self._quick_score(result)
                                }
                                leads.append(lead)
                            
                            print(f"✅ Brave Search: {len(results)} results for '{query[:40]}...'")
                        else:
                            print(f"⚠️ Brave Search error: {response.status}")
                            
                except Exception as e:
                    print(f"⚠️ Brave Search query failed: {e}")
        
        if leads:
            self.api_results = len(leads)
            print(f"✅ Brave Search total: {len(leads)} leads")
        
        return leads
    
    def _extract_company_name(self, url):
        """Extract company name from URL."""
        if not url:
            return "Unknown"
        
        from urllib.parse import urlparse
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.replace("www.", "")
            name = domain.split(".")[0]
            return name.title()
        except:
            return "Unknown"
    
    def _quick_score(self, result):
        """Quick lead scoring (0-100)."""
        score = 50  # Base score
        
        title = result.get("title", "").lower()
        desc = result.get("content", result.get("snippet", "")).lower()
        
        # Size indicators (+25)
        size_keywords = ["50-200", "20-100", "30-150", "employees", "staff", "team"]
        if any(kw in title or kw in desc for kw in size_keywords):
            score += 25
        
        # Industry match (+25)
        industry_keywords = ["manufacturing", "technology", "healthcare", "professional services"]
        if any(kw in title or kw in desc for kw in industry_keywords):
            score += 25
        
        return min(score, 100)
    
    async def run(self):
        """Main execution flow."""
        print("="*60)
        print("🚀 Enhanced Lead Gen v2 - Scrapling-First")
        print("="*60)
        
        # Step 1: Try Scrapling
        leads = await self.try_scrapling()
        
        # Step 2: Fall back to Tavily if needed
        if not leads:
            leads = await self.try_tavily()
        
        # Step 3: Fall back to Brave Search if needed
        if not leads:
            leads = await self.try_brave_search()
        
        self.leads = leads
        
        # Calculate processing time
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        # Save results
        await self.save_results(elapsed)
        
        # Print summary
        self.print_summary(elapsed)
        
        return leads
    
    async def save_results(self, elapsed_time):
        """Save leads to file."""
        today = datetime.now().strftime("%Y-%m-%d")
        output_dir = Path("/Users/cubiczan/.openclaw/workspace/leads")
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"daily-leads-{today}.md"
        
        # Sort by lead score
        sorted_leads = sorted(self.leads, key=lambda x: x.get("lead_score", 0), reverse=True)
        
        # Count priorities
        high_priority = sum(1 for l in sorted_leads if l.get("lead_score", 0) >= 70)
        medium_priority = sum(1 for l in sorted_leads if 50 <= l.get("lead_score", 0) < 70)
        
        with open(output_file, 'w') as f:
            f.write(f"# Daily Leads - {today}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Leads:** {len(sorted_leads)}\n")
            f.write(f"**High Priority (70+):** {high_priority}\n")
            f.write(f"**Medium Priority (50-69):** {medium_priority}\n")
            f.write(f"**Processing Time:** {elapsed_time:.1f} seconds\n\n")
            
            f.write("## 🔍 Data Source Report\n")
            f.write(f"- **Scrapling Used:** {'✅ Yes' if self.scrapling_used else '❌ No'}\n")
            f.write(f"- **Scrapling Results:** {self.scrapling_results} leads\n")
            f.write(f"- **Traditional API Results:** {self.api_results} leads\n\n")
            
            f.write("## 📊 Top 3 High-Priority Leads\n\n")
            for i, lead in enumerate(sorted_leads[:3], 1):
                f.write(f"### {i}. {lead.get('company_name', 'Unknown')}\n")
                f.write(f"- **Score:** {lead.get('lead_score', 0)}/100\n")
                f.write(f"- **URL:** {lead.get('url', 'N/A')}\n")
                f.write(f"- **Title:** {lead.get('title', 'N/A')}\n")
                if lead.get('description'):
                    f.write(f"- **Description:** {lead.get('description')}\n")
                f.write(f"- **Source:** {lead.get('source', 'Unknown')}\n\n")
            
            f.write("## 📋 All Leads\n\n")
            for i, lead in enumerate(sorted_leads, 1):
                score = lead.get('lead_score', 0)
                priority_emoji = "🔥" if score >= 70 else "⭐" if score >= 50 else "📌"
                f.write(f"{i}. {priority_emoji} **{lead.get('company_name', 'Unknown')}** (Score: {score})\n")
                f.write(f"   - URL: {lead.get('url', 'N/A')}\n")
                f.write(f"   - Source: {lead.get('source', 'Unknown')}\n\n")
        
        print(f"\n✅ Results saved to: {output_file}")
    
    def print_summary(self, elapsed_time):
        """Print execution summary."""
        sorted_leads = sorted(self.leads, key=lambda x: x.get("lead_score", 0), reverse=True)
        high_priority = sum(1 for l in sorted_leads if l.get("lead_score", 0) >= 70)
        
        print("\n" + "="*60)
        print("📊 EXECUTION SUMMARY")
        print("="*60)
        print(f"✅ Total leads found: {len(sorted_leads)}")
        print(f"🔥 High priority (70+): {high_priority}")
        print(f"⏱️  Processing time: {elapsed_time:.1f} seconds")
        print(f"\n🔍 Data Source:")
        print(f"   Scrapling Used: {'✅ Yes' if self.scrapling_used else '❌ No'}")
        print(f"   Scrapling Results: {self.scrapling_results}")
        print(f"   API Results: {self.api_results}")
        
        print(f"\n🎯 Top 3 Companies:")
        for i, lead in enumerate(sorted_leads[:3], 1):
            print(f"   {i}. {lead.get('company_name', 'Unknown')} (Score: {lead.get('lead_score', 0)})")


async def main():
    generator = EnhancedLeadGenerator()
    await generator.run()


if __name__ == "__main__":
    asyncio.run(main())
