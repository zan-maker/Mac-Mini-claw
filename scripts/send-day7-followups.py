#!/usr/bin/env python3
"""
Send Day 7 Follow-ups - March 11, 2026
Batch 10 and 11 (contacted March 4, 2026)
"""

import requests
import json
from datetime import datetime

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

def create_day7_email(company_name, industry, savings_amount, contact_email):
    """Create Day 7 follow-up email"""
    
    # Simplified industry name
    industry_simple = industry.split(" - ")[0] if " - " in industry else industry
    
    subject = f"Quick question about {company_name}'s benefits strategy"
    
    text_content = f"""Hi there,

I'll keep this brief. We've helped similar organizations in {industry_simple} achieve:
- ${savings_amount:,} in annual savings
- $50-$400/month employee pay increase
- 30-60 day implementation

The program is fully compliant, with legal opinions from ERISA counsel and independent accounting review.

Open to seeing how this would work for your team?

Best,
Zane
Zane@agentmail.to
Wellness 125 Cafeteria Plan

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info
"""

    html_content = f"""<p>Hi there,</p>

<p>I'll keep this brief. We've helped similar organizations in {industry_simple} achieve:</p>
<ul>
<li><strong>${savings_amount:,} in annual savings</strong></li>
<li>$50-$400/month employee pay increase</li>
<li>30-60 day implementation</li>
</ul>

<p>The program is fully compliant, with legal opinions from ERISA counsel and independent accounting review.</p>

<p>Open to seeing how this would work for your team?</p>

<p>Best,<br>
Zane<br>
Zane@agentmail.to<br>
Wellness 125 Cafeteria Plan</p>

<p>---<br>
For further information, reach Sam Desigan (Agent Manager)<br>
sam@impactquadrant.info</p>
"""

    return {
        "to": contact_email,
        "subject": subject,
        "text": text_content,
        "html": html_content,
        "cc": CC_EMAIL
    }

# Batch 10 leads (contacted March 4, Day 7 follow-up due March 11)
batch_10_leads = [
    {
        "company_name": "Hospice Care Partners",
        "industry": "Healthcare - Hospice",
        "savings": 99720,
        "email": "hr@hospicecarepartners.com"
    },
    {
        "company_name": "Sunrise Senior Living - Phoenix",
        "industry": "Healthcare - Senior Living",
        "savings": 70635,
        "email": "hr@sunriseseniorliving.com"
    },
    {
        "company_name": "Premier Hotel Group",
        "industry": "Hospitality - Hotels",
        "savings": 124650,
        "email": "hr@premierhotelgroup.com"
    },
    {
        "company_name": "Metro Medical Transport",
        "industry": "Healthcare - Medical Transportation",
        "savings": 37395,
        "email": "hr@metromedicaltransport.com"
    },
    {
        "company_name": "Mountain View Manufacturing",
        "industry": "Manufacturing",
        "savings": 62325,
        "email": "hr@mvmanuf.com"
    }
]

# Batch 11 leads (contacted March 4, Day 7 follow-up due March 11)
batch_11_leads = [
    {
        "company_name": "Coastal Hospice",
        "industry": "Healthcare - Hospice",
        "savings": 66480,
        "email": "hr@coastalhospice.org"
    },
    {
        "company_name": "Heartland Hospice",
        "industry": "Healthcare - Hospice",
        "savings": 124650,
        "email": "hr@heartlandhospice.com"
    },
    {
        "company_name": "Comfort Keepers",
        "industry": "Healthcare - Senior Care",
        "savings": 83100,
        "email": "hr@comfortkeepers.com"
    },
    {
        "company_name": "Grace Hospice",
        "industry": "Healthcare - Hospice",
        "savings": 49860,
        "email": "hr@gracehospice.com"
    },
    {
        "company_name": "Affiliated Hospice",
        "industry": "Healthcare - Hospice",
        "savings": 58170,
        "email": "hr@affiliatedhospice.com"
    }
]

def main():
    print("\n" + "="*60)
    print("Day 7 Follow-ups - March 11, 2026")
    print("Batches 10 & 11 (contacted March 4)")
    print("="*60 + "\n")
    
    all_leads = batch_10_leads + batch_11_leads
    results = {
        "sent": [],
        "bounced": [],
        "errors": []
    }
    
    for lead in all_leads:
        print(f"Sending to {lead['company_name']} ({lead['email']})...")
        
        email_data = create_day7_email(
            company_name=lead["company_name"],
            industry=lead["industry"],
            savings_amount=lead["savings"],
            contact_email=lead["email"]
        )
        
        result = send_email(
            to_email=email_data["to"],
            subject=email_data["subject"],
            text_content=email_data["text"],
            html_content=email_data["html"],
            cc=email_data["cc"]
        )
        
        if result["success"]:
            print(f"  ✅ SENT - Message ID: {result['message_id']}")
            results["sent"].append({
                "company": lead["company_name"],
                "email": lead["email"],
                "savings": lead["savings"],
                "message_id": result["message_id"]
            })
        else:
            error_msg = result.get("error", "Unknown error")
            if "bounce" in error_msg.lower() or "block" in error_msg.lower() or "404" in error_msg or "403" in error_msg:
                print(f"  ❌ BOUNCED - {error_msg}")
                results["bounced"].append({
                    "company": lead["company_name"],
                    "email": lead["email"],
                    "error": error_msg
                })
            else:
                print(f"  ⚠️ ERROR - {error_msg}")
                results["errors"].append({
                    "company": lead["company_name"],
                    "email": lead["email"],
                    "error": error_msg
                })
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total emails sent: {len(results['sent'])}")
    print(f"Total bounced: {len(results['bounced'])}")
    print(f"Total errors: {len(results['errors'])}")
    
    if results["sent"]:
        total_savings = sum(r["savings"] for r in results["sent"])
        print(f"\nTotal potential savings (sent): ${total_savings:,}/year")
    
    print("\n" + "="*60)
    
    # Return results for logging
    return results

if __name__ == "__main__":
    results = main()
