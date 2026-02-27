#!/usr/bin/env python3
"""
Batch 3 Outreach - 2:00 PM - 5 emails
Wellness 125 Cafeteria Plan
"""

import requests
import json

# AgentMail Configuration
AGENTMAIL_API_KEY = "am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
AGENTMAIL_INBOX = "zane@agentmail.to"
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

# Companies to contact
companies = [
    {
        "name": "Hospice & Palliative Care",
        "email": "Info@hospicecareinc.org",
        "employees": 40,
        "industry": "Healthcare / Hospice",
        "location": "New Hartford, NY"
    },
    {
        "name": "HospiceCare",
        "email": "info@hospicecarewv.org",
        "employees": 85,
        "industry": "Healthcare / Hospice",
        "location": "Charleston, WV"
    },
    {
        "name": "SoCal Premium Hospice",
        "email": "info@socalpremiumhospice.com",
        "employees": 35,
        "industry": "Healthcare / Hospice",
        "location": "Encino, CA"
    },
    {
        "name": "North Hawaii Hospice",
        "email": "info@northhawaiihospice.org",
        "employees": 25,
        "industry": "Healthcare / Hospice",
        "location": "Kamuela, HI"
    },
    {
        "name": "Suncrest Hospice",
        "email": "info@suncrestcare.com",
        "employees": 60,
        "industry": "Healthcare / Hospice",
        "location": "Phoenix, AZ"
    }
]

def create_email(company):
    """Create personalized outreach email"""
    
    # Calculate savings
    fica_savings = company["employees"] * 681
    workers_comp_savings = company["employees"] * 500 * 0.30
    total_savings = fica_savings + workers_comp_savings
    
    subject = f"${total_savings:,} annual savings for {company['name']} (zero cost to implement)"
    
    text = f"""Hi there,

I noticed {company['name']} has about {company['employees']} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.

Organizations your size are typically saving:
• $681 per employee annually in FICA savings
• 30-60% reduction in workers' comp premiums
• Total savings: ${total_savings:,}

One medical transportation company with 66 employees saved over $140,000 last year.

The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.

Would you be open to a 10-minute call this week to see the numbers for {company['name']}?

Best,
Zane
Zane@agentmail.to
Wellness 125 Cafeteria Plan
"""

    html = f"""<p>Hi there,</p>

<p>I noticed {company['name']} has about {company['employees']} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.</p>

<p><strong>Organizations your size are typically saving:</strong></p>
<ul>
<li>$681 per employee annually in FICA savings</li>
<li>30-60% reduction in workers' comp premiums</li>
<li><strong>Total savings: ${total_savings:,}</strong></li>
</ul>

<p>One medical transportation company with 66 employees saved over $140,000 last year.</p>

<p>The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.</p>

<p>Would you be open to a 10-minute call this week to see the numbers for {company['name']}?</p>

<p>Best,<br>
Zane<br>
Zane@agentmail.to<br>
Wellness 125 Cafeteria Plan</p>
"""

    return {
        "to": company["email"],
        "subject": subject,
        "text": text,
        "html": html
    }

def main():
    print("\n" + "="*60)
    print("Batch 3 Outreach - 2:00 PM")
    print("Target: 5 emails")
    print("="*60 + "\n")
    
    results = []
    
    for i, company in enumerate(companies, 1):
        print(f"\n[{i}/5] Sending to {company['name']}...")
        print(f"  Email: {company['email']}")
        print(f"  Employees: {company['employees']}")
        print(f"  Industry: {company['industry']}")
        
        email_data = create_email(company)
        
        result = send_email(
            to_email=email_data["to"],
            subject=email_data["subject"],
            text_content=email_data["text"],
            html_content=email_data["html"],
            cc="sam@impactquadrant.info"
        )
        
        if result["success"]:
            print(f"  ✅ SUCCESS - Message ID: {result['message_id']}")
            results.append({
                "company": company["name"],
                "email": company["email"],
                "message_id": result["message_id"],
                "status": "sent"
            })
        else:
            print(f"  ❌ FAILED - {result['error']}")
            results.append({
                "company": company["name"],
                "email": company["email"],
                "error": result["error"],
                "status": "failed"
            })
    
    print("\n" + "="*60)
    print("BATCH SUMMARY")
    print("="*60)
    
    success_count = sum(1 for r in results if r["status"] == "sent")
    failed_count = sum(1 for r in results if r["status"] == "failed")
    
    print(f"\n✅ Sent: {success_count}/{len(companies)}")
    print(f"❌ Failed: {failed_count}/{len(companies)}")
    
    if success_count > 0:
        print("\n📧 Successfully sent to:")
        for r in results:
            if r["status"] == "sent":
                print(f"  - {r['company']} ({r['email']})")
                print(f"    Message ID: {r['message_id']}")
    
    if failed_count > 0:
        print("\n⚠️ Failed to send to:")
        for r in results:
            if r["status"] == "failed":
                print(f"  - {r['company']} ({r['email']})")
                print(f"    Error: {r['error']}")
    
    print("\n" + "="*60 + "\n")
    
    return results

if __name__ == "__main__":
    main()
