#!/usr/bin/env python3
"""
Craigslist Business & Service Lead Generator
Focus: Referral Fee/Commission Opportunities

Targets:
1. Business-for-Sale (biz category) - M&A referral fees
2. Service Businesses (sks, cps, lbs) - Expense reduction referral fees
"""

import craigslistscraper as cs
import json
import pandas as pd
from datetime import datetime
import os
import time
from typing import Dict, List, Optional

# Configuration
CONFIG = {
    "cities": ["newyork", "losangeles", "chicago", "miami", "houston", "phoenix"],
    "categories": {
        "business_for_sale": "biz",  # Idea 1
        "skilled_trade": "sks",      # Idea 3
        "computer_services": "cps",  # Idea 3
        "labor_services": "lbs"      # Idea 3
    },
    "min_price": 25000,  # Minimum deal size for referral fees
    "max_price": 5000000,  # Maximum deal size we can handle
    "output_dir": "/Users/cubiczan/.openclaw/workspace/craigslist-leads"
}

# Referral Fee Structures
REFERRAL_FEES = {
    "business_for_sale": {
        "fee_type": "percentage",
        "rate": 0.01,  # 1% of deal value
        "min_fee": 5000,
        "max_fee": 50000
    },
    "service_business": {
        "fee_type": "savings_percentage",
        "rate": 0.15,  # 15% of first-year savings
        "min_fee": 1000,
        "max_fee": 10000
    }
}

def ensure_directory(path: str):
    """Ensure output directory exists"""
    os.makedirs(path, exist_ok=True)

def scrape_category(city: str, category: str, category_name: str) -> List[Dict]:
    """Scrape a specific category from a city"""
    leads = []
    
    try:
        print(f"  Scraping {category_name} in {city}...")
        
        # Create search
        search = cs.Search(
            city=city,
            category=category,
            query=""  # Empty query gets all listings
        )
        
        # Fetch results
        status = search.fetch()
        if status != 200:
            print(f"    Failed to fetch: HTTP {status}")
            return leads
        
        print(f"    Found {len(search.ads)} listings")
        
        # Process each ad
        for ad in search.ads[:50]:  # Limit to 50 per category to avoid rate limiting
            try:
                # Fetch ad details
                ad_status = ad.fetch()
                if ad_status != 200:
                    continue
                
                # Convert to dict
                data = ad.to_dict()
                
                # Add metadata
                data["scraped_at"] = datetime.now().isoformat()
                data["city"] = city
                data["category"] = category_name
                data["craigslist_url"] = ad.url
                
                # Calculate potential referral fee
                data["referral_fee"] = calculate_referral_fee(data, category_name)
                
                # Only include if referral fee meets minimum
                if data["referral_fee"] and data["referral_fee"]["estimated_fee"] >= 1000:
                    leads.append(data)
                    print(f"    ✓ Qualified: {data.get('title', 'Unknown')} - ${data['referral_fee']['estimated_fee']:,}")
                
                # Be respectful to Craigslist
                time.sleep(0.5)
                
            except Exception as e:
                print(f"    Error processing ad: {e}")
                continue
                
    except Exception as e:
        print(f"  Error scraping {category_name} in {city}: {e}")
    
    return leads

def calculate_referral_fee(listing: Dict, category_name: str) -> Optional[Dict]:
    """Calculate potential referral fee for a listing"""
    
    # Extract price from listing
    price = extract_price(listing)
    if not price:
        return None
    
    # Determine fee structure based on category
    if category_name == "business_for_sale":
        fee_config = REFERRAL_FEES["business_for_sale"]
        
        # 1% of business sale price
        estimated_fee = price * fee_config["rate"]
        estimated_fee = max(fee_config["min_fee"], min(fee_config["max_fee"], estimated_fee))
        
        return {
            "type": "business_sale_referral",
            "rate": fee_config["rate"],
            "estimated_fee": estimated_fee,
            "business_value": price,
            "description": f"1% referral fee on business sale (${price:,})"
        }
    
    else:  # Service business
        fee_config = REFERRAL_FEES["service_business"]
        
        # Estimate annual revenue for service business
        # Rule of thumb: 3x monthly price or 20x weekly price
        annual_revenue = estimate_service_revenue(listing, price)
        
        # Estimate savings potential (15-25% of expenses)
        # Assume 60% expense ratio for service businesses
        annual_expenses = annual_revenue * 0.6
        potential_savings = annual_expenses * 0.2  # 20% savings
        
        # 15% of first-year savings
        estimated_fee = potential_savings * fee_config["rate"]
        estimated_fee = max(fee_config["min_fee"], min(fee_config["max_fee"], estimated_fee))
        
        return {
            "type": "expense_reduction_referral",
            "rate": fee_config["rate"],
            "estimated_fee": estimated_fee,
            "estimated_revenue": annual_revenue,
            "potential_savings": potential_savings,
            "description": f"15% of first-year savings (${potential_savings:,.0f})"
        }

def extract_price(listing: Dict) -> Optional[float]:
    """Extract price from listing data"""
    
    # Try price field first
    price_str = listing.get("price", "")
    if price_str:
        try:
            # Remove $ and commas
            price_str = price_str.replace("$", "").replace(",", "")
            return float(price_str)
        except:
            pass
    
    # Try to extract from title or description
    text = f"{listing.get('title', '')} {listing.get('description', '')}"
    
    # Look for price patterns
    import re
    
    # Pattern for $XX,XXX or $XXX,XXX
    price_patterns = [
        r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',  # $XX,XXX.XX
        r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:dollars|usd)',  # XX,XXX dollars
    ]
    
    for pattern in price_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            try:
                price_str = matches[0].replace(",", "")
                price = float(price_str)
                if price >= CONFIG["min_price"] and price <= CONFIG["max_price"]:
                    return price
            except:
                continue
    
    return None

def estimate_service_revenue(listing: Dict, price: float) -> float:
    """Estimate annual revenue for service business"""
    
    title = listing.get("title", "").lower()
    description = listing.get("description", "").lower()
    
    # Check for indicators in text
    text = f"{title} {description}"
    
    # Monthly service indicators
    monthly_indicators = ["monthly", "per month", "/month", "monthly rate"]
    weekly_indicators = ["weekly", "per week", "/week", "weekly rate"]
    hourly_indicators = ["hourly", "per hour", "/hr", "/hour"]
    
    # Default assumptions based on price
    if any(indicator in text for indicator in monthly_indicators):
        # Price is monthly rate
        return price * 12
    
    elif any(indicator in text for indicator in weekly_indicators):
        # Price is weekly rate
        return price * 52
    
    elif any(indicator in text for indicator in hourly_indicators):
        # Price is hourly rate
        # Assume 20 billable hours/week
        return price * 20 * 52
    
    else:
        # Default: assume price is monthly asking price for business
        # Use industry multiple (2-3x revenue for service businesses)
        return price / 2.5  # Middle of range

def save_leads(leads: List[Dict], category_name: str):
    """Save leads to JSON and CSV files"""
    
    if not leads:
        print(f"  No qualified leads for {category_name}")
        return
    
    # Create timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Ensure directory exists
    ensure_directory(CONFIG["output_dir"])
    ensure_directory(f"{CONFIG['output_dir']}/{category_name}")
    ensure_directory(f"{CONFIG['output_dir']}/{category_name}/{date_str}")
    
    # Save JSON
    json_file = f"{CONFIG['output_dir']}/{category_name}/{date_str}/leads_{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump(leads, f, indent=2)
    
    # Save CSV
    csv_file = f"{CONFIG['output_dir']}/{category_name}/{date_str}/leads_{timestamp}.csv"
    
    # Flatten data for CSV
    flattened_leads = []
    for lead in leads:
        flat_lead = {
            "title": lead.get("title", ""),
            "price": lead.get("price", ""),
            "location": lead.get("location", ""),
            "city": lead.get("city", ""),
            "category": lead.get("category", ""),
            "url": lead.get("craigslist_url", ""),
            "scraped_at": lead.get("scraped_at", ""),
            "description": lead.get("description", "")[:200]  # Truncate
        }
        
        # Add referral fee details
        if lead.get("referral_fee"):
            fee = lead["referral_fee"]
            flat_lead.update({
                "fee_type": fee.get("type", ""),
                "estimated_fee": fee.get("estimated_fee", 0),
                "fee_description": fee.get("description", "")
            })
        
        flattened_leads.append(flat_lead)
    
    df = pd.DataFrame(flattened_leads)
    df.to_csv(csv_file, index=False)
    
    print(f"  Saved {len(leads)} leads to {json_file}")
    print(f"  Saved CSV to {csv_file}")
    
    return json_file, csv_file

def generate_summary_report(leads_by_category: Dict[str, List[Dict]]):
    """Generate summary report of all leads"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_leads": 0,
        "total_estimated_fees": 0,
        "by_category": {},
        "top_opportunities": []
    }
    
    # Calculate totals
    for category_name, leads in leads_by_category.items():
        if not leads:
            continue
        
        category_total = len(leads)
        category_fees = sum(lead.get("referral_fee", {}).get("estimated_fee", 0) for lead in leads)
        
        summary["by_category"][category_name] = {
            "lead_count": category_total,
            "estimated_fees": category_fees,
            "avg_fee_per_lead": category_fees / category_total if category_total > 0 else 0
        }
        
        summary["total_leads"] += category_total
        summary["total_estimated_fees"] += category_fees
        
        # Add top opportunities
        sorted_leads = sorted(leads, key=lambda x: x.get("referral_fee", {}).get("estimated_fee", 0), reverse=True)
        for lead in sorted_leads[:5]:  # Top 5 per category
            fee = lead.get("referral_fee", {})
            summary["top_opportunities"].append({
                "title": lead.get("title", "Unknown"),
                "category": category_name,
                "city": lead.get("city", ""),
                "price": lead.get("price", ""),
                "estimated_fee": fee.get("estimated_fee", 0),
                "url": lead.get("craigslist_url", "")
            })
    
    # Save summary
    summary_file = f"{CONFIG['output_dir']}/summary_{date_str}_{timestamp}.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n{'='*60}")
    print("SUMMARY REPORT")
    print(f"{'='*60}")
    print(f"Total Leads: {summary['total_leads']}")
    print(f"Total Estimated Fees: ${summary['total_estimated_fees']:,.2f}")
    
    for category_name, stats in summary["by_category"].items():
        print(f"\n{category_name.upper()}:")
        print(f"  Leads: {stats['lead_count']}")
        print(f"  Estimated Fees: ${stats['estimated_fees']:,.2f}")
        print(f"  Avg Fee/Lead: ${stats['avg_fee_per_lead']:,.2f}")
    
    print(f"\nTop Opportunities:")
    for opp in summary["top_opportunities"][:10]:
        print(f"  ${opp['estimated_fee']:,.0f} - {opp['title'][:50]}... ({opp['category']}, {opp['city']})")
    
    print(f"{'='*60}")
    
    return summary_file

def create_actionable_report(leads_by_category: Dict[str, List[Dict]], summary_file: str):
    """Create actionable report for agent follow-up"""
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    report_file = f"{CONFIG['output_dir']}/actionable_report_{date_str}.md"
    
    with open(report_file, 'w') as f:
        f.write(f"# Craigslist Referral Fee Opportunities - {date_str}\n\n")
        f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        
        f.write("## Executive Summary\n\n")
        
        total_leads = sum(len(leads) for leads in leads_by_category.values())
        total_fees = sum(
            sum(lead.get("referral_fee", {}).get("estimated_fee", 0) for lead in leads)
            for leads in leads_by_category.values()
        )
        
        f.write(f"- **Total Opportunities:** {total_leads}\n")
        f.write(f"- **Total Estimated Fees:** ${total_fees:,.2f}\n")
        f.write(f"- **Average Fee/Opportunity:** ${total_fees/total_leads:,.2f}\n\n")
        
        f.write("## By Category\n\n")
        
        for category_name, leads in leads_by_category.items():
            if not leads:
                continue
            
            category_fees = sum(lead.get("referral_fee", {}).get("estimated_fee", 0) for lead in leads)
            
            f.write(f"### {category_name.replace('_', ' ').title()} ({len(leads)} opportunities)\n\n")
            f.write(f"**Estimated Fees:** ${category_fees:,.2f}\n\n")
            
            f.write("| Title | Price | City | Est. Fee | Action |\n")
            f.write("|-------|-------|------|----------|--------|\n")
            
            for lead in sorted(leads, key=lambda x: x.get("referral_fee", {}).get("estimated_fee", 0), reverse=True)[:10]:
                title = lead.get("title", "Unknown")[:50]
                price = lead.get("price", "N/A")
                city = lead.get("city", "")
                fee = lead.get("referral_fee", {}).get("estimated_fee", 0)
                url = lead.get("craigslist_url", "")
                
                if category_name == "business_for_sale":
                    action = "Contact seller for M&A referral"
                else:
                    action = "Pitch expense reduction services"
                
                f.write(f"| [{title}...]({url}) | {price} | {city} | ${fee:,.0f} | {action} |\n")
            
            f.write("\n")
        
        f.write("## Next Steps\n\n")
        f.write("1. **Business-for-Sale Leads:** Contact sellers, offer M&A brokerage services\n")
        f.write("2. **Service Business Leads:** Pitch expense reduction (15% of savings referral)\n")
        f.write("3. **Follow-up:** Use AgentMail for automated outreach\n")
        f.write("4. **Track:** Log responses in CRM for conversion tracking\n")
    
    print(f"Actionable report saved to: {report_file}")
    return report_file

def main():
    """Main execution function"""
    
    print(f"{'='*60}")
    print("CRAIGSLIST REFERRAL FEE LEAD GENERATOR")
    print(f"{'='*60}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Cities: {', '.join(CONFIG['cities'])}")
    print(f"Categories: {', '.join(CONFIG['categories'].keys())}")
    print(f"{