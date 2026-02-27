#!/usr/bin/env python3
"""
Dorada Resort - Complete Wave 2 & Start Wave 3 Outreach
Send emails to remaining Wave 2 contacts and begin Wave 3
"""

import requests
import json
from datetime import datetime

# AgentMail Configuration
AGENTMAIL_API_KEY = "am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
AGENTMAIL_INBOX = "Zane@agentmail.to"
CC_EMAIL = "sam@impactquadrant.info"
BASE_URL = "https://api.agentmail.to/v0"

# Contacts to send (Wave 2 remaining + Wave 3 start)
CONTACTS = [
    # Wave 2 - Remaining
    {
        "name": "Jack Ablin",
        "company": "Cresset",
        "email": "jablin@cressetcapital.com",
        "phone": "(562) 665-7402",
        "version": "family_office",
        "wave": 2,
        "contact_id": 5
    },
    {
        "name": "Rebecca Farrer",
        "company": "BHB Private",
        "email": "rf@bhbprivate.com",
        "phone": "",
        "version": "family_office",
        "wave": 2,
        "contact_id": 8
    },
    {
        "name": "Michael Bar",
        "company": "Fisher Brothers",
        "email": "mbar@fisherbrothers.com",
        "phone": "",
        "version": "institutional",
        "wave": 2,
        "contact_id": 9
    },
    {
        "name": "Lee Graham",
        "company": "The Graham Group",
        "email": "graham@thegrahamgroup.co.uk",
        "phone": "",
        "version": "family_office",
        "wave": 2,
        "contact_id": 10
    },
    # Wave 3 - First 2 contacts
    {
        "name": "Bob Rowling",
        "company": "TRT Holdings",
        "email": "bob.rowling@omnihotels.com",
        "phone": "(972) 871-5600",
        "version": "institutional",
        "wave": 3,
        "contact_id": 11
    },
    {
        "name": "Brendan O'Hara",
        "company": "TRT Holdings",
        "email": "brendan.ohara@omnihotels.com",
        "phone": "(972) 871-5600",
        "version": "institutional",
        "wave": 3,
        "contact_id": 12
    }
]

def generate_family_office_email(name, company):
    """Generate family office version email"""
    
    subject = f"Legacy wellness asset in Costa Rica - health preservation meets wealth preservation"
    
    text = f"""Dear {'Mr.' if not name.startswith('Rebecca') else 'Ms.'} {name.split()[1]},

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

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    
    return subject, text

def generate_institutional_email(name, company):
    """Generate institutional version email"""
    
    subject = f"Luxury wellness platform in Costa Rica - $2.1T market opportunity"
    
    text = f"""Dear {'Mr.' if not name.startswith('Julie') else 'Ms.'} {name.split()[1]},

I'm reaching out regarding **Dorada**, a category-defining luxury wellness and longevity platform in Costa Rica's Blue Zone.

Given {company}'s portfolio spanning hotels, healthcare, and wellness, I believe Dorada represents a strategic fit as a **multi-stream revenue platform**:

**Revenue Streams:**
- Luxury real estate sales and appreciation
- Hospitality and branded residence income
- High-margin longevity and performance programs (7-10 day intensives)
- Membership-based recurring revenues
- Farm-to-table dining and experiential services

**Core Differentiator:**
The **Longevity & Human Performance Center** delivers personalized, data-driven healthspan interventions—transforming Dorada from a destination into a **lifetime engagement model** with materially higher customer LTV.

**Asset Overview:**
- 300-acre protected development
- Ultra-low density, premium positioning
- Replicable model across Blue Zone geographies
- Brand extensibility into digital health and affiliated clinics

The global wellness and longevity economy is projected to reach **$2.1T by 2030** (12.4% CAGR). Dorada is positioned at the intersection of this trend with defensible scientific credibility.

Would you be open to reviewing the investor deck?

Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    
    return subject, text

def send_email(to_email, subject, text_content, cc=None):
    """Send an email via AgentMail API"""

    headers = {
        "Authorization": f"Bearer {AGENTMAIL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inbox_id": AGENTMAIL_INBOX,
        "to": [to_email],
        "subject": subject,
        "text": text_content
    }

    if cc:
        payload["cc"] = [cc] if isinstance(cc, str) else cc

    try:
        response = requests.post(
            f"{BASE_URL}/inboxes/{AGENTMAIL_INBOX}/messages",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return {"success": True, "response": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    """Main execution"""
    
    print("=" * 70)
    print(f"DORADA RESORT OUTREACH - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    print()
    
    results = []
    
    for contact in CONTACTS:
        print(f"Processing Wave {contact['wave']} - Contact #{contact['contact_id']}")
        print(f"  Company: {contact['company']}")
        print(f"  Contact: {contact['name']}")
        print(f"  Email: {contact['email']}")
        print(f"  Version: {contact['version']}")
        
        # Generate email based on version
        if contact['version'] == 'family_office':
            subject, body = generate_family_office_email(contact['name'], contact['company'])
        else:
            subject, body = generate_institutional_email(contact['name'], contact['company'])
        
        # Send email
        result = send_email(contact['email'], subject, body, cc=CC_EMAIL)
        
        if result['success']:
            print(f"  ✅ EMAIL SENT SUCCESSFULLY")
            status = "sent"
        else:
            print(f"  ❌ FAILED: {result['error']}")
            status = "failed"
        
        results.append({
            "wave": contact['wave'],
            "contact_id": contact['contact_id'],
            "company": contact['company'],
            "contact": contact['name'],
            "email": contact['email'],
            "status": status,
            "timestamp": datetime.now().isoformat()
        })
        
        print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    wave2_sent = sum(1 for r in results if r['wave'] == 2 and r['status'] == 'sent')
    wave3_sent = sum(1 for r in results if r['wave'] == 3 and r['status'] == 'sent')
    
    print(f"Wave 2 emails sent: {wave2_sent}/4")
    print(f"Wave 3 emails sent: {wave3_sent}/2")
    print(f"Total sent: {wave2_sent + wave3_sent}/6")
    print()
    print(f"All emails CC'd to: {CC_EMAIL}")
    print("=" * 70)
    
    # Save results
    output_file = f"/Users/cubiczan/.openclaw/workspace/dorada-outreach-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    main()
