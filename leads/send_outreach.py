#!/usr/bin/env python3
"""Send outreach emails via AgentMail SDK"""
from agentmail import AgentMail

# Initialize client
client = AgentMail(api_key="am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68")

# HIGH Priority Leads
leads = [
    {
        "company": "Hospice Care Partners",
        "email": "hr@hospicecarepartners.com",
        "employees": 120,
        "savings": 99720
    },
    {
        "company": "Sunrise Senior Living - Phoenix",
        "email": "hr@sunriseseniorliving.com",
        "employees": 85,
        "savings": 70635
    },
    {
        "company": "Premier Hotel Group",
        "email": "hr@premierhotelgroup.com",
        "employees": 150,
        "savings": 124650
    }
]

results = {"sent": 0, "errors": []}

for lead in leads:
    subject = f"${lead['savings']:,} annual savings for {lead['company']} (zero cost to implement)"
    text = f"""Hi HR Director,

I noticed {lead['company']} has about {lead['employees']} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.

Organizations your size are typically saving:
• $681 per employee annually in FICA savings
• 30-60% reduction in workers' comp premiums
• Total savings: ${lead['savings']:,}

One medical transportation company with 66 employees saved over $140,000 last year.

The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.

Would you be open to a 10-minute call this week to see the numbers for {lead['company']}?

Best,
Zane
Zane@agentmail.to
Wellness 125 Cafeteria Plan"""

    try:
        result = client.inboxes.messages.send(
            inbox_id="zane@agentmail.to",
            to=lead["email"],
            cc=["sam@impactquadrant.info"],
            subject=subject,
            text=text
        )
        print(f"✅ Sent to {lead['company']}: {result}")
        results["sent"] += 1
    except Exception as e:
        print(f"❌ Error sending to {lead['company']}: {e}")
        results["errors"].append({"company": lead["company"], "error": str(e)})

print(f"\n=== Summary ===")
print(f"Sent: {results['sent']}")
print(f"Errors: {len(results['errors'])}")
