#!/usr/bin/env python3
"""
Test Scrapling for finding off-market business sellers
"""
import asyncio
import sys

sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

try:
    from cron_integration import ScraplingCronIntegration
    
    async def test_scrapling():
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if success:
            print("✅ Scrapling initialized successfully")
            
            # Try the find_off_market_sellers method if it exists
            if hasattr(scrapling, 'find_off_market_sellers'):
                search_terms = [
                    "HVAC business for sale owner retiring",
                    "plumbing company owner retirement",
                    "electrical contractor business sale"
                ]
                sellers = await scrapling.find_off_market_sellers(search_terms)
                print(f"Found {len(sellers)} sellers")
                return sellers
            else:
                print("⚠️ find_off_market_sellers method not available")
                return None
        else:
            print("❌ Scrapling initialization failed")
            return None
    
    results = asyncio.run(test_scrapling())
    if results is None:
        sys.exit(1)
    else:
        print(json.dumps(results, indent=2))
        sys.exit(0)
        
except ImportError as e:
    print(f"⚠️ Scrapling not available: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
