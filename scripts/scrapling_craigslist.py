#!/usr/bin/env python3
"""
Craigslist Construction Business Scraper using Scrapling
More robust scraping with anti-bot bypass and adaptive parsing
"""

import os
import sys
import json
import csv
import time
import random
from datetime import datetime
from typing import List, Dict, Any
from urllib.parse import urljoin, quote_plus

from scrapling.fetchers import StealthyFetcher, DynamicFetcher
from scrapling.parsers import Parser

class ScraplingCraigslistScraper:
    def __init__(self):
        # Configure Scrapling fetcher
        StealthyFetcher.adaptive = True  # Enable adaptive mode
        self.fetcher = StealthyFetcher()
        
        # Construction-related keywords
        self.keywords = [
            'construction', 'contractor', 'builder', 'general contractor',
            'construction company', 'construction business', 'contracting',
            'home builder', 'commercial construction', 'residential construction',
            'remodeling', 'renovation', 'construction firm'
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
        
        # Results storage
        self.listings = []
        self.seen_urls = set()
        
    def search_city(self, city: str, keyword: str, max_results: int = 20) -> List[Dict]:
        """Search for listings in a specific city using Scrapling"""
        city_listings = []
        
        try:
            # Construct search URL
            search_url = f"https://{city}.craigslist.org/search/bfs?query={quote_plus(keyword)}&sort=date"
            
            print(f"🔍 Searching {city} for '{keyword}'...")
            
            # Use Scrapling's stealthy fetcher to bypass anti-bot measures
            page = self.fetcher.fetch(
                search_url,
                headless=True,  # Use headless browser for JavaScript rendering
                network_idle=True,  # Wait for network to be idle
                timeout=30
            )
            
            # Use adaptive parsing to handle website changes
            parser = Parser(page.html, adaptive=True)
            
            # Find listing containers - Scrapling will adapt if CSS selectors change
            listings = parser.css('li.cl-static-search-result, li.result-row, li.result-item')
            
            if not listings:
                # Try alternative selectors
                listings = parser.css('[data-pid], .result-info, .search-result')
            
            for listing_elem in listings[:max_results]:
                listing = self.parse_listing(listing_elem, city)
                if listing and listing['url'] not in self.seen_urls:
                    self.seen_urls.add(listing['url'])
                    city_listings.append(listing)
            
            # Random delay to avoid rate limiting
            delay = random.uniform(2, 5)
            time.sleep(delay)
            
        except Exception as e:
            print(f"❌ Error searching {city} for '{keyword}': {str(e)[:100]}...")
            # Try with dynamic fetcher as fallback
            try:
                print(f"   Trying dynamic fetcher as fallback...")
                dynamic_fetcher = DynamicFetcher()
                page = dynamic_fetcher.fetch(search_url, timeout=20)
                # Parse with dynamic fetcher results...
            except:
                pass
        
        return city_listings
    
    def parse_listing(self, listing_elem, city: str) -> Dict:
        """Parse individual listing using Scrapling's adaptive parsing"""
        try:
            # Create parser for this listing element
            parser = Parser(str(listing_elem), adaptive=True)
            
            # Extract title - Scrapling will find the right selector
            title = parser.css_first('.title, .result-title, a[class*="title"]')
            title_text = title.text().strip() if title else "No title"
            
            # Extract price
            price = parser.css_first('.price, .result-price, .priceinfo')
            price_text = price.text().strip() if price else ""
            
            # Extract location
            location = parser.css_first('.location, .result-hood, .nearby')
            location_text = location.text().strip() if location else city
            
            # Extract link
            link = parser.css_first('a[href]')
            link_url = link.attr('href') if link else ""
            if link_url and not link_url.startswith('http'):
                link_url = f"https://{city}.craigslist.org{link_url}"
            
            # Extract date
            date_elem = parser.css_first('time, .result-date')
            date_text = date_elem.attr('datetime') if date_elem and date_elem.has_attr('datetime') else ""
            if not date_text and date_elem:
                date_text = date_elem.text().strip()
            
            # Check if it's construction-related
            if not self.is_construction_related(title_text):
                return None
            
            # Create listing object
            listing = {
                'title': title_text,
                'price': self.clean_price(price_text),
                'location': f"{self.clean_location(location_text)}, {city.upper()}",
                'url': link_url,
                'date': date_text,
                'city': city,
                'source': 'craigslist',
                'category': 'construction',
                'scraped_at': datetime.now().isoformat()
            }
            
            # If we have a link, try to fetch details for contact info
            if link_url and 'craigslist.org' in link_url:
                contact_info = self.extract_contact_details(link_url)
                if contact_info:
                    listing.update(contact_info)
            
            return listing
            
        except Exception as e:
            print(f"❌ Error parsing listing: {str(e)[:50]}...")
            return None
    
    def extract_contact_details(self, url: str) -> Dict:
        """Extract contact details from listing page"""
        contact_info = {}
        
        try:
            # Use dynamic fetcher for listing pages (might have more JavaScript)
            dynamic_fetcher = DynamicFetcher()
            page = dynamic_fetcher.fetch(url, timeout=15)
            
            parser = Parser(page.html, adaptive=True)
            
            # Try to find contact information
            # Look for phone numbers in the page
            phone_patterns = [
                r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
                r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
                r'\d{10}'
            ]
            
            page_text = parser.text()
            for pattern in phone_patterns:
                import re
                phones = re.findall(pattern, page_text)
                if phones:
                    contact_info['phone'] = phones[0]
                    break
            
            # Look for email addresses
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            emails = re.findall(email_pattern, page_text)
            if emails:
                contact_info['email'] = emails[0]
            
            # Look for reply button/link
            reply_link = parser.css_first('a[href*="mailto"], .reply-button, .contact')
            if reply_link:
                href = reply_link.attr('href')
                if href and 'mailto:' in href:
                    contact_info['email'] = href.replace('mailto:', '')
            
            # Short delay before next request
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            # Silently fail - contact extraction is optional
            pass
        
        return contact_info
    
    def clean_price(self, price_text: str) -> str:
        """Clean and format price"""
        if not price_text:
            return ""
        
        # Remove extra whitespace and normalize
        price_text = price_text.strip()
        
        # Ensure it starts with $ if it's a price
        if any(c.isdigit() for c in price_text) and not price_text.startswith('$'):
            # Try to extract numeric price
            import re
            match = re.search(r'(\$?\d[\d,\.]*)', price_text)
            if match:
                price = match.group(1)
                if not price.startswith('$'):
                    price = f"${price}"
                return price
        
        return price_text
    
    def clean_location(self, location_text: str) -> str:
        """Clean location text"""
        if not location_text:
            return ""
        
        # Remove common prefixes and clean up
        location = location_text.strip()
        location = location.replace('(','').replace(')','').strip()
        
        # Capitalize first letter of each word
        location = ' '.join(word.capitalize() for word in location.split())
        
        return location
    
    def is_construction_related(self, text: str) -> bool:
        """Check if text is construction-related"""
        text_lower = text.lower()
        
        # Check for construction keywords
        construction_keywords = [
            'construction', 'contractor', 'builder', 'general contractor',
            'remodel', 'renovation', 'home improvement', 'construction company',
            'licensed contractor', 'gc license', 'construction business',
            'commercial construction', 'residential construction'
        ]
        
        for keyword in construction_keywords:
            if keyword in text_lower:
                return True
        
        # Check for business-for-sale indicators
        business_indicators = ['for sale', 'selling', 'owner retiring', 'established business', 'business opportunity']
        for indicator in business_indicators:
            if indicator in text_lower:
                # Double-check it's not just equipment
                equipment_terms = ['equipment', 'tool', 'machine', 'vehicle', 'truck']
                if not any(term in text_lower for term in equipment_terms):
                    return True
        
        return False
    
    def scrape_nationwide(self, target_count: int = 500) -> List[Dict]:
        """Scrape nationwide for construction businesses"""
        print(f"🚀 Starting nationwide Craigslist scrape using Scrapling...")
        print(f"Target: {target_count} construction businesses")
        print(f"Cities to search: {len(self.cities)}")
        print(f"Keywords: {', '.join(self.keywords[:5])}...")
        print("=" * 60)
        
        total_scraped = 0
        cities_scraped = 0
        
        for city_idx, city in enumerate(self.cities):
            if total_scraped >= target_count:
                print(f"✅ Reached target of {target_count} listings!")
                break
            
            print(f"\n📍 City {city_idx + 1}/{len(self.cities)}: {city.upper()}")
            
            city_listings = []
            
            # Search with multiple keywords
            for keyword_idx, keyword in enumerate(self.keywords[:3]):  # Use top 3 keywords
                if total_scraped + len(city_listings) >= target_count:
                    break
                
                print(f"   Keyword {keyword_idx + 1}/3: '{keyword}'")
                listings = self.search_city(city, keyword, max_results=15)
                city_listings.extend(listings)
                
                # Update progress
                current_total = total_scraped + len(city_listings)
                progress = min(100, int((current_total / target_count) * 100))
                print(f"   Progress: {progress}% ({current_total}/{target_count})")
            
            # Remove duplicates within this city
            unique_city_listings = []
            seen_titles = set()
            for listing in city_listings:
                if listing['title'] not in seen_titles:
                    seen_titles.add(listing['title'])
                    unique_city_listings.append(listing)
            
            if unique_city_listings:
                self.listings.extend(unique_city_listings)
                total_scraped = len(self.listings)
                cities_scraped += 1
                
                print(f"✅ {city}: Found {len(unique_city_listings)} unique construction businesses")
                print(f"📊 Total so far: {total_scraped} listings")
            
            print("-" * 40)
        
        # Final deduplication
        final_listings = []
        seen_urls = set()
        for listing in self.listings:
            if listing['url'] not in seen_urls:
                seen_urls.add(listing['url'])
                final_listings.append(listing)
        
        return final_listings[:target_count]
    
    def save_to_csv(self, listings: List[Dict], filename: str = None):
        """Save listings to CSV file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"scrapling_craigslist_construction_{timestamp}.csv"
        
        # Define CSV fields
        fields = [
            'title', 'price', 'location', 'city', 'phone', 'email',
            'url', 'date', 'source', 'category', 'scraped_at'
        ]
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
                writer.writeheader()
                
                for listing in listings:
                    # Ensure all fields are present
                    row = {field: listing.get(field, '') for field in fields}
                    writer.writerow(row)
            
            print(f"\n✅ CSV saved: {filename}")
            print(f"📊 Total listings saved: {len(listings)}")
            
            # Show file size
            file_size = os.path.getsize(filename) / 1024
            print(f"📁 File size: {file_size:.1f} KB")
            print(f"🔗 Full path: {os.path.abspath(filename)}")
            
            return filename
            
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")
            return None
    
    def print_summary(self, listings: List[Dict]):
        """Print summary of scraped data"""
        print("\n" + "="*60)
        print("📊 SCRAPING SUMMARY (Using Scrapling)")
        print("="*60)
        
        print(f"Total unique listings: {len(listings)}")
        
        # Price analysis
        prices = []
        for listing in listings:
            price = listing['price']
            if price and price.startswith('$'):
                try:
                    # Remove $ and commas, convert to int
                    price_num = int(price.replace('$', '').replace(',', ''))
                    prices.append(price_num)
                except:
                    pass
        
        if prices:
            avg_price = sum(prices) / len(prices)
            print(f"\n💰 Price Analysis:")
            print(f"   Average asking price: ${avg_price:,.0f}")
            print(f"   Price range: ${min(prices):,.0f} - ${max(prices):,.0f}")
            print(f"   Number of priced listings: {len(prices)}")
        
        # Location distribution
        from collections import Counter
        cities = Counter([listing['city'] for listing in listings])
        
        print(f"\n📍 Top 5 Cities:")
        for city, count in cities.most_common(5):
            print(f"   {city.upper()}: {count} listings")
        
        # Contact info stats
        phones = sum(1 for l in listings if l.get('phone'))
        emails = sum(1 for l in listings if l.get('email'))
        
        print(f"\n📞 Contact Information Found:")
        print(f"   Phone numbers: {phones} ({phones/len(listings)*100:.1f}%)")
        print(f"   Email addresses: {emails} ({emails/len(listings)*100:.1f}%)")
        
        print("\n📋 Sample Listings:")
        for i, listing in enumerate(listings[:3]):
            print(f"\n{i+1}. {listing['title'][:70]}...")
            print(f"   Price: {listing['price']}")
            print(f"   Location: {listing['location']}")
            if listing.get('phone'):
                print(f"   Phone: {listing['phone']}")
            if listing.get('email'):
                print(f"   Email: {listing['email']}")
            print(f"   URL: {listing['url'][:60]}...")

def main():
    """Main function"""
    print("🏗️ CRAIGSLIST CONSTRUCTION BUSINESS SCRAPER (Using Scrapling)")
    print("="*60)
    print("Features:")
    print("  • Anti-bot bypass with StealthyFetcher")
    print("  • Adaptive parsing that survives website changes")
    print("  • JavaScript rendering for dynamic content")
    print("  • Contact details extraction from listing pages")
    print("="*60)
    
    # Create scraper
    scraper = ScraplingCraigslistScraper()
    
    # Scrape nationwide
    target_count = 500
    print(f"\n🎯 Target: {target_count} construction businesses nationwide")
    print("⏳ Estimated time: 15-25 minutes (due to anti-bot delays)")
    print("\nStarting scrape in 3 seconds...")
    time.sleep(3)
    
    listings = scraper.scrape_nationwide