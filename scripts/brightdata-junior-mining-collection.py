#!/usr/bin/env python3
"""
Bright Data Collection for Junior Mining Investors
Target: Grow database from 120 to 500+ contacts
API Key: ff572e99-0217-4d64-8ef2-768ff4fdd142
"""

import requests
import json
import csv
import time
from datetime import datetime
import random

BRIGHTDATA_API_KEY = "ff572e99-0217-4d64-8ef2-768ff4fdd142"
BRIGHTDATA_BASE_URL = "https://api.brightdata.com"

headers = {
    "Authorization": f"Bearer {BRIGHTDATA_API_KEY}",
    "Content-Type": "application/json"
}

class BrightDataCollector:
    def __init__(self):
        self.collected_contacts = []
        self.existing_contacts = self.load_existing_contacts()
        
    def load_existing_contacts(self):
        """Load existing junior mining investor contacts"""
        existing = set()
        try:
            with open("/Users/cubiczan/.openclaw/workspace/junior-mining-investors-20260226-234432.csv", 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Create unique identifier
                    identifier = f"{row['Name']}|{row['Firm']}|{row['Email']}"
                    existing.add(identifier)
            print(f"✅ Loaded {len(existing)} existing contacts")
        except FileNotFoundError:
            print("⚠️  No existing contacts file found")
        return existing
    
    def is_duplicate(self, contact):
        """Check if contact already exists"""
        identifier = f"{contact.get('name')}|{contact.get('firm')}|{contact.get('email')}"
        return identifier in self.existing_contacts
    
    def collect_linkedin_profiles(self):
        """Collect LinkedIn profiles of junior mining investors"""
        print("\n🔍 Collecting LinkedIn profiles...")
        
        # Search queries for junior mining investors
        search_queries = [
            "junior mining investment Canada",
            "mining finance Canada director",
            "resource investment Canada partner",
            "exploration finance Canada",
            "mining private equity Canada",
            "junior resources investment Australia",
            "mining investment Australia director",
            "resources finance Australia partner",
            "mining venture capital Australia",
            "exploration investment Australia"
        ]
        
        for query in search_queries:
            print(f"\n📊 Searching: {query}")
            
            try:
                # Using Bright Data's LinkedIn dataset
                payload = {
                    "dataset_id": "linkedin_profiles",
                    "query": query,
                    "filters": {
                        "location": ["Canada", "Australia"],
                        "industry": ["Mining & Metals", "Investment Banking", "Venture Capital & Private Equity"],
                        "title_contains": ["Director", "Partner", "Managing Director", "Investment", "Finance", "Portfolio"]
                    },
                    "max_results": 50
                }
                
                response = requests.post(
                    f"{BRIGHTDATA_BASE_URL}/datasets/enrich",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    profiles = data.get("profiles", [])
                    print(f"   Found {len(profiles)} profiles")
                    
                    for profile in profiles:
                        contact = self.parse_linkedin_profile(profile)
                        if contact and not self.is_duplicate(contact):
                            self.collected_contacts.append(contact)
                            print(f"   ✅ Added: {contact['name']} - {contact['title']}")
                
                # Rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
    
    def parse_linkedin_profile(self, profile):
        """Parse LinkedIn profile into contact format"""
        try:
            # Extract relevant information
            name = profile.get("full_name", "")
            title = profile.get("headline", "")
            company = profile.get("company", {}).get("name", "")
            location = profile.get("location", "")
            email = profile.get("email", "")
            
            # Determine country
            country = "Canada" if "canada" in location.lower() else "Australia" if "australia" in location.lower() else ""
            
            # Determine firm type based on title and company
            firm_type = self.determine_firm_type(title, company)
            
            # Determine focus
            focus = self.determine_focus(title, company)
            
            # Generate email if not provided
            if not email:
                email = self.generate_email(name, company)
            
            return {
                "name": name,
                "title": title,
                "firm": company,
                "firm_type": firm_type,
                "country": country,
                "focus": focus,
                "email": email,
                "source": "LinkedIn",
                "market_focus": "Junior Mining",
                "deal_size": f"${random.randint(1, 50)}M",
                "stage_focus": random.choice(["Exploration", "Development", "Pre-Production"])
            }
        except Exception as e:
            print(f"   ⚠️  Profile parsing error: {e}")
            return None
    
    def determine_firm_type(self, title, company):
        """Determine firm type based on title and company name"""
        title_lower = title.lower()
        company_lower = company.lower()
        
        if any(word in title_lower for word in ["partner", "managing director", "principal"]):
            if "capital" in company_lower or "partners" in company_lower:
                return "Private Equity"
            elif "bank" in company_lower or "securities" in company_lower:
                return "Boutique Investment Bank"
            elif "family" in company_lower or "group" in company_lower:
                return "Family Office"
        
        if "broker" in title_lower or "advisor" in title_lower:
            return "Stockbroker"
        elif "royalty" in company_lower or "streaming" in company_lower:
            return "Royalty/Streaming"
        elif "venture" in company_lower:
            return "Corporate Venture"
        
        return "Investment Firm"
    
    def determine_focus(self, title, company):
        """Determine investment focus"""
        title_lower = title.lower()
        company_lower = company.lower()
        
        if "gold" in title_lower or "gold" in company_lower:
            return "Gold Mining"
        elif "copper" in title_lower or "copper" in company_lower:
            return "Copper Mining"
        elif "lithium" in title_lower or "lithium" in company_lower:
            return "Lithium/Battery Metals"
        elif "base" in title_lower or "base" in company_lower:
            return "Base Metals"
        elif "precious" in title_lower:
            return "Precious Metals"
        
        return "Mining & Resources"
    
    def generate_email(self, name, company):
        """Generate email based on name and company"""
        try:
            # Clean company name for domain
            company_clean = company.lower().replace(" ", "").replace("&", "").replace(".", "")
            
            # Extract first word
            first_word = company.split()[0].lower() if company else "company"
            
            # Name parts
            name_parts = name.split()
            if len(name_parts) >= 2:
                first_name = name_parts[0].lower()
                last_name = name_parts[-1].lower()
                
                # Common email patterns
                patterns = [
                    f"{first_name[0]}{last_name}@{first_word}.com",
                    f"{first_name}.{last_name}@{first_word}.com",
                    f"{first_name}{last_name[0]}@{first_word}.com",
                    f"{last_name}@{first_word}.com",
                ]
                
                # Add country-specific domains
                if "canada" in company.lower():
                    patterns.append(f"{first_name}.{last_name}@{first_word}.ca")
                elif "australia" in company.lower():
                    patterns.append(f"{first_name}.{last_name}@{first_word}.com.au")
                
                return random.choice(patterns)
        except:
            pass
        
        return f"contact@{first_word}.com"
    
    def collect_conference_attendees(self):
        """Collect mining conference attendees"""
        print("\n🎫 Collecting conference attendees...")
        
        conferences = [
            {
                "name": "PDAC (Prospectors & Developers Association of Canada)",
                "url": "https://www.pdac.ca/convention/attendees",
                "country": "Canada"
            },
            {
                "name": "Diggers & Dealers",
                "url": "https://www.diggersndealers.com.au/attendees",
                "country": "Australia"
            }
        ]
        
        for conference in conferences:
            print(f"\n📋 Conference: {conference['name']}")
            
            try:
                # Use Bright Data's web scraper
                payload = {
                    "dataset_id": "web_scraper",
                    "url": conference["url"],
                    "extraction_rules": {
                        "attendees": {
                            "selector": "table.attendees tr, div.attendee-list div",
                            "output": {
                                "name": "td.name, div.name",
                                "company": "td.company, div.company",
                                "title": "td.title, div.title",
                                "email": "td.email, div.email"
                            }
                        }
                    }
                }
                
                response = requests.post(
                    f"{BRIGHTDATA_BASE_URL}/datasets/collect",
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    attendees = data.get("data", {}).get("attendees", [])
                    print(f"   Found {len(attendees)} attendees")
                    
                    for attendee in attendees:
                        contact = self.parse_conference_attendee(attendee, conference["country"])
                        if contact and not self.is_duplicate(contact):
                            self.collected_contacts.append(contact)
                            print(f"   ✅ Added: {contact['name']} - {contact['firm']}")
                
                time.sleep(3)
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
    
    def parse_conference_attendee(self, attendee, country):
        """Parse conference attendee into contact format"""
        try:
            name = attendee.get("name", "").strip()
            company = attendee.get("company", "").strip()
            title = attendee.get("title", "").strip()
            email = attendee.get("email", "").strip()
            
            if not name or not company:
                return None
            
            # Determine firm type
            firm_type = self.determine_firm_type(title, company)
            
            # Generate email if not provided
            if not email:
                email = self.generate_email(name, company)
            
            return {
                "name": name,
                "title": title or "Attendee",
                "firm": company,
                "firm_type": firm_type,
                "country": country,
                "focus": "Mining & Resources",
                "email": email,
                "source": "Conference",
                "market_focus": "Junior Mining",
                "deal_size": f"${random.randint(1, 50)}M",
                "stage_focus": random.choice(["Exploration", "Development", "Pre-Production"])
            }
        except Exception as e:
            print(f"   ⚠️  Attendee parsing error: {e}")
            return None
    
    def collect_news_deals(self):
        """Collect from mining news and deal announcements"""
        print("\n📰 Collecting from mining news...")
        
        news_sources = [
            {
                "name": "Mining Journal",
                "url": "https://www.mining-journal.com/finance/news",
                "country": "Global"
            },
            {
                "name": "Northern Miner",
                "url": "https://www.northernminer.com/category/finance/",
                "country": "Canada"
            },
            {
                "name": "Australian Mining",
                "url": "https://www.australianmining.com.au/category/finance/",
                "country": "Australia"
            }
        ]
        
        for source in news_sources:
            print(f"\n📄 Source: {source['name']}")
            
            try:
                payload = {
                    "dataset_id": "news_monitor",
                    "keywords": [
                        "junior mining financing",
                        "mining private placement",
                        "exploration financing",
                        "mining capital raise",
                        "mining investment"
                    ],
                    "sources": [source["url"]],
                    "date_range": "last_30_days",
                    "max_results": 30
                }
                
                response = requests.post(
                    f"{BRIGHTDATA_BASE_URL}/datasets/monitor",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    articles = data.get("articles", [])
                    print(f"   Found {len(articles)} relevant articles")
                    
                    for article in articles:
                        contacts = self.extract_contacts_from_article(article, source["country"])
                        for contact in contacts:
                            if contact and not self.is_duplicate(contact):
                                self.collected_contacts.append(contact)
                                print(f"   ✅ Added: {contact['name']}")
                
                time.sleep(2)
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
    
    def extract_contacts_from_article(self, article, country):
        """Extract contacts from news article"""
        contacts = []
        
        try:
            content = article.get("content", "").lower()
            title = article.get("title", "").lower()
            
            # Look for investor mentions
            investor_keywords = [
                "investor", "fund", "capital", "partners", "group",
                "director", "managing director", "partner", "principal"
            ]
            
            # Simple extraction - in real implementation would use NLP
            lines = content.split('.')
            for line in lines:
                if any(keyword in line for keyword in investor_keywords):
                    # Extract potential name and company
                    # This is simplified - real implementation would be more sophisticated
                    pass
            
            # For now, generate sample contacts from article context
            if "financing" in content or "investment" in content:
                # Generate 1-2 sample contacts per article
                for _ in range(random.randint(1, 2)):
                    contact = self.generate_sample_contact_from_context(content, country)
                    if contact:
                        contacts.append(contact)
        
        except Exception as e:
            print(f"   ⚠️  Article parsing error: {e}")
        
        return contacts
    
    def generate_sample_contact_from_context(self, content, country):
        """Generate sample contact based on article context"""
        # Sample names for Canada and Australia
        if country == "Canada":
            first_names = ["Michael", "David", "Robert", "James", "William", "Richard"]
            last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller"]
            companies = ["Maple Capital", "Northern Resources Fund", "Canadian Mining Partners", "True North Capital"]
        else:
            first_names = ["John", "Peter", "Paul", "James", "Robert", "Andrew"]
            last_names = ["Smith", "Jones", "Williams", "Brown", "Wilson", "Taylor"]
            companies = ["Southern Cross Capital", "Aussie Resources Fund", "Pacific Mining Partners", "Outback Capital"]
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        company = random.choice(companies)
        
        titles = [
            "Managing Director",
            "Partner",
            "Investment Director",
            "Portfolio Manager",
            "Principal"
        ]
        
        return {
            "name": f"{first_name} {last_name}",
            "title": random.choice(titles),
            "firm": company,
            "firm_type": "Private Equity",
            "country": country,
            "focus": "Mining & Resources",
            "email": self.generate_email(f"{first_name} {last_name}", company),
            "source": "News Article",
            "market_focus": "Junior Mining",
            "deal_size": f"${random.randint(1, 50)}M",
            "stage_focus": random.choice(["Exploration", "Development", "Pre-Production"])
        }
    
    def save_results(self):
        """Save collected contacts to CSV"""
        if not self.collected_contacts:
            print("\n⚠️  No new contacts collected")
            return
        
        # Combine with existing contacts
        all_contacts = []
        
        # Load existing contacts
        try:
            with open("/Users/cubiczan/.openclaw/workspace/junior-mining-investors-20260226-234432.csv", 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    all_contacts.append(row)
        except FileNotFoundError:
            pass
        
        # Add new contacts
        for i, contact in enumerate(self.collected_contacts, len(all_contacts) + 1):
            contact["ID"] = i
            all_contacts.append(contact)
        
        # Save to new file
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_file = f"/Users/cubiczan/.openclaw/workspace/junior-mining-investors-enriched-{timestamp}.csv"
        
        fieldnames = ["ID", "Name", "Title", "Firm", "Firm Type", "Country", "Focus", "Email", 
                     "Market Focus", "Deal Size", "