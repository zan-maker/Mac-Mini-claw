#!/usr/bin/env python3
"""
Expense Reduction Lead Generator with Craigslist/Reddit Scraping
Targets businesses (20-500 employees) for OPEX reduction services
"""

import os
import json
import requests
from datetime import datetime

# Configuration
OUTPUT_DIR = "/Users/cubiczan/.openclaw/workspace/expense-reduction-leads"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Stevesie/Craigslist API endpoints
CRAIGSLIST_API = "http://craigslist.demoz.co/api"
REDDIT_API = "https://www.reddit.com/r"

# Target cities (focus on business hubs)
CITIES = [
    "newyork", "losangeles", "chicago", "houston", "phoenix",
    "philadelphia", "sanantonio", "sandiego", "dallas", "sanfrancisco",
    "austin", "jacksonville", "fortworth", "columbus", "charlotte",
    "indianapolis", "seattle", "denver", "washington", "boston"
]

# Business categories
CATEGORIES = ["biz", "ofc", "rea"]  # biz=business, ofc=office, rea=real estate

# Reddit subreddits for business/finance discussions
SUBREDDITS = [
    "smallbusiness", "entrepreneur", "startups", "business",
    "finance", "accounting", "operations", "procurement",
    "restaurantowners", "retail", "manufacturing", "construction"
]

def scrape_craigslist_companies():
    """Scrape Craigslist for established businesses"""
    leads = []
    
    for city in CITIES:
        for category in CATEGORIES:
            try:
                url = f"{CRAIGSLIST_API}/{city}/{category}/1"
                response = requests.get(url, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for listing in data.get("listings", []):
                        title = listing.get("title", "").lower()
                        description = listing.get("description", "").lower()
                        
                        # Keywords indicating established businesses with expenses
                        business_keywords = [
                            "established", "profitable", "revenue", "cash flow",
                            "office", "warehouse", "facility", "location",
                            "equipment", "inventory", "supplies", "vendor",
                            "telecom", "utilities", "waste", "shipping",
                            "saas", "software", "subscription", "contract"
                        ]
                        
                        # Size indicators
                        size_keywords = [
                            "employees", "staff", "team", "crew",
                            "20+", "50+", "100+", "500+",
                            "multi-location", "multiple locations", "branches"
                        ]
                        
                        # Expense pain points
                        expense_keywords = [
                            "costs", "expenses", "overhead", "budget",
                            "saving", "cutting", "reducing", "lowering",
                            "negotiate", "vendor", "contract", "lease",
                            "telephone", "internet", "electric", "gas",
                            "waste", "recycling", "shipping", "freight"
                        ]
                        
                        # Check if this is an established business with expense management needs
                        has_business = any(keyword in title + description for keyword in business_keywords)
                        has_size = any(keyword in title + description for keyword in size_keywords)
                        has_expense_mention = any(keyword in title + description for keyword in expense_keywords)
                        
                        if has_business and (has_size or has_expense_mention):
                            lead = {
                                "source": "craigslist",
                                "city": city,
                                "category": category,
                                "title": listing.get("title", ""),
                                "price": listing.get("price", ""),
                                "date": listing.get("date", ""),
                                "url": listing.get("url", ""),
                                "description": listing.get("description", "")[:500],
                                "business_indicators": has_business,
                                "size_indicators": has_size,
                                "expense_mentions": has_expense_mention,
                                "scraped_at": datetime.now().isoformat()
                            }
                            leads.append(lead)
                            
                            print(f"Found: {lead['title']} - {city}")
                
            except Exception as e:
                print(f"Error scraping {city}/{category}: {e}")
    
    return leads

def scrape_reddit_expense_discussions():
    """Scrape Reddit for expense/finance discussions"""
    leads = []
    
    for subreddit in SUBREDDITS:
        try:
            url = f"{REDDIT_API}/{subreddit}/hot.json?limit=100"
            headers = {"User-Agent": "ExpenseReductionLeadBot/1.0"}
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                for post in data.get("data", {}).get("children", []):
                    post_data = post.get("data", {})
                    
                    title = post_data.get("title", "").lower()
                    selftext = post_data.get("selftext", "").lower()
                    
                    # Keywords indicating expense management needs
                    expense_keywords = [
                        "costs too high", "expenses", "overhead", "budget",
                        "saving money", "cutting costs", "reducing expenses",
                        "vendor", "contract", "negotiate", "telecom",
                        "utilities", "electric", "gas", "internet",
                        "phone bill", "waste", "shipping", "freight",
                        "saas", "software costs", "subscription",
                        "opex", "operating expenses", "cash flow",
                        "profit margin", "bottom line", "spend",
                        "procurement", "supplier", "lease", "rent"
                    ]
                    
                    # Business context keywords
                    business_keywords = [
                        "my business", "our company", "we have",
                        "employees", "staff", "team", "office",
                        "warehouse", "facility", "location",
                        "manufacturing", "production", "retail",
                        "restaurant", "construction", "service"
                    ]
                    
                    has_expense = any(keyword in title + selftext for keyword in expense_keywords)
                    has_business = any(keyword in title + selftext for keyword in business_keywords)
                    
                    if has_expense and has_business:
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
                            "expense_topics": [k for k in expense_keywords if k in title + selftext][:5],
                            "scraped_at": datetime.now().isoformat()
                        }
                        leads.append(lead)
                        
                        print(f"Found expense discussion: {lead['title'][:80]}... - r/{subreddit}")
        
        except Exception as e:
            print(f"Error scraping r/{subreddit}: {e}")
    
    return leads

def enrich_expense_leads(leads):
    """Enrich expense reduction leads"""
    enriched_leads = []
    
    for lead in leads:
        enriched_lead = lead.copy()
        
        # Estimate savings potential
        if lead["source"] == "craigslist":
            text = (lead.get("title", "") + " " + lead.get("description", "")).lower()
            
            # Estimate employee count
            if "500+" in text or "500 employees" in text:
                emp_range = "500+"
                est_savings = "$250,000-$500,000+"
                priority = "high"
            elif "100+" in text or "100 employees" in text:
                emp_range = "100-500"
                est_savings = "$100,000-$250,000"
                priority = "high"
            elif "50+" in text or "50 employees" in text:
                emp_range = "50-100"
                est_savings = "$50,000-$100,000"
                priority = "medium"
            elif "20+" in text or "20 employees" in text:
                emp_range = "20-50"
                est_savings = "$25,000-$50,000"
                priority = "medium"
            else:
                emp_range = "unknown"
                est_savings = "$15,000-$50,000"
                priority = "low"
            
            enriched_lead["employee_range"] = emp_range
            enriched_lead["estimated_savings"] = est_savings
            enriched_lead["priority"] = priority
            
            # Identify expense categories mentioned
            expense_categories = []
            categories_map = {
                "telecom": ["phone", "internet", "telecom", "communication"],
                "utilities": ["electric", "gas", "water", "utility"],
                "waste": ["waste", "recycling", "trash", "disposal"],
                "shipping": ["shipping", "freight", "logistics", "delivery"],
                "saas": ["software", "saas", "subscription", "app"],
                "vendor": ["vendor", "supplier", "contract", "lease"]
            }
            
            for category, keywords in categories_map.items():
                if any(keyword in text for keyword in keywords):
                    expense_categories.append(category)
            
            enriched_lead["expense_categories"] = expense_categories
        
        elif lead["source"] == "reddit":
            # Reddit leads - focus on discussion topics
            enriched_lead["employee_range"] = "unknown"
            enriched_lead["estimated_savings"] = "$25,000-$100,000"
            enriched_lead["priority"] = "medium"  # Actively discussing expenses
            enriched_lead["expense_categories"] = lead.get("expense_topics", [])
        
        enriched_lead["service_type"] = "expense_reduction"
        enriched_lead["value_prop"] = "15-30% OPEX reduction with contingency-based pricing"
        
        enriched_leads.append(enriched_lead)
    
    return enriched_leads

def save_expense_leads(leads):
    """Save expense reduction leads"""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    # JSON file
    json_file = f"{OUTPUT_DIR}/expense-reduction-leads-{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump(leads, f, indent=2)
    
    # Markdown report
    md_file = f"{OUTPUT_DIR}/expense-reduction-leads-{timestamp}.md"
    with open(md_file, 'w') as f:
        f.write(f"# Expense Reduction Leads - {timestamp}\n\n")
        f.write(f"**Total Leads:** {len(leads)}\n")
        f.write(f"**Sources:** Craigslist ({sum(1 for l in leads if l['source']=='craigslist')}), ")
        f.write(f"Reddit ({sum(1 for l in leads if l['source']=='reddit')})\n\n")
        
        f.write("## Priority Breakdown\n\n")
        f.write(f"- **High Priority:** {sum(1 for l in leads if l.get('priority')=='high')}\n")
        f.write(f"- **Medium Priority:** {sum(1 for l in leads if l.get('priority')=='medium')}\n")
        f.write(f"- **Low Priority:** {sum(1 for l in leads if l.get('priority')=='low')}\n\n")
        
        f.write("## Estimated Savings Potential\n\n")
        total_savings_low = 0
        total_savings_high = 0
        
        for lead in leads:
            savings = lead.get('estimated_savings', '$0')
            if '-' in savings:
                low, high = savings.replace('$', '').replace(',', '').split('-')
                total_savings_low += float(low.strip().split('+')[0])
                total_savings_high += float(high.strip().split('+')[0])
        
        f.write(f"- **Total Addressable Savings:** ${total_savings_low:,.0f} - ${total_savings_high:,.0f}\n")
        f.write(f"- **Average per Lead:** ${(total_savings_low + total_savings_high)/2/len(leads):,.0f}\n\n")
        
        f.write("## Lead Details\n\n")
        
        for i, lead in enumerate(leads, 1):
            f.write(f"### {i}. {lead.get('title', 'No title')[:100]}\n\n")
            f.write(f"- **Priority:** {lead.get('priority', 'unknown')}\n")
            f.write(f"- **Source:** {lead['source']}\n")
            f.write(f"- **Employee Range:** {lead.get('employee_range', 'unknown')}\n")
            f.write(f"- **Est. Savings:** {lead.get('estimated_savings', 'unknown')}\n")
            
            if lead['source'] == 'craigslist':
                f.write(f"- **Location:** {lead.get('city', 'unknown')}\n")
                f.write(f"- **Expense Categories:** {', '.join(lead.get('expense_categories', []))}\n")
                f.write(f"- **URL:** {lead.get('url', '')}\n")
            elif lead['source'] == 'reddit':
                f.write(f"- **Subreddit:** r/{lead.get('subreddit', '')}\n")
                f.write(f"- **Expense Topics:** {', '.join(lead.get('expense_topics', []))}\n")
                f.write(f"- **URL:** {lead.get('url', '')}\n")
            
            f.write(f"- **Description:** {lead.get('description', lead.get('text', ''))[:300]}...\n\n")
        
        f.write("## Outreach Strategy\n\n")
        f.write("1. **High Priority:** Immediate personalized outreach\n")
        f.write("2. **Medium Priority:** Add to weekly outreach sequence\n")
        f.write("3. **Low Priority:** Monthly newsletter/nurturing\n")
        f.write("4. **Reddit Discussions:** Engage with value-first advice\n")
    
    print(f"\n✅ Saved {len(leads)} leads to:")
    print(f"   - {json_file}")
    print(f"   - {md_file}")
    
    return json_file, md_file

def main():
    """Main execution"""
    print("=" * 60)
    print("EXPENSE REDUCTION LEAD GENERATOR")
    print("Scraping Craigslist & Reddit for OPEX reduction leads")
    print("=" * 60)
    print()
    
    # Step 1: Scrape Craigslist
    print("🔍 Scraping Craigslist for established businesses...")
    craigslist_leads = scrape_craigslist_companies()
    print(f"   Found {len(craigslist_leads)} Craigslist leads")
    
    # Step 2: Scrape Reddit
    print("\n🔍 Scraping Reddit expense discussions...")
    reddit_leads = scrape_reddit_expense_discussions()
    print(f"   Found {len(reddit_leads)} Reddit leads")
    
    # Combine leads
    all_leads = craigslist_leads + reddit_leads
    print(f"\n📊 Total raw leads: {len(all_leads)}")
    
    if not all_leads:
        print("❌ No leads found. Exiting.")
        return
    
    # Step 3: Enrich leads
    print("\n🎯 Enriching leads with savings estimates...")
    enriched_leads = enrich_expense_leads(all_leads)
    
    # Step 4: Save leads
    print("\n💾 Saving leads to files...")
    json_file, md_file = save_expense_leads(enriched_leads)
    
    # Step 5: Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    high_priority = sum(1 for l in enriched_leads if l.get('priority') == 'high')
    medium_priority = sum(1 for l in enriched_leads if l.get('priority') == 'medium')
    
    print(f"Total Leads: {len(enriched_leads)}")
    print(f"High Priority: {high_priority}")
    print(f"Medium Priority: {medium_priority}")
    print(f"Sources: Craigslist ({len(craigslist_leads)}), Reddit ({len(reddit_leads)})")
    print()
    print(f"📁 Report: {md_file}")
    print(f"📊 Data: {json_file}")
    print()
    print("Next: Run expense reduction outreach for high-priority leads")
    print("=" * 60)

if __name__ == "__main__":
    main()
