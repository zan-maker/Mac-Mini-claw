#!/usr/bin/env python3
"""
Send final Dorada campaign email to Christopher Sutphen (Oxford Capital)
"""

import requests
import json
from datetime import datetime

# AgentMail Configuration
AGENTMAIL_API_KEY = "am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
AGENTMAIL_INBOX = "zane@agentmail.to"
BASE_URL = "https://api.agentmail.to/v0"

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

    # Add CC if provided
    if cc:
        payload["cc"] = [cc] if isinstance(cc, str) else cc

    try:
        response = requests.post(
            f"{BASE_URL}/inboxes/{AGENTMAIL_INBOX}/messages/send",
            headers=headers,
            json=payload
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

# Email content
to_email = "csutphen@oxford-capital.com"
cc_email = "sam@impactquadrant.info"
subject = "Luxury wellness resort opportunity - Costa Rica Blue Zone"

text_content = """Dear Mr. Sutphen,

I'm reaching out regarding Dorada, a first-of-its-kind regenerative destination resort and residential community in one of the world's rare Blue Zone regions of Costa Rica.

Given Oxford Capital's focus on hotels, resorts, and mixed-use developments, I believe Dorada aligns with your investment philosophy—particularly as a multi-generational legacy asset that combines:

- 300-acre protected bio-reserve with panoramic ocean views
- 40 private estate homes (1+ acre lots)
- Longevity & Human Performance Center offering personalized healthspan programs
- Fully off-grid with sustainable infrastructure
- Recurring revenue from wellness programs and memberships

Dorada is the vision of Dr. Vincent Giampapa, a globally recognized leader in anti-aging medicine and regenerative science. It's designed not as a hospitality project, but as a permanent wellness ecosystem for long-term ownership.

Why for family offices: Capital preservation with upside, intergenerational relevance, personal use optionality, and alignment with the $2.1T wellness economy (12.4% CAGR).

Would you be open to a brief call to discuss the opportunity? I'd be happy to share the full investor deck.

Best,
Agent Manager

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info"""

# Send email
print(f"Sending email to {to_email}...")
result = send_email(to_email, subject, text_content, cc=cc_email)

if result["success"]:
    print(f"✅ Email sent successfully!")
    print(f"   Message ID: {result['message_id']}")
    print(f"   To: {to_email}")
    print(f"   CC: {cc_email}")
    print(f"   Subject: {subject}")
else:
    print(f"❌ Failed to send email")
    print(f"   Error: {result['error']}")

# Save result to file
with open("/Users/cubiczan/.openclaw/workspace/memory/sutphen-email-result.json", "w") as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "to": to_email,
        "cc": cc_email,
        "subject": subject,
        "result": result
    }, f, indent=2)

print(f"\nResult saved to: memory/sutphen-email-result.json")
