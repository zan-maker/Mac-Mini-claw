#!/usr/bin/env python3
"""
Daily Craigslist Referral Fee Lead Generator
Runs as cron job to find referral fee opportunities
"""

import craigslistscraper as cs
import json
import os
import time
from datetime import datetime
import re

# Configuration
CONFIG = {
    "cities": ["newyork", "losangeles"],
    "categories": {
        "business_for_sale": "biz",
        "skilled_trade": "sks"
    },
    "max_ads_per_category": 20,
    "output_dir": "/Users/cubiczan/.openclaw/workspace/craigslist-leads"
}

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def extract_price(text):
    """Extract price from text"""
    if not text:
        return None
    
    # Look for price patterns
    patterns = [
        r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:dollars|usd)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            try:
                price_str = matches[0].replace(",", "")
                price = float(price_str)
                if 10000 <= price <= 5000000:  # Reasonable range for referral fees
                    return price
            except:
                continue
    
    return None

def calculate_referral_fee(category, price, title):
    """Calculate potential referral fee"""
    
    if not price:
        return None
    
    if category == "business_for_sale":
        # 1% of business sale, min $5K, max $50K
        fee = price * 0.01
        fee = max(5000, min(50000, fee))
        return {
            "type": "business_sale_referral",
            "estimated_fee": fee,
            "business_value": price,
            "description": f"1% referral on ${price:,.0f} business sale"
        }
    
    elif category == "skilled_trade":
        # Estimate revenue and savings
        annual_revenue = price * 12  # Assume monthly price
        annual_expenses = annual_revenue * 0.6
        potential_savings = annual_expenses * 0.2  # 20% savings
        fee = potential_savings * 0.15  # 15% of savings
        fee = max(1000, min(10000, fee))
        
        return {
            "type": "expense_reduction_referral",
            "estimated_fee": fee,
            "estimated_revenue": annual_revenue,
            "potential_savings": potential_savings,
            "description": f"15% of ${potential_savings:,.0f} annual savings"
        }
    
    return None

def scrape_daily():
    """Main scraping function for daily cron job"""
    
    print(f"{'='*60}")
    print(f"DAILY CRAIGSLIST REFERRAL FEE SCRAPER")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    ensure_dir(CONFIG["output_dir"])
    
    all_leads = []
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    for category_name, category_code in CONFIG["categories"].items():
        print(f"\nScraping {category_name.replace('_', ' ').title()}...")
        
        for city in CONFIG["cities"]:
            print(f"  City: {city}")
            
            try:
                # Create search
                search = cs.Search(
                    city=city,
                    category=category_code,
                    query=""
                )
                
                # Fetch results
                status = search.fetch()
                if status != 200:
                    print(f"    Failed: HTTP {status}")
                    continue
                
                print(f"    Found {len(search.ads)} ads")
                
                # Process ads
                processed = 0
                for ad in search.ads[:CONFIG["max_ads_per_category"]]:
                    try:
                        # Fetch ad details
                        ad_status = ad.fetch()
                        if ad_status != 200:
                            continue
                        
                        data = ad.to_dict()
                        
                        # Extract price
                        text = f"{data.get('title', '')} {data.get('description', '')}"
                        price = extract_price(text)
                        
                        if price:
                            # Calculate referral fee
                            fee_info = calculate_referral_fee(category_name, price, data.get('title', ''))
                            
                            if fee_info and fee_info["estimated_fee"] >= 1000:
                                lead = {
                                    "title": data.get("title", ""),
                                    "description": data.get("description", "")[:500],
                                    "price": f"${price:,.0f}",
                                    "location": data.get("location", ""),
                                    "city": city,
                                    "category": category_name,
                                    "url": ad.url,
                                    "scraped_at": datetime.now().isoformat(),
                                    "referral_fee": fee_info
                                }
                                
                                all_leads.append(lead)
                                print(f"    ✓ ${fee_info['estimated_fee']:,.0f} - {data.get('title', '')[:50]}...")
                        
                        processed += 1
                        if processed >= 10:  # Limit per city
                            break
                            
                        time.sleep(0.5)  # Be respectful
                        
                    except Exception as e:
                        print(f"    Error processing ad: {e}")
                        continue
                
                time.sleep(1)  # Be respectful between cities
                
            except Exception as e:
                print(f"  Error scraping {city}: {e}")
    
    # Save results
    if all_leads:
        # Save JSON
        json_file = f"{CONFIG['output_dir']}/daily_leads_{date_str}.json"
        with open(json_file, 'w') as f:
            json.dump(all_leads, f, indent=2)
        
        # Calculate summary
        total_fees = sum(lead["referral_fee"]["estimated_fee"] for lead in all_leads)
        
        # Create summary report
        summary = {
            "date": date_str,
            "total_leads": len(all_leads),
            "total_estimated_fees": total_fees,
            "avg_fee_per_lead": total_fees / len(all_leads) if all_leads else 0,
            "top_opportunities": sorted(all_leads, key=lambda x: x["referral_fee"]["estimated_fee"], reverse=True)[:5]
        }
        
        summary_file = f"{CONFIG['output_dir']}/daily_summary_{date_str}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n{'='*60}")
        print("DAILY SUMMARY")
        print(f"{'='*60}")
        print(f"Total Qualified Leads: {len(all_leads)}")
        print(f"Total Estimated Fees: ${total_fees:,.2f}")
        print(f"Average Fee/Lead: ${summary['avg_fee_per_lead']:,.2f}")
        
        print(f"\nTop 5 Opportunities:")
        for i, lead in enumerate(summary["top_opportunities"], 1):
            fee = lead["referral_fee"]["estimated_fee"]
            title = lead["title"][:60]
            category = lead["category"].replace("_", " ").title()
            print(f"  {i}. ${fee:,.0f} - {title}... ({category})")
        
        print(f"\nFiles saved:")
        print(f"  - Leads: {json_file}")
        print(f"  - Summary: {summary_file}")
        
        # Create Discord message
        discord_message = create_discord_message(summary, all_leads)
        discord_file = f"{CONFIG['output_dir']}/discord_report_{date_str}.txt"
        with open(discord_file, 'w') as f:
            f.write(discord_message)
        
        print(f"  - Discord report: {discord_file}")
        
    else:
        print(f"\nNo qualified leads found today.")
    
    print(f"\n{'='*60}")
    print("DAILY SCRAPING COMPLETE")
    print(f"{'='*60}")

def create_discord_message(summary, all_leads):
    """Create Discord-friendly report"""
    
    message = f"**📊 Daily Craigslist Referral Fee Report**\n"
    message += f"*{datetime.now().strftime('%Y-%m-%d')}*\n\n"
    
    message += f"**Total Opportunities:** {summary['total_leads']}\n"
    message += f"**Total Estimated Fees:** ${summary['total_estimated_fees']:,.2f}\n"
    message += f"**Avg Fee/Opportunity:** ${summary['avg_fee_per_lead']:,.2f}\n\n"
    
    # Group by category
    biz_leads = [l for l in all_leads if l["category"] == "business_for_sale"]
    service_leads = [l for l in all_leads if l["category"] == "skilled_trade"]
    
    if biz_leads:
        biz_fees = sum(l["referral_fee"]["estimated_fee"] for l in biz_leads)
        message += f"**🏢 Business-for-Sale:** {len(biz_leads)} leads (${biz_fees:,.0f})\n"
    
    if service_leads:
        service_fees = sum(l["referral_fee"]["estimated_fee"] for l in service_leads)
        message += f"**🔧 Service Businesses:** {len(service_leads)} leads (${service_fees:,.0f})\n"
    
    message += f"\n**🎯 Top Opportunities:**\n"
    
    for i, lead in enumerate(summary["top_opportunities"][:3], 1):
        fee = lead["referral_fee"]["estimated_fee"]
        title = lead["title"][:50]
        city = lead["city"]
        category = "Biz Sale" if lead["category"] == "business_for_sale" else "Service"
        
        message += f"{i}. **${fee:,.0f}** - {title}... ({city}, {category})\n"
    
    message += f"\n**📈 Next Steps:**\n"
    message += f"1. Business sales → Contact sellers for M&A referral (1% fee)\n"
    message += f"2. Service businesses → Pitch expense reduction (15% of savings)\n"
    message += f"3. Use AgentMail for automated outreach\n"
    
    return message

if __name__ == "__main__":
    scrape_daily()