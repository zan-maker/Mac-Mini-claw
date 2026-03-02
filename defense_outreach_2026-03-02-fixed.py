#!/usr/bin/env python3
"""
Defense Sector Outreach - 2026-03-02
Sends emails to defense companies and PE/VC funds in Asia/India
"""

import requests
import json
from datetime import datetime
from pathlib import Path

# Configuration
API_KEY = "am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f"
BASE_URL = "https://api.agentmail.to/v0"
FROM_EMAIL = "Zander@agentmail.to"
CC_EMAIL = "sam@impactquadrant.info"
FROM_NAME = "Zander"

# Headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Defense Companies (Top 10)
defense_companies = [
    {
        "name": "Shield AI",
        "contact_name": "Leadership Team",
        "sector": "AI & Autonomous Systems",
        "email": "contact@shield.ai",
        "priority": "HIGH"
    },
    {
        "name": "Anduril Industries",
        "contact_name": "Leadership Team",
        "sector": "Autonomous Systems & Counter-Drone",
        "email": "contact@anduril.com",
        "priority": "HIGH"
    },
    {
        "name": "Skydio",
        "contact_name": "Leadership Team",
        "sector": "Autonomous Drones",
        "email": "contact@skydio.com",
        "priority": "HIGH"
    },
    {
        "name": "Chaos Industries",
        "contact_name": "Leadership Team",
        "sector": "Defense Manufacturing",
        "email": "contact@chaosindustries.com",
        "priority": "HIGH"
    },
    {
        "name": "Epirus",
        "contact_name": "Leadership Team",
        "sector": "Counter-Drone (C-UAS)",
        "email": "contact@epirusinc.com",
        "priority": "HIGH"
    },
    {
        "name": "Onebrief",
        "contact_name": "Leadership Team",
        "sector": "Defense Data Analytics / ISR",
        "email": "contact@onebrief.com",
        "priority": "MEDIUM"
    },
    {
        "name": "Hidden Level",
        "contact_name": "Leadership Team",
        "sector": "Counter-Drone / Surveillance",
        "email": "contact@hiddenlevel.com",
        "priority": "MEDIUM"
    },
    {
        "name": "Rebellion Defense",
        "contact_name": "Leadership Team",
        "sector": "AI & Defense Software",
        "email": "contact@rebelliondefense.com",
        "priority": "MEDIUM"
    },
    {
        "name": "Palantir Technologies",
        "contact_name": "Partnerships Team",
        "sector": "Defense Data Analytics",
        "email": "partnerships@palantir.com",
        "priority": "MEDIUM"
    },
    {
        "name": "Astranis",
        "contact_name": "Leadership Team",
        "sector": "Space-Based Defense",
        "email": "contact@astranis.com",
        "priority": "MEDIUM"
    }
]

# PE/VC Investors (Top 5)
investors = [
    {
        "name": "General Catalyst",
        "contact_name": "Investment Team",
        "email": "india@generalcatalyst.com",
        "priority": "HIGH"
    },
    {
        "name": "Lightspeed Venture Partners",
        "contact_name": "Investment Team",
        "email": "india@lightspeedvp.com",
        "priority": "HIGH"
    },
    {
        "name": "Accel Partners",
        "contact_name": "Investment Team",
        "email": "india@accel.com",
        "priority": "HIGH"
    },
    {
        "name": "BEENEXT",
        "contact_name": "Investment Team",
        "email": "contact@beenext.com",
        "priority": "HIGH"
    },
    {
        "name": "Vertex Ventures",
        "contact_name": "Investment Team",
        "email": "contact@vertexventures.com",
        "priority": "MEDIUM"
    }
]

def send_email(to_email, subject, text_content, html_content=None, cc=None):
    """Send an email via AgentMail API"""

    payload = {
        "inbox_id": FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "text": text_content
    }

    # Add HTML version if provided
    if html_content:
        payload["html"] = html_content

    # Add CC if provided
    if cc:
        payload["cc"] = [cc] if isinstance(cc, str) else cc

    try:
        response = requests.post(
            f"{BASE_URL}/inboxes/{FROM_EMAIL}/messages/send",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code in [200, 201]:
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

def send_company_email(company):
    """Send email to defense company"""
    
    subject = f"Strategic Partnership - {company['name']}"
    
    text = f"""Hi {company['contact_name']},

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
    
    html = f"""<p>Hi {company['contact_name']},</p>

<p>Regarding {company['name']}'s work in {company['sector']}.</p>

<p>Our group has 70+ years in defense and security, specializing in 
electromagnetic spectrum control and multi-domain solutions.</p>

<p>We seek partnerships in cybersecurity, AI/ML, counter-drone, 
space defense, and data analytics.</p>

<p>Open to a brief call?</p>

<p>Best,<br>Zander</p>

<hr>
<p><em>For further information, reach Sam Desigan (Agent Manager)<br>
sam@impactquadrant.info</em></p>
"""
    
    result = send_email(
        to_email=company['email'],
        subject=subject,
        text_content=text,
        html_content=html,
        cc=CC_EMAIL
    )
    
    result['recipient'] = company['name']
    result['type'] = 'company'
    
    if result['success']:
        print(f"✅ Sent to {company['name']} (company)")
    else:
        print(f"❌ Failed to send to {company['name']}: {result.get('error', 'Unknown error')}")
    
    return result

def send_investor_email(investor):
    """Send email to PE/VC fund"""
    
    subject = "Investment Opportunity - Drone Technology Platform"
    
    text = f"""Hi {investor['contact_name']},

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
sam@impactquadrant.info
"""
    
    html = f"""<p>Hi {investor['contact_name']},</p>

<p>I'm reaching out about a drone technology platform seeking growth capital.</p>

<p><strong>Company Profile:</strong></p>
<ul>
<li>Founded 2015 in India</li>
<li>3,000+ drones deployed, 190+ enterprise projects</li>
<li>20+ patents, 30+ platforms</li>
<li>$13.8M revenue (FY25), 17-22% EBITDA margins</li>
<li>$242M+ valuation (KPMG assessed)</li>
<li>Expanding to US, Africa, South Asia</li>
<li>Defense revenue: 15-20% FY26, 30% FY27</li>
</ul>

<p>Sectors: Agriculture, inspections, surveillance, logistics, defense</p>

<p>Strategic partnership with Redington for nationwide distribution.</p>

<p>Would {investor['name']} be interested in exploring this opportunity?</p>

<p>Best,<br>Zander</p>

<hr>
<p><em>For further information, reach Sam Desigan (Agent Manager)<br>
sam@impactquadrant.info</em></p>
"""
    
    result = send_email(
        to_email=investor['email'],
        subject=subject,
        text_content=text,
        html_content=html,
        cc=CC_EMAIL
    )
    
    result['recipient'] = investor['name']
    result['type'] = 'investor'
    
    if result['success']:
        print(f"✅ Sent to {investor['name']} (investor)")
    else:
        print(f"❌ Failed to send to {investor['name']}: {result.get('error', 'Unknown error')}")
    
    return result

def main():
    """Main execution"""
    
    print("=" * 60)
    print("DEFENSE SECTOR OUTREACH - 2026-03-02")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"From: {FROM_EMAIL}")
    print(f"CC: {CC_EMAIL}")
    print()
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "companies": [],
        "investors": [],
        "summary": {
            "total_sent": 0,
            "total_failed": 0,
            "companies_sent": 0,
            "investors_sent": 0
        }
    }
    
    # Send to defense companies (max 10)
    print(f"📧 Sending to Defense Companies (max 10)...")
    print("-" * 60)
    
    for company in defense_companies[:10]:
        result = send_company_email(company)
        results["companies"].append(result)
        
        if result["success"]:
            results["summary"]["companies_sent"] += 1
            results["summary"]["total_sent"] += 1
        else:
            results["summary"]["total_failed"] += 1
    
    print()
    
    # Send to investors (max 5)
    print(f"📧 Sending to PE/VC Funds (max 5)...")
    print("-" * 60)
    
    for investor in investors[:5]:
        result = send_investor_email(investor)
        results["investors"].append(result)
        
        if result["success"]:
            results["summary"]["investors_sent"] += 1
            results["summary"]["total_sent"] += 1
        else:
            results["summary"]["total_failed"] += 1
    
    print()
    
    # Summary
    print("=" * 60)
    print("OUTREACH SUMMARY")
    print("=" * 60)
    print(f"✅ Total Sent: {results['summary']['total_sent']}")
    print(f"   • Companies: {results['summary']['companies_sent']}")
    print(f"   • Investors: {results['summary']['investors_sent']}")
    print(f"❌ Failed: {results['summary']['total_failed']}")
    print()
    
    # Save results
    results_file = Path("defense-leads/outreach-results-2026-03-02.json")
    results_file.parent.mkdir(exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"📁 Results saved to: {results_file}")
    
    # Create outreach log
    log_file = Path("defense-leads/outreach-log-2026-03-02.md")
    
    with open(log_file, 'w') as f:
        f.write(f"# Defense Sector Outreach Log - 2026-03-02\n\n")
        f.write(f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- **Total Sent:** {results['summary']['total_sent']}\n")
        f.write(f"- **Companies Contacted:** {results['summary']['companies_sent']}\n")
        f.write(f"- **Investors Contacted:** {results['summary']['investors_sent']}\n")
        f.write(f"- **Failed:** {results['summary']['total_failed']}\n\n")
        
        f.write(f"## Companies Contacted\n\n")
        for company in results["companies"]:
            status = "✅" if company["success"] else "❌"
            f.write(f"- {status} **{company['recipient']}** ({company['type']})\n")
        
        f.write(f"\n## Investors Contacted\n\n")
        for investor in results["investors"]:
            status = "✅" if investor["success"] else "❌"
            f.write(f"- {status} **{investor['recipient']}** ({investor['type']})\n")
    
    print(f"📝 Log saved to: {log_file}")
    
    return results

if __name__ == "__main__":
    main()
