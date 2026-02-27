#!/usr/bin/env python3
"""
B2B Referral Fee Engine - Supply Side (Service Providers)
Identifies 3-4 daily providers willing to pay referral fees
"""

import json
from datetime import datetime
import os

# Service provider categories
PROVIDER_CATEGORIES = {
    "accounting": {
        "name": "Accounting Firms",
        "services": ["Audit", "Tax", "Bookkeeping", "Fractional CFO"],
        "fee_range": "$5,000-$7,500 (10-15% first year)",
        "sources": ["AICPA directory", "State CPA societies", "LinkedIn"]
    },
    "legal": {
        "name": "Law Firms",
        "services": ["Corporate", "M&A", "Compliance", "IP"],
        "fee_range": "$5,000-$7,500 (10-15% first year)",
        "sources": ["Martindale", "State bar associations", "Chambers"]
    },
    "consulting": {
        "name": "Consulting Firms",
        "services": ["Strategy", "Operations", "Technology", "HR"],
        "fee_range": "$3,000-$5,000 (10% of contract)",
        "sources": ["LinkedIn", "Industry associations", "Consulting directories"]
    },
    "saas_partners": {
        "name": "SaaS Partner Programs",
        "services": ["Implementation", "Integration", "Consulting"],
        "fee_range": "$5,000 or 10-20% ACV",
        "sources": ["Partner program pages", "SaaS company websites"]
    },
    "contractors": {
        "name": "Construction Contractors",
        "services": ["General", "Electrical", "Plumbing", "HVAC"],
        "fee_range": "$3,000 per referral",
        "sources": ["License databases", "Trade associations", "BBB"]
    },
    "brokers": {
        "name": "Commercial Real Estate Brokers",
        "services": ["Office", "Industrial", "Retail"],
        "fee_range": "25% of commission ($3K-$10K)",
        "sources": ["CCIM", "SIOR", "Local brokerages"]
    }
}

def generate_sample_providers():
    """Generate sample service providers for testing"""
    sample_providers = [
        {
            "firm_name": "CFO Partners LLC",
            "category": "accounting",
            "services": ["Fractional CFO", "Audit", "Tax Planning"],
            "location": "San Francisco, CA",
            "size": "15 professionals",
            "fee_offer": "15% of first year billings",
            "referral_history": "Active referral program - 10+ partners",
            "contact": "John Mitchell, Partner",
            "email": "partners@cfopartners.com",
            "willingness_score": 95
        },
        {
            "firm_name": "TechLaw Group",
            "category": "legal",
            "services": ["Corporate", "M&A", "Venture Capital"],
            "location": "New York, NY",
            "size": "50 attorneys",
            "fee_offer": "10% of first year fees",
            "referral_history": "Established referral network",
            "contact": "Sarah Chen, Business Development",
            "email": "bd@techlawgroup.com",
            "willingness_score": 90
        },
        {
            "firm_name": "Growth Consulting Partners",
            "category": "consulting",
            "services": ["Strategy", "Operations", "Digital Transformation"],
            "location": "Chicago, IL",
            "size": "30 consultants",
            "fee_offer": "10% of engagement value",
            "referral_history": "New referral program - seeking partners",
            "contact": "Mike Torres, Director",
            "email": "partnerships@growthcp.com",
            "willingness_score": 92
        },
        {
            "firm_name": "Snowflake Implementation Co",
            "category": "saas_partners",
            "services": ["Snowflake", "Data Engineering", "Analytics"],
            "location": "Austin, TX",
            "size": "25 engineers",
            "fee_offer": "$5,000 per closed deal",
            "referral_history": "Official Snowflake partner - referral fees standard",
            "contact": "Lisa Park, Partner Manager",
            "email": "partners@snowflakeimpl.com",
            "willingness_score": 98
        },
        {
            "firm_name": "Elite Electrical Services",
            "category": "contractors",
            "services": ["Commercial Electrical", "Industrial"],
            "location": "Denver, CO",
            "size": "75 electricians",
            "fee_offer": "$3,000 per commercial project",
            "referral_history": "Pays referral fees to architects and PMs",
            "contact": "Dave Wilson, Owner",
            "email": "dave@eliteelectrical.com",
            "willingness_score": 85
        },
        {
            "firm_name": "Commercial Space Advisors",
            "category": "brokers",
            "services": ["Office Leasing", "Industrial", "Tenant Rep"],
            "location": "Los Angeles, CA",
            "size": "20 brokers",
            "fee_offer": "25% of commission",
            "referral_history": "Actively seeks referral partners",
            "contact": "Jennifer Adams, Managing Director",
            "email": "jadams@commspaceadvisors.com",
            "willingness_score": 93
        },
        {
            "firm_name": "DataStack Solutions",
            "category": "saas_partners",
            "services": ["Databricks", "AWS", "Data Platform"],
            "location": "Seattle, WA",
            "size": "40 engineers",
            "fee_offer": "15% of first year contract",
            "referral_history": "Multiple referral partners",
            "contact": "Alex Kim, VP Business Dev",
            "email": "alex@datastack.io",
            "willingness_score": 91
        },
        {
            "firm_name": "Regional Audit Partners",
            "category": "accounting",
            "services": ["Audit", "Review", "Compilation"],
            "location": "Boston, MA",
            "size": "8 CPAs",
            "fee_offer": "12% of first year fees",
            "referral_history": "Growing firm - seeking referrals",
            "contact": "Mark Stevens, CPA",
            "email": "mstevens@regionalaudit.com",
            "willingness_score": 88
        }
    ]
    return sample_providers

def score_provider(provider):
    """Score provider based on referral willingness and fee structure"""
    score = 0
    
    # Willingness score from data (0-40)
    score += min(provider.get("willingness_score", 0) * 0.4, 40)
    
    # Fee structure (0-30)
    fee = provider.get("fee_offer", "").lower()
    if "15%" in fee or "$5,000" in fee:
        score += 30
    elif "10%" in fee or "25%" in fee:
        score += 25
    else:
        score += 20
    
    # Referral history (0-20)
    history = provider.get("referral_history", "").lower()
    if "active" in history or "established" in history:
        score += 20
    elif "seeking" in history or "new" in history:
        score += 15
    else:
        score += 10
    
    # Category potential (0-10)
    category = provider.get("category", "")
    if category in ["accounting", "legal", "saas_partners"]:
        score += 10
    else:
        score += 5
    
    return min(score, 100)

def save_provider_leads(providers, date_str):
    """Save providers to daily file"""
    workspace = "/Users/cubiczan/.openclaw/workspace/referral-engine/providers"
    os.makedirs(workspace, exist_ok=True)
    
    filename = f"{workspace}/daily-providers-{date_str}.md"
    
    with open(filename, 'w') as f:
        f.write(f"# B2B Referral Engine - Daily Service Providers\n\n")
        f.write(f"**Date:** {date_str}\n")
        f.write(f"**Total Providers:** {len(providers)}\n")
        f.write(f"**Target:** 3-4 daily\n\n")
        f.write("---\n\n")
        
        # Sort by score
        providers_sorted = sorted(providers, key=lambda x: x.get('score', 0), reverse=True)
        
        for i, p in enumerate(providers_sorted, 1):
            score = p.get('score', 0)
            priority = "🔴 HIGH" if score >= 80 else "🟡 MEDIUM" if score >= 60 else "🟢 LOW"
            category_info = PROVIDER_CATEGORIES.get(p.get('category', ''), {})
            
            f.write(f"## Provider #{i} - {p.get('firm_name', 'Unknown')}\n\n")
            f.write(f"**Priority:** {priority} (Score: {score}/100)\n\n")
            f.write(f"**Firm:** {p.get('firm_name', 'N/A')}\n")
            f.write(f"**Category:** {category_info.get('name', p.get('category', 'N/A'))}\n")
            f.write(f"**Location:** {p.get('location', 'N/A')}\n")
            f.write(f"**Size:** {p.get('size', 'N/A')}\n\n")
            
            f.write(f"**Services:** {', '.join(p.get('services', []))}\n\n")
            
            f.write(f"**Fee Offer:** {p.get('fee_offer', 'N/A')}\n")
            f.write(f"**Referral History:** {p.get('referral_history', 'N/A')}\n\n")
            
            f.write(f"**Contact:**\n")
            f.write(f"- Name: {p.get('contact', 'N/A')}\n")
            f.write(f"- Email: {p.get('email', 'N/A')}\n\n")
            f.write(f"---\n\n")
    
    return filename

def main():
    print("\n" + "="*60)
    print("B2B Referral Engine - Supply Side (Service Providers)")
    print("="*60 + "\n")
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    # Generate providers
    providers = generate_sample_providers()
    
    # Score each
    for p in providers:
        p['score'] = score_provider(p)
    
    # Save
    filename = save_provider_leads(providers, date_str)
    
    # Summary
    high_priority = sum(1 for p in providers if p['score'] >= 80)
    ready_for_outreach = sum(1 for p in providers if 'active' in p.get('referral_history', '').lower() or 'established' in p.get('referral_history', '').lower())
    
    print(f"✅ Generated {len(providers)} service providers")
    print(f"📁 Saved to: {filename}")
    print(f"\n📊 Summary:")
    print(f"   High Priority (80+): {high_priority}")
    print(f"   Ready for Outreach: {ready_for_outreach}")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
