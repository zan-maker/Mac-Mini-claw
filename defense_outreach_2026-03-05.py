#!/usr/bin/env python3
"""Defense Sector Outreach - 2026-03-05"""
from agentmail import AgentMail
import json
from datetime import datetime

# Initialize client with provided API key
client = AgentMail(api_key="am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f")

# Part 1: Defense Companies
companies = [
    {
        "name": "Aetherflux",
        "email": "partnerships@aetherflux.com",
        "sector": "Space-Based Solar Power",
        "priority": "High"
    },
    {
        "name": "Antares Industries",
        "email": "info@antaresindustries.com",
        "sector": "Nuclear Microreactors",
        "priority": "High"
    },
    {
        "name": "Theseus Tech",
        "email": "info@theseus.us",
        "sector": "Drone Navigation Systems",
        "priority": "High"
    },
    {
        "name": "Scale AI",
        "email": "partnerships@scale.com",
        "sector": "AI Infrastructure",
        "priority": "High"
    },
    {
        "name": "DarkSaber Labs",
        "email": "info@darksaberlabs.com",
        "sector": "Tactical AI Systems",
        "priority": "Medium"
    },
    {
        "name": "Warfytr AI",
        "email": "info@warfytr.ai",
        "sector": "Battlefield AI",
        "priority": "Medium"
    },
    {
        "name": "Aurum Systems",
        "email": "info@aurum.systems",
        "sector": "Mission Planning Platforms",
        "priority": "Medium"
    },
    {
        "name": "Deca Defense",
        "email": "info@decadefense.com",
        "sector": "AI/ML Defense Systems",
        "priority": "Medium"
    },
    {
        "name": "Xebec Systems",
        "email": "info@xebec-systems.com",
        "sector": "Airborne Defense",
        "priority": "Medium"
    },
    {
        "name": "Wild West Systems",
        "email": "info@wildwestsystems.com",
        "sector": "Autonomous Drones",
        "priority": "Low"
    }
]

# Part 2: PE/VC Investors (Asia/India)
investors = [
    {
        "name": "BEENEXT",
        "email": "hero@beenext.com",
        "region": "Asia/India",
        "priority": "High"
    },
    {
        "name": "Vertex Ventures",
        "email": "info@vertexventures.com",
        "region": "Asia/Global",
        "priority": "High"
    },
    {
        "name": "Sequoia Capital India",
        "email": "info@sequoiacap.com",
        "region": "India",
        "priority": "High"
    },
    {
        "name": "Accel India",
        "email": "india@accel.com",
        "region": "India",
        "priority": "Medium"
    },
    {
        "name": "Matrix Partners India",
        "email": "info@matrixpartners.com",
        "region": "India",
        "priority": "Medium"
    }
]

results = {
    "companies": [],
    "investors": [],
    "summary": {
        "total_sent": 0,
        "total_failed": 0
    }
}

# Send to Defense Companies
print("=== Sending Defense Company Outreach ===")
for company in companies[:10]:  # Max 10 companies
    subject = f"Strategic Partnership - {company['name']}"
    text = f"""Hi,

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
sam@impactquadrant.info"""

    try:
        result = client.inboxes.messages.send(
            inbox_id="zander@agentmail.to",
            to=company["email"],
            cc=["sam@impactquadrant.info"],
            subject=subject,
            text=text
        )
        print(f"✅ {company['name']}: Sent")
        results["companies"].append({
            "name": company["name"],
            "email": company["email"],
            "status": "sent",
            "message_id": result.get("id", "unknown"),
            "timestamp": datetime.now().isoformat()
        })
        results["summary"]["total_sent"] += 1
    except Exception as e:
        print(f"❌ {company['name']}: {str(e)}")
        results["companies"].append({
            "name": company["name"],
            "email": company["email"],
            "status": "failed",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
        results["summary"]["total_failed"] += 1

# Send to Investors
print("\n=== Sending Investor Outreach ===")
for investor in investors[:5]:  # Max 5 investors
    subject = f"Investment Opportunity - Drone Technology Platform"
    text = f"""Hi,

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

Would {investor['name']} be interested in exploring this opportunity?

Best,
Zander

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info"""

    try:
        result = client.inboxes.messages.send(
            inbox_id="zander@agentmail.to",
            to=investor["email"],
            cc=["sam@impactquadrant.info"],
            subject=subject,
            text=text
        )
        print(f"✅ {investor['name']}: Sent")
        results["investors"].append({
            "name": investor["name"],
            "email": investor["email"],
            "status": "sent",
            "message_id": result.get("id", "unknown"),
            "timestamp": datetime.now().isoformat()
        })
        results["summary"]["total_sent"] += 1
    except Exception as e:
        print(f"❌ {investor['name']}: {str(e)}")
        results["investors"].append({
            "name": investor["name"],
            "email": investor["email"],
            "status": "failed",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
        results["summary"]["total_failed"] += 1

# Save results
output_file = f"/Users/cubiczan/.openclaw/workspace/defense-leads/outreach-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n=== Summary ===")
print(f"Total Sent: {results['summary']['total_sent']}")
print(f"Total Failed: {results['summary']['total_failed']}")
print(f"Results saved to: {output_file}")
