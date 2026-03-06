#!/usr/bin/env python3
"""
Wellness 125 Outreach - March 5, 2026 (9 AM Batch)
Sends 5 initial outreach emails via AgentMail API
FROM: Zane@agentmail.to
CC: sam@impactquadrant.info
"""

import requests
import json
from datetime import datetime

# AgentMail Configuration
API_KEY = "am_us_f03e762c50d6e353bbe7b4307b452bd73f58aed725bc0ef53f25d9f8e91c962a"
FROM_EMAIL = "zane@agentmail.to"
FROM_NAME = "Zane"
CC_EMAIL = "sam@impactquadrant.info"
BASE_URL = "https://api.agentmail.to/v0"

# Today's NEW high-priority leads (not yet contacted)
# Selected from industries with 20+ employees that fit the Wellness 125 profile
NEW_LEADS = [
    {
        "company": "Bloomberg LP",
        "industry": "Business/Financial Information",
        "employees": 20000,
        "location": "New York, NY",
        "email": "hr@bloomberg.net",
        "estimated_savings": 1662000,  # $681 * 20000 + 30% workers comp
        "score": 100
    },
    {
        "company": "Hearst Corporation",
        "industry": "Media/Information Services",
        "employees": 22190,
        "location": "New York, NY",
        "email": "hr@hearst.com",
        "estimated_savings": 1839339,
        "score": 100
    },
    {
        "company": "STO Building Group",
        "industry": "Construction Management",
        "employees": 5300,
        "location": "New York, NY",
        "email": "hr@stobuildinggroup.com",
        "estimated_savings": 438990,
        "score": 95
    },
    {
        "company": "Standard Industries",
        "industry": "Industrial/Building Materials",
        "employees": 20000,
        "location": "New York, NY",
        "email": "hr@standardindustries.com",
        "estimated_savings": 1662000,
        "score": 95
    },
    {
        "company": "Horizon Media Inc",
        "industry": "Media/Marketing Services",
        "employees": 2400,
        "location": "New York, NY",
        "email": "hr@horizonmedia.com",
        "estimated_savings": 198720,
        "score": 90
    }
]

def calculate_savings(employees):
    """Calculate estimated annual savings"""
    fica_savings = employees * 681
    # Estimate workers comp at 30% of FICA for rough calculation
    workers_comp_savings = fica_savings * 0.30
    total = fica_savings + workers_comp_savings
    return int(total)

def create_email_content(lead):
    """Generate personalized email content"""
    company = lead["company"]
    employees = lead["employees"]
    savings = lead["estimated_savings"]
    industry = lead["industry"]
    
    # Format savings as currency
    savings_formatted = f"${savings:,}"
    
    # Subject line with specific savings amount
    subject = f"{savings_formatted} annual savings for {company}"
    
    # Plain text body
    text_body = f"""Hi,

I noticed {company} has about {employees:,} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.

Organizations your size are typically saving:
• $681 per employee annually in FICA savings
• 30-60% reduction in workers' comp premiums
• Total savings: {savings_formatted}/year

One medical transportation company with 66 employees saved over $140,000 last year.

The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.

Would you be open to a 10-minute call this week to see the numbers for {company}?

Best,
Zane
Zane@agentmail.to
Wellness 125 Cafeteria Plan

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info
"""
    
    # HTML body
    html_body = f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<p>Hi,</p>

<p>I noticed <strong>{company}</strong> has about <strong>{employees:,} employees</strong>, which positions you for significant annual savings through a compliant Section 125 wellness program.</p>

<p><strong>Organizations your size are typically saving:</strong></p>
<ul>
<li>$681 per employee annually in FICA savings</li>
<li>30-60% reduction in workers' comp premiums</li>
<li><strong>Total savings: {savings_formatted}/year</strong></li>
</ul>

<p>One medical transportation company with 66 employees saved over $140,000 last year.</p>

<p>The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at <strong>zero cost to you or your employees</strong>.</p>

<p>Would you be open to a 10-minute call this week to see the numbers for {company}?</p>

<p>Best,<br>
Zane<br>
Zane@agentmail.to<br>
Wellness 125 Cafeteria Plan</p>

<hr style="border: none; border-top: 1px solid #ccc; margin: 20px 0;">

<p style="font-size: 12px; color: #666;">For further information, reach Sam Desigan (Agent Manager)<br>
<a href="mailto:sam@impactquadrant.info">sam@impactquadrant.info</a></p>
</body>
</html>
"""
    
    return subject, text_body, html_body

def send_email(to_email, subject, text_body, html_body):
    """Send email via AgentMail API"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inbox_id": FROM_EMAIL,
        "to": [to_email],
        "cc": [CC_EMAIL],
        "subject": subject,
        "text": text_body,
        "html": html_body
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/inboxes/{FROM_EMAIL}/messages/send",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "message_id": result.get("message_id", "No ID returned"),
                "status": "sent"
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text[:200]}",
                "status": "failed"
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "status": "failed"
        }

def main():
    print("=" * 70)
    print("WELLNESS 125 OUTREACH - March 5, 2026 (9:00 AM Batch)")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"From: {FROM_NAME} <{FROM_EMAIL}>")
    print(f"CC: {CC_EMAIL}")
    print(f"New leads to contact: {len(NEW_LEADS)}")
    print(f"Target: 5 emails (Batch 1 of 4)")
    print()
    
    results = {
        "sent": 0,
        "failed": 0,
        "total": len(NEW_LEADS),
        "emails": [],
        "total_savings": 0
    }
    
    for i, lead in enumerate(NEW_LEADS, 1):
        print(f"\n[{i}/{len(NEW_LEADS)}] {lead['company']}")
        print(f"   Industry: {lead['industry']}")
        print(f"   Location: {lead['location']}")
        print(f"   Employees: {lead['employees']:,}")
        print(f"   Potential savings: ${lead['estimated_savings']:,}/year")
        print(f"   Email: {lead['email']}")
        print(f"   Score: {lead['score']}/100")
        
        # Generate email content
        subject, text_body, html_body = create_email_content(lead)
        print(f"   Subject: {subject}")
        
        # Send email
        print(f"   Sending...", end=" ")
        result = send_email(lead["email"], subject, text_body, html_body)
        
        if result["success"]:
            print(f"✅ SENT - Message ID: {result['message_id'][:50]}...")
            results["sent"] += 1
            results["total_savings"] += lead["estimated_savings"]
            results["emails"].append({
                "company": lead["company"],
                "email": lead["email"],
                "savings": lead["estimated_savings"],
                "message_id": result["message_id"],
                "status": "sent",
                "timestamp": datetime.now().isoformat()
            })
        else:
            print(f"❌ FAILED: {result['error'][:100]}")
            results["failed"] += 1
            results["emails"].append({
                "company": lead["company"],
                "email": lead["email"],
                "savings": lead["estimated_savings"],
                "error": result["error"],
                "status": "failed",
                "timestamp": datetime.now().isoformat()
            })
    
    # Print summary
    print("\n" + "=" * 70)
    print("BATCH SUMMARY")
    print("=" * 70)
    print(f"Total leads: {results['total']}")
    print(f"✅ Sent: {results['sent']}")
    print(f"❌ Failed: {results['failed']}")
    if results['total_savings'] > 0:
        print(f"Total potential savings: ${results['total_savings']:,}/year")
    print(f"Daily progress: {results['sent']}/20 emails sent")
    print(f"Remaining today: {20 - results['sent']} emails")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"/Users/cubiczan/.openclaw/workspace/outreach-results/wellness_outreach_2026-03-05_9am_{timestamp}.json"
    
    with open(log_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "batch": "9am",
            "type": "initial_outreach",
            "from": FROM_EMAIL,
            "cc": CC_EMAIL,
            "results": results
        }, f, indent=2)
    
    print(f"\nResults saved: {log_file}")
    print("=" * 70)
    
    return results

if __name__ == "__main__":
    main()
