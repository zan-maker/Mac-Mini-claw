#!/usr/bin/env python3
"""
Send expense reduction outreach emails to enriched leads
Uses AgentMail API to send personalized emails
"""

import os
import requests
import json
from datetime import datetime

# AgentMail API configuration
AGENTMAIL_API_KEY = "am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
FROM_EMAIL = "zane@agentmail.to"
CC_EMAIL = "sam@impactquadrant.info"

# Contacts enriched via Tavily
leads = [
    {
        "company": "Precision Products Machining Group",
        "contact": "Don Brown",
        "title": "CEO",
        "email": "dbrown@precprodmachgrp.com",
        "phone": "630-543-9570",
        "location": "Addison, IL",
        "industry": "Precision Manufacturing",
        "score": 87
    },
    {
        "company": "Midwest Foods",
        "contact": "Erin Fitzgerald",
        "title": "Owner/President",
        "email": "efitzgerald@midwestfoods.com",
        "phone": "773-927-8870",
        "location": "Chicago, IL",
        "industry": "Food Distribution",
        "score": 82
    },
    {
        "company": "Industrial Supply Company",
        "contact": "Jessica Yurgaitis",
        "title": "CEO",
        "email": "jyurgaitis@indsupply.com",
        "phone": "801-532-1234",
        "location": "Salt Lake City, UT",
        "industry": "Industrial Distribution",
        "score": 84
    },
    {
        "company": "Peninsula Building Materials",
        "contact": "Leadership Team",
        "title": "Executive Team",
        "email": "PGshowroom@pbm1923.com",
        "phone": "877-282-0522",
        "location": "San Francisco Bay Area, CA",
        "industry": "Building Materials",
        "score": 79
    }
]

def send_agentmail_email(to_email, to_name, company, subject, body):
    """Send email via AgentMail API"""
    
    url = "https://api.agentmail.to/v1/emails"
    
    headers = {
        "Authorization": f"Bearer {AGENTMAIL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "from": FROM_EMAIL,
        "to": [to_email],
        "cc": [CC_EMAIL],
        "subject": subject,
        "body": body
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return {"success": True, "response": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}

def generate_email_body(contact_name, company, industry, score):
    """Generate personalized email body"""
    
    # Estimate savings based on score (15-25% of expenses)
    savings_pct = 15 + (score - 70) * 0.5
    
    body = f"""Hi {contact_name},

I hope this message finds you well. I'm reaching out because we've identified {company} as an excellent candidate for our expense reduction program.

Our team specializes in helping {industry} companies reduce operating expenses by {savings_pct:.0f}% without compromising quality or service levels. We've successfully partnered with similar organizations and consistently deliver:

✓ 15-25% reduction in telecommunications, waste management, and utility costs
✓ 100% contingency-based model - you only pay from savings generated
✓ Zero upfront costs or risks to your organization

Given {company}'s profile and industry position, we're confident we can identify significant savings opportunities across your vendor contracts and operational expenses.

Would you be open to a brief 15-minute call next week to explore potential areas where we might help reduce costs? I'd be happy to share specific examples from similar {industry} companies.

If you're not the right person to speak with about this, could you point me in the right direction?

Best regards,

Zane
Impact Quadrant
sam@impactquadrant.info

P.S. Our average client saves $75,000-$150,000 annually, and there's absolutely no cost unless we deliver measurable savings.
"""
    
    return body

def main():
    """Main execution"""
    
    print(f"\n{'='*60}")
    print(f"EXPENSE REDUCTION OUTREACH - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")
    
    results = []
    
    for lead in leads:
        print(f"Processing: {lead['company']}")
        print(f"  Contact: {lead['contact']} ({lead['title']})")
        print(f"  Email: {lead['email']}")
        print(f"  Score: {lead['score']}")
        
        # Generate email
        subject = f"Quick question about {lead['company']}'s operating expenses"
        body = generate_email_body(
            lead['contact'].split()[0],  # First name
            lead['company'],
            lead['industry'],
            lead['score']
        )
        
        # Send email
        result = send_agentmail_email(
            lead['email'],
            lead['contact'],
            lead['company'],
            subject,
            body
        )
        
        if result['success']:
            print(f"  ✅ SENT SUCCESSFULLY")
            results.append({
                "company": lead['company'],
                "contact": lead['contact'],
                "email": lead['email'],
                "score": lead['score'],
                "status": "sent",
                "timestamp": datetime.now().isoformat()
            })
        else:
            print(f"  ❌ FAILED: {result['error']}")
            results.append({
                "company": lead['company'],
                "contact": lead['contact'],
                "email": lead['email'],
                "score": lead['score'],
                "status": "failed",
                "error": result['error'],
                "timestamp": datetime.now().isoformat()
            })
        
        print()
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    sent_count = sum(1 for r in results if r['status'] == 'sent')
    print(f"Total leads: {len(results)}")
    print(f"Emails sent: {sent_count}")
    print(f"Failed: {len(results) - sent_count}")
    
    # Save results
    output_file = f"/Users/cubiczan/.openclaw/workspace/outreach-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {output_file}\n")

if __name__ == "__main__":
    main()
