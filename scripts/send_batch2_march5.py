#!/usr/bin/env python3
"""
Batch 2 Outreach - March 5, 2026 (11:00 AM)
Sends 5 outreach emails from daily leads
"""

import requests
import json

# AgentMail Configuration
AGENTMAIL_API_KEY = "am_us_f03e762c50d6e353bbe7b4307b452bd73f58aed725bc0ef53f25d9f8e91c962a"
AGENTMAIL_INBOX = "zane@agentmail.to"
FROM_EMAIL = "zane@agentmail.to"
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

# Companies extracted from daily-leads-2026-03-05.md
leads = [
    {
        "company_name": "Breakthru Beverage Group",
        "employees": 10000,
        "email": "hr@breakthrubev.com",
        "industry": "Wine and Spirits Distribution",
        "location": "New York"
    },
    {
        "company_name": "TECO-Westinghouse",
        "employees": 750,
        "email": "hr@tecowestinghouse.com",
        "industry": "Electrical & Electronic Manufacturing",
        "location": "Round Rock, Texas"
    },
    {
        "company_name": "Powell",
        "employees": 7500,
        "email": "hr@powellind.com",
        "industry": "Electrical & Electronic Manufacturing",
        "location": "Houston, Texas"
    },
    {
        "company_name": "Orlando Health",
        "employees": 10001,
        "email": "hr@orlandohealth.com",
        "industry": "Healthcare",
        "location": "Orlando, Florida"
    },
    {
        "company_name": "Communications & Power Industries",
        "employees": 7500,
        "email": "hr@cpi.com",
        "industry": "Electrical & Electronic Manufacturing",
        "location": "Plano, Texas"
    }
]

def calculate_savings(employee_count):
    """Calculate potential annual savings"""
    fica_savings = employee_count * 681
    workers_comp_savings = employee_count * 500 * 0.30
    total_savings = fica_savings + workers_comp_savings
    return total_savings

def create_email(lead):
    """Create personalized outreach email"""
    company = lead["company_name"]
    employees = lead["employees"]
    industry = lead["industry"]
    location = lead["location"]
    
    total_savings = calculate_savings(employees)
    
    subject = f"${total_savings:,} annual savings for {company} (zero cost to implement)"
    
    text = f"""Hi there,

I noticed {company} has about {employees:,} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.

Organizations your size are typically saving:
• $681 per employee annually in FICA savings
• 30-60% reduction in workers' comp premiums
• Total savings: ${total_savings:,}

One medical transportation company with 66 employees saved over $140,000 last year.

The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.

Would you be open to a 10-minute call this week to see the numbers for {company}?

Best,
Zane
Zane@agentmail.to
Wellness 125 Cafeteria Plan
"""

    html = f"""<p>Hi there,</p>

<p>I noticed {company} has about {employees:,} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.</p>

<p><strong>Organizations your size are typically saving:</strong></p>
<ul>
<li>$681 per employee annually in FICA savings</li>
<li>30-60% reduction in workers' comp premiums</li>
<li><strong>Total savings: ${total_savings:,}</strong></li>
</ul>

<p>One medical transportation company with 66 employees saved over $140,000 last year.</p>

<p>The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.</p>

<p>Would you be open to a 10-minute call this week to see the numbers for {company}?</p>

<p>Best,<br>
Zane<br>
Zane@agentmail.to<br>
Wellness 125 Cafeteria Plan</p>
"""
    
    return {
        "to": lead["email"],
        "subject": subject,
        "text": text,
        "html": html
    }

def main():
    print("\n" + "="*60)
    print("BATCH 2 OUTREACH - March 5, 2026 (11:00 AM)")
    print("="*60 + "\n")
    
    results = []
    
    for lead in leads:
        print(f"Sending to: {lead['company_name']} ({lead['employees']:,} employees)")
        print(f"  Email: {lead['email']}")
        print(f"  Industry: {lead['industry']}")
        
        email_data = create_email(lead)
        
        result = send_email(
            to_email=email_data["to"],
            subject=email_data["subject"],
            text_content=email_data["text"],
            html_content=email_data["html"],
            cc=CC_EMAIL
        )
        
        if result['success']:
            total_savings = calculate_savings(lead['employees'])
            print(f"  ✅ SENT - Message ID: {result['message_id']}")
            print(f"  Est. Savings: ${total_savings:,}/year\n")
            results.append({
                "company": lead['company_name'],
                "success": True,
                "message_id": result['message_id'],
                "savings": total_savings
            })
        else:
            print(f"  ❌ FAILED - {result['error']}\n")
            results.append({
                "company": lead['company_name'],
                "success": False,
                "error": result['error']
            })
    
    # Summary
    print("="*60)
    print("BATCH 2 SUMMARY")
    print("="*60)
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"\n✅ Emails Sent: {len(successful)}/5")
    print(f"❌ Failed: {len(failed)}/5")
    
    if successful:
        total_potential = sum(r['savings'] for r in successful)
        print(f"\n💰 Total Potential Annual Savings: ${total_potential:,}")
    
    print(f"\n🎯 Daily Progress: 10/20 (Batch 2 of 4 complete)")
    print(f"   Batch 1 (9:43 AM): 5 sent")
    print(f"   Batch 2 (11:00 AM): {len(successful)} sent")
    print(f"   Remaining: 10 emails (2 batches)")
    
    print("\n" + "="*60 + "\n")
    
    return results

if __name__ == "__main__":
    main()
