#!/usr/bin/env python3
"""
Enhanced Lead Gen v2 - Scrapling-First Approach
Tries Scrapling first, falls back to Tavily, then Serper API
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import aiohttp
import re

# Add scrapling to path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# Configuration
SERPER_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"
TAVILY_API_KEY = "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"
ZEROBOUNCE_API_KEY = "fd0105c8c98340e0a2b63e2fbe39d7a4"

# Search queries
SEARCH_QUERIES = [
    "manufacturing companies 50-200 employees Texas",
    "technology companies 20-100 employees California",
    "healthcare companies 30-150 employees Florida",
    "professional services firms 25-75 employees New York"
]

class EnhancedLeadGenerator:
    def __init__(self):
        self.scrapling_used = False
        self.scrapling_results = 0
        self.api_results = 0
        self.start_time = datetime.now()
        self.leads = []
        
    async def try_scrapling(self):
        """Try Scrapling integration first."""
        print("🔧 Attempting Scrapling integration...")
        
        try:
            from cron_integration import ScraplingCronIntegration
            
            scrapling = ScraplingCronIntegration(stealth_mode=True)
            success = await scrapling.initialize()
            
            if success:
                print("✅ Scrapling initialized successfully")
                leads = await scrapling.generate_expense_reduction_leads(
                    search_queries=SEARCH_QUERIES,
                    limit=30,
                    fast_mode=True
                )
                
                if leads and len(leads) > 0:
                    self.scrapling_used = True
                    self.scrapling_results = len(leads)
                    self.leads = leads
                    print(f"✅ Scrapling found {len(leads)} leads")
                    return True
                else:
                    print("⚠️ Scrapling returned no results")
                    return False
            else:
                print("⚠️ Scrapling initialization failed")
                return False
                
        except ImportError as e:
            print(f"⚠️ Scrapling not available: {e}")
            return False
        except Exception as e:
            print(f"⚠️ Scrapling error: {e}")
            return False
    
    async def search_tavily(self, query):
        """Search using Tavily API."""
        print(f"🔍 Searching Tavily: {query}")
        
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "basic",
            "max_results": 10
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("results", [])
                    else:
                        print(f"⚠️ Tavily API error: {response.status}")
                        return []
        except Exception as e:
            print(f"⚠️ Tavily error: {e}")
            return []
    
    async def search_serper(self, query):
        """Search using Serper API."""
        print(f"🔍 Searching Serper: {query}")
        
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {"q": query}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Extract organic results
                        organic = data.get("organic", [])
                        return organic
                    else:
                        print(f"⚠️ Serper API error: {response.status}")
                        return []
        except Exception as e:
            print(f"⚠️ Serper error: {e}")
            return []
    
    def score_lead(self, company_name, description, url, source_query):
        """Score lead 0-100."""
        score = 0
        
        # Size fit (50-200 employees): 25 pts
        if any(x in description.lower() for x in ["50-200", "100+", "mid-sized", "growing"]):
            score += 25
        elif any(x in description.lower() for x in ["20-", "30-", "40-", "50-"]):
            score += 15
        
        # Industry match: 25 pts
        if any(x in source_query.lower() for x in ["manufacturing", "technology", "healthcare", "professional"]):
            if any(x in description.lower() for x in ["manufacturing", "technology", "healthcare", "services"]):
                score += 25
        
        # Contact potential: 25 pts
        if any(x in url.lower() for x in ["contact", "about"]):
            score += 15
        if "linkedin" in url.lower():
            score += 10
        
        # Intent signal: 25 pts
        if any(x in description.lower() for x in ["hiring", "growing", "expanding", "new location"]):
            score += 25
        elif any(x in description.lower() for x in ["services", "solutions", "provider"]):
            score += 15
        
        return min(score, 100)
    
    async def generate_with_apis(self):
        """Generate leads using APIs (Tavily first, then Serper)."""
        print("\n📡 Using traditional APIs...")
        
        for query in SEARCH_QUERIES:
            # Try Tavily first
            results = await self.search_tavily(query)
            
            # If Tavily fails, try Serper
            if not results:
                results = await self.search_serper(query)
            
            # Process results
            for result in results[:8]:  # Limit to 8 per query
                company_name = result.get("title", "Unknown")
                description = result.get("snippet", result.get("content", ""))
                url = result.get("link", result.get("url", ""))
                
                score = self.score_lead(company_name, description, url, query)
                
                lead = {
                    "company_name": company_name,
                    "description": description[:200],
                    "url": url,
                    "source_query": query,
                    "score": score,
                    "priority": "HIGH" if score >= 70 else "MEDIUM" if score >= 50 else "LOW"
                }
                
                self.leads.append(lead)
                self.api_results += 1
        
        print(f"✅ APIs found {self.api_results} leads")
    
    def save_leads(self):
        """Save leads to markdown file."""
        today = datetime.now().strftime("%Y-%m-%d")
        output_dir = Path("/Users/cubiczan/.openclaw/workspace/leads")
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"daily-leads-{today}.md"
        
        # Sort by score
        self.leads.sort(key=lambda x: x["score"], reverse=True)
        
        # Calculate stats
        total = len(self.leads)
        high_priority = len([l for l in self.leads if l["score"] >= 70])
        medium_priority = len([l for l in self.leads if 50 <= l["score"] < 70])
        
        # Processing time
        processing_time = (datetime.now() - self.start_time).total_seconds()
        
        with open(output_file, "w") as f:
            f.write(f"# Daily Leads - {today}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Data source report
            f.write("## 🔍 Data Source Report\n\n")
            f.write(f"- **Scrapling Used:** {'✅ Yes' if self.scrapling_used else '❌ No'}\n")
            f.write(f"- **Scrapling Results:** {self.scrapling_results} leads\n")
            f.write(f"- **Traditional API Results:** {self.api_results} leads\n")
            f.write(f"- **Total Processing Time:** {processing_time:.1f} seconds\n\n")
            
            # Summary
            f.write("## 📊 Summary\n\n")
            f.write(f"- **Total Leads:** {total}\n")
            f.write(f"- **High Priority (70+):** {high_priority}\n")
            f.write(f"- **Medium Priority (50-69):** {medium_priority}\n\n")
            
            # Top 3
            f.write("## 🏆 Top 3 Companies\n\n")
            for i, lead in enumerate(self.leads[:3], 1):
                f.write(f"{i}. **{lead['company_name']}** (Score: {lead['score']})\n")
                f.write(f"   - {lead['description']}\n")
                f.write(f"   - URL: {lead['url']}\n\n")
            
            # All leads
            f.write("## 📋 All Leads\n\n")
            for lead in self.leads:
                f.write(f"### {lead['company_name']} (Score: {lead['score']})\n\n")
                f.write(f"- **Priority:** {lead['priority']}\n")
                f.write(f"- **Source:** {lead['source_query']}\n")
                f.write(f"- **Description:** {lead['description']}\n")
                f.write(f"- **URL:** {lead['url']}\n\n")
        
        print(f"✅ Leads saved to {output_file}")
        
        return {
            "total": total,
            "high_priority": high_priority,
            "medium_priority": medium_priority,
            "processing_time": processing_time,
            "top_3": self.leads[:3],
            "output_file": str(output_file)
        }
    
    async def run(self):
        """Main execution."""
        print("🚀 Enhanced Lead Gen v2 - Scrapling-First\n")
        print(f"⏰ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Try Scrapling first
        scrapling_success = await self.try_scrapling()
        
        # Fall back to APIs if needed
        if not scrapling_success:
            await self.generate_with_apis()
        
        # Save results
        if self.leads:
            stats = self.save_leads()
            return stats
        else:
            print("❌ No leads generated")
            return None

async def main():
    generator = EnhancedLeadGenerator()
    stats = await generator.run()
    
    if stats:
        print(f"\n✅ Complete!")
        print(f"Total leads: {stats['total']}")
        print(f"High priority: {stats['high_priority']}")
        print(f"Processing time: {stats['processing_time']:.1f}s")
    
    return stats

if __name__ == "__main__":
    result = asyncio.run(main())
    
    # Output for Discord
    if result:
        print("\n" + "="*50)
        print("DISCORD REPORT:")
        print("="*50)
        print(f"🎯 **Enhanced Lead Gen v2 Complete**\n")
        print(f"🔍 **Data Source:**")
        print(f"- Scrapling: {'✅' if result.get('scrapling_used') else '❌'}")
        print(f"- API Results: {result.get('api_results', 0)}\n")
        print(f"📊 **Results:**")
        print(f"- Total: {result['total']}")
        print(f"- High Priority: {result['high_priority']}")
        print(f"- Time: {result['processing_time']:.1f}s\n")
        print(f"🏆 **Top 3:**")
        for i, lead in enumerate(result['top_3'], 1):
            print(f"{i}. {lead['company_name']} ({lead['score']})")
