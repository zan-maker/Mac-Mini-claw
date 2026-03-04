#!/usr/bin/env python3
"""
Defense Sector Outreach - March 3, 2026
Using Gmail SMTP (AgentMail API down)
Following cron job specifications
"""

import sys
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
from datetime import datetime

# Import Hunter.io client
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace')
from hunter_io_config import HunterIOClient

# Initialize Hunter.io with API key
HUNTER_API_KEY = "6b48c50fc1df93f1df0b7b1aaf17616a71e369b5"
hunter_client = HunterIOClient(api_key=HUNTER_API_KEY)

# Email Configuration
FROM_EMAIL = "Zander@agentmail.to"
GMAIL_EMAIL = "sam@cubiczan.com"
GMAIL_PASSWORD = "mwzh abbf ssih mjsf"
CC_EMAIL = "sam@impactquadrant.info"

# Drone company profile for investor emails
DRONE_PROFILE = """
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
"""

# Defense companies (using proven list from previous successful runs)
DEFENSE_COMPANIES = [
    {"name": "Shield AI", "domain": "shield.ai", "sector": "AI & Autonomous Systems"},
    {"name": "Anduril Industries", "domain": "anduril.com", "sector": "Autonomous Systems & Counter-Drone"},
    {"name": "Skydio", "domain": "skydio.com", "sector": "Autonomous Drones"},
    {"name": "Chaos Industries", "domain": "chaosindustries.com", "sector": "Defense Manufacturing"},
    {"name": "Epirus", "domain": "epirusinc.com", "sector": "Counter-Drone (C-UAS)"},
    {"name": "Onebrief", "domain": "onebrief.com", "sector": "Defense Data Analytics / ISR"},
    {"name": "Hidden Level", "domain": "hiddenlevel.com", "sector": "Counter-Drone / Surveillance"},
    {"name": "Rebellion Defense", "domain": "rebelliondefense.com", "sector": "AI & Defense Software"},
    {"name": "Palantir Technologies", "domain": "palantir.com", "sector": "Defense Data Analytics"},
    {"name": "Astranis", "domain": "astranis.com", "sector": "Space-Based Defense"},
]

# PE/VC Funds (Asia/India focus)
INVESTOR_FUNDS = [
    {"name": "General Catalyst", "domain": "generalcatalyst.com", "region": "US/Global"},
    {"name": "Lightspeed Venture Partners", "domain": "lightspeedvp.com", "region": "US/Global"},
    {"name": "Accel Partners", "domain": "accel.com", "region": "US/Global"},
    {"name": "BEENEXT", "domain": "beenext.com", "region": "Asia/India"},
    {"name": "Vertex Ventures", "domain": "vertexventures.com", "region": "Asia/Global"},
]

def find_best_email(domain):
    """Find the best email for a domain using Hunter.io"""
    try:
        result = hunter_client.domain_search(domain, limit=10)
        
        if result.get('data') and result['data'].get('emails'):
            emails = result['data']['emails']
            
            # Filter for high-confidence emails
            high_conf = [e for e in emails if e.get('confidence', 0) >= 70]
            
            if not high_conf:
                return None
            
            # Prefer personal emails
            personal = [e for e in high_conf if e.get('type') == 'personal']
            if personal:
                best = max(personal, key=lambda x: x.get('confidence', 0))
                return {
                    'email': best['value'],
                    'type': best['type'],
                    'confidence': best['confidence'],
                    'name': f"{best.get('first_name', '')} {best.get('last_name', '')}".strip(),
                    'position': best.get('position', ''),
                }
            else:
                best = max(high_conf, key=lambda x: x.get('confidence', 0))
                return {
                    'email': best['value'],
                    'type': best['type'],
                    'confidence': best['confidence'],
                    'name': f"{best.get('first_name', '')} {best.get('last_name', '')}".strip(),
                    'position': best.get('position', ''),
                }
    
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    return None

def send_email_via_gmail(to_email, subject, body):
    """Send email via Gmail SMTP"""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = f"Zander <{GMAIL_EMAIL}>"
        msg['To'] = to_email
        msg['Cc'] = CC_EMAIL
        msg['Subject'] = subject
        
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        context = ssl.create_default_context()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls(context=context)
        server.login(GMAIL_EMAIL, GMAIL_PASSWORD)
        
        recipients = [to_email, CC_EMAIL]
        server.sendmail(GMAIL_EMAIL, recipients, msg.as_string())
        server.quit()
        
        return True, "Sent successfully"
    
    except Exception as e:
        return False, str(e)

def generate_company_email(company, contact_name):
    """Generate defense company email per cron spec"""
    subject = f"Strategic Partnership - {company['name']}"
    
    name = contact_name.split()[0] if contact_name and contact_name != '' else "there"
    
    body = f"""Hi {name},

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
    
    return subject, body

def generate_investor_email(fund, contact_name):
    """Generate investor email per cron spec"""
    subject = "Investment Opportunity - Drone Technology Platform"
    
    name = contact_name.split()[0] if contact_name and contact_name != '' else "there"
    
    body = f"""Hi {name},

I'm reaching out about a drone technology platform seeking growth capital.

{DRONE_PROFILE}

Would {fund['name']} be interested in exploring this opportunity?

Best,
Zander

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info
"""
    
    return subject, body

def main():
    """Main execution"""
    print("=" * 80)
    print("DEFENSE SECTOR OUTREACH - MARCH 3, 2026")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Check Hunter.io credits
    print("\n📊 Checking Hunter.io account...")
    try:
        account_info = hunter_client.get_account_info()
        if account_info.get('data'):
            credits = account_info['data'].get('requests', {}).get('credits', {}).get('available', 0)
            searches = account_info['data'].get('requests', {}).get('searches', {}).get('available', 0)
            print(f"   ✅ Credits: {credits}, Searches: {searches}")
    except Exception as e:
        print(f"   ⚠️ Could not check account: {e}")
    
    results = {
        'companies': [],
        'investors': [],
        'summary': {
            'total_targets': 15,
            'companies_target': 10,
            'investors_target': 5,
            'emails_found': 0,
            'emails_sent': 0,
            'emails_failed': 0,
            'no_contact': 0
        }
    }
    
    # Part 1: Defense Companies (max 10)
    print(f"\n🏢 PART 1: DEFENSE COMPANIES (Target: 10)")
    print("-" * 80)
    
    for i, company in enumerate(DEFENSE_COMPANIES[:10], 1):
        print(f"\n[{i}/10] {company['name']}")
        
        email_info = find_best_email(company['domain'])
        
        if not email_info:
            print(f"   ❌ No email found for {company['domain']}")
            results['companies'].append({
                'name': company['name'],
                'domain': company['domain'],
                'sector': company['sector'],
                'status': 'no_email'
            })
            results['summary']['no_contact'] += 1
            continue
        
        print(f"   ✅ Found: {email_info['email']} ({email_info['confidence']}%)")
        print(f"      Name: {email_info.get('name', 'N/A')}")
        
        subject, body = generate_company_email(company, email_info.get('name', ''))
        
        print(f"   📧 Sending...")
        success, message = send_email_via_gmail(email_info['email'], subject, body)
        
        if success:
            print(f"   ✅ SENT")
            results['summary']['emails_sent'] += 1
            status = 'sent'
        else:
            print(f"   ❌ FAILED: {message}")
            results['summary']['emails_failed'] += 1
            status = 'failed'
        
        results['companies'].append({
            'name': company['name'],
            'domain': company['domain'],
            'sector': company['sector'],
            'email': email_info['email'],
            'contact_name': email_info.get('name', ''),
            'confidence': email_info['confidence'],
            'status': status,
            'timestamp': datetime.now().isoformat()
        })
        results['summary']['emails_found'] += 1
        
        time.sleep(2)  # Rate limiting
    
    # Part 2: PE/VC Funds (max 5)
    print(f"\n\n💰 PART 2: PE/VC FUNDS - ASIA/INDIA (Target: 5)")
    print("-" * 80)
    
    for i, fund in enumerate(INVESTOR_FUNDS[:5], 1):
        print(f"\n[{i}/5] {fund['name']}")
        
        email_info = find_best_email(fund['domain'])
        
        if not email_info:
            print(f"   ❌ No email found for {fund['domain']}")
            results['investors'].append({
                'name': fund['name'],
                'domain': fund['domain'],
                'region': fund['region'],
                'status': 'no_email'
            })
            results['summary']['no_contact'] += 1
            continue
        
        print(f"   ✅ Found: {email_info['email']} ({email_info['confidence']}%)")
        print(f"      Name: {email_info.get('name', 'N/A')}")
        
        subject, body = generate_investor_email(fund, email_info.get('name', ''))
        
        print(f"   📧 Sending...")
        success, message = send_email_via_gmail(email_info['email'], subject, body)
        
        if success:
            print(f"   ✅ SENT")
            results['summary']['emails_sent'] += 1
            status = 'sent'
        else:
            print(f"   ❌ FAILED: {message}")
            results['summary']['emails_failed'] += 1
            status = 'failed'
        
        results['investors'].append({
            'name': fund['name'],
            'domain': fund['domain'],
            'region': fund['region'],
            'email': email_info['email'],
            'contact_name': email_info.get('name', ''),
            'confidence': email_info['confidence'],
            'status': status,
            'timestamp': datetime.now().isoformat()
        })
        results['summary']['emails_found'] += 1
        
        time.sleep(2)  # Rate limiting
    
    # Save results
    output_file = f"/Users/cubiczan/.openclaw/workspace/defense-leads/outreach-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Update outreach log
    log_file = f"/Users/cubiczan/.openclaw/workspace/defense-leads/outreach-log-2026-03-03.md"
    with open(log_file, 'w') as f:
        f.write(f"# Defense Sector Outreach Log - 2026-03-03\n\n")
        f.write(f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- **Total Sent:** {results['summary']['emails_sent']}\n")
        f.write(f"- **Companies Contacted:** {len([c for c in results['companies'] if c['status'] == 'sent'])}\n")
        f.write(f"- **Investors Contacted:** {len([i for i in results['investors'] if i['status'] == 'sent'])}\n")
        f.write(f"- **Failed:** {results['summary']['emails_failed']}\n")
        f.write(f"- **No Contact Found:** {results['summary']['no_contact']}\n\n")
        
        f.write(f"## Companies Contacted\n\n")
        for company in results['companies']:
            emoji = "✅" if company['status'] == 'sent' else "❌"
            f.write(f"- {emoji} **{company['name']}** (company)")
            if company.get('email'):
                f.write(f" - {company['email']}")
            f.write(f"\n")
        
        f.write(f"\n## Investors Contacted\n\n")
        for investor in results['investors']:
            emoji = "✅" if investor['status'] == 'sent' else "❌"
            f.write(f"- {emoji} **{investor['name']}** (investor)")
            if investor.get('email'):
                f.write(f" - {investor['email']}")
            f.write(f"\n")
        
        f.write(f"\n## Email Details\n\n")
        f.write(f"- **From:** {FROM_EMAIL} (via Gmail SMTP)\n")
        f.write(f"- **CC:** {CC_EMAIL}\n")
        f.write(f"- **Results File:** {output_file}\n")
    
    # Print final summary
    print("\n" + "=" * 80)
    print("✅ OUTREACH COMPLETE!")
    print("=" * 80)
    print(f"\n📊 Summary:")
    print(f"   • Emails sent: {results['summary']['emails_sent']}/{results['summary']['total_targets']}")
    print(f"   • Companies: {len([c for c in results['companies'] if c['status'] == 'sent'])}/10")
    print(f"   • Investors: {len([i for i in results['investors'] if i['status'] == 'sent'])}/5")
    print(f"   • Failed: {results['summary']['emails_failed']}")
    print(f"   • No contact: {results['summary']['no_contact']}")
    print(f"\n📁 Files:")
    print(f"   • Results: {output_file}")
    print(f"   • Log: {log_file}")
    print(f"\n📧 All emails CC'd to: {CC_EMAIL}")
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    main()
