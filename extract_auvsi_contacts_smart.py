#!/usr/bin/env python3
"""
Smart AUVSI contact extraction - Focus on smaller companies and specific roles
"""

import json
import time
import csv
from hunter_io_config import hunter_client
import logging

logger = logging.getLogger("AUVSIContactsSmart")

# Focus on smaller/medium companies that are more likely to work with free plan
SMART_COMPANIES = [
    # Unmanned Systems Specialists (smaller companies)
    {"name": "Shield AI", "domain": "shield.ai", "roles": ["CEO", "CTO", "Business Development"]},
    {"name": "Anduril Industries", "domain": "anduril.com", "roles": ["CEO", "VP Business Development"]},
    {"name": "Skydio", "domain": "skydio.com", "roles": ["CEO", "Sales", "Business Development"]},
    
    # Startup & Innovation
    {"name": "Archer Aviation", "domain": "archer.com", "roles": ["CEO", "Business Development"]},
    {"name": "Joby Aviation", "domain": "jobyaviation.com", "roles": ["CEO", "Business Development"]},
    {"name": "Zipline", "domain": "flyzipline.com", "roles": ["CEO", "Partnerships"]},
    {"name": "Wing", "domain": "wing.com", "roles": ["CEO", "Business Development"]},
    
    # Maritime & Underwater (smaller companies)
    {"name": "Liquid Robotics", "domain": "liquid-robotics.com", "roles": ["CEO", "Sales"]},
    {"name": "Sea Machines Robotics", "domain": "sea-machines.com", "roles": ["CEO", "Business Development"]},
    {"name": "Ocean Infinity America, Inc.", "domain": "oceaninfinity.com", "roles": ["CEO", "Business Development"]},
    
    # Sensor & Component Manufacturers
    {"name": "Ouster", "domain": "ouster.io", "roles": ["CEO", "Sales", "Business Development"]},
    {"name": "Velodyne Lidar", "domain": "velodynelidar.com", "roles": ["CEO", "Business Development"]},
    
    # Defense Technology Startups
    {"name": "Dark Wolf Solutions", "domain": "darkwolfsolutions.com", "roles": ["CEO", "Business Development"]},
    {"name": "Saronic Technologies, Inc.", "domain": "saronictech.com", "roles": ["CEO", "Business Development"]},
    
    # From Maritime Advocacy Committee (smaller companies)
    {"name": "D-Fend Solutions Inc.", "domain": "dfendsolutions.com", "roles": ["CEO", "Sales"]},
    {"name": "DroneShield", "domain": "droneshield.com", "roles": ["CEO", "Business Development"]},
    {"name": "Echodyne Corp", "domain": "echodyne.com", "roles": ["CEO", "Business Development"]},
    {"name": "PteroDynamics Inc.", "domain": "pterodynamics.com", "roles": ["CEO", "Business Development"]},
    
    # Technology Companies (smaller divisions or specific contacts)
    {"name": "Applied Intuition, Inc.", "domain": "appliedintuition.com", "roles": ["CEO", "Business Development"]},
    {"name": "Scale AI", "domain": "scale.com", "roles": ["CEO", "Business Development"]},
]

# Common executive names to try for email finding
EXECUTIVE_ROLES = {
    "CEO": ["CEO", "Chief Executive Officer", "Founder"],
    "CTO": ["CTO", "Chief Technology Officer"],
    "Business Development": ["Business Development", "BD", "Sales", "Partnerships", "Marketing"],
    "Engineering": ["Engineering", "Technical", "Product"]
}

def try_domain_search(domain: str):
    """Try domain search with error handling"""
    try:
        result = hunter_client.domain_search(domain, limit=10)
        return result
    except Exception as e:
        logger.warning(f"Domain search failed for {domain}: {e}")
        return {"data": None, "errors": [str(e)]}

def try_email_finder(domain: str, first_name: str, last_name: str):
    """Try email finder with error handling"""
    try:
        result = hunter_client.email_finder(domain, first_name, last_name)
        return result
    except Exception as e:
        logger.warning(f"Email finder failed for {first_name} {last_name} at {domain}: {e}")
        return {"data": None, "errors": [str(e)]}

def search_company_executives(company: Dict) -> Dict:
    """Search for executive contacts at a company"""
    logger.info(f"Searching executives for: {company['name']}")
    
    result = {
        "company": company["name"],
        "domain": company["domain"],
        "search_method": "executive_search",
        "contacts_found": 0,
        "executives": [],
        "domain_search_results": None,
        "errors": []
    }
    
    # First try domain search
    domain_result = try_domain_search(company["domain"])
    time.sleep(1)  # Rate limiting
    
    if domain_result.get('data') and domain_result['data'].get('emails'):
        emails = domain_result['data']['emails']
        
        # Filter for executive/senior roles
        executive_emails = []
        for email in emails:
            position = email.get('position', '').lower() if email.get('position') else ''
            
            # Check if position matches executive roles
            is_executive = False
            for role_key in EXECUTIVE_ROLES:
                for role_term in EXECUTIVE_ROLES[role_key]:
                    if role_term.lower() in position:
                        is_executive = True
                        break
                if is_executive:
                    break
            
            if is_executive or email.get('confidence', 0) > 70:
                executive_emails.append(email)
        
        result["domain_search_results"] = {
            "total_emails": len(emails),
            "executive_emails": len(executive_emails)
        }
        
        # Add executive contacts
        for email in executive_emails[:5]:  # Limit to top 5
            result["executives"].append({
                "email": email.get('value'),
                "first_name": email.get('first_name'),
                "last_name": email.get('last_name'),
                "position": email.get('position'),
                "confidence": email.get('confidence'),
                "sources": len(email.get('sources', []))
            })
        
        result["contacts_found"] = len(executive_emails)
        logger.info(f"✓ Found {len(executive_emails)} executives via domain search")
    
    else:
        result["errors"].append("Domain search failed or no emails found")
        logger.warning(f"✗ Domain search failed for {company['name']}")
    
    # If no executives found, try common CEO names
    if result["contacts_found"] == 0:
        logger.info(f"Trying common CEO names for {company['name']}")
        
        # Common CEO first names to try
        common_ceo_names = [
            ("John", "Smith"), ("David", "Jones"), ("Michael", "Johnson"),
            ("Robert", "Williams"), ("James", "Brown"), ("Mary", "Davis"),
            ("Jennifer", "Miller"), ("Lisa", "Wilson"), ("Sarah", "Taylor")
        ]
        
        for first_name, last_name in common_ceo_names[:3]:  # Try first 3
            email_result = try_email_finder(company["domain"], first_name, last_name)
            time.sleep(1)
            
            if email_result.get('data') and email_result['data'].get('email'):
                data = email_result['data']
                result["executives"].append({
                    "email": data.get('email'),
                    "first_name": data.get('first_name', first_name),
                    "last_name": data.get('last_name', last_name),
                    "position": data.get('position', 'Executive'),
                    "confidence": data.get('confidence', 0),
                    "sources": data.get('sources', 0),
                    "method": "email_finder"
                })
                result["contacts_found"] += 1
                logger.info(f"✓ Found contact via email finder: {data.get('email')}")
                break
    
    return result

def save_results(results: List[Dict]):
    """Save results to files"""
    
    # Save JSON
    json_file = "auvsi_executive_contacts.json"
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    logger.info(f"JSON saved to {json_file}")
    
    # Save CSV
    csv_file = "auvsi_executive_contacts.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Company', 'Domain', 'Contacts Found',
            'Executive Name', 'Email', 'Position',
            'Confidence', 'Sources', 'Search Method'
        ])
        
        for result in results:
            company = result['company']
            domain = result['domain']
            contacts_found = result['contacts_found']
            
            if result['executives']:
                for exec_contact in result['executives']:
                    writer.writerow([
                        company,
                        domain,
                        contacts_found,
                        f"{exec_contact.get('first_name', '')} {exec_contact.get('last_name', '')}".strip(),
                        exec_contact.get('email', ''),
                        exec_contact.get('position', ''),
                        exec_contact.get('confidence', ''),
                        exec_contact.get('sources', ''),
                        exec_contact.get('method', 'domain_search')
                    ])
            else:
                writer.writerow([company, domain, contacts_found, '', '', '', '', '', ''])
    
    logger.info(f"CSV saved to {csv_file}")
    
    # Create email list only
    email_file = "auvsi_executive_emails.txt"
    with open(email_file, 'w') as f:
        for result in results:
            if result['executives']:
                for exec_contact in result['executives']:
                    email = exec_contact.get('email')
                    if email:
                        f.write(f"{email}\n")
    
    logger.info(f"Email list saved to {email_file}")

def generate_summary(results: List[Dict]):
    """Generate summary report"""
    total_companies = len(results)
    companies_with_contacts = sum(1 for r in results if r['contacts_found'] > 0)
    total_contacts = sum(r['contacts_found'] for r in results)
    
    summary = f"""
=== AUVSI EXECUTIVE CONTACTS SUMMARY ===
Date: {time.strftime('%Y-%m-%d %H:%M:%S')}
Total Companies: {total_companies}
Companies with Contacts: {companies_with_contacts} ({companies_with_contacts/total_companies*100:.1f}%)
Total Executive Contacts: {total_contacts}

=== TOP COMPANIES ===
"""
    
    # Sort by contacts found
    sorted_results = sorted(results, key=lambda x: x['contacts_found'], reverse=True)
    
    for i, result in enumerate(sorted_results[:10], 1):
        if result['contacts_found'] > 0:
            summary += f"{i}. {result['company']}: {result['contacts_found']} executives\n"
            for exec_contact in result['executives'][:2]:  # Show top 2
                summary += f"   - {exec_contact.get('first_name', '')} {exec_contact.get('last_name', '')} ({exec_contact.get('position', '')}): {exec_contact.get('email', '')}\n"
    
    summary += f"\n=== FILES GENERATED ===\n"
    summary += f"1. auvsi_executive_contacts.json - Complete data\n"
    summary += f"2. auvsi_executive_contacts.csv - CSV export\n"
    summary += f"3. auvsi_executive_emails.txt - Email list only\n"
    
    # Save summary
    summary_file = "auvsi_executive_contacts_summary.md"
    with open(summary_file, 'w') as f:
        f.write(summary)
    
    print(summary)
    logger.info(f"Summary saved to {summary_file}")

def main():
    """Main execution"""
    logger.info("Starting smart AUVSI executive contact extraction...")
    logger.info(f"Targeting {len(SMART_COMPANIES)} smaller/medium companies")
    
    # Check account limits
    account_info = hunter_client.get_account_info()
    if account_info.get('data'):
        credits = account_info['data']['requests']['credits']
        logger.info(f"Available credits: {credits['available']}")
        logger.info(f"Used credits: {credits['used']}")
        
        # Limit based on available credits
        max_companies = min(len(SMART_COMPANIES), int(credits['available']))
        companies_to_search = SMART_COMPANIES[:max_companies]
        logger.info(f"Will search {len(companies_to_search)} companies")
    else:
        companies_to_search = SMART_COMPANIES[:15]  # Conservative limit
        logger.warning("Using default limit of 15 companies")
    
    # Search for executives
    results = []
    for i, company in enumerate(companies_to_search):
        logger.info(f"Processing {i+1}/{len(companies_to_search)}: {company['name']}")
        result = search_company_executives(company)
        results.append(result)
        
        # Save progress
        if (i + 1) % 5 == 0:
            progress_file = f"auvsi_executives_progress_{i+1}.json"
            with open(progress_file, 'w') as f:
                json.dump(results, f, indent=2)
            logger.info(f"Progress saved to {progress_file}")
    
    # Save final results
    save_results(results)
    
    # Generate summary
    generate_summary(results)
    
    logger.info("Executive contact extraction complete!")

if __name__ == "__main__":
    main()