#!/usr/bin/env python3
"""
Wellness 125 Lead Generator with Craigslist/Reddit Scraping
Targets small businesses (20+ employees) for cafeteria plan services
"""

import os
import json
import requests
from datetime import datetime

# Configuration
OUTPUT_DIR = "/Users/cubiczan/.openclaw/workspace/wellness-125-leads"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Stevesie/Craigslist API endpoints
CRAIGSLIST_API = "http://craigslist.demoz.co/api"
REDDIT_API = "https://www.reddit.com/r"

# Target cities for business listings
CITIES = [
    "phoenix", "losangeles", "sandiego", "sanfrancisco",
    "seattle", "denver", "dallas", "houston", "atlanta",
    "miami", "chicago", "boston", "newyork"
]

# Business categories to target
CATEGORIES = ["biz", "car", "lab"]  # biz=business for sale, car=auto businesses, lab=service businesses

# Reddit subreddits for business discussions
SUBREDDITS = [
    "smallbusiness", "entrepreneur", "business", "startups",
    "restaurateur", "retail", "fitnessbusiness", "consulting"
]

def scrape_craigslist_businesses():
    """Scrape Craigslist for business-for-sale listings"""
    leads = []
    
    for city in CITIES:
        for category in CATEGORIES:
            try:
                url = f"{CRAIGSLIST_API}/{city}/{category}/1"
                response = requests.get(url, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for listing in data.get("listings", []):
                        # Filter for relevant business types
                        title = listing.get("title", "").lower()
                        description = listing.get("description", "").lower()
                        
                        # Keywords indicating established businesses
                        business_keywords = [
                            "established", "franchise", "owner retiring", 
                            "turnkey", "profitable", "cash flow", "revenue",
                            "employees", "staff", "team", "location", "lease",
                            "equipment", "inventory", "customer base"
                        ]
                        
                        # Check if this is an established business (not just equipment)
                        if any(keyword in title + description for keyword in business_keywords):
                            lead = {
                                "source": "craigslist",
                                "city": city,
                                "category": category,
                                "title": listing.get("title", ""),
                                "price": listing.get("price", ""),
                                "date": listing.get("date", ""),
                                "url": listing.get("url", ""),
                                "description": listing.get("description", "")[:500],
                                "scraped_at": datetime.now().isoformat()
                            }
                            leads.append(lead)
                            
                            print(f"Found: {lead['title']} - {city} - ${lead['price']}")
                
            except Exception as e:
                print(f"Error scraping {city}/{category}: {e}")
    
    return leads

def scrape_reddit_business_discussions():
    """Scrape Reddit for business owner discussions"""
    leads = []
    
    for subreddit in SUBREDDITS:
        try:
            url = f"{REDDIT_API}/{subreddit}/hot.json?limit=50"
            headers = {"User-Agent": "Wellness125LeadBot/1.0"}
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                for post in data.get("data", {}).get("children", []):
                    post_data = post.get("data", {})
                    
                    title = post_data.get("title", "").lower()
                    selftext = post_data.get("selftext", "").lower()
                    
                    # Keywords indicating business owners with employees
                    owner_keywords = [
                        "my business", "our company", "employees", "staff",
                        "team of", "hiring", "payroll", "benefits", "insurance",
                        "healthcare", "taxes", "compliance", "hr", "human resources",
                        "small business owner", "entrepreneur", "founder"
                    ]
                    
                    # Keywords indicating business challenges
                    challenge_keywords = [
                        "costs", "expenses", "overhead", "budget",
                        "saving money", "cutting costs", "reducing expenses",
                        "employee benefits", "health insurance", "tax savings",
                        "compliance", "paperwork", "administration"
                    ]
                    
                    if (any(keyword in title + selftext for keyword in owner_keywords) and
                        any(keyword in title + selftext for keyword in challenge_keywords)):
                        
                        lead = {
                            "source": "reddit",
                            "subreddit": subreddit,
                            "title": post_data.get("title", ""),
                            "author": post_data.get("author", ""),
                            "url": f"https://reddit.com{post_data.get('permalink', '')}",
                            "score": post_data.get("score", 0),
                            "comments": post_data.get("num_comments", 0),
                            "created_utc": post_data.get("created_utc", 0),
                            "text": post_data.get("selftext", "")[:1000],
                            "scraped_at": datetime.now().isoformat()
                        }
                        leads.append(lead)
                        
                        print(f"Found Reddit post: {lead['title'][:80]}... - r/{subreddit}")
        
        except Exception as e:
            print(f"Error scraping r/{subreddit}: {e}")
    
    return leads

def enrich_with_company_info(leads):
    """Enrich leads with company information (placeholder for actual enrichment)"""
    enriched_leads = []
    
    for lead in leads:
        # Placeholder for actual company enrichment
        # In production, this would use Clearbit, Hunter.io, etc.
        
        enriched_lead = lead.copy()
        
        # Estimate employee count based on listing type
        if lead["source"] == "craigslist":
            # Business-for-sale listings often mention employee count
            text = (lead.get("title", "") + " " + lead.get("description", "")).lower()
            
            if "20+" in text or "20 employees" in text or "20 staff" in text:
                enriched_lead["estimated_employees"] = "20-50"
                enriched_lead["wellness125_fit"] = "high"
            elif "10+" in text or "10 employees" in text:
                enriched_lead["estimated_employees"] = "10-20"
                enriched_lead["wellness125_fit"] = "medium"
            else:
                enriched_lead["estimated_employees"] = "unknown"
                enriched_lead["wellness125_fit"] = "low"
        
        elif lead["source"] == "reddit":
            # Reddit posts - harder to estimate
            enriched_lead["estimated_employees"] = "unknown"
            enriched_lead["wellness125_fit"] = "medium"  # Business owners discussing challenges
        
        enriched_lead["service_type"] = "wellness125"
        enriched_lead["value_prop"] = "Cafeteria Plan (Section 125) for tax savings & employee benefits"
        enriched_lead["estimated_savings"] = "$15,000-$50,000 annually"
        
        enriched_leads.append(enriched_lead)
    
    return enriched_leads

def save_leads(leads):
    """Save leads to JSON and Markdown files"""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    # JSON file
    json_file = f"{OUTPUT_DIR}/wellness125-leads-{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump(leads, f, indent=2)
    
    # Markdown report
    md_file = f"{OUTPUT_DIR}/wellness125-leads-{timestamp}.md"
    with open(md_file, 'w') as f:
        f.write(f"# Wellness 125 Leads - {timestamp}\n\n")
        f.write(f"**Total Leads:** {len(leads)}\n")
        f.write(f"**Sources:** Craigslist ({sum(1 for l in leads if l['source']=='craigslist')}), ")
        f.write(f"Reddit ({sum(1 for l in leads if l['source']=='reddit')})\n\n")
        
        f.write("## Summary\n\n")
        f.write(f"- **High Fit:** {sum(1 for l in leads if l.get('wellness125_fit')=='high')}\n")
        f.write(f"- **Medium Fit:** {sum(1 for l in leads if l.get('wellness125_fit')=='medium')}\n")
        f.write(f"- **Low Fit:** {sum(1 for l in leads if l.get('wellness125_fit')=='low')}\n\n")
        
        f.write("## Lead Details\n\n")
        
        for i, lead in enumerate(leads, 1):
            f.write(f"### {i}. {lead.get('title', 'No title')[:100]}\n\n")
            f.write(f"- **Source:** {lead['source']}\n")
            f.write(f"- **Fit:** {lead.get('wellness125_fit', 'unknown')}\n")
            f.write(f"- **Employees:** {lead.get('estimated_employees', 'unknown')}\n")
            
            if lead['source'] == 'craigslist':
                f.write(f"- **Location:** {lead.get('city', 'unknown')}\n")
                f.write(f"- **Price:** {lead.get('price', 'N/A')}\n")
                f.write(f"- **URL:** {lead.get('url', '')}\n")
            elif lead['source'] == 'reddit':
                f.write(f"- **Subreddit:** r/{lead.get('subreddit', '')}\n")
                f.write(f"- **Author:** u/{lead.get('author', '')}\n")
                f.write(f"- **URL:** {lead.get('url', '')}\n")
            
            f.write(f"- **Description:** {lead.get('description', lead.get('text', ''))[:300]}...\n\n")
        
        f.write("## Next Steps\n\n")
        f.write("1. **High Fit Leads:** Immediate outreach via email/phone\n")
        f.write("2. **Medium Fit Leads:** Add to nurturing sequence\n")
        f.write("3. **Low Fit Leads:** Monitor for changes\n")
        f.write("4. **Reddit Discussions:** Engage with helpful advice, then mention Wellness 125\n")
    
    print(f"\n✅ Saved {len(leads)} leads to:")
    print(f"   - {json_file}")
    print(f"   - {md_file}")
    
    return json_file, md_file

def main():
    """Main execution"""
    print("=" * 60)
    print("WELLNESS 125 LEAD GENERATOR")
    print("Scraping Craigslist & Reddit for small business leads")
    print("=" * 60)
    print()
    
    # Step 1: Scrape Craigslist
    print("🔍 Scraping Craigslist business-for-sale listings...")
    craigslist_leads = scrape_craigslist_businesses()
    print(f"   Found {len(craigslist_leads)} Craigslist leads")
    
    # Step 2: Scrape Reddit
    print("\n🔍 Scraping Reddit business discussions...")
    reddit_leads = scrape_reddit_business_discussions()
    print(f"   Found {len(reddit_leads)} Reddit leads")
    
    # Combine leads
    all_leads = craigslist_leads + reddit_leads
    print(f"\n📊 Total raw leads: {len(all_leads)}")
    
    if not all_leads:
        print("❌ No leads found. Exiting.")
        return
    
    # Step 3: Enrich leads
    print("\n🎯 Enriching leads with company info...")
    enriched_leads = enrich_with_company_info(all_leads)
    
    # Step 4: Save leads
    print("\n💾 Saving leads to files...")
    json_file, md_file = save_leads(enriched_leads)
    
    # Step 5: Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    high_fit = sum(1 for l in enriched_leads if l.get('wellness125_fit') == 'high')
    medium_fit = sum(1 for l in enriched_leads if l.get('wellness125_fit') == 'medium')
    
    print(f"Total Leads: {len(enriched_leads)}")
    print(f"High Fit (Immediate Outreach): {high_fit}")
    print(f"Medium Fit (Nurturing): {medium_fit}")
    print(f"Sources: Craigslist ({len(craigslist_leads)}), Reddit ({len(reddit_leads)})")
    print()
    print(f"📁 Report: {md_file}")
    print(f"📊 Data: {json_file}")
    print()
    print("Next: Run outreach script for high-fit leads")
    print("=" * 60)

if __name__ == "__main__":
    main()
