#!/usr/bin/env python3
"""
Find off-market seller leads using Scrapling-first approach with API fallback
"""

import asyncio
import sys
import json
from datetime import datetime
from typing import List, Dict, Any

# Add scrapling integration to path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

try:
    from cron_integration import ScraplingCronIntegration
    SCRAPLING_AVAILABLE = True
except ImportError:
    SCRAPLING_AVAILABLE = False
    print("⚠️ Scrapling not available, will use API fallback")

class SellerFinder:
    def __init__(self):
        self.scrapling_used = False
        self.scrapling_results = 0
        self.api_results = 0
        self.start_time = datetime.now()
        
    async def try_scrapling_first(self, search_terms: List[str]) -> List[Dict[str, Any]]:
        """Try to use Scrapling for seller discovery"""
        if not SCRAPLING_AVAILABLE:
            print("⚠️ Scrapling not available, skipping")
            return []
        
        try:
            print("🔍 Attempting Scrapling integration...")
            scrapling = ScraplingCronIntegration(stealth_mode=True)
            success = await scrapling.initialize()
            
            if not success:
                print("⚠️ Scrapling initialization failed")
                return []
            
            # Scrapling is better at scraping known URLs than discovering them
            # So we'll need to use APIs for discovery, then optionally enrich with Scrapling
            print("ℹ️ Scrapling initialized but requires URLs to scrape")
            print("ℹ️ Using API for discovery, Scrapling for enrichment")
            self.scrapling_used = True
            return []
            
        except Exception as e:
            print(f"❌ Scrapling error: {e}")
            return []
    
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
    
    def get_elapsed_time(self) -> str:
        """Get elapsed time since start"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        return f"{elapsed:.1f}s"

async def main():
    finder = SellerFinder()
    
    # Search terms for off-market sellers
    search_terms = [
        "HVAC business for sale owner retiring",
        "plumbing company owner retirement",
        "electrical contractor business sale",
        "commercial cleaning business owner exit",
        "healthcare services business acquisition"
    ]
    
    print(f"🚀 Starting seller search at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📋 Search terms: {len(search_terms)}")
    print()
    
    # Step 1: Try Scrapling first
    scrapling_sellers = await finder.try_scrapling_first(search_terms)
    
    if scrapling_sellers:
        finder.scrapling_results = len(scrapling_sellers)
        print(f"✅ Scrapling found {len(scrapling_sellers)} sellers")
    else:
        print("ℹ️ No Scrapling results, will use API fallback")
    
    print()
    print(f"⏱️ Elapsed time: {finder.get_elapsed_time()}")
    
    # Return results for processing by main script
    results = {
        "scrapling_used": finder.scrapling_used,
        "scrapling_results": finder.scrapling_results,
        "api_results": finder.api_results,
        "elapsed_time": finder.get_elapsed_time(),
        "sellers": scrapling_sellers
    }
    
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
