#!/usr/bin/env python3
"""
Enhanced Lead Gen v2 - Scrapling-First Approach
Generates 20-30 expense reduction leads with Scrapling integration
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import List, Dict, Any
import requests

# Add Scrapling integration to path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# API Keys
SERPER_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"
TAVILY_API_KEY = "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"

class EnhancedLeadGenerator:
    def __init__(self):
        self.scrapling_used = False
        self.scrapling_results = 0
        self.api_results = 0
        self.start_time = datetime.now()
        
    async def try_scrapling(self) -> List[Dict[str, Any]]:
        """Try Scrapling integration first."""
        print("🔍 Attempting Scrapling integration...")
        
        try:
            from cron_integration import ScraplingCronIntegration
            
            scrapling = ScraplingCronIntegration(stealth_mode=True)
            success = await scrapling.initialize()
            
            if success:
                print("✅ Scrapling initialized successfully")
                
                # Generate leads
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
                
                if leads and len(leads) > 0:
                    self.scrapling_used = True
                    self.scrapling_results = len(leads)
                    print(f"✅ Scrapling found {len(leads)} leads")
                    return leads
                else:
                    print("⚠️ Scrapling returned no results")
                    return []
            else:
                print("⚠️ Scrapling initialization failed")
                return []
                
        except ImportError as e:
            print(f"⚠️ Scrapling not available: {e}")
            return []
        except Exception as e:
            print(f"⚠️ Scrapling error: {e}")
            return []
    
    def search_tavily(self, query: str) -> List[Dict[str, Any]]:
        """Search using Tavily API."""
        print(f"🔍 Searching Tavily: {query}")
        
        try:
            url = "https://api.tavily.com/search"
            payload = {
                "api_key": TAVILY_API_KEY,
                "query": query,
                "search_depth": "basic",
                "max_results": 10
            }
            
            response = requests.post(url, json=payload, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                print(f"✅ Tavily found {len(results)} results")
                return results
            else:
                print(f"⚠️ Tavily API error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"⚠️ Tavily search error: {e}")
            return []
    
    def search_brave(self, query: str) -> List[Dict[str, Any]]:
        """Search using Brave Search API (Serper)."""
        print(f"🔍 Searching Brave/Serper: {query}")
        
        try:
            url = "https://google.serper.dev/search"
            headers = {
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json"
            }
            payload = {"q": query}
            
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                # Convert Serper format to common format
                results = []
                
                # Organic results
                for item in data.get("organic", []):
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("link", ""),
                        "snippet": item.get("snippet", "")
                    })
                
                print(f"✅ Brave/Serper found {len(results)} results")
                return results
            else:
                print(f"⚠️ Brave API error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"⚠️ Brave search error: {e}")
            return []
    
    def score_lead(self, lead: Dict[str, Any]) -> int:
        """Score lead from 0-100."""
        score = 0
        
        # Size fit (50-200 employees): 25 pts
        snippet = lead.get("snippet", "").lower()
        title = lead.get("title", "").lower()
        text = snippet + " " + title
        
        if any(size in text for size in ["50-200", "100+ employees", "50+ employees", "200 employees"]):
            score += 25
        elif any(size in text for size in ["employees", "staff", "team"]):
            score += 15
        
        # Industry match: 25 pts
        if any(industry in text for industry in ["manufacturing", "technology", "healthcare", "professional services"]):
            score += 25
        elif any(industry in text for industry in ["company", "corporation", "inc", "llc"]):
            score += 10
        
        # Contact found: 25 pts
        if any(contact in text for contact in ["contact", "email", "phone", "ceo", "president", "director"]):
            score += 25
        elif any(contact in text for contact in ["about", "team", "leadership"]):
            score += 15
        
        # Intent signal: 25 pts
        if any(signal in text for signal in ["growing", "expanding", "hiring", "new location", "investment"]):
            score += 25
        elif any(signal in text for signal in ["services", "solutions", "products"]):
            score += 15
        
        return min(score, 100)
    
    def process_api_results(self, results: List[Dict[str, Any]], source: str) -> List[Dict[str, Any]]:
        """Process and score API results."""
        leads = []
        
        for result in results:
            lead = {
                "company_name": result.get("title", "Unknown"),
                "url": result.get("url", ""),
                "description": result.get("snippet", ""),
                "source": source,
                "found_at": datetime.now().isoformat()
            }
            
            # Score the lead
            lead["score"] = self.score_lead(lead)
            
            # Only include leads with score > 30
            if lead["score"] > 30:
                leads.append(lead)
        
        return leads
    
    async def generate_leads(self) -> List[Dict[str, Any]]:
        """Generate leads using Scrapling-first approach."""
        all_leads = []
        
        # Step 1: Try Scrapling
        scrapling_leads = await self.try_scrapling()
        if scrapling_leads:
            all_leads.extend(scrapling_leads)
        
        # Step 2: Fall back to APIs if needed
        if len(all_leads) < 20:
            print("\n📊 Falling back to traditional APIs...")
            
            search_queries = [
                "manufacturing companies 50-200 employees Texas site:linkedin.com OR site:crunchbase.com",
                "technology companies 20-100 employees California site:linkedin.com OR site:crunchbase.com",
                "healthcare companies 30-150 employees Florida site:linkedin.com OR site:crunchbase.com",
                "professional services firms 25-75 employees New York site:linkedin.com OR site:crunchbase.com"
            ]
            
            for query in search_queries:
                if len(all_leads) >= 30:
                    break
                
                # Try Tavily first
                results = self.search_tavily(query)
                if results:
                    leads = self.process_api_results(results, "Tavily")
                    all_leads.extend(leads)
                    self.api_results += len(leads)
                else:
                    # Fall back to Brave/Serper
                    results = self.search_brave(query)
                    if results:
                        leads = self.process_api_results(results, "Brave")
                        all_leads.extend(leads)
                        self.api_results += len(leads)
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_leads = []
        for lead in all_leads:
            url = lead.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_leads.append(lead)
        
        # Sort by score
        unique_leads.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        # Limit to 30
        return unique_leads[:30]
    
    def save_leads(self, leads: List[Dict[str, Any]]):
        """Save leads to markdown file."""
        today = datetime.now().strftime("%Y-%m-%d")
        output_file = f"/Users/cubiczan/.openclaw/workspace/leads/daily-leads-{today}.md"
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, "w") as f:
            f.write(f"# Daily Leads - {today}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Leads:** {len(leads)}\n")
            f.write(f"**High Priority (70+):** {sum(1 for l in leads if l.get('score', 0) >= 70)}\n\n")
            
            f.write("---\n\n")
            
            for i, lead in enumerate(leads, 1):
                score = lead.get("score", 0)
                priority_emoji = "🔥" if score >= 70 else "⭐" if score >= 50 else "📌"
                
                f.write(f"## {priority_emoji} Lead #{i}: {lead.get('company_name', 'Unknown')}\n\n")
                f.write(f"**Score:** {score}/100\n")
                f.write(f"**Source:** {lead.get('source', 'Unknown')}\n")
                f.write(f"**URL:** {lead.get('url', 'N/A')}\n\n")
                f.write(f"**Description:**\n{lead.get('description', 'No description available')}\n\n")
                f.write("---\n\n")
        
        print(f"✅ Saved {len(leads)} leads to {output_file}")
        return output_file
    
    def generate_report(self, leads: List[Dict[str, Any]]) -> str:
        """Generate Discord report."""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        high_priority = [l for l in leads if l.get("score", 0) >= 70]
        
        report = f"""# 🎯 Enhanced Lead Gen Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 🔍 Data Source Report:
- **Scrapling Used:** {'✅ Yes' if self.scrapling_used else '❌ No'}
- **Scrapling Results:** {self.scrapling_results} leads
- **Traditional API Results:** {self.api_results} leads
- **Total Processing Time:** {elapsed:.1f} seconds

## 📊 Summary:
- **Total Found:** {len(leads)}
- **High Priority (70+):** {len(high_priority)}

## 🔥 Top 3 Companies:
"""
        
        for i, lead in enumerate(leads[:3], 1):
            report += f"\n**{i}. {lead.get('company_name', 'Unknown')}** (Score: {lead.get('score', 0)})\n"
            report += f"   • {lead.get('description', 'No description')[:100]}...\n"
            report += f"   • Source: {lead.get('source', 'Unknown')}\n"
        
        report += f"\n---\n✅ Leads saved to: `/workspace/leads/daily-leads-{datetime.now().strftime('%Y-%m-%d')}.md`"
        
        return report


async def main():
    print("🚀 Starting Enhanced Lead Generation v2 (Scrapling-First)\n")
    
    generator = EnhancedLeadGenerator()
    
    # Generate leads
    leads = await generator.generate_leads()
    
    if leads:
        # Save leads
        output_file = generator.save_leads(leads)
        
        # Generate report
        report = generator.generate_report(leads)
        print("\n" + report)
        
        return report
    else:
        error_report = """# ❌ Lead Generation Failed

## 🔍 Data Source Report:
- **Scrapling Used:** ❌ No
- **Scrapling Results:** 0 leads
- **Traditional API Results:** 0 leads

## ⚠️ Error:
No leads were generated. Please check API keys and network connectivity.
"""
        print(error_report)
        return error_report


if __name__ == "__main__":
    result = asyncio.run(main())
    print(result)
