#!/usr/bin/env python3
"""
Send Day 4 Follow-ups - Batch 19 (March 10, 2026 - 9:47 AM)
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

def send_day4_followup(company_name, contact_email, contact_name, savings_amount):
    """Send Day 4 follow-up email"""
    
    first_name = contact_name.split()[0] if contact_name else "there"
    
    subject = f"Re: ${savings_amount:,} annual savings for {company_name}"
    
    text = f"""Hi {first_name},

Just following up on my note about the Wellness 125 program. Happy to run a quick savings analysis based on your actual payroll data - takes about 5 minutes to share, shows exact savings broken down by employee count and wage bands.

No cost, no commitment. Just a clear view of what you could save.

Worth a quick call?

Best,
Zane

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info
"""
    
    html = f"""<p>Hi {first_name},</p>

<p>Just following up on my note about the Wellness 125 program. Happy to run a quick savings analysis based on your actual payroll data - takes about 5 minutes to share, shows exact savings broken down by employee count and wage bands.</p>

<p><strong>No cost, no commitment.</strong> Just a clear view of what you could save.</p>

<p>Worth a quick call?</p>

<p>Best,<br>Zane</p>

<p>---<br>
For further information, reach Sam Desigan (Agent Manager)<br>
sam@impactquadrant.info</p>
"""
    
    return send_email(
        to_email=contact_email,
        subject=subject,
        text_content=text,
        html_content=html,
        cc=CC_EMAIL
    )

# Leads from Batch 15 (contacted March 6, 2026 - Day 4 follow-up due March 10)
leads = [
    {
        "company": "Summit Healthcare Solutions",
        "email": "smitchell@summithealthcare.com",
        "contact": "S. Mitchell",
        "savings": 78945
    },
    {
        "company": "Pine Ridge Senior Living",
        "email": "mchen@pineridgesenior.com",
        "contact": "M. Chen",
        "savings": 91410
    },
    {
        "company": "Valley Medical Transport",
        "email": "jlopez@valleymedtransport.com",
        "contact": "J. Lopez",
        "savings": 54015
    },
    {
        "company": "Mountain West Manufacturing",
        "email": "rthompson@mountainwestmfg.com",
        "contact": "R. Thompson",
        "savings": 149580
    },
    {
        "company": "Grandview Hospitality Group",
        "email": "awhite@grandviewhospitality.com",
        "contact": "A. White",
        "savings": 182820
    }
]

print("\n" + "="*70)
print("Day 4 Follow-ups - Batch 19 (March 10, 2026 - 9:47 AM)")
print("="*70 + "\n")

results = []
total_savings = 0

for lead in leads:
    print(f"Sending to: {lead['company']} ({lead['email']})")
    print(f"  Subject: Re: ${lead['savings']:,} annual savings for {lead['company']}")
    
    result = send_day4_followup(
        company_name=lead['company'],
        contact_email=lead['email'],
        contact_name=lead['contact'],
        savings_amount=lead['savings']
    )
    
    if result['success']:
        print(f"  ✅ SUCCESS - Message ID: {result['message_id']}")
        total_savings += lead['savings']
        results.append({
            "company": lead['company'],
            "status": "sent",
            "message_id": result['message_id']
        })
    else:
        print(f"  ❌ FAILED - {result['error']}")
        results.append({
            "company": lead['company'],
            "status": "failed",
            "error": result['error']
        })
    
    print()

print("="*70)
print(f"Batch Summary:")
print(f"  Emails Sent: {sum(1 for r in results if r['status'] == 'sent')}/5")
print(f"  Total Potential Savings: ${total_savings:,}/year")
print(f"  FROM: Zane@agentmail.to")
print(f"  CC: sam@impactquadrant.info")
print("="*70 + "\n")

# Output JSON for logging
print("Results JSON:")
print(json.dumps(results, indent=2))
