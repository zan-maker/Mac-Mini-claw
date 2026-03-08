#!/usr/bin/env python3
"""
Send batch of 5 outreach emails for Wellness 125
"""
import requests
import json
from datetime import datetime

# AgentMail Configuration
AGENTMAIL_API_KEY = "am_us_f03e762c50d6e353bbe7b4307b452bd73f58aed725bc0ef53f25d9f8e91c962a"
AGENTMAIL_INBOX = "zane@agentmail.to"
CC_EMAIL = "sam@impactquadrant.info"
BASE_URL = "https://api.agentmail.to/v0"

# Leads to contact
leads = [
    {
        "company_name": "Hospice Care Partners",
        "employees": 120,
        "industry": "Healthcare - Hospice",
        "location": "Atlanta, GA",
        "email": "hr@hospicecarepartners.com",
        "contact_name": "HR Director",
        "total_savings": 99720
    },
    {
        "company_name": "Sunrise Senior Living - Phoenix",
        "employees": 85,
        "industry": "Healthcare - Senior Living",
        "location": "Phoenix, AZ",
        "email": "hr@sunriseseniorliving.com",
        "contact_name": "HR Director",
        "total_savings": 70635
    },
    {
        "company_name": "Premier Hotel Group",
        "employees": 150,
        "industry": "Hospitality - Hotels",
        "location": "Orlando, FL",
        "email": "hr@premierhotelgroup.com",
        "contact_name": "HR Director",
        "total_savings": 124650
    },
    {
        "company_name": "Metro Medical Transport",
        "employees": 45,
        "industry": "Healthcare - Medical Transportation",
        "location": "Denver, CO",
        "email": "hr@metromedicaltransport.com",
        "contact_name": "HR Director",
        "total_savings": 37395
    },
    {
        "company_name": "Mountain View Manufacturing",
        "employees": 75,
        "industry": "Manufacturing",
        "location": "Salt Lake City, UT",
        "email": "hr@mvmanuf.com",
        "contact_name": "HR Director",
        "total_savings": 62325
    }
]

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

def create_email(lead):
    """Create personalized email for a lead"""
    subject = f"${lead['total_savings']:,} annual savings for {lead['company_name']}"
    
    text_content = f"""Hi there,

I noticed {lead['company_name']} has about {lead['employees']} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.

Organizations your size are typically saving:
• $681 per employee annually in FICA savings
• 30-60% reduction in workers' comp premiums
• Total savings: ${lead['total_savings']:,}

One medical transportation company with 66 employees saved over $140,000 last year.

The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.

Would you be open to a 10-minute call this week to see the numbers for {lead['company_name']}?

Best,
Zane
Zane@agentmail.to
Wellness 125 Cafeteria Plan

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info
"""

    html_content = f"""<p>Hi there,</p>

<p>I noticed {lead['company_name']} has about {lead['employees']} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.</p>

<p><strong>Organizations your size are typically saving:</strong></p>
<ul>
<li>$681 per employee annually in FICA savings</li>
<li>30-60% reduction in workers' comp premiums</li>
<li><strong>Total savings: ${lead['total_savings']:,}</strong></li>
</ul>

<p>One medical transportation company with 66 employees saved over $140,000 last year.</p>

<p>The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.</p>

<p>Would you be open to a 10-minute call this week to see the numbers for {lead['company_name']}?</p>

<p>Best,<br>
Zane<br>
Zane@agentmail.to<br>
Wellness 125 Cafeteria Plan</p>

<p>---<br>
For further information, reach Sam Desigan (Agent Manager)<br>
sam@impactquadrant.info</p>
"""

    return {
        "to": lead["email"],
        "subject": subject,
        "text": text_content,
        "html": html_content,
        "cc": CC_EMAIL
    }

def main():
    results = []
    print(f"\n{'='*60}")
    print(f"Wellness 125 Outreach - Batch Email Send")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    for i, lead in enumerate(leads, 1):
        print(f"[{i}/5] Sending to {lead['company_name']}...")
        print(f"  To: {lead['email']}")
        print(f"  Subject: ${lead['total_savings']:,} annual savings for {lead['company_name']}")
        
        email_data = create_email(lead)
        result = send_email(
            to_email=email_data["to"],
            subject=email_data["subject"],
            text_content=email_data["text"],
            html_content=email_data["html"],
            cc=email_data["cc"]
        )
        
        result["company"] = lead["company_name"]
        result["email"] = lead["email"]
        results.append(result)
        
        if result["success"]:
            print(f"  ✅ SUCCESS - Message ID: {result['message_id']}")
        else:
            print(f"  ❌ FAILED - {result['error']}")
        print()
    
    print(f"{'='*60}")
    print("BATCH SUMMARY")
    print(f"{'='*60}")
    success_count = sum(1 for r in results if r["success"])
    print(f"Total emails sent: {success_count}/5")
    print(f"Failed: {5 - success_count}")
    print()
    
    return results

if __name__ == "__main__":
    results = main()
    print(json.dumps(results, indent=2))
