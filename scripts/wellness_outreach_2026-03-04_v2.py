#!/usr/bin/env python3
"""
Wellness 125 Outreach - March 4, 2026
Sends initial outreach to high-priority leads via AgentMail
Using verified API keys from config
"""

import requests
import json
from datetime import datetime

# AgentMail Configuration - Using verified keys from config
API_KEY = "am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f"
FROM_EMAIL = "sam@impactquadrant.info"
FROM_NAME = "Sam Desigan"
CC_EMAIL = "sam@impactquadrant.info"
BASE_URL = "https://api.agentmail.to/v0"

# Today's high-priority leads (score 70+)
HIGH_PRIORITY_LEADS = [
    {
        "company": "Hospice Care Partners",
        "industry": "Healthcare - Hospice",
        "employees": 120,
        "location": "Atlanta, GA",
        "email": "hr@hospicecarepartners.com",
        "savings": 99720,
        "score": 75
    },
    {
        "company": "Sunrise Senior Living - Phoenix",
        "industry": "Healthcare - Senior Living",
        "employees": 85,
        "location": "Phoenix, AZ",
        "email": "hr@sunriseseniorliving.com",
        "savings": 70635,
        "score": 70
    },
    {
        "company": "Premier Hotel Group",
        "industry": "Hospitality - Hotels",
        "employees": 150,
        "location": "Orlando, FL",
        "email": "hr@premierhotelgroup.com",
        "savings": 124650,
        "score": 70
    }
]

def create_email_content(lead):
    """Generate personalized email content"""
    company = lead["company"]
    employees = lead["employees"]
    savings = lead["savings"]
    industry = lead["industry"]
    
    # Format savings as currency
    savings_formatted = f"${savings:,}"
    
    # Subject line
    subject = f"{savings_formatted} annual savings for {company}"
    
    # Plain text body
    text_body = f"""Hi,

I noticed {company} has about {employees} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.

Organizations your size in the {industry} sector are typically saving:
- $681 per employee annually in FICA savings
- 30-60% reduction in workers' comp premiums
- Total savings: {savings_formatted}/year

The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.

Would you be open to a 10-minute call this week to see the numbers for {company}?

Best,
Zane

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info
"""
    
    # HTML body
    html_body = f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<p>Hi,</p>

<p>I noticed <strong>{company}</strong> has about <strong>{employees} employees</strong>, which positions you for significant annual savings through a compliant Section 125 wellness program.</p>

<p>Organizations your size in the {industry} sector are typically saving:</p>
<ul>
<li><strong>$681 per employee annually</strong> in FICA savings</li>
<li><strong>30-60% reduction</strong> in workers' comp premiums</li>
<li><strong>Total savings: {savings_formatted}/year</strong></li>
</ul>

<p>The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at <strong>zero cost to you or your employees</strong>.</p>

<p>Would you be open to a 10-minute call this week to see the numbers for {company}?</p>

<p>Best,<br>
Zane</p>

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
    print("=" * 60)
    print("WELLNESS 125 OUTREACH - March 4, 2026")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"From: {FROM_EMAIL}")
    print(f"CC: {CC_EMAIL}")
    print(f"High-priority leads: {len(HIGH_PRIORITY_LEADS)}")
    print()
    
    results = {
        "sent": 0,
        "failed": 0,
        "total": len(HIGH_PRIORITY_LEADS),
        "emails": [],
        "total_savings": 0
    }
    
    for i, lead in enumerate(HIGH_PRIORITY_LEADS, 1):
        print(f"\n[{i}/{len(HIGH_PRIORITY_LEADS)}] {lead['company']}")
        print(f"   Industry: {lead['industry']}")
        print(f"   Employees: {lead['employees']}")
        print(f"   Potential savings: ${lead['savings']:,}/year")
        print(f"   Email: {lead['email']}")
        
        # Generate email content
        subject, text_body, html_body = create_email_content(lead)
        print(f"   Subject: {subject}")
        
        # Send email
        print(f"   Sending...", end=" ")
        result = send_email(lead["email"], subject, text_body, html_body)
        
        if result["success"]:
            print(f"✅ SENT")
            results["sent"] += 1
            results["total_savings"] += lead["savings"]
            results["emails"].append({
                "company": lead["company"],
                "email": lead["email"],
                "savings": lead["savings"],
                "message_id": result["message_id"],
                "status": "sent",
                "timestamp": datetime.now().isoformat()
            })
        else:
            print(f"❌ FAILED: {result['error']}")
            results["failed"] += 1
            results["emails"].append({
                "company": lead["company"],
                "email": lead["email"],
                "savings": lead["savings"],
                "error": result["error"],
                "status": "failed",
                "timestamp": datetime.now().isoformat()
            })
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total leads: {results['total']}")
    print(f"✅ Sent: {results['sent']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"💰 Total potential savings: ${results['total_savings']:,}/year")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"/Users/cubiczan/.openclaw/workspace/outreach-results/wellness_outreach_{timestamp}.json"
    
    with open(log_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "type": "initial_outreach",
            "results": results
        }, f, indent=2)
    
    print(f"\n📁 Results saved: {log_file}")
    print("=" * 60)
    
    return results

if __name__ == "__main__":
    main()
