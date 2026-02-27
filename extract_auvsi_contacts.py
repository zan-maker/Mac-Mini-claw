#!/usr/bin/env python3
"""
Extract email contacts for AUVSI member companies using Hunter.io
"""

import re
import json
import time
from typing import Dict, List, Optional
from hunter_io_config import hunter_client
import logging

logger = logging.getLogger("AUVSIContacts")

def extract_domains_from_md(file_path: str) -> List[Dict]:
    """Extract company names and guess domains from markdown file"""
    companies = []
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract company names from the detailed directory
    # Look for lines with company names and numbers
    lines = content.split('\n')
    
    for line in lines:
        # Look for company entries in the format: "### X. Company Name"
        if re.match(r'^### \d+\.\s+.+', line):
            # Extract company name
            company_match = re.match(r'^### \d+\.\s+(.+)$', line)
            if company_match:
                company_name = company_match.group(1).strip()
                
                # Try to find description in next lines
                description = ""
                for next_line in lines[lines.index(line)+1:lines.index(line)+5]:
                    if next_line.strip().startswith('**Description:**'):
                        description = next_line.replace('**Description:**', '').strip()
                        break
                
                # Guess domain from company name
                domain = guess_domain_from_name(company_name)
                
                companies.append({
                    "name": company_name,
                    "description": description,
                    "domain": domain,
                    "emails": [],
                    "contacts": []
                })
    
    return companies

def guess_domain_from_name(company_name: str) -> str:
    """Guess domain from company name"""
    # Remove common suffixes and special characters
    name_clean = re.sub(r'[^\w\s]', '', company_name)
    name_clean = re.sub(r'\s+(Inc|Corp|Corporation|LLC|Ltd|Company|Co|Systems|Technologies|Solutions|Group|International|\.com|\.org)$', '', name_clean, flags=re.IGNORECASE)
    
    # Convert to lowercase and replace spaces with dots or hyphens
    domain_base = name_clean.lower().strip()
    
    # Common domain patterns
    patterns = [
        f"{domain_base.replace(' ', '').replace('&', 'and')}.com",
        f"{domain_base.replace(' ', '-')}.com",
        f"{domain_base.replace(' ', '')}.com",
        f"www.{domain_base.replace(' ', '')}.com",
    ]
    
    return patterns[0]  # Return first guess

def search_company_contacts(company: Dict) -> Dict:
    """Search for contacts at a company domain"""
    if not company.get('domain'):
        logger.warning(f"No domain for {company['name']}")
        return company
    
    logger.info(f"Searching contacts for {company['name']} ({company['domain']})")
    
    try:
        # Domain search
        result = hunter_client.domain_search(company['domain'], limit=10)
        
        if result.get('data'):
            emails = result['data'].get('emails', [])
            company['emails'] = emails
            
            # Extract key contacts
            contacts = []
            for email in emails[:5]:  # Limit to top 5
                contact = {
                    "email": email.get('value'),
                    "first_name": email.get('first_name'),
                    "last_name": email.get('last_name'),
                    "position": email.get('position'),
                    "department": email.get('department'),
                    "confidence": email.get('confidence'),
                    "sources": email.get('sources', [])
                }
                contacts.append(contact)
            
            company['contacts'] = contacts
            company['search_status'] = 'success'
            company['total_emails_found'] = len(emails)
            
            logger.info(f"Found {len(emails)} emails for {company['name']}")
        else:
            company['search_status'] = 'no_results'
            company['error'] = result.get('errors', ['No data returned'])
            logger.warning(f"No emails found for {company['name']}")
            
    except Exception as e:
        company['search_status'] = 'error'
        company['error'] = str(e)
        logger.error(f"Error searching {company['name']}: {e}")
    
    # Rate limiting
    time.sleep(1)
    
    return company

def check_account_limits():
    """Check Hunter.io account limits"""
    logger.info("Checking Hunter.io account limits...")
    account_info = hunter_client.get_account_info()
    
    if account_info.get('data'):
        data = account_info['data']
        logger.info(f"Account: {data.get('email')}")
        logger.info(f"Plan: {data.get('plan_name')}")
        logger.info(f"Calls available: {data.get('calls_available')}")
        logger.info(f"Calls used: {data.get('calls_used')}")
        
        return data
    else:
        logger.error(f"Failed to get account info: {account_info.get('errors')}")
        return None

def save_results(companies: List[Dict], output_file: str):
    """Save results to JSON file"""
    with open(output_file, 'w') as f:
        json.dump(companies, f, indent=2)
    
    logger.info(f"Results saved to {output_file}")
    
    # Also create a summary CSV
    import csv
    csv_file = output_file.replace('.json', '.csv')
    
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Company', 'Domain', 'Status', 'Emails Found', 'Primary Contact', 'Email', 'Position'])
        
        for company in companies:
            primary_contact = company['contacts'][0] if company['contacts'] else {}
            writer.writerow([
                company['name'],
                company.get('domain', ''),
                company.get('search_status', ''),
                company.get('total_emails_found', 0),
                f"{primary_contact.get('first_name', '')} {primary_contact.get('last_name', '')}".strip(),
                primary_contact.get('email', ''),
                primary_contact.get('position', '')
            ])
    
    logger.info(f"CSV summary saved to {csv_file}")

def main():
    """Main execution function"""
    logger.info("Starting AUVSI contact extraction...")
    
    # Check account limits first
    account_info = check_account_limits()
    if not account_info:
        logger.error("Cannot proceed without account info")
        return
    
    calls_available = account_info.get('calls_available', 0)
    logger.info(f"Available API calls: {calls_available}")
    
    # Extract companies from the detailed directory
    companies = extract_domains_from_md('auvsi_detailed_member_directory.md')
    logger.info(f"Extracted {len(companies)} companies")
    
    # Limit based on available calls (each search uses 1 call)
    max_companies = min(len(companies), calls_available - 10)  # Leave some buffer
    companies_to_search = companies[:max_companies]
    
    logger.info(f"Will search {len(companies_to_search)} companies (limited by API calls)")
    
    # Search for contacts
    results = []
    for i, company in enumerate(companies_to_search):
        logger.info(f"Processing {i+1}/{len(companies_to_search)}: {company['name']}")
        result = search_company_contacts(company)
        results.append(result)
        
        # Save progress periodically
        if (i + 1) % 10 == 0:
            temp_file = f"auvsi_contacts_partial_{i+1}.json"
            save_results(results, temp_file)
    
    # Save final results
    output_file = 'auvsi_contacts_complete.json'
    save_results(results, output_file)
    
    # Generate summary report
    successful = sum(1 for c in results if c.get('search_status') == 'success')
    total_emails = sum(c.get('total_emails_found', 0) for c in results)
    
    logger.info(f"=== SUMMARY ===")
    logger.info(f"Companies processed: {len(results)}")
    logger.info(f"Successful searches: {successful}")
    logger.info(f"Total emails found: {total_emails}")
    logger.info(f"Results saved to: {output_file}")
    logger.info(f"CSV summary: {output_file.replace('.json', '.csv')}")

if __name__ == "__main__":
    main()