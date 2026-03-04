#!/usr/bin/env python3
"""
Send Batch 3 - 5 Outreach Emails
2026-03-04 2:17 PM
"""

import requests
import json
from datetime import datetime

# AgentMail Configuration - Using verified API key
AGENTMAIL_API_KEY = "am_us_f03e762c50d6e353bbe7b4307b452bd73f58aed725bc0ef53f25d9f8e91c962a"
AGENTMAIL_INBOX = "zane@agentmail.to"  # Use lowercase
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

def create_outreach_email(company_name, employee_count, industry, decision_maker_name, decision_maker_email, total_savings):
    """Create personalized outreach email for Wellness 125"""

    # Subject line
    subject = f"${total_savings:,} annual savings for {company_name} (zero cost to implement)"

    # Plain text version
    text_content = f"""Hi {decision_maker_name.split()[0] if decision_maker_name else 'there'},

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
    html_content = f"""<p>Hi {decision_maker_name.split()[0] if decision_maker_name else 'there'},</p>

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
        "to": decision_maker_email,
        "subject": subject,
        "text": text_content,
        "html": html_content,
        "cc": CC_EMAIL
    }

# Leads from daily-leads-2026-03-04.md
leads = [
    {
        "company_name": "Hospice Care Partners",
        "employees": 120,
        "industry": "Healthcare - Hospice",
        "decision_maker_name": "HR Director",
        "decision_maker_email": "hr@hospicecarepartners.com",
        "total_savings": 99720
    },
    {
        "company_name": "Sunrise Senior Living - Phoenix",
        "employees": 85,
        "industry": "Healthcare - Senior Living",
        "decision_maker_name": "HR Director",
        "decision_maker_email": "hr@sunriseseniorliving.com",
        "total_savings": 70635
    },
    {
        "company_name": "Premier Hotel Group",
        "employees": 150,
        "industry": "Hospitality - Hotels",
        "decision_maker_name": "HR Director",
        "decision_maker_email": "hr@premierhotelgroup.com",
        "total_savings": 124650
    },
    {
        "company_name": "Metro Medical Transport",
        "employees": 45,
        "industry": "Healthcare - Medical Transportation",
        "decision_maker_name": "HR Director",
        "decision_maker_email": "hr@metromedicaltransport.com",
        "total_savings": 37395
    },
    {
        "company_name": "Mountain View Manufacturing",
        "employees": 75,
        "industry": "Manufacturing",
        "decision_maker_name": "HR Director",
        "decision_maker_email": "hr@mvmanuf.com",
        "total_savings": 62325
    }
]

# Send emails
print("\n" + "="*70)
print("SENDING BATCH 3 - 5 OUTREACH EMAILS")
print("Time: 2026-03-04 2:17 PM")
print("="*70 + "\n")

results = []
for i, lead in enumerate(leads, 1):
    print(f"[{i}/5] Sending to: {lead['company_name']}")
    print(f"  Email: {lead['decision_maker_email']}")
    print(f"  Savings: ${lead['total_savings']:,}")
    
    email_data = create_outreach_email(
        company_name=lead["company_name"],
        employee_count=lead["employees"],
        industry=lead["industry"],
        decision_maker_name=lead["decision_maker_name"],
        decision_maker_email=lead["decision_maker_email"],
        total_savings=lead["total_savings"]
    )
    
    result = send_email(
        to_email=email_data["to"],
        subject=email_data["subject"],
        text_content=email_data["text"],
        html_content=email_data["html"],
        cc=email_data["cc"]
    )
    
    results.append({
        "company": lead["company_name"],
        "email": lead["decision_maker_email"],
        "result": result
    })
    
    if result["success"]:
        print(f"  ✅ SUCCESS - Message ID: {result['message_id']}\n")
    else:
        print(f"  ❌ FAILED - {result['error']}\n")

# Summary
print("="*70)
print("BATCH SUMMARY")
print("="*70)
success_count = sum(1 for r in results if r["result"]["success"])
failed_count = len(results) - success_count
print(f"✅ Sent: {success_count}")
print(f"❌ Failed: {failed_count}")
print(f"📊 Total Batch: {len(results)}")
print("="*70 + "\n")

# Save results
with open("/Users/cubiczan/.openclaw/workspace/logs/outreach_batch_2026-03-04_14-17.json", "w") as f:
    json.dump({
        "timestamp": "2026-03-04 14:17:00",
        "batch": 3,
        "total_sent": success_count,
        "total_failed": failed_count,
        "results": results
    }, f, indent=2)

print("Results saved to: logs/outreach_batch_2026-03-04_14-17.json\n")
