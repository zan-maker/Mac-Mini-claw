#!/usr/bin/env python3
"""
Defense Sector Outreach - 2026-03-09
Uses working AgentMail credentials
"""

import requests
import json
from datetime import datetime
from pathlib import Path
import time

# WORKING CONFIGURATION
API_KEY = "am_us_6aa957b36fb69693140cb0787c894d90ec2e65ffe937049634b685b911c1ac14"
FROM_EMAIL = "zane@agentmail.to"
FROM_NAME = "Zander"
CC_EMAIL = "sam@impactquadrant.info"
BASE_URL = "https://api.agentmail.to/v0"

# Workspace paths
WORKSPACE = Path("/Users/cubiczan/.openclaw/workspace")
DEFENSE_LEADS = WORKSPACE / "defense-leads"
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
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {error_data.get('message', response.text[:100])}",
                "status": "failed"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "status": "error"
        }

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

# Defense companies to contact (top 10) with email patterns
DEFENSE_COMPANIES = [
    {"name": "Harmattan AI", "email": "contact@harmattan.ai", "sector": "AI/Autonomy for Defense Aircraft"},
    {"name": "Castelion", "email": "info@castelion.com", "sector": "Hypersonic Munitions"},
    {"name": "Saronic", "email": "contact@saronic.com", "sector": "Autonomous Surface Vessels (Naval)"},
    {"name": "Chaos Industries", "email": "info@chaosind.com", "sector": "Defense & Critical Infrastructure"},
    {"name": "Defense Unicorns", "email": "contact@defenseunicorns.com", "sector": "Software Delivery for National Security"},
    {"name": "HawkEye 360", "email": "info@he360.com", "sector": "Space-Based Defense/ISR"},
    {"name": "Anduril Industries", "email": "contact@anduril.com", "sector": "Defense Tech (Hardware-Intensive)"},
    {"name": "Digantara", "email": "contact@digantara.com", "sector": "Space Intelligence/Satellite Tracking"},
    {"name": "Aonic", "email": "info@aonic.com", "sector": "Drone Technology"},
    {"name": "RADICL", "email": "contact@radicl.com", "sector": "Cybersecurity for Defense"}
]

# PE/VC investors to contact (top 5)
INVESTORS = [
    {"name": "Maharashtra Defence Fund", "email": "aif@idbicapital.com", "fund_name": "Maharashtra Defence Fund"},
    {"name": "Kairous Capital", "email": "contact@kairouscapital.com", "fund_name": "Kairous Capital"},
    {"name": "XYZ Venture Capital", "email": "invest@xyz.vc", "fund_name": "XYZ Venture Capital"},
    {"name": "Airbus Ventures", "email": "contact@airbusventures.com", "fund_name": "Airbus Ventures"},
    {"name": "DCVC", "email": "invest@dcvc.com", "fund_name": "DCVC"}
]

def main():
    print("="*60)
    print("DEFENSE SECTOR OUTREACH - 2026-03-09")
    print("="*60)
    print(f"From: {FROM_EMAIL}")
    print(f"CC: {CC_EMAIL}")
    print()
    
    results = {
        "date": "2026-03-09",
        "companies_sent": 0,
        "companies_failed": 0,
        "investors_sent": 0,
        "investors_failed": 0,
        "details": []
    }
    
    # Send to defense companies (max 10)
    print("📧 Sending to Defense Companies...")
    for i, company in enumerate(DEFENSE_COMPANIES[:10], 1):
        print(f"\n{i}. {company['name']}")
        print(f"   Email: {company['email']}")
        
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
        
        result = send_email(company["email"], subject, body, cc=CC_EMAIL)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "defense_company",
            "name": company["name"],
            "email": company["email"],
            "sector": company["sector"],
            "result": result
        }
        log_outreach(log_entry)
        
        if result["success"]:
            print(f"   ✅ SENT - Message ID: {result.get('message_id', 'N/A')}")
            results["companies_sent"] += 1
        else:
            print(f"   ❌ FAILED - {result.get('error', 'Unknown error')}")
            results["companies_failed"] += 1
            results["details"].append({
                "type": "company",
                "name": company["name"],
                "email": company["email"],
                "error": result.get("error")
            })
        
        # Rate limiting
        time.sleep(1)
    
    # Send to investors (max 5)
    print("\n" + "="*60)
    print("📧 Sending to PE/VC Investors...")
    for i, investor in enumerate(INVESTORS[:5], 1):
        print(f"\n{i}. {investor['name']}")
        print(f"   Email: {investor['email']}")
        
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
        
        result = send_email(investor["email"], subject, body, cc=CC_EMAIL)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "investor",
            "name": investor["name"],
            "email": investor["email"],
            "fund_name": investor["fund_name"],
            "result": result
        }
        log_outreach(log_entry)
        
        if result["success"]:
            print(f"   ✅ SENT - Message ID: {result.get('message_id', 'N/A')}")
            results["investors_sent"] += 1
        else:
            print(f"   ❌ FAILED - {result.get('error', 'Unknown error')}")
            results["investors_failed"] += 1
            results["details"].append({
                "type": "investor",
                "name": investor["name"],
                "email": investor["email"],
                "error": result.get("error")
            })
        
        # Rate limiting
        time.sleep(1)
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Defense Companies: {results['companies_sent']}/10 sent, {results['companies_failed']} failed")
    print(f"PE/VC Investors:   {results['investors_sent']}/5 sent, {results['investors_failed']} failed")
    print(f"Total Sent:        {results['companies_sent'] + results['investors_sent']}/15")
    
    if results["details"]:
        print("\nFailed emails:")
        for detail in results["details"]:
            print(f"  - {detail['name']} ({detail['email']}): {detail['error']}")
    
    # Save final results
    results_file = DEFENSE_LEADS / f"outreach-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {results_file.name}")
    
    return results

if __name__ == "__main__":
    results = main()
