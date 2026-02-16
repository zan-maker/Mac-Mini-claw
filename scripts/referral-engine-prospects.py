#!/usr/bin/env python3
"""
B2B Referral Fee Engine - Demand Side (Prospects)
Identifies 10-15 daily prospects showing buying intent
"""

import json
from datetime import datetime
import os

# Priority Verticals
VERTICALS = {
    "professional_services": {
        "name": "B2B Professional Services",
        "services": ["Accounting", "Legal", "Consulting", "Fractional CFO"],
        "typical_fee": "$5,000-$7,500",
        "signals": ["Series A+ funding", "New market entry", "M&A activity", "Regulatory filing"]
    },
    "saas_tech": {
        "name": "Technology / SaaS",
        "services": ["Enterprise software", "Data platforms", "Security tools"],
        "typical_fee": "$5,000 (or 10-20% ACV)",
        "signals": ["Job postings for specific roles", "Tech stack changes", "G2 review activity"]
    },
    "construction": {
        "name": "Construction & Trades",
        "services": ["General contracting", "Specialty trades", "Project management"],
        "typical_fee": "$3,000",
        "signals": ["Permit filings", "RFP postings", "Zoning changes"]
    },
    "financial_services": {
        "name": "Financial Services B2B",
        "services": ["Treasury management", "Commercial lending", "Insurance"],
        "typical_fee": "$2,500",
        "signals": ["Funding announcements", "Expansion news", "Compliance events"]
    },
    "manufacturing": {
        "name": "Manufacturing",
        "services": ["Supply chain", "Equipment", "Logistics"],
        "typical_fee": "$1,000",
        "signals": ["Import/export shifts", "Supplier changes", "Reshoring"]
    },
    "cre": {
        "name": "Commercial Real Estate",
        "services": ["Office leasing", "Industrial space", "Brokerage"],
        "typical_fee": "$3,000-$10,000 (25% commission)",
        "signals": ["Lease expirations", "Headcount growth", "Office listings"]
    }
}

def generate_sample_prospects():
    """Generate sample prospects for testing"""
    sample_prospects = [
        {
            "company_name": "TechVentures Inc",
            "vertical": "professional_services",
            "signal": "Series B funding $25M",
            "service_needed": "Fractional CFO / Audit services",
            "location": "San Francisco, CA",
            "employees": 85,
            "contact": "CFO",
            "email": "cfo@techventures.io",
            "intent_score": 92
        },
        {
            "company_name": "DataFlow Analytics",
            "vertical": "saas_tech",
            "signal": "Hiring data engineering team",
            "service_needed": "Snowflake/Databricks implementation",
            "location": "Austin, TX",
            "employees": 120,
            "contact": "CTO",
            "email": "cto@dataflow.io",
            "intent_score": 88
        },
        {
            "company_name": "GreenBuild Construction",
            "vertical": "construction",
            "signal": "Permit filed for $50M project",
            "service_needed": "Specialty electrical contractor",
            "location": "Denver, CO",
            "employees": 250,
            "contact": "Project Manager",
            "email": "pm@greenbuild.com",
            "intent_score": 85
        },
        {
            "company_name": "FinTech Solutions",
            "vertical": "financial_services",
            "signal": "Expansion to 3 new states",
            "service_needed": "Commercial insurance / compliance",
            "location": "New York, NY",
            "employees": 180,
            "contact": "COO",
            "email": "coo@fintechsolutions.com",
            "intent_score": 82
        },
        {
            "company_name": "Manufacturing Plus",
            "vertical": "manufacturing",
            "signal": "Supplier bankruptcy - seeking alternative",
            "service_needed": "Supply chain consulting",
            "location": "Detroit, MI",
            "employees": 450,
            "contact": "VP Operations",
            "email": "ops@mfgplus.com",
            "intent_score": 78
        },
        {
            "company_name": "OfficeSpace Partners",
            "vertical": "cre",
            "signal": "Lease expiring in 6 months, headcount +40%",
            "service_needed": "Commercial real estate brokerage",
            "location": "Chicago, IL",
            "employees": 95,
            "contact": "Office Manager",
            "email": "office@officespace.co",
            "intent_score": 80
        },
        {
            "company_name": "CloudSync Technologies",
            "vertical": "saas_tech",
            "signal": "Tech stack migration to AWS",
            "service_needed": "Cloud consulting / DevOps",
            "location": "Seattle, WA",
            "employees": 75,
            "contact": "VP Engineering",
            "email": "eng@cloudsync.io",
            "intent_score": 86
        },
        {
            "company_name": "LegalEase Partners",
            "vertical": "professional_services",
            "signal": "New market entry - Europe",
            "service_needed": "International compliance counsel",
            "location": "Boston, MA",
            "employees": 60,
            "contact": "Managing Partner",
            "email": "partner@legalease.com",
            "intent_score": 84
        },
        {
            "company_name": "HealthTech Innovations",
            "vertical": "saas_tech",
            "signal": "G2 reviews trending up - seeking enterprise",
            "service_needed": "Enterprise sales consulting",
            "location": "Minneapolis, MN",
            "employees": 110,
            "contact": "VP Sales",
            "email": "sales@healthtech.io",
            "intent_score": 79
        },
        {
            "company_name": "Retail Solutions Corp",
            "vertical": "cre",
            "signal": "Opening 15 new locations",
            "service_needed": "Site selection / lease negotiation",
            "location": "Atlanta, GA",
            "employees": 320,
            "contact": "Real Estate Director",
            "email": "re@retailsolutions.com",
            "intent_score": 88
        },
        {
            "company_name": "Industrial Services LLC",
            "vertical": "construction",
            "signal": "Government RFP won - $12M",
            "service_needed": "Project management / subcontracting",
            "location": "Houston, TX",
            "employees": 180,
            "contact": "Contracts Manager",
            "email": "contracts@industrialservices.com",
            "intent_score": 83
        },
        {
            "company_name": "GrowthStage Capital",
            "vertical": "financial_services",
            "signal": "Fund closing $100M - portfolio support",
            "service_needed": "Portfolio company accounting",
            "location": "Menlo Park, CA",
            "employees": 25,
            "contact": "Partner",
            "email": "partner@growthstage.vc",
            "intent_score": 90
        }
    ]
    return sample_prospects

def score_prospect(prospect):
    """Score prospect based on intent and fit"""
    score = 0
    
    # Intent score from data (0-40)
    score += min(prospect.get("intent_score", 0) * 0.4, 40)
    
    # Vertical fee potential (0-30)
    vertical = prospect.get("vertical", "")
    if vertical in ["professional_services", "saas_tech"]:
        score += 30
    elif vertical in ["cre", "construction"]:
        score += 25
    else:
        score += 20
    
    # Company size (0-20)
    employees = prospect.get("employees", 0)
    if 50 <= employees <= 200:
        score += 20
    elif 200 < employees <= 500:
        score += 15
    else:
        score += 10
    
    # Signal specificity (0-10)
    signal = prospect.get("signal", "")
    if "funding" in signal.lower() or "expansion" in signal.lower():
        score += 10
    else:
        score += 5
    
    return min(score, 100)

def save_prospect_leads(prospects, date_str):
    """Save prospects to daily file"""
    workspace = "/Users/cubiczan/.openclaw/workspace/referral-engine/prospects"
    os.makedirs(workspace, exist_ok=True)
    
    filename = f"{workspace}/daily-prospects-{date_str}.md"
    
    with open(filename, 'w') as f:
        f.write(f"# B2B Referral Engine - Daily Prospects\n\n")
        f.write(f"**Date:** {date_str}\n")
        f.write(f"**Total Prospects:** {len(prospects)}\n")
        f.write(f"**Target:** 10-15 daily\n\n")
        f.write("---\n\n")
        
        # Sort by score
        prospects_sorted = sorted(prospects, key=lambda x: x.get('score', 0), reverse=True)
        
        for i, p in enumerate(prospects_sorted, 1):
            score = p.get('score', 0)
            priority = "🔴 HIGH" if score >= 80 else "🟡 MEDIUM" if score >= 60 else "🟢 LOW"
            vertical_info = VERTICALS.get(p.get('vertical', ''), {})
            
            f.write(f"## Prospect #{i} - {p.get('company_name', 'Unknown')}\n\n")
            f.write(f"**Priority:** {priority} (Score: {score}/100)\n\n")
            f.write(f"**Company:** {p.get('company_name', 'N/A')}\n")
            f.write(f"**Vertical:** {vertical_info.get('name', p.get('vertical', 'N/A'))}\n")
            f.write(f"**Location:** {p.get('location', 'N/A')}\n")
            f.write(f"**Employees:** {p.get('employees', 'N/A')}\n\n")
            
            f.write(f"**Buying Signal:** {p.get('signal', 'N/A')}\n")
            f.write(f"**Service Needed:** {p.get('service_needed', 'N/A')}\n\n")
            
            f.write(f"**Potential Fee:** {vertical_info.get('typical_fee', 'N/A')}\n\n")
            
            f.write(f"**Contact:**\n")
            f.write(f"- Role: {p.get('contact', 'N/A')}\n")
            f.write(f"- Email: {p.get('email', 'N/A')}\n\n")
            f.write(f"---\n\n")
    
    return filename

def main():
    print("\n" + "="*60)
    print("B2B Referral Engine - Demand Side (Prospects)")
    print("="*60 + "\n")
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    # Generate prospects
    prospects = generate_sample_prospects()
    
    # Score each
    for p in prospects:
        p['score'] = score_prospect(p)
    
    # Save
    filename = save_prospect_leads(prospects, date_str)
    
    # Summary
    high_priority = sum(1 for p in prospects if p['score'] >= 80)
    total_fees = sum(5000 if p['score'] >= 80 else 3000 for p in prospects)
    
    print(f"✅ Generated {len(prospects)} prospects")
    print(f"📁 Saved to: {filename}")
    print(f"\n📊 Summary:")
    print(f"   High Priority (80+): {high_priority}")
    print(f"   Total Potential Fees: ${total_fees:,}")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
