#!/usr/bin/env python3
"""
Daily Outreach Runner - March 10, 2026
Sends follow-ups based on pipeline sequence timing
"""

import requests
import json
from datetime import datetime

# AgentMail Configuration
AGENTMAIL_API_KEY = "am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
AGENTMAIL_INBOX = "zane@agentmail.to"
BASE_URL = "https://api.agentmail.to/v0"
CC_EMAIL = "sam@impactquadrant.info"

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

def send_follow_up_day4(lead_data):
    """Send Day 4 follow-up"""
    subject = f"Re: ${lead_data.get('potential_savings', {}).get('total', 0):,} annual savings for {lead_data.get('company_name', 'Company')}"

    first_name = lead_data.get("decision_maker", {}).get("name", "there")
    if first_name == "HR Director":
        first_name = "there"
    else:
        first_name = first_name.split()[0] if first_name else "there"

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
Zane<br><br>
---<br>
For further information, reach Sam Desigan (Agent Manager)<br>
sam@impactquadrant.info</p>
"""

    return send_email(
        to_email=lead_data.get("decision_maker", {}).get("email", ""),
        subject=subject,
        text_content=text,
        html_content=html,
        cc=CC_EMAIL
    )

# Batch 16c - Day 4 Follow-ups (contacted March 6, 2:11 PM)
batch_16c = [
    {
        "company_name": "Heart to Heart Hospice",
        "decision_maker": {"name": "HR Director", "email": "hr@hearttohearthospice.com"},
        "potential_savings": {"total": 70635}
    },
    {
        "company_name": "Compassionate Care Hospice",
        "decision_maker": {"name": "HR Director", "email": "hr@cch-info.com"},
        "potential_savings": {"total": 58170}
    },
    {
        "company_name": "Southern Care Hospice",
        "decision_maker": {"name": "HR Director", "email": "hr@southerncarehospice.com"},
        "potential_savings": {"total": 78945}
    },
    {
        "company_name": "Medicine Shoppe International",
        "decision_maker": {"name": "HR Director", "email": "hr@medicineshoppe.com"},
        "potential_savings": {"total": 99720}
    },
    {
        "company_name": "Senior Helpers",
        "decision_maker": {"name": "HR Director", "email": "hr@seniorhelpers.com"},
        "potential_savings": {"total": 91410}
    }
]

# Batch 5 - Day 7 Follow-ups (contacted Feb 27, 9:45 AM)
batch_5_day7 = [
    {
        "company_name": "BEON.tech",
        "decision_maker": {"name": "Team", "email": "info@beon.tech"},
        "potential_savings": {"total": 83100},
        "industry": "Technology / Staff Augmentation"
    }
]

# Batch 6 - Day 7 Follow-ups (contacted Feb 27, 2:11 PM)
batch_6_day7 = [
    {
        "company_name": "Hospice & Palliative Care",
        "decision_maker": {"name": "Team", "email": "Info@hospicecareinc.org"},
        "potential_savings": {"total": 37240},
        "industry": "Healthcare / Hospice"
    },
    {
        "company_name": "HospiceCare",
        "decision_maker": {"name": "Team", "email": "info@hospicecarewv.org"},
        "potential_savings": {"total": 79135},
        "industry": "Healthcare / Hospice"
    },
    {
        "company_name": "SoCal Premium Hospice",
        "decision_maker": {"name": "Team", "email": "info@socalpremiumhospice.com"},
        "potential_savings": {"total": 32585},
        "industry": "Healthcare / Hospice"
    },
    {
        "company_name": "North Hawaii Hospice",
        "decision_maker": {"name": "Team", "email": "info@northhawaiihospice.org"},
        "potential_savings": {"total": 23275},
        "industry": "Healthcare / Hospice"
    },
    {
        "company_name": "Suncrest Hospice",
        "decision_maker": {"name": "Team", "email": "info@suncrestcare.com"},
        "potential_savings": {"total": 55860},
        "industry": "Healthcare / Hospice"
    }
]

# Batch 7 - Day 7 Follow-ups (contacted Feb 27, 4:01 PM)
batch_7_day7 = [
    {
        "company_name": "Adecco Staffing",
        "decision_maker": {"name": "Team", "email": "info@adecco.com"},
        "potential_savings": {"total": 124650},
        "industry": "Staffing / HR Services"
    },
    {
        "company_name": "Alive Hospice",
        "decision_maker": {"name": "Team", "email": "info@alivehospice.org"},
        "potential_savings": {"total": 124650},
        "industry": "Healthcare / Hospice"
    },
    {
        "company_name": "Daikin Comfort Technologies",
        "decision_maker": {"name": "Team", "email": "info@daikincomfort.com"},
        "potential_savings": {"total": 166200},
        "industry": "Manufacturing / HVAC"
    }
]

def send_day7_followup(lead_data):
    """Send Day 7 follow-up"""
    subject = f"Quick question about {lead_data.get('company_name', 'Company')}'s benefits strategy"
    
    first_name = lead_data.get("decision_maker", {}).get("name", "there")
    if first_name == "Team":
        first_name = "there"
    else:
        first_name = first_name.split()[0] if first_name else "there"
    
    industry = lead_data.get("industry", "your industry")
    
    text = f"""Hi {first_name},

I'll keep this brief. We've helped similar organizations in {industry} achieve significant savings through the Wellness 125 program:
- Zero cost to implement
- $681 per employee in FICA savings
- 30-60% workers' comp reduction
- 30-60 day implementation

The program is fully compliant, with legal opinions from ERISA counsel and independent accounting review.

Open to seeing how this would work for your team?

Best,
Zane

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info
"""

    html = f"""<p>Hi {first_name},</p>

<p>I'll keep this brief. We've helped similar organizations in {industry} achieve significant savings through the Wellness 125 program:</p>
<ul>
<li>Zero cost to implement</li>
<li>$681 per employee in FICA savings</li>
<li>30-60% workers' comp reduction</li>
<li>30-60 day implementation</li>
</ul>

<p>The program is fully compliant, with legal opinions from ERISA counsel and independent accounting review.</p>

<p>Open to seeing how this would work for your team?</p>

<p>Best,<br>
Zane<br><br>
---<br>
For further information, reach Sam Desigan (Agent Manager)<br>
sam@impactquadrant.info</p>
"""

    return send_email(
        to_email=lead_data.get("decision_maker", {}).get("email", ""),
        subject=subject,
        text_content=text,
        html_content=html,
        cc=CC_EMAIL
    )

def main():
    print("\n" + "="*60)
    print(f"Lead Outreach Report - {datetime.now().strftime('%Y-%m-%d %I:%M %p')}")
    print("="*60 + "\n")
    
    results = {
        "day4_sent": 0,
        "day4_bounced": 0,
        "day7_sent": 0,
        "day7_bounced": 0,
        "total_savings": 0,
        "errors": []
    }
    
    # Send Day 4 follow-ups (Batch 16c)
    print("📧 SENDING DAY 4 FOLLOW-UPS (Batch 16c)")
    print("-" * 40)
    for lead in batch_16c:
        print(f"\n  → {lead['company_name']} (${lead['potential_savings']['total']:,} savings)")
        result = send_follow_up_day4(lead)
        if result['success']:
            print(f"    ✅ Sent! Message ID: {result.get('message_id', 'N/A')}")
            results["day4_sent"] += 1
            results["total_savings"] += lead['potential_savings']['total']
        else:
            print(f"    ❌ BOUNCED: {result.get('error', 'Unknown error')}")
            results["day4_bounced"] += 1
            results["errors"].append(f"{lead['company_name']}: {result.get('error', 'Bounced')}")
    
    # Send Day 7 follow-ups
    print("\n\n📧 SENDING DAY 7 FOLLOW-UPS")
    print("-" * 40)
    
    all_day7 = batch_5_day7 + batch_6_day7 + batch_7_day7
    for lead in all_day7:
        print(f"\n  → {lead['company_name']} (${lead['potential_savings']['total']:,} savings)")
        result = send_day7_followup(lead)
        if result['success']:
            print(f"    ✅ Sent! Message ID: {result.get('message_id', 'N/A')}")
            results["day7_sent"] += 1
            results["total_savings"] += lead['potential_savings']['total']
        else:
            print(f"    ❌ BOUNCED: {result.get('error', 'Unknown error')}")
            results["day7_bounced"] += 1
            results["errors"].append(f"{lead['company_name']}: {result.get('error', 'Bounced')}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    print(f"  Day 4 Follow-ups Sent: {results['day4_sent']}")
    print(f"  Day 4 Follow-ups Bounced: {results['day4_bounced']}")
    print(f"  Day 7 Follow-ups Sent: {results['day7_sent']}")
    print(f"  Day 7 Follow-ups Bounced: {results['day7_bounced']}")
    print(f"  Total Emails Sent: {results['day4_sent'] + results['day7_sent']}")
    print(f"  Total Bounced: {results['day4_bounced'] + results['day7_bounced']}")
    print(f"  Total Potential Savings: ${results['total_savings']:,}/year")
    
    if results['errors']:
        print("\n⚠️ ERRORS:")
        for err in results['errors']:
            print(f"  - {err}")
    
    print("\n" + "="*60 + "\n")
    
    return results

if __name__ == "__main__":
    main()
