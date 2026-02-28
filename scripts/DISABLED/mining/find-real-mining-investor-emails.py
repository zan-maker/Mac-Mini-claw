#!/usr/bin/env python3
"""
Find real mining investor emails through web search
"""

import requests
import json
import csv
from datetime import datetime
import time

# Tavily API for search
TAVILY_API_KEY = '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'
TAVILY_URL = 'https://api.tavily.com/search'

def search_tavily(query, max_results=5):
    """Search using Tavily API"""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TAVILY_API_KEY}'
    }
    
    data = {
        'query': query,
        'search_depth': 'advanced',
        'max_results': max_results
    }
    
    try:
        response = requests.post(TAVILY_URL, headers=headers, json=data, timeout=30)
        return response.json()
    except Exception as e:
        print(f"Error searching Tavily: {e}")
        return {'results': []}

def extract_contact_info_from_url(url):
    """Try to extract contact info from a URL"""
    try:
        response = requests.get(url, timeout=10)
        content = response.text.lower()
        
        # Look for email patterns
        import re
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
        
        # Look for contact info
        contact_info = {}
        if 'contact' in content or 'email' in content or 'info@' in content:
            # Try to find email addresses
            for email in emails:
                if 'contact' in email or 'info' in email or 'enquiries' in email:
                    contact_info['email'] = email
                    break
            
            # Look for phone numbers
            phones = re.findall(r'\+?1?\s*\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', content)
            if phones:
                contact_info['phone'] = phones[0]
        
        return contact_info
    except Exception as e:
        print(f"Error extracting from {url}: {e}")
        return {}

def find_mining_investment_firms():
    """Find mining investment firms with contact info"""
    
    print("🔍 Searching for mining investment firms...")
    
    # List of known mining investment firms
    mining_firms = [
        "Resource Capital Funds",
        "Denham Capital",
        "CAI Capital Partners",
        "Kensington Capital Partners",
        "GenCap Mining Advisory",
        "Sprott Resource Corporation",
        "Waterton Global Resource Management",
        "Appian Capital Advisory",
        "Orion Resource Partners",
        "Triple Flag Precious Metals",
        "EMX Royalty Corporation",
        "Maverix Metals",
        "Osisko Gold Royalties",
        "Franco-Nevada Corporation",
        "Wheaton Precious Metals"
    ]
    
    contacts = []
    
    for firm in mining_firms:
        print(f"\n📋 Searching for: {firm}")
        
        # Search for firm contact info
        results = search_tavily(f"{firm} contact email", max_results=3)
        
        for result in results.get('results', []):
            url = result.get('url', '')
            title = result.get('title', '')
            
            print(f"  • Checking: {title[:50]}...")
            
            # Extract contact info
            contact_info = extract_contact_info_from_url(url)
            
            if contact_info:
                contact = {
                    'firm': firm,
                    'url': url,
                    'title': title,
                    'email': contact_info.get('email', ''),
                    'phone': contact_info.get('phone', ''),
                    'source': 'web_search',
                    'timestamp': datetime.now().isoformat()
                }
                contacts.append(contact)
                print(f"    ✅ Found contact info")
                break
        
        # Small delay to avoid rate limiting
        time.sleep(1)
    
    return contacts

def find_mining_conference_attendees():
    """Find contacts from mining conferences"""
    
    print("\n🎪 Searching mining conference attendees...")
    
    conferences = [
        "PDAC Toronto attendees",
        "Diggers and Dealers Kalgoorlie",
        "Mines and Money London",
        "121 Mining Investment London",
        "Denver Gold Forum",
        "Gold Forum Americas"
    ]
    
    contacts = []
    
    for conference in conferences:
        print(f"\n📋 Searching: {conference}")
        
        results = search_tavily(f"{conference} investor list contact", max_results=2)
        
        for result in results.get('results', []):
            url = result.get('url', '')
            title = result.get('title', '')
            
            print(f"  • Found: {title[:50]}...")
            
            # For conferences, we might find lists of attending companies
            contact = {
                'firm': conference,
                'url': url,
                'title': title,
                'email': '',
                'phone': '',
                'source': 'conference',
                'timestamp': datetime.now().isoformat(),
                'notes': 'Conference attendee list - need to extract specific contacts'
            }
            contacts.append(contact)
        
        time.sleep(1)
    
    return contacts

def find_mining_news_media():
    """Find mining news/media contacts"""
    
    print("\n📰 Searching mining news/media contacts...")
    
    media_outlets = [
        "Mining Journal contact",
        "Northern Miner contact",
        "Mining.com contact",
        "The Assay contact",
        "Kitco Mining contact"
    ]
    
    contacts = []
    
    for outlet in media_outlets:
        print(f"\n📋 Searching: {outlet}")
        
        results = search_tavily(outlet, max_results=2)
        
        for result in results.get('results', []):
            url = result.get('url', '')
            title = result.get('title', '')
            
            print(f"  • Found: {title[:50]}...")
            
            # Extract contact info
            contact_info = extract_contact_info_from_url(url)
            
            contact = {
                'firm': outlet.replace(' contact', ''),
                'url': url,
                'title': title,
                'email': contact_info.get('email', ''),
                'phone': contact_info.get('phone', ''),
                'source': 'media',
                'timestamp': datetime.now().isoformat()
            }
            contacts.append(contact)
        
        time.sleep(1)
    
    return contacts

def save_contacts(contacts, filename):
    """Save contacts to CSV"""
    if not contacts:
        print("❌ No contacts found to save")
        return
    
    with open(filename, 'w', newline='') as f:
        fieldnames = ['firm', 'url', 'title', 'email', 'phone', 'source', 'timestamp', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(contacts)
    
    print(f"✅ Saved {len(contacts)} contacts to {filename}")

def main():
    """Main function"""
    print("="*60)
    print("🔍 REAL MINING INVESTOR EMAIL FINDER")
    print("="*60)
    
    all_contacts = []
    
    # 1. Find mining investment firms
    firm_contacts = find_mining_investment_firms()
    all_contacts.extend(firm_contacts)
    
    # 2. Find conference attendees
    conference_contacts = find_mining_conference_attendees()
    all_contacts.extend(conference_contacts)
    
    # 3. Find mining media
    media_contacts = find_mining_news_media()
    all_contacts.extend(media_contacts)
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = f"/Users/cubiczan/.openclaw/workspace/real-mining-contacts-{timestamp}.csv"
    
    save_contacts(all_contacts, filename)
    
    # Summary
    print("\n" + "="*60)
    print("📊 SEARCH COMPLETE")
    print("="*60)
    print(f"Total contacts found: {len(all_contacts)}")
    
    # Count contacts with emails
    contacts_with_emails = [c for c in all_contacts if c.get('email')]
    print(f"Contacts with emails: {len(contacts_with_emails)}")
    
    # Show sample
    if contacts_with_emails:
        print("\n📧 Sample contacts with emails:")
        for contact in contacts_with_emails[:5]:
            print(f"  • {contact['firm']}: {contact['email']}")
    
    print(f"\n📁 Results saved to: {filename}")
    
    # Next steps
    print("\n🚀 Next steps:")
    print("1. Review the CSV file for quality contacts")
    print("2. Use email verification service (ZeroBounce) to validate emails")
    print("3. Create targeted email campaign")
    print("4. Send emails asking about mining investment criteria")

if __name__ == "__main__":
    main()