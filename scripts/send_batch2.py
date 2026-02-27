#!/usr/bin/env python3
import requests

API_KEY = "am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
INBOX = "zane@agentmail.to"
CC = "sam@impactquadrant.info"
BASE_URL = "https://api.agentmail.to/v0"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Companies to try with standard info@ emails
# From today's leads that aren't in pipeline yet
companies = [
    {
        "name": "BEON.tech",
        "email": "info@beon.tech",
        "employees": 100,
        "industry": "Technology/Staff Augmentation"
    },
    {
        "name": "Texas Injection Molding",  # Already in pipeline, skip
        "email": "info@texasinjectionmolding.com",
        "employees": 50,
        "skip": True
    },
    {
        "name": "USA Compression Partners",
        "email": "info@usacompression.com",
        "employees": 200,
        "industry": "Energy/Manufacturing"
    },
    {
        "name": "Wisconsin Aluminum Foundry",
        "email": "info@wafco.com",
        "employees": 200,
        "industry": "Manufacturing"
    },
    {
        "name": "Best Fitness",
        "email": "info@bestfitness.com",
        "employees": 100,
        "industry": "Healthcare/Fitness"
    }
]

sent = 0
for company in companies:
    if company.get('skip'):
        continue
        
    print(f"📧 {company['name']}...")
    
    # Calculate savings
    fica = company['employees'] * 681
    wc = company['employees'] * 500 * 0.30
    total = fica + wc
    
    subject = f"${total:,} annual savings for {company['name']} (zero cost to implement)"
    
    payload = {
        "inbox_id": INBOX,
        "to": [company['email']],
        "cc": [CC],
        "subject": subject,
        "text": f"""Hi,

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
        "html": f"""<p>Hi,</p>

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
Wellness 125 Cafeteria Plan</p>
<p><small>For further information, reach Sam Desigan (Agent Manager)<br>sam@impactquadrant.info</small></p>
"""
    }
    
    try:
        r = requests.post(f"{BASE_URL}/inboxes/{INBOX}/messages/send", headers=headers, json=payload, timeout=15)
        if r.status_code == 200:
            msg_id = r.json().get('message_id')
            print(f"   ✅ SENT! ${total:,} savings - ID: {msg_id}")
            sent += 1
        else:
            print(f"   ❌ Error {r.status_code}")
    except Exception as e:
        print(f"   ❌ {e}")
    
    if sent >= 4:  # We already sent 1 follow-up
        break

print(f"\n📊 Total sent this batch: {sent}")
