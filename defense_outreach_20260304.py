#!/usr/bin/env python3
"""
Defense Sector Outreach - March 4, 2026
Sends emails to defense companies and PE/VC funds
"""

import requests
import json
from datetime import datetime
import sys

# Configuration
API_KEY = "am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f"
FROM_EMAIL = "Zander@agentmail.to"
CC_EMAIL = "sam@impactquadrant.info"
BASE_URL = "https://api.agentmail.to/v0"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def send_email(to_email, to_name, subject, body):
    """Send email via AgentMail API"""
    payload = {
        "inbox_id": FROM_EMAIL,
        "to": [to_email],
        "cc": [CC_EMAIL],
        "subject": subject,
        "text": body
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/inboxes/{FROM_EMAIL}/messages/send",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return True, result.get('message_id', 'No ID')
        else:
            return False, f"HTTP {response.status_code}: {response.text[:100]}"
            
    except Exception as e:
        return False, str(e)

# Defense Companies (max 10)
companies = [
    {
        "name": "Helsing",
        "contact_name": "Partnerships Team",
        "email": "partnerships@helsing.ai",
        "sector": "AI-powered defense systems and electronic warfare"
    },
    {
        "name": "Shield AI",
        "contact_name": "Business Development",
        "email": "bd@shield.ai",
        "sector": "AI pilots for autonomous drones and GPS-denied environments"
    },
    {
        "name": "Anduril Industries",
        "contact_name": "Partnerships",
        "email": "partnerships@anduril.com",
        "sector": "Autonomous weapon systems and drone technology"
    },
    {
        "name": "Saronic",
        "contact_name": "Business Development",
        "email": "info@saronic.io",
        "sector": "Autonomous maritime vehicles for military operations"
    },
    {
        "name": "Quantum Systems",
        "contact_name": "Partnerships Team",
        "email": "info@quantum-systems.com",
        "sector": "AI drones for surveillance and decision-making"
    },
    {
        "name": "Firefly Aerospace",
        "contact_name": "Business Development",
        "email": "bd@fireflyspace.com",
        "sector": "Lunar landers, orbital vehicles, military satellite operations"
    },
    {
        "name": "Capella Space",
        "contact_name": "Partnerships",
        "email": "info@capellaspace.com",
        "sector": "SAR satellites for persistent monitoring"
    },
    {
        "name": "Skydio",
        "contact_name": "Business Development",
        "email": "sales@skydio.com",
        "sector": "Autonomous drones for defense applications"
    },
    {
        "name": "Forterra",
        "contact_name": "Partnerships",
        "email": "info@forterra.com",
        "sector": "Autonomous systems for defense sector"
    },
    {
        "name": "Applied Intuition",
        "contact_name": "Business Development",
        "email": "info@appliedintuition.com",
        "sector": "AI software for autonomous systems testing"
    }
]

# PE/VC Funds Asia/India (max 5)
investors = [
    {
        "name": "Drone Fund",
        "contact_name": "Investment Team",
        "email": "info@dronefund.jp",
        "fund_name": "Drone Fund"
    },
    {
        "name": "Public Investment Fund",
        "contact_name": "Investment Team",
        "email": "info@pif.gov.sa",
        "fund_name": "PIF"
    },
    {
        "name": "Mubadala Investment Company",
        "contact_name": "Investment Team",
        "email": "info@mubadala.com",
        "fund_name": "Mubadala"
    },
    {
        "name": "GIC Private Limited",
        "contact_name": "Investment Team",
        "email": "info@gic.com.sg",
        "fund_name": "GIC"
    },
    {
        "name": "Temasek Holdings",
        "contact_name": "Investment Team",
        "email": "info@temasek.com.sg",
        "fund_name": "Temasek"
    }
]

# Track results
results = {
    "companies_sent": 0,
    "companies_failed": 0,
    "investors_sent": 0,
    "investors_failed": 0,
    "errors": [],
    "timestamp": datetime.now().isoformat()
}

print("="*70)
print("Defense Sector Outreach - March 4, 2026")
print("="*70)
print(f"\nFrom: {FROM_EMAIL}")
print(f"CC: {CC_EMAIL}")
print(f"\nSending to {len(companies)} defense companies and {len(investors)} investors...")
print()

# Send to defense companies
print("📧 PART 1: DEFENSE COMPANIES")
print("-"*70)
for company in companies:
    subject = f"Strategic Partnership - {company['name']}"
    
    body = f"""Hi {company['contact_name']},

Regarding {company['name']}'s work in {company['sector']}.

Our group has 70+ years in defense and security, specializing in 
electromagnetic spectrum control and multi-domain solutions.

We seek partnerships in cybersecurity, AI/ML, counter-drone, 
space defense, and data analytics.

Open to a brief call?

Best,
Zander

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info
"""
    
    success, message = send_email(company['email'], company['contact_name'], subject, body)
    
    if success:
        print(f"✅ {company['name']}: {company['email']} - Message ID: {message}")
        results["companies_sent"] += 1
    else:
        print(f"❌ {company['name']}: {company['email']} - {message}")
        results["companies_failed"] += 1
        results["errors"].append(f"{company['name']}: {message}")

# Send to investors
print(f"\n📧 PART 2: PE/VC FUNDS (ASIA/INDIA)")
print("-"*70)
for investor in investors:
    subject = "Investment Opportunity - Drone Technology Platform"
    
    body = f"""Hi {investor['contact_name']},

I'm reaching out about a drone technology platform seeking growth capital.

**Company Profile:**
- Founded 2015 in India
- 3,000+ drones deployed, 190+ enterprise projects
- 20+ patents, 30+ platforms
- $13.8M revenue (FY25), 17-22% EBITDA margins
- $242M+ valuation (KPMG assessed)
- Expanding to US, Africa, South Asia
- Defense revenue: 15-20% FY26, 30% FY27

Sectors: Agriculture, inspections, surveillance, logistics, defense

Strategic partnership with Redington for nationwide distribution.

Would {investor['fund_name']} be interested in exploring this opportunity?

Best,
Zander

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info
"""
    
    success, message = send_email(investor['email'], investor['contact_name'], subject, body)
    
    if success:
        print(f"✅ {investor['name']}: {investor['email']} - Message ID: {message}")
        results["investors_sent"] += 1
    else:
        print(f"❌ {investor['name']}: {investor['email']} - {message}")
        results["investors_failed"] += 1
        results["errors"].append(f"{investor['name']}: {message}")

# Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"\nDefense Companies:")
print(f"  ✅ Sent: {results['companies_sent']}")
print(f"  ❌ Failed: {results['companies_failed']}")
print(f"\nPE/VC Funds:")
print(f"  ✅ Sent: {results['investors_sent']}")
print(f"  ❌ Failed: {results['investors_failed']}")
print(f"\nTotal: {results['companies_sent'] + results['investors_sent']} sent, {results['companies_failed'] + results['investors_failed']} failed")

if results['errors']:
    print(f"\nErrors:")
    for error in results['errors']:
        print(f"  - {error}")

# Save results to JSON
output_file = f"/Users/cubiczan/.openclaw/workspace/defense_outreach_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to: {output_file}")
print("="*70)

# Return summary for Discord reporting
print("\n📋 DISCORD REPORT:")
print(f"Defense Sector Outreach Complete - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(f"Sent: {results['companies_sent'] + results['investors_sent']} emails")
print(f"  • {results['companies_sent']} defense companies")
print(f"  • {results['investors_sent']} PE/VC funds (Asia/India)")
if results['companies_failed'] + results['investors_failed'] > 0:
    print(f"Failed: {results['companies_failed'] + results['investors_failed']} emails")
