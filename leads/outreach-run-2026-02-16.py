#!/usr/bin/env python3
"""
Outreach Run - 2026-02-16 2:00 PM
Sends initial outreach to HIGH priority leads via AgentMail
"""

import requests
import json
from datetime import datetime

# AgentMail Configuration
AGENTMAIL_API_KEY = "am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
AGENTMAIL_INBOX = "Zane@agentmail.to"
CC_EMAIL = "sam@impactquadrant.info"
BASE_URL = "https://api.agentmail.to/v0"

# HIGH Priority Leads (Score 70+)
HIGH_PRIORITY_LEADS = [
    {
        "company_name": "Hospice Care Partners",
        "industry": "Healthcare - Hospice",
        "employees_count": 120,
        "location": "Atlanta, GA",
        "decision_maker": {
            "name": "HR Director",
            "email": "hr@hospicecarepartners.com"
        },
        "potential_savings": {
            "fica": 81720,
            "workers_comp": 18000,
            "total": 99720
        }
    },
    {
        "company_name": "Sunrise Senior Living - Phoenix",
        "industry": "Healthcare - Senior Living",
        "employees_count": 85,
        "location": "Phoenix, AZ",
        "decision_maker": {
            "name": "HR Director",
            "email": "hr@sunriseseniorliving.com"
        },
        "potential_savings": {
            "fica": 57885,
            "workers_comp": 12750,
            "total": 70635
        }
    },
    {
        "company_name": "Premier Hotel Group",
        "industry": "Hospitality - Hotels",
        "employees_count": 150,
        "location": "Orlando, FL",
        "decision_maker": {
            "name": "HR Director",
            "email": "hr@premierhotelgroup.com"
        },
        "potential_savings": {
            "fica": 102150,
            "workers_comp": 22500,
            "total": 124650
        }
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
            f"{BASE_URL}/inboxes/{AGENTMAIL_INBOX}/messages",
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

def create_outreach_email(lead):
    """Create personalized outreach email"""
    
    company_name = lead["company_name"]
    employee_count = lead["employees_count"]
    total_savings = lead["potential_savings"]["total"]
    first_name = lead["decision_maker"]["name"].split()[0]
    to_email = lead["decision_maker"]["email"]
    
    subject = f"${total_savings:,} annual savings for {company_name} (zero cost to implement)"
    
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
        "to": to_email,
        "subject": subject,
        "text": text_content,
        "html": html_content,
        "cc": CC_EMAIL
    }

def main():
    print("\n" + "="*60)
    print("Lead Outreach - AgentMail")
    print(f"Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    results = {
        "sent": 0,
        "errors": 0,
        "emails": []
    }
    
    for lead in HIGH_PRIORITY_LEADS:
        company = lead["company_name"]
        email_data = create_outreach_email(lead)
        
        print(f"Sending to: {company}")
        print(f"  To: {email_data['to']}")
        print(f"  CC: {email_data['cc']}")
        print(f"  Subject: {email_data['subject']}")
        
        result = send_email(
            to_email=email_data["to"],
            subject=email_data["subject"],
            text_content=email_data["text"],
            html_content=email_data["html"],
            cc=email_data["cc"]
        )
        
        if result["success"]:
            print(f"  ✅ Sent! Message ID: {result['message_id']}")
            results["sent"] += 1
            results["emails"].append({
                "company": company,
                "to": email_data["to"],
                "message_id": result["message_id"],
                "status": "sent"
            })
        else:
            print(f"  ❌ Error: {result['error']}")
            results["errors"] += 1
            results["emails"].append({
                "company": company,
                "to": email_data["to"],
                "error": result["error"],
                "status": "error"
            })
        
        print()
    
    print("="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Emails Sent: {results['sent']}")
    print(f"Errors: {results['errors']}")
    print(f"Total Processed: {len(HIGH_PRIORITY_LEADS)}")
    print("="*60 + "\n")
    
    # Save results
    with open("/Users/cubiczan/.openclaw/workspace/leads/outreach-results-2026-02-16.json", "w") as f:
        json.dump({
            "run_time": datetime.now().isoformat(),
            "summary": results,
            "leads_processed": HIGH_PRIORITY_LEADS
        }, f, indent=2)
    
    return results

if __name__ == "__main__":
    main()
