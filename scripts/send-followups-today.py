#!/usr/bin/env python3
"""
Send overdue Day 4 follow-ups for Wellness 125
"""

import requests
from datetime import datetime

# AgentMail Configuration
AGENTMAIL_API_KEY = "am_us_6aa957b36fb69693140cb0787c894d90ec2e65ffe937049634b685b911c1ac14"
AGENTMAIL_INBOX = "Zane@agentmail.to"
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
            return {"success": True, "message_id": response.json().get("message_id"), "response": response.json()}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Overdue Day 4 follow-ups (contacted Feb 25-27, due Feb 29 - Mar 1)
FOLLOWUPS = [
    # Batch 1 - Feb 25 7:31 AM
    {
        "company_name": "Texas Manufacturing Company",
        "email": "info@texasmanufacturingco.com",
        "contact": "Decision Maker",
        "savings": "$103,875",
        "initial_subject": "$103,875 annual savings for Texas Manufacturing Company"
    },
    {
        "company_name": "Southwest Systems Technology, Inc.",
        "email": "info@swsystems.com",
        "contact": "Dee Claybrook",
        "savings": "$88,530",
        "initial_subject": "$88,530 annual savings for Southwest Systems Technology"
    },
    {
        "company_name": "Johnson Equipment Company",
        "email": "info@johnsonequipment.com",
        "contact": "Justin Johnson",
        "savings": "$136,200",
        "initial_subject": "$136,200 annual savings for Johnson Equipment Company"
    },
    {
        "company_name": "Texas Injection Molding",
        "email": "info@texasinjectionmolding.com",
        "contact": "Jeff Applegate",
        "savings": "$53,000",
        "initial_subject": "$53,000 annual savings for Texas Injection Molding"
    },
    {
        "company_name": "Signal Metal Industries, Inc.",
        "email": "info@signalmetal.com",
        "contact": "Decision Maker",
        "savings": "$103,875",
        "initial_subject": "$103,875 annual savings for Signal Metal Industries"
    },
    # Batch 2 - Feb 25 9:38 AM
    {
        "company_name": "Newport LLC",
        "email": "info@newportllc.com",
        "contact": "Decision Maker",
        "savings": "$62,325",
        "initial_subject": "$62,325 annual savings for Newport LLC"
    },
    {
        "company_name": "Nonprofit HR",
        "email": "info@nonprofithr.com",
        "contact": "Decision Maker",
        "savings": "$41,550",
        "initial_subject": "$41,550 annual savings for Nonprofit HR"
    },
    {
        "company_name": "GiaSpace",
        "email": "info@giaspace.com",
        "contact": "Decision Maker",
        "savings": "$66,480",
        "initial_subject": "$66,480 annual savings for GiaSpace"
    },
    {
        "company_name": "Loud Solutions",
        "email": "info@loudsolutions.com",
        "contact": "Decision Maker",
        "savings": "$33,240",
        "initial_subject": "$33,240 annual savings for Loud Solutions"
    },
    # Batch 3 - Feb 25 11:10 AM
    {
        "company_name": "Ingeniu Solutions",
        "email": "bonjour@ingeniusolutions.com",
        "contact": "Decision Maker",
        "savings": "$46,130",
        "initial_subject": "$46,130 annual savings for Ingeniu Solutions"
    },
    {
        "company_name": "BRITECITY",
        "email": "info@britecity.com",
        "contact": "Decision Maker",
        "savings": "$32,335",
        "initial_subject": "$32,335 annual savings for BRITECITY"
    },
    {
        "company_name": "EPC Group",
        "email": "contact@epcgroup.net",
        "contact": "Decision Maker",
        "savings": "$88,130",
        "initial_subject": "$88,130 annual savings for EPC Group"
    },
    {
        "company_name": "Henriott",
        "email": "info@henriott.com",
        "contact": "Decision Maker",
        "savings": "$46,130",
        "initial_subject": "$46,130 annual savings for Henriott"
    },
    {
        "company_name": "Mobix Labs",
        "email": "info@mobixlabs.com",
        "contact": "Decision Maker",
        "savings": "$88,130",
        "initial_subject": "$88,130 annual savings for Mobix Labs"
    },
    # Batch 4 - Feb 25 4:00 PM
    {
        "company_name": "Houston Hospice",
        "email": "info@houstonhospice.org",
        "contact": "Decision Maker",
        "savings": "$112,835",
        "initial_subject": "$112,835 annual savings for Houston Hospice"
    },
    {
        "company_name": "Altus Hospice",
        "email": "info@altushospice.com",
        "contact": "Decision Maker",
        "savings": "$76,125",
        "initial_subject": "$76,125 annual savings for Altus Hospice"
    },
    {
        "company_name": "Hospice of New Mexico",
        "email": "info@hospiceofnewmexico.com",
        "contact": "Decision Maker",
        "savings": "$32,688",
        "initial_subject": "$32,688 annual savings for Hospice of New Mexico"
    },
    {
        "company_name": "Lifted Hospice",
        "email": "info@liftedhospice.com",
        "contact": "Decision Maker",
        "savings": "$49,050",
        "initial_subject": "$49,050 annual savings for Lifted Hospice"
    },
    {
        "company_name": "Hospice of North Idaho",
        "email": "info@hospiceofnorthidaho.org",
        "contact": "Decision Maker",
        "savings": "$25,525",
        "initial_subject": "$25,525 annual savings for Hospice of North Idaho"
    }
]

def create_day4_followup(lead):
    """Create Day 4 follow-up email"""
    first_name = lead["contact"].split()[0] if lead["contact"] != "Decision Maker" else "there"
    
    subject = f"Re: {lead['initial_subject']}"
    
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

<p>Best,<br>
Zane</p>

<p>---<br>
For further information, reach Sam Desigan (Agent Manager)<br>
sam@impactquadrant.info</p>
"""

    return {
        "to": lead["email"],
        "subject": subject,
        "text": text,
        "html": html
    }

def main():
    print("\n" + "="*60)
    print(f"Day 4 Follow-up Outreach - {datetime.now().strftime('%Y-%m-%d %I:%M %p')}")
    print("="*60 + "\n")
    
    results = []
    
    for i, lead in enumerate(FOLLOWUPS, 1):
        print(f"\n[{i}/{len(FOLLOWUPS)}] {lead['company_name']} ({lead['savings']})")
        print(f"  To: {lead['email']}")
        print(f"  CC: {CC_EMAIL}")
        
        email_data = create_day4_followup(lead)
        
        result = send_email(
            to_email=email_data["to"],
            subject=email_data["subject"],
            text_content=email_data["text"],
            html_content=email_data["html"],
            cc=CC_EMAIL
        )
        
        if result["success"]:
            print(f"  ✅ SENT - Message ID: {result.get('message_id', 'N/A')[:50]}...")
            results.append({"company": lead["company_name"], "status": "sent", "message_id": result.get("message_id")})
        else:
            print(f"  ❌ FAILED - {result['error']}")
            results.append({"company": lead["company_name"], "status": "failed", "error": result["error"]})
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    sent = [r for r in results if r["status"] == "sent"]
    failed = [r for r in results if r["status"] == "failed"]
    print(f"Total: {len(results)}")
    print(f"Sent: {len(sent)}")
    print(f"Failed: {len(failed)}")
    
    if failed:
        print("\nFailed emails:")
        for f in failed:
            print(f"  - {f['company']}: {f['error']}")
    
    return results

if __name__ == "__main__":
    main()
