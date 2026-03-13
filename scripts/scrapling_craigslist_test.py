#!/usr/bin/env python3
"""
Quick test of Scrapling Craigslist scraper
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapling_craigslist import ScraplingCraigslistScraper
import time

def quick_test():
    """Quick test with 2 cities"""
    print("🧪 Testing Scrapling Craigslist Scraper...")
    print("="*50)
    
    scraper = ScraplingCraigslistScraper()
    
    # Test with just 2 cities for speed
    test_cities = ['newyork', 'losangeles']
    scraper.cities = test_cities
    
    print(f"Testing with cities: {', '.join(test_cities)}")
    print("Using keyword: 'construction'")
    print("-"*50)
    
    test_listings = []
    
    for city in test_cities:
        print(f"\n🔍 Testing {city}...")
        try:
            listings = scraper.search_city(city, 'construction', max_results=5)
            test_listings.extend(listings)
            print(f"   Found {len(listings)} listings")
            
            if listings:
                print("   Sample:")
                for i, listing in enumerate(listings[:2]):
                    print(f"     {i+1}. {listing['title'][:50]}...")
                    print(f"        Price: {listing['price']}")
                    print(f"        Location: {listing['location']}")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}...")
        
        time.sleep(2)
    
    print("\n" + "="*50)
    print(f"✅ Test completed!")
    print(f"Total listings found: {len(test_listings)}")
    
    if test_listings:
        # Save test results
        import csv
        from datetime import datetime
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"scrapling_test_{timestamp}.csv"
        
        fields = ['title', 'price', 'location', 'city', 'url', 'date', 'source', 'category']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for listing in test_listings:
                row = {field: listing.get(field, '') for field in fields}
                writer.writerow(row)
        
        print(f"📁 Test results saved to: {filename}")
        print(f"🔗 Full path: {os.path.abspath(filename)}")
    
    return len(test_listings) > 0

if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1)