#!/usr/bin/env python3
"""
Defense Sector Lead Generation - Scrapling-First Approach
Runs daily to find defense companies and PE/VC investors
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import List, Dict, Any

# Add scrapling integration path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# Try to import Scrapling
try:
    from cron_integration import ScraplingCronIntegration
    SCRAPLING_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Scrapling import failed: {e}")
    SCRAPLING_AVAILABLE = False

class DefenseSectorLeadGen:
    """Defense sector lead generation with Scrapling-first approach."""
    
    def __init__(self):
        self.scrapling_used = False
        self.scrapling_results = 0
        self.api_results = 0
        self.start_time = datetime.now()
        
    async def run_with_scrapling(self) -> List[Dict[str, Any]]:
        """Try to use Scrapling for defense company search."""
        if not SCRAPLING_AVAILABLE:
            print("⚠️ Scrapling not available, skipping")
            return []
        
        try:
            print("🔧 Initializing Scrapling with stealth mode...")
            scrapling = ScraplingCronIntegration(stealth_mode=True)
            success = await scrapling.initialize()
            
            if not success:
                print("❌ Scrapling initialization failed")
                return []
            
            print("✅ Scrapling initialized successfully")
            
            # Search terms for defense companies
            search_terms = [
                "defense technology companies",
                "cybersecurity companies military",
                "drone technology defense",
                "space defense technology",
                "military AI companies"
            ]
            
            companies = await scrapling.scrape_defense_companies(search_terms)
            
            if companies:
                self.scrapling_used = True
                self.scrapling_results = len(companies)
                print(f"✅ Scrapling found {len(companies)} companies")
                return companies
            else:
                print("⚠️ Scrapling returned no results")
                return []
                
        except Exception as e:
            print(f"❌ Scrapling error: {e}")
            return []
    
    async def run_with_tavily(self) -> List[Dict[str, Any]]:
        """Fall back to Tavily API for defense company search."""
        print("🔍 Using Tavily API as fallback...")
        
        # In real implementation, this would call Tavily API
        # For now, we'll return simulated results
        print("⚠️ Tavily integration not implemented in this script")
        return []
    
    async def search_defense_companies(self) -> List[Dict[str, Any]]:
        """Search for defense companies using Scrapling-first approach."""
        # Try Scrapling first
        companies = await self.run_with_scrapling()
        
        # If Scrapling fails or returns no results, use Tavily
        if not companies:
            companies = await self.run_with_tavily()
            self.api_results = len(companies)
        
        return companies
    
    def get_processing_time(self) -> str:
        """Calculate processing time."""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        return f"{elapsed:.1f}"

async def main():
    """Main execution function."""
    print("=" * 60)
    print("🛡️ Defense Sector Lead Generation - Scrapling-First")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    lead_gen = DefenseSectorLeadGen()
    
    # Search for defense companies
    print("📋 Part 1: Searching for Defense Companies (US/UK/EU)")
    print("-" * 60)
    companies = await lead_gen.search_defense_companies()
    
    print()
    print("=" * 60)
    print("📊 Results Summary")
    print("=" * 60)
    print(f"Scrapling Used: {'✅ Yes' if lead_gen.scrapling_used else '❌ No'}")
    print(f"Scrapling Results: {lead_gen.scrapling_results}")
    print(f"API Results: {lead_gen.api_results}")
    print(f"Total Companies Found: {len(companies)}")
    print(f"Processing Time: {lead_gen.get_processing_time()} seconds")
    
    return {
        "companies": companies,
        "scrapling_used": lead_gen.scrapling_used,
        "scrapling_results": lead_gen.scrapling_results,
        "api_results": lead_gen.api_results,
        "processing_time": lead_gen.get_processing_time()
    }

if __name__ == "__main__":
    results = asyncio.run(main())
    print(json.dumps(results, indent=2, default=str))
