#!/usr/bin/env python3
"""
Hunter.io Email Enrichment and Outreach
Uses Hunter.io API to find and verify emails, then sends outreach
"""

import os
import sys
import json
import time
from typing import Dict, List, Optional
import requests
from datetime import datetime

# Add current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load Hunter.io client
try:
    from hunter_io_config import hunter_client
    HUNTER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Hunter.io client not available: {e}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path[:3]}")
    HUNTER_AVAILABLE = False

# AgentMail configuration
AGENTMAIL_API_KEY = os.environ.get("AGENTMAIL_API_KEY", "am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f")
FROM_EMAIL = "Zane@agentmail.to"
CC_EMAIL = "sam@impactquadrant.info"

# Companies to enrich (with domains)
COMPANIES = [
    {
        "name": "Precision Products Machining Group",
        "domain": "precprodmachgrp.com",
        "industry": "Precision Manufacturing",
        "known_contacts": [
            {"name": "Don Brown", "title": "CEO", "email": "dbrown@precprodmachgrp.com"}
        ]
    },
    {
        "name": "Midwest Foods",
        "domain": "midwestfoods.com",
        "industry": "Food Distribution",
        "known_contacts": [
            {"name": "Erin Fitzgerald", "title": "Owner/President", "email": "efitzgerald@midwestfoods.com"}
        ]
    },
    {
        "name": "Industrial Supply Company",
        "domain": "indsupply.com",
        "industry": "Industrial Distribution",
        "known_contacts": [
            {"name": "Jessica Yurgaitis", "title": "CEO", "email": "jyurgaitis@indsupply.com"},
            {"name": "Andrew Ward", "title": "CFO", "email": None},
            {"name": "Bob Evans", "title": "Executive Vice President", "email": None}
        ]
    },
    {
        "name": "Peninsula Building Materials",
        "domain": "pbm1923.com",
        "industry": "Building Materials",
        "known_contacts": [
            {"name": "Leadership Team", "title": "Executive Team", "email": "PGshowroom@pbm1923.com"}
        ]
    }
]

def get_hunter_account_info():
    """Get Hunter.io account information"""
    if not HUNTER_AVAILABLE:
        return None
    
    try:
        info = hunter_client.get_account_info()
        return info.get('data')
    except Exception as e:
        print(f"❌ Error getting Hunter.io account info: {e}")
        return None

def domain_search(domain: str, limit: int = 50):
    """Search for emails associated with a domain"""
    if not HUNTER_AVAILABLE:
        return None
    
    try:
        print(f"🔍 Searching domain: {domain}")
        result = hunter_client.domain_search(domain, limit=limit)
        
        if result.get('data') and result['data'].get('emails'):
            emails = result['data']['emails']
            print(f"   Found {len(emails)} emails")
            return emails
        else:
            print(f"   No emails found or error: {result.get('errors', ['Unknown error'])}")
            return None
    except Exception as e:
        print(f"❌ Error searching domain {domain}: {e}")
        return None

def verify_email(email: str):
    """Verify an email address"""
    if not HUNTER_AVAILABLE:
        return None
    
    try:
        print(f"📧 Verifying email: {email}")
        result = hunter_client.email_verifier(email)
        
        if result.get('data'):
            data = result['data']
            status = data.get('status', 'unknown')
            score = data.get('score', 0)
            print(f"   Status: {status}, Score: {score}")
            return data
        else:
            print(f"   Verification failed: {result.get('errors', ['Unknown error'])}")
            return None
    except Exception as e:
        print(f"❌ Error verifying email {email}: {e}")
        return None

def find_email_for_person(domain: str, first_name: str = None, last_name: str = None):
    """Find email for a specific person"""
    if not HUNTER_AVAILABLE:
        return None
    
    try:
        print(f"👤 Finding email for {first_name} {last_name} at {domain}")
        result = hunter_client.email_finder(domain, first_name, last_name)
        
        if result.get('data'):
            data = result['data']
            email = data.get('email')
            if email:
                print(f"   Found: {email}")
                return data
            else:
                print(f"   No email found")
                return None
        else:
            print(f"   Error: {result.get('errors', ['Unknown error'])}")
            return None
    except Exception as e:
        print(f"❌ Error finding email: {e}")
        return None

def send_agentmail_email(to_email: str, to_name: str, company: str, industry: str):
    """Send email via AgentMail API"""
    
    url = "https://api.agentmail.to/v1/emails"
    
    headers = {
        "Authorization": f"Bearer {AGENTMAIL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Generate personalized email body
    first_name = to_name.split()[0] if to_name.split() else to_name
    
    body = f"""Hi {first_name},

I hope this message finds you well. I'm reaching out because we've identified {company} as an excellent candidate for our expense reduction program.

Our team specializes in helping {industry} companies reduce operating expenses by 18-23% without compromising quality or service levels. We've successfully partnered with similar organizations and consistently deliver:

✓ 15-25% reduction in telecommunications, waste management, and utility costs
✓ 100% contingency-based model - you only pay from savings generated
✓ Zero upfront costs or risks to your organization

Given {company}'s profile and industry position, we're confident we can identify significant savings opportunities across your vendor contracts and operational expenses.

Would you be open to a brief 15-minute call next week to explore potential areas where we might help reduce costs? I'd be happy to share specific examples from similar {industry} companies.

If you're not the right person to speak with about this, could you point me in the right direction?

Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.

P.S. Our average client saves $75,000-$150,000 annually, and there's absolutely no cost unless we deliver measurable savings."""
    
    payload = {
        "from": FROM_EMAIL,
        "to": [to_email],
        "cc": [CC_EMAIL],
        "subject": f"Quick question about {company}'s operating expenses",
        "body": body
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        print(f"   ✅ Email sent to {to_email}")
        return {"success": True, "response": response.json()}
    except Exception as e:
        print(f"   ❌ Failed to send email: {e}")
        return {"success": False, "error": str(e)}

def main():
    """Main execution"""
    print("=" * 70)
    print("HUNTER.IO ENRICHMENT & OUTREACH")
    print("=" * 70)
    print()
    
    # Check Hunter.io availability
    if not HUNTER_AVAILABLE:
        print("❌ Hunter.io client not available. Exiting.")
        return
    
    # Get account info
    account_info = get_hunter_account_info()
    if account_info:
        print(f"🔑 Hunter.io Account:")
        print(f"   Email: {account_info.get('email', 'N/A')}")
        print(f"   Plan: {account_info.get('plan_name', 'N/A')}")
        print(f"   Credits: {account_info.get('calls', {}).get('available', 'N/A')}")
        print()
    
    results = []
    
    for company in COMPANIES:
        print(f"\n{'='*50}")
        print(f"Processing: {company['name']}")
        print(f"Domain: {company['domain']}")
        print(f"{'='*50}")
        
        # 1. Domain search to find all emails
        domain_emails = domain_search(company['domain'], limit=20)
        
        # 2. Process known contacts
        for contact in company['known_contacts']:
            print(f"\n📇 Contact: {contact['name']} ({contact['title']})")
            
            email_to_use = None
            
            # If we already have an email, verify it
            if contact['email']:
                verification = verify_email(contact['email'])
                if verification and verification.get('status') == 'valid':
                    email_to_use = contact['email']
                    print(f"   ✅ Email verified: {email_to_use}")
                else:
                    print(f"   ⚠️ Email not valid or verification failed")
            
            # If no email or invalid, try to find it
            if not email_to_use:
                # Extract first and last name
                name_parts = contact['name'].split()
                first_name = name_parts[0] if name_parts else None
                last_name = name_parts[-1] if len(name_parts) > 1 else None
                
                if first_name and last_name:
                    found = find_email_for_person(company['domain'], first_name, last_name)
                    if found and found.get('email'):
                        email_to_use = found['email']
                        # Verify the found email
                        verification = verify_email(email_to_use)
                        if not verification or verification.get('status') != 'valid':
                            email_to_use = None
            
            # Send email if we have a valid address
            if email_to_use:
                print(f"   📤 Sending outreach to: {email_to_use}")
                send_result = send_agentmail_email(
                    email_to_use,
                    contact['name'],
                    company['name'],
                    company['industry']
                )
                
                results.append({
                    "company": company['name'],
                    "contact": contact['name'],
                    "title": contact['title'],
                    "email": email_to_use,
                    "sent": send_result['success'],
                    "timestamp": datetime.now().isoformat()
                })
            else:
                print(f"   ⚠️ No valid email found for {contact['name']}")
                results.append({
                    "company": company['name'],
                    "contact": contact['name'],
                    "title": contact['title'],
                    "email": None,
                    "sent": False,
                    "timestamp": datetime.now().isoformat()
                })
        
        # Small delay between companies to avoid rate limiting
        time.sleep(2)
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    
    sent_count = sum(1 for r in results if r['sent'])
    total_contacts = len(results)
    
    print(f"Total contacts processed: {total_contacts}")
    print(f"Emails sent: {sent_count}")
    print(f"Failed: {total_contacts - sent_count}")
    
    # Save results
    output_file = f"/Users/cubiczan/.openclaw/workspace/hunter-enrichment-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    print(f"{'='*70}")

if __name__ == "__main__":
    # Set environment variable for Hunter.io
    os.environ["HUNTER_IO_API_KEY"] = "e341bb9af29f1da98190364caafb01a6b38e8e1c"
    
    main()
