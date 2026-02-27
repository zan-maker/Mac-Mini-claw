#!/usr/bin/env python3
"""
Final AUVSI contact extraction - Comprehensive for smaller companies
"""

import json
import csv
import time
from hunter_io_config import hunter_client

# Comprehensive list of AUVSI smaller/medium member companies
AUVSI_COMPANIES = [
    # Unmanned Systems & Defense Tech
    {"name": "Ouster", "domain": "ouster.io"},
    {"name": "Shield AI", "domain": "shield.ai"},
    {"name": "Anduril Industries", "domain": "anduril.com"},
    {"name": "AeroVironment", "domain": "avinc.com"},
    {"name": "Kratos Defense", "domain": "kratosdefense.com"},
    
    # eVTOL & Urban Air Mobility
    {"name": "Archer Aviation", "domain": "archer.com"},
    {"name": "Joby Aviation", "domain": "jobyaviation.com"},
    {"name": "Beta Technologies", "domain": "beta.team"},
    {"name": "Wisk Aero", "domain": "wisk.aero"},
    {"name": "Volocopter", "domain": "volocopter.com"},
    
    # Drone Delivery & Services
    {"name": "Zipline", "domain": "flyzipline.com"},
    {"name": "Wing", "domain": "wing.com"},
    {"name": "Matternet", "domain": "matternet.com"},
    {"name": "Flytrex", "domain": "flytrex.com"},
    {"name": "Skydio", "domain": "skydio.com"},
    
    # Maritime & Underwater
    {"name": "Sea Machines Robotics", "domain": "sea-machines.com"},
    {"name": "Liquid Robotics", "domain": "liquid-robotics.com"},
    {"name": "Ocean Infinity", "domain": "oceaninfinity.com"},
    {"name": "SeaRobotics Corporation", "domain": "searobotics.com"},
    {"name": "Teledyne Marine", "domain": "teledyne.com"},
    
    # Sensors & Components
    {"name": "Velodyne Lidar", "domain": "velodynelidar.com"},
    {"name": "FLIR Systems", "domain": "flir.com"},
    {"name": "Trimble", "domain": "trimble.com"},
    {"name": "Garmin", "domain": "garmin.com"},
    {"name": "Honeywell", "domain": "honeywell.com"},
    
    # AI & Software
    {"name": "Applied Intuition", "domain": "appliedintuition.com"},
    {"name": "Scale AI", "domain": "scale.com"},
    {"name": "CrowdAI", "domain": "crowdai.com"},
    {"name": "NVIDIA", "domain": "nvidia.com"},
    {"name": "Intel", "domain": "intel.com"},
    
    # Defense Startups
    {"name": "Dark Wolf Solutions", "domain": "darkwolfsolutions.com"},
    {"name": "Saronic Technologies", "domain": "saronictech.com"},
    {"name": "D-Fend Solutions", "domain": "dfendsolutions.com"},
    {"name": "DroneShield", "domain": "droneshield.com"},
    {"name": "Echodyne", "domain": "echodyne.com"},
    
    # Additional from AUVSI lists
    {"name": "PteroDynamics", "domain": "pterodynamics.com"},
    {"name": "Parrot", "domain": "parrot.com"},
    {"name": "DJI", "domain": "dji.com"},
    {"name": "Auterion", "domain": "auterion.com"},
    {"name": "PrecisionHawk", "domain": "precisionhawk.com"},
]

def extract_company_contacts(company):
    """Extract contacts for a single company"""
    print(f"  Processing: {company['name']}")
    
    try:
        result = hunter_client.domain_search(company['domain'], limit=10)
        time.sleep(1)  # Rate limiting
        
        if result.get('data') and result['data'].get('emails'):
            emails = result['data']['emails']
            
            # Extract all contacts
            contacts = []
            for email in emails:
                contacts.append({
                    "email": email.get('value'),
                    "first_name": email.get('first_name'),
                    "last_name": email.get('last_name'),
                    "position": email.get('position'),
                    "department": email.get('department'),
                    "seniority": email.get('seniority'),
                    "confidence": email.get('confidence'),
                    "sources": len(email.get('sources', [])),
                    "verification": email.get('verification', {}).get('status')
                })
            
            return {
                "company": company['name'],
                "domain": company['domain'],
                "status": "success",
                "total_contacts": len(emails),
                "contacts": contacts,
                "organization": result['data'].get('organization'),
                "pattern": result['data'].get('pattern')
            }
        else:
            return {
                "company": company['name'],
                "domain": company['domain'],
                "status": "no_results",
                "total_contacts": 0,
                "contacts": [],
                "error": result.get('errors', ['No emails found'])[0] if result.get('errors') else 'No emails found'
            }
            
    except Exception as e:
        return {
            "company": company['name'],
            "domain": company['domain'],
            "status": "error",
            "total_contacts": 0,
            "contacts": [],
            "error": str(e)
        }

def main():
    """Main execution"""
    print("=" * 70)
    print("AUVSI MEMBER CONTACT EXTRACTION")
    print("Using Hunter.io API")
    print("=" * 70)
    
    # Check account limits
    account_info = hunter_client.get_account_info()
    if account_info.get('data'):
        credits = account_info['data']['requests']['credits']
        print(f"Available credits: {credits['available']}")
        print(f"Used credits: {credits['used']}")
        remaining = int(credits['available'] - credits['used'])
        print(f"Remaining searches: {remaining}")
        
        # Limit companies based on remaining credits
        max_companies = min(len(AUVSI_COMPANIES), remaining)
        companies_to_process = AUVSI_COMPANIES[:max_companies]
        print(f"Will process {len(companies_to_process)} companies")
    else:
        print("Warning: Could not check account limits")
        companies_to_process = AUVSI_COMPANIES[:20]  # Safe default
    
    print("\n" + "=" * 70)
    print("Starting contact extraction...\n")
    
    # Process companies
    results = []
    for i, company in enumerate(companies_to_process):
        print(f"{i+1}/{len(companies_to_process)}: {company['name']} ({company['domain']})")
        result = extract_company_contacts(company)
        results.append(result)
        
        # Show quick summary
        if result['status'] == 'success':
            print(f"    ✓ Found {result['total_contacts']} contacts")
            # Show executives if any
            executives = [c for c in result['contacts'] if c.get('position') and 
                         ('ceo' in c['position'].lower() or 'cto' in c['position'].lower() or 
                          'director' in c['position'].lower() or 'vp' in c['position'].lower())]
            if executives:
                for exec_contact in executives[:2]:
                    print(f"      - {exec_contact['first_name']} {exec_contact['last_name']} ({exec_contact['position']})")
        else:
            print(f"    ✗ {result['status']}: {result.get('error', '')}")
        
        print()
    
    print("=" * 70)
    print("Saving results...")
    
    # Save complete JSON
    with open('auvsi_member_contacts_complete.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("✓ Complete data saved to auvsi_member_contacts_complete.json")
    
    # Save CSV summary
    with open('auvsi_member_contacts_summary.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Company', 'Domain', 'Status', 'Total Contacts',
            'Contact Name', 'Email', 'Position', 'Department',
            'Seniority', 'Confidence', 'Sources', 'Verification'
        ])
        
        for result in results:
            company = result['company']
            domain = result['domain']
            status = result['status']
            total = result['total_contacts']
            
            if result['contacts']:
                for contact in result['contacts'][:5]:  # Top 5 contacts per company
                    writer.writerow([
                        company,
                        domain,
                        status,
                        total,
                        f"{contact.get('first_name', '')} {contact.get('last_name', '')}".strip(),
                        contact.get('email', ''),
                        contact.get('position', ''),
                        contact.get('department', ''),
                        contact.get('seniority', ''),
                        contact.get('confidence', ''),
                        contact.get('sources', ''),
                        contact.get('verification', '')
                    ])
            else:
                writer.writerow([company, domain, status, total, '', '', '', '', '', '', '', ''])
    
    print("✓ CSV summary saved to auvsi_member_contacts_summary.csv")
    
    # Save executive email list
    executive_emails = []
    for result in results:
        if result['contacts']:
            for contact in result['contacts']:
                position = contact.get('position', '').lower() if contact.get('position') else ''
                if ('ceo' in position or 'cto' in position or 'president' in position or 
                    'vp' in position or 'director' in position or 'head' in position):
                    executive_emails.append(contact['email'])
    
    with open('auvsi_executive_emails.txt', 'w') as f:
        for email in executive_emails:
            f.write(f"{email}\n")
    
    print(f"✓ Executive email list saved to auvsi_executive_emails.txt ({len(executive_emails)} emails)")
    
    # Generate report
    successful = sum(1 for r in results if r['status'] == 'success')
    total_contacts = sum(r['total_contacts'] for r in results)
    
    report = f"""
=== AUVSI MEMBER CONTACTS EXTRACTION REPORT ===
Date: {time.strftime('%Y-%m-%d %H:%M:%S')}
Total Companies Processed: {len(results)}
Successful Searches: {successful} ({successful/len(results)*100:.1f}%)
Total Contacts Found: {total_contacts}
Average Contacts per Company: {total_contacts/len(results) if len(results) > 0 else 0:.1f}
Executive Emails Extracted: {len(executive_emails)}

=== TOP COMPANIES BY CONTACTS FOUND ===
"""
    
    # Sort by contacts found
    sorted_results = sorted(results, key=lambda x: x['total_contacts'], reverse=True)
    
    for i, result in enumerate(sorted_results[:10], 1):
        if result['total_contacts'] > 0:
            report += f"{i}. {result['company']}: {result['total_contacts']} contacts\n"
    
    report += f"""
=== FILES GENERATED ===
1. auvsi_member_contacts_complete.json - Complete contact data
2. auvsi_member_contacts_summary.csv - CSV summary
3. auvsi_executive_emails.txt - Executive email list

=== NEXT STEPS ===
1. Use emails for outreach campaigns
2. Verify emails before mass sending
3. Segment by company type/industry
4. Personalize outreach based on role/department
"""

    with open('auvsi_contacts_extraction_report.md', 'w') as f:
        f.write(report)
    
    print("✓ Report saved to auvsi_contacts_extraction_report.md")
    
    print("\n" + "=" * 70)
    print("✅ CONTACT EXTRACTION COMPLETE!")
    print(f"• Processed: {len(results)} companies")
    print(f"• Successful: {successful} searches")
    print(f"• Total contacts: {total_contacts}")
    print(f"• Executive emails: {len(executive_emails)}")
    print("=" * 70)

if __name__ == "__main__":
    main()