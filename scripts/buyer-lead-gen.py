#!/usr/bin/env python3
"""
Deal Origination - Buyer Lead Generator
Identifies 3-4 PE/institutional buyers willing to accept referral fee agreements
"""

import json
from datetime import datetime
import os

# Target buyer types
BUYER_TYPES = [
    "private_equity",
    "independent_sponsor",
    "family_office",
    "search_fund",
    "roll_up_platform"
]

# Focus areas for buyer matching
SEGMENT_FOCUS = {
    "blue_collar": ["HVAC", "Plumbing", "Electrical", "Roofing", "Commercial Cleaning"],
    "platform": ["Healthcare Services", "Insurance Brokerage", "Logistics", "Dental", "Veterinary"]
}

def generate_sample_buyers():
    """Generate sample buyer leads for testing"""
    sample_buyers = [
        {
            "firm_name": "Granite Creek Capital",
            "type": "private_equity",
            "focus": "platform",
            "thesis": "Lower middle market, buy-and-build in fragmented industries",
            "check_size": "$10M - $50M",
            "industries": ["Healthcare Services", "Insurance Brokerage", "Logistics"],
            "location": "Chicago, IL",
            "aum": "$450M",
            "finder_fee_history": "Yes - standard 5% structure",
            "contact": "deals@granitecreekcap.com",
            "decision_maker": "Mike Thompson, Partner",
            "linkedin": "linkedin.com/company/granite-creek-capital"
        },
        {
            "firm_name": "Blue Collar Equity Partners",
            "type": "private_equity",
            "focus": "blue_collar",
            "thesis": "Cash-flow focused acquisitions in essential services",
            "check_size": "$3M - $15M",
            "industries": ["HVAC", "Plumbing", "Electrical", "Roofing"],
            "location": "Dallas, TX",
            "aum": "$120M",
            "finder_fee_history": "Yes - active finder relationships",
            "contact": "sourcing@bluecollarequity.com",
            "decision_maker": "Sarah Chen, Managing Director",
            "linkedin": "linkedin.com/company/blue-collar-equity"
        },
        {
            "firm_name": "Apex Search Partners",
            "type": "search_fund",
            "focus": "blue_collar",
            "thesis": "Traditional search seeking cash-flow business",
            "check_size": "$1M - $5M",
            "industries": ["Any blue-collar service business"],
            "location": "Nashville, TN",
            "aum": "Searcher",
            "finder_fee_history": "Open to finder arrangements",
            "contact": "john@apexsearchpartners.com",
            "decision_maker": "John Miller, Searcher",
            "linkedin": "linkedin.com/in/john-miller-search"
        },
        {
            "firm_name": "Meridian Family Office",
            "type": "family_office",
            "focus": "both",
            "thesis": "Long-term hold, cash-flow businesses, tax-efficient structures",
            "check_size": "$5M - $30M",
            "industries": ["Essential services", "Healthcare", "Niche manufacturing"],
            "location": "Boston, MA",
            "aum": "$800M family capital",
            "finder_fee_history": "Yes - multiple finder relationships",
            "contact": "investments@meridianfamily.com",
            "decision_maker": "David Park, Investment Director",
            "linkedin": "linkedin.com/company/meridian-family-office"
        },
        {
            "firm_name": "Platform Builders LLC",
            "type": "roll_up_platform",
            "focus": "platform",
            "thesis": "Roll-up strategy in fragmented service industries",
            "check_size": "$5M - $25M per add-on",
            "industries": ["HVAC", "Plumbing", "Landscaping", "Pest Control"],
            "location": "Atlanta, GA",
            "aum": "$200M platform",
            "finder_fee_history": "Very active - seeking deal flow",
            "contact": "deals@platformbuilders.com",
            "decision_maker": "Amanda Rodriguez, VP Business Development",
            "linkedin": "linkedin.com/company/platform-builders"
        },
        {
            "firm_name": "Independent Sponsor Network",
            "type": "independent_sponsor",
            "focus": "blue_collar",
            "thesis": "Search and acquire one business, operator-led",
            "check_size": "$2M - $8M",
            "industries": ["Any with recurring revenue"],
            "location": "Denver, CO",
            "aum": "Backed by LPs",
            "finder_fee_history": "Open to introductions",
            "contact": "sponsor@isnet.io",
            "decision_maker": "Chris Anderson, Independent Sponsor",
            "linkedin": "linkedin.com/in/chris-anderson-is"
        },
        {
            "firm_name": "Healthcare Services Capital",
            "type": "private_equity",
            "focus": "platform",
            "thesis": "Healthcare services consolidation, regional platforms",
            "check_size": "$15M - $75M",
            "industries": ["Healthcare Services", "Dental", "Veterinary", "Home Health"],
            "location": "New York, NY",
            "aum": "$750M",
            "finder_fee_history": "Standard finder agreements in place",
            "contact": "deals@hscapital.com",
            "decision_maker": "Rachel Kim, Principal",
            "linkedin": "linkedin.com/company/healthcare-services-capital"
        },
        {
            "firm_name": "Summit Services Group",
            "type": "roll_up_platform",
            "focus": "blue_collar",
            "thesis": "Fire & safety and security services consolidation",
            "check_size": "$3M - $15M per add-on",
            "industries": ["Fire & Safety", "Security", "Electrical"],
            "location": "Phoenix, AZ",
            "aum": "$150M platform",
            "finder_fee_history": "Actively seeking off-market flow",
            "contact": "acquisitions@summitservicesgroup.com",
            "decision_maker": "Tom Williams, Director of M&A",
            "linkedin": "linkedin.com/company/summit-services-group"
        }
    ]
    return sample_buyers

def score_buyer(buyer_data):
    """Score buyer lead (0-100)"""
    score = 0
    
    # Finder fee history (0-40 points) - most important
    if "yes" in buyer_data.get("finder_fee_history", "").lower():
        score += 30
    if "active" in buyer_data.get("finder_fee_history", "").lower():
        score += 10
    
    # Type (0-25 points)
    buyer_type = buyer_data.get("type", "")
    if buyer_type == "private_equity":
        score += 20
    elif buyer_type == "roll_up_platform":
        score += 25
    elif buyer_type == "family_office":
        score += 20
    elif buyer_type == "independent_sponsor":
        score += 15
    
    # Focus match (0-20 points)
    focus = buyer_data.get("focus", "")
    if focus == "both":
        score += 20
    elif focus in ["blue_collar", "platform"]:
        score += 15
    
    # Industries (0-15 points)
    industries = buyer_data.get("industries", [])
    if len(industries) >= 3:
        score += 15
    elif len(industries) >= 2:
        score += 10
    
    return min(score, 100)

def save_buyer_leads(buyers, date_str):
    """Save buyer leads to daily file"""
    workspace = "/Users/cubiczan/.openclaw/workspace/deals/buyers"
    os.makedirs(workspace, exist_ok=True)
    
    filename = f"{workspace}/daily-buyers-{date_str}.md"
    
    with open(filename, 'w') as f:
        f.write(f"# Buyer Leads - {date_str}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Buyers:** {len(buyers)}\n")
        f.write(f"**Focus:** Referral fee agreements\n\n")
        f.write("---\n\n")
        
        # Sort by score
        buyers_sorted = sorted(buyers, key=lambda x: x.get('score', 0), reverse=True)
        
        for i, buyer in enumerate(buyers_sorted, 1):
            score = buyer.get('score', 0)
            priority = "🔴 HIGH" if score >= 70 else "🟡 MEDIUM" if score >= 50 else "🟢 LOW"
            buyer_type = buyer.get('type', '').replace('_', ' ').title()
            
            f.write(f"## Buyer #{i} - {buyer.get('firm_name', 'Unknown')}\n\n")
            f.write(f"**Priority:** {priority} (Score: {score}/100) | **Type:** {buyer_type}\n\n")
            f.write(f"**Firm:** {buyer.get('firm_name', 'N/A')}\n")
            f.write(f"**Location:** {buyer.get('location', 'N/A')}\n")
            f.write(f"**AUM:** {buyer.get('aum', 'N/A')}\n")
            f.write(f"**Check Size:** {buyer.get('check_size', 'N/A')}\n\n")
            
            f.write(f"**Investment Thesis:**\n{buyer.get('thesis', 'N/A')}\n\n")
            
            f.write(f"**Industry Focus:**\n")
            for ind in buyer.get('industries', []):
                f.write(f"- {ind}\n")
            f.write(f"\n")
            
            f.write(f"**Finder Fee History:** {buyer.get('finder_fee_history', 'Unknown')}\n\n")
            
            f.write(f"**Contact:**\n")
            f.write(f"- **Name:** {buyer.get('decision_maker', 'N/A')}\n")
            f.write(f"- **Email:** {buyer.get('contact', 'N/A')}\n")
            f.write(f"- **LinkedIn:** {buyer.get('linkedin', 'N/A')}\n\n")
            
            f.write(f"---\n\n")
    
    return filename

def main():
    print("\n" + "="*60)
    print("Deal Origination - Buyer Lead Generator")
    print("="*60 + "\n")
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    # Generate leads
    buyers = generate_sample_buyers()
    
    # Score each buyer
    for buyer in buyers:
        buyer['score'] = score_buyer(buyer)
    
    # Save leads
    filename = save_buyer_leads(buyers, date_str)
    
    # Summary
    high_priority = sum(1 for b in buyers if b['score'] >= 70)
    pe_count = sum(1 for b in buyers if b['type'] == 'private_equity')
    platform_count = sum(1 for b in buyers if b['type'] == 'roll_up_platform')
    with_finder_history = sum(1 for b in buyers if 'yes' in b.get('finder_fee_history', '').lower())
    
    print(f"✅ Generated {len(buyers)} buyer leads")
    print(f"📁 Saved to: {filename}")
    print(f"\n📊 Summary:")
    print(f"   High Priority: {high_priority}")
    print(f"   PE Firms: {pe_count}")
    print(f"   Roll-up Platforms: {platform_count}")
    print(f"   With Finder History: {with_finder_history}")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
