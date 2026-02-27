#!/usr/bin/env python3
"""
Batch 1: Extract contacts for 10 key AUVSI companies
"""

import json
import csv
import time
from hunter_io_config import hunter_client

# First batch of 10 key companies
BATCH_1_COMPANIES = [
    {"name": "Ouster", "domain": "ouster.io"},
    {"name": "Shield AI", "domain": "shield.ai"},
    {"name": "Archer Aviation", "domain": "archer.com"},
    {"name": "Joby Aviation", "domain": "jobyaviation.com"},
    {"name": "Zipline", "domain": "flyzipline.com"},
    {"name": "Sea Machines Robotics", "domain": "sea-machines.com"},
    {"name": "Applied Intuition", "domain": "appliedintuition.com"},
    {"name": "Scale AI", "domain": "scale.com"},
    {"name": "Velodyne Lidar", "domain": "velodynelidar.com"},
    {"name": "Anduril Industries", "domain": "anduril.com"},
]

print("Batch 1: Extracting contacts for 10 key AUVSI companies")
print("=" * 60)

results = []
executive_emails = []

for i, company in enumerate(BATCH_1_COMPANIES):
    print(f"{i+1}/10: {company['name']} ({company['domain']})")
    
    try:
        result = hunter_client.domain_search(company['domain'], limit=8)
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
                    "department": email.get('department'),
                    "confidence": email.get('confidence'),
                    "sources": len(email.get('sources', [])),
                    "verification": email.get('verification', {}).get('status')
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
with open('auvsi_contacts_batch1.json', 'w') as f:
    json.dump(results, f, indent=2)
print("✓ JSON saved to auvsi_contacts_batch1.json")

# Save CSV
with open('auvsi_contacts_batch1.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Company', 'Domain', 'Status', 'Contacts', 'Name', 'Email', 'Position', 'Confidence'])
    
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
                    contact.get('confidence', '')
                ])
        else:
            writer.writerow([result['company'], result['domain'], result['status'], result['contacts_found'], '', '', '', ''])

print("✓ CSV saved to auvsi_contacts_batch1.csv")

# Save executive emails
with open('auvsi_executive_emails_batch1.txt', 'w') as f:
    for email in executive_emails:
        f.write(f"{email}\n")

print(f"✓ Executive emails saved to auvsi_executive_emails_batch1.txt ({len(executive_emails)} emails)")

# Summary
successful = sum(1 for r in results if r['status'] == 'success')
total_contacts = sum(r['contacts_found'] for r in results)

print("\n" + "=" * 60)
print("BATCH 1 SUMMARY")
print(f"Companies processed: {len(results)}")
print(f"Successful searches: {successful}")
print(f"Total contacts found: {total_contacts}")
print(f"Executive emails: {len(executive_emails)}")
print("=" * 60)

# Check remaining credits
account_info = hunter_client.get_account_info()
if account_info.get('data'):
    credits = account_info['data']['requests']['credits']
    print(f"\nRemaining credits: {credits['available'] - credits['used']:.1f}")
    print(f"Used: {credits['used']:.1f}")
    print(f"Available: {credits['available']:.1f}")