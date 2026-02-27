#!/usr/bin/env python3
"""
Simple test to extract contacts for a few AUVSI companies
"""

import json
import time
from hunter_io_config import hunter_client

# Test with just 5 companies
test_companies = [
    {"name": "Ouster", "domain": "ouster.io"},
    {"name": "Shield AI", "domain": "shield.ai"},
    {"name": "Archer Aviation", "domain": "archer.com"},
    {"name": "Sea Machines Robotics", "domain": "sea-machines.com"},
    {"name": "Applied Intuition", "domain": "appliedintuition.com"},
]

print("Testing Hunter.io API with 5 AUVSI companies...")
print("=" * 50)

contacts_found = []

for company in test_companies:
    print(f"\nSearching: {company['name']} ({company['domain']})")
    
    try:
        result = hunter_client.domain_search(company['domain'], limit=5)
        
        if result.get('data') and result['data'].get('emails'):
            emails = result['data']['emails']
            print(f"  Found {len(emails)} emails")
            
            # Show executives
            for email in emails:
                if email.get('position') and ('ceo' in email['position'].lower() or 'cto' in email['position'].lower()):
                    print(f"  ✓ {email.get('first_name', '')} {email.get('last_name', '')} - {email.get('position')}: {email.get('value')}")
                    contacts_found.append({
                        "company": company['name'],
                        "name": f"{email.get('first_name', '')} {email.get('last_name', '')}",
                        "position": email.get('position'),
                        "email": email.get('value'),
                        "confidence": email.get('confidence')
                    })
        else:
            print(f"  No emails found")
            
    except Exception as e:
        print(f"  Error: {e}")
    
    time.sleep(1)  # Rate limiting

print("\n" + "=" * 50)
print(f"Total executive contacts found: {len(contacts_found)}")

if contacts_found:
    print("\nExecutive Contacts Found:")
    for contact in contacts_found:
        print(f"• {contact['company']}: {contact['name']} ({contact['position']}) - {contact['email']}")
    
    # Save to file
    with open('auvsi_test_contacts.json', 'w') as f:
        json.dump(contacts_found, f, indent=2)
    print(f"\n✓ Contacts saved to auvsi_test_contacts.json")

# Check remaining credits
print("\n" + "=" * 50)
print("Checking account credits...")
account_info = hunter_client.get_account_info()
if account_info.get('data'):
    credits = account_info['data']['requests']['credits']
    print(f"Used: {credits['used']}")
    print(f"Available: {credits['available']}")
    print(f"Remaining: {credits['available'] - credits['used']}")