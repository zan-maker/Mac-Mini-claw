#!/usr/bin/env python3
"""
Send Batch 7 Outreach Emails - 4 PM Batch
"""

import requests
import json

# AgentMail Configuration
AGENTMAIL_API_KEY = "am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
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

def create_outreach_email(company_name, employee_count, industry, contact_name):
    """Create personalized outreach email for Wellness 125"""
    
    # Calculate potential savings
    fica_savings = employee_count * 681
    workers_comp_savings = employee_count * 500 * 0.30
    total_savings = fica_savings + workers_comp_savings
    
    # Subject line
    subject = f"${total_savings:,} annual savings for {company_name} (zero cost to implement)"
    
    # Plain text version
    first_name = contact_name.split()[0] if contact_name else "there"
    
    text_content = f"""Hi {first_name},

I noticed {company_name} has about {employee_count} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.

Organizations your size are typically saving:
• $681 per employee annually in FICA savings
• 30-60% reduction in workers' comp premiums
• Total savings: ${total_savings:,}

One medical transportation company with 66 employees saved over $140,000 last year.

The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.

Would you be open to a 10-minute call this week to see the numbers for {company_name}?

Best,
Zane
Zane@agentmail.to
Wellness 125 Cafeteria Plan
"""

    # HTML version
    html_content = f"""<p>Hi {first_name},</p>

<p>I noticed {company_name} has about {employee_count} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.</p>

<p><strong>Organizations your size are typically saving:</strong></p>
<ul>
<li>$681 per employee annually in FICA savings</li>
<li>30-60% reduction in workers' comp premiums</li>
<li><strong>Total savings: ${total_savings:,}</strong></li>
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
        "subject": subject,
        "text": text_content,
        "html": html_content,
        "savings": total_savings
    }

# Companies to contact
companies = [
    {
        "company_name": "VITAS Healthcare",
        "employees_count": 100,
        "industry": "Healthcare / Hospice",
        "contact_name": "Leadership Team",
        "email": "info@vitas.com"
    },
    {
        "company_name": "Adecco Staffing",
        "employees_count": 150,
        "industry": "Staffing / HR Services",
        "contact_name": "HR Department",
        "email": "info@adecco.com"
    },
    {
        "company_name": "Lakewood Staffing",
        "employees_count": 50,
        "industry": "Staffing Services",
        "contact_name": "Management Team",
        "email": "info@lakewoodstaffing.com"
    },
    {
        "company_name": "Alive Hospice",
        "employees_count": 150,
        "industry": "Healthcare / Hospice",
        "contact_name": "Leadership Team",
        "email": "info@alivehospice.org"
    },
    {
        "company_name": "Daikin Comfort Technologies",
        "employees_count": 200,
        "industry": "Manufacturing / HVAC",
        "contact_name": "HR Department",
        "email": "info@daikincomfort.com"
    }
]

print("\n" + "="*60)
print("BATCH 7 OUTREACH - 4 PM (5 emails)")
print("="*60 + "\n")

results = []
total_savings = 0

for company in companies:
    email_data = create_outreach_email(
        company_name=company["company_name"],
        employee_count=company["employees_count"],
        industry=company["industry"],
        contact_name=company["contact_name"]
    )
    
    result = send_email(
        to_email=company["email"],
        subject=email_data["subject"],
        text_content=email_data["text"],
        html_content=email_data["html"],
        cc=CC_EMAIL
    )
    
    results.append({
        "company": company["company_name"],
        "email": company["email"],
        "employees": company["employees_count"],
        "savings": email_data["savings"],
        "result": result
    })
    
    print(f"\n{company['company_name']}")
    print(f"  Email: {company['email']}")
    print(f"  Employees: {company['employees_count']}")
    print(f"  Est. Savings: ${email_data['savings']:,}/year")
    
    if result['success']:
        print(f"  ✅ SUCCESS - Message ID: {result['message_id']}")
        total_savings += email_data['savings']
    else:
        print(f"  ❌ FAILED - Error: {result['error']}")

print("\n" + "="*60)
print("BATCH 7 SUMMARY")
print("="*60)
success_count = sum(1 for r in results if r['result']['success'])
print(f"Emails sent: {success_count}/5")
print(f"Failed: {5 - success_count}")
print(f"Total potential savings: ${total_savings:,}/year")
print(f"CC: {CC_EMAIL} (on all emails)")
print("="*60 + "\n")
