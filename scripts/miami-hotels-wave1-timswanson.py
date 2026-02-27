#!/usr/bin/env python3
"""
Miami Hotels Wave 1 - Tim Swanson (Marsh McLennan)
Send via AgentMail API
"""

import requests
import json
from datetime import datetime

# AgentMail Configuration
AGENTMAIL_API_KEY = "am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
AGENTMAIL_INBOX = "zane@agentmail.to"
CC_EMAIL = "sam@impactquadrant.info"
BASE_URL = "https://api.agentmail.to/v0"

# Contact Info
CONTACT = {
    "name": "Tim Swanson",
    "company": "Marsh McLennan Agency",
    "title": "CIO",
    "email": "tim.swanson@marshmma.com",
    "template": "Template 2 (Thesis Hotel)"
}

def send_email(to_email, subject, text_content, html_content=None, cc=None):
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

    if html_content:
        payload["html"] = html_content

    if cc:
        payload["cc"] = [cc] if isinstance(cc, str) else cc

    try:
        response = requests.post(
            f"{BASE_URL}/inboxes/{AGENTMAIL_INBOX}/messages",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            return {
                "success": True,
                "message_id": response.json().get("message_id"),
                "response": response.json()
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def create_thesis_email(contact):
    """Create Thesis Hotel email (Template 2)"""
    
    first_name = contact["name"].split()[0]
    company = contact["company"]
    
    subject = "Mixed-use hospitality opportunity - $315M Miami asset near University of Miami"
    
    text_content = f"""Dear {first_name},

I'm reaching out regarding an institutional-scale mixed-use asset in Coral Gables, Florida—Thesis Hotel Miami.

Asset Overview:
- Location: 1350 S Dixie Hwy, adjacent to University of Miami
- Composition: 245 hotel keys + 204 multifamily units + 30K sq ft retail
- Asking Price: $315,000,000
- NOI: $18,128,000
- Debt: $150M assumable at 4.65% (significant value)

Multifamily Performance:
- 99% occupancy
- 80-90 person waiting list (UM students + medical staff)
- Strong demand driver with institutional backing

Investment Optionality:
1. Hotel + Multifamily Hold: Current income + retail lease-up upside
2. Student Housing Conversion: Up to 245 keys convertible to student housing
3. Hotel-Only Acquisition: Seller can separate components
4. Densification: Zoning allows additional residential density

Process: LOI + proof of funds + buyer bio required to proceed.

Given {company}'s focus on mixed-use investments and portfolio diversification, I believe this aligns with your investment criteria.

Would you be interested in reviewing the full package?

Best regards,

Sam Desigan
Agent Manager
Impact Quadrant

For follow-up, please reach out to Sam Desigan at Sam@impactquadrant.info.
"""

    html_content = f"""<p>Dear {first_name},</p>

<p>I'm reaching out regarding an institutional-scale mixed-use asset in Coral Gables, Florida—<strong>Thesis Hotel Miami</strong>.</p>

<h3>Asset Overview:</h3>
<ul>
<li><strong>Location:</strong> 1350 S Dixie Hwy, adjacent to University of Miami</li>
<li><strong>Composition:</strong> 245 hotel keys + 204 multifamily units + 30K sq ft retail</li>
<li><strong>Asking Price:</strong> $315,000,000</li>
<li><strong>NOI:</strong> $18,128,000</li>
<li><strong>Debt:</strong> $150M assumable at 4.65% (significant value)</li>
</ul>

<h3>Multifamily Performance:</h3>
<ul>
<li>99% occupancy</li>
<li>80-90 person waiting list (UM students + medical staff)</li>
<li>Strong demand driver with institutional backing</li>
</ul>

<h3>Investment Optionality:</h3>
<ol>
<li><strong>Hotel + Multifamily Hold:</strong> Current income + retail lease-up upside</li>
<li><strong>Student Housing Conversion:</strong> Up to 245 keys convertible to student housing</li>
<li><strong>Hotel-Only Acquisition:</strong> Seller can separate components</li>
<li><strong>Densification:</strong> Zoning allows additional residential density</li>
</ol>

<p><strong>Process:</strong> LOI + proof of funds + buyer bio required to proceed.</p>

<p>Given {company}'s focus on mixed-use investments and portfolio diversification, I believe this aligns with your investment criteria.</p>

<p>Would you be interested in reviewing the full package?</p>

<p>Best regards,<br>
Sam Desigan<br>
Agent Manager<br>
Impact Quadrant</p>

<p>For follow-up, please reach out to Sam Desigan at Sam@impactquadrant.info.</p>
"""

    return {
        "to": contact["email"],
        "subject": subject,
        "text": text_content,
        "html": html_content
    }

def main():
    print("\n" + "="*70)
    print("Miami Hotels Wave 1 - Tim Swanson (Marsh McLennan)")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")
    
    print(f"Contact: {CONTACT['name']} ({CONTACT['title']}, {CONTACT['company']})")
    print(f"Email: {CONTACT['email']}")
    print(f"Template: {CONTACT['template']}")
    print(f"CC: {CC_EMAIL}\n")
    
    email_data = create_thesis_email(CONTACT)
    
    print("Attempting to send via AgentMail API...")
    result = send_email(
        to_email=email_data["to"],
        subject=email_data["subject"],
        text_content=email_data["text"],
        html_content=email_data["html"],
        cc=CC_EMAIL
    )
    
    if result['success']:
        print(f"\n✅ Email sent successfully!")
        print(f"Message ID: {result['message_id']}")
        print(f"\n{'='*70}")
        print("Wave 1 Progress: 3/4 contacts emailed")
        print("  ✅ 1/4: Jihad Hazzan (ALFAHIM) - Sent 2026-02-21")
        print("  ✅ 2/4: David Stein (Long Wharf Capital) - Sent 2026-02-22")
        print("  ✅ 3/4: Tim Swanson (Marsh McLennan) - Sent 2026-02-23")
        print("  ⬜ 4/4: Jon Flood (Roseview) - Pending")
        print(f"{'='*70}\n")
        return 0
    else:
        print(f"\n❌ Error sending email: {result['error']}")
        print("\n" + "="*70)
        print("FALLBACK REQUIRED: AgentMail API not responding")
        print("Manual send needed or alternative SMTP required")
        print("="*70)
        return 1

if __name__ == "__main__":
    exit(main())
