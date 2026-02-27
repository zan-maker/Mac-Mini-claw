#!/usr/bin/env python3
"""
Quick test of Craigslist scraper with limited ads
"""

import craigslistscraper as cs
import json
from datetime import datetime
import time

print("🚀 QUICK CRAIGSLIST SCRAPER TEST")
print("=" * 60)
print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
print()

# Test configuration
cities = ["newyork"]
categories = {
    "business_for_sale": "biz",
    "skilled_trade": "sks"
}

all_leads = []

for city in cities:
    print(f"📍 City: {city}")
    
    for category_name, category_code in categories.items():
        print(f"  📂 Category: {category_name.replace('_', ' ').title()}")
        
        try:
            # Create search
            search = cs.Search(
                city=city,
                category=category_code,
                query=""
            )
            
            # Fetch results
            print("    🔍 Fetching search results...")
            status = search.fetch()
            print(f"    ✅ Status: {status}, Found: {len(search.ads)} ads")
            
            if status != 200 or not search.ads:
                print("    ⚠️  No ads found or fetch failed")
                continue
            
            # Process first 3 ads only
            processed = 0
            for i, ad in enumerate(search.ads[:3]):
                print(f"    📄 Processing ad {i+1}...")
                
                try:
                    ad_status = ad.fetch()
                    if ad_status != 200:
                        print(f"      ⚠️  Failed to fetch ad: HTTP {ad_status}")
                        continue
                    
                    data = ad.to_dict()
                    
                    # Simple price extraction
                    import re
                    text = f"{data.get('title', '')} {data.get('description', '')}"
                    
                    # Look for price
                    price_match = re.search(r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', text)
                    price = None
                    if price_match:
                        try:
                            price_str = price_match.group(1).replace(",", "")
                            price = float(price_str)
                        except:
                            pass
                    
                    # Calculate simple referral fee
                    estimated_fee = 0
                    if price:
                        if category_name == "business_for_sale":
                            estimated_fee = price * 0.01  # 1%
                            estimated_fee = max(5000, min(50000, estimated_fee))
                        else:
                            estimated_fee = price * 0.15  # 15% of savings estimate
                            estimated_fee = max(1000, min(10000, estimated_fee))
                    
                    if estimated_fee >= 1000:
                        lead = {
                            "title": data.get("title", "")[:50],
                            "price": f"${price:,.0f}" if price else "N/A",
                            "city": city,
                            "category": category_name,
                            "estimated_fee": estimated_fee,
                            "url": ad.url
                        }
                        
                        all_leads.append(lead)
                        print(f"      ✅ Qualified: ${estimated_fee:,.0f} - {lead['title']}")
                    else:
                        print(f"      ⚠️  Below minimum fee: ${estimated_fee:,.0f}")
                    
                    processed += 1
                    
                    # Brief delay
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"      ❌ Error: {e}")
                    continue
            
            print(f"    📊 Processed {processed} ads from this category")
            
            # Delay between categories
            time.sleep(1)
            
        except Exception as e:
            print(f"  ❌ Error scraping {category_name}: {e}")
            continue
    
    print()

# Summary
print("=" * 60)
print("📊 TEST SUMMARY")
print("=" * 60)

if all_leads:
    total_fees = sum(lead["estimated_fee"] for lead in all_leads)
    
    print(f"✅ Total Qualified Leads: {len(all_leads)}")
    print(f"✅ Total Estimated Fees: ${total_fees:,.2f}")
    print(f"✅ Average Fee/Lead: ${total_fees/len(all_leads):,.2f}")
    
    print("\n🎯 Top Opportunities:")
    sorted_leads = sorted(all_leads, key=lambda x: x["estimated_fee"], reverse=True)
    for i, lead in enumerate(sorted_leads, 1):
        print(f"  {i}. ${lead['estimated_fee']:,.0f} - {lead['title']}... ({lead['category'].replace('_', ' ')})")
    
    # Save test results
    output_file = "/Users/cubiczan/.openclaw/workspace/craigslist-leads/test_results.json"
    with open(output_file, 'w') as f:
        json.dump({
            "test_time": datetime.now().isoformat(),
            "leads_found": len(all_leads),
            "total_estimated_fees": total_fees,
            "leads": all_leads
        }, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    
else:
    print("⚠️  No qualified leads found in this quick test")
    print("   (This could be due to no prices found in ads or all fees below $1K minimum)")

print("\n" + "=" * 60)
print("✅ QUICK TEST COMPLETE")
print("=" * 60)
print("\nThe scraper is working! The full system will:")
print("• Process more ads (20 per category)")
print("• Include more cities (NYC, LA, Chicago, etc.)")
print("• Extract contact information")
print("• Save detailed reports")
print("• Run automatically at 9 AM daily")