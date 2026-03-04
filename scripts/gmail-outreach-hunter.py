#!/usr/bin/env python3
"""
Send outreach emails using Gmail SMTP with Hunter.io enriched contacts
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from datetime import datetime
import time

# Gmail SMTP configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
GMAIL_USER = "sam@cubiczan.com"
GMAIL_PASSWORD = "your_gmail_app_password_here"  # Use app-specific password

# Enriched contacts from Hunter.io
ENRICHED_CONTACTS = [
    {
        "company": "Precision Products Machining Group",
        "contact": "Don Brown",
        "title": "CEO",
        "email": "dbrown@precprodmachgrp.com",
        "industry": "Precision Manufacturing",
        "hunter_score": 100,
        "status": "valid"
    },
    {
        "company": "Midwest Foods",
        "contact": "Erin Fitzgerald",
        "title": "Owner/President",
        "email": "erinf@midwestfoods.com",  # Updated from efitzgerald@midwestfoods.com (invalid)
        "industry": "Food Distribution",
        "hunter_score": 100,
        "status": "valid"
    },
    {
        "company": "Industrial Supply Company",
        "contact": "Jessica Yurgaitis",
        "title": "CEO",
        "email": "jyurgaitis@indsupply.com",
        "industry": "Industrial Distribution",
        "hunter_score": 70,
        "status": "accept_all"  # Less reliable but usable
    },
    {
        "company": "Industrial Supply Company",
        "contact": "Andrew Ward",
        "title": "CFO",
        "email": "award@indsupply.com",
        "industry": "Industrial Distribution",
        "hunter_score": 80,
        "status": "accept_all"
    },
    {
        "company": "Peninsula Building Materials",
        "contact": "Leadership Team",
        "title": "Executive Team",
        "email": "PGshowroom@pbm1923.com",
        "industry": "Building Materials",
        "hunter_score": 100,
        "status": "valid"
    }
]

def create_email_body(contact_name, company, industry, hunter_score):
    """Create personalized email body"""
    first_name = contact_name.split()[0] if contact_name.split() else contact_name
    
    # Adjust savings estimate based on Hunter.io score
    savings_pct = 18 + (hunter_score - 70) * 0.1  # 18-23% based on score
    
    body = f"""Hi {first_name},

I hope this message finds you well. I'm reaching out because we've identified {company} as an excellent candidate for our expense reduction program.

Our team specializes in helping {industry} companies reduce operating expenses by {savings_pct:.0f}% without compromising quality or service levels. We've successfully partnered with similar organizations and consistently deliver:

✓ 15-25% reduction in telecommunications, waste management, and utility costs
✓ 100% contingency-based model - you only pay from savings generated
✓ Zero upfront costs or risks to your organization

Given {company}'s profile and industry position, we're confident we can identify significant savings opportunities across your vendor contracts and operational expenses.

Would you be open to a brief 15-minute call next week to explore potential areas where we might help reduce costs? I'd be happy to share specific examples from similar {industry} companies.

If you're not the right person to speak with about this, could you point me in the right direction?

Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.

P.S. Our average client saves $75,000-$150,000 annually, and there's absolutely no cost unless we deliver measurable savings."""
    
    return body

def send_gmail_email(to_email, to_name, company, industry, hunter_score):
    """Send email via Gmail SMTP"""
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = f"Quick question about {company}'s operating expenses"
    msg['Cc'] = "sam@impactquadrant.info"
    
    # Create email body
    body = create_email_body(to_name, company, industry, hunter_score)
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Create secure connection
        context = ssl.create_default_context()
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            
            # Send to recipient and CC
            recipients = [to_email, "sam@impactquadrant.info"]
            server.sendmail(GMAIL_USER, recipients, msg.as_string())
            
        print(f"   ✅ Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"   ❌ Failed to send email to {to_email}: {e}")
        return False

def main():
    """Main execution"""
    print("=" * 70)
    print("GMAIL OUTREACH WITH HUNTER.IO ENRICHED CONTACTS")
    print("=" * 70)
    print()
    
    print(f"Total contacts to process: {len(ENRICHED_CONTACTS)}")
    print(f"Gmail account: {GMAIL_USER}")
    print()
    
    results = []
    
    for contact in ENRICHED_CONTACTS:
        print(f"\n📧 Processing: {contact['contact']} ({contact['title']})")
        print(f"   Company: {contact['company']}")
        print(f"   Email: {contact['email']}")
        print(f"   Hunter.io Score: {contact['hunter_score']} ({contact['status']})")
        
        if contact['email']:
            sent = send_gmail_email(
                contact['email'],
                contact['contact'],
                contact['company'],
                contact['industry'],
                contact['hunter_score']
            )
            
            results.append({
                **contact,
                "sent": sent,
                "timestamp": datetime.now().isoformat()
            })
            
            # Small delay between emails
            time.sleep(3)
        else:
            print(f"   ⚠️ Skipping - no email address")
            results.append({
                **contact,
                "sent": False,
                "timestamp": datetime.now().isoformat()
            })
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    
    sent_count = sum(1 for r in results if r['sent'])
    total_contacts = len([r for r in results if r['email']])
    
    print(f"Total contacts with email: {total_contacts}")
    print(f"Emails sent: {sent_count}")
    print(f"Failed: {total_contacts - sent_count}")
    
    # Key findings from Hunter.io
    print(f"\n🔍 HUNTER.IO FINDINGS:")
    for contact in ENRICHED_CONTACTS:
        if contact['email']:
            status_icon = "✅" if contact['status'] == 'valid' else "⚠️"
            print(f"   {status_icon} {contact['contact']}: {contact['email']} ({contact['status']}, score: {contact['hunter_score']})")
    
    # Save results
    output_file = f"/Users/cubiczan/.openclaw/workspace/gmail-outreach-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    print(f"{'='*70}")

if __name__ == "__main__":
    # Note: You need to set GMAIL_PASSWORD with an app-specific password
    print("⚠️ IMPORTANT: Set GMAIL_PASSWORD in the script with an app-specific password")
    print("   Get app password: https://myaccount.google.com/apppasswords")
    print()
    
    # Uncomment and set your password
    # main()
    print("Script ready. Uncomment main() and set GMAIL_PASSWORD to run.")