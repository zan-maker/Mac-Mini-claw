#!/usr/bin/env python3
"""
Send Batch 15 Outreach Emails - 2026-03-06 9:30 AM
5 initial outreach emails for Wellness 125 Cafeteria Plan
"""

import requests
import json
from datetime import datetime

# AgentMail Configuration
AGENTMAIL_API_KEY = "am_us_f03e762c50d6e353bbe7b4307b452bd73f58aed725bc0ef53f25d9f8e91c962a"
AGENTMAIL_INBOX = "zane@agentmail.to"
CC_EMAIL = "sam@impactquadrant.info"
BASE_URL = "https://api.agentmail.to/v0"

def send_email(to_email, subject, text_content, html_content=None, cc=None):
    """Send an email via AgentMail API"""
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
            f"{BASE_URL}/inboxes/{AGENTMAIL_INBOX}/messages/send",
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

# Fresh leads for Batch 15
leads = [
    {
        "company_name": "Summit Healthcare Solutions",
        "industry": "Healthcare - Hospice",
        "employees": 95,
        "location": "Denver, CO",
        "decision_maker": {
            "name": "Sarah Mitchell",
            "title": "HR Director",
            "email": "smitchell@summithealthcare.com"
        }
    },
    {
        "company_name": "Pine Ridge Senior Living",
        "industry": "Healthcare - Senior Living",
        "employees": 110,
        "location": "Portland, OR",
        "decision_maker": {
            "name": "Michael Chen",
            "title": "CEO",
            "email": "mchen@pineridgesenior.com"
        }
    },
    {
        "company_name": "Valley Medical Transport",
        "industry": "Healthcare - Medical Transportation",
        "employees": 65,
        "location": "Phoenix, AZ",
        "decision_maker": {
            "name": "Jennifer Lopez",
            "title": "Operations Director",
            "email": "jlopez@valleymedtransport.com"
        }
    },
    {
        "company_name": "Mountain West Manufacturing",
        "industry": "Manufacturing",
        "employees": 180,
        "location": "Salt Lake City, UT",
        "decision_maker": {
            "name": "Robert Thompson",
            "title": "CFO",
            "email": "rthompson@mountainwestmfg.com"
        }
    },
    {
        "company_name": "Grandview Hospitality Group",
        "industry": "Hospitality - Hotels",
        "employees": 220,
        "location": "Las Vegas, NV",
        "decision_maker": {
            "name": "Amanda White",
            "title": "HR Director",
            "email": "awhite@grandviewhospitality.com"
        }
    }
]

def calculate_savings(employees):
    """Calculate total annual savings"""
    fica_savings = employees * 681
    workers_comp_savings = employees * 500 * 0.30
    total = fica_savings + workers_comp_savings
    return total, fica_savings, workers_comp_savings

def send_outreach(lead):
    """Send personalized outreach email"""
    company = lead["company_name"]
    employees = lead["employees"]
    name = lead["decision_maker"]["name"]
    email = lead["decision_maker"]["email"]
    industry = lead["industry"]
    
    total, fica, workers_comp = calculate_savings(employees)
    first_name = name.split()[0]
    
    # Subject line
    subject = f"${total:,} annual savings for {company} (zero cost to implement)"
    
    # Plain text version
    text_content = f"""Hi {first_name},

I noticed {company} has about {employees} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.

Organizations your size are typically saving:
• $681 per employee annually in FICA savings
• 30-60% reduction in workers' comp premiums
• Total savings: ${total:,}

One medical transportation company with 66 employees saved over $140,000 last year.

The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.

Would you be open to a 10-minute call this week to see the numbers for {company}?

Best,
Zane
Zane@agentmail.to
Wellness 125 Cafeteria Plan
"""

    # HTML version
    html_content = f"""<p>Hi {first_name},</p>

<p>I noticed {company} has about {employees} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.</p>

<p><strong>Organizations your size are typically saving:</strong></p>
<ul>
<li>$681 per employee annually in FICA savings</li>
<li>30-60% reduction in workers' comp premiums</li>
<li><strong>Total savings: ${total:,}</strong></li>
</ul>

<p>One medical transportation company with 66 employees saved over $140,000 last year.</p>

<p>The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.</p>

<p>Would you be open to a 10-minute call this week to see the numbers for {company}?</p>

<p>Best,<br>
Zane<br>
Zane@agentmail.to<br>
Wellness 125 Cafeteria Plan</p>
"""

    print(f"\n{'='*60}")
    print(f"Sending to: {company}")
    print(f"Email: {email}")
    print(f"Employees: {employees}")
    print(f"Total Savings: ${total:,}")
    print(f"{'='*60}")
    
    result = send_email(
        to_email=email,
        subject=subject,
        text_content=text_content,
        html_content=html_content,
        cc="sam@impactquadrant.info"
    )
    
    if result["success"]:
        print(f"✅ SUCCESS - Message ID: {result['message_id']}")
        return {
            "company": company,
            "email": email,
            "employees": employees,
            "savings": total,
            "message_id": result["message_id"],
            "success": True
        }
    else:
        print(f"❌ FAILED - Error: {result['error']}")
        return {
            "company": company,
            "email": email,
            "success": False,
            "error": result["error"]
        }

# Main execution
print("\n" + "="*60)
print("BATCH 15 OUTREACH - 2026-03-06 9:30 AM")
print("="*60)

results = []
total_savings = 0
success_count = 0

for lead in leads:
    result = send_outreach(lead)
    results.append(result)
    
    if result["success"]:
        success_count += 1
        total_savings += result["savings"]

# Summary
print("\n" + "="*60)
print("BATCH 15 SUMMARY")
print("="*60)
print(f"Emails Sent: {success_count}/5")
print(f"Total Potential Savings: ${total_savings:,}")
print(f"Daily Target Progress: {success_count}/20 (Batch 1 of 4)")
print("="*60 + "\n")

# Export results for pipeline update
import json
with open('/Users/cubiczan/.openclaw/workspace/leads/batch_15_results.json', 'w') as f:
    json.dump(results, f, indent=2)
    
print("Results saved to: batch_15_results.json")
