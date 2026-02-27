#!/usr/bin/env python3
"""
Test Craigslist scraper with minimal functionality
"""

import craigslistscraper as cs
import json
from datetime import datetime

def test_scraper():
    """Test the Craigslist scraper"""
    
    print("Testing CraigslistScraper...")
    
    # Test 1: Business for sale in NYC
    print("\n1. Testing Business-for-Sale (biz) in New York...")
    try:
        search = cs.Search(
            city="newyork",
            category="biz",
            query=""
        )
        
        status = search.fetch()
        print(f"   Status: {status}")
        print(f"   Found {len(search.ads)} ads")
        
        if search.ads:
            # Get first ad
            ad = search.ads[0]
            ad_status = ad.fetch()
            if ad_status == 200:
                data = ad.to_dict()
                print(f"   First ad: {data.get('title', 'Unknown')}")
                print(f"   Price: {data.get('price', 'N/A')}")
                print(f"   Location: {data.get('location', 'N/A')}")
            else:
                print(f"   Failed to fetch ad: HTTP {ad_status}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Skilled trade services in NYC
    print("\n2. Testing Skilled Trade (sks) in New York...")
    try:
        search = cs.Search(
            city="newyork",
            category="sks",
            query=""
        )
        
        status = search.fetch()
        print(f"   Status: {status}")
        print(f"   Found {len(search.ads)} ads")
        
        if search.ads:
            # Get first ad
            ad = search.ads[0]
            ad_status = ad.fetch()
            if ad_status == 200:
                data = ad.to_dict()
                print(f"   First ad: {data.get('title', 'Unknown')}")
                print(f"   Price: {data.get('price', 'N/A')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\nTest complete!")

if __name__ == "__main__":
    test_scraper()