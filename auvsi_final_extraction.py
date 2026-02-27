#!/usr/bin/env python3
"""
Final AUVSI contact extraction - Process all remaining companies
"""

import json
import csv
import time
from hunter_io_config2 import hunter_client2

# All remaining companies to process
COMPANIES_TO_PROCESS = [
    {"name": "AeroVironment", "domain": "avinc.com"},
    {"name": "Kratos Defense", "domain": "kratosdefense.com"},
    {"name": "Beta Technologies", "domain": "beta.team"},
    {"name": "Wisk Aero", "domain": "wisk.aero"},
    {"name": "Volocopter", "domain": "volocopter.com"},
    {"name": "Wing", "domain": "wing.com"},
    {"name": "Matternet", "domain": "matternet.com"},
    {"name": "Parrot", "domain": "parrot.com"},
    {"name": "Auterion", "domain": "auterion.com"},
    {"name": "Liquid Robotics", "domain": "liquid-robotics.com"},
    {"name": "Ocean Infinity", "domain": "oceaninfinity.com"},
    {"name": "Teledyne Marine", "domain": "teledyne.com"},
    {"name": "FLIR Systems", "domain": "flir.com"},
    {"name": "Trimble", "domain": "trimble.com"},
    {"name": "Garmin", "domain": "garmin.com"},
    {"name": "CrowdAI", "domain": "crowdai.com"},
    {"name": "NVIDIA", "domain": "nvidia.com"},
    {"name": "D-Fend Solutions", "domain": "dfendsolutions.com"},
    {"name": "DroneShield", "domain": "droneshield.com"},
    {"name": "Echodyne", "domain": "echodyne.com"},
    {"name": "General Atomics", "domain": "ga-asi.com"},
    {"name": "Lilium", "domain": "lilium.com"},
    {"name": "Vertical Aerospace", "domain": "vertical-aerospace.com"},
    {"name": "Flytrex", "domain": "flytrex.com"},
    {"name": "DJI", "domain": "dji.com"},
    {"name": "PrecisionHawk", "domain": "precisionhawk.com"},
    {"name": "SeaRobotics Corporation", "domain": "searobotics.com"},
    {"name": "Kongsberg Maritime", "domain": "kongsberg.com"},
    {"name": "Honeywell", "domain": "honeywell.com"},
    {"name": "SICK Sensor Intelligence", "domain": "sick.com"},
    {"name": "Intel", "domain": "intel.com"},
    {"name": "AMD", "domain": "amd.com"},
    {"name": "Saronic Technologies", "domain": "saronictech.com"},
    {"name": "PteroDynamics", "domain": "pterodynamics.com"},
]

print("Starting final AUVSI contact extraction...")
print(f"Processing {len(COMPANIES_TO_PROCESS)} companies")
print("=" * 60)

results = []
executive_emails = []

for i, company in enumerate(COMPANIES_TO_PROCESS):
    print(f"\n{i+1}/{len(COMPANIES_TO_PROCESS)}: {company['name']} ({company['domain']})")
    
    try:
        # Try domain search
        result = hunter_client2.domain_search(company['domain'], limit=5)
        
        if result.get('data') and result['data'].get('emails'):
            emails = result['data']['emails']
            contacts = []
            
            for email in emails:
                contact = {
                    "email": email.get('value'),
                    "first_name": email.get('first_name'),
                    "last_name": email.get('last_name'),
                    "position": email.get('position'),
                    "confidence": email.get('confidence'),
                    "sources": len(email.get('sources', []))
                }
                contacts.append(contact)
                
                # Check if executive
                position = contact['position'].lower() if contact['position'] else ''
                if ('ceo' in position or 'cto' in position or 'director' in position or 
                    'vp' in position or 'president' in position or 'head' in position):
                    executive_emails.append(contact['email'])
            
            company_result = {
                "company": company['name'],
                "domain": company['domain'],
                "status": "success",
                "contacts_found": len(emails),
                "contacts": contacts
            }
            
            print(f"  ✓ Found {len(emails)} contacts")
            
            # Show executives if any
            exec_contacts = [c for c in contacts if c.get('position')]
            if exec_contacts:
                for exec_contact in exec_contacts[:2]:
                    print(f"    - {exec_contact['first_name']} {exec_contact['last_name']} ({exec_contact['position']})")
        
        else:
            company_result = {
                "company": company['name'],
                "domain": company['domain'],
                "status": "no_results",
                "contacts_found": 0,
                "contacts": []
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
    
    # Rate limiting
    time.sleep(1)
    
    # Save progress every 5 companies
    if (i + 1) % 5 == 0:
        progress_file = f"auvsi_final_progress_{i+1}.json"
        with open(progress_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"  [Progress saved to {progress_file}]")

print("\n" + "=" * 60)
print("Saving final results...")

# Save final JSON
with open('auvsi_contacts_final.json', 'w') as f:
    json.dump(results, f, indent=2)
print("✓ Final JSON saved to auvsi_contacts_final.json")

# Save CSV
with open('auvsi_contacts_final.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Company', 'Domain', 'Status', 'Contacts', 'Name', 'Email', 'Position', 'Confidence'])
    
    for result in results:
        if result['contacts']:
            for contact in result['contacts'][:3]:
                writer.writerow([
                    result['company'],
                    result['domain'],
                    result['status'],
                    result['contacts_found'],
                    f"{contact.get('first_name', '')} {contact.get('last_name', '')}".strip(),
                    contact.get('email', ''),
                    contact.get('position', ''),
                    contact.get('confidence', '')
                ])
        else:
            writer.writerow([result['company'], result['domain'], result['status'], result['contacts_found'], '', '', '', ''])

print("✓ Final CSV saved to auvsi_contacts_final.csv")

# Save executive emails
with open('auvsi_executive_emails_final.txt', 'w') as f:
    for email in executive_emails:
        f.write(f"{email}\n")

print(f"✓ Final executive emails saved to auvsi_executive_emails_final.txt ({len(executive_emails)} emails)")

# Combine with batch1
try:
    with open('auvsi_executive_emails_batch1.txt', 'r') as f:
        batch1_emails = [line.strip() for line in f if line.strip()]
    
    all_executive_emails = batch1_emails + executive_emails
    
    with open('auvsi_all_executive_emails_complete.txt', 'w') as f:
        for email in all_executive_emails:
            f.write(f"{email}\n")
    
    print(f"✓ Complete executive emails: {len(all_executive_emails)} total")
    
except Exception as e:
    print(f"⚠ Could not combine with batch1: {e}")

# Summary
successful = sum(1 for r in results if r['status'] == 'success')
total_contacts = sum(r['contacts_found'] for r in results)

print("\n" + "=" * 60)
print("FINAL EXTRACTION SUMMARY")
print(f"Companies processed: {len(results)}")
print(f"Successful searches: {successful}")
print(f"Total contacts found: {total_contacts}")
print(f"Executive emails extracted: {len(executive_emails)}")
print("=" * 60)

# Check remaining credits
account_info = hunter_client2.get_account_info()
if account_info.get('data'):
    credits = account_info['data']['requests']['credits']
    print(f"\nRemaining credits: {credits['available'] - credits['used']:.1f}")
    print(f"Used: {credits['used']:.1f}")
    print(f"Available: {credits['available']:.1f}")

print("\n✅ Final extraction complete!")