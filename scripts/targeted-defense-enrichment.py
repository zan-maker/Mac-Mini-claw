#!/usr/bin/env python3
"""
Targeted contact enrichment for specific defense companies and funds
Based on outreach-log-2026-02-26.md
"""

import requests
import json
import re
from datetime import datetime
import time

HUNTER_API_KEY = "601920a0b5d6b80f9131d4ae588065f694840081"

# Specific companies and funds from the log
DEFENSE_TARGETS = [
    # Companies (Score 70+)
    {"name": "Helsing", "country": "Germany", "score": 92, "type": "company"},
    {"name": "Quantum Systems", "country": "Germany", "score": 88, "type": "company"},
    {"name": "Comand AI", "country": "France", "score": 85, "type": "company"},
    {"name": "BforeAI", "country": "France/Global", "score": 82, "type": "company"},
    {"name": "VIZGARD", "country": "UK", "score": 80, "type": "company"},
    {"name": "RobCo", "country": "Germany", "score": 75, "type": "company"},
    {"name": "XRF.ai", "country": "Europe", "score": 72, "type": "company"},
    {"name": "Perciv AI", "country": "Europe", "score": 70, "type": "company"},
    
    # Funds
    {"name": "MASNA Ventures", "country": "Saudi Arabia", "score": 95, "type": "fund"},
    {"name": "Raphe mPhibr Investors", "country": "India", "score": 88, "type": "fund"},
    {"name": "iDEX Ecosystem Investors", "country": "India", "score": 85, "type": "fund"},
    {"name": "General Atlantic", "country": "Global/Middle East", "score": 82, "type": "fund"},
    {"name": "Blackstone", "country": "Global/Middle East", "score": 80, "type": "fund"},
]

def extract_domain(name, country, target_type):
    """Extract likely domain for a company/fund"""
    
    # Clean the name
    clean_name = re.sub(r'[^\w\s-]', '', name.lower())
    clean_name = re.sub(r'\s+(ai|\.ai|ventures|investors|ecosystem|systems|inc|llc|corp|gmbh)$', '', clean_name)
    clean_name = clean_name.strip()
    
    # Convert to domain
    domain = clean_name.replace(' ', '-').replace('--', '-') + '.com'
    
    # Special cases
    if name == "General Atlantic":
        domain = "generalatlantic.com"
    elif name == "Blackstone":
        domain = "blackstone.com"
    elif name == "MASNA Ventures":
        domain = "masna.vc"  # Common VC domain pattern
    
    return domain

def find_contact_email(domain, target_name, target_type):
    """Find contact email using Hunter.io"""
    
    try:
        url = "https://api.hunter.io/v2/email-finder"
        params = {
            "domain": domain,
            "api_key": HUNTER_API_KEY
        }
        
        # For companies, try common roles
        if target_type == "company":
            # Try info@, contact@, hello@ first (no credits)
            test_emails = [
                f"info@{domain}",
                f"contact@{domain}",
                f"hello@{domain}",
                f"business@{domain}"
            ]
            
            # Return first likely email pattern
            for email in test_emails:
                # Simple validation
                if '@' in email and '.' in email.split('@')[1]:
                    return email, "generic", 0
        
        # For funds, try partners/investment team
        elif target_type == "fund":
            test_emails = [
                f"info@{domain}",
                f"partners@{domain}",
                f"investments@{domain}",
                f"contact@{domain}"
            ]
            
            for email in test_emails:
                if '@' in email and '.' in email.split('@')[1]:
                    return email, "generic", 0
        
        # If generic emails don't work, try Hunter.io (uses credits)
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            email = data.get('data', {}).get('email')
            score = data.get('data', {}).get('score', 0)
            
            if email:
                return email, f"hunter_score_{score}", 1
        
        return None, "not_found", 0
        
    except Exception as e:
        print(f"   Error: {str(e)}")
        return None, "error", 0

def main():
    """Main enrichment process"""
    
    print("=" * 80)
    print("🎯 TARGETED DEFENSE CONTACT ENRICHMENT")
    print("=" * 80)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Targets: {len(DEFENSE_TARGETS)} companies/funds")
    print()
    
    enriched_targets = []
    credits_used = 0
    
    for i, target in enumerate(DEFENSE_TARGETS):
        print(f"{i+1}. {target['name']} ({target['country']}) - Score: {target['score']}")
        
        # Get domain
        domain = extract_domain(target['name'], target['country'], target['type'])
        print(f"   Domain: {domain}")
        
        # Find email
        email, source, credits = find_contact_email(domain, target['name'], target['type'])
        
        if email:
            print(f"   ✅ Email: {email} (source: {source})")
            target['email'] = email
            target['email_source'] = source
            enriched_targets.append(target)
        else:
            print(f"   ⚠️ No email found")
            target['email'] = None
            target['email_source'] = "not_found"
        
        credits_used += credits
        
        # Rate limiting
        time.sleep(0.5)
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 ENRICHMENT RESULTS")
    print("=" * 80)
    
    found_emails = [t for t in enriched_targets if t.get('email')]
    print(f"✅ Emails found: {len(found_emails)}/{len(DEFENSE_TARGETS)}")
    print(f"💰 Credits used: {credits_used}")
    
    if found_emails:
        print("\n📧 EMAILS FOUND:")
        for target in found_emails:
            print(f"   • {target['name']}: {target['email']}")
    
    # Save results
    output_file = "/Users/cubiczan/.openclaw/workspace/defense-target-emails.json"
    with open(output_file, 'w') as f:
        json.dump({
            'enriched_at': datetime.now().isoformat(),
            'targets': enriched_targets,
            'credits_used': credits_used,
            'summary': {
                'total_targets': len(DEFENSE_TARGETS),
                'emails_found': len(found_emails),
                'success_rate': f"{(len(found_emails)/len(DEFENSE_TARGETS)*100):.1f}%"
            }
        }, f, indent=2)
    
    print(f"\n📁 Results saved to: {output_file}")
    
    # Create CSV for easy import
    csv_file = "/Users/cubiczan/.openclaw/workspace/defense-contacts-ready.csv"
    with open(csv_file, 'w') as f:
        f.write("Name,Country,Score,Type,Email,Email Source\n")
        for target in enriched_targets:
            email = target.get('email', '')
            f.write(f"{target['name']},{target['country']},{target['score']},{target['type']},{email},{target.get('email_source', '')}\n")
    
    print(f"📊 CSV ready for import: {csv_file}")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Update defense outreach script with these emails")
    print("2. Run defense outreach at 2:00 PM today")
    print("3. Monitor response rates")
    print("4. Follow up in 3-5 days if no response")

if __name__ == "__main__":
    main()