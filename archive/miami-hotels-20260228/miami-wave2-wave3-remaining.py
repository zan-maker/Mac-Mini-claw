#!/usr/bin/env python3
"""
Miami Hotels - Send Wave 2 & 3 Remaining Emails
Send emails to remaining Wave 2 and Wave 3 contacts using Gmail SMTP
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

# Miami Hotels Contacts to send
MIAMI_CONTACTS = [
    # Wave 2 - Remaining
    {
        "name": "Justin Cooper",
        "company": "Layla Capital",
        "email": "justin@laylacapital.com",
        "template": "Template 3 (Both)",
        "wave": 2,
        "contact_id": 6
    },
    {
        "name": "Maxwell Deibel",
        "company": "Layla Capital",
        "email": "max@laylacapital.com",
        "template": "Template 3 (Both)",
        "wave": 2,
        "contact_id": 7
    },
    {
        "name": "Andrea Cassandro",
        "company": "East To West Capital",
        "email": "andrea.cassandro@investincapital.com",
        "template": "Template 3 (Both)",
        "wave": 2,
        "contact_id": 8
    },
    {
        "name": "Joseph O'Connor",
        "company": "Mandrake Capital",
        "email": "joconnor@mandrakecapital.com",
        "template": "Template 3 (Both)",
        "wave": 2,
        "contact_id": 9
    },
    # Wave 3 - Remaining
    {
        "name": "Blair Humphreys",
        "company": "Humphreys Capital",
        "email": "blair@humphreyscapital.com",
        "template": "Template 2 (Thesis)",
        "wave": 3,
        "contact_id": 11
    },
    {
        "name": "Richard Kessler",
        "company": "Benenson Capital Partners",
        "email": "rkessler@benensoncapital.com",
        "template": "Template 3 (Both)",
        "wave": 3,
        "contact_id": 12
    },
    {
        "name": "Pedro Silva",
        "company": "Caoba Capital Partners",
        "email": "psilva@caoba.partners",
        "template": "Template 3 (Both)",
        "wave": 3,
        "contact_id": 13
    },
    {
        "name": "Matthew Monterroso",
        "company": "Commercial Asset Advisors",
        "email": "matt@caacre.com",
        "template": "Template 3 (Both)",
        "wave": 3,
        "contact_id": 14
    }
]

def get_email_template(contact_name, company, template_type):
    """Get appropriate email template based on template type"""
    
    if template_type == "Template 1 (Tides)":
        subject = f"Trophy oceanfront asset - Miami Beach (45 suites + 95-key expansion)"
        
        body = f"""Dear {contact_name.split()[0]},

I'm reaching out regarding a rare oceanfront hospitality opportunity in Miami Beach—**The Tides South Beach & Tides Village**.

**Key Highlights:**
- **Prime Location:** 1220 Ocean Drive, direct beachfront on Miami Beach
- **Current Asset:** 45 luxury suites (100% oceanfront, avg 652 sq ft)
- **Expansion Opportunity:** 95 additional keys across three parcels
- **Grandfathered Beach Rights:** Exclusive beach service (chairs, umbrellas, F&B)
- **Recent Renovation:** $18M capital program ($400K/key)
- **Market Position:** Luxury segment, one of highest RevPAR markets in US

**Investment Thesis:**
- Trophy oceanfront positioning with expansion potential
- ADR upside via rebranding (currently underperforming comp set)
- Mixed-use opportunity with new F&B/retail components
- Scale to 140 total keys post-expansion

**Miami Beach Market:**
- 12M+ annual visitors
- $17B tourism spend
- Limited new supply due to zoning constraints

Would you be interested in reviewing the confidential offering memorandum?

Best regards,

Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    
    elif template_type == "Template 2 (Thesis)":
        subject = f"Mixed-use hospitality opportunity - $315M Miami asset near University of Miami"
        
        body = f"""Dear {contact_name.split()[0]},

I'm reaching out regarding an institutional-scale mixed-use asset in Coral Gables, Florida—**Thesis Hotel Miami**.

**Asset Overview:**
- **Location:** 1350 S Dixie Hwy, adjacent to University of Miami
- **Composition:** 245 hotel keys + 204 multifamily units + 30K sq ft retail
- **Asking Price:** $315,000,000
- **NOI:** $18,128,000
- **Debt:** $150M assumable at 4.65% (significant value)

**Multifamily Performance:**
- 99% occupancy
- 80-90 person waiting list (UM students + medical staff)
- Strong demand driver with institutional backing

**Investment Optionality:**
1. **Hotel + Multifamily Hold:** Current income + retail lease-up upside
2. **Student Housing Conversion:** Up to 245 keys convertible to student housing
3. **Hotel-Only Acquisition:** Seller can separate components
4. **Densification:** Zoning allows additional residential density

**Process:** LOI + proof of funds + buyer bio required to proceed.

Given {company}'s focus on hospitality/mixed-use/student housing, I believe this aligns with your investment criteria.

Would you be interested in reviewing the full package?

Best regards,

Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    
    else:  # Template 3 (Both)
        subject = f"Two Miami hospitality opportunities - Oceanfront trophy + Mixed-use campus"
        
        body = f"""Dear {contact_name.split()[0]},

I'm reaching out with two distinct Miami hospitality opportunities that may align with {company}'s investment focus:

**1. Tides South Beach & Tides Village**
- 45 luxury oceanfront suites (South Beach)
- 95-key expansion opportunity
- Direct beachfront with grandfathered rights
- Trophy positioning, ADR upside potential

**2. Thesis Hotel Miami**
- 245 hotel + 204 multifamily + 30K retail
- $315M asking, $150M assumable debt at 4.65%
- Adjacent to University of Miami
- Student housing conversion optionality

Both assets represent institutional-scale opportunities with clear value-add pathways. The Miami hospitality market continues to outperform national averages, driven by strong tourism fundamentals and limited new supply.

Would you be interested in reviewing either or both opportunities?

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
    print("MIAMI HOTELS - WAVE 2 & 3 EMAIL OUTREACH")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    print(f"Sending {len(MIAMI_CONTACTS)} emails (Wave 2: 4, Wave 3: 4)...")
    print()
    
    results = []
    
    for contact in MIAMI_CONTACTS:
        print(f"Processing: {contact['name']} - {contact['company']}")
        print(f"  Email: {contact['email']}")
        print(f"  Wave: {contact['wave']}, Template: {contact['template']}")
        
        # Get email template
        subject, body = get_email_template(
            contact['name'],
            contact['company'],
            contact['template']
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
            "template": contact['template'],
            "success": success,
            "timestamp": datetime.now().isoformat()
        })
        
        # Small delay between emails
        if contact != MIAMI_CONTACTS[-1]:
            time.sleep(2)
        
        print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r['success'])
    wave2_sent = sum(1 for r in results if r['wave'] == 2 and r['success'])
    wave3_sent = sum(1 for r in results if r['wave'] == 3 and r['success'])
    
    print(f"Total attempted: {len(results)}")
    print(f"Successfully sent: {success_count}")
    print(f"Failed: {len(results) - success_count}")
    print()
    print(f"Wave 2 sent: {wave2_sent}/4")
    print(f"Wave 3 sent: {wave3_sent}/4")
    
    # Update campaign tracking (would need to update the markdown file)
    print()
    print("Note: Campaign tracking in miami-hotels-outreach-campaign.md should be updated")
    print("with sent dates for these contacts.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
