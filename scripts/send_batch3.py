#!/usr/bin/env python3
"""Send Batch 3 outreach emails - 11 AM"""

import requests
import json

API_KEY = "am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
INBOX = "Zane@agentmail.to"
CC = "sam@impactquadrant.info"

def send_email(to_email, subject, text_content, html_content=None):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "to": [to_email],
        "subject": subject,
        "text": text_content,
        "cc": [CC]
    }
    
    if html_content:
        payload["html"] = html_content
    
    try:
        response = requests.post(
            f"https://api.agentmail.to/v0/inboxes/{INBOX}/messages/send",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            return {"success": True, "message_id": response.json().get("message_id")}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Lead data for Batch 3
leads = [
    {
        "company": "Ingeniu Solutions",
        "email": "bonjour@ingeniusolutions.com",
        "employees": 50,
        "savings": 46130
    },
    {
        "company": "BRITECITY",
        "email": "info@britecity.com",
        "employees": 35,
        "savings": 32335
    },
    {
        "company": "EPC Group",
        "email": "contact@epcgroup.net",
        "employees": 100,
        "savings": 88130
    },
    {
        "company": "Henriott",
        "email": "info@henriott.com",
        "employees": 50,
        "savings": 46130
    },
    {
        "company": "Mobix Labs",
        "email": "info@mobixlabs.com",
        "employees": 100,
        "savings": 88130
    }
]

results = []
for lead in leads:
    subject = f"${lead['savings']:,} annual savings for {lead['company']} (zero cost to implement)"
    
    text = f"""Hi there,

I noticed {lead['company']} has about {lead['employees']} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.

Organizations your size are typically saving:
• $681 per employee annually in FICA savings
• 30-60% reduction in workers' comp premiums
• Total savings: ${lead['savings']:,}

One medical transportation company with 66 employees saved over $140,000 last year.

The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.

Would you be open to a 10-minute call this week to see the numbers for {lead['company']}?

Best,
Zane
Zane@agentmail.to
Wellness 125 Cafeteria Plan

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info"""

    html = f"""<p>Hi there,</p>
<p>I noticed {lead['company']} has about {lead['employees']} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.</p>
<p><strong>Organizations your size are typically saving:</strong></p>
<ul>
<li>$681 per employee annually in FICA savings</li>
<li>30-60% reduction in workers' comp premiums</li>
<li><strong>Total savings: ${lead['savings']:,}</strong></li>
</ul>
<p>One medical transportation company with 66 employees saved over $140,000 last year.</p>
<p>The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.</p>
<p>Would you be open to a 10-minute call this week to see the numbers for {lead['company']}?</p>
<p>Best,<br>Zane<br>Zane@agentmail.to<br>Wellness 125 Cafeteria Plan</p>
<p>---<br>For further information, reach Sam Desigan (Agent Manager)<br>sam@impactquadrant.info</p>"""

    result = send_email(lead['email'], subject, text, html)
    results.append({
        "company": lead['company'],
        "email": lead['email'],
        "savings": lead['savings'],
        "result": result
    })
    
    status = "✅" if result['success'] else "❌"
    print(f"{status} {lead['company']} ({lead['email']}): ${lead['savings']:,}")
    if not result['success']:
        print(f"   Error: {result['error']}")
    elif result.get('message_id'):
        print(f"   Message ID: {result['message_id']}")

print(f"\n{'='*60}")
print(f"Batch 3 Summary: {sum(1 for r in results if r['result']['success'])}/5 sent successfully")
