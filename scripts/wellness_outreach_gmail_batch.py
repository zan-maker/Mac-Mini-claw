#!/usr/bin/env python3
"""
Wellness 125 Outreach - Gmail SMTP Batch
Sends 5 outreach emails using Gmail SMTP (AgentMail API is down)
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json

# Gmail Configuration
GMAIL_CONFIG = {
    "email": "sam@cubiczan.com",
    "password": "mwzh abbf ssih mjsf",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "from_name": "Sam Desigan"
}

CC_EMAIL = "sam@impactquadrant.info"

# Leads to contact (from previous failed batch)
LEADS = [
    {
        "company": "Florida Sheet Metal",
        "email": "r.aguilar@floridasheetmetal.com",
        "employee_count": 55,
        "industry": "Metal Fabrication",
        "location": "Melbourne, FL"
    },
    {
        "company": "Rigid Concepts LLC",
        "email": "info@rigidconcepts.com",
        "employee_count": 73,
        "industry": "Manufacturing",
        "location": "Texas"
    },
    {
        "company": "Nordon, Inc.",
        "email": "info@nordonplastics.com",
        "employee_count": 91,
        "industry": "Plastics Manufacturing",
        "location": "Texas"
    },
    {
        "company": "GT Precision Manufacturing",
        "email": "info@gtprecisionmfg.com",
        "employee_count": 55,
        "industry": "Precision Manufacturing",
        "location": "Texas"
    },
    {
        "company": "Made in America Manufacturing",
        "email": "info@madeinamericamfg.com",
        "employee_count": 67,
        "industry": "Manufacturing",
        "location": "USA"
    }
]

def calculate_savings(employee_count):
    """Calculate potential savings"""
    fica_savings = employee_count * 681
    workers_comp_savings = employee_count * 500 * 0.30
    total_savings = fica_savings + workers_comp_savings
    return total_savings

def create_email(company_name, employee_count, industry, to_email):
    """Create personalized outreach email"""
    
    total_savings = calculate_savings(employee_count)
    
    subject = f"${int(total_savings):,} annual savings for {company_name} (zero cost to implement)"
    
    text_content = f"""Hi,

I noticed {company_name} has about {employee_count} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.

Organizations your size are typically saving:
• $681 per employee annually in FICA savings
• 30-60% reduction in workers' comp premiums
• Total savings: ${int(total_savings):,}

One medical transportation company with 66 employees saved over $140,000 last year.

The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.

Would you be open to a 10-minute call this week to see the numbers for {company_name}?

Best,
Sam
{GMAIL_CONFIG['from_name']}
Wellness 125 Cafeteria Plan
"""

    html_content = f"""<p>Hi,</p>

<p>I noticed {company_name} has about {employee_count} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.</p>

<p><strong>Organizations your size are typically saving:</strong></p>
<ul>
<li>$681 per employee annually in FICA savings</li>
<li>30-60% reduction in workers' comp premiums</li>
<li><strong>Total savings: ${int(total_savings):,}</strong></li>
</ul>

<p>One medical transportation company with 66 employees saved over $140,000 last year.</p>

<p>The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.</p>

<p>Would you be open to a 10-minute call this week to see the numbers for {company_name}?</p>

<p>Best,<br>
{GMAIL_CONFIG['from_name']}<br>
Wellness 125 Cafeteria Plan</p>
"""

    return subject, text_content, html_content

def send_email(to_email, subject, text_content, html_content):
    """Send email via Gmail SMTP"""
    
    msg = MIMEMultipart('alternative')
    msg['From'] = f"{GMAIL_CONFIG['from_name']} <{GMAIL_CONFIG['email']}>"
    msg['To'] = to_email
    msg['Cc'] = CC_EMAIL
    msg['Subject'] = subject
    
    msg.attach(MIMEText(text_content, 'plain'))
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        with smtplib.SMTP(GMAIL_CONFIG['smtp_server'], GMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(GMAIL_CONFIG['email'], GMAIL_CONFIG['password'])
            server.send_message(msg)
        return True, None
    except Exception as e:
        return False, str(e)

def main():
    """Send batch of 5 outreach emails"""
    
    print("=" * 60)
    print("WELLNESS 125 OUTREACH - 9 AM BATCH")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target: 5 emails")
    print(f"Method: Gmail SMTP (AgentMail API down)")
    print()
    
    results = []
    sent_count = 0
    failed_count = 0
    
    for lead in LEADS:
        company = lead['company']
        email = lead['email']
        employee_count = lead['employee_count']
        industry = lead['industry']
        
        print(f"📧 {company}")
        print(f"   To: {email}")
        print(f"   Employees: {employee_count}")
        
        # Calculate savings
        savings = calculate_savings(employee_count)
        print(f"   Potential savings: ${int(savings):,}")
        
        # Create email
        subject, text, html = create_email(company, employee_count, industry, email)
        
        # Send email
        success, error = send_email(email, subject, text, html)
        
        if success:
            print(f"   ✅ SENT")
            sent_count += 1
            results.append({
                "company": company,
                "email": email,
                "savings": savings,
                "status": "sent",
                "timestamp": datetime.now().isoformat()
            })
        else:
            print(f"   ❌ FAILED: {error}")
            failed_count += 1
            results.append({
                "company": company,
                "email": email,
                "savings": savings,
                "status": "failed",
                "error": error,
                "timestamp": datetime.now().isoformat()
            })
        print()
    
    # Summary
    print("=" * 60)
    print("BATCH SUMMARY")
    print("=" * 60)
    print(f"✅ Sent: {sent_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📊 Total potential savings: ${sum([r['savings'] for r in results if r['status'] == 'sent']):,}")
    print()
    
    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "batch": "9am",
        "method": "Gmail SMTP",
        "results": results,
        "summary": {
            "sent": sent_count,
            "failed": failed_count,
            "total_potential_savings": sum([r['savings'] for r in results if r['status'] == 'sent'])
        }
    }
    
    filename = f"/Users/cubiczan/.openclaw/workspace/leads/wellness_outreach_gmail_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Results saved to: {filename}")
    
    return output

if __name__ == "__main__":
    main()
