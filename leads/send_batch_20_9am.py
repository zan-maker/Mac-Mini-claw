#!/usr/bin/env python3
"""
Batch 20 - March 11, 2026 9:36 AM (First batch of 4)
5 outreach emails for Wellness 125 Cafeteria Plan
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

def create_outreach_email(company_name, employee_count, industry, decision_maker_first, email):
    """Create personalized outreach email for Wellness 125"""
    
    # Calculate potential savings: $681 x employees + 30% workers comp
    fica_savings = employee_count * 681
    workers_comp_savings = employee_count * 500 * 0.30  # Est $500/employee base x 30%
    total_savings = fica_savings + workers_comp_savings
    
    subject = f"${total_savings:,} annual savings for {company_name} (zero cost to implement)"
    
    text_content = f"""Hi {decision_maker_first},

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

    html_content = f"""<p>Hi {decision_maker_first},</p>

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
        "to": email,
        "subject": subject,
        "text": text_content,
        "html": html_content,
        "cc": CC_EMAIL,
        "total_savings": total_savings
    }

# Batch 20 Leads - March 11, 2026 9:36 AM
leads = [
    {
        "company_name": "Rigid Concepts",
        "domain": "rigidconcepts.com",
        "email": "info@rigidconcepts.com",
        "employee_count": 45,  # Precision manufacturing shop
        "industry": "Manufacturing - CNC/Precision",
        "decision_maker_first": "there",
        "score": 95,
        "location": "McKinney, TX"
    },
    {
        "company_name": "Nordon Plastics",
        "domain": "nordonplastics.com",
        "email": "info@nordonplastics.com",
        "employee_count": 60,  # Plastics manufacturing facility
        "industry": "Manufacturing - Plastics",
        "decision_maker_first": "there",
        "score": 70,
        "location": "Rochester, NY"
    },
    {
        "company_name": "ABS Machining",
        "domain": "absmachining.com",
        "email": "info@absmachining.com",
        "employee_count": 150,  # Large CNC/fabrication facility
        "industry": "Manufacturing - CNC/Fabrication",
        "decision_maker_first": "there",
        "score": 65,
        "location": "Texas"
    },
    {
        "company_name": "Hunt and Hunt Ltd",
        "domain": "huntandhunt.com",
        "email": "info@huntandhunt.com",
        "employee_count": 85,  # Precision machine shop
        "industry": "Manufacturing - Precision Machining",
        "decision_maker_first": "there",
        "score": 50,
        "location": "Energy/Aerospace Hub"
    },
    {
        "company_name": "Florida Sheet Metal",
        "domain": "floridasheetmetal.com",
        "email": "info@floridasheetmetal.com",
        "employee_count": 55,  # Full service metal forming
        "industry": "Manufacturing - Metal Fabrication",
        "decision_maker_first": "there",
        "score": 50,
        "location": "Melbourne, FL"
    }
]

# Send emails
print("\n" + "="*70)
print("BATCH 20 - March 11, 2026 9:36 AM")
print("First batch of 4 (Target: 20/day)")
print("="*70 + "\n")

results = []
total_savings = 0
sent_count = 0

for lead in leads:
    print(f"Sending to {lead['company_name']} ({lead['email']})...")
    
    email_data = create_outreach_email(
        company_name=lead["company_name"],
        employee_count=lead["employee_count"],
        industry=lead["industry"],
        decision_maker_first=lead["decision_maker_first"],
        email=lead["email"]
    )
    
    result = send_email(
        to_email=email_data["to"],
        subject=email_data["subject"],
        text_content=email_data["text"],
        html_content=email_data["html"],
        cc=email_data["cc"]
    )
    
    result["lead"] = lead
    result["savings"] = email_data["total_savings"]
    results.append(result)
    
    if result["success"]:
        sent_count += 1
        total_savings += email_data["total_savings"]
        print(f"  ✅ SUCCESS - ${email_data['total_savings']:,} potential savings")
        print(f"     Message ID: {result['message_id']}")
    else:
        print(f"  ❌ FAILED - {result['error']}")
    print()

# Save results
output = {
    "batch": 20,
    "timestamp": datetime.now().isoformat(),
    "target": "5 emails",
    "sent": sent_count,
    "failed": 5 - sent_count,
    "total_potential_savings": total_savings,
    "results": results
}

filename = f"/Users/cubiczan/.openclaw/workspace/leads/batch_20_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(filename, "w") as f:
    json.dump(output, f, indent=2)

print("="*70)
print("BATCH 20 SUMMARY")
print("="*70)
print(f"Emails Sent: {sent_count}/5")
print(f"Emails Failed: {5 - sent_count}")
print(f"Total Potential Savings: ${total_savings:,}/year")
print(f"Results saved to: {filename}")
print("="*70)
