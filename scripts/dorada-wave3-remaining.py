#!/usr/bin/env python3
"""
Dorada Resort - Send Wave 3 Remaining Emails
Send emails to remaining Wave 3 contacts using Gmail SMTP
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
from datetime import datetime
import time

# Gmail Configuration
GMAIL_SENDER = "zan@impactquadrant.info"
GMAIL_PASSWORD = "apbj bvsl tngo vqhu"
GMAIL_CC = "sam@impactquadrant.info"

# Wave 3 Contacts to send
WAVE_3_CONTACTS = [
    {
        "name": "Praveen Vetrivel",
        "company": "Libra Group",
        "email": "praveen.vetrivel@libra.com",
        "title": "Group CFO",
        "version": "institutional",
        "wave": 3,
        "contact_id": 13
    },
    {
        "name": "Jeffrey Weidell",
        "company": "Northmarq",
        "email": "jweidell@northmarq.com",
        "title": "CEO",
        "version": "institutional",
        "wave": 3,
        "contact_id": 14
    },
    {
        "name": "Shawn Power",
        "company": "Northmarq",
        "email": "spower@northmarq.com",
        "title": "CFO",
        "version": "institutional",
        "wave": 3,
        "contact_id": 15
    }
]

def get_email_template(contact_name, company, version):
    """Get appropriate email template based on version"""
    
    if version == "institutional":
        subject = f"Scalable longevity real estate platform - Costa Rica Blue Zone"
        
        body = f"""Dear {contact_name.split()[0]},

I'm reaching out regarding **Dorada**, a luxury wellness and longevity platform in Costa Rica that combines premium real estate with recurring health services revenue.

Given {company}'s investment focus across wellness, hospitality, real estate, and healthcare, Dorada offers exposure to **structural tailwinds in the $2.1T longevity economy** (12.4% CAGR).

**Investment Thesis:**
- **Tangible real assets** with experiential differentiation
- **Multi-stream revenue model** (real estate + hospitality + longevity programs + memberships)
- **Recurring revenue** from 7-10 day health intensives and membership programs
- **Scalable platform** with replication potential across Blue Zone geographies
- **Brand extensibility** into digital health, clinics, and affiliated services

**Core Differentiator:**
Unlike traditional wellness resorts, Dorada's **Longevity & Human Performance Center** delivers science-driven, measurable longevity outcomes—creating a **repeat-engagement model** with high customer LTV.

**Asset:** 300-acre protected bio-reserve with ultra-low density development (40 estate homes, eco-hotel, branded residences, farm-to-table dining).

**Exit Optionality:** Portfolio expansion, strategic sale, or long-term cash flow hold.

Would you be open to reviewing the investor materials?

Best regards,

Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    
    else:  # family_office version
        subject = f"Legacy wellness asset in Costa Rica - health preservation meets wealth preservation"
        
        body = f"""Dear {contact_name.split()[0]},

I'm reaching out regarding **Dorada**, a first-of-its-kind regenerative destination resort in Costa Rica's Blue Zone—designed specifically for families seeking to preserve both health and capital across generations.

Given {company}'s focus on healthcare, wellness, and family office clients, I believe Dorada aligns with your clients' priorities:

- **Capital preservation with upside**
- **Hard assets paired with experiential value**
- **Intergenerational relevance**
- **Personal use optionality alongside returns**

**The Asset:**
- **300-acre protected bio-reserve** with world-class ocean views
- **40 private estate homes** (1+ acre lots)
- **Longevity & Human Performance Center** with personalized healthspan programs
- Fully off-grid with sustainable infrastructure
- **Curated longevity community** of like-minded families

**Founder:** Dr. Vincent Giampapa, globally recognized leader in anti-aging medicine and regenerative science.

**Market Opportunity:** The wellness economy is projected to reach **$2.1T by 2030**, driven by aging HNW populations seeking preventive, performance-based health solutions.

**Legacy Value:** Dorada allows families to invest in something that enhances not only balance sheets—but quality of life, longevity, and human potential.

Would you be interested in sharing this opportunity with your family office clients?

Best regards,

Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    
    return subject, body

def send_gmail_email(to_email, to_name, subject, body):
    """Send email via Gmail SMTP"""
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = GMAIL_SENDER
        msg['To'] = to_email
        msg['Cc'] = GMAIL_CC
        
        # Create HTML version
        html_body = body.replace('\n', '<br>')
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        # Create plain text version
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(GMAIL_SENDER, GMAIL_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email sent to: {to_name} ({to_email})")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send to {to_name} ({to_email}): {str(e)}")
        return False

def main():
    """Main execution"""
    
    print("=" * 60)
    print("DORADA RESORT - WAVE 3 EMAIL OUTREACH")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    print(f"Sending {len(WAVE_3_CONTACTS)} Wave 3 emails...")
    print()
    
    results = []
    
    for contact in WAVE_3_CONTACTS:
        print(f"Processing: {contact['name']} - {contact['company']}")
        print(f"  Email: {contact['email']}")
        print(f"  Version: {contact['version']}")
        
        # Get email template
        subject, body = get_email_template(
            contact['name'],
            contact['company'],
            contact['version']
        )
        
        # Send email
        success = send_gmail_email(
            contact['email'],
            contact['name'],
            subject,
            body
        )
        
        # Record result
        results.append({
            "contact": contact['name'],
            "company": contact['company'],
            "email": contact['email'],
            "wave": contact['wave'],
            "success": success,
            "timestamp": datetime.now().isoformat()
        })
        
        # Small delay between emails
        if contact != WAVE_3_CONTACTS[-1]:
            time.sleep(2)
        
        print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r['success'])
    print(f"Total attempted: {len(results)}")
    print(f"Successfully sent: {success_count}")
    print(f"Failed: {len(results) - success_count}")
    
    # Update campaign tracking (would need to update the markdown file)
    print()
    print("Note: Campaign tracking in dorada-outreach-campaign.md should be updated")
    print("with sent dates for these contacts.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
