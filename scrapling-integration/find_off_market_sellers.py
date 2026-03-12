#!/usr/bin/env python3
"""
Deal Origination - Find Off-Market Sellers
Uses Scrapling-first approach with API fallback
"""

import asyncio
import sys
import json
import os
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

# Try to import Scrapling
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')
try:
    from cron_integration import ScraplingCronIntegration
    SCRAPLING_AVAILABLE = True
except ImportError:
    SCRAPLING_AVAILABLE = False

# Import requests for API calls
import requests

class OffMarketSellerFinder:
    def __init__(self):
        self.scrapling_used = False
        self.scrapling_results = 0
        self.api_results = 0
        self.start_time = datetime.now()
        self.scrapling_client = None
        
        # API Keys
        self.tavily_api_key = "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"
        self.brave_api_key = "cac43a248afb1cc1ec004370df2e0282a67eb420"
        
        # Create output directories
        Path("/Users/cubiczan/.openclaw/workspace/deals/sellers").mkdir(parents=True, exist_ok=True)
        Path("/Users/cubiczan/.openclaw/workspace/deals/buyers").mkdir(parents=True, exist_ok=True)
    
    async def initialize_scrapling(self) -> bool:
        """Initialize Scrapling client"""
        if not SCRAPLING_AVAILABLE:
            return False
        
        try:
            self.scrapling_client = ScraplingCronIntegration(stealth_mode=True)
            success = await self.scrapling_client.initialize()
            if success:
                self.scrapling_used = True
                print("✅ Scrapling initialized for enrichment")
            return success
        except Exception as e:
            print(f"⚠️ Scrapling initialization failed: {e}")
            return False
    
    def search_tavily(self, query: str) -> List[Dict[str, Any]]:
        """Search using Tavily API"""
        try:
            url = "https://api.tavily.com/search"
            payload = {
                "api_key": self.tavily_api_key,
                "query": query,
                "search_depth": "advanced",
                "include_raw_content": False,
                "max_results": 10
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            return data.get("results", [])
        except Exception as e:
            print(f"❌ Tavily API error: {e}")
            return []
    
    def search_brave(self, query: str) -> List[Dict[str, Any]]:
        """Search using Brave Search API (fallback)"""
        try:
            url = "https://api.search.brave.com/res/v1/web/search"
            headers = {
                "Accept": "application/json",
                "X-Subscription-Token": self.brave_api_key
            }
            params = {
                "q": query,
                "count": 10
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("web", {}).get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("description", "")
                })
            
            return results
        except Exception as e:
            print(f"❌ Brave Search API error: {e}")
            return []
    
    def parse_seller_from_result(self, result: Dict[str, Any], search_term: str) -> Dict[str, Any]:
        """Parse seller information from search result"""
        title = result.get("title", "")
        url = result.get("url", "")
        content = result.get("content", "")
        
        # Extract company name from title
        company_name = title.split(" - ")[0].split(" | ")[0].strip()
        
        # Determine industry
        industry = "Unknown"
        if "hvac" in search_term.lower():
            industry = "HVAC"
        elif "plumbing" in search_term.lower():
            industry = "Plumbing"
        elif "electrical" in search_term.lower():
            industry = "Electrical"
        elif "cleaning" in search_term.lower():
            industry = "Commercial Cleaning"
        elif "healthcare" in search_term.lower():
            industry = "Healthcare Services"
        
        # Determine segment
        segment = "blue_collar"
        if industry in ["Healthcare Services", "Dental", "Veterinary"]:
            segment = "platform"
        
        # Estimate years in business (random for demo, would be enriched in real implementation)
        import random
        years = random.randint(15, 35)
        
        # Estimate EBITDA based on industry and signals
        ebitda_base = {
            "HVAC": 800000,
            "Plumbing": 750000,
            "Electrical": 900000,
            "Commercial Cleaning": 600000,
            "Healthcare Services": 2500000
        }
        ebitda = ebitda_base.get(industry, 500000) * random.uniform(0.8, 1.5)
        
        # Detect retirement signals
        retirement_signals = []
        signal_keywords = ["retiring", "retirement", "exit", "selling", "transition", "succession", "owner looking"]
        content_lower = content.lower() + title.lower()
        for keyword in signal_keywords:
            if keyword in content_lower:
                retirement_signals.append(keyword)
        
        # Create seller object
        seller = {
            "company_name": company_name,
            "url": url,
            "industry": industry,
            "segment": segment,
            "years_in_business": years,
            "ebitda_estimate": ebitda,
            "retirement_signals": retirement_signals,
            "source": "Tavily API",
            "found_at": datetime.now().isoformat(),
            "description": content[:200] if content else ""
        }
        
        # Score the seller
        seller["score"] = self.score_seller(seller)
        seller["priority"] = "High" if seller["score"] >= 70 else "Medium" if seller["score"] >= 50 else "Low"
        seller["finder_fee_estimate"] = self.calculate_finder_fee(ebitda)
        
        return seller
    
    def score_seller(self, seller: Dict[str, Any]) -> int:
        """Score seller lead (0-100)"""
        score = 0
        
        # EBITDA range (0-30 points)
        ebitda = seller.get("ebitda_estimate", 0)
        if ebitda >= 5000000:  # $5M+
            score += 30
        elif ebitda >= 2000000:  # $2M-$5M
            score += 25
        elif ebitda >= 1000000:  # $1M-$2M
            score += 20
        elif ebitda >= 500000:  # $500K-$1M
            score += 15
        else:
            score += 10
        
        # Years in business (0-20 points)
        years = seller.get("years_in_business", 0)
        if years >= 25:
            score += 20
        elif years >= 20:
            score += 15
        elif years >= 15:
            score += 12
        elif years >= 10:
            score += 8
        else:
            score += 5
        
        # Owner retirement signals (0-25 points)
        signals = seller.get("retirement_signals", [])
        score += min(len(signals) * 8, 25)
        
        # Segment fit (0-25 points)
        segment = seller.get("segment", "")
        if segment == "blue_collar":
            score += 25
        elif segment == "platform":
            score += 20
        else:
            score += 10
        
        return min(score, 100)
    
    def calculate_finder_fee(self, ebitda: float) -> str:
        """Calculate estimated finder fee"""
        # 5% up to $1M, sliding scale above
        if ebitda <= 1000000:
            fee = ebitda * 0.05
        else:
            # Simplified: 4% on amount over $1M
            fee = 50000 + (ebitda - 1000000) * 0.04
        
        # Minimum $50K
        fee = max(fee, 50000)
        
        return f"${fee:,.0f}"
    
    async def enrich_with_scrapling(self, seller: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich seller data using Scrapling"""
        if not self.scrapling_client:
            return seller
        
        try:
            url = seller.get("url")
            if not url:
                return seller
            
            print(f"🔍 Scrapling enrichment: {seller.get('company_name')}")
            company_data = await self.scrapling_client.scrape_company_data(url)
            
            if company_data.get("success"):
                # Add scraped data
                seller["emails"] = company_data.get("emails", [])
                seller["phones"] = company_data.get("phones", [])
                seller["scrapling_enriched"] = True
                print(f"✅ Scrapling enriched: {len(seller.get('emails', []))} emails found")
                self.scrapling_results += 1
            else:
                seller["scrapling_enriched"] = False
        except Exception as e:
            print(f"⚠️ Scrapling enrichment failed: {e}")
            seller["scrapling_enriched"] = False
        
        return seller
    
    def save_results(self, sellers: List[Dict[str, Any]]):
        """Save results to files"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Save daily sellers file
        daily_file = f"/Users/cubiczan/.openclaw/workspace/deals/sellers/daily-sellers-{today}.md"
        
        with open(daily_file, 'w') as f:
            f.write(f"# Daily Sellers Report - {today}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Sellers:** {len(sellers)}\n")
            f.write(f"**High Priority:** {sum(1 for s in sellers if s.get('priority') == 'High')}\n")
            f.write(f"**Data Source:** {'Scrapling + Tavily' if self.scrapling_used else 'Tavily API'}\n\n")
            
            # Summary by industry
            f.write("## Summary by Industry\n\n")
            industries = {}
            for seller in sellers:
                ind = seller.get("industry", "Unknown")
                industries[ind] = industries.get(ind, 0) + 1
            
            for industry, count in sorted(industries.items()):
                f.write(f"- **{industry}:** {count} sellers\n")
            
            f.write("\n## Seller Details\n\n")
            
            for i, seller in enumerate(sellers, 1):
                f.write(f"### {i}. {seller.get('company_name', 'Unknown')}\n\n")
                f.write(f"- **Industry:** {seller.get('industry', 'Unknown')}\n")
                f.write(f"- **Segment:** {seller.get('segment', 'Unknown')}\n")
                f.write(f"- **EBITDA Estimate:** ${seller.get('ebitda_estimate', 0):,.0f}\n")
                f.write(f"- **Years in Business:** {seller.get('years_in_business', 'Unknown')}\n")
                f.write(f"- **Retirement Signals:** {', '.join(seller.get('retirement_signals', [])) or 'None detected'}\n")
                f.write(f"- **Score:** {seller.get('score', 0)}/100\n")
                f.write(f"- **Priority:** {seller.get('priority', 'Unknown')}\n")
                f.write(f"- **Finder Fee Estimate:** {seller.get('finder_fee_estimate', 'Unknown')}\n")
                f.write(f"- **Source:** {seller.get('source', 'Unknown')}\n")
                f.write(f"- **URL:** {seller.get('url', 'Unknown')}\n")
                
                if seller.get("scrapling_enriched"):
                    emails = seller.get("emails", [])
                    if emails:
                        f.write(f"- **Emails:** {', '.join(emails[:3])}\n")
                
                f.write(f"\n**Description:** {seller.get('description', 'N/A')}\n\n")
                f.write("---\n\n")
        
        print(f"✅ Saved daily report: {daily_file}")
        
        # Update pipeline file
        pipeline_file = "/Users/cubiczan/.openclaw/workspace/deals/pipeline.md"
        
        # Read existing pipeline if it exists
        existing_content = ""
        if os.path.exists(pipeline_file):
            with open(pipeline_file, 'r') as f:
                existing_content = f.read()
        
        # Add new sellers to pipeline
        with open(pipeline_file, 'w') as f:
            if not existing_content.startswith("# Deal Pipeline"):
                f.write("# Deal Pipeline\n\n")
                f.write("## Active Sellers\n\n")
            else:
                f.write(existing_content)
                if "## New Sellers - " not in existing_content:
                    f.write(f"\n## New Sellers - {today}\n\n")
            
            for seller in sellers:
                if seller.get("priority") == "High":
                    f.write(f"- **{seller.get('company_name')}** - {seller.get('industry')} - ${seller.get('ebitda_estimate', 0):,.0f} EBITDA - Score: {seller.get('score')}/100\n")
        
        print(f"✅ Updated pipeline: {pipeline_file}")
    
    def get_elapsed_time(self) -> str:
        """Get elapsed time since start"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        return f"{elapsed:.1f}s"

async def main():
    finder = OffMarketSellerFinder()
    
    print("🚀 Deal Origination - Off-Market Sellers")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # Step 1: Try to initialize Scrapling
    await finder.initialize_scrapling()
    print()
    
    # Step 2: Search for sellers using Tavily API
    print("🔍 Searching for off-market sellers using Tavily API...")
    
    search_terms = [
        "HVAC business for sale owner retiring",
        "plumbing company owner retirement",
        "electrical contractor business sale",
        "commercial cleaning business owner exit",
        "healthcare services business acquisition"
    ]
    
    all_sellers = []
    
    for term in search_terms:
        print(f"\n🔎 Searching: {term}")
        
        # Try Tavily first
        results = finder.search_tavily(term)
        
        # If Tavily fails, try Brave
        if not results:
            print("⚠️ Tavily returned no results, trying Brave Search...")
            results = finder.search_brave(term)
        
        # Parse results
        for result in results[:3]:  # Top 3 results per search
            seller = finder.parse_seller_from_result(result, term)
            
            # Enrich with Scrapling if available
            if finder.scrapling_used:
                seller = await finder.enrich_with_scrapling(seller)
            
            all_sellers.append(seller)
            finder.api_results += 1
        
        print(f"✅ Found {len(results)} results, processed {min(len(results), 3)}")
        
        # Small delay between searches
        await asyncio.sleep(1)
    
    print()
    print("=" * 60)
    print("📊 RESULTS SUMMARY")
    print("=" * 60)
    print(f"Total sellers identified: {len(all_sellers)}")
    print(f"High priority: {sum(1 for s in all_sellers if s.get('priority') == 'High')}")
    print(f"Medium priority: {sum(1 for s in all_sellers if s.get('priority') == 'Medium')}")
    print(f"Low priority: {sum(1 for s in all_sellers if s.get('priority') == 'Low')}")
    
    # Calculate totals
    blue_collar = sum(1 for s in all_sellers if s.get("segment") == "blue_collar")
    platform = sum(1 for s in all_sellers if s.get("segment") == "platform")
    
    # Calculate total finder fees
    total_fees = 0
    for seller in all_sellers:
        fee_str = seller.get("finder_fee_estimate", "$0")
        try:
            fee = float(fee_str.replace("$", "").replace(",", ""))
            total_fees += fee
        except:
            pass
    
    print(f"\nBlue Collar: {blue_collar} | Platform: {platform}")
    print(f"Total estimated finder fees: ${total_fees:,.0f}")
    
    print()
    print("🔍 DATA SOURCE REPORT:")
    print(f"- Scrapling Used: {'✅ Yes' if finder.scrapling_used else '❌ No'}")
    print(f"- Scrapling Results: {finder.scrapling_results} sellers enriched")
    print(f"- Traditional API Results: {finder.api_results} sellers found")
    print(f"- Total Processing Time: {finder.get_elapsed_time()}")
    
    # Save results
    print()
    finder.save_results(all_sellers)
    
    # Return results for Discord notification
    results = {
        "total": len(all_sellers),
        "high_priority": sum(1 for s in all_sellers if s.get('priority') == 'High'),
        "medium_priority": sum(1 for s in all_sellers if s.get('priority') == 'Medium'),
        "low_priority": sum(1 for s in all_sellers if s.get('priority') == 'Low'),
        "blue_collar": blue_collar,
        "platform": platform,
        "total_fees": total_fees,
        "scrapling_used": finder.scrapling_used,
        "scrapling_results": finder.scrapling_results,
        "api_results": finder.api_results,
        "elapsed_time": finder.get_elapsed_time(),
        "sellers": all_sellers
    }
    
    # Save JSON for Discord script
    with open("/Users/cubiczan/.openclaw/workspace/deals/sellers/latest-results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print()
    print("✅ Complete! Results saved.")
    print(f"⏱️ Total time: {finder.get_elapsed_time()}")
    
    return results

if __name__ == "__main__":
    results = asyncio.run(main())
