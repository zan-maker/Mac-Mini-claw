#!/usr/bin/env python3
# CRON JOB DEDICATED GMAIL ACCOUNT

# Gmail Rotation System
import sys
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scripts')
from gmail_rotation_simple import send_email_with_rotation

CRON_GMAIL_EMAIL = "sam@cubiczan.com"
CRON_GMAIL_PASSWORD = "mwzh abbf ssih mjsf"
CRON_GMAIL_CC = "sam@impactquadrant.info"

STANDARD_SIGNATURE = """Best regards,

def send_email_with_rotation(to_emails, subject, body_text, body_html=None, cc_emails=None):
    """Send email using dedicated cron job Gmail account"""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import ssl
    
    try:
        # Prepare recipients
        if isinstance(to_emails, str):
            to_list = [to_emails]
        else:
            to_list = to_emails
        
        if cc_emails is None:
            cc_list = [CRON_GMAIL_CC]
        elif isinstance(cc_emails, str):
            cc_list = [cc_emails]
        else:
            cc_list = cc_emails
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f'Agent Manager <{CRON_GMAIL_EMAIL}>'
        msg['To'] = ', '.join(to_list)
        msg['Cc'] = ', '.join(cc_list)
        msg['Subject'] = subject
        
        # Add text version
        full_text = body_text + "\n\n" + STANDARD_SIGNATURE
        text_part = MIMEText(full_text, 'plain')
        msg.attach(text_part)
        
        # Add HTML version if provided
        if body_html:
            full_html = body_html + "<br><br>" + STANDARD_SIGNATURE.replace('\n', '<br>')
            html_part = MIMEText(full_html, 'html')
            msg.attach(html_part)
        
        # Connect and send
        context = ssl.create_default_context()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls(context=context)
        server.login(CRON_GMAIL_EMAIL, CRON_GMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True, f"Email sent successfully using {CRON_GMAIL_EMAIL}"
        
    except Exception as e:
        return False, f"Error sending email: {str(e)}"


Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""

"""
Defense Sector Outreach - Today's Batch
Find contacts and send emails to top defense companies and investors
"""

import sys
import json
import time
from datetime import datetime
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace')

from hunter_io_config import hunter_client
import requests

# Gmail SMTP (Cron) Configuration
# Removed old Gmail SMTP (Cron) API key
AGENTMAIL_INBOX = "Zander@cron_gmail.to"
CC_EMAIL = "sam@impactquadrant.info"
AGENTMAIL_BASE_URL = "https://api.cron_gmail.to/v0"

# Top companies from today's report
TOP_COMPANIES = [
    {"name": "Helsing", "domain": "helsing.ai", "sector": "AI & Machine Learning - Battlefield AI software", "score": 95},
    {"name": "Chaos Industries", "domain": "chaosindustries.com", "sector": "Counter-Drone (C-UAS) - Electronic warfare", "score": 92},
    {"name": "Saronic Technologies", "domain": "saronictech.com", "sector": "Autonomous Systems - Maritime", "score": 90},
    {"name": "Quantum Systems", "domain": "quantum-systems.com", "sector": "Counter-Drone / AI - eVTOL reconnaissance", "score": 88},
    {"name": "ICEYE", "domain": "iceye.com", "sector": "Space-Based Defense - SAR satellites", "score": 85},
    {"name": "Fortem Technologies", "domain": "fortemtech.com", "sector": "Counter-Drone (C-UAS) - DroneHunter", "score": 75},
    {"name": "DroneShield", "domain": "droneshield.com", "sector": "Counter-Drone (C-UAS) - Acoustic detection", "score": 72},
    {"name": "Epirus", "domain": "epirusinc.com", "sector": "Counter-Drone (C-UAS) - Directed energy", "score": 70},
    {"name": "Skydio", "domain": "skydio.com", "sector": "Autonomous Systems - AI drones", "score": 65},
    {"name": "True Anomaly", "domain": "trueanomaly.com", "sector": "Space-Based Defense - Space domain awareness", "score": 62},
]

# Top investors from today's report
TOP_INVESTORS = [
    {"name": "Speciale Invest", "domain": "specialeinvest.com", "region": "India", "focus": "Deep-tech, aerospace, defense", "score": 88},
    {"name": "Keen Venture Partners", "domain": "keenventurepartners.com", "region": "Netherlands", "focus": "Defense specialist", "score": 85},
    {"name": "Prima Materia", "domain": "primamateria.com", "region": "Sweden", "focus": "Deep tech, defense", "score": 82},
    {"name": "General Catalyst", "domain": "generalcatalyst.com", "region": "US/Global", "focus": "Defense tech, AI", "score": 75},
    {"name": "Lightspeed Venture Partners", "domain": "lsvp.com", "region": "US/Global", "focus": "Enterprise, AI, defense", "score": 72},
]

def find_contacts(domain, company_name):
    """Find contacts for a company using Hunter.io"""
    print(f"  Finding contacts for {company_name} ({domain})...")
    
    result = hunter_client.domain_search(domain, limit=5)
    time.sleep(1)  # Rate limiting
    
    if result.get('data') and result['data'].get('emails'):
        emails = result['data']['emails']
        
        # Prioritize executives and key roles
        contacts = []
        for email in emails:
            position = email.get('position', '').lower()
            # Look for executives, founders, or key decision makers
            if any(role in position for role in ['ceo', 'cto', 'founder', 'partner', 'managing', 'director', 'vp', 'head']):
                contacts.append({
                    "email": email.get('value'),
                    "name": f"{email.get('first_name', '')} {email.get('last_name', '')}".strip(),
                    "position": email.get('position'),
                    "confidence": email.get('confidence'),
                })
        
        # If no executives found, take the first contact
        if not contacts and emails:
            email = emails[0]
            contacts.append({
                "email": email.get('value'),
                "name": f"{email.get('first_name', '')} {email.get('last_name', '')}".strip(),
                "position": email.get('position'),
                "confidence": email.get('confidence'),
            })
        
        return contacts
    
    return []

def send_defense_company_email(contact, company):
    """Send outreach email to defense company"""
    
    headers = {
        "Authorization": f"Bearer {AGENTMAIL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    name_parts = contact['name'].split()
    first_name = name_parts[0] if name_parts else "there"
    
    subject = f"Strategic Partnership - {company['name']}"
    
    text_content = f"""Hi {first_name},

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

    payload = {
        "inbox_id": AGENTMAIL_INBOX,
        "to": [contact['email']],
        "subject": subject,
        "text": text_content,
        "cc": [CC_EMAIL]
    }
    
    try:
        response = send_email_with_rotation(to_emails, subject, body_text)
        
        if response.status_code == 200:
            return {"success": True, "message_id": response.json().get("message_id")}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def send_investor_email(contact, fund):
    """Send outreach email to PE/VC fund"""
    
    headers = {
        "Authorization": f"Bearer {AGENTMAIL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    name_parts = contact['name'].split()
    first_name = name_parts[0] if name_parts else "there"
    
    subject = f"Investment Opportunity - Drone Technology Platform"
    
    text_content = f"""Hi {first_name},

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

Would {fund['name']} be interested in exploring this opportunity?

Best,
Zander

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info
"""

    payload = {
        "inbox_id": AGENTMAIL_INBOX,
        "to": [contact['email']],
        "subject": subject,
        "text": text_content,
        "cc": [CC_EMAIL]
    }
    
    try:
        response = send_email_with_rotation(to_emails, subject, body_text)
        
        if response.status_code == 200:
            return {"success": True, "message_id": response.json().get("message_id")}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    print("="*70)
    print("DEFENSE SECTOR OUTREACH - TODAY'S BATCH")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Check Hunter.io credits
    print("\nChecking Hunter.io API credits...")
    account_info = hunter_client.get_account_info()
    if account_info.get('data'):
        credits = account_info['data']['requests']['credits']
        print(f"  Available: {credits['available']}, Used: {credits['used']}, Remaining: {int(credits['available'] - credits['used'])}")
    
    # Process companies
    print("\n" + "="*70)
    print("PART 1: DEFENSE COMPANIES (Max 10)")
    print("="*70)
    
    company_emails_sent = 0
    company_results = []
    
    for company in TOP_COMPANIES[:10]:  # Max 10 companies
        if company_emails_sent >= 10:
            break
            
        contacts = find_contacts(company['domain'], company['name'])
        
        if contacts:
            contact = contacts[0]  # Take the best contact
            print(f"  Found: {contact['name']} ({contact['position']}) - {contact['email']}")
            
            result = send_defense_company_email(contact, company)
            
            if result['success']:
                print(f"  ✅ Email sent successfully! Message ID: {result['message_id']}")
                company_emails_sent += 1
                company_results.append({
                    "company": company['name'],
                    "contact": contact['name'],
                    "email": contact['email'],
                    "status": "sent",
                    "message_id": result['message_id']
                })
            else:
                print(f"  ❌ Failed to send: {result['error']}")
                company_results.append({
                    "company": company['name'],
                    "contact": contact['name'],
                    "email": contact['email'],
                    "status": "failed",
                    "error": result['error']
                })
            
            time.sleep(2)  # Delay between sends
        else:
            print(f"  ⚠️ No contacts found for {company['name']}")
            company_results.append({
                "company": company['name'],
                "status": "no_contacts"
            })
    
    # Process investors
    print("\n" + "="*70)
    print("PART 2: PE/VC FUNDS (Max 5)")
    print("="*70)
    
    investor_emails_sent = 0
    investor_results = []
    
    for fund in TOP_INVESTORS[:5]:  # Max 5 investors
        if investor_emails_sent >= 5:
            break
            
        contacts = find_contacts(fund['domain'], fund['name'])
        
        if contacts:
            contact = contacts[0]  # Take the best contact
            print(f"  Found: {contact['name']} ({contact['position']}) - {contact['email']}")
            
            result = send_investor_email(contact, fund)
            
            if result['success']:
                print(f"  ✅ Email sent successfully! Message ID: {result['message_id']}")
                investor_emails_sent += 1
                investor_results.append({
                    "fund": fund['name'],
                    "contact": contact['name'],
                    "email": contact['email'],
                    "status": "sent",
                    "message_id": result['message_id']
                })
            else:
                print(f"  ❌ Failed to send: {result['error']}")
                investor_results.append({
                    "fund": fund['name'],
                    "contact": contact['name'],
                    "email": contact['email'],
                    "status": "failed",
                    "error": result['error']
                })
            
            time.sleep(2)  # Delay between sends
        else:
            print(f"  ⚠️ No contacts found for {fund['name']}")
            investor_results.append({
                "fund": fund['name'],
                "status": "no_contacts"
            })
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Companies: {company_emails_sent}/10 emails sent")
    print(f"Investors: {investor_emails_sent}/5 emails sent")
    print(f"Total: {company_emails_sent + investor_emails_sent}/15 emails sent")
    
    # Save results
    results = {
        "date": datetime.now().isoformat(),
        "companies": company_results,
        "investors": investor_results,
        "summary": {
            "companies_sent": company_emails_sent,
            "investors_sent": investor_emails_sent,
            "total_sent": company_emails_sent + investor_emails_sent
        }
    }
    
    with open('/Users/cubiczan/.openclaw/workspace/defense-leads/outreach-log-2026-02-25.md', 'w') as f:
        f.write(f"# Defense Sector Outreach Log - 2026-02-25\n\n")
        f.write(f"## Summary\n")
        f.write(f"- **Companies Contacted:** {company_emails_sent}/10\n")
        f.write(f"- **Investors Contacted:** {investor_emails_sent}/5\n")
        f.write(f"- **Total Emails Sent:** {company_emails_sent + investor_emails_sent}/15\n\n")
        
        f.write(f"## Companies\n")
        for result in company_results:
            if result.get('status') == 'sent':
                f.write(f"- ✅ {result['company']}: {result['contact']} ({result['email']}) - Message ID: {result['message_id']}\n")
            else:
                f.write(f"- ⚠️ {result['company']}: {result.get('status', 'unknown')}\n")
        
        f.write(f"\n## Investors\n")
        for result in investor_results:
            if result.get('status') == 'sent':
                f.write(f"- ✅ {result['fund']}: {result['contact']} ({result['email']}) - Message ID: {result['message_id']}\n")
            else:
                f.write(f"- ⚠️ {result['fund']}: {result.get('status', 'unknown')}\n")
        
        f.write(f"\n---\n")
        f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    print("\nResults saved to: outreach-log-2026-02-25.md")
    
    return results

if __name__ == "__main__":
    results = main()
