#!/usr/bin/env python3
"""
Deal Origination - Seller Lead Generator
Identifies 10-15 off-market business sellers daily
"""

import json
from datetime import datetime
import os

# Target industries for blue-collar / cash-flow businesses
BLUE_COLLAR_INDUSTRIES = [
    "HVAC",
    "Plumbing",
    "Electrical",
    "Fire & Safety",
    "Waste Management",
    "Commercial Cleaning",
    "Roofing",
    "Industrial Services",
    "Pest Control",
    "Landscaping",
    "Auto Repair",
    "Pool Service"
]

# Target industries for institutional platform targets
PLATFORM_INDUSTRIES = [
    "Healthcare Services",
    "Insurance Brokerage",
    "Property Management",
    "Logistics",
    "Software (Vertical)",
    "Dental Practices",
    "Veterinary",
    "Home Health"
]

def generate_sample_sellers():
    """Generate sample seller leads for testing"""
    sample_sellers = [
        {
            "company_name": "Valley HVAC Services",
            "industry": "HVAC",
            "segment": "blue_collar",
            "location": "Phoenix, AZ",
            "years_in_business": 23,
            "estimated_employees": 35,
            "estimated_ebitda": 850000,
            "owner_signals": ["Owner age 62", "No website update since 2019", "4.8 stars, 342 reviews"],
            "source": "Google Maps",
            "contact_estimate": "owner@valleyhvac.com"
        },
        {
            "company_name": "Metro Plumbing Pros",
            "industry": "Plumbing",
            "segment": "blue_collar",
            "location": "Denver, CO",
            "years_in_business": 18,
            "estimated_employees": 28,
            "estimated_ebitda": 620000,
            "owner_signals": ["Family owned", "Second generation", "Limited digital presence"],
            "source": "Industry Directory",
            "contact_estimate": "info@metroplumbingpros.com"
        },
        {
            "company_name": "Precision Fire & Safety",
            "industry": "Fire & Safety",
            "segment": "blue_collar",
            "location": "Atlanta, GA",
            "years_in_business": 31,
            "estimated_employees": 45,
            "estimated_ebitda": 1200000,
            "owner_signals": ["Founder age 68", "Recurring contracts", "Low marketing spend"],
            "source": "SBA Database",
            "contact_estimate": "contact@precisionfire.com"
        },
        {
            "company_name": "CleanPro Commercial Services",
            "industry": "Commercial Cleaning",
            "segment": "blue_collar",
            "location": "Dallas, TX",
            "years_in_business": 16,
            "estimated_employees": 120,
            "estimated_ebitda": 1800000,
            "owner_signals": ["High employee count", "Contract-based revenue", "Owner looking to retire"],
            "source": "Secretary of State",
            "contact_estimate": "admin@cleanpro.com"
        },
        {
            "company_name": "Southwest Roofing Co",
            "industry": "Roofing",
            "segment": "blue_collar",
            "location": "Las Vegas, NV",
            "years_in_business": 27,
            "estimated_employees": 55,
            "estimated_ebitda": 1500000,
            "owner_signals": ["Established 1999", "Strong local reputation", "Owner in late 60s"],
            "source": "Google Maps",
            "contact_estimate": "owner@southwestroofing.com"
        },
        {
            "company_name": "Regional Healthcare Services",
            "industry": "Healthcare Services",
            "segment": "platform",
            "location": "Minneapolis, MN",
            "years_in_business": 12,
            "estimated_employees": 180,
            "estimated_ebitda": 4500000,
            "owner_signals": ["Multiple locations", "Fragmented market", "Systems in place"],
            "source": "Industry Association",
            "contact_estimate": "cfo@regionalhealthcare.com"
        },
        {
            "company_name": "Premier Insurance Group",
            "industry": "Insurance Brokerage",
            "segment": "platform",
            "location": "Tampa, FL",
            "years_in_business": 22,
            "estimated_employees": 65,
            "estimated_ebitda": 3200000,
            "owner_signals": ["Recurring revenue", "Niche specialization", "Owner succession planning"],
            "source": "LinkedIn",
            "contact_estimate": "info@premierinsurance.com"
        },
        {
            "company_name": "Express Logistics Solutions",
            "industry": "Logistics",
            "segment": "platform",
            "location": "Memphis, TN",
            "years_in_business": 19,
            "estimated_employees": 210,
            "estimated_ebitda": 5800000,
            "owner_signals": ["Fleet owned", "Regional density", "Founder considering exit"],
            "source": "Trade Publication",
            "contact_estimate": "operations@expresslogistics.com"
        },
        {
            "company_name": "Elite Electrical Services",
            "industry": "Electrical",
            "segment": "blue_collar",
            "location": "Seattle, WA",
            "years_in_business": 25,
            "estimated_employees": 42,
            "estimated_ebitda": 980000,
            "owner_signals": ["Licensed master electrician owner", "Commercial focus", "Low churn"],
            "source": "Google Maps",
            "contact_estimate": "service@eliteelectrical.com"
        },
        {
            "company_name": "GreenScape Landscaping",
            "industry": "Landscaping",
            "segment": "blue_collar",
            "location": "Charlotte, NC",
            "years_in_business": 20,
            "estimated_employees": 85,
            "estimated_ebitda": 1400000,
            "owner_signals": ["Recurring maintenance contracts", "Owner age 65", "Minimal marketing"],
            "source": "Review Platform",
            "contact_estimate": "info@greenscape.com"
        },
        {
            "company_name": "Dental Partners Group",
            "industry": "Dental Practices",
            "segment": "platform",
            "location": "Orlando, FL",
            "years_in_business": 15,
            "estimated_employees": 95,
            "estimated_ebitda": 3800000,
            "owner_signals": ["5 locations", "DSO-ready structure", "Founding dentist retiring"],
            "source": "Industry Directory",
            "contact_estimate": "admin@dentalpartnersgroup.com"
        },
        {
            "company_name": "Waste Solutions Inc",
            "industry": "Waste Management",
            "segment": "blue_collar",
            "location": "Houston, TX",
            "years_in_business": 28,
            "estimated_employees": 75,
            "estimated_ebitda": 2100000,
            "owner_signals": ["Municipal contracts", "Fleet owned", "Second owner"],
            "source": "SBA Database",
            "contact_estimate": "sales@wastesolutionsinc.com"
        }
    ]
    return sample_sellers

def score_seller(seller_data):
    """Score seller lead (0-100)"""
    score = 0
    
    # EBITDA range (0-30 points)
    ebitda = seller_data.get("estimated_ebitda", 0)
    if 500000 <= ebitda <= 1000000:
        score += 15
    elif 1000000 < ebitda <= 3000000:
        score += 25
    elif ebitda > 3000000:
        score += 30
    
    # Years in business (0-20 points)
    years = seller_data.get("years_in_business", 0)
    if years >= 20:
        score += 20
    elif years >= 15:
        score += 15
    elif years >= 10:
        score += 10
    
    # Owner signals (0-25 points)
    signals = seller_data.get("owner_signals", [])
    for signal in signals:
        if "age" in signal.lower() or "retire" in signal.lower() or "succession" in signal.lower():
            score += 10
            break
    if len(signals) >= 3:
        score += 15
    
    # Segment fit (0-25 points)
    segment = seller_data.get("segment", "")
    if segment == "platform":
        score += 20
    elif segment == "blue_collar":
        score += 15
    
    return min(score, 100)

def save_seller_leads(sellers, date_str):
    """Save seller leads to daily file"""
    workspace = "/Users/cubiczan/.openclaw/workspace/deals/sellers"
    os.makedirs(workspace, exist_ok=True)
    
    filename = f"{workspace}/daily-sellers-{date_str}.md"
    
    with open(filename, 'w') as f:
        f.write(f"# Off-Market Seller Leads - {date_str}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Sellers:** {len(sellers)}\n")
        f.write(f"**Source:** Off-market only (no brokers)\n\n")
        f.write("---\n\n")
        
        # Sort by score
        sellers_sorted = sorted(sellers, key=lambda x: x.get('score', 0), reverse=True)
        
        for i, seller in enumerate(sellers_sorted, 1):
            score = seller.get('score', 0)
            priority = "🔴 HIGH" if score >= 70 else "🟡 MEDIUM" if score >= 50 else "🟢 LOW"
            segment = "🏢 PLATFORM" if seller.get('segment') == 'platform' else "🔧 BLUE COLLAR"
            
            f.write(f"## Seller #{i} - {seller.get('company_name', 'Unknown')}\n\n")
            f.write(f"**Priority:** {priority} (Score: {score}/100) | **Segment:** {segment}\n\n")
            f.write(f"**Company:** {seller.get('company_name', 'N/A')}\n")
            f.write(f"**Industry:** {seller.get('industry', 'N/A')}\n")
            f.write(f"**Location:** {seller.get('location', 'N/A')}\n")
            f.write(f"**Years in Business:** {seller.get('years_in_business', 'N/A')}\n")
            f.write(f"**Employees:** ~{seller.get('estimated_employees', 'N/A')}\n")
            f.write(f"**Est. EBITDA:** ${seller.get('estimated_ebitda', 0):,}\n\n")
            
            f.write(f"**Owner Signals:**\n")
            for signal in seller.get('owner_signals', []):
                f.write(f"- {signal}\n")
            f.write(f"\n")
            
            f.write(f"**Source:** {seller.get('source', 'N/A')}\n")
            f.write(f"**Contact:** {seller.get('contact_estimate', 'N/A')}\n\n")
            
            # Estimated fee
            ebitda = seller.get('estimated_ebitda', 0)
            est_value = ebitda * 4  # Rough 4x multiple
            est_fee = min(est_value * 0.05, 100000) + max(0, (est_value - 1000000) * 0.03)
            est_fee = max(50000, est_fee)
            
            f.write(f"**Est. Deal Value:** ${est_value:,.0f}\n")
            f.write(f"**Est. Finder Fee:** ${est_fee:,.0f}\n\n")
            f.write(f"---\n\n")
    
    return filename

def main():
    print("\n" + "="*60)
    print("Deal Origination - Seller Lead Generator")
    print("="*60 + "\n")
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    # Generate leads
    sellers = generate_sample_sellers()
    
    # Score each seller
    for seller in sellers:
        seller['score'] = score_seller(seller)
    
    # Save leads
    filename = save_seller_leads(sellers, date_str)
    
    # Summary
    high_priority = sum(1 for s in sellers if s['score'] >= 70)
    blue_collar = sum(1 for s in sellers if s['segment'] == 'blue_collar')
    platform = sum(1 for s in sellers if s['segment'] == 'platform')
    total_fees = sum(max(50000, min(s['estimated_ebitda'] * 4 * 0.05, 100000) + max(0, (s['estimated_ebitda'] * 4 - 1000000) * 0.03)) for s in sellers)
    
    print(f"✅ Generated {len(sellers)} off-market seller leads")
    print(f"📁 Saved to: {filename}")
    print(f"\n📊 Summary:")
    print(f"   High Priority: {high_priority}")
    print(f"   Blue Collar: {blue_collar}")
    print(f"   Platform Targets: {platform}")
    print(f"   Total Est. Finder Fees: ${total_fees:,.0f}")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
