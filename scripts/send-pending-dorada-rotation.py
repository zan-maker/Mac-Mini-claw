#!/usr/bin/env python3
"""
Send all pending Dorada emails with Gmail rotation
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
from datetime import datetime
import time
import json
import os

# Gmail accounts for rotation
GMAIL_ACCOUNTS = [
    {"email": "zan@impactquadrant.info", "password": "apbj bvsl tngo vqhu", "name": "Zane"},
    {"email": "sam@impactquadrant.info", "password": "ajup xyhf abbx iugj", "name": "Sam"}
]

CC_EMAIL = "sam@impactquadrant.info"

# Pending Dorada contacts (Waves 4, 5, 6)
# From dorada-outreach-campaign.md tracking table
PENDING_CONTACTS = [
    # Wave 4 (16-22)
    {"name": "John Dziminski", "company": "The Rosewood Corp", "email": "jdziminski@rosewd.com", "version": "family_office", "wave": 4},
    {"name": "Kyle Van de Ven", "company": "The Rosewood Corp", "email": "kyle@guideboatcap.com", "version": "family_office", "wave": 4},
    {"name": "Bart Marlar", "company": "Griffis/Blessing", "email": "bart@gb85.com", "version": "family_office", "wave": 4},
    {"name": "Jessica Pagan", "company": "Machen McChesney", "email": "jpagan@machenmcchesney.com", "version": "institutional", "wave": 4},
    {"name": "Mark Long", "company": "Private Medical", "email": "mlong@privatemedical.org", "version": "family_office", "wave": 4},
    {"name": "Marina Beierbeck", "company": "SITOA GmbH", "email": "m.beierbeck@sitoa.de", "version": "institutional", "wave": 4},
    {"name": "Iva Kochovska", "company": "Jimdo", "email": "iva.kochovska@jimdo.com", "version": "family_office", "wave": 4},
    
    # Wave 5 (24-33) - skipping #23 Manu Gupta (already sent)
    {"name": "Matt Atkin", "company": "Blue Lion", "email": "matkin@bluelionglobal.com", "version": "institutional", "wave": 5},
    {"name": "Colin Bosa", "company": "Bosa Properties", "email": "cbosa@bosaproperties.com", "version": "institutional", "wave": 5},
    {"name": "Andy Farbman", "company": "Farbman Group", "email": "afarbman@farbman.com", "version": "family_office", "wave": 5},
    {"name": "Michael Kalil", "company": "Farbman Group", "email": "kalil@farbman.com", "version": "institutional", "wave": 5},
    {"name": "Mark Bartholomay", "company": "Nath Companies", "email": "mbartholomay@nathcompanies.com", "version": "family_office", "wave": 5},
    {"name": "Michael Orsak", "company": "Nimes Real Estate", "email": "m.orsak@nimesrealestate.com", "version": "family_office", "wave": 5},
    # {"name": "Christopher Sutphen", "company": "Oxford Capital", "email": "", "version": "institutional", "wave": 5}, # No email
    {"name": "Joanna Wu", "company": "Churchill Finance HK", "email": "joanna@churchill-finance.com", "version": "family_office", "wave": 5},
    {"name": "Anjuli Nanda Habbas", "company": "Kapital Partners", "email": "anjuli@kapitalp.com", "version": "family_office", "wave": 5},
    {"name": "Ross McBride", "company": "Globalvestment Capital", "email": "ross.mcbride@globalvestmentpartners.com", "version": "institutional", "wave": 5},
    
    # Wave 6 (34-42) - skipping #34 John Catsimatidis (already sent)
    {"name": "John Catsimatidis Jr", "company": "Red Apple Group", "email": "jac@ragny.com", "version": "family_office", "wave": 6},
    {"name": "Sam Gillespie", "company": "AssetBlue Investment", "email": "sam@assetblue.com", "version": "family_office", "wave": 6},
    {"name": "Michael Howley", "company": "Bratenahl Capital", "email": "mhowley@bratenahlcapital.com", "version": "family_office", "wave": 6},
    {"name": "Randy Williams", "company": "Keiretsu Forum", "email": "randy@keiretsuforum.com", "version": "family_office", "wave": 6},
    {"name": "Andrew Le", "company": "Investment Counsel NV", "email": "andrew@iccnv.com", "version": "family_office", "wave": 6},
    {"name": "Manu Punnoose", "company": "Subhkam Ventures", "email": "manu@subhkam.com", "version": "family_office", "wave": 6},
    {"name": "Bridget Palmer", "company": "Bisdorf Palmer", "email": "bridget@bisdorfpalmer.com", "version": "family_office", "wave": 6},
    {"name": "Emily Barreca", "company": "National Retail Group", "email": "emily@nrgproperty.com.au", "version": "family_office", "wave": 6},
]

# Remove contacts without email
PENDING_CONTACTS = [c for c in PENDING_CONTACTS if c['email']]

def get_dorada_template(contact_name, company, version):
    """Get Dorada email template"""
    
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
    
    else:  # family_office
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

def send_email(account, to_email, to_name, subject, body):
    """Send email using specified Gmail account"""
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{account['name']} <{account['email']}>"
        msg['To'] = to_email
        msg['Cc'] = CC_EMAIL
        
        html_body = body.replace('\n', '<br>')
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(account['email'], account['password'])
            server.send_message(msg)
        
        return True, account['email']
        
    except Exception as e:
        return False, str(e)

def main():
    """Send all pending Dorada emails with rotation"""
    
    print("=" * 60)
    print("DORADA PENDING EMAILS - ROTATION SEND")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    print(f"Total pending contacts: {len(PENDING_CONTACTS)}")
    print(f"Gmail accounts: {len(GMAIL_ACCOUNTS)} (rotation enabled)")
    print()
    
    results = []
    current_account_idx = 0
    sent_count = 0
    
    for i, contact in enumerate(PENDING_CONTACTS):
        print(f"[{i+1}/{len(PENDING_CONTACTS)}] Processing: {contact['name']} - {contact['company']}")
        print(f"  Email: {contact['email']}")
        print(f"  Wave: {contact['wave']}, Version: {contact['version']}")
        
        # Get template
        subject, body = get_dorada_template(
            contact['name'],
            contact['company'],
            contact['version']
        )
        
        # Select account (simple rotation)
        account = GMAIL_ACCOUNTS[current_account_idx]
        print(f"  Using account: {account['email']}")
        
        # Send email
        success, result = send_email(account, contact['email'], contact['name'], subject, body)
        
        if success:
            print(f"  ✅ SENT")
            sent_count += 1
            results.append({
                "contact": contact['name'],
                "company": contact['company'],
                "email": contact['email'],
                "wave": contact['wave'],
                "success": True,
                "account": account['email'],
                "timestamp": datetime.now().isoformat()
            })
            
            # Rotate to next account
            current_account_idx = (current_account_idx + 1) % len(GMAIL_ACCOUNTS)
            
        else:
            print(f"  ❌ FAILED: {result}")
            results.append({
                "contact": contact['name'],
                "company": contact['company'],
                "email": contact['email'],
                "wave": contact['wave'],
                "success": False,
                "error": result,
                "timestamp": datetime.now().isoformat()
            })
            
            # Try with other account
            other_idx = (current_account_idx + 1) % len(GMAIL_ACCOUNTS)
            other_account = GMAIL_ACCOUNTS[other_idx]
            print(f"  Trying backup account: {other_account['email']}")
            
            success2, result2 = send_email(other_account, contact['email'], contact['name'], subject, body)
            
            if success2:
                print(f"  ✅ SENT via backup")
                sent_count += 1
                results[-1]["success"] = True
                results[-1]["account"] = other_account['email']
                del results[-1]["error"]
                
                # Continue with backup account
                current_account_idx = other_idx
            else:
                print(f"  ❌ Backup also failed: {result2}")
        
        # Delay between emails (5 seconds to avoid rate limits)
        if i < len(PENDING_CONTACTS) - 1:
            print(f"  Waiting 5 seconds...")
            time.sleep(5)
        
        print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total attempted: {len(PENDING_CONTACTS)}")
    print(f"Successfully sent: {sent_count}")
    print(f"Failed: {len(PENDING_CONTACTS) - sent_count}")
    
    # Save results
    results_file = f"/Users/cubiczan/.openclaw/workspace/dorada-pending-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {results_file}")
    
    # Update campaign tracking
    print("\nNote: Update dorada-outreach-campaign.md with sent dates")
    print("for successfully sent contacts.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
