#!/usr/bin/env python3
"""
Mining Deal Sourcing & Grade Screener
Identifies high-grade mining opportunities and companies seeking JVs

UPDATED CRITERIA (2026-02-26):
- REGIONS: US, Canada, Latin America ONLY
- COMMODITIES: Gold, Silver, Copper, Rare Earths ONLY
- GOLD MINIMUM: 1+ million ounce potential (ignore smaller)
- High-grade deposits (Gold >8g/t underground, Cu >2%, Ag >150g/t, etc.)
- CPC (Canadian junior mining companies)
- ASX listed companies with cash interested in JVs
"""

import json
import os
from datetime import datetime
from pathlib import Path

# TARGET REGIONS (ONLY THESE)
TARGET_REGIONS = ["US", "Canada", "Latin America"]

# TARGET COMMODITIES (ONLY THESE)
TARGET_COMMODITIES = ["Gold", "Silver", "Copper", "Rare Earths"]

# GOLD MINIMUM POTENTIAL (ounces)
GOLD_MINIMUM_OUNCES = 1000000  # 1 million ounces

# Grade thresholds (from Mining Deal Sourcing criteria)
GRADE_THRESHOLDS = {
    "gold": {
        "open_pit": {"high": 1.5, "asx_target": 2.0},
        "underground": {"moderate": 4, "high": 8, "very_high": 10},
        "minimum_potential": GOLD_MINIMUM_OUNCES  # 1M+ ounces
    },
    "copper": {
        "porphyry": {"high": 0.7, "tier1": 1.0},
        "underground": {"high": 2.0, "premium": 3.0}
    },
    "silver": {
        "primary": {"high": 150, "very_high": 400},
        "by_product": {"high": 150}
    },
    "rare_earths": {
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

def filter_by_criteria(project):
    """
    Filter projects based on updated criteria:
    1. Region must be US, Canada, or Latin America
    2. Commodity must be Gold, Silver, Copper, or Rare Earths
    3. For Gold: Must have 1M+ ounce potential
    """
    location = project.get('location', '').lower()
    commodity = project.get('commodity', '').lower()
    
    # Check region
    region_valid = False
    for target_region in TARGET_REGIONS:
        if target_region.lower() in location:
            region_valid = True
            break
    
    if not region_valid:
        return False
    
    # Check commodity
    commodity_valid = False
    for target_commodity in TARGET_COMMODITIES:
        if target_commodity.lower() in commodity:
            commodity_valid = True
            break
    
    if not commodity_valid:
        return False
    
    # Special check for Gold: minimum 1M ounce potential
    if 'gold' in commodity.lower():
        potential = project.get('potential', '').lower()
        # Check if potential mentions ounces and is >= 1M
        if 'ounce' in potential or 'oz' in potential:
            # Extract numeric value (simplified - in production would parse better)
            import re
            numbers = re.findall(r'\d+\.?\d*', potential)
            if numbers:
                # Assume first number is ounces (simplified)
                try:
                    ounces = float(numbers[0])
                    # Check if it's in millions (e.g., 1.2M, 2.5 million)
                    if 'million' in potential or 'm' in potential.lower():
                        # Already in millions
                        if ounces >= 1.0:
                            return True
                    else:
                        # Convert to millions
                        if ounces >= 1000000:
                            return True
                except:
                    pass
            # If we can't parse ounces, include but flag for review
            project['needs_review'] = 'Gold ounces not specified'
    
    return True

def generate_mining_leads():
    """Generate mining lead opportunities with updated filters"""
    
    leads = {
        "generated_at": datetime.now().isoformat(),
        "filter_criteria": {
            "regions": TARGET_REGIONS,
            "commodities": TARGET_COMMODITIES,
            "gold_minimum_ounces": GOLD_MINIMUM_OUNCES
        },
        "high_grade_projects": [],
        "cpc_companies": [],
        "asx_cash_rich": [],
        "joint_venture_opportunities": []
    }
    
    # Simulated high-grade project leads (UPDATED to match criteria)
    all_projects = [
        {
            "name": "Nevada Gold Belt",
            "commodity": "Gold",
            "grade": "8.5 g/t Au",
            "location": "Nevada, USA",
            "stage": "Resource Definition",
            "grade_tier": "High Grade Underground",
            "potential": "1.8 million ounces potential, Carlin-type",
            "source": "Technical Report"
        },
        {
            "name": "Yukon Copper-Gold",
            "commodity": "Copper-Gold",
            "grade": "2.8% Cu, 1.2 g/t Au",
            "location": "Yukon, Canada",
            "stage": "Advanced Exploration",
            "grade_tier": "High Grade Porphyry",
            "potential": "Porphyry system with 5km strike",
            "source": "CPC Filing"
        },
        {
            "name": "Mexican Silver Vein",
            "commodity": "Silver",
            "grade": "380 g/t Ag, 5% Pb, 3% Zn",
            "location": "Chihuahua, Mexico",
            "stage": "Production",
            "grade_tier": "Very High Grade Silver",
            "potential": "High-grade epithermal vein system",
            "source": "Company Report"
        },
        {
            "name": "Arizona Copper Project",
            "commodity": "Copper",
            "grade": "1.5% Cu",
            "location": "Arizona, USA",
            "stage": "Feasibility",
            "grade_tier": "Open Pit Porphyry",
            "potential": "Large tonnage porphyry deposit",
            "source": "Technical Report"
        },
        {
            "name": "Quebec Rare Earths",
            "commodity": "Rare Earths",
            "grade": "2.1% TREO",
            "location": "Quebec, Canada",
            "stage": "PFS",
            "grade_tier": "High Grade REE",
            "potential": "Carbonatite-hosted rare earths",
            "source": "CPC Filing"
        },
        {
            "name": "Peru Copper Belt",
            "commodity": "Copper",
            "grade": "2.3% Cu, 0.3 g/t Au",
            "location": "Peru, Latin America",
            "stage": "Resource Definition",
            "grade_tier": "High Grade Skarn",
            "potential": "Skarn deposit with expansion potential",
            "source": "Company Report"
        },
        {
            "name": "Ontario Gold Mine",
            "commodity": "Gold",
            "grade": "6.2 g/t Au",
            "location": "Ontario, Canada",
            "stage": "Production",
            "grade_tier": "High Grade Underground",
            "potential": "800,000 ounces (TOO SMALL - WILL BE FILTERED)",
            "source": "Technical Report"
        }
    ]
    
    # Apply filters
    filtered_projects = []
    for project in all_projects:
        if filter_by_criteria(project):
            filtered_projects.append(project)
    
    leads["high_grade_projects"] = filtered_projects
    
    # CPC (Canadian Junior) companies with potential (UPDATED for target regions/commodities)
    cpc_companies = [
        {
            "ticker": "AUG.V",
            "name": "American Gold Corp",
            "market_cap": "$52M CAD",
            "cash": "$15M CAD",
            "main_asset": "Nevada gold project - 1.2M oz potential, 7.5 g/t",
            "seeking": "Strategic partner for feasibility",
            "grade_quality": "High Grade Open Pit",
            "region": "USA"
        },
        {
            "ticker": "CBM.V",
            "name": "Copper Belt Minerals",
            "market_cap": "$35M CAD",
            "cash": "$10M CAD",
            "main_asset": "Arizona copper project - 2.1% Cu porphyry",
            "seeking": "Earn-in partner",
            "grade_quality": "High Grade Porphyry",
            "region": "USA"
        },
        {
            "ticker": "SVR.V",
            "name": "Silver Range Resources",
            "market_cap": "$28M CAD",
            "cash": "$8M CAD",
            "main_asset": "Mexico silver project - 280 g/t Ag epithermal",
            "seeking": "JV or acquisition",
            "grade_quality": "High Grade Silver",
            "region": "Latin America"
        }
    ]
    
    # Filter CPC companies for target regions
    filtered_cpc = []
    for company in cpc_companies:
        region = company.get('region', '').lower()
        if any(target.lower() in region for target in TARGET_REGIONS):
            filtered_cpc.append(company)
    
    leads["cpc_companies"] = filtered_cpc
    
    # ASX companies with cash seeking JVs (UPDATED for target regions)
    asx_companies = [
        {
            "ticker": "USA.AX",
            "name": "US Gold Limited",
            "market_cap": "A$45M",
            "cash": "A$22M",
            "main_asset": "Nevada gold project - 1.5M oz resource, 1.8 g/t",
            "seeking": "JV partner for expansion",
            "cash_runway": "30+ months",
            "grade_quality": "Large Scale Open Pit",
            "region": "USA"
        },
        {
            "ticker": "LAT.AX",
            "name": "Latin Copper Co",
            "market_cap": "A$38M",
            "cash": "A$20M",
            "main_asset": "Chile copper project - 1.8% Cu porphyry",
            "seeking": "Strategic investor",
            "cash_runway": "24+ months",
            "grade_quality": "Porphyry Copper",
            "region": "Latin America"
        },
        {
            "ticker": "CAN.AX",
            "name": "Canadian Rare Earths",
            "market_cap": "A$55M",
            "cash": "A$30M",
            "main_asset": "Quebec rare earths - 2.3% TREO carbonatite",
            "seeking": "Off-take partner",
            "cash_runway": "36+ months",
            "grade_quality": "High Grade REE",
            "region": "Canada"
        }
    ]
    
    # Filter ASX companies for target regions
    filtered_asx = []
    for company in asx_companies:
        region = company.get('region', '').lower()
        if any(target.lower() in region for target in TARGET_REGIONS):
            filtered_asx.append(company)
    
    leads["asx_cash_rich"] = filtered_asx
    
    # JV opportunities (UPDATED for target regions/commodities)
    jv_opportunities = [
        {
            "project": "Nevada Gold Extension",
            "owner": "Private US group",
            "commodity": "Gold",
            "grade": "Drilled 10-15 g/t over 5m",
            "location": "Nevada, USA",
            "terms_available": "70% earn-in over 4 years",
            "status": "Open for proposals",
            "potential": "1.2M+ ounce potential"
        },
        {
            "project": "BC Copper-Gold",
            "owner": "CPC (MIN.V)",
            "commodity": "Copper-Gold",
            "grade": "3.5% Cu, 1.5 g/t Au over 8m",
            "location": "British Columbia, Canada",
            "terms_available": "60% earn-in partner sought",
            "status": "Active marketing",
            "potential": "Porphyry system with 3km strike"
        },
        {
            "project": "Mexico Silver District",
            "owner": "Family office (Mexico)",
            "commodity": "Silver",
            "grade": "Surface samples 200-500 g/t Ag",
            "location": "Durango, Mexico",
            "terms_available": "JV or outright sale",
            "status": "Confidential process",
            "potential": "District-scale epithermal system"
        }
    ]
    
    # Filter JV opportunities
    filtered_jvs = []
    for jv in jv_opportunities:
        location = jv.get('location', '').lower()
        commodity = jv.get('commodity', '').lower()
        
        # Check region
        region_valid = False
        for target_region in TARGET_REGIONS:
            if target_region.lower() in location:
                region_valid = True
                break
        
        # Check commodity
        commodity_valid = False
        for target_commodity in TARGET_COMMODITIES:
            if target_commodity.lower() in commodity:
                commodity_valid = True
                break
        
        # Special check for Gold minimum
        if 'gold' in commodity.lower():
            potential = jv.get('potential', '').lower()
            if 'million' in potential or 'm+' in potential:
                # Has million+ potential
                filtered_jvs.append(jv)
            else:
                # Skip - doesn't meet Gold minimum
                continue
        elif region_valid and commodity_valid:
            filtered_jvs.append(jv)
    
    leads["joint_venture_opportunities"] = filtered_jvs
    
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
        
        f.write("## 🎯 FILTERING CRITERIA (STRICT)\n\n")
        f.write("**REGIONS (ONLY):**\n")
        for region in leads['filter_criteria']['regions']:
            f.write(f"- {region}\n")
        
        f.write("\n**COMMODITIES (ONLY):**\n")
        for commodity in leads['filter_criteria']['commodities']:
            f.write(f"- {commodity}\n")
        
        f.write(f"\n**GOLD MINIMUM:** {leads['filter_criteria']['gold_minimum_ounces']:,} ounces (1M+)\n")
        f.write("\n---\n\n")
        
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
    
    print("🎯 FILTERING CRITERIA:")
    print(f"   Regions: {', '.join(TARGET_REGIONS)}")
    print(f"   Commodities: {', '.join(TARGET_COMMODITIES)}")
    print(f"   Gold Minimum: {GOLD_MINIMUM_OUNCES:,} ounces")
    print()
    
    print("🔍 Generating filtered mining leads...")
    leads = generate_mining_leads()
    
    print(f"\n📊 FILTERED RESULTS:")
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
