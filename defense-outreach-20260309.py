#!/usr/bin/env python3
"""
Defense Sector Outreach - 2026-03-09
Sends emails to defense companies and PE/VC investors
"""

import requests
import json
from datetime import datetime
from pathlib import Path

# Configuration
API_KEY = "am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f"
FROM_EMAIL = "zanking@agentmail.to"  # Using Zan King inbox
FROM_NAME = "Zander"
CC_EMAIL = "sam@impactquadrant.info"
BASE_URL = "https://api.agentmail.to/v0"

# Workspace paths
WORKSPACE = Path("/Users/cubiczan/.openclaw/workspace")
DEFENSE_LEADS = WORKSPACE / "defense-leads"
CONTACTED_FILE = DEFENSE_LEADS / "contacted-leads.json"
LOG_FILE = DEFENSE_LEADS / "outreach-log-2026-03-09.json"

def send_email(to_email, subject, text_body, cc=None):
    """Send email via AgentMail API"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inbox_id": FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "text": text_body
    }
    
    if cc:
        payload["cc"] = [cc] if isinstance(cc, str) else cc
    
    try:
        response = requests.post(
            f"{BASE_URL}/inboxes/{FROM_EMAIL}/messages/send",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "message_id": result.get("message_id"),
                "status": "sent"
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text[:200]}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def get_contacted_leads():
    """Load contacted leads tracking"""
    if CONTACTED_FILE.exists():
        with open(CONTACTED_FILE, 'r') as f:
            return json.load(f)
    return {"companies": [], "investors": []}

def save_contacted_leads(data):
    """Save contacted leads tracking"""
    CONTACTED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONTACTED_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def log_outreach(log_entry):
    """Log outreach attempt"""
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    
    logs.append(log_entry)
    
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

# Defense companies to contact (top 10)
DEFENSE_COMPANIES = [
    {
        "name": "Harmattan AI",
        "contact_email": "contact@harmattan.ai",  # Placeholder
        "sector": "AI/Autonomy for Defense Aircraft",
        "priority": "High"
    },
    {
        "name": "Castelion",
        "contact_email": "info@castelion.com",  # Placeholder
        "sector": "Hypersonic Munitions",
        "priority": "High"
    },
    {
        "name": "Saronic",
        "contact_email": "contact@saronic.com",  # Placeholder
        "sector": "Autonomous Surface Vessels (Naval)",
        "priority": "High"
    },
    {
        "name": "Chaos Industries",
        "contact_email": "info@chaosind.com",  # Placeholder
        "sector": "Defense & Critical Infrastructure",
        "priority": "High"
    },
    {
        "name": "Defense Unicorns",
        "contact_email": "contact@defenseunicorns.com",  # Placeholder
        "sector": "Software Delivery for National Security",
        "priority": "High"
    },
    {
        "name": "HawkEye 360",
        "contact_email": "info@he360.com",  # Placeholder
        "sector": "Space-Based Defense/ISR",
        "priority": "High"
    },
    {
        "name": "Anduril Industries",
        "contact_email": "contact@anduril.com",  # Placeholder
        "sector": "Defense Tech (Hardware-Intensive)",
        "priority": "High"
    },
    {
        "name": "Digantara",
        "contact_email": "contact@digantara.com",  # Placeholder
        "sector": "Space Intelligence/Satellite Tracking",
        "priority": "Medium"
    },
    {
        "name": "Aonic",
        "contact_email": "info@aonic.com",  # Placeholder
        "sector": "Drone Technology",
        "priority": "Medium"
    },
    {
        "name": "RADICL",
        "contact_email": "contact@radicl.com",  # Placeholder
        "sector": "Cybersecurity for Defense",
        "priority": "Medium"
    }
]

# PE/VC investors to contact (top 5)
INVESTORS = [
    {
        "name": "Maharashtra Defence and Aerospace Venture Fund",
        "contact_email": "aif@idbicapital.com",  # Placeholder
        "fund_name": "Maharashtra Defence Fund",
        "priority": "High"
    },
    {
        "name": "Kairous Capital",
        "contact_email": "contact@kairouscapital.com",  # Placeholder
        "fund_name": "Kairous Capital",
        "priority": "High"
    },
    {
        "name": "XYZ Venture Capital",
        "contact_email": "invest@xyz.vc",  # Placeholder
        "fund_name": "XYZ Venture Capital",
        "priority": "High"
    },
    {
        "name": "Airbus Ventures",
        "contact_email": "contact@airbusventures.com",  # Placeholder
        "fund_name": "Airbus Ventures",
        "priority": "Medium"
    },
    {
        "name": "DCVC (Data Collective)",
        "contact_email": "invest@dcvc.com",  # Placeholder
        "fund_name": "DCVC",
        "priority": "Medium"
    }
]

def main():
    print("="*60)
    print("DEFENSE SECTOR OUTREACH - 2026-03-09")
    print("="*60)
    
    contacted = get_contacted_leads()
    results = {
        "companies_sent": 0,
        "companies_failed": 0,
        "investors_sent": 0,
        "investors_failed": 0,
        "details": []
    }
    
    # Send to defense companies
    print("\n📧 Sending to Defense Companies (max 10)...")
    for company in DEFENSE_COMPANIES[:10]:
        if company["name"] in contacted["companies"]:
            print(f"  ⏭️  {company['name']} - already contacted")
            continue
        
        subject = f"Strategic Partnership - {company['name']}"
        body = f"""Hi,

Regarding {company['name']}'s work in {company['sector']}.

Our group has 70+ years in defense and security, specializing in 
electromagnetic spectrum control and multi-domain solutions.

We seek partnerships in cybersecurity, AI/ML, counter-drone, 
space defense, and data analytics.

Open to a brief call?

Best,
{FROM_NAME}

---
For further information, reach Sam Desigan (Agent Manager)
{CC_EMAIL}
"""
        
        result = send_email(company["contact_email"], subject, body, cc=CC_EMAIL)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "defense_company",
            "name": company["name"],
            "email": company["contact_email"],
            "sector": company["sector"],
            "priority": company["priority"],
            "result": result
        }
        log_outreach(log_entry)
        
        if result["success"]:
            print(f"  ✅ {company['name']}")
            results["companies_sent"] += 1
            contacted["companies"].append(company["name"])
        else:
            print(f"  ❌ {company['name']}: {result.get('error', 'Unknown error')}")
            results["companies_failed"] += 1
            results["details"].append({
                "name": company["name"],
                "error": result.get("error")
            })
    
    # Send to investors
    print("\n📧 Sending to PE/VC Investors (max 5)...")
    for investor in INVESTORS[:5]:
        if investor["name"] in contacted["investors"]:
            print(f"  ⏭️  {investor['name']} - already contacted")
            continue
        
        subject = "Investment Opportunity - Drone Technology Platform"
        body = f"""Hi,

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
{FROM_NAME}

---
For further information, reach Sam Desigan (Agent Manager)
{CC_EMAIL}
"""
        
        result = send_email(investor["contact_email"], subject, body, cc=CC_EMAIL)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "investor",
            "name": investor["name"],
            "email": investor["contact_email"],
            "fund_name": investor["fund_name"],
            "priority": investor["priority"],
            "result": result
        }
        log_outreach(log_entry)
        
        if result["success"]:
            print(f"  ✅ {investor['name']}")
            results["investors_sent"] += 1
            contacted["investors"].append(investor["name"])
        else:
            print(f"  ❌ {investor['name']}: {result.get('error', 'Unknown error')}")
            results["investors_failed"] += 1
            results["details"].append({
                "name": investor["name"],
                "error": result.get("error")
            })
    
    # Save contacted leads
    save_contacted_leads(contacted)
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Defense Companies: {results['companies_sent']} sent, {results['companies_failed']} failed")
    print(f"PE/VC Investors:   {results['investors_sent']} sent, {results['investors_failed']} failed")
    print(f"Total:             {results['companies_sent'] + results['investors_sent']} sent")
    
    if results["details"]:
        print("\nFailed emails:")
        for detail in results["details"]:
            print(f"  - {detail['name']}: {detail['error']}")
    
    # Return results for Discord reporting
    return results

if __name__ == "__main__":
    results = main()
    print("\n" + json.dumps(results, indent=2))
