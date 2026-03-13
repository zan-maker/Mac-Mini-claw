#!/usr/bin/env python3
"""
Simple Craigslist scraper using Scrapling's basic features
"""

import csv
import time
import random
from datetime import datetime
from scrapling import Scraper

class SimpleCraigslistScraper:
    def __init__(self):
        self.scraper = Scraper()
        self.results = []
        
        # Major US cities
        self.cities = [
            'newyork', 'losangeles', 'chicago', 'houston', 'phoenix',
            'philadelphia', 'sanantonio', 'sandiego', 'dallas', 'austin'
        ]
        
        # Construction keywords
        self.keywords = ['construction', 'contractor', 'builder']
    
    def scrape_city(self, city, keyword):
        """Scrape a single city for a keyword"""
        url = f"https://{city}.craigslist.org/search/bfs?query={keyword}&sort=date"
        
        print(f"🔍 {city}: Searching for '{keyword}'...")
        
        try:
            # Use Scrapling to fetch and parse
            response = self.scraper.get(url)
            
            # Extract listings - Craigslist structure
            listings = []
            
            # Method 1: Try data-pid attribute (common Craigslist pattern)
            for item in response.html.find('[data-pid]'):
                listing = self.parse_listing(item, city)
                if listing:
                    listings.append(listing)
            
            # Method 2: Try result-row class
            if not listings:
                for item in response.html.find('.result-row'):
                    listing = self.parse_listing(item, city)
                    if listing:
                        listings.append(listing)
            
            # Method 3: Try cl-static-search-result (newer Craigslist)
            if not listings:
                for item in response.html.find('.cl-static-search-result'):
                    listing = self.parse_listing(item, city)
                    if listing:
                        listings.append(listing)
            
            print(f"   Found {len(listings)} listings")
            return listings
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:80]}...")
            return []
    
    def parse_listing(self, item, city):
        """Parse a single listing item"""
        try:
            # Extract title
            title_elem = item.find('.result-title, .title', first=True)
            title = title_elem.text.strip() if title_elem else "No title"
            
            # Extract price
            price_elem = item.find('.result-price, .price', first=True)
            price = price_elem.text.strip() if price_elem else ""
            
            # Extract location
            location_elem = item.find('.result-hood, .location', first=True)
            location = location_elem.text.strip() if location_elem else city
            
            # Extract link
            link_elem = item.find('a[href]', first=True)
            link = link_elem.attrs.get('href', '') if link_elem else ""
            if link and not link.startswith('http'):
                link = f"https://{city}.craigslist.org{link}"
            
            # Extract date
            date_elem = item.find('time', first=True)
            date = date_elem.attrs.get('datetime', '') if date_elem else ""
            
            # Check if construction-related
            if not self.is_construction_related(title):
                return None
            
            return {
                'title': title,
                'price': price,
                'location': f"{location}, {city.upper()}",
                'url': link,
                'date': date,
                'city': city,
                'source': 'craigslist',
                'category': 'construction',
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return None
    
    def is_construction_related(self, text):
        """Check if text is construction-related"""
        text_lower = text.lower()
        keywords = ['construction', 'contractor', 'builder', 'remodel', 'renovation']
        return any(keyword in text_lower for keyword in keywords)
    
    def scrape(self, target_count=100):
        """Main scraping function"""
        print("🚀 Starting Craigslist construction business scrape...")
        print(f"Target: {target_count} listings")
        print(f"Cities: {len(self.cities)}")
        print("="*60)
        
        all_listings = []
        
        for city in self.cities:
            if len(all_listings) >= target_count:
                break
            
            city_listings = []
            for keyword in self.keywords:
                if len(all_listings) + len(city_listings) >= target_count:
                    break
                
                listings = self.scrape_city(city, keyword)
                city_listings.extend(listings)
                
                # Remove duplicates by URL
                seen_urls = set()
                unique_listings = []
                for listing in city_listings:
                    if listing['url'] not in seen_urls:
                        seen_urls.add(listing['url'])
                        unique_listings.append(listing)
                
                city_listings = unique_listings
            
            if city_listings:
                all_listings.extend(city_listings)
                print(f"✅ {city}: Added {len(city_listings)} unique listings")
                print(f"📊 Total: {len(all_listings)}/{target_count}")
            
            # Random delay between cities
            time.sleep(random.uniform(2, 4))
        
        # Final deduplication
        seen_urls = set()
        final_listings = []
        for listing in all_listings:
            if listing['url'] not in seen_urls:
                seen_urls.add(listing['url'])
                final_listings.append(listing)
        
        return final_listings[:target_count]
    
    def save_csv(self, listings, filename=None):
        """Save results to CSV"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"craigslist_construction_{timestamp}.csv"
        
        fields = ['title', 'price', 'location', 'city', 'url', 'date', 'source', 'category', 'scraped_at']
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for listing in listings:
                writer.writerow(listing)
        
        print(f"\n✅ Saved {len(listings)} listings to {filename}")
        return filename

def main():
    """Main function"""
    print("🏗️ Simple Craigslist Construction Business Scraper")
    print("Using Scrapling framework")
    print("="*50)
    
    scraper = SimpleCraigslistScraper()
    
    # Scrape 100 listings (quick test)
    target = 100
    print(f"\n🎯 Target: {target} construction businesses")
    print("⏳ Starting scrape...")
    
    listings = scraper.scrape(target_count=target)
    
    if not listings:
        print("❌ No listings found. Exiting.")
        return
    
    # Save results
    filename = scraper.save_csv(listings)
    
    # Print summary
    print("\n📊 SUMMARY:")
    print(f"Total listings: {len(listings)}")
    
    # Count by city
    from collections import Counter
    city_counts = Counter([l['city'] for l in listings])
    print("\n📍 Listings by city:")
    for city, count in city_counts.most_common():
        print(f"  {city.upper()}: {count}")
    
    # Sample listings
    print("\n📋 Sample listings:")
    for i, listing in enumerate(listings[:3]):
        print(f"\n{i+1}. {listing['title'][:60]}...")
        print(f"   Price: {listing['price']}")
        print(f"   Location: {listing['location']}")
        print(f"   URL: {listing['url'][:50]}...")
    
    print(f"\n✅ Done! File: {filename}")

if __name__ == "__main__":
    main()