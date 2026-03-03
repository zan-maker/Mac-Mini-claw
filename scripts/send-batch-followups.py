#!/usr/bin/env python3
"""
Send Day 4 Follow-up Batch - March 3, 2026 (9:38 AM Batch)
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

# Day 4 Follow-up Leads (Due March 3, 2026)
follow_ups = [
    {
        "company": "BEON.tech",
        "email": "info@beon.tech",
        "savings": 83100,
        "employees": 100,
        "industry": "Technology / Staff Augmentation"
    },
    {
        "company": "USA Compression Partners",
        "email": "info@usacompression.com",
        "savings": 166200,
        "employees": 200,
        "industry": "Energy / Manufacturing"
    },
    {
        "company": "Wisconsin Aluminum Foundry",
        "email": "info@wafco.com",
        "savings": 166200,
        "employees": 200,
        "industry": "Manufacturing"
    },
    {
        "company": "Best Fitness",
        "email": "info@bestfitness.com",
        "savings": 83100,
        "employees": 100,
        "industry": "Healthcare / Fitness"
    },
    {
        "company": "Hospice & Palliative Care",
        "email": "Info@hospicecareinc.org",
        "savings": 37240,
        "employees": 40,
        "industry": "Healthcare / Hospice (New Hartford, NY)"
    }
]

def create_day4_followup(company, savings):
    """Create Day 4 follow-up email"""
    subject = f"Re: ${savings:,} annual savings for {company}"
    
    text = f"""Hi there,

Just following up on my note about the Wellness 125 program. Happy to run a quick savings analysis based on your actual payroll data - takes about 5 minutes to share, shows exact savings broken down by employee count and wage bands.

No cost, no commitment. Just a clear view of what you could save.

Worth a quick call?

Best,
Zane
Zane@agentmail.to
Wellness 125 Cafeteria Plan

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info
"""

    html = f"""<p>Hi there,</p>

<p>Just following up on my note about the Wellness 125 program. Happy to run a quick savings analysis based on your actual payroll data - takes about 5 minutes to share, shows exact savings broken down by employee count and wage bands.</p>

<p><strong>No cost, no commitment.</strong> Just a clear view of what you could save.</p>

<p>Worth a quick call?</p>

<p>Best,<br>
Zane<br>
Zane@agentmail.to<br>
Wellness 125 Cafeteria Plan</p>

<p>---<br>
For further information, reach Sam Desigan (Agent Manager)<br>
sam@impactquadrant.info</p>
"""

    return subject, text, html

# Send follow-ups
print("="*60)
print("Day 4 Follow-up Batch - March 3, 2026 (9:38 AM)")
print("="*60 + "\n")

results = []
total_savings = 0

for lead in follow_ups:
    subject, text, html = create_day4_followup(lead["company"], lead["savings"])
    
    print(f"Sending to: {lead['company']}")
    print(f"  Email: {lead['email']}")
    print(f"  Savings: ${lead['savings']:,}")
    
    result = send_email(
        to_email=lead["email"],
        subject=subject,
        text_content=text,
        html_content=html,
        cc=CC_EMAIL
    )
    
    if result["success"]:
        print(f"  ✅ SUCCESS - Message ID: {result['message_id']}")
        total_savings += lead["savings"]
        results.append({
            "company": lead["company"],
            "email": lead["email"],
            "savings": lead["savings"],
            "status": "sent",
            "message_id": result["message_id"]
        })
    else:
        print(f"  ❌ FAILED - {result['error']}")
        results.append({
            "company": lead["company"],
            "email": lead["email"],
            "savings": lead["savings"],
            "status": "failed",
            "error": result["error"]
        })
    
    print()

print("="*60)
print("BATCH SUMMARY")
print("="*60)
sent = sum(1 for r in results if r["status"] == "sent")
failed = sum(1 for r in results if r["status"] == "failed")
print(f"Emails sent: {sent}/{len(follow_ups)}")
print(f"Failed: {failed}")
print(f"Total potential savings: ${total_savings:,}/year")
print("="*60)

# Save results
with open("/Users/cubiczan/.openclaw/workspace/leads/batch-results-2026-03-03-9am.json", "w") as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "batch": "9:38 AM - Day 4 Follow-ups",
        "results": results,
        "summary": {
            "sent": sent,
            "failed": failed,
            "total_savings": total_savings
        }
    }, f, indent=2)

print("\nResults saved to batch-results-2026-03-03-9am.json")
