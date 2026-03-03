#!/usr/bin/env python3
"""
Mining Company Outreach Script - Gmail SMTP Version
Reach out to CPC and ASX companies with high-grade project opportunities
"""

import os
import json
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
from datetime import datetime

# Gmail Configuration (from b2b-referral-agentmail.py)
CRON_GMAIL_EMAIL = "sam@cubiczan.com"
CRON_GMAIL_PASSWORD = "mwzh abbf ssih mjsf"
CRON_GMAIL_CC = "sam@cubiczan.com"  # User requested CC

# Tavily API for contact search
TAVILY_API_KEY = "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"

# Standard Signature
STANDARD_SIGNATURE = """Best regards,

Agent Manager
Sam Desigan
Sam@impactquadrant.info
Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up"""

# Companies to contact (from March 2, 2026 report)
COMPANIES = [
    # CPC Companies (Canadian)
    {
        "ticker": "AUG.V",
        "name": "American Gold Corp",
        "type": "CPC",
        "cash": "$15M CAD",
        "asset": "Nevada gold project - 1.2M oz potential, 7.5 g/t",
        "seeking": "Strategic partner for feasibility",
        "search_terms": ["American Gold Corp", "AUG.V", "CEO", "contact"]
    },
    {
        "ticker": "CBM.V",
        "name": "Copper Belt Minerals",
        "type": "CPC",
        "cash": "$10M CAD",
        "asset": "Arizona copper project - 2.1% Cu porphyry",
        "seeking": "Earn-in partner",
        "search_terms": ["Copper Belt Minerals", "CBM.V", "CEO", "contact"]
    },
    {
        "ticker": "SVR.V",
        "name": "Silver Range Resources",
        "type": "CPC",
        "cash": "$8M CAD",
        "asset": "Mexico silver project - 280 g/t Ag epithermal",
        "seeking": "JV or acquisition",
        "search_terms": ["Silver Range Resources", "SVR.V", "CEO", "contact"]
    },
    # ASX Companies (Australian)
    {
        "ticker": "USA.AX",
        "name": "US Gold Limited",
        "type": "ASX",
        "cash": "A$22M",
        "asset": "Nevada gold project - 1.5M oz resource, 1.8 g/t",
        "seeking": "JV partner for expansion",
        "search_terms": ["US Gold Limited", "USA.AX", "CEO", "contact"]
    },
    {
        "ticker": "LAT.AX",
        "name": "Latin Copper Co",
        "type": "ASX",
        "cash": "A$20M",
        "asset": "Chile copper project - 1.8% Cu porphyry",
        "seeking": "Strategic investor",
        "search_terms": ["Latin Copper Co", "LAT.AX", "CEO", "contact"]
    },
    {
        "ticker": "CAN.AX",
        "name": "Canadian Rare Earths",
        "type": "ASX",
        "cash": "A$30M",
        "asset": "Quebec rare earths - 2.3% TREO carbonatite",
        "seeking": "Off-take partner",
        "search_terms": ["Canadian Rare Earths", "CAN.AX", "CEO", "contact"]
    }
]

# High-grade projects to present (from March 2 report)
HIGH_GRADE_PROJECTS = [
    {
        "name": "Nevada Gold Belt",
        "commodity": "Gold",
        "grade": "8.5 g/t Au",
        "location": "Nevada, USA",
        "stage": "Resource Definition",
        "potential": "1.8 million ounces potential, Carlin-type"
    },
    {
        "name": "Yukon Copper-Gold",
        "commodity": "Copper-Gold",
        "grade": "2.8% Cu, 1.2 g/t Au",
        "location": "Yukon, Canada",
        "stage": "Advanced Exploration",
        "potential": "Porphyry system with 5km strike"
    },
    {
        "name": "Arizona Copper Project",
        "commodity": "Copper",
        "grade": "1.5% Cu",
        "location": "Arizona, USA",
        "stage": "Feasibility",
        "potential": "Large tonnage porphyry deposit"
    },
    {
        "name": "Quebec Rare Earths",
        "commodity": "Rare Earths",
        "grade": "2.1% TREO",
        "location": "Quebec, Canada",
        "stage": "PFS",
        "potential": "Carbonatite-hosted rare earths"
    },
    {
        "name": "Peru Copper Belt",
        "commodity": "Copper",
        "grade": "2.3% Cu, 0.3 g/t Au",
        "location": "Peru, Latin America",
        "stage": "Resource Definition",
        "potential": "Skarn deposit with expansion potential"
    }
]

def search_company_contact(company):
    """Search for company contact information using Tavily API"""
    query = f"{company['name']} {company['ticker']} CEO CFO contact email"
    
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            headers={"Content-Type": "application/json"},
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "search_depth": "advanced",
                "max_results": 3
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("results", [])
        else:
            print(f"  ❌ Tavily API error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"  ❌ Search error: {e}")
        return []

def extract_email_from_results(results):
    """Extract email addresses from search results"""
    emails = []
    
    for result in results:
        content = result.get("content", "").lower()
        
        # Look for email patterns
        import re
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        found_emails = re.findall(email_pattern, content)
        
        # Filter out common non-personal emails
        for email in found_emails:
            if not any(domain in email for domain in ["noreply", "info@", "contact@", "support@", "hello@", "admin@"]):
                emails.append(email)
    
    return list(set(emails))[:3]  # Return up to 3 unique emails

def generate_email_body(company, projects):
    """Generate personalized email body for the company"""
    
    # Filter projects relevant to the company's focus
    relevant_projects = []
    company_focus = company['asset'].lower()
    
    for project in projects:
        if any(keyword in company_focus for keyword in ['gold', 'copper', 'silver', 'rare earth']):
            # Check if project commodity matches company focus
            project_commodity = project['commodity'].lower()
            if ('gold' in company_focus and 'gold' in project_commodity) or \
               ('copper' in company_focus and 'copper' in project_commodity) or \
               ('silver' in company_focus and 'silver' in project_commodity) or \
               ('rare earth' in company_focus and 'rare earth' in project_commodity):
                relevant_projects.append(project)
    
    # If no exact matches, use top 2 projects
    if not relevant_projects:
        relevant_projects = projects[:2]
    
    # Generate email body
    body = f"""Dear {company['name']} Team,

I hope this message finds you well. I'm reaching out regarding potential partnership opportunities that may align with {company['name']}'s ({company['ticker']}) strategic objectives.

I understand from public filings that {company['name']} is seeking {company['seeking'].lower()} for your {company['asset']}.

Our network includes several high-grade projects that may be of interest:

"""
    
    for i, project in enumerate(relevant_projects, 1):
        body += f"""{i}. **{project['name']}** ({project['location']})
   • Commodity: {project['commodity']}
   • Grade: {project['grade']}
   • Stage: {project['stage']}
   • Potential: {project['potential']}

"""
    
    body += f"""Given {company['name']}'s strong cash position ({company['cash']}) and focus on {company['asset'].split(' - ')[0]}, I believe there may be strategic alignment with one or more of these opportunities.

Would you be open to a brief discussion to explore potential synergies? I'd be happy to provide additional details on any projects that pique your interest.
"""
    
    return body

def send_email_via_gmail(to_email, company_name, subject, body_text):
    """Send email using Gmail SMTP"""
    
    try:
        # Prepare recipients
        to_list = [to_email] if isinstance(to_email, str) else to_email
        cc_list = [CRON_GMAIL_CC]
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = CRON_GMAIL_EMAIL
        msg['To'] = ', '.join(to_list)
        msg['Cc'] = ', '.join(cc_list)
        
        # Add body with signature
        full_body = body_text + '\n\n' + STANDARD_SIGNATURE
        part1 = MIMEText(full_body, 'plain')
        msg.attach(part1)
        
        # Send email
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(CRON_GMAIL_EMAIL, CRON_GMAIL_PASSWORD)
            server.send_message(msg)
        
        return {"success": True}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    """Main execution function"""
    
    print("=" * 70)
    print("MINING COMPANY OUTREACH - HIGH-GRADE PROJECTS")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    print()
    
    results = []
    
    for company in COMPANIES:
        print(f"Processing: {company['name']} ({company['ticker']})")
        print(f"  Type: {company['type']}")
        print(f"  Cash: {company['cash']}")
        print(f"  Seeking: {company['seeking']}")
        
        # Step 1: Search for contact information
        print("  Searching for contact information...")
        search_results = search_company_contact(company)
        
        if not search_results:
            print("  ⚠️ No search results found")
            results.append({
                "company": company['name'],
                "ticker": company['ticker'],
                "status": "failed",
                "reason": "No search results"
            })
            print()
            continue
        
        # Step 2: Extract email addresses
        emails = extract_email_from_results(search_results)
        
        if not emails:
            print("  ⚠️ No email addresses found in search results")
            # Try to get website and guess email format
            for result in search_results:
                url = result.get('url', '')
                if company['name'].lower().replace(' ', '') in url.lower():
                    # Guess email format
                    domain = url.split('//')[-1].split('/')[0]
                    if '.' in domain:
                        guess_email = f"info@{domain}"
                        emails.append(guess_email)
                        print(f"  Guessed email: {guess_email}")
                        break
            
            if not emails:
                results.append({
                    "company": company['name'],
                    "ticker": company['ticker'],
                    "status": "failed",
                    "reason": "No email addresses found"
                })
                print()
                continue
        
        # Step 3: Generate email content
        print("  Generating email content...")
        email_body = generate_email_body(company, HIGH_GRADE_PROJECTS)
        subject = f"High-grade project opportunities for {company['name']} ({company['ticker']})"
        
        # Step 4: Send email via Gmail
        print(f"  Sending to: {emails[0]}")
        send_result = send_email_via_gmail(
            emails[0],
            company['name'],
            subject,
            email_body
        )
        
        if send_result['success']:
            print(f"  ✅ Email sent successfully via Gmail")
            results.append({
                "company": company['name'],
                "ticker": company['ticker'],
                "email": emails[0],
                "status": "sent",
                "timestamp": datetime.now().isoformat()
            })
        else:
            print(f"  ❌ Failed to send email: {send_result.get('error', 'Unknown error')}")
            results.append({
                "company": company['name'],
                "ticker": company['ticker'],
                "email": emails[0],
                "status": "failed",
                "error": send_result.get('error', 'Unknown error'),
                "timestamp": datetime.now().isoformat()
            })
        
        print()
    
    # Summary
    print("=" * 70)
    print("OUTREACH SUMMARY")
    print("=" * 70)
    
    sent_count = sum(1 for r in results if r['status'] == 'sent')
    failed_count = sum(1 for r in results if r['status'] == 'failed')
    
    print(f"Total companies: {len(COMPANIES)}")
    print(f"Emails sent: {sent_count}")
    print(f"Failed: {failed_count}")
    print()
    
    print("Details:")
    for result in results:
        status_icon = "✅" if result['status'] == 'sent' else "❌"
        print(f"{status_icon} {result['company']} ({result['ticker']}) - {result['status']}")
        if result['status'] == 'failed' and 'reason' in result:
            print(f"   Reason: {result['reason']}")
    
    # Save results
    output_file = f"/Users/cubiczan/.openclaw/workspace/mining-outreach-gmail-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print()
    print(f"Results saved to: {output_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()
