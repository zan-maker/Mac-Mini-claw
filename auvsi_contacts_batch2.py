#!/usr/bin/env python3
"""
Batch 2: Extract contacts for remaining AUVSI companies using fresh API key
"""

import json
import csv
import time
from hunter_io_config2 import hunter_client2

# Remaining AUVSI companies (40+ companies)
REMAINING_COMPANIES = [
    # Defense & Aerospace (continued)
    {"name": "AeroVironment", "domain": "avinc.com"},
    {"name": "Kratos Defense", "domain": "kratosdefense.com"},
    {"name": "General Atomics", "domain": "ga-asi.com"},
    
    # eVTOL & Urban Air Mobility (continued)
    {"name": "Beta Technologies", "domain": "beta.team"},
    {"name": "Wisk Aero", "domain": "wisk.aero"},
    {"name": "Volocopter", "domain": "volocopter.com"},
    {"name": "Lilium", "domain": "lilium.com"},
    {"name": "Vertical Aerospace", "domain": "vertical-aerospace.com"},
    {"name": "Eve Air Mobility", "domain": "eveairmobility.com"},
    
    # Drone Delivery & Services (continued)
    {"name": "Wing", "domain": "wing.com"},
    {"name": "Matternet", "domain": "matternet.com"},
    {"name": "Flytrex", "domain": "flytrex.com"},
    {"name": "Parrot", "domain": "parrot.com"},
    {"name": "DJI", "domain": "dji.com"},
    {"name": "Auterion", "domain": "auterion.com"},
    {"name": "PrecisionHawk", "domain": "precisionhawk.com"},
    {"name": "DroneDeploy", "domain": "dronedeploy.com"},
    {"name": "Skyward", "domain": "skyward.io"},
    
    # Maritime & Underwater (continued)
    {"name": "Liquid Robotics", "domain": "liquid-robotics.com"},
    {"name": "Ocean Infinity", "domain": "oceaninfinity.com"},
    {"name": "SeaRobotics Corporation", "domain": "searobotics.com"},
    {"name": "Teledyne Marine", "domain": "teledyne.com"},
    {"name": "Kongsberg Maritime", "domain": "kongsberg.com"},
    {"name": "Saab Seaeye", "domain": "saabseaeye.com"},
    {"name": "Hydroid", "domain": "hydroid.com"},
    
    # Sensors & Components (continued)
    {"name": "FLIR Systems", "domain": "flir.com"},
    {"name": "Trimble", "domain": "trimble.com"},
    {"name": "Garmin", "domain": "garmin.com"},
    {"name": "Honeywell", "domain": "honeywell.com"},
    {"name": "SICK Sensor Intelligence", "domain": "sick.com"},
    {"name": "ifm electronic", "domain": "ifm.com"},
    {"name": "Banner Engineering", "domain": "bannerengineering.com"},
    
    # AI & Software (continued)
    {"name": "CrowdAI", "domain": "crowdai.com"},
    {"name": "NVIDIA", "domain": "nvidia.com"},
    {"name": "Intel", "domain": "intel.com"},
    {"name": "AMD", "domain": "amd.com"},
    {"name": "Qualcomm", "domain": "qualcomm.com"},
    
    # Defense Startups (continued)
    {"name": "Saronic Technologies", "domain": "saronictech.com"},
    {"name": "D-Fend Solutions", "domain": "dfendsolutions.com"},
    {"name": "DroneShield", "domain": "droneshield.com"},
    {"name": "Echodyne", "domain": "echodyne.com"},
    {"name": "PteroDynamics", "domain": "pterodynamics.com"},
    {"name": "Shield AI", "domain": "shield.ai"},  # Already in batch1 but worth checking again
    
    # Additional from AUVSI lists
    {"name": "Collins Aerospace", "domain": "collinsaerospace.com"},
    {"name": "L3Harris Technologies", "domain": "l3harris.com"},
    {"name": "Textron Systems", "domain": "textronsystems.com"},
    {"name": "BAE Systems", "domain": "baesystems.com"},
    {"name": "Thales", "domain": "thalesgroup.com"},
    {"name": "Safran", "domain": "safran-group.com"},
    {"name": "Leonardo", "domain": "leonardo.com"},
    {"name": "Airbus", "domain": "airbus.com"},
    {"name": "Boeing", "domain": "boeing.com"},  # Might be restricted but worth trying
    {"name": "Lockheed Martin", "domain": "lockheedmartin.com"},  # Might be restricted
]

print("=" * 70)
print("BATCH 2: Extracting contacts for remaining AUVSI companies")
print(f"Total companies: {len(REMAINING_COMPANIES)}")
print("Using fresh API key with 50 available searches")
print("=" * 70)

# Check account info
account_info = hunter_client2.get_account_info()
if account_info.get('data'):
    credits = account_info['data']['requests']['credits']
    print(f"Available credits: {credits['available']}")
    print(f"Used credits: {credits['used']}")
    remaining = int(credits['available'] - credits['used'])
    print(f"Remaining searches: {remaining}")
    
    # Limit based on available credits
    max_companies = min(len(REMAINING_COMPANIES), remaining)
    companies_to_process = REMAINING_COMPANIES[:max_companies]
    print(f"Will process {len(companies_to_process)} companies")
else:
    print("Warning: Could not check account limits")
    companies_to_process = REMAINING_COMPANIES[:25]  # Safe default

print("\n" + "=" * 70)
print("Starting extraction...\n")

results = []
executive_emails = []
all_contacts = []

for i, company in enumerate(companies_to_process):
    print(f"{i+1}/{len(companies_to_process)}: {company['name']} ({company['domain']})")
    
    try:
        result = hunter_client2.domain_search(company['domain'], limit=8)
        time.sleep(1)  # Rate limiting
        
        if result.get('data') and result['data'].get('emails'):
            emails = result['data']['emails']
            contacts = []
            
            for email in emails:
                contact = {
                    "email": email.get('value'),
                    "first_name": email.get('first_name'),
                    "last_name": email.get('last_name'),
                    "position": email.get('position'),
                    "department": email.get('department'),
                    "confidence": email.get('confidence'),
                    "sources": len(email.get('sources', [])),
                    "verification": email.get('verification', {}).get('status')
                }
                contacts.append(contact)
                all_contacts.append({
                    "company": company['name'],
                    "domain": company['domain'],
                    **contact
                })
                
                # Collect executive emails
                position = contact['position'].lower() if contact['position'] else ''
                if ('ceo' in position or 'cto' in position or 'director' in position or 
                    'vp' in position or 'president' in position or 'head' in position):
                    executive_emails.append(contact['email'])
            
            company_result = {
                "company": company['name'],
                "domain": company['domain'],
                "status": "success",
                "contacts_found": len(emails),
                "contacts": contacts,
                "organization": result['data'].get('organization'),
                "pattern": result['data'].get('pattern')
            }
            
            print(f"  ✓ Found {len(emails)} contacts")
            if contacts:
                # Show top executives
                execs = [c for c in contacts if c.get('position') and 
                        ('ceo' in c['position'].lower() or 'cto' in c['position'].lower())]
                for exec_contact in execs[:2]:
                    print(f"    - {exec_contact['first_name']} {exec_contact['last_name']} ({exec_contact['position']})")
        
        else:
            company_result = {
                "company": company['name'],
                "domain": company['domain'],
                "status": "no_results",
                "contacts_found": 0,
                "contacts": [],
                "error": result.get('errors', ['No emails found'])[0] if result.get('errors') else 'No emails found'
            }
            print(f"  ✗ No contacts found")
            
    except Exception as e:
        company_result = {
            "company": company['name'],
            "domain": company['domain'],
            "status": "error",
            "contacts_found": 0,
            "contacts": [],
            "error": str(e)
        }
        print(f"  ✗ Error: {e}")
    
    results.append(company_result)
    
    # Save progress every 5 companies
    if (i + 1) % 5 == 0:
        progress_file = f"auvsi_batch2_progress_{i+1}.json"
        with open(progress_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"  [Progress saved to {progress_file}]")
    
    print()

print("=" * 70)
print("Saving results...")

# Save complete JSON
with open('auvsi_contacts_batch2.json', 'w') as f:
    json.dump(results, f, indent=2)
print("✓ Complete data saved to auvsi_contacts_batch2.json")

# Save all contacts combined
with open('auvsi_all_contacts_combined.json', 'w') as f:
    json.dump(all_contacts, f, indent=2)
print("✓ All contacts combined saved to auvsi_all_contacts_combined.json")

# Save CSV summary
with open('auvsi_contacts_batch2.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Company', 'Domain', 'Status', 'Contacts Found',
        'Contact Name', 'Email', 'Position', 'Department',
        'Confidence', 'Sources', 'Verification'
    ])
    
    for result in results:
        if result['contacts']:
            for contact in result['contacts'][:3]:  # Top 3 per company
                writer.writerow([
                    result['company'],
                    result['domain'],
                    result['status'],
                    result['contacts_found'],
                    f"{contact.get('first_name', '')} {contact.get('last_name', '')}".strip(),
                    contact.get('email', ''),
                    contact.get('position', ''),
                    contact.get('department', ''),
                    contact.get('confidence', ''),
                    contact.get('sources', ''),
                    contact.get('verification', '')
                ])
        else:
            writer.writerow([
                result['company'],
                result['domain'],
                result['status'],
                result['contacts_found'],
                '', '', '', '', '', '', ''
            ])

print("✓ CSV summary saved to auvsi_contacts_batch2.csv")

# Save executive emails
with open('auvsi_executive_emails_batch2.txt', 'w') as f:
    for email in executive_emails:
        f.write(f"{email}\n")

print(f"✓ Executive emails saved to auvsi_executive_emails_batch2.txt ({len(executive_emails)} emails)")

# Combine with batch1 executive emails
try:
    with open('auvsi_executive_emails_batch1.txt', 'r') as f:
        batch1_emails = [line.strip() for line in f if line.strip()]
    
    all_executive_emails = batch1_emails + executive_emails
    with open('auvsi_all_executive_emails.txt', 'w') as f:
        for email in all_executive_emails:
            f.write(f"{email}\n")
    
    print(f"✓ All executive emails combined: {len(all_executive_emails)} total")
except:
    print("⚠ Could not combine with batch1 emails")

# Summary
successful = sum(1 for r in results if r['status'] == 'success')
total_contacts = sum(r['contacts_found'] for r in results)

print("\n" + "=" * 70)
print("BATCH 2 SUMMARY")
print(f"Companies processed: {len(results)}")
print(f"Successful searches: {successful}")
print(f"Total contacts found: {total_contacts}")
print(f"Executive emails extracted: {len(executive_emails)}")
print("=" * 70)

# Check remaining credits
account_info = hunter_client2.get_account_info()
if account_info.get('data'):
    credits = account_info['data']['requests']['credits']
    print(f"\nRemaining credits: {credits['available'] - credits['used']:.1f}")
    print(f"Used: {credits['used']:.1f}")
    print(f"Available: {credits['available']:.1f}")

print("\n✅ Batch 2 extraction complete!")