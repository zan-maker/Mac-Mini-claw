#!/usr/bin/env python3
"""
Day 4 Follow-up Emails - March 9, 2026
Sending to Batch 14 (originally contacted March 5, 2026 at 2:00 PM)
"""

import requests
import json
from datetime import datetime

# AgentMail Configuration
AGENTMAIL_API_KEY = "am_us_f03e762c50d6e353bbe7b4307b452bd73f58aed725bc0ef53f25d9f8e91c962a"
AGENTMAIL_INBOX = "zane@agentmail.to"
CC_EMAIL = "sam@impactquadrant.info"
BASE_URL = "https://api.agentmail.to/v0"

# Leads due for Day 4 follow-up (March 9, 2026)
FOLLOWUP_LEADS = [
    {
        "company_name": "Select Medical",
        "email": "hr@selectmedical.com",
        "employees": 47000,
        "industry": "Healthcare - Post-Acute Care",
        "savings": 39057000,
        "contacted_date": "2026-03-05"
    },
    {
        "company_name": "Molina Healthcare",
        "email": "hr@molinahealthcare.com",
        "employees": 15000,
        "industry": "Healthcare - Managed Care",
        "savings": 12465000,
        "contacted_date": "2026-03-05"
    },
    {
        "company_name": "Daikin Comfort Technologies",
        "email": "hr@daikincomfort.com",
        "employees": 5000,
        "industry": "Manufacturing - HVAC",
        "savings": 4155000,
        "contacted_date": "2026-03-05"
    },
    {
        "company_name": "Norwex USA",
        "email": "hr@norwex.com",
        "employees": 400,
        "industry": "Manufacturing - Consumer Products",
        "savings": 332400,
        "contacted_date": "2026-03-05"
    },
    {
        "company_name": "Royal Case Company",
        "email": "info@royalcase.com",
        "employees": 300,
        "industry": "Manufacturing - Cases",
        "savings": 249300,
        "contacted_date": "2026-03-05"
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

def create_day4_followup(lead):
    """Create Day 4 follow-up email"""
    
    company = lead["company_name"]
    savings = lead["savings"]
    
    subject = f"Re: ${savings:,} annual savings for {company}"
    
    text = f"""Hi there,

Just following up on my note about the Wellness 125 program. Happy to run a quick savings analysis based on your actual payroll data - takes about 5 minutes to share, shows exact savings broken down by employee count and wage bands.

No cost, no commitment. Just a clear view of what you could save.

Worth a quick call?

Best,
Zane
Zane@agentmail.to
Wellness 125 Cafeteria Plan
"""

    html = f"""<p>Hi there,</p>

<p>Just following up on my note about the Wellness 125 program. Happy to run a quick savings analysis based on your actual payroll data - takes about 5 minutes to share, shows exact savings broken down by employee count and wage bands.</p>

<p><strong>No cost, no commitment.</strong> Just a clear view of what you could save.</p>

<p>Worth a quick call?</p>

<p>Best,<br>
Zane<br>
Zane@agentmail.to<br>
Wellness 125 Cafeteria Plan</p>
"""

    return {
        "to": lead["email"],
        "subject": subject,
        "text": text,
        "html": html,
        "cc": CC_EMAIL
    }

def main():
    print("\n" + "="*60)
    print("Day 4 Follow-up Emails - March 9, 2026 (9:27 AM Batch)")
    print("="*60 + "\n")
    
    results = []
    sent_count = 0
    failed_count = 0
    
    for lead in FOLLOWUP_LEADS:
        print(f"\n📧 Sending to: {lead['company_name']}")
        print(f"   Email: {lead['email']}")
        print(f"   Employees: {lead['employees']:,}")
        print(f"   Savings: ${lead['savings']:,}/year")
        
        email_data = create_day4_followup(lead)
        
        result = send_email(
            to_email=email_data["to"],
            subject=email_data["subject"],
            text_content=email_data["text"],
            html_content=email_data["html"],
            cc=email_data["cc"]
        )
        
        if result["success"]:
            print(f"   ✅ SENT - Message ID: {result['message_id']}")
            sent_count += 1
            results.append({
                "company": lead["company_name"],
                "email": lead["email"],
                "status": "sent",
                "message_id": result["message_id"],
                "savings": lead["savings"]
            })
        else:
            print(f"   ❌ FAILED - {result['error']}")
            failed_count += 1
            results.append({
                "company": lead["company_name"],
                "email": lead["email"],
                "status": "failed",
                "error": result["error"],
                "savings": lead["savings"]
            })
    
    # Summary
    print("\n" + "="*60)
    print("BATCH SUMMARY")
    print("="*60)
    print(f"✅ Sent: {sent_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📊 Total potential savings (sent): ${sum(r['savings'] for r in results if r['status']=='sent'):,}/year")
    print(f"📊 Total potential savings (failed): ${sum(r['savings'] for r in results if r['status']=='failed'):,}/year")
    
    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "batch_type": "day4_followup",
        "sent": sent_count,
        "failed": failed_count,
        "results": results
    }
    
    with open("leads/batch_results_20260309_9am.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n📁 Results saved to: leads/batch_results_20260309_9am.json")
    
    return output

if __name__ == "__main__":
    main()
