#!/usr/bin/env python3
"""
Send pending Dorada emails using Gmail rotation system
"""

import sys
sys.path.append('/Users/cubiczan/.openclaw/workspace/scripts')

from gmail_rotation import GmailRotator
from datetime import datetime
import time

# Pending Dorada contacts (simplified list)
PENDING_CONTACTS = [
    # Wave 4
    {"name": "John Dziminski", "company": "The Rosewood Corp", "email": "jdziminski@rosewd.com", "version": "family_office", "wave": 4},
    {"name": "Kyle Van de Ven", "company": "The Rosewood Corp", "email": "kyle@guideboatcap.com", "version": "family_office", "wave": 4},
    {"name": "Bart Marlar", "company": "Griffis/Blessing", "email": "bart@gb85.com", "version": "family_office", "wave": 4},
    {"name": "Jessica Pagan", "company": "Machen McChesney", "email": "jpagan@machenmcchesney.com", "version": "institutional", "wave": 4},
    {"name": "Mark Long", "company": "Private Medical", "email": "mlong@privatemedical.org", "version": "family_office", "wave": 4},
    {"name": "Marina Beierbeck", "company": "SITOA GmbH", "email": "m.beierbeck@sitoa.de", "version": "institutional", "wave": 4},
    {"name": "Iva Kochovska", "company": "Jimdo", "email": "iva.kochovska@jimdo.com", "version": "family_office", "wave": 4},
    
    # Wave 5
    {"name": "Matt Atkin", "company": "Blue Lion", "email": "matkin@bluelionglobal.com", "version": "institutional", "wave": 5},
    {"name": "Colin Bosa", "company": "Bosa Properties", "email": "cbosa@bosaproperties.com", "version": "institutional", "wave": 5},
    {"name": "Andy Farbman", "company": "Farbman Group", "email": "afarbman@farbman.com", "version": "family_office", "wave": 5},
    {"name": "Michael Kalil", "company": "Farbman Group", "email": "kalil@farbman.com", "version": "institutional", "wave": 5},
    {"name": "Mark Bartholomay", "company": "Nath Companies", "email": "mbartholomay@nathcompanies.com", "version": "family_office", "wave": 5},
    {"name": "Michael Orsak", "company": "Nimes Real Estate", "email": "m.orsak@nimesrealestate.com", "version": "family_office", "wave": 5},
    {"name": "Joanna Wu", "company": "Churchill Finance HK", "email": "joanna@churchill-finance.com", "version": "family_office", "wave": 5},
    {"name": "Anjuli Nanda Habbas", "company": "Kapital Partners", "email": "anjuli@kapitalp.com", "version": "family_office", "wave": 5},
    {"name": "Ross McBride", "company": "Globalvestment Capital", "email": "ross.mcbride@globalvestmentpartners.com", "version": "institutional", "wave": 5},
    
    # Wave 6
    {"name": "John Catsimatidis Jr", "company": "Red Apple Group", "email": "jac@ragny.com", "version": "family_office", "wave": 6},
    {"name": "Sam Gillespie", "company": "AssetBlue Investment", "email": "sam@assetblue.com", "version": "family_office", "wave": 6},
    {"name": "Michael Howley", "company": "Bratenahl Capital", "email": "mhowley@bratenahlcapital.com", "version": "family_office", "wave": 6},
    {"name": "Randy Williams", "company": "Keiretsu Forum", "email": "randy@keiretsuforum.com", "version": "family_office", "wave": 6},
    {"name": "Andrew Le", "company": "Investment Counsel NV", "email": "andrew@iccnv.com", "version": "family_office", "wave": 6},
    {"name": "Manu Punnoose", "company": "Subhkam Ventures", "email": "manu@subhkam.com", "version": "family_office", "wave": 6},
    {"name": "Bridget Palmer", "company": "Bisdorf Palmer", "email": "bridget@bisdorfpalmer.com", "version": "family_office", "wave": 6},
    {"name": "Emily Barreca", "company": "National Retail Group", "email": "emily@nrgproperty.com.au", "version": "family_office", "wave": 6},
]

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

def main():
    """Send pending Dorada emails with rotation"""
    
    print("=" * 60)
    print("DORADA PENDING EMAILS - GMAIL ROTATION")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # Initialize rotator
    rotator = GmailRotator()
    rotator.print_stats()
    
    print(f"Pending contacts: {len(PENDING_CONTACTS)}")
    print(f"Estimated time: {len(PENDING_CONTACTS) * 5 / 60:.1f} minutes (5-second delays)")
    print()
    
    results = []
    
    for i, contact in enumerate(PENDING_CONTACTS):
        print(f"[{i+1}/{len(PENDING_CONTACTS)}] {contact['name']} - {contact['company']}")
        print(f"  Email: {contact['email']}, Wave: {contact['wave']}")
        
        # Get template
        subject, body = get_dorada_template(
            contact['name'],
            contact['company'],
            contact['version']
        )
        
        # Send with rotation (5-second delay built in)
        success, account_used, error = rotator.send_email(
            to_email=contact['email'],
            to_name=contact['name'],
            subject=subject,
            body=body,
            delay_seconds=5
        )
        
        if success:
            print(f"  ✅ Sent using: {account_used}")
            results.append({
                "contact": contact['name'],
                "company": contact['company'],
                "email": contact['email'],
                "wave": contact['wave'],
                "success": True,
                "account": account_used,
                "timestamp": datetime.now().isoformat()
            })
        else:
            print(f"  ❌ Failed: {error}")
            results.append({
                "contact": contact['name'],
                "company": contact['company'],
                "email": contact['email'],
                "wave": contact['wave'],
                "success": False,
                "error": error,
                "timestamp": datetime.now().isoformat()
            })
        
        print()
    
    # Final stats
    rotator.print_stats()
    
    # Summary
    success_count = sum(1 for r in results if r['success'])
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total attempted: {len(PENDING_CONTACTS)}")
    print(f"Successfully sent: {success_count}")
    print(f"Failed: {len(PENDING_CONTACTS) - success_count}")
    
    # Account usage
    print("\nAccount usage:")
    stats = rotator.get_stats()
    for acc in stats['accounts']:
        print(f"  {acc['name']}: {acc['sent_today']} emails sent today")
    
    print("\nNote: Update dorada-outreach-campaign.md with sent dates")
    print("=" * 60)

if __name__ == "__main__":
    main()
