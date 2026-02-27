#!/usr/bin/env python3
"""
Miami Hotels Wave 2 Outreach
Sends personalized emails to remaining Wave 2 buyers
"""

import sys
import time
from datetime import datetime

# Import rotation system
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scripts')
from gmail_rotation_simple import send_email_with_rotation

# Email templates from campaign
TEMPLATE_2_THESIS = """Dear {name},

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

Given {company}'s focus on {focus}, I believe this aligns with your investment criteria.

Would you be interested in reviewing the full package?"""

TEMPLATE_3_BOTH = """Dear {name},

I'm reaching out with two distinct Miami hospitality opportunities that may align with {company}'s investment focus:

**1. Tides South Beach & Tides Village**
- 45 luxury oceanfront suites (South Beach)
- 95-key expansion opportunity
- Direct beachfront with grandfathered rights
- Trophy positioning, ADR upside potential

**2. Thesis Hotel Miami**
- 245 hotel + 204 multifamily + 30K retail
- $315M asking, $18.1M NOI
- Student housing conversion potential
- Adjacent to University of Miami

Both assets offer:
- Strong Miami tourism fundamentals (12M+ visitors, $17B spend)
- Limited new supply dynamics
- Multiple exit pathways
- Institutional-scale opportunities

Would you like to review the confidential materials for either or both assets?"""

# Standard signature (will be appended by rotation system)
SIGNATURE = """Best,

Agent Manager

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info"""

# Wave 2 contacts
CONTACTS = [
    {
        "name": "Justin",
        "company": "Layla Capital",
        "email": "justin@laylacapital.com",
        "template": "template_3",
        "focus": "Florida hospitality investments",
        "subject": "Two Miami hospitality opportunities - Oceanfront trophy + Mixed-use campus"
    },
    {
        "name": "Maxwell",
        "company": "Layla Capital",
        "email": "max@laylacapital.com",
        "template": "template_3",
        "focus": "Florida hospitality investments",
        "subject": "Two Miami hospitality opportunities - Oceanfront trophy + Mixed-use campus"
    },
    {
        "name": "Andrea",
        "company": "East To West Capital",
        "email": "andrea.cassandro@investincapital.com",
        "template": "template_2",
        "focus": "student housing",
        "subject": "Mixed-use hospitality opportunity - $315M Miami asset near University of Miami"
    },
    {
        "name": "Joseph",
        "company": "Mandrake Capital Partners",
        "email": "joconnor@mandrakecapital.com",
        "template": "template_2",
        "focus": "hotel and student housing investments",
        "subject": "Mixed-use hospitality opportunity - $315M Miami asset near University of Miami"
    }
]

def send_wave2_emails():
    """Send Wave 2 emails"""
    print("=" * 60)
    print("🏨 MIAMI HOTELS - WAVE 2 OUTREACH")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Contacts to email: {len(CONTACTS)}")
    print()
    
    results = []
    
    for i, contact in enumerate(CONTACTS, 1):
        print(f"\n{'='*60}")
        print(f"📧 Email {i}/{len(CONTACTS)}: {contact['name']} {contact['company']}")
        print(f"   To: {contact['email']}")
        print(f"   Template: {contact['template']}")
        print()
        
        # Prepare email content
        if contact["template"] == "template_2":
            body = TEMPLATE_2_THESIS.format(
                name=contact["name"],
                company=contact["company"],
                focus=contact["focus"]
            )
        else:  # template_3
            body = TEMPLATE_3_BOTH.format(
                name=contact["name"],
                company=contact["company"]
            )
        
        # Send email with rotation
        success, message, account_used = send_email_with_rotation(
            to_emails=contact["email"],
            subject=contact["subject"],
            body_text=body,
            force_account=None  # Use rotation
        )
        
        result = {
            "contact": contact["name"],
            "company": contact["company"],
            "email": contact["email"],
            "success": success,
            "message": message,
            "account_used": account_used,
            "timestamp": datetime.now().isoformat()
        }
        results.append(result)
        
        if success:
            print(f"   ✅ SUCCESS")
        else:
            print(f"   ❌ FAILED: {message}")
        
        # Wait between emails to avoid rate limiting
        if i < len(CONTACTS):
            print(f"\n   ⏳ Waiting 3 seconds...")
            time.sleep(3)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 WAVE 2 SUMMARY")
    print("=" * 60)
    
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful
    
    print(f"✅ Successful: {successful}/{len(results)}")
    print(f"❌ Failed: {failed}/{len(results)}")
    print()
    
    if successful > 0:
        print("Emails sent to:")
        for r in results:
            if r["success"]:
                print(f"  • {r['contact']} ({r['company']}) - via {r['account_used']}")
    
    if failed > 0:
        print("\nFailed emails:")
        for r in results:
            if not r["success"]:
                print(f"  • {r['contact']} ({r['company']}) - {r['message']}")
    
    print()
    print("✅ WAVE 2 OUTREACH COMPLETE")
    
    return results

if __name__ == "__main__":
    results = send_wave2_emails()
