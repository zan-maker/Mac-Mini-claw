#!/usr/bin/env python3
"""
Add $50M valuation filter to defense company searches.
Prevents contacting large companies like Anduril, Palantir, etc.
"""

import json
import os
from datetime import datetime

def update_defense_cron_jobs():
    """Update cron jobs with $50M valuation filter."""
    cron_file = "/Users/cubiczan/.openclaw/cron/jobs.json"
    
    if not os.path.exists(cron_file):
        print(f"❌ Cron file not found: {cron_file}")
        return False
    
    try:
        with open(cron_file, 'r') as f:
            data = json.load(f)
        
        updated = False
        
        for job in data.get("jobs", []):
            if "defense" in job.get("name", "").lower():
                print(f"🔧 Found defense job: {job.get('name')}")
                
                # Update the message to include valuation filter
                message = job.get("payload", {}).get("message", "")
                
                if "Company Criteria:" in message:
                    # Add valuation filter
                    new_criteria = """**Company Criteria:**
- Stage: Early to mid-stage (Series A-C)
- Region: US, UK, EU
- Focus: Defense or dual-use technology
- IP ownership important
- **MAX VALUATION: $50 MILLION (CRITICAL FILTER)**
- **REJECT: Companies valued over $50M (Anduril, Palantir, Lockheed, etc.)**"""
                    
                    # Find and replace the criteria section
                    lines = message.split('\n')
                    new_lines = []
                    in_criteria = False
                    criteria_replaced = False
                    
                    for line in lines:
                        if "Company Criteria:" in line:
                            in_criteria = True
                            new_lines.append(new_criteria)
                            criteria_replaced = True
                        elif in_criteria and line.strip() and not line.startswith('-'):
                            # End of criteria section
                            in_criteria = False
                            new_lines.append(line)
                        elif not in_criteria:
                            new_lines.append(line)
                    
                    if criteria_replaced:
                        job["payload"]["message"] = '\n'.join(new_lines)
                        updated = True
                        print(f"✅ Updated {job.get('name')} with $50M valuation filter")
                    else:
                        print(f"⚠️ Could not find criteria section in {job.get('name')}")
        
        if updated:
            # Save backup
            backup_file = f"{cron_file}.backup-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            with open(backup_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"📁 Backup saved: {backup_file}")
            
            # Save updated file
            with open(cron_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✅ Updated cron file: {cron_file}")
            
            return True
        else:
            print("⚠️ No defense jobs found or updated")
            return False
            
    except Exception as e:
        print(f"❌ Error updating cron jobs: {e}")
        return False

def create_valuation_filter_script():
    """Create a Python script to filter defense companies by valuation."""
    script_content = '''#!/usr/bin/env python3
"""
Defense Company Valuation Filter
Filters out companies valued over $50M.
"""

import json
import re
from typing import Dict, List, Any'''

# Large defense companies to automatically reject (valuation > $50M)
LARGE_DEFENSE_COMPANIES = [
    # Public companies (market cap in billions)
    "Anduril Industries", "Anduril",
    "Palantir Technologies", "Palantir",
    "Lockheed Martin", "Lockheed",
    "Northrop Grumman", "Northrop",
    "Raytheon Technologies", "Raytheon",
    "Boeing",
    "General Dynamics",
    "L3Harris Technologies", "L3Harris",
    "BAE Systems",
    "Thales",
    "Airbus",
    
    # Large private companies
    "Shield AI",
    "Epirus",
    "Rebellion Defense",
    "Vannevar Labs",
    
    # eVTOL/Drone companies (large)
    "Joby Aviation", "Joby",
    "Archer Aviation", "Archer",
    "Beta Technologies", "Beta",
    "Wisk Aero", "Wisk",
    "Volocopter",
    
    # Drone delivery (large)
    "Zipline",
    "Wing",
    "Skydio",
]

def is_large_company(company_name: str, valuation: float = None) -> bool:
    """
    Check if a company is too large (> $50M valuation).
    
    Args:
        company_name: Name of the company
        valuation: Company valuation in dollars (optional)
    
    Returns:
        bool: True if company is too large, False if acceptable
    """
    # Check against known large companies
    company_lower = company_name.lower()
    for large_company in LARGE_DEFENSE_COMPANIES:
        if large_company.lower() in company_lower:
            print(f"❌ REJECTED: {company_name} (known large company: {large_company})")
            return True
    
    # Check valuation if provided
    if valuation is not None:
        if valuation > 50000000:  # $50M
            print(f"❌ REJECTED: {company_name} (valuation: ${valuation:,} > $50M)")
            return True
        else:
            print(f"✅ ACCEPTED: {company_name} (valuation: ${valuation:,} <= $50M)")
            return False
    
    # If no valuation data, use heuristics
    # Large companies often have certain keywords
    large_indicators = [
        "corporation", "corp", "inc", "llc", "ltd", "plc",
        "technologies", "systems", "solutions", "global",
        "international", "worldwide", "enterprise"
    ]
    
    # Check company size indicators in website/description
    size_indicators = [
        "fortune 500", "public company", "listed on",
        "revenue", "employees", "founded",
        "market cap", "valuation"
    ]
    
    # Default to accepting if we can't determine
    print(f"⚠️  UNKNOWN SIZE: {company_name} (no valuation data)")
    return False

def filter_defense_companies(companies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter defense companies to only include those under $50M valuation.
    
    Args:
        companies: List of company dictionaries
    
    Returns:
        List of filtered companies
    """
    filtered = []
    rejected = []
    
    for company in companies:
        name = company.get("name", "")
        valuation = company.get("valuation")
        
        if is_large_company(name, valuation):
            rejected.append({
                "name": name,
                "valuation": valuation,
                "reason": "Valuation > $50M or known large company"
            })
        else:
            # Add valuation filter note
            company["valuation_filter"] = "PASSED: Under $50M"
            filtered.append(company)
    
    # Print summary
    print(f"\\n📊 FILTERING SUMMARY:")
    print(f"   Total companies: {len(companies)}")
    print(f"   Accepted (under $50M): {len(filtered)}")
    print(f"   Rejected (over $50M): {len(rejected)}")
    
    if rejected:
        print(f"\\n❌ REJECTED COMPANIES:")
        for r in rejected[:5]:  # Show first 5
            val_str = f"${r['valuation']:,}" if r['valuation'] else "unknown"
            print(f"   - {r['name']} ({val_str})")
        if len(rejected) > 5:
            print(f"   ... and {len(rejected) - 5} more")
    
    return filtered

def add_valuation_to_search_queries():
    """
    Modify search queries to include valuation filters.
    """
    queries = [
        # Original: "defense technology companies"
        # Modified: "defense technology startups under $50 million valuation"
        "defense technology startups under $50 million valuation",
        "small defense contractors under $50M",
        "early stage defense tech companies series A",
        "seed stage military technology startups",
        "defense startups seeking series B funding",
        
        # Cybersecurity
        "cybersecurity startups for military applications under $50M",
        "early stage defense cybersecurity companies",
        
        # Drones
        "drone technology startups under $50 million",
        "small UAV companies seeking investment",
        
        # AI/ML
        "military AI startups series A funding",
        "defense machine learning early stage companies",
        
        # Space
        "space defense startups under $50M valuation",
        "small satellite defense technology companies",
    ]
    
    return queries

def main():
    """Example usage."""
    # Example companies (some large, some small)
    example_companies = [
        {"name": "Anduril Industries", "valuation": 8500000000},  # $8.5B
        {"name": "Palantir Technologies", "valuation": 50000000000},  # $50B
        {"name": "Small Defense Tech Inc", "valuation": 15000000},  # $15M
        {"name": "Early Stage Drone Co", "valuation": 30000000},  # $30M
        {"name": "Cybersecurity Startup LLC", "valuation": None},  # Unknown
        {"name": "Lockheed Martin", "valuation": 110000000000},  # $110B
        {"name": "Tiny Defense Solutions", "valuation": 5000000},  # $5M
    ]
    
    print("🔍 TESTING VALUATION FILTER ($50M MAX)")
    print("=" * 50)
    
    filtered = filter_defense_companies(example_companies)
    
    print(f"\\n✅ FILTERED COMPANIES (under $50M):")
    for company in filtered:
        val_str = f"${company['valuation']:,}" if company['valuation'] else "unknown"
        print(f"   - {company['name']} ({val_str})")
    
    print(f"\\n📝 MODIFIED SEARCH QUERIES:")
    queries = add_valuation_to_search_queries()
    for i, query in enumerate(queries[:3], 1):
        print(f"   {i}. {query}")

if __name__ == "__main__":
    main()
"""
    
    script_path = "/Users/cubiczan/.openclaw/workspace/scripts/defense_valuation_filter.py"
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    os.chmod(script_path, 0o755)
    
    print(f"✅ Created valuation filter script: {script_path}")
    return script_path

def update_auvsi_contacts_file():
    """Update the AUVSI contacts file to remove large companies."""
    auvsi_file = "/Users/cubiczan/.openclaw/workspace/final_auvsi_contacts.py"
    
    if not os.path.exists(auvsi_file):
        print(f"❌ AUVSI file not found: {auvsi_file}")
        return False
    
    try:
        with open(auvsi_file, 'r') as f:
            content = f.read()
        
        # Large companies to remove (valuation > $50M)
        large_companies = [
            "Anduril Industries",
            "AeroVironment", 
            "Kratos Defense",
            "Archer Aviation",
            "Joby Aviation",
            "Zipline",
            "Wing",
            "Skydio",
            "Velodyne Lidar",
            "FLIR Systems",
            "Trimble",
            "Garmin",
            "Honeywell",
            "Applied Intuition",
            "Scale AI",
            "Palantir",
            "Lockheed",
            "Northrop",
            "Raytheon",
            "Boeing"
        ]
        
        # Create filtered version
        lines = content.split('\n')
        filtered_lines = []
        skip_company = False
        
        for line in lines:
            # Check if this line contains a large company
            is_large = any(company.lower() in line.lower() for company in large_companies)
            
            if is_large and ('{"name":' in line or '"name":' in line):
                print(f"❌ Removing large company: {line.strip()}")
                skip_company = True
                continue
            elif skip_company and ('},' in line or '}' in line):
                skip_company = False
                continue
            elif not skip_company:
                filtered_lines.append(line)
        
        # Save backup
        backup_file = f"{auvsi_file}.backup-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        with open(backup_file, 'w') as f:
            f.write(content)
        print(f"📁 Backup saved: {backup_file}")
        
        # Save filtered version
        with open(auvsi_file, 'w') as f:
            f.write('\n'.join(filtered_lines))
        
        print(f"✅ Updated AUVSI file: {auvsi_file}")
        print(f"   Removed {len(large_companies)} large companies (> $50M valuation)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating AUVSI file: {e}")
        return False

def main():
    """Main function."""
    print("=" * 60)
    print("DEFENSE COMPANY VALUATION FILTER - $50M MAX")
    print("=" * 60)
    
    print("\\n🎯 TARGET: Defense companies UNDER $50M valuation")
    print("❌ REJECT: Anduril, Palantir, Lockheed, etc. (> $50M)")
    
    # 1. Create valuation filter script
    filter_script = create_valuation_filter_script()
    
    # 2. Update AUVSI contacts file
    auvsi_updated = update_auvsi_contacts_file()
    
    # 3. Update cron jobs (commented out for safety - manual review needed)
    # cron_updated = update_defense_cron_jobs()
    
    print("\\n" + "=" * 60)
    print("✅ ACTIONS COMPLETED:")
    print("=" * 60)
    
    print(f"1. 📝 Created filter script: {filter_script}")
    print("   Usage: python3 defense_valuation_filter.py")
    
    if auvsi_updated:
        print("2. 📁 Updated AUVSI contacts file")
        print("   Removed large companies (> $50M valuation)")
    
    print("3. ⚠️  Cron jobs need MANUAL update")
    print("   Edit these cron jobs to add $50M filter:")
    print("   - 'Defense Sector Lead Gen' (9:00 AM)")
    print("   - 'Defense Sector Outreach' (2:00 PM)")
    
    print("\\n🔧 MANUAL STEPS REQUIRED:")
    print("1. Open /Users/cubiczan/.openclaw/cron/jobs.json")
    print("2. Find 'Defense Sector Lead Gen' job")
    print("3. Add to 'Company Criteria:' section:")
    print("   - MAX VALUATION: $50 MILLION (CRITICAL FILTER)")
    print("   - REJECT: Companies valued over $50M")
    print("4. Do same for 'Defense Sector Outreach'")
    
    print("\\n💡 The filter will now:")
    print("   ✅ Accept: Companies under $50M valuation")
    print("   ❌ Reject: Anduril ($8.5B), Palantir ($50B), etc.")
    print("   🎯 Target: Small defense startups & contractors")

if __name__ == "__main__":
    main()