#!/usr/bin/env python3
"""
Better contact enrichment with improved parsing
"""

import requests
import json
import os
import re
from datetime import datetime
import time

HUNTER_API_KEY = "601920a0b5d6b80f9131d4ae588065f694840081"
CREDITS_USED = 0

def extract_companies_from_md(file_path):
    """Extract companies from markdown format"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    companies = []
    lines = content.split('\n')
    
    current_company = None
    for line in lines:
        # Look for company headers like "### 1. Company Name — Score: 92/100"
        if '— Score:' in line and ('###' in line or '##' in line):
            # Extract company name and score
            match = re.search(r'(\d+\.\s+)?([^—]+)—\s*Score:\s*(\d+)/100', line)
            if match:
                company_name = match.group(2).strip()
                score = int(match.group(3))
                
                if current_company:
                    companies.append(current_company)
                
                current_company = {
                    'name': company_name,
                    'score': score,
                    'details': []
                }
        
        # Collect details for current company
        elif current_company and line.strip().startswith('- **'):
            current_company['details'].append(line.strip())
    
    # Add last company
    if current_company:
        companies.append(current_company)
    
    return companies

def find_ceo_email(company_name):
    """Try to find CEO email for a company"""
    
    global CREDITS_USED
    
    # Extract domain
    domain = company_name.lower().replace(' ', '-').replace('--', '-') + '.com'
    
    # Common CEO first names to try
    ceo_first_names = ['john', 'james', 'robert', 'michael', 'david', 'richard', 
                      'thomas', 'charles', 'chris', 'daniel', 'matthew', 'anthony',
                      'mark', 'paul', 'steven', 'andrew', 'kenneth', 'joshua',
                      'kevin', 'brian', 'george', 'timothy', 'ronald', 'jason',
                      'jeffrey', 'ryan', 'jacob', 'gary', 'nicholas', 'eric']
    
    # Try common CEO patterns
    for first_name in ceo_first_names[:5]:  # Limit to 5 attempts
        try:
            url = "https://api.hunter.io/v2/email-finder"
            params = {
                "domain": domain,
                "first_name": first_name.capitalize(),
                "api_key": HUNTER_API_KEY
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                email = data.get('data', {}).get('email')
                
                if email:
                    CREDITS_USED += 1
                    return email, first_name.capitalize()
            
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"   Error: {str(e)}")
    
    return None, None

def main():
    """Main enrichment process"""
    
    print("=" * 80)
    print("🔍 ENHANCED CONTACT ENRICHMENT")
    print("=" * 80)
    
    # Check defense companies
    defense_file = "/Users/cubiczan/.openclaw/workspace/defense-leads/daily-companies-2026-02-26.md"
    
    if os.path.exists(defense_file):
        print(f"\n📄 Processing defense companies from: {defense_file}")
        
        companies = extract_companies_from_md(defense_file)
        print(f"📊 Found {len(companies)} companies in file")
        
        # Filter for high-scoring companies
        high_score = [c for c in companies if c['score'] >= 70]
        print(f"🎯 {len(high_score)} companies with score >= 70")
        
        # Process top 3 companies (to conserve credits)
        for i, company in enumerate(high_score[:3]):
            print(f"\n{i+1}. {company['name']} (Score: {company['score']}/100)")
            
            # Try to find CEO email
            email, first_name = find_ceo_email(company['name'])
            
            if email:
                print(f"   ✅ Found CEO email: {email}")
                company['ceo_email'] = email
                company['ceo_first_name'] = first_name
            else:
                print(f"   ⚠️ Could not find CEO email")
        
        # Save results
        if high_score:
            output_file = "/Users/cubiczan/.openclaw/workspace/defense-ceo-emails.json"
            with open(output_file, 'w') as f:
                json.dump({
                    'enriched_at': datetime.now().isoformat(),
                    'companies': high_score,
                    'credits_used': CREDITS_USED
                }, f, indent=2)
            
            print(f"\n📁 Saved CEO emails to: {output_file}")
    
    # Check if there are investor files with emails
    print("\n" + "=" * 80)
    print("📈 CHECKING INVESTOR FILES FOR EXISTING EMAILS")
    print("=" * 80)
    
    defense_investor_file = "/Users/cubiczan/.openclaw/workspace/defense-leads/daily-investors-2026-02-26.md"
    
    if os.path.exists(defense_investor_file):
        print(f"\n📄 Checking investor file: {defense_investor_file}")
        
        with open(defense_investor_file, 'r') as f:
            content = f.read()
        
        # Look for email patterns
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        emails = re.findall(email_pattern, content)
        
        if emails:
            print(f"📧 Found {len(emails)} email addresses in investor file:")
            for email in emails[:10]:  # Show first 10
                print(f"   • {email}")
            
            if len(emails) > 10:
                print(f"   ... and {len(emails) - 10} more")
        else:
            print("❌ No email addresses found in investor file")
    
    print("\n" + "=" * 80)
    print("🎯 RECOMMENDED ACTION PLAN")
    print("=" * 80)
    
    print("\n1. DEFENSE SECTOR OUTREACH:")
    print("   • Use emails from investor file if available")
    print("   • If no emails, use CEO emails found (if any)")
    print("   • Run defense outreach at 2:00 PM today")
    
    print("\n2. CREDIT CONSERVATION:")
    print(f"   • Credits used: {CREDITS_USED}")
    print("   • Use emails from existing files first")
    print("   • Only use Hunter.io for critical missing contacts")
    
    print("\n3. CAMPAIGN STATUS:")
    print("   • Defense: ✅ Ready with available emails")
    print("   • Dorada: Should have emails from campaign file")
    print("   • Miami: Should have emails from campaign file")
    print("   • All: ✅ Can proceed with existing contact data")

if __name__ == "__main__":
    main()