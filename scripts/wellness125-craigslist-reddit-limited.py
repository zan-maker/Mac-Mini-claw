#!/usr/bin/env python3
"""
Wellness 125 Lead Generator with Craigslist/Reddit Scraping
Targets small businesses (20-199 employees) for cafeteria plan services
LIMITED TO COMPANIES WITH LESS THAN 200 EMPLOYEES
"""

import os
import json
import requests
import re
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

# MAXIMUM EMPLOYEE COUNT (NEW LIMIT)
MAX_EMPLOYEES = 200

def estimate_employee_count(text):
    """
    Estimate employee count from text.
    Returns: (estimated_count, confidence)
    """
    text_lower = text.lower()
    
    # Patterns to match employee counts
    patterns = [
        (r'(\d+)\+?\s*(?:employees|staff|team members|workers|people)', 0.9),  # "20 employees"
        (r'(\d+)\s*to\s*(\d+)\s*(?:employees|staff)', 0.8),  # "20 to 50 employees"
        (r'(\d+)\s*-\s*(\d+)\s*(?:employees|staff)', 0.8),   # "20-50 employees"
        (r'about\s*(\d+)\s*(?:employees|staff)', 0.7),       # "about 20 employees"
        (r'approximately\s*(\d+)\s*(?:employees|staff)', 0.7), # "approximately 20 employees"
        (r'over\s*(\d+)\s*(?:employees|staff)', 0.6),        # "over 20 employees"
        (r'under\s*(\d+)\s*(?:employees|staff)', 0.6),       # "under 20 employees"
        (r'less than\s*(\d+)\s*(?:employees|staff)', 0.6),   # "less than 20 employees"
        (r'(\d+)\s*(?:employee|staff)\s*business', 0.5),     # "20 employee business"
    ]
    
    for pattern, confidence in patterns:
        matches = re.findall(pattern, text_lower)
        if matches:
            if len(matches[0]) == 2:  # Range like "20-50"
                try:
                    min_emp = int(matches[0][0])
                    max_emp = int(matches[0][1])
                    avg_emp = (min_emp + max_emp) // 2
                    return avg_emp, confidence
                except:
                    continue
            else:  # Single number
                try:
                    emp_count = int(matches[0])
                    return emp_count, confidence
                except:
                    continue
    
    # Fallback: Look for business size indicators
    size_indicators = {
        "small business": (10, 0.4),
        "medium business": (50, 0.4),
        "large business": (150, 0.3),
        "family business": (5, 0.5),
        "startup": (5, 0.4),
        "established business": (25, 0.5),
        "franchise": (15, 0.6),
        "chain": (30, 0.5),
        "corporation": (100, 0.3),
        "enterprise": (200, 0.2),
    }
    
    for indicator, (count, conf) in size_indicators.items():
        if indicator in text_lower:
            return count, conf
    
    return None, 0.0

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
                    text = title + " " + selftext
                    
                    # Keywords indicating business owners with employees
                    owner_keywords = [
                        "my business", "our company", "employees", "staff",
                        "team", "hiring", "payroll", "benefits", "insurance",
                        "tax", "compliance", "hr", "human resources",
                        "small business owner", "entrepreneur", "startup founder"
                    ]
                    
                    # Keywords indicating Wellness 125 needs
                    wellness_keywords = [
                        "health insurance", "employee benefits", "tax savings",
                        "section 125", "cafeteria plan", "pre-tax benefits",
                        "healthcare costs", "benefits package", "hr compliance"
                    ]
                    
                    if any(keyword in text for keyword in owner_keywords):
                        lead = {
                            "source": "reddit",
                            "subreddit": subreddit,
                            "title": post_data.get("title", ""),
                            "author": post_data.get("author", ""),
                            "url": f"https://reddit.com{post_data.get('permalink', '')}",
                            "text": post_data.get("selftext", "")[:1000],
                            "score": post_data.get("score", 0),
                            "comments": post_data.get("num_comments", 0),
                            "created_utc": post_data.get("created_utc", 0),
                            "scraped_at": datetime.now().isoformat()
                        }
                        leads.append(lead)
                        
                        print(f"Found: {lead['title'][:50]}... - r/{subreddit}")
        
        except Exception as e:
            print(f"Error scraping r/{subreddit}: {e}")
    
    return leads

def enrich_with_company_info(leads):
    """Enrich leads with estimated employee counts and Wellness 125 fit"""
    enriched_leads = []
    
    for lead in leads:
        enriched_lead = lead.copy()
        
        # Combine text for employee estimation
        text = ""
        if lead["source"] == "craigslist":
            text = (lead.get("title", "") + " " + lead.get("description", "")).lower()
        elif lead["source"] == "reddit":
            text = (lead.get("title", "") + " " + lead.get("text", "")).lower()
        
        # Estimate employee count
        emp_count, confidence = estimate_employee_count(text)
        
        if emp_count is not None:
            enriched_lead["estimated_employees"] = emp_count
            enriched_lead["employee_confidence"] = confidence
            
            # CHECK EMPLOYEE LIMIT: REJECT IF 200+ EMPLOYEES
            if emp_count >= MAX_EMPLOYEES:
                enriched_lead["wellness125_fit"] = "rejected"
                enriched_lead["rejection_reason"] = f"Too large ({emp_count} employees, limit is {MAX_EMPLOYEES})"
                print(f"  ⚠️ Rejected: {emp_count} employees (over {MAX_EMPLOYEES} limit)")
            elif emp_count >= 50:
                enriched_lead["wellness125_fit"] = "high"
                enriched_lead["fit_reason"] = f"Good size ({emp_count} employees)"
            elif emp_count >= 20:
                enriched_lead["wellness125_fit"] = "medium"
                enriched_lead["fit_reason"] = f"Minimum size ({emp_count} employees)"
            else:
                enriched_lead["wellness125_fit"] = "low"
                enriched_lead["fit_reason"] = f"Too small ({emp_count} employees)"
        else:
            enriched_lead["estimated_employees"] = "unknown"
            enriched_lead["employee_confidence"] = 0.0
            enriched_lead["wellness125_fit"] = "unknown"
            enriched_lead["fit_reason"] = "Could not estimate employee count"
        
        enriched_lead["service_type"] = "wellness125"
        enriched_lead["value_prop"] = "Cafeteria Plan (Section 125) for tax savings & employee benefits"
        enriched_lead["estimated_savings"] = "$15,000-$50,000 annually"
        enriched_lead["max_employee_limit"] = MAX_EMPLOYEES  # Add the limit to output
        
        enriched_leads.append(enriched_lead)
    
    return enriched_leads

def filter_by_employee_limit(leads):
    """Filter leads to only include companies under 200 employees"""
    filtered = []
    
    for lead in leads:
        emp_data = lead.get("estimated_employees")
        
        if emp_data == "unknown":
            # Keep unknown for manual review
            filtered.append(lead)
        elif isinstance(emp_data, int):
            if emp_data < MAX_EMPLOYEES:
                filtered.append(lead)
            else:
                print(f"  🚫 Filtered out: {lead.get('title', 'Unknown')[:50]}... - {emp_data} employees")
        else:
            # Keep for manual review
            filtered.append(lead)
    
    return filtered

def save_leads(leads):
    """Save leads to JSON and Markdown files"""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    # Filter leads by employee limit
    filtered_leads = filter_by_employee_limit(leads)
    
    # JSON file
    json_file = f"{OUTPUT_DIR}/wellness125-leads-limited-{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump(filtered_leads, f, indent=2)
    
    # Markdown report
    md_file = f"{OUTPUT_DIR}/wellness125-leads-limited-{timestamp}.md"
    with open(md_file, 'w') as f:
        f.write(f"# Wellness 125 Leads - {timestamp}\n")
        f.write(f"**EMPLOYEE LIMIT: < {MAX_EMPLOYEES} employees**\n\n")
        f.write(f"**Total Raw Leads:** {len(leads)}\n")
        f.write(f"**After Employee Filter:** {len(filtered_leads)}\n")
        f.write(f"**Sources:** Craigslist ({sum(1 for l in leads if l['source']=='craigslist')}), ")
        f.write(f"Reddit ({sum(1 for l in leads if l['source']=='reddit')})\n\n")
        
        f.write("## Summary\n\n")
        
        # Count by fit category
        fit_categories = {}
        for lead in filtered_leads:
            fit = lead.get('wellness125_fit', 'unknown')
            fit_categories[fit] = fit_categories.get(fit, 0) + 1
        
        for fit, count in sorted(fit_categories.items()):
            f.write(f"- **{fit.upper()} Fit:** {count} leads\n")
        
        f.write("\n## Employee Size Distribution\n\n")
        
        # Count by employee range
        emp_ranges = {
            "1-19": 0,
            "20-49": 0,
            "50-99": 0,
            "100-199": 0,
            "200+ (filtered out)": len(leads) - len(filtered_leads),
            "Unknown": 0
        }
        
        for lead in leads:
            emp_data = lead.get("estimated_employees")
            if emp_data == "unknown":
                emp_ranges["Unknown"] += 1
            elif isinstance(emp_data, int):
                if emp_data < 20:
                    emp_ranges["1-19"] += 1
                elif emp_data < 50:
                    emp_ranges["20-49"] += 1
                elif emp_data < 100:
                    emp_ranges["50-99"] += 1
                elif emp_data < 200:
                    emp_ranges["100-199"] += 1
                else:
                    emp_ranges["200+ (filtered out)"] += 1
        
        for range_name, count in emp_ranges.items():
            if count > 0:
                f.write(f"- **{range_name}:** {count} leads\n")
        
        f.write("\n## Top Leads for Outreach\n\n")
        
        # Show top 10 leads (sorted by fit)
        sorted_leads = sorted(
            filtered_leads,
            key=lambda x: (
                0 if x.get('wellness125_fit') == 'high' else
                1 if x.get('wellness125_fit') == 'medium' else
                2 if x.get('wellness125_fit') == 'low' else
                3
            )
        )
        
        for i, lead in enumerate(sorted_leads[:10], 1):
            f.write(f"### {i}. {lead.get('title', 'Unknown')[:80]}...\n")
            f.write(f"- **Source:** {lead['source']}\n")
            f.write(f"- **Employees:** {lead.get('estimated_employees', 'unknown')}\n")
            f.write(f"- **Fit:** {lead.get('wellness125_fit', 'unknown')}\n")
            if 'fit_reason' in lead:
                f.write(f"- **Reason:** {lead['fit_reason']}\n")
            if lead['source'] == 'craigslist':
                f.write(f"- **Location:** {lead.get('city', 'unknown')}\n")
                f.write(f"- **Price:** {lead.get('price', 'unknown')}\n")
            elif lead['source'] == 'reddit':
                f.write(f"- **Subreddit:** r/{lead.get('subreddit', 'unknown')}\n")
                f.write(f"- **Score:** {lead.get('score', 0)} votes\n")
            f.write(f"- **URL:** {lead.get('url', 'N/A')}\n\n")
        
        f.write("\n## Notes\n\n")
        f.write(f"1. **Employee Limit:** Strictly limited to companies with < {MAX_EMPLOYEES} employees\n")
        f.write("2. **Unknown employee counts:** Kept for manual review\n")
        f.write("3. **High Fit:** 50-199 employees (ideal for Wellness 125)\n")
        f.write("4. **Medium Fit:** 20-49 employees (minimum viable size)\n")
        f.write("5. **Low Fit:** <20 employees (too small, consider other services)\n")
        f.write("6. **Rejected:** ≥200 employees (over limit, refer to enterprise solutions)\n")
    
    return json_file, md_file

def main():
    """Main function"""
    print("=" * 60)
    print(f"WELLNESS 125 LEAD GENERATOR")
    print(f"EMPLOYEE LIMIT: < {MAX_EMPLOYEES} employees")
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
    print("\n🎯 Enriching leads with employee estimates...")
    enriched_leads = enrich_with_company_info(all_leads)
    
    # Step 4: Save leads (with filtering)
    print("\n💾 Saving leads to files (with employee filter)...")
    json_file, md_file = save_leads(enriched_leads)
    
    # Step 5: Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    # Count statistics
    total_leads = len(enriched_leads)
    filtered_leads = len(filter_by_employee_limit(enriched_leads))
    
    fit_counts = {}
    for lead in enriched_leads:
        fit = lead.get('wellness125_fit', 'unknown')
        fit_counts[fit] = fit_counts.get(fit, 0) + 1
    
    print(f"Total Raw Leads: {total_leads}")
    print(f"After Employee Filter (<{MAX_EMPLOYEES}): {filtered_leads}")
    print(f"Leads Filtered Out (≥{MAX_EMPLOYEES}): {total_leads - filtered_leads}")
    print()
    
    for fit, count in sorted(fit_counts.items()):
        print(f"{fit.upper()} Fit: {count} leads")
    
    print()
    print(f"📁 Report: {md_file}")
    print(f"📊 Data: {json_file}")
    print()
    print("Next: Run outreach only for companies with <200 employees")
    print("=" * 60)

if __name__ == "__main__":
    main()