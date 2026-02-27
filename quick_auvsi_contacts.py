#!/usr/bin/env python3
"""
Quick AUVSI contact extraction for key smaller companies
"""

import json
import csv
import time
from hunter_io_config import hunter_client

# Smaller AUVSI companies that are likely to work
COMPANIES = [
    {"name": "Ouster", "domain": "ouster.io"},
    {"name": "Shield AI", "domain": "shield.ai"},
    {"name": "Anduril Industries", "domain": "anduril.com"},
    {"name": "Archer Aviation", "domain": "archer.com"},
    {"name": "Joby Aviation", "domain": "jobyaviation.com"},
    {"name": "Zipline", "domain": "flyzipline.com"},
    {"name": "Sea Machines Robotics", "domain": "sea-machines.com"},
    {"name": "Liquid Robotics", "domain": "liquid-robotics.com"},
    {"name": "Velodyne Lidar", "domain": "velodynelidar.com"},
    {"name": "Applied Intuition, Inc.", "domain": "appliedintuition.com"},
    {"name": "Scale AI", "domain": "scale.com"},
    {"name": "Dark Wolf Solutions", "domain": "darkwolfsolutions.com"},
    {"name": "Saronic Technologies, Inc.", "domain": "saronictech.com"},
    {"name": "D-Fend Solutions Inc.", "domain": "dfendsolutions.com"},
    {"name": "DroneShield", "domain": "droneshield.com"},
    {"name": "Echodyne Corp", "domain": "echodyne.com"},
    {"name": "PteroDynamics Inc.", "domain": "pterodynamics.com"},
    {"name": "Skydio", "domain": "skydio.com"},
    {"name": "Parrot", "domain": "parrot.com"},
    {"name": "Matternet", "domain": "matternet.com"},
]

def extract_contacts():
    """Extract contacts for selected companies"""
    results = []
    
    print("Starting AUVSI contact extraction...")
    print(f"Processing {len(COMPANIES)} companies")
    print("=" * 60)
    
    for i, company in enumerate(COMPANIES):
        print(f"{i+1}/{len(COMPANIES)}: {company['name']} ({company['domain']})")
        
        try:
            # Domain search
            result = hunter_client.domain_search(company['domain'], limit=10)
            time.sleep(1)  # Rate limiting
            
            if result.get('data') and result['data'].get('emails'):
                emails = result['data']['emails']
                
                # Filter for executive/senior contacts
                executives = []
                for email in emails:
                    position = email.get('position', '').lower() if email.get('position') else ''
                    seniority = email.get('seniority', '').lower() if email.get('seniority') else ''
                    
                    # Look for executives
                    if ('ceo' in position or 'cto' in position or 'president' in position or 
                        'vp' in position or 'director' in position or 'head' in position or
                        'executive' in seniority or email.get('confidence', 0) > 80):
                        
                        executives.append({
                            "email": email.get('value'),
                            "first_name": email.get('first_name'),
                            "last_name": email.get('last_name'),
                            "position": email.get('position'),
                            "seniority": email.get('seniority'),
                            "department": email.get('department'),
                            "confidence": email.get('confidence'),
                            "sources": len(email.get('sources', [])),
                            "verification": email.get('verification', {}).get('status')
                        })
                
                company_result = {
                    "company": company['name'],
                    "domain": company['domain'],
                    "status": "success",
                    "total_emails": len(emails),
                    "executives_found": len(executives),
                    "executives": executives,
                    "pattern": result['data'].get('pattern'),
                    "organization": result['data'].get('organization')
                }
                
                print(f"  ✓ Found {len(emails)} emails, {len(executives)} executives")
                
                if executives:
                    for exec in executives[:2]:  # Show top 2
                        print(f"    - {exec['first_name']} {exec['last_name']} ({exec['position']}): {exec['email']}")
                
            else:
                company_result = {
                    "company": company['name'],
                    "domain": company['domain'],
                    "status": "no_results",
                    "total_emails": 0,
                    "executives_found": 0,
                    "executives": [],
                    "error": result.get('errors', ['No data'])[0] if result.get('errors') else 'No emails found'
                }
                print(f"  ✗ No emails found")
                
        except Exception as e:
            company_result = {
                "company": company['name'],
                "domain": company['domain'],
                "status": "error",
                "total_emails": 0,
                "executives_found": 0,
                "executives": [],
                "error": str(e)
            }
            print(f"  ✗ Error: {e}")
        
        results.append(company_result)
        print()
    
    return results

def save_results(results):
    """Save results to files"""
    
    # Save JSON
    with open('auvsi_contacts_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("✓ Results saved to auvsi_contacts_results.json")
    
    # Save CSV summary
    with open('auvsi_contacts_summary.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Company', 'Domain', 'Status', 'Total Emails', 'Executives', 'Executive Name', 'Email', 'Position', 'Confidence'])
        
        for result in results:
            company = result['company']
            domain = result['domain']
            status = result['status']
            total_emails = result['total_emails']
            executives = result['executives_found']
            
            if result['executives']:
                for exec in result['executives'][:3]:  # Top 3 executives
                    writer.writerow([
                        company,
                        domain,
                        status,
                        total_emails,
                        executives,
                        f"{exec.get('first_name', '')} {exec.get('last_name', '')}".strip(),
                        exec.get('email', ''),
                        exec.get('position', ''),
                        exec.get('confidence', '')
                    ])
            else:
                writer.writerow([company, domain, status, total_emails, executives, '', '', '', ''])
    
    print("✓ Summary saved to auvsi_contacts_summary.csv")
    
    # Save email list
    with open('auvsi_executive_emails.txt', 'w') as f:
        for result in results:
            if result['executives']:
                for exec in result['executives']:
                    email = exec.get('email')
                    if email:
                        f.write(f"{email}\n")
    
    print("✓ Email list saved to auvsi_executive_emails.txt")
    
    # Generate report
    successful = sum(1 for r in results if r['status'] == 'success')
    total_emails = sum(r['total_emails'] for r in results)
    total_executives = sum(r['executives_found'] for r in results)
    
    report = f"""
=== AUVSI CONTACT EXTRACTION REPORT ===
Date: {time.strftime('%Y-%m-%d %H:%M:%S')}
Companies Processed: {len(results)}
Successful Searches: {successful}
Total Emails Found: {total_emails}
Executive Contacts Found: {total_executives}

=== TOP COMPANIES ===
"""
    
    # Sort by executives found
    sorted_results = sorted(results, key=lambda x: x['executives_found'], reverse=True)
    
    for i, result in enumerate(sorted_results[:10], 1):
        if result['executives_found'] > 0:
            report += f"{i}. {result['company']}: {result['executives_found']} executives\n"
    
    report += f"\n=== FILES GENERATED ===\n"
    report += f"1. auvsi_contacts_results.json - Complete data\n"
    report += f"2. auvsi_contacts_summary.csv - CSV summary\n"
    report += f"3. auvsi_executive_emails.txt - Email list\n"
    
    with open('auvsi_contacts_report.md', 'w') as f:
        f.write(report)
    
    print("✓ Report saved to auvsi_contacts_report.md")
    print("\n" + "=" * 60)
    print(report)

def main():
    """Main function"""
    print("AUVSI Member Contact Extraction")
    print("Using Hunter.io API")
    print("=" * 60)
    
    # Check account info
    account_info = hunter_client.get_account_info()
    if account_info.get('data'):
        credits = account_info['data']['requests']['credits']
        print(f"Available credits: {credits['available']}")
        print(f"Used credits: {credits['used']}")
        print(f"Remaining searches: ~{int(credits['available'])}")
        print()
    
    # Extract contacts
    results = extract_contacts()
    
    # Save results
    save_results(results)
    
    print("\n✅ Contact extraction complete!")

if __name__ == "__main__":
    main()