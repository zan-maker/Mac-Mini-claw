#!/usr/bin/env python3
"""
Dorada Resort Wave 5 Outreach - Send to Tier 5 investors
Using cubiczan Gmail SMTP credentials
"""

import smtplib
import ssl
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Gmail SMTP Credentials (from b2b-referral-agentmail.py)
CRON_GMAIL_EMAIL = "sam@cubiczan.com"
CRON_GMAIL_PASSWORD = "mwzh abbf ssih mjsf"
CRON_GMAIL_CC = "sam@impactquadrant.info"

# Wave 5 - Tier 5 Contacts (Score 10)
WAVE5_CONTACTS = [
    {
        "name": "Manu Gupta",
        "company": "Blue Lion",
        "email": "manu@bluelionglobal.com",
        "phone": "",
        "sectors": "Real Estate, Food & Beverage, Hospitality, Family Office",
        "version": "family_office"
    },
    {
        "name": "Matt Atkin",
        "company": "Blue Lion",
        "email": "matkin@bluelionglobal.com",
        "phone": "",
        "sectors": "Real Estate, Food & Beverage, Hospitality",
        "version": "family_office"
    },
    {
        "name": "Colin Bosa",
        "company": "Bosa Properties",
        "email": "cbosa@bosaproperties.com",
        "phone": "",
        "sectors": "Real Estate, Property Development, Hospitality",
        "version": "family_office"
    },
    {
        "name": "Andy Farbman",
        "company": "Farbman Group",
        "email": "afarbman@farbman.com",
        "phone": "(248) 353-0500",
        "sectors": "Commercial Real Estate, Hospitality, Family Office",
        "version": "family_office"
    },
    {
        "name": "Michael Kalil",
        "company": "Farbman Group",
        "email": "kalil@farbman.com",
        "phone": "(248) 353-0500",
        "sectors": "Commercial Real Estate, Hospitality",
        "version": "family_office"
    },
    {
        "name": "Mark Bartholomay",
        "company": "Nath Companies",
        "email": "mbartholomay@nathcompanies.com",
        "phone": "(281) 757-3158",
        "sectors": "Hotels, Multi-Family, Restaurants, Family-Owned",
        "version": "family_office"
    },
    {
        "name": "Michael Orsak",
        "company": "Nimes Real Estate",
        "email": "m.orsak@nimesrealestate.com",
        "phone": "(512) 574-8833",
        "sectors": "Multifamily, Hospitality, Family Office",
        "version": "family_office"
    },
    {
        "name": "Christopher Sutphen",
        "company": "Oxford Capital",
        "email": "",  # No email provided
        "phone": "",
        "sectors": "Hotels, Resorts, Senior Housing, Mixed-Use",
        "version": "institutional"
    },
    {
        "name": "Joanna Wu",
        "company": "Churchill Finance HK",
        "email": "joanna@churchill-finance.com",
        "phone": "+852 3975 3009",
        "sectors": "Real Estate, Hospitality, Healthcare, Family Office",
        "version": "family_office"
    },
    {
        "name": "Anjuli Nanda Habbas",
        "company": "Kapital Partners",
        "email": "anjuli@kapitalp.com",
        "phone": "",
        "sectors": "Real Estate, Hospitality, Family Office",
        "version": "family_office"
    },
    {
        "name": "Ross McBride",
        "company": "Globalvestment Capital",
        "email": "ross.mcbride@globalvestmentpartners.com",
        "phone": "",
        "sectors": "Hospitality Real Estate, Multifamily, Family Office",
        "version": "family_office"
    }
]

def create_dorada_family_office_email(contact):
    """Create FAMILY OFFICE VERSION email for Dorada Resort"""
    
    last_name = contact["name"].split()[-1]
    company = contact["company"]
    sectors = contact["sectors"]
    
    subject = "Multi-generational wellness asset in Costa Rica's Blue Zone"
    
    text_content = f"""Dear Mr. {last_name},

I'm reaching out regarding Dorada, a first-of-its-kind regenerative destination resort and residential community in one of the world's rare Blue Zone regions of Costa Rica.

Given {company}'s focus on {sectors}, I believe Dorada aligns with your investment philosophy—particularly as a multi-generational legacy asset that combines:

• 300-acre protected bio-reserve with panoramic ocean views
• 40 private estate homes (1+ acre lots)
• Longevity & Human Performance Center offering personalized healthspan programs
• Fully off-grid with sustainable infrastructure
• Recurring revenue from wellness programs and memberships

Dorada is the vision of Dr. Vincent Giampapa, a globally recognized leader in anti-aging medicine and regenerative science. It's designed not as a hospitality project, but as a permanent wellness ecosystem for long-term ownership.

Why for family offices: Capital preservation with upside, intergenerational relevance, personal use optionality, and alignment with the $2.1T wellness economy (12.4% CAGR).

Would you be open to a brief call to discuss the opportunity? I'd be happy to share the full investor deck.

Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.
"""

    html_content = f"""<p>Dear Mr. {last_name},</p>

<p>I'm reaching out regarding <strong>Dorada</strong>, a first-of-its-kind regenerative destination resort and residential community in one of the world's rare Blue Zone regions of Costa Rica.</p>

<p>Given {company}'s focus on {sectors}, I believe Dorada aligns with your investment philosophy—particularly as a multi-generational legacy asset that combines:</p>

<ul>
<li><strong>300-acre protected bio-reserve</strong> with panoramic ocean views</li>
<li><strong>40 private estate homes</strong> (1+ acre lots)</li>
<li><strong>Longevity & Human Performance Center</strong> offering personalized healthspan programs</li>
<li>Fully off-grid with sustainable infrastructure</li>
<li><strong>Recurring revenue</strong> from wellness programs and memberships</li>
</ul>

<p>Dorada is the vision of <strong>Dr. Vincent Giampapa</strong>, a globally recognized leader in anti-aging medicine and regenerative science. It's designed not as a hospitality project, but as a <strong>permanent wellness ecosystem</strong> for long-term ownership.</p>

<p><strong>Why for family offices:</strong> Capital preservation with upside, intergenerational relevance, personal use optionality, and alignment with the $2.1T wellness economy (12.4% CAGR).</p>

<p>Would you be open to a brief call to discuss the opportunity? I'd be happy to share the full investor deck.</p>

<p>Best regards,<br>
Zane<br>
Agent Manager<br>
Impact Quadrant</p>

<p>Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.</p>
"""

    return {
        "to": contact["email"],
        "subject": subject,
        "text": text_content,
        "html": html_content
    }

def create_dorada_institutional_email(contact):
    """Create INSTITUTIONAL VERSION email for Dorada Resort"""
    
    last_name = contact["name"].split()[-1]
    company = contact["company"]
    sectors = contact["sectors"]
    
    subject = "Luxury wellness platform in Costa Rica - $2.1T market opportunity"
    
    text_content = f"""Dear Mr. {last_name},

I'm reaching out regarding Dorada, a category-defining luxury wellness and longevity platform in Costa Rica's Blue Zone.

Given {company}'s portfolio spanning {sectors}, I believe Dorada represents a strategic fit as a multi-stream revenue platform:

Revenue Streams:
• Luxury real estate sales and appreciation
• Hospitality and branded residence income
• High-margin longevity and performance programs (7-10 day intensives)
• Membership-based recurring revenues
• Farm-to-table dining and experiential services

Core Differentiator:
The Longevity & Human Performance Center delivers personalized, data-driven healthspan interventions—transforming Dorada from a destination into a lifetime engagement model with materially higher customer LTV.

Asset Overview:
• 300-acre protected development
• Ultra-low density, premium positioning
• Replicable model across Blue Zone geographies
• Brand extensibility into digital health and affiliated clinics

The global wellness and longevity economy is projected to reach $2.1T by 2030 (12.4% CAGR). Dorada is positioned at the intersection of this trend with defensible scientific credibility.

Would you be open to reviewing the investor deck?

Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.
"""

    html_content = f"""<p>Dear Mr. {last_name},</p>

<p>I'm reaching out regarding <strong>Dorada</strong>, a category-defining luxury wellness and longevity platform in Costa Rica's Blue Zone.</p>

<p>Given {company}'s portfolio spanning {sectors}, I believe Dorada represents a strategic fit as a <strong>multi-stream revenue platform</strong>:</p>

<p><strong>Revenue Streams:</strong></p>
<ul>
<li>Luxury real estate sales and appreciation</li>
<li>Hospitality and branded residence income</li>
<li>High-margin longevity and performance programs (7-10 day intensives)</li>
<li>Membership-based recurring revenues</li>
<li>Farm-to-table dining and experiential services</li>
</ul>

<p><strong>Core Differentiator:</strong><br>
The <strong>Longevity & Human Performance Center</strong> delivers personalized, data-driven healthspan interventions—transforming Dorada from a destination into a <strong>lifetime engagement model</strong> with materially higher customer LTV.</p>

<p><strong>Asset Overview:</strong></p>
<ul>
<li>300-acre protected development</li>
<li>Ultra-low density, premium positioning</li>
<li>Replicable model across Blue Zone geographies</li>
<li>Brand extensibility into digital health and affiliated clinics</li>
</ul>

<p>The global wellness and longevity economy is projected to reach <strong>$2.1T by 2030</strong> (12.4% CAGR). Dorada is positioned at the intersection of this trend with defensible scientific credibility.</p>

<p>Would you be open to reviewing the investor deck?</p>

<p>Best regards,<br>
Zane<br>
Agent Manager<br>
Impact Quadrant</p>

<p>Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.</p>
"""

    return {
        "to": contact["email"],
        "subject": subject,
        "text": text_content,
        "html": html_content
    }

def send_email_gmail_smtp(to_email, subject, text_content, html_content=None, cc=None):
    """Send email via Gmail SMTP"""
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f'Agent Manager <{CRON_GMAIL_EMAIL}>'
        msg['To'] = to_email
        msg['Subject'] = subject
        
        if cc:
            msg['Cc'] = cc
        
        # Add text version
        text_part = MIMEText(text_content, 'plain')
        msg.attach(text_part)
        
        # Add HTML version if provided
        if html_content:
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
        
        # Connect and send
        context = ssl.create_default_context()
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(CRON_GMAIL_EMAIL, CRON_GMAIL_PASSWORD)
            
            # Send email
            recipients = [to_email]
            if cc:
                recipients.append(cc)
            
            server.sendmail(CRON_GMAIL_EMAIL, recipients, msg.as_string())
        
        return {"success": True}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    print("\n" + "="*60)
    print("Dorada Resort - Wave 5 Outreach (Gmail SMTP)")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    total_contacts = len(WAVE5_CONTACTS)
    sent_count = 0
    failed_count = 0
    skipped_count = 0
    
    for i, contact in enumerate(WAVE5_CONTACTS, 1):
        print(f"\n[{i}/{total_contacts}] Processing: {contact['name']} ({contact['company']})")
        
        # Skip if no email
        if not contact['email']:
            print(f"  ⚠️ SKIPPED: No email address")
            skipped_count += 1
            continue
        
        print(f"  Email: {contact['email']}")
        print(f"  CC: {CRON_GMAIL_CC}")
        print(f"  Template: {contact['version'].upper()} VERSION")
        
        # Create email based on version
        if contact['version'] == 'family_office':
            email_data = create_dorada_family_office_email(contact)
        else:
            email_data = create_dorada_institutional_email(contact)
        
        # Send email
        result = send_email_gmail_smtp(
            to_email=email_data["to"],
            subject=email_data["subject"],
            text_content=email_data["text"],
            html_content=email_data.get("html"),
            cc=CRON_GMAIL_CC
        )
        
        if result['success']:
            print(f"  ✅ SENT SUCCESSFULLY")
            sent_count += 1
        else:
            print(f"  ❌ FAILED: {result['error']}")
            failed_count += 1
        
        # Small delay between sends to avoid rate limiting
        if i < total_contacts:
            time.sleep(3)
    
    # Summary
    print("\n" + "="*60)
    print("WAVE 5 OUTREACH SUMMARY")
    print("="*60)
    print(f"Total contacts: {total_contacts}")
    print(f"Successfully sent: {sent_count}")
    print(f"Failed: {failed_count}")
    print(f"Skipped (no email): {skipped_count}")
    print(f"Completion: {sent_count}/{total_contacts-skipped_count} ({sent_count/(total_contacts-skipped_count)*100:.1f}% of reachable)")
    print("="*60)
    
    # Save results
    import json
    results = {
        "wave": 5,
        "timestamp": datetime.now().isoformat(),
        "total_contacts": total_contacts,
        "sent": sent_count,
        "failed": failed_count,
        "skipped": skipped_count,
        "email_used": CRON_GMAIL_EMAIL,
        "contacts": WAVE5_CONTACTS
    }
    
    results_file = f"/Users/cubiczan/.openclaw/workspace/dorada-wave5-gmail-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {results_file}")
    
    return 0 if failed_count == 0 else 1

if __name__ == "__main__":
    exit(main())
