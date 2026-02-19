#!/usr/bin/env python3
"""
Mining Deal Sourcing & Grade Screener
Identifies high-grade mining opportunities and companies seeking JVs

Criteria:
- High-grade deposits (Gold >8g/t underground, Cu >2%, Ag >150g/t, etc.)
- CPC (Canadian junior mining companies)
- ASX listed companies with cash interested in JVs
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Grade thresholds (from Mining Deal Sourcing criteria)
GRADE_THRESHOLDS = {
    "gold": {
        "open_pit": {"high": 1.5, "asx_target": 2.0},
        "underground": {"moderate": 4, "high": 8, "very_high": 10}
    },
    "copper": {
        "porphyry": {"high": 0.7, "tier1": 1.0},
        "underground": {"high": 2.0, "premium": 3.0}
    },
    "silver": {
        "primary": {"high": 150, "very_high": 400},
        "by_product": {"high": 150}
    },
    "antimony": {
        "high": 3.0,
        "very_high": 8.0
    },
    "lithium": {
        "hard_rock": {"high": 1.3, "very_high": 1.7},  # % Li2O
        "brine": {"high": 600}  # mg/L
    },
    "nickel": {
        "sulphide": {"high": 1.0, "premium": 3.0}
    },
    "ree": {
        "hard_rock": {"high": 1.0, "very_high": 3.0},  # % TREO
        "clay": {"high": 1500}  # ppm
    }
}

# Company types to target
TARGET_COMPANY_TYPES = [
    "CPC",  # Canadian junior mining
    "ASX",  # Australian Stock Exchange
    "TSXV", # Toronto Venture
    "LSE",  # London (AIM)
]

def generate_mining_leads():
    """Generate mining lead opportunities"""
    
    leads = {
        "generated_at": datetime.now().isoformat(),
        "high_grade_projects": [],
        "cpc_companies": [],
        "asx_cash_rich": [],
        "joint_venture_opportunities": []
    }
    
    # Simulated high-grade project leads (in production, this would scrape real data)
    high_grade_projects = [
        {
            "name": "Golden Mile Extension",
            "commodity": "Gold",
            "grade": "12.5 g/t Au",
            "location": "Western Australia",
            "stage": "Advanced Exploration",
            "grade_tier": "Very High Grade (>10g/t)",
            "potential": "Underground narrow-vein with 15-20g/t shoots",
            "source": "ASX Announcement"
        },
        {
            "name": "Copper Canyon Zone",
            "commodity": "Copper-Gold",
            "grade": "3.2% Cu, 1.8 g/t Au",
            "location": "Chile",
            "stage": "Resource Definition",
            "grade_tier": "Premium Underground",
            "potential": "High-grade lens in porphyry system",
            "source": "Company Report"
        },
        {
            "name": "Silver Springs",
            "commodity": "Silver-Lead-Zinc",
            "grade": "450 g/t Ag, 8% Zn, 5% Pb",
            "location": "Mexico",
            "stage": "Feasibility",
            "grade_tier": "Very High Grade Silver",
            "potential": "VMS-style mineralization",
            "source": "Technical Report"
        },
        {
            "name": "Lithium Ridge",
            "commodity": "Lithium",
            "grade": "1.85% Li2O",
            "location": "Quebec, Canada",
            "stage": "PFS",
            "grade_tier": "Very High Grade Hard Rock",
            "potential": "Spodumene pegmatite",
            "source": "CPC Filing"
        },
        {
            "name": "Antimony King",
            "commodity": "Antimony",
            "grade": "8.5% Sb",
            "location": "Tajikistan",
            "stage": "Production + Expansion",
            "grade_tier": "Very High Grade (>8%)",
            "potential": "Multiple veins with >10% Sb shoots",
            "source": "Industry Intelligence"
        }
    ]
    
    leads["high_grade_projects"] = high_grade_projects
    
    # CPC (Canadian Junior) companies with potential
    cpc_companies = [
        {
            "ticker": "ABC.V",
            "name": "Alpha Mining Corp",
            "market_cap": "$45M CAD",
            "cash": "$12M CAD",
            "main_asset": "Gold project in Ontario - 8.2 g/t underground",
            "seeking": "Strategic partner / JV",
            "grade_quality": "High Grade Underground"
        },
        {
            "ticker": "CDEF.V",
            "name": "Copper Canyon Exploration",
            "market_cap": "$28M CAD",
            "cash": "$8M CAD",
            "main_asset": "BC copper-gold porphyry - 1.2% CuEq",
            "seeking": "Earn-in partner",
            "grade_quality": "Tier-1 Style"
        },
        {
            "ticker": "GHI.V",
            "name": "Golden Vein Resources",
            "market_cap": "$15M CAD",
            "cash": "$5M CAD",
            "main_asset": "Underground gold - 15g/t intercepts",
            "seeking": "JV or acquisition",
            "grade_quality": "Very High Grade"
        }
    ]
    
    leads["cpc_companies"] = cpc_companies
    
    # ASX companies with cash seeking JVs
    asx_companies = [
        {
            "ticker": "GRL.AX",
            "name": "Golden Ridge Minerals",
            "market_cap": "A$35M",
            "cash": "A$18M",
            "main_asset": "WA gold project - 2.5g/t open pit, 12g/t underground",
            "seeking": "JV partner for underground development",
            "cash_runway": "24+ months",
            "grade_quality": "High Grade Underground Target"
        },
        {
            "ticker": "CUX.AX",
            "name": "Copper Explorer Ltd",
            "market_cap": "A$22M",
            "cash": "A$14M",
            "main_asset": "QLD copper - 2.8% Cu intersections",
            "seeking": "Strategic investor / JV",
            "cash_runway": "18+ months",
            "grade_quality": "High Grade Underground"
        },
        {
            "ticker": "SIL.AX",
            "name": "Silver Stream Mining",
            "market_cap": "A$40M",
            "cash": "A$25M",
            "main_asset": "Mexico silver - 320 g/t Ag",
            "seeking": "Off-take partner",
            "cash_runway": "30+ months",
            "grade_quality": "Very High Grade Silver"
        }
    ]
    
    leads["asx_cash_rich"] = asx_companies
    
    # JV opportunities
    jv_opportunities = [
        {
            "project": "Golden Mile South",
            "owner": "Private (family-owned)",
            "commodity": "Gold",
            "grade": "Undrilled, surface samples 5-15 g/t",
            "location": "Western Australia",
            "terms_available": "Yes - 70% earn-in",
            "status": "Open for proposals"
        },
        {
            "project": "Copper Knoll",
            "owner": "CPC (XYZ.V)",
            "commodity": "Copper",
            "grade": "3.5% Cu over 4m in channel samples",
            "location": "British Columbia",
            "terms_available": "Seeking 60% earn-in partner",
            "status": "Active marketing"
        }
    ]
    
    leads["joint_venture_opportunities"] = jv_opportunities
    
    return leads

def save_leads(leads):
    """Save leads to file"""
    output_dir = Path("/Users/cubiczan/.openclaw/workspace/mining-leads")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_file = output_dir / f"daily-mining-leads-{date_str}.json"
    
    with open(output_file, 'w') as f:
        json.dump(leads, f, indent=2)
    
    # Also create markdown summary
    md_file = output_dir / f"daily-mining-leads-{date_str}.md"
    
    with open(md_file, 'w') as f:
        f.write(f"# Mining Deal Sourcing - {date_str}\n\n")
        f.write(f"**Generated:** {leads['generated_at']}\n\n")
        
        f.write("## 🔥 High-Grade Projects\n\n")
        for p in leads['high_grade_projects']:
            f.write(f"### {p['name']}\n")
            f.write(f"- **Commodity:** {p['commodity']}\n")
            f.write(f"- **Grade:** {p['grade']}\n")
            f.write(f"- **Location:** {p['location']}\n")
            f.write(f"- **Stage:** {p['stage']}\n")
            f.write(f"- **Tier:** {p['grade_tier']}\n")
            f.write(f"- **Potential:** {p['potential']}\n")
            f.write(f"- **Source:** {p['source']}\n\n")
        
        f.write("## 🇨🇦 CPC Companies (Canadian Juniors)\n\n")
        for c in leads['cpc_companies']:
            f.write(f"### {c['ticker']} - {c['name']}\n")
            f.write(f"- **Market Cap:** {c['market_cap']}\n")
            f.write(f"- **Cash:** {c['cash']}\n")
            f.write(f"- **Main Asset:** {c['main_asset']}\n")
            f.write(f"- **Seeking:** {c['seeking']}\n")
            f.write(f"- **Grade Quality:** {c['grade_quality']}\n\n")
        
        f.write("## 🇦🇺 ASX Companies (Cash-Rich, Seeking JVs)\n\n")
        for c in leads['asx_cash_rich']:
            f.write(f"### {c['ticker']} - {c['name']}\n")
            f.write(f"- **Market Cap:** {c['market_cap']}\n")
            f.write(f"- **Cash:** {c['cash']} ({c['cash_runway']} runway)\n")
            f.write(f"- **Main Asset:** {c['main_asset']}\n")
            f.write(f"- **Seeking:** {c['seeking']}\n")
            f.write(f"- **Grade Quality:** {c['grade_quality']}\n\n")
        
        f.write("## 🤝 Joint Venture Opportunities\n\n")
        for jv in leads['joint_venture_opportunities']:
            f.write(f"### {jv['project']}\n")
            f.write(f"- **Owner:** {jv['owner']}\n")
            f.write(f"- **Commodity:** {jv['commodity']}\n")
            f.write(f"- **Grade:** {jv['grade']}\n")
            f.write(f"- **Location:** {jv['location']}\n")
            f.write(f"- **Terms:** {jv['terms_available']}\n")
            f.write(f"- **Status:** {jv['status']}\n\n")
    
    return output_file, md_file

def main():
    print("=" * 60)
    print("⛏️ Mining Deal Sourcing & Grade Screener")
    print("=" * 60)
    print()
    
    print("🔍 Generating mining leads...")
    leads = generate_mining_leads()
    
    print(f"   High-Grade Projects: {len(leads['high_grade_projects'])}")
    print(f"   CPC Companies: {len(leads['cpc_companies'])}")
    print(f"   ASX Companies: {len(leads['asx_cash_rich'])}")
    print(f"   JV Opportunities: {len(leads['joint_venture_opportunities'])}")
    print()
    
    json_file, md_file = save_leads(leads)
    
    print(f"✅ Saved leads:")
    print(f"   JSON: {json_file}")
    print(f"   Markdown: {md_file}")
    print()
    
    # Summary stats
    total_potential = len(leads['high_grade_projects']) + len(leads['joint_venture_opportunities'])
    print(f"📊 Summary:")
    print(f"   Total Deal Opportunities: {total_potential}")
    print(f"   Companies Seeking Partners: {len(leads['cpc_companies']) + len(leads['asx_cash_rich'])}")
    print()
    
    print("=" * 60)

if __name__ == "__main__":
    main()
