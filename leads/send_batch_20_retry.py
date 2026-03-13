#!/usr/bin/env python3
"""
Batch 20 Retry - Send 5 queued outreach emails
Date: March 12, 2026 4:00 PM (Batch 4 of 4)
"""

import requests
import json
from datetime import datetime
from pathlib import Path

# AgentMail Configuration
AGENTMAIL_API_KEY = "am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
AGENTMAIL_INBOX = "zane@agentmail.to"
CC_EMAIL = "sam@impactquadrant.info"
BASE_URL = "https://api.agentmail.to/v0"

# Queued leads from failed Batch 20
QUEUED_LEADS = [
    {
        "company_name": "Rigid Concepts",
        "email": "info@rigidconcepts.com",
        "employee_count": 45,
        "industry": "Manufacturing - CNC/Precision",
        "location": "McKinney, TX",
        "score": 95
    },
    {
        "company_name": "Nordon Plastics",
        "email": "info@nordonplastics.com",
        "employee_count": 60,
        "industry": "Manufacturing - Plastics",
        "location": "Rochester, NY",
        "score": 70
    },
    {
        "company_name": "ABS Machining",
        "email": "info@absmachining.com",
        "employee_count": 150,
        "industry": "Manufacturing - CNC/Fabrication",
        "location": "Texas",
        "score": 65
    },
    {
        "company_name": "Hunt and Hunt Ltd",
        "email": "info@huntandhunt.com",
        "employee_count": 85,
        "industry": "Manufacturing - Precision Machining",
        "location": "Energy/Aerospace Hub",
        "score": 50
    },
    {
        "company_name": "Florida Sheet Metal",
        "email": "info@floridasheetmetal.com",
        "employee_count": 55,
        "industry": "Manufacturing - Metal Fabrication",
        "location": "Melbourne, FL",
        "score": 50
    }
]

def calculate_savings(employee_count):
    """Calculate total annual savings"""
    fica_savings = employee_count * 681
    workers_comp_savings = employee_count * 500 * 0.30
    return fica_savings + workers_comp_savings

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

    # Add HTML version if provided
    if html_content:
        payload["html"] = html_content

    # Add CC if provided
    if cc:
        payload["cc"] = [cc] if isinstance(cc, str) else cc

    try:
        # Correct endpoint: /v0/inboxes/{inbox_id}/messages/send
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

def create_email_content(lead):
    """Create personalized email for a lead"""
    savings = calculate_savings(lead["employee_count"])
    
    subject = f"${int(savings):,} annual savings for {lead['company_name']} (zero cost to implement)"
    
    text = f"""Hi there,

I noticed {lead['company_name']} has about {lead['employee_count']} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.

Organizations your size are typically saving:
• $681 per employee annually in FICA savings
• 30-60% reduction in workers' comp premiums
• Total savings: ${int(savings):,}

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

    html = f"""<p>Hi there,</p>

<p>I noticed {lead['company_name']} has about {lead['employee_count']} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.</p>

<p><strong>Organizations your size are typically saving:</strong></p>
<ul>
<li>$681 per employee annually in FICA savings</li>
<li>30-60% reduction in workers' comp premiums</li>
<li><strong>Total savings: ${int(savings):,}</strong></li>
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

    return subject, text, html, savings

def send_batch():
    """Send outreach emails to queued leads"""
    print("\n" + "="*70)
    print("BATCH 20 RETRY - Wellness 125 Outreach")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}")
    print("="*70 + "\n")
    
    results = {
        "batch": "20_retry",
        "timestamp": datetime.now().isoformat(),
        "target": "5 emails",
        "sent": 0,
        "failed": 0,
        "total_potential_savings": 0,
        "results": []
    }
    
    for i, lead in enumerate(QUEUED_LEADS, 1):
        print(f"\n[{i}/5] Sending to: {lead['company_name']}")
        print(f"  Email: {lead['email']}")
        print(f"  Employees: {lead['employee_count']}")
        print(f"  Location: {lead['location']}")
        
        subject, text, html, savings = create_email_content(lead)
        
        print(f"  Subject: {subject}")
        print(f"  Est. Savings: ${int(savings):,}/year")
        print(f"  From: {AGENTMAIL_INBOX}")
        print(f"  CC: {CC_EMAIL}")
        
        # Send email
        result = send_email(
            to_email=lead['email'],
            subject=subject,
            text_content=text,
            html_content=html,
            cc=CC_EMAIL
        )
        
        result_data = {
            "lead": lead,
            "savings": savings,
            "success": result.get("success", False),
            "error": result.get("error"),
            "message_id": result.get("message_id")
        }
        
        results["results"].append(result_data)
        
        if result.get("success"):
            results["sent"] += 1
            results["total_potential_savings"] += savings
            print(f"  ✅ SUCCESS - Message ID: {result.get('message_id')}")
        else:
            results["failed"] += 1
            print(f"  ❌ FAILED - {result.get('error')}")
    
    # Summary
    print("\n" + "="*70)
    print("BATCH SUMMARY")
    print("="*70)
    print(f"  Sent: {results['sent']}/5")
    print(f"  Failed: {results['failed']}/5")
    print(f"  Total Potential Savings: ${int(results['total_potential_savings']):,}/year")
    print("="*70 + "\n")
    
    # Save results
    output_file = Path(__file__).parent / f"batch_20_retry_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to: {output_file}\n")
    
    return results

if __name__ == "__main__":
    import sys
    results = send_batch()
    
    # Exit with error code if any failed
    sys.exit(0 if results["failed"] == 0 else 1)
