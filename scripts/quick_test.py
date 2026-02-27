#!/usr/bin/env python3
"""
Quick test of Craigslist scraper
"""

import craigslistscraper as cs
import json
from datetime import datetime

print("Quick test of CraigslistScraper...")
print(f"Time: {datetime.now().strftime('%H:%M:%S')}")

# Test with minimal ads
try:
    search = cs.Search(
        city="newyork",
        category="biz",
        query=""
    )
    
    print("Fetching search results...")
    status = search.fetch()
    print(f"Status: {status}")
    
    if status == 200:
        print(f"Total ads found: {len(search.ads)}")
        
        # Just look at first 2 ads
        for i, ad in enumerate(search.ads[:2]):
            print(f"\nAd {i+1}:")
            ad_status = ad.fetch()
            print(f"  Ad fetch status: {ad_status}")
            
            if ad_status == 200:
                data = ad.to_dict()
                print(f"  Title: {data.get('title', 'N/A')[:50]}...")
                print(f"  Price: {data.get('price', 'N/A')}")
                print(f"  Has description: {'Yes' if data.get('description') else 'No'}")
            else:
                print(f"  Failed to fetch ad details")
    
    print("\nTest completed successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()