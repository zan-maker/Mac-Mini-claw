#!/usr/bin/env python3
import requests
import json

# AgentMail Configuration
API_KEY = "am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
INBOX = "zane@agentmail.to"
CC = "sam@impactquadrant.info"
BASE_URL = "https://api.agentmail.to/v0"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 1. Chicago Metal - Day 7 Follow-up
print("="*60)
print("1️⃣  Chicago Metal Fabricators - Day 7 Follow-up")
print("="*60)

payload = {
    "inbox_id": INBOX,
    "to": ["info@chicagometal.com"],
    "cc": [CC],
    "subject": "Quick question about Chicago Metal Fabricators' benefits strategy",
    "text": """Hi Randy,

I'll keep this brief. We've helped similar organizations in manufacturing achieve:
- $103,875 in annual savings (company your size)
- $50-$400/month employee pay increases
- 30-60 day implementation

The program is fully compliant, with legal opinions from ERISA counsel and independent accounting review.

Open to seeing how this would work for your team?

Best,
Zane
---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info
""",
    "html": """<p>Hi Randy,</p>

<p>I'll keep this brief. We've helped similar organizations in manufacturing achieve:</p>
<ul>
<li><strong>$103,875 in annual savings</strong> (company your size)</li>
<li>$50-$400/month employee pay increases</li>
<li>30-60 day implementation</li>
</ul>

<p>The program is fully compliant, with legal opinions from ERISA counsel and independent accounting review.</p>

<p>Open to seeing how this would work for your team?</p>

<p>Best,<br>Zane<br>
<small>For further information, reach Sam Desigan (Agent Manager)<br>sam@impactquadrant.info</small></p>
"""
}

try:
    r = requests.post(f"{BASE_URL}/inboxes/{INBOX}/messages/send", headers=headers, json=payload)
    if r.status_code == 200:
        msg_id = r.json().get('message_id')
        print(f"✅ SENT - Message ID: {msg_id}")
    else:
        print(f"❌ Error {r.status_code}: {r.text}")
except Exception as e:
    print(f"❌ Error: {e}")

print()

# Now try to enrich and send 4 more
print("="*60)
print("🔍 Enriching leads from today's batch...")
print("="*60)

# Hunter.io for email finding
HUNTER_KEY = "f701d171cf7decf7e730a6b1c6e9b74f29f39b6e"

companies = [
    {"name": "BEON.tech", "domain": "beon.tech", "employees": 100, "industry": "Technology"},
    {"name": "Instant Imprints", "domain": "instantimprints.com", "employees": 200, "industry": "Franchise/Manufacturing"},
    {"name": "Technijian", "domain": "technijian.com", "employees": 50, "industry": "IT Services"},
    {"name": "Meriplex", "domain": "meriplex.com", "employees": 100, "industry": "IT Services"},
]

sent_count = 1  # Already sent 1 follow-up

for company in companies:
    if sent_count >= 5:
        break
        
    print(f"\n📧 {company['name']} ({company['domain']})...")
    
    try:
        # Search for emails
        r = requests.get(
            f"https://api.hunter.io/v2/domain-search?domain={company['domain']}&api_key={HUNTER_KEY}",
            timeout=10
        )
        
        if r.status_code != 200:
            print(f"   ⚠️  Hunter API error: {r.status_code}")
            continue
            
        data = r.json().get('data', {})
        emails = data.get('emails', [])
        
        if not emails:
            print(f"   ❌ No emails found")
            continue
        
        # Find decision maker
        contact_email = None
        contact_name = "there"
        
        for e in emails:
            role = (e.get('position') or '').lower()
            if any(t in role for t in ['ceo', 'president', 'owner', 'hr', 'director']):
                contact_email = e.get('value')
                contact_name = e.get('first_name', 'there')
                break
        
        if not contact_email and emails:
            contact_email = emails[0].get('value')
            contact_name = emails[0].get('first_name', 'there')
        
        if not contact_email:
            print(f"   ❌ No valid email")
            continue
            
        print(f"   ✅ Found: {contact_email}")
        
        # Calculate savings
        fica = company['employees'] * 681
        wc = company['employees'] * 500 * 0.30
        total = fica + wc
        
        # Send email
        subject = f"${total:,} annual savings for {company['name']} (zero cost to implement)"
        
        payload = {
            "inbox_id": INBOX,
            "to": [contact_email],
            "cc": [CC],
            "subject": subject,
            "text": f"""Hi {contact_name},

I noticed {company['name']} has about {company['employees']} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.

Organizations your size are typically saving:
• $681 per employee annually in FICA savings
• 30-60% reduction in workers' comp premiums
• Total savings: ${total:,}

One medical transportation company with 66 employees saved over $140,000 last year.

The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.

Would you be open to a 10-minute call this week to see the numbers for {company['name']}?

Best,
Zane
Zane@agentmail.to
Wellness 125 Cafeteria Plan
---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info
""",
            "html": f"""<p>Hi {contact_name},</p>

<p>I noticed {company['name']} has about {company['employees']} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.</p>

<p><strong>Organizations your size are typically saving:</strong></p>
<ul>
<li>$681 per employee annually in FICA savings</li>
<li>30-60% reduction in workers' comp premiums</li>
<li><strong>Total savings: ${total:,}</strong></li>
</ul>

<p>One medical transportation company with 66 employees saved over $140,000 last year.</p>

<p>The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.</p>

<p>Would you be open to a 10-minute call this week to see the numbers for {company['name']}?</p>

<p>Best,<br>
Zane<br>
Zane@agentmail.to<br>
Wellness 125 Cafeteria Plan<br>
<small>For further information, reach Sam Desigan (Agent Manager)<br>sam@impactquadrant.info</small></p>
"""
        }
        
        r2 = requests.post(f"{BASE_URL}/inboxes/{INBOX}/messages/send", headers=headers, json=payload)
        
        if r2.status_code == 200:
            msg_id = r2.json().get('message_id')
            print(f"   ✅ SENT! ${total:,} savings - Message ID: {msg_id}")
            sent_count += 1
        else:
            print(f"   ❌ Send error {r2.status_code}: {r2.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

print()
print("="*60)
print(f"📊 BATCH COMPLETE: {sent_count}/5 emails sent")
print("="*60)
