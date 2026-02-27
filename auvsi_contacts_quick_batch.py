#!/usr/bin/env python3
"""
Quick batch: Extract contacts for 20 key remaining AUVSI companies
"""

import json
import csv
import time
from hunter_io_config2 import hunter_client2

# 20 key remaining companies
QUICK_BATCH = [
    # Defense & Aerospace
    {"name": "AeroVironment", "domain": "avinc.com"},
    {"name": "Kratos Defense", "domain": "kratosdefense.com"},
    
    # eVTOL & Urban Air Mobility
    {"name": "Beta Technologies", "domain": "beta.team"},
    {"name": "Wisk Aero", "domain": "wisk.aero"},
    {"name": "Volocopter", "domain": "volocopter.com"},
    
    # Drone Delivery
    {"name": "Wing", "domain": "wing.com"},
    {"name": "Matternet", "domain": "matternet.com"},
    {"name": "Parrot", "domain": "parrot.com"},
    {"name": "Auterion", "domain": "auterion.com"},
    
    # Maritime
    {"name": "Liquid Robotics", "domain": "liquid-robotics.com"},
    {"name": "Ocean Infinity", "domain": "oceaninfinity.com"},
    {"name": "Teledyne Marine", "domain": "teledyne.com"},
    
    # Sensors
    {"name": "FLIR Systems", "domain": "flir.com"},
    {"name": "Trimble", "domain": "trimble.com"},
    {"name": "Garmin", "domain": "garmin.com"},
    
    # AI & Software
    {"name": "CrowdAI", "domain": "crowdai.com"},
    {"name": "NVIDIA", "domain": "nvidia.com"},
    
    # Defense Startups
    {"name": "D-Fend Solutions", "domain": "dfendsolutions.com"},
    {"name": "DroneShield", "domain": "droneshield.com"},
    {"name": "Echodyne", "domain": "echodyne.com"},
]

print("Quick Batch: Extracting contacts for 20 key AUVSI companies")
print("=" * 60)

results = []
executive_emails = []

for i, company in enumerate(QUICK_BATCH):
    print(f"{i+1}/20: {company['name']} ({company['domain']})")
    
    try:
        result = hunter_client2.domain_search(company['domain'], limit=6)
        time.sleep(1)
        
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
                
                # Collect executive emails
                position = contact['position'].lower() if contact['position'] else ''
                if ('ceo' in position or 'cto' in position or 'director' in position or 
                    'vp' in position or 'president' in position):
                    executive_emails.append(contact['email'])
            
            company_result = {
                "company": company['name'],
                "domain": company['domain'],
                "status": "success",
                "contacts_found": len(emails),
                "contacts": contacts
            }
            
            print(f"  ✓ Found {len(emails)} contacts")
            if contacts:
                # Show executives
                execs = [c for c in contacts if c.get('position')]
                for exec_contact in execs[:2]:
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
    print()

print("=" * 60)
print("Saving results...")

# Save JSON
with open('auvsi_contacts_quick_batch.json', 'w') as f:
    json.dump(results, f, indent=2)
print("✓ JSON saved to auvsi_contacts_quick_batch.json")

# Save CSV
with open('auvsi_contacts_quick_batch.csv', 'w', newline='') as f:
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

print("✓ CSV saved to auvsi_contacts_quick_batch.csv")

# Save executive emails
with open('auvsi_executive_emails_quick_batch.txt', 'w') as f:
    for email in executive_emails:
        f.write(f"{email}\n")

print(f"✓ Executive emails saved to auvsi_executive_emails_quick_batch.txt ({len(executive_emails)} emails)")

# Combine all executive emails
try:
    # Load batch1 emails
    with open('auvsi_executive_emails_batch1.txt', 'r') as f:
        batch1_emails = [line.strip() for line in f if line.strip()]
    
    # Combine
    all_executive_emails = batch1_emails + executive_emails
    
    # Save combined
    with open('auvsi_all_executive_emails_combined.txt', 'w') as f:
        for email in all_executive_emails:
            f.write(f"{email}\n")
    
    print(f"✓ Combined executive emails: {len(all_executive_emails)} total")
    
except Exception as e:
    print(f"⚠ Could not combine emails: {e}")

# Summary
successful = sum(1 for r in results if r['status'] == 'success')
total_contacts = sum(r['contacts_found'] for r in results)

print("\n" + "=" * 60)
print("QUICK BATCH SUMMARY")
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

print("\n✅ Quick batch extraction complete!")