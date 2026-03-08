#!/usr/bin/env python3
"""
Batch 16 Lead Generation and Outreach - 2:00 PM March 6, 2026
Target: 5 fresh leads with verified emails
"""

import requests
import json
from datetime import datetime

# Configuration
HUNTER_API_KEY = "f701d171cf7decf7e730a6b1c6e9b74f29f39b6e"
AGENTMAIL_API_KEY = "am_us_f03e762c50d6e353bbe7b4307b452bd73f58aed725bc0ef53f25d9f8e91c962a"
AGENTMAIL_INBOX = "zane@agentmail.to"
CC_EMAIL = "sam@impactquadrant.info"

# Target companies (manually curated for email verification)
TARGET_COMPANIES = [
    {
        "company": "Phoenix Children's Hospital",
        "domain": "phoenixchildrens.org",
        "industry": "Healthcare - Pediatric",
        "location": "Phoenix, AZ",
        "employees": 3000,
        "target_role": "HR Director"
    },
    {
        "company": "Banner Health",
        "domain": "bannerhealth.com",
        "industry": "Healthcare - Hospital System",
        "location": "Phoenix, AZ",
        "employees": 50000,
        "target_role": "Benefits Manager"
    },
    {
        "company": "HonorHealth",
        "domain": "honorhealth.com",
        "industry": "Healthcare - Hospital System",
        "location": "Scottsdale, AZ",
        "employees": 12000,
        "target_role": "HR Director"
    },
    {
        "company": "Dignity Health",
        "domain": "dignityhealth.org",
        "industry": "Healthcare - Hospital System",
        "location": "San Francisco, CA",
        "employees": 60000,
        "target_role": "Benefits Manager"
    },
    {
        "company": "Valleywise Health",
        "domain": "valleywisehealth.org",
        "industry": "Healthcare - Public Hospital",
        "location": "Phoenix, AZ",
        "employees": 3500,
        "target_role": "HR Director"
    }
]

def find_email_hunter(domain, company_name):
    """Use Hunter.io to find decision maker email"""
    try:
        url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={HUNTER_API_KEY}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            emails = data.get('data', {}).get('emails', [])
            
            # Look for HR or executive emails
            for email_data in emails:
                email = email_data.get('value', '')
                first_name = email_data.get('first_name', '')
                last_name = email_data.get('last_name', '')
                position = email_data.get('position', '').lower()
                
                # Prioritize HR, Benefits, or C-level
                if any(role in position for role in ['hr', 'human resources', 'benefits', 'ceo', 'cfo', 'president']):
                    return {
                        'email': email,
                        'name': f"{first_name} {last_name}".strip(),
                        'title': email_data.get('position', 'Decision Maker')
                    }
            
            # Fallback to first available email
            if emails:
                email_data = emails[0]
                return {
                    'email': email_data.get('value', ''),
                    'name': f"{email_data.get('first_name', '')} {email_data.get('last_name', '')}".strip(),
                    'title': email_data.get('position', 'Decision Maker')
                }
        
        return None
    except Exception as e:
        print(f"Error finding email for {company_name}: {e}")
        return None

def calculate_savings(employee_count):
    """Calculate potential annual savings"""
    fica_savings = employee_count * 681
    workers_comp_savings = employee_count * 500 * 0.30
    total_savings = fica_savings + workers_comp_savings
    return {
        'fica': fica_savings,
        'workers_comp': workers_comp_savings,
        'total': total_savings
    }

def send_email(to_email, subject, text_content, html_content=None, cc=None):
    """Send email via AgentMail API"""
    headers = {
        "Authorization": f"Bearer {AGENTMAIL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inbox_id": AGENTMAIL_INBOX,
        "to": [to_email],
        "subject": subject,
        "text": text_content
    }
    
    if html_content:
        payload["html"] = html_content
    
    if cc:
        payload["cc"] = [cc] if isinstance(cc, str) else cc
    
    try:
        response = requests.post(
            f"https://api.agentmail.to/v0/inboxes/{AGENTMAIL_INBOX}/messages/send",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "message_id": response.json().get("message_id"),
                "response": response.json()
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def create_outreach_email(company_name, employee_count, industry, decision_maker_name, decision_maker_email):
    """Create personalized outreach email"""
    savings = calculate_savings(employee_count)
    
    subject = f"${savings['total']:,} annual savings for {company_name} (zero cost to implement)"
    
    first_name = decision_maker_name.split()[0] if decision_maker_name else "there"
    
    text_content = f"""Hi {first_name},

I noticed {company_name} has about {employee_count:,} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.

Organizations your size are typically saving:
• $681 per employee annually in FICA savings
• 30-60% reduction in workers' comp premiums
• Total savings: ${savings['total']:,}

One medical transportation company with 66 employees saved over $140,000 last year.

The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.

Would you be open to a 10-minute call this week to see the numbers for {company_name}?

Best,
Zane
Zane@agentmail.to
Wellness 125 Cafeteria Plan
"""
    
    html_content = f"""<p>Hi {first_name},</p>

<p>I noticed {company_name} has about {employee_count:,} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.</p>

<p><strong>Organizations your size are typically saving:</strong></p>
<ul>
<li>$681 per employee annually in FICA savings</li>
<li>30-60% reduction in workers' comp premiums</li>
<li><strong>Total savings: ${savings['total']:,}</strong></li>
</ul>

<p>One medical transportation company with 66 employees saved over $140,000 last year.</p>

<p>The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.</p>

<p>Would you be open to a 10-minute call this week to see the numbers for {company_name}?</p>

<p>Best,<br>
Zane<br>
Zane@agentmail.to<br>
Wellness 125 Cafeteria Plan</p>
"""
    
    return {
        "to": decision_maker_email,
        "subject": subject,
        "text": text_content,
        "html": html_content,
        "cc": CC_EMAIL
    }

def main():
    print("\n" + "="*70)
    print("Batch 16 Lead Generation & Outreach - 2:00 PM March 6, 2026")
    print("="*70 + "\n")
    
    results = []
    sent_count = 0
    bounced_count = 0
    
    for i, company in enumerate(TARGET_COMPANIES, 1):
        print(f"\n[{i}/{len(TARGET_COMPANIES)}] Processing {company['company']}...")
        
        # Find email
        email_data = find_email_hunter(company['domain'], company['company'])
        
        if not email_data or not email_data['email']:
            print(f"  ❌ No email found for {company['company']}")
            bounced_count += 1
            results.append({
                'company': company['company'],
                'status': 'failed',
                'reason': 'No email found'
            })
            continue
        
        # Calculate savings
        savings = calculate_savings(company['employees'])
        
        print(f"  ✓ Found: {email_data['email']} ({email_data['name']})")
        print(f"  ✓ Potential savings: ${savings['total']:,}/year")
        
        # Create and send email
        email = create_outreach_email(
            company_name=company['company'],
            employee_count=company['employees'],
            industry=company['industry'],
            decision_maker_name=email_data['name'],
            decision_maker_email=email_data['email']
        )
        
        result = send_email(
            to_email=email['to'],
            subject=email['subject'],
            text_content=email['text'],
            html_content=email['html'],
            cc=email['cc']
        )
        
        if result['success']:
            sent_count += 1
            print(f"  ✅ Email sent! Message ID: {result['message_id']}")
            results.append({
                'company': company['company'],
                'status': 'sent',
                'email': email_data['email'],
                'contact': email_data['name'],
                'savings': savings['total'],
                'message_id': result['message_id']
            })
        else:
            bounced_count += 1
            print(f"  ❌ Failed: {result['error']}")
            results.append({
                'company': company['company'],
                'status': 'failed',
                'reason': result['error']
            })
    
    # Summary
    print("\n" + "="*70)
    print("BATCH 16 SUMMARY")
    print("="*70)
    print(f"Total companies processed: {len(TARGET_COMPANIES)}")
    print(f"Emails sent: {sent_count}")
    print(f"Failed/Bounced: {bounced_count}")
    print(f"Total potential savings: ${sum([r.get('savings', 0) for r in results]):,}/year")
    print(f"\nFrom: Zane@agentmail.to")
    print(f"CC: {CC_EMAIL}")
    print(f"Time: 2:00 PM EST, March 6, 2026")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"/Users/cubiczan/.openclaw/workspace/leads/batch_16_results_{timestamp}.json"
    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'batch': 16,
            'sent': sent_count,
            'failed': bounced_count,
            'results': results
        }, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    print("="*70 + "\n")
    
    return sent_count, bounced_count

if __name__ == "__main__":
    sent, failed = main()
    exit(0 if sent >= 3 else 1)  # Success if at least 3 sent
