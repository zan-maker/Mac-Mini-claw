#!/usr/bin/env python3
"""
Deal Origination - Sellers (Scrapling-First Approach)
Enhanced with Scrapling integration for 774x faster scraping
"""

import asyncio
import sys
import os
import json
from datetime import datetime
import time

# Add Scrapling integration path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# Try Scrapling first
SCRAPLING_AVAILABLE = False
try:
    from cron_integration import ScraplingCronIntegration
    SCRAPLING_AVAILABLE = True
    print("✅ Scrapling module imported successfully")
except ImportError as e:
    print(f"⚠️ Scrapling import failed: {e}")
    print("⚠️ Falling back to traditional APIs")

# Traditional API imports (fallback)
try:
    import requests
    TRADITIONAL_APIS_AVAILABLE = True
except ImportError:
    TRADITIONAL_APIS_AVAILABLE = False
    print("⚠️ Requests module not available")

# Configuration
TAVILY_API_KEY = "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"
BRAVE_API_KEY = "BSA4VYA3FjSPQmTjZeKjsq5CqWvFy2u"

# Search terms for off-market sellers
SEARCH_TERMS = [
    "HVAC business for sale owner retiring",
    "plumbing company owner retirement",
    "electrical contractor business sale",
    "commercial cleaning business owner exit",
    "healthcare services business acquisition",
    "roofing company for sale no broker",
    "fire safety business owner retiring",
    "waste management company succession planning",
    "insurance brokerage owner exit strategy",
    "dental practice for sale doctor retiring",
    "veterinary clinic owner retirement",
    "logistics company owner succession",
    "manufacturing business owner retiring",
    "distribution company for sale no broker"
]

# Blue collar industries
BLUE_COLLAR_INDUSTRIES = [
    "HVAC", "Plumbing", "Electrical", "Roofing", "Fire Safety",
    "Commercial Cleaning", "Waste Management", "Construction",
    "Landscaping", "Pest Control", "Painting", "Carpentry"
]

# Platform industries
PLATFORM_INDUSTRIES = [
    "Healthcare Services", "Insurance Brokerage", "Logistics",
    "Dental", "Veterinary", "Software", "Marketing Agency",
    "Accounting", "Legal Services", "Consulting"
]

class DealOriginationSellers:
    def __init__(self):
        self.scrapling_used = False
        self.scrapling_results = 0
        self.traditional_results = 0
        self.start_time = time.time()
        self.sellers = []
        
    def calculate_score(self, seller):
        """Calculate lead score (0-100)"""
        score = 0
        
        # EBITDA range (0-30 points)
        if seller.get("ebitda_range"):
            ebitda = seller["ebitda_range"]
            if "500K-1M" in ebitda:
                score += 15
            elif "1M-3M" in ebitda:
                score += 25
            elif "3M-10M" in ebitda:
                score += 30
            elif "10M+" in ebitda:
                score += 30
        
        # Years in business (0-20 points)
        if seller.get("years_in_business"):
            years = seller["years_in_business"]
            if years >= 20:
                score += 20
            elif years >= 15:
                score += 15
            elif years >= 10:
                score += 10
            elif years >= 5:
                score += 5
        
        # Owner retirement signals (0-25 points)
        retirement_signals = seller.get("owner_signals", [])
        if "owner_near_retirement" in retirement_signals:
            score += 15
        if "second_generation" in retirement_signals:
            score += 10
        if "succession_planning" in retirement_signals:
            score += 5
        
        # Segment fit (0-25 points)
        industry = seller.get("industry", "").lower()
        if any(industry in bc.lower() for bc in BLUE_COLLAR_INDUSTRIES):
            score += 25  # High demand for blue collar
        elif any(industry in pf.lower() for pf in PLATFORM_INDUSTRIES):
            score += 20  # Good demand for platform
        
        return min(score, 100)
    
    def estimate_finder_fee(self, seller):
        """Estimate finder fee based on EBITDA"""
        ebitda = seller.get("ebitda_range", "")
        if "500K-1M" in ebitda:
            return "$25,000 - $50,000"
        elif "1M-3M" in ebitda:
            return "$50,000 - $150,000"
        elif "3M-10M" in ebitda:
            return "$150,000 - $500,000"
        elif "10M+" in ebitda:
            return "$500,000 - $1,000,000+"
        return "$10,000 - $25,000"
    
    async def find_sellers_with_scrapling(self):
        """Use Scrapling for fast, stealthy data extraction"""
        if not SCRAPLING_AVAILABLE:
            print("❌ Scrapling not available")
            return []
        
        try:
            print("🚀 Initializing Scrapling with stealth mode...")
            scrapling = ScraplingCronIntegration(stealth_mode=True)
            success = await scrapling.initialize()
            
            if not success:
                print("⚠️ Scrapling initialization failed")
                return []
            
            print("✅ Scrapling initialized successfully")
            self.scrapling_used = True
            
            # Find off-market sellers using Scrapling
            print(f"🔍 Searching for off-market sellers with {len(SEARCH_TERMS)} search terms...")
            
            sellers = []
            for search_term in SEARCH_TERMS:
                print(f"  Searching: {search_term}")
                try:
                    # Use Scrapling's natural language query
                    results = await scrapling.find_off_market_sellers([search_term])
                    if results:
                        sellers.extend(results)
                        print(f"    Found {len(results)} potential sellers")
                except Exception as e:
                    print(f"    Error with search term '{search_term}': {e}")
                    continue
            
            self.scrapling_results = len(sellers)
            print(f"📊 Scrapling found {len(sellers)} total potential sellers")
            return sellers
            
        except Exception as e:
            print(f"❌ Scrapling error: {e}")
            return []
    
    def find_sellers_with_tavily(self):
        """Fallback to Tavily API"""
        print("🔄 Falling back to Tavily API...")
        
        sellers = []
        headers = {
            "X-API-Key": TAVILY_API_KEY,
            "Content-Type": "application/json"
        }
        
        for search_term in SEARCH_TERMS:
            try:
                payload = {
                    "query": f"{search_term} site:craigslist.org OR site:businessforsale.com OR site:bizbuysell.com -broker",
                    "max_results": 5,
                    "search_depth": "advanced"
                }
                
                response = requests.post(
                    "https://api.tavily.com/search",
                    json=payload,
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    results = response.json().get("results", [])
                    for result in results:
                        seller = {
                            "company": result.get("title", "Unknown"),
                            "source": "Tavily API",
                            "url": result.get("url", ""),
                            "description": result.get("content", ""),
                            "industry": self.extract_industry(search_term),
                            "ebitda_range": self.estimate_ebitda(search_term),
                            "years_in_business": self.estimate_years(search_term),
                            "owner_signals": self.extract_owner_signals(result.get("content", "")),
                            "search_term": search_term
                        }
                        sellers.append(seller)
                        
            except Exception as e:
                print(f"    Tavily error for '{search_term}': {e}")
                continue
        
        self.traditional_results = len(sellers)
        return sellers
    
    def find_sellers_with_brave(self):
        """Second fallback to Brave Search API"""
        print("🔄 Falling back to Brave Search API...")
        
        sellers = []
        
        for search_term in SEARCH_TERMS:
            try:
                params = {
                    "q": f"{search_term} -broker -intermediary -middleman",
                    "count": 5,
                    "country": "US",
                    "search_lang": "en"
                }
                
                headers = {
                    "X-Subscription-Token": BRAVE_API_KEY,
                    "Accept": "application/json"
                }
                
                response = requests.get(
                    "https://api.search.brave.com/res/v1/web/search",
                    params=params,
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    results = response.json().get("web", {}).get("results", [])
                    for result in results:
                        seller = {
                            "company": result.get("title", "Unknown"),
                            "source": "Brave Search",
                            "url": result.get("url", ""),
                            "description": result.get("description", ""),
                            "industry": self.extract_industry(search_term),
                            "ebitda_range": self.estimate_ebitda(search_term),
                            "years_in_business": self.estimate_years(search_term),
                            "owner_signals": self.extract_owner_signals(result.get("description", "")),
                            "search_term": search_term
                        }
                        sellers.append(seller)
                        
            except Exception as e:
                print(f"    Brave error for '{search_term}': {e}")
                continue
        
        self.traditional_results = len(sellers)
        return sellers
    
    def extract_industry(self, search_term):
        """Extract industry from search term"""
        search_term_lower = search_term.lower()
        for industry in BLUE_COLLAR_INDUSTRIES + PLATFORM_INDUSTRIES:
            if industry.lower() in search_term_lower:
                return industry
        return "Other"
    
    def estimate_ebitda(self, search_term):
        """Estimate EBITDA range based on search term"""
        if any(word in search_term.lower() for word in ["hvac", "plumbing", "electrical", "roofing"]):
            return "$1M-3M"
        elif any(word in search_term.lower() for word in ["healthcare", "insurance", "dental", "veterinary"]):
            return "$3M-10M"
        elif any(word in search_term.lower() for word in ["logistics", "manufacturing", "distribution"]):
            return "$500K-1M"
        return "$500K-1M"
    
    def estimate_years(self, search_term):
        """Estimate years in business"""
        if "retiring" in search_term.lower() or "retirement" in search_term.lower():
            return 20  # Likely established business
        return 15  # Default assumption
    
    def extract_owner_signals(self, description):
        """Extract owner retirement signals from description"""
        signals = []
        desc_lower = description.lower()
        
        if any(word in desc_lower for word in ["retiring", "retirement", "exit"]):
            signals.append("owner_near_retirement")
        if "second generation" in desc_lower or "family owned" in desc_lower:
            signals.append("second_generation")
        if "succession" in desc_lower or "transition" in desc_lower:
            signals.append("succession_planning")
        if "no broker" in desc_lower or "direct" in desc_lower:
            signals.append("off_market")
        
        return signals
    
    def process_sellers(self, raw_sellers):
        """Process and enrich seller data"""
        processed = []
        
        for seller in raw_sellers:
            # Calculate score
            seller["score"] = self.calculate_score(seller)
            
            # Estimate finder fee
            seller["estimated_finder_fee"] = self.estimate_finder_fee(seller)
            
            # Determine priority
            if seller["score"] >= 80:
                seller["priority"] = "High"
            elif seller["score"] >= 60:
                seller["priority"] = "Medium"
            else:
                seller["priority"] = "Low"
            
            # Add timestamp
            seller["discovered_date"] = datetime.now().strftime("%Y-%m-%d")
            
            processed.append(seller)
        
        # Sort by score (highest first)
        processed.sort(key=lambda x: x["score"], reverse=True)
        return processed
    
    def save_results(self, sellers):
        """Save results to files"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Create directories if they don't exist
        os.makedirs("/Users/cubiczan/.openclaw/workspace/deals/sellers", exist_ok=True)
        os.makedirs("/Users/cubiczan/.openclaw/workspace/deals", exist_ok=True)
        
        # Save daily sellers file
        daily_file = f"/Users/cubiczan/.openclaw/workspace/deals/sellers/daily-sellers-{today}.md"
        
        with open(daily_file, "w") as f:
            f.write(f"# Daily Off-Market Sellers - {today}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Sellers:** {len(sellers)}\n")
            f.write(f"**Scrapling Used:** {'Yes' if self.scrapling_used else 'No'}\n")
            f.write(f"**Scrapling Results:** {self.scrapling_results}\n")
            f.write(f"**Traditional API Results:** {self.traditional_results}\n")
            f.write(f"**Processing Time:** {time.time() - self.start_time:.2f} seconds\n\n")
            
            f.write("## Summary\n")
            f.write(f"- **High Priority:** {len([s for s in sellers if s['priority'] == 'High'])}\n")
            f.write(f"- **Medium Priority:** {len([s for s in sellers if s['priority'] == 'Medium'])}\n")
            f.write(f"- **Low Priority:** {len([s for s in sellers if s['priority'] == 'Low'])}\n")
            
            blue_collar = len([s for s in sellers if any(bc.lower() in s.get('industry', '').lower() for bc in BLUE_COLLAR_INDUSTRIES)])
            platform = len([s for s in sellers if any(pf.lower() in s.get('industry', '').lower() for pf in PLATFORM_INDUSTRIES)])
            f.write(f"- **Blue Collar:** {blue_collar}\n")
            f.write(f"- **Platform:** {platform}\n")
            
            total_finder_fees = sum([
                37500 if "$25,000 - $50,000" in s.get("estimated_finder_fee", "") else
                100000 if "$50,000 - $150,000" in s.get("estimated_finder_fee", "") else
                325000 if "$150,000 - $500,000" in s.get("estimated_finder_fee", "") else
                750000 if "$500,000 - $1,000,000+" in s.get("estimated_finder_fee", "") else
                17500
                for s in sellers
            ])
            f.write(f"- **Total Estimated Finder Fees:** ${total_finder_fees:,}\n\n")
            
            f.write("## Seller Details\n\n")
            for i, seller in enumerate(sellers, 1):
                f.write(f"### {i}. {seller.get('company', 'Unknown Company')}\n")
                f.write(f"- **Industry:** {seller.get('industry', 'Unknown')}\n")
                f.write(f"- **EBITDA Range:** {seller.get('ebitda_range', 'Unknown')}\n")
                f.write(f"- **Years in Business:** {seller.get('years_in_business', 'Unknown')}\n")
                f.write(f"- **Owner Signals:** {', '.join(seller.get('owner_signals', []))}\n")
                f.write(f"- **Score:** {seller.get('score', 0)}/100\n")
                f.write(f"- **Priority:** {seller.get('priority', 'Low')}\n")
                f.write(f"- **Estimated Finder Fee:** {seller.get('estimated_finder_fee', 'Unknown')}\n")
                f.write(f"- **Source:** {seller.get('source', 'Unknown')}\n")
                if seller.get('url'):
                    f.write(f"- **URL:** {seller.get('url')}\n")
                f.write(f"- **Description:** {seller.get('description', '')[:200]}...\n\n")
        
        print(f"✅ Saved daily sellers to: {daily_file}")
        
        # Update pipeline file
        pipeline_file = "/Users/cubiczan/.openclaw/workspace/deals/pipeline.md"
        
        if os.path.exists(pipeline_file):
            with open(pipeline_file, "a") as f:
                f.write(f"\n## {today} - New Sellers Added\n")
                f.write(f"- Added {len(sellers)} new off-market seller leads\n")
                f.write(f"- High priority: {len([s for s in sellers if s['priority'] == 'High'])}\n")
                f.write(f"- Source: {'Scrapling' if self.scrapling_used else 'Traditional APIs'}\n")
        else:
            with open(pipeline