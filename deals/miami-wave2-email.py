#!/usr/bin/env python3
"""Miami Hotels Wave 2 - Send first email (Matt Djokovic)"""
from agentmail import AgentMail
from datetime import datetime

# Use API key from MEMORY.md
client = AgentMail(api_key="am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f")

# Wave 2 Contact 1
contact = {
    "name": "Matt",
    "company": "Mast-Jägermeister SE",
    "email": "mdjokovic@jagermeister.com"
}

subject = "Trophy oceanfront asset - Miami Beach (45 suites + 95-key expansion)"

text = f"""Dear {contact['name']},

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

Claw
Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""

try:
    result = client.inboxes.messages.send(
        inbox_id="zane@agentmail.to",
        to=contact["email"],
        cc=["sam@impactquadrant.info"],
        subject=subject,
        text=text
    )
    print(f"✅ SUCCESS: Sent to {contact['name']} at {contact['company']}")
    print(f"   Email: {contact['email']}")
    print(f"   Result: {result}")
    print(f"   Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
except Exception as e:
    print(f"❌ ERROR: {e}")
    print(f"   Attempted to send to: {contact['email']}")
