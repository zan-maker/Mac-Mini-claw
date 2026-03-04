#!/usr/bin/env python3
"""
Quick Outreach - 4 PM Batch
Generates 5 qualified leads and sends outreach immediately
"""

import requests
import json
from datetime import datetime

# Configuration
AGENTMAIL_API_KEY = "am_us_f03e762c50d6e353bbe7b4307b452bd73f58aed725bc0ef53f25d9f8e91c962a"
AGENTMAIL_INBOX = "zane@agentmail.to"
HUNTER_API_KEY = "f701d171cf7decf7e730a6b1c6e9b74f29f39b6e"
CC_EMAIL = "sam@impactquadrant.info"

# Target companies for quick outreach
TARGET_COMPANIES = [
    {"name": "Coastal Hospice", "domain": "coastalhospice.org", "industry": "Healthcare - Hospice", "employees": 80, "location": "Maryland"},
    {"name": "Heartland Hospice", "domain": "heartlandhospice.com", "industry": "Healthcare - Hospice", "employees": 150, "location": "Multi-location"},
    {"name": "Comfort Keepers", "domain": "comfortkeepers.com", "industry": "Healthcare - Senior Care", "employees": 100, "location": "Multi-location"},
    {"name": "Grace Hospice", "domain": "gracehospice.com", "industry": "Healthcare - Hospice", "employees": 60, "location": "Ohio"},
    {"name": "Affiliated Hospice", "domain": "affiliatedhospice.com", "industry": "Healthcare - Hospice", "employees": 70, "location": "Multi-location"},
]

def find_email_hunter(domain):
    """Find email using Hunter.io API"""
    try:
        url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={HUNTER_API_KEY}"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            emails = data.get('data', {}).get('emails', [])
            
            # Find HR or generic email
            for email_data in emails:
                email = email_data.get('value', '')
                if 'hr@' in email or 'info@' in email or 'contact@' in email:
                    return email
            
            # Return first email if found
            if emails:
                return emails[0].get('value', f'hr@{domain}')
        
        # Fallback to generic email
        return f"hr@{domain}"
    except Exception as e:
        print(f"  ⚠️ Hunter error: {e}")
        return f"hr@{domain}"

def calculate_savings(employees):
    """Calculate potential savings"""
    fica = employees * 681
    workers_comp = employees * 500 * 0.30
    total = fica + workers_comp
    return fica, workers_comp, total

def send_email(to_email, subject, text_content, html_content):
    """Send email via AgentMail API"""
    headers = {
        "Authorization": f"Bearer {AGENTMAIL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inbox_id": AGENTMAIL_INBOX,
        "to": [to_email],
        "subject": subject,
        "text": text_content,
        "html": html_content,
        "cc": [CC_EMAIL]
    }
    
    try:
        response = requests.post(
            f"https://api.agentmail.to/v0/inboxes/{AGENTMAIL_INBOX}/messages/send",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return {"success": True, "message_id": response.json().get("message_id")}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}: {response.text[:200]}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def create_outreach_email(company, email, employees):
    """Create personalized outreach email"""
    fica, workers_comp, total = calculate_savings(employees)
    
    subject = f"${total:,} annual savings for {company} (zero cost to implement)"
    
    text = f"""Hi there,

I noticed {company} has about {employees} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.

Organizations your size are typically saving:
- $681 per employee annually in FICA savings
- 30-60% reduction in workers' comp premiums
- Total savings: ${total:,}

One medical transportation company with 66 employees saved over $140,000 last year.

The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.

Would you be open to a 10-minute call this week to see the numbers for {company}?

Best,
Zane
Zane@agentmail.to
Wellness 125 Cafeteria Plan
"""

    html = f"""<p>Hi there,</p>

<p>I noticed {company} has about {employees} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.</p>

<p><strong>Organizations your size are typically saving:</strong></p>
<ul>
<li>$681 per employee annually in FICA savings</li>
<li>30-60% reduction in workers' comp premiums</li>
<li><strong>Total savings: ${total:,}</strong></li>
</ul>

<p>One medical transportation company with 66 employees saved over $140,000 last year.</p>

<p>The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.</p>

<p>Would you be open to a 10-minute call this week to see the numbers for {company}?</p>

<p>Best,<br>
Zane<br>
Zane@agentmail.to<br>
Wellness 125 Cafeteria Plan</p>
"""
    
    return subject, text, html

def main():
    print("\n" + "="*60)
    print("🚀 4 PM BATCH - Wellness 125 Outreach")
    print("="*60 + "\n")
    
    results = []
    sent_count = 0
    total_savings = 0
    
    for company in TARGET_COMPANIES:
        print(f"📧 Processing: {company['name']}")
        
        # Find email
        email = find_email_hunter(company['domain'])
        print(f"  📧 Email: {email}")
        
        # Calculate savings
        fica, workers_comp, total = calculate_savings(company['employees'])
        print(f"  💰 Est. Savings: ${total:,}")
        
        # Create and send email
        subject, text, html = create_outreach_email(
            company['name'], 
            email, 
            company['employees']
        )
        
        result = send_email(email, subject, text, html)
        
        if result['success']:
            sent_count += 1
            total_savings += total
            print(f"  ✅ SENT - Message ID: {result['message_id']}")
            results.append({
                "company": company['name'],
                "email": email,
                "employees": company['employees'],
                "savings": total,
                "message_id": result['message_id'],
                "success": True
            })
        else:
            print(f"  ❌ FAILED: {result['error']}")
            results.append({
                "company": company['name'],
                "email": email,
                "success": False,
                "error": result['error']
            })
    
    # Summary
    print("\n" + "="*60)
    print("📊 BATCH SUMMARY")
    print("="*60)
    print(f"✅ Emails Sent: {sent_count}/5")
    print(f"💰 Total Potential Savings: ${total_savings:,}")
    print(f"📋 All emails CC'd to: {CC_EMAIL}")
    print("="*60 + "\n")
    
    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "batch": "4 PM",
        "sent": sent_count,
        "total_savings": total_savings,
        "results": results
    }
    
    with open("/Users/cubiczan/.openclaw/workspace/leads/batch-results-2026-03-04-4pm.json", "w") as f:
        json.dump(output, f, indent=2)
    
    return output

if __name__ == "__main__":
    main()
