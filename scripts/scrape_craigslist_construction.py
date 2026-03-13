#!/usr/bin/env python3
"""
Craigslist Construction Business Scraper
Scrapes 500+ construction businesses for sale nationwide
"""

import os
import sys
import json
import csv
import time
import random
from datetime import datetime
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
import re

class CraigslistConstructionScraper:
    def __init__(self):
        self.base_url = "https://craigslist.org"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Construction-related keywords
        self.keywords = [
            'construction', 'contractor', 'builder', 'general contractor',
            'construction company', 'construction business', 'contracting',
            'home builder', 'commercial construction', 'residential construction',
            'remodeling', 'renovation', 'construction firm', 'gc license',
            'construction license', 'licensed contractor'
        ]
        
        # Major US cities for nationwide search
        self.cities = [
            'newyork', 'losangeles', 'chicago', 'houston', 'phoenix',
            'philadelphia', 'sanantonio', 'sandiego', 'dallas', 'austin',
            'jacksonville', 'fortworth', 'columbus', 'charlotte', 'indianapolis',
            'sanfrancisco', 'seattle', 'denver', 'washington', 'boston',
            'elpaso', 'detroit', 'nashville', 'memphis', 'portland',
            'oklahomacity', 'lasvegas', 'louisville', 'baltimore', 'milwaukee',
            'albuquerque', 'tucson', 'fresno', 'sacramento', 'kansascity',
            'atlanta', 'miami', 'raleigh', 'omaha', 'minneapolis'
        ]
        
    def search_city(self, city: str, keyword: str) -> List[Dict]:
        """Search for listings in a specific city"""
        listings = []
        
        try:
            # Construct search URL
            search_url = f"https://{city}.craigslist.org/search/bfs?query={keyword}&sort=date"
            
            print(f"🔍 Searching {city} for '{keyword}'...")
            
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find listing containers
            result_containers = soup.find_all('li', class_='cl-static-search-result')
            
            if not result_containers:
                # Try alternative class names
                result_containers = soup.find_all('li', class_=re.compile(r'result-'))
            
            for container in result_containers[:20]:  # Limit to 20 per keyword
                listing = self.parse_listing(container, city)
                if listing:
                    listings.append(listing)
            
            # Random delay to avoid rate limiting
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            print(f"❌ Error searching {city} for '{keyword}': {e}")
        
        return listings
    
    def parse_listing(self, container, city: str) -> Dict:
        """Parse individual listing"""
        try:
            # Extract title
            title_elem = container.find('div', class_='title')
            if not title_elem:
                title_elem = container.find('a', class_=re.compile(r'title|result-title'))
            
            title = title_elem.text.strip() if title_elem else "No title"
            
            # Extract price
            price_elem = container.find('div', class_='price')
            if not price_elem:
                price_elem = container.find('span', class_=re.compile(r'price|result-price'))
            
            price_text = price_elem.text.strip() if price_elem else ""
            price = self.extract_price(price_text)
            
            # Extract location
            location_elem = container.find('div', class_='location')
            if not location_elem:
                location_elem = container.find('span', class_=re.compile(r'location|result-hood'))
            
            location = location_elem.text.strip() if location_elem else city
            
            # Extract link
            link_elem = container.find('a', href=True)
            link = link_elem['href'] if link_elem else ""
            if link and not link.startswith('http'):
                link = f"https://{city}.craigslist.org{link}"
            
            # Extract date
            date_elem = container.find('time')
            date = date_elem['datetime'] if date_elem and date_elem.has_attr('datetime') else ""
            
            # Check if it's construction-related
            if not self.is_construction_related(title):
                return None
            
            listing = {
                'title': title,
                'price': price,
                'location': f"{location}, {city.upper()}",
                'link': link,
                'date': date,
                'city': city,
                'source': 'craigslist',
                'scraped_at': datetime.now().isoformat(),
                'category': 'construction'
            }
            
            # Try to extract contact info from title/description
            contact_info = self.extract_contact_info(title)
            if contact_info:
                listing.update(contact_info)
            
            return listing
            
        except Exception as e:
            print(f"❌ Error parsing listing: {e}")
            return None
    
    def extract_price(self, price_text: str) -> str:
        """Extract price from text"""
        if not price_text:
            return ""
        
        # Look for dollar amounts
        match = re.search(r'\$([\d,]+)', price_text)
        if match:
            return f"${match.group(1)}"
        
        return price_text
    
    def extract_contact_info(self, text: str) -> Dict:
        """Extract phone and email from text"""
        contact_info = {}
        
        # Extract phone numbers
        phone_patterns = [
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
            r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\d{10}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                contact_info['phone'] = phones[0]
                break
        
        # Extract emails
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['email'] = emails[0]
        
        return contact_info
    
    def is_construction_related(self, text: str) -> bool:
        """Check if text is construction-related"""
        text_lower = text.lower()
        
        # Check for construction keywords
        for keyword in self.keywords:
            if keyword in text_lower:
                return True
        
        # Check for business-for-sale indicators
        business_indicators = ['for sale', 'selling', 'owner retiring', 'established', 'business opportunity']
        for indicator in business_indicators:
            if indicator in text_lower:
                return True
        
        return False
    
    def scrape_nationwide(self, target_count: int = 500) -> List[Dict]:
        """Scrape nationwide for construction businesses"""
        all_listings = []
        cities_scraped = 0
        
        print(f"🚀 Starting nationwide Craigslist scrape for construction businesses...")
        print(f"Target: {target_count} listings")
        print(f"Cities to search: {len(self.cities)}")
        print(f"Keywords: {', '.join(self.keywords[:5])}...")
        print("-" * 50)
        
        for city in self.cities:
            if len(all_listings) >= target_count:
                print(f"✅ Reached target of {target_count} listings!")
                break
            
            city_listings = []
            
            # Search with multiple keywords
            for keyword in self.keywords[:3]:  # Use top 3 keywords
                if len(all_listings) + len(city_listings) >= target_count:
                    break
                
                listings = self.search_city(city, keyword)
                city_listings.extend(listings)
                
                # Remove duplicates by title
                seen_titles = set()
                unique_listings = []
                for listing in city_listings:
                    if listing['title'] not in seen_titles:
                        seen_titles.add(listing['title'])
                        unique_listings.append(listing)
                
                city_listings = unique_listings
            
            if city_listings:
                all_listings.extend(city_listings)
                cities_scraped += 1
                print(f"✅ {city}: Found {len(city_listings)} construction businesses")
                print(f"   Total so far: {len(all_listings)} listings")
            
            # Progress update
            progress = min(100, int((len(all_listings) / target_count) * 100))
            print(f"📊 Progress: {progress}% ({len(all_listings)}/{target_count})")
            print("-" * 30)
        
        # Remove duplicates from all listings
        seen_titles = set()
        unique_listings = []
        for listing in all_listings:
            if listing['title'] not in seen_titles:
                seen_titles.add(listing['title'])
                unique_listings.append(listing)
        
        return unique_listings[:target_count]
    
    def save_to_csv(self, listings: List[Dict], filename: str = None):
        """Save listings to CSV file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"craigslist_construction_businesses_{timestamp}.csv"
        
        # Define CSV fields
        fields = [
            'title', 'price', 'location', 'city', 'phone', 'email',
            'link', 'date', 'source', 'category', 'scraped_at'
        ]
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
                writer.writeheader()
                
                for listing in listings:
                    # Ensure all fields are present
                    row = {field: listing.get(field, '') for field in fields}
                    writer.writerow(row)
            
            print(f"✅ CSV saved: {filename}")
            print(f"📊 Total listings saved: {len(listings)}")
            
            # Show file size
            file_size = os.path.getsize(filename) / 1024
            print(f"📁 File size: {file_size:.1f} KB")
            
            return filename
            
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")
            return None
    
    def print_summary(self, listings: List[Dict]):
        """Print summary of scraped data"""
        print("\n" + "="*60)
        print("📊 SCRAPE SUMMARY")
        print("="*60)
        
        print(f"Total listings: {len(listings)}")
        
        # Price analysis
        prices = []
        for listing in listings:
            if listing['price'] and listing['price'].startswith('$'):
                try:
                    price_num = int(listing['price'].replace('$', '').replace(',', ''))
                    prices.append(price_num)
                except:
                    pass
        
        if prices:
            avg_price = sum(prices) / len(prices)
            print(f"Average asking price: ${avg_price:,.0f}")
            print(f"Price range: ${min(prices):,.0f} - ${max(prices):,.0f}")
        
        # Location distribution
        locations = {}
        for listing in listings:
            city = listing['city']
            locations[city] = locations.get(city, 0) + 1
        
        print(f"\n📍 Top locations:")
        sorted_locations = sorted(locations.items(), key=lambda x: x[1], reverse=True)[:5]
        for city, count in sorted_locations:
            print(f"  {city}: {count} listings")
        
        # Contact info stats
        phones = sum(1 for l in listings if l.get('phone'))
        emails = sum(1 for l in listings if l.get('email'))
        print(f"\n📞 Contact information:")
        print(f"  Phone numbers: {phones} ({phones/len(listings)*100:.1f}%)")
        print(f"  Email addresses: {emails} ({emails/len(listings)*100:.1f}%)")
        
        print("\n📋 Sample listings:")
        for i, listing in enumerate(listings[:3]):
            print(f"\n{i+1}. {listing['title'][:60]}...")
            print(f"   Price: {listing['price']}")
            print(f"   Location: {listing['location']}")
            if listing.get('phone'):
                print(f"   Phone: {listing['phone']}")
            if listing.get('email'):
                print(f"   Email: {listing['email']}")

def main():
    """Main function"""
    print("🏗️ CRAIGSLIST CONSTRUCTION BUSINESS SCRAPER")
    print("="*50)
    
    # Create scraper
    scraper = CraigslistConstructionScraper()
    
    # Scrape nationwide
    target_count = 500
    print(f"\n🎯 Target: {target_count} construction businesses nationwide")
    print("⏳ This may take 10-15 minutes...")
    print("\nStarting scrape...")
    
    listings = scraper.scrape_nationwide(target_count=target_count)
    
    if not listings:
        print("❌ No listings found. Exiting.")
        return
    
    # Save to CSV
    csv_file = scraper.save_to_csv(listings)
    
    # Print summary
    scraper.print_summary(listings)
    
    print(f"\n✅ Scrape completed successfully!")
    print(f"📁 Output file: {csv_file}")
    print(f"🔗 Full path: {os.path.abspath(csv_file)}")
    
    # Show next steps
    print("\n🚀 NEXT STEPS:")
    print("1. Review the CSV file for quality")
    print("2. Import into your CRM or email system")
    print("3. Use for lead generation campaigns")
    print("4. Run the scraper daily for fresh leads")

if __name__ == "__main__":
    main()