#!/usr/bin/env python3
"""
Targeted email contact extraction for key AUVSI members
Limited to 50 searches (Hunter.io Free plan limit)
"""

import re
import json
import time
import csv
from typing import Dict, List
from hunter_io_config import hunter_client
import logging

logger = logging.getLogger("AUVSIContactsTargeted")

# Key AUVSI member companies to prioritize (based on importance and domain guessability)
KEY_COMPANIES = [
    # Major Defense Contractors (High Priority)
    {"name": "Boeing Company", "domain": "boeing.com"},
    {"name": "Lockheed Martin Corporation", "domain": "lockheedmartin.com"},
    {"name": "Northrop Grumman", "domain": "northropgrumman.com"},
    {"name": "Raytheon Company", "domain": "raytheon.com"},
    {"name": "General Dynamics Mission Systems", "domain": "gdmissionsystems.com"},
    
    # Unmanned Systems Specialists
    {"name": "AeroVironment", "domain": "avinc.com"},
    {"name": "General Atomics Aeronautical Systems, Inc.", "domain": "ga-asi.com"},
    {"name": "Kratos Defense and Security Solutions, Inc.", "domain": "kratosdefense.com"},
    {"name": "Shield AI", "domain": "shield.ai"},
    {"name": "Anduril Industries", "domain": "anduril.com"},
    
    # Technology Companies
    {"name": "Amazon", "domain": "amazon.com"},
    {"name": "Google", "domain": "google.com"},
    {"name": "Qualcomm Inc.", "domain": "qualcomm.com"},
    {"name": "Intel Corporation", "domain": "intel.com"},
    {"name": "NVIDIA", "domain": "nvidia.com"},
    
    # Startup & Innovation
    {"name": "Archer Aviation", "domain": "archer.com"},
    {"name": "Joby Aviation", "domain": "jobyaviation.com"},
    {"name": "Zipline", "domain": "flyzipline.com"},
    {"name": "Wing", "domain": "wing.com"},
    {"name": "Volocopter", "domain": "volocopter.com"},
    
    # Maritime & Underwater
    {"name": "Liquid Robotics", "domain": "liquid-robotics.com"},
    {"name": "Ocean Infinity America, Inc.", "domain": "oceaninfinity.com"},
    {"name": "Sea Machines Robotics", "domain": "sea-machines.com"},
    {"name": "Teledyne Marine", "domain": "teledyne.com"},
    {"name": "Kongsberg Underwater Technology, Inc.", "domain": "kongsberg.com"},
    
    # Sensor & Component Manufacturers
    {"name": "Ouster", "domain": "ouster.io"},
    {"name": "Velodyne Lidar", "domain": "velodynelidar.com"},
    {"name": "Honeywell", "domain": "honeywell.com"},
    {"name": "Trimble", "domain": "trimble.com"},
    {"name": "FLIR Systems", "domain": "flir.com"},
    
    # Additional from Maritime Advocacy Committee
    {"name": "Booz Allen Hamilton", "domain": "boozallen.com"},
    {"name": "Collins Aerospace", "domain": "collinsaerospace.com"},
    {"name": "Leidos", "domain": "leidos.com"},
    {"name": "SAIC", "domain": "saic.com"},
    {"name": "L3Harris Technologies", "domain": "l3harris.com"},
    
    # International Members
    {"name": "Airbus", "domain": "airbus.com"},
    {"name": "BAE Systems", "domain": "baesystems.com"},
    {"name": "Thales Group", "domain": "thalesgroup.com"},
    {"name": "Leonardo S.p.A.", "domain": "leonardo.com"},
    {"name": "Rafael Advanced Defense Systems", "domain": "rafael.co.il"},
]

def search_company_contacts(company: Dict) -> Dict:
    """Search for contacts at a company domain"""
    logger.info(f"Searching: {company['name']} ({company['domain']})")
    
    result_data = {
        "company": company["name"],
        "domain": company["domain"],
        "search_status": "pending",
        "emails_found": 0,
        "contacts": [],
        "error": None
    }
    
    try:
        # Domain search (uses 1 credit)
        result = hunter_client.domain_search(company['domain'], limit=20)
        
        if result.get('data'):
            data = result['data']
            emails = data.get('emails', [])
            
            # Extract key contacts
            contacts = []
            for email in emails[:10]:  # Limit to top 10
                contact = {
                    "email": email.get('value'),
                    "first_name": email.get('first_name'),
                    "last_name": email.get('last_name'),
                    "position": email.get('position'),
                    "department": email.get('department'),
                    "confidence": email.get('confidence'),
                    "sources_count": len(email.get('sources', [])),
                    "verification_status": email.get('verification', {}).get('status') if email.get('verification') else None
                }
                contacts.append(contact)
            
            result_data.update({
                "search_status": "success",
                "emails_found": len(emails),
                "contacts": contacts,
                "organization": data.get('organization'),
                "country": data.get('country'),
                "pattern": data.get('pattern'),
                "disposable": data.get('disposable'),
                "webmail": data.get('webmail')
            })
            
            logger.info(f"✓ Found {len(emails)} emails for {company['name']}")
            
        else:
            result_data.update({
                "search_status": "no_results",
                "error": result.get('errors', ['No data returned'])[0]
            })
            logger.warning(f"✗ No emails found for {company['name']}")
            
    except Exception as e:
        result_data.update({
            "search_status": "error",
            "error": str(e)
        })
        logger.error(f"✗ Error searching {company['name']}: {e}")
    
    # Rate limiting (1 second between requests)
    time.sleep(1)
    
    return result_data

def save_results(results: List[Dict], output_base: str = "auvsi_key_contacts"):
    """Save results to JSON and CSV files"""
    
    # Save JSON
    json_file = f"{output_base}.json"
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    logger.info(f"JSON results saved to {json_file}")
    
    # Save CSV summary
    csv_file = f"{output_base}.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Company', 'Domain', 'Status', 'Emails Found',
            'Contact Name', 'Email', 'Position', 'Department',
            'Confidence', 'Sources', 'Verification'
        ])
        
        for result in results:
            company = result['company']
            domain = result['domain']
            status = result['search_status']
            emails_found = result['emails_found']
            
            if result['contacts']:
                for contact in result['contacts'][:3]:  # Top 3 contacts
                    writer.writerow([
                        company,
                        domain,
                        status,
                        emails_found,
                        f"{contact.get('first_name', '')} {contact.get('last_name', '')}".strip(),
                        contact.get('email', ''),
                        contact.get('position', ''),
                        contact.get('department', ''),
                        contact.get('confidence', ''),
                        contact.get('sources_count', 0),
                        contact.get('verification_status', '')
                    ])
            else:
                writer.writerow([company, domain, status, emails_found, '', '', '', '', '', '', ''])
    
    logger.info(f"CSV summary saved to {csv_file}")
    
    # Save detailed contacts CSV
    detailed_csv = f"{output_base}_detailed.csv"
    with open(detailed_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Company', 'Domain', 'Email', 'First Name', 'Last Name',
            'Position', 'Department', 'Confidence', 'Sources', 'Verification'
        ])
        
        for result in results:
            if result['contacts']:
                for contact in result['contacts']:
                    writer.writerow([
                        result['company'],
                        result['domain'],
                        contact.get('email', ''),
                        contact.get('first_name', ''),
                        contact.get('last_name', ''),
                        contact.get('position', ''),
                        contact.get('department', ''),
                        contact.get('confidence', ''),
                        contact.get('sources_count', 0),
                        contact.get('verification_status', '')
                    ])
    
    logger.info(f"Detailed contacts saved to {detailed_csv}")

def generate_report(results: List[Dict]):
    """Generate a summary report"""
    successful = sum(1 for r in results if r['search_status'] == 'success')
    total_emails = sum(r['emails_found'] for r in results)
    
    report = f"""
=== AUVSI CONTACT EXTRACTION REPORT ===
Date: {time.strftime('%Y-%m-%d %H:%M:%S')}
Total Companies Searched: {len(results)}
Successful Searches: {successful} ({successful/len(results)*100:.1f}%)
Failed/No Results: {len(results) - successful}
Total Emails Found: {total_emails}
Average Emails per Company: {total_emails/len(results) if len(results) > 0 else 0:.1f}

=== TOP COMPANIES BY EMAILS FOUND ===
"""
    
    # Sort by emails found
    sorted_results = sorted(results, key=lambda x: x['emails_found'], reverse=True)
    
    for i, result in enumerate(sorted_results[:10], 1):
        report += f"{i}. {result['company']}: {result['emails_found']} emails\n"
    
    report += f"\n=== FILES GENERATED ===\n"
    report += f"1. auvsi_key_contacts.json - Complete JSON data\n"
    report += f"2. auvsi_key_contacts.csv - Summary CSV\n"
    report += f"3. auvsi_key_contacts_detailed.csv - All contacts\n"
    
    # Save report
    report_file = "auvsi_contacts_report.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    logger.info(f"Report saved to {report_file}")
    print(report)

def main():
    """Main execution"""
    logger.info("Starting targeted AUVSI contact extraction...")
    logger.info(f"Targeting {len(KEY_COMPANIES)} key companies")
    
    # Check account limits
    account_info = hunter_client.get_account_info()
    if account_info.get('data'):
        credits = account_info['data']['requests']['credits']
        logger.info(f"Available credits: {credits['available']}")
        logger.info(f"Used credits: {credits['used']}")
        
        if credits['available'] < len(KEY_COMPANIES):
            logger.warning(f"Only {credits['available']} credits available, limiting search")
            companies_to_search = KEY_COMPANIES[:credits['available']]
        else:
            companies_to_search = KEY_COMPANIES
    else:
        logger.error("Failed to get account info")
        companies_to_search = KEY_COMPANIES[:25]  # Default limit
    
    # Search for contacts
    results = []
    for i, company in enumerate(companies_to_search):
        logger.info(f"Processing {i+1}/{len(companies_to_search)}")
        result = search_company_contacts(company)
        results.append(result)
        
        # Save progress every 5 companies
        if (i + 1) % 5 == 0:
            temp_file = f"auvsi_contacts_progress_{i+1}.json"
            with open(temp_file, 'w') as f:
                json.dump(results, f, indent=2)
            logger.info(f"Progress saved to {temp_file}")
    
    # Save final results
    save_results(results)
    
    # Generate report
    generate_report(results)
    
    logger.info("Contact extraction complete!")

if __name__ == "__main__":
    main()