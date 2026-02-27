#!/usr/bin/env python3
"""
Complete AUVSI contact extraction - Process ALL remaining companies using all 3 API keys
"""

import json
import csv
import time
from hunter_io_config import hunter_client
from hunter_io_config2 import hunter_client2
from hunter_io_config3 import hunter_client3

# All remaining AUVSI companies (40+ companies)
ALL_REMAINING_COMPANIES = [
    # Defense & Aerospace Giants (try with fresh key)
    {"name": "Boeing", "domain": "boeing.com"},
    {"name": "Lockheed Martin", "domain": "lockheedmartin.com"},
    {"name": "Northrop Grumman", "domain": "northropgrumman.com"},
    {"name": "Raytheon", "domain": "raytheon.com"},
    {"name": "General Dynamics", "domain": "gdmissionsystems.com"},
    
    # eVTOL & Urban Air Mobility
    {"name": "Lilium", "domain": "lilium.com"},
    {"name": "Vertical Aerospace", "domain": "vertical-aerospace.com"},
    {"name": "Eve Air Mobility", "domain": "eveairmobility.com"},
    {"name": "Overair", "domain": "overair.com"},
    {"name": "Supernal", "domain": "supernal.aero"},
    
    # Drone Delivery & Services
    {"name": "Flytrex", "domain": "flytrex.com"},
    {"name": "DJI", "domain": "dji.com"},
    {"name": "PrecisionHawk", "domain": "precisionhawk.com"},
    {"name": "DroneDeploy", "domain": "dronedeploy.com"},
    {"name": "Skyward", "domain": "skyward.io"},
    {"name": "AirMap", "domain": "airmap.com"},
    {"name": "Kittyhawk", "domain": "kittyhawk.io"},
    
    # Maritime & Underwater
    {"name": "SeaRobotics Corporation", "domain": "searobotics.com"},
    {"name": "Kongsberg Maritime", "domain": "kongsberg.com"},
    {"name": "Saab Seaeye", "domain": "saabseaeye.com"},
    {"name": "Hydroid", "domain": "hydroid.com"},
    {"name": "iXblue", "domain": "ixblue.com"},
    {"name": "ECA Group", "domain": "ecagroup.com"},
    
    # Sensors & Components
    {"name": "SICK Sensor Intelligence", "domain": "sick.com"},
    {"name": "ifm electronic", "domain": "ifm.com"},
    {"name": "Banner Engineering", "domain": "bannerengineering.com"},
    {"name": "Keyence", "domain": "keyence.com"},
    {"name": "Cognex", "domain": "cognex.com"},
    {"name": "Omron", "domain": "omron.com"},
    
    # AI & Software Giants
    {"name": "Intel", "domain": "intel.com"},
    {"name": "AMD", "domain": "amd.com"},
    {"name": "Qualcomm", "domain": "qualcomm.com"},
    {"name": "Microsoft", "domain": "microsoft.com"},
    {"name": "Google", "domain": "google.com"},
    {"name": "Amazon", "domain": "amazon.com"},
    
    # Defense Startups & Additional
    {"name": "Saronic Technologies", "domain": "saronictech.com"},
    {"name": "PteroDynamics", "domain": "pterodynamics.com"},
    {"name": "Collins Aerospace", "domain": "collinsaerospace.com"},
    {"name": "L3Harris Technologies", "domain": "l3harris.com"},
    {"name": "Textron Systems", "domain": "textronsystems.com"},
    {"name": "BAE Systems", "domain": "baesystems.com"},
    {"name": "Thales", "domain": "thalesgroup.com"},
    {"name": "Safran", "domain": "safran-group.com"},
    {"name": "Leonardo", "domain": "leonardo.com"},
    {"name": "Airbus", "domain": "airbus.com"},
]

# API key rotation strategy
API_CLIENTS = [
    {"client": hunter_client3, "name": "Key3", "remaining": 50},  # Fresh key first
    {"client": hunter_client, "name": "Key1", "remaining": 14},   # Then Key1
    {"client": hunter_client2, "name": "Key2", "remaining": 5},   # Finally Key2
]

current_api_index = 0

def get_next_api_client():
    """Get next available API client with credits"""
    global current_api_index
    
    for i in range(len(API_CLIENTS)):
        idx = (current_api_index + i) % len(API_CLIENTS)
        api_info = API_CLIENTS[idx]
        
        # Check remaining credits
        try:
            account_info = api_info["client"].get_account_info()
            if account_info.get('data'):
                credits = account_info['data']['requests']['credits']
                remaining = credits['available'] - credits['used']
                if remaining > 0:
                    current_api_index = idx
                    return api_info["client"], api_info["name"], remaining
        except:
            continue
    
    return None, "No API", 0

print("=" * 70)
print("COMPLETE AUVSI CONTACT EXTRACTION")
print(f"Processing ALL remaining companies: {len(ALL_REMAINING_COMPANIES)}")
print("Using 3 API keys with intelligent rotation")
print("=" * 70)

results = []
executive_emails = []
all_contacts = []
api_usage = {"Key1": 0, "Key2": 0, "Key3": 0}

for i, company in enumerate(ALL_REMAINING_COMPANIES):
    print(f"\n{i+1}/{len(ALL_REMAINING_COMPANIES)}: {company['name']} ({company['domain']})")
    
    # Get API client
    client, api_name, remaining = get_next_api_client()
    if not client:
        print("  ⚠ All API keys exhausted!")
        break
    
    print(f"  Using API: {api_name} (Remaining: {remaining:.1f})")
    
    try:
        # Try domain search
        result = client.domain_search(company['domain'], limit=6)
        api_usage[api_name] += 1
        
        if result.get('data') and result['data'].get('emails'):
            emails = result['data']['emails']
            contacts = []
            
            for email in emails:
                contact = {
                    "company": company['name'],
                    "domain": company['domain'],
                    "email": email.get('value'),
                    "first_name": email.get('first_name'),
                    "last_name": email.get('last_name'),
                    "position": email.get('position'),
                    "department": email.get('department'),
                    "confidence": email.get('confidence'),
                    "sources": len(email.get('sources', [])),
                    "verification": email.get('verification', {}).get('status'),
                    "api_used": api_name
                }
                contacts.append(contact)
                all_contacts.append(contact)
                
                # Collect executive emails
                position = contact['position'].lower() if contact['position'] else ''
                if ('ceo' in position or 'cto' in position or 'director' in position or 
                    'vp' in position or 'president' in position or 'head' in position or
                    'chief' in position):
                    executive_emails.append(contact['email'])
            
            company_result = {
                "company": company['name'],
                "domain": company['domain'],
                "status": "success",
                "contacts_found": len(emails),
                "contacts": contacts,
                "api_used": api_name,
                "organization": result['data'].get('organization')
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
                "contacts": [],
                "api_used": api_name,
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
            "api_used": api_name,
            "error": str(e)
        }
        print(f"  ✗ Error: {e}")
    
    results.append(company_result)
    
    # Rate limiting
    time.sleep(1)
    
    # Save progress every 10 companies
    if (i + 1) % 10 == 0:
        progress_file = f"auvsi_complete_progress_{i+1}.json"
        with open(progress_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"  [Progress saved to {progress_file}]")

print("\n" + "=" * 70)
print("Saving complete results...")

# Save complete JSON
with open('auvsi_contacts_complete.json', 'w') as f:
    json.dump(results, f, indent=2)
print("✓ Complete data saved to auvsi_contacts_complete.json")

# Save all contacts combined
with open('auvsi_all_contacts_complete.json', 'w') as f:
    json.dump(all_contacts, f, indent=2)
print("✓ All contacts combined saved to auvsi_all_contacts_complete.json")

# Save CSV summary
with open('auvsi_contacts_complete.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Company', 'Domain', 'Status', 'Contacts Found', 'API Used',
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
                    result['api_used'],
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
                result['api_used'],
                '', '', '', '', '', '', ''
            ])

print("✓ CSV summary saved to auvsi_contacts_complete.csv")

# Save executive emails
with open('auvsi_executive_emails_complete.txt', 'w') as f:
    for email in executive_emails:
        f.write(f"{email}\n")

print(f"✓ Executive emails saved to auvsi_executive_emails_complete.txt ({len(executive_emails)} emails)")

# Combine with previous executive emails
try:
    with open('auvsi_all_executive_emails_final.txt', 'r') as f:
        previous_emails = [line.strip() for line in f if line.strip()]
    
    all_executive_emails_combined = list(set(previous_emails + executive_emails))  # Remove duplicates
    
    with open('auvsi_all_executive_emails_master.txt', 'w') as f:
        for email in all_executive_emails_combined:
            f.write(f"{email}\n")
    
    print(f"✓ Master executive emails: {len(all_executive_emails_combined)} total (combined)")
    
except Exception as e:
    print(f"⚠ Could not combine with previous emails: {e}")

# Summary
successful = sum(1 for r in results if r['status'] == 'success')
total_contacts = sum(r['contacts_found'] for r in results)

print("\n" + "=" * 70)
print("COMPLETE EXTRACTION SUMMARY")
print(f"Companies processed: {len(results)}")
print(f"Successful searches: {successful}")
print(f"Total contacts found: {total_contacts}")
print(f"Executive emails extracted: {len(executive_emails)}")
print(f"API Usage: Key1={api_usage['Key1']}, Key2={api_usage['Key2']}, Key3={api_usage['Key3']}")
print("=" * 70)

# Check remaining credits for all APIs
print("\nRemaining credits:")
for api_info in API_CLIENTS:
    try:
        account_info = api_info["client"].get_account_info()
        if account_info.get('data'):
            credits = account_info['data']['requests']['credits']
            remaining = credits['available'] - credits['used']
            print(f"  {api_info['name']}: {remaining:.1f} remaining")
    except:
        print(f"  {api_info['name']}: Could not check")

print("\n✅ Complete extraction finished!")