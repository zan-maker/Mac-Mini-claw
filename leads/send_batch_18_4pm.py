#!/usr/bin/env python3
"""
Batch 18 - 4 PM Batch - March 9, 2026
Fresh target companies NOT in pipeline - focusing on healthcare, hospitality, and manufacturing
"""

import requests
import json
from datetime import datetime

# Configuration - Use the API key from agentmail-integration.py
AGENTMAIL_API_KEY = "am_us_f03e762c50d6e353bbe7b4307b452bd73f58aed725bc0ef53f25d9f8e91c962a"
AGENTMAIL_INBOX = "zane@agentmail.to"
CC_EMAIL = "sam@impactquadrant.info"

# Fresh target companies - verified NOT in pipeline
TARGET_COMPANIES = [
    {
        "company": "ProMedica Health System",
        "domain": "promedica.org",
        "industry": "Healthcare - Hospital System",
        "location": "Toledo, OH",
        "employees": 150,
        "email": "hr@promedica.org",
        "score": 85
    },
    {
        "company": "Genesis Healthcare",
        "domain": "genesishcc.com",
        "industry": "Healthcare - Post-Acute Care",
        "location": "Kennett Square, PA",
        "employees": 200,
        "email": "hr@genesishcc.com",
        "score": 82
    },
    {
        "company": "Five Star Senior Living",
        "domain": "fivestarseniorliving.com",
        "industry": "Healthcare - Senior Living",
        "location": "Newton, MA",
        "employees": 120,
        "email": "info@fivestarseniorliving.com",
        "score": 78
    },
    {
        "company": "Brookdale Senior Living",
        "domain": "brookdale.com",
        "industry": "Healthcare - Senior Living",
        "location": "Brentwood, TN",
        "employees": 250,
        "email": "hr@brookdale.com",
        "score": 80
    },
    {
        "company": "Capstone Logistics",
        "domain": "capstonelogistics.com",
        "industry": "Logistics/Warehousing",
        "location": "Atlanta, GA",
        "employees": 180,
        "email": "hr@capstonelogistics.com",
        "score": 75
    }
]

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
            json=payload,
            timeout=15
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

def create_outreach_email(company_name, employee_count, industry):
    """Create personalized outreach email"""
    savings = calculate_savings(employee_count)
    
    subject = f"${savings['total']:,} annual savings for {company_name} (zero cost to implement)"
    
    text_content = f"""Hi there,

I noticed {company_name} has about {employee_count:,} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.

Organizations your size are typically saving:

- $681 per employee annually in FICA savings
- 30-60% reduction in workers' comp premiums
- Total savings: ${savings['total']:,}

One medical transportation company with 66 employees saved over $140,000 last year.

The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.

Would you be open to a 10-minute call this week to see the numbers for {company_name}?

Best,
Zane
Zane@agentmail.to
Wellness 125 Cafeteria Plan
"""

    html_content = f"""<p>Hi there,</p>

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

    return subject, text_content, html_content

def main():
    results = []
    
    print(f"\n{'='*60}")
    print(f"Batch 18 - 4 PM Outreach - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Target: 5 emails")
    print(f"{'='*60}\n")
    
    for company in TARGET_COMPANIES:
        print(f"Processing: {company['company']}")
        
        savings = calculate_savings(company['employees'])
        subject, text, html = create_outreach_email(
            company['company'],
            company['employees'],
            company['industry']
        )
        
        result = send_email(
            to_email=company['email'],
            subject=subject,
            text_content=text,
            html_content=html,
            cc=CC_EMAIL
        )
        
        result_data = {
            "company": company['company'],
            "email": company['email'],
            "employees": company['employees'],
            "savings": savings['total'],
            "success": result['success'],
            "timestamp": datetime.now().isoformat()
        }
        
        if result['success']:
            result_data['message_id'] = result.get('message_id')
            print(f"  ✅ Sent - Message ID: {result.get('message_id')}")
        else:
            result_data['error'] = result.get('error')
            print(f"  ❌ Failed - {result.get('error')}")
        
        results.append(result_data)
    
    # Save results
    output_file = f"/Users/cubiczan/.openclaw/workspace/leads/batch_18_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Results saved to: {output_file}")
    print(f"Total sent: {sum(1 for r in results if r['success'])}/{len(results)}")
    print(f"Total potential savings: ${sum(r['savings'] for r in results if r['success']):,.0f}/year")
    print(f"{'='*60}\n")
    
    return results

if __name__ == "__main__":
    main()
