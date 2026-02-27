#!/usr/bin/env python3
"""
Defense Sector Lead Gen - Scrapling-First Approach
"""

import sys
import os
import asyncio
import json
from datetime import datetime

# Add scrapling integration to path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

async def try_scrapling():
    """Try to use Scrapling for defense company search"""
    try:
        from cron_integration import ScraplingCronIntegration
        
        print("🔄 Initializing Scrapling...")
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if success:
            print("✅ Scrapling initialized successfully")
            
            # Search for defense companies
            search_terms = [
                "defense technology companies Series A B C funding",
                "cybersecurity companies military contracts",
                "counter-drone C-UAS technology startups",
                "space defense technology companies Europe",
                "military AI machine learning companies US UK"
            ]
            
            companies = await scrapling.scrape_defense_companies(search_terms)
            
            return {
                "success": True,
                "companies": companies,
                "count": len(companies) if companies else 0
            }
        else:
            print("⚠️ Scrapling initialization failed")
            return {"success": False, "companies": [], "count": 0}
            
    except ImportError as e:
        print(f"⚠️ Scrapling import error: {e}")
        return {"success": False, "companies": [], "count": 0}
    except Exception as e:
        print(f"⚠️ Scrapling error: {e}")
        return {"success": False, "companies": [], "count": 0}

if __name__ == "__main__":
    result = asyncio.run(try_scrapling())
    print(json.dumps(result, indent=2))
