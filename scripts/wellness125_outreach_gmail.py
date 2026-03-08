#!/usr/bin/env python3
"""
Wellness 125 Outreach - Gmail SMTP Version
Sends outreach emails via Gmail SMTP (NOT AgentMail)
FROM: sam@cubiczan.com (primary) or other Gmail accounts
CC: sam@impactquadrant.info
Standard signature with "Agent Manager" title
"""

import sys
import os
import json
from datetime import datetime

# Add scripts directory to path to import gmail module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from gmail_smtp_standard import GmailSender, STANDARD_SIGNATURE
except ImportError:
    print("❌ ERROR: gmail_smtp_standard.py not found in scripts directory")
    print("Please ensure gmail_smtp_standard.py is in the same directory")
    sys.exit(1)

def load_todays_leads():
    """Load today's Wellness 125 leads from the limited file"""
    leads_file = "/Users/cubiczan/.openclaw/workspace/wellness-125-leads/wellness125-leads-limited-2026-03-06.json"
    
    if not os.path.exists(leads_file):
        print(f"❌ Leads file not found: {leads_file}")
        return []
    
    try:
        with open(leads_file, 'r') as f:
            leads = json.load(f)
        
        print(f"✅ Loaded {len(leads)} leads from {leads_file}")
        return leads[:10]  # Limit to first 10 for testing
        
    except Exception as e:
        print(f"❌ Error loading leads: {e}")
        return []

def create_wellness125_email(company_info):
    """
    Create Wellness 125 outreach email
    
    Args:
        company_info: Dictionary with company details
        
    Returns:
        tuple: (subject, body_text, body_html)
    """
    company = company_info.get('company', '')
    industry = company_info.get('industry', '')
    employees = company_info.get('employees', 0)
    location = company_info.get('location', '')
    estimated_savings = company_info.get('estimated_savings', 0)
    
    # Format savings for display
    if estimated_savings >= 1000000:
        savings_display = f"${estimated_savings/1000000:.1f}M"
    else:
        savings_display = f"${estimated_savings/1000:.0f}K"
    
    # Subject line
    subject = f"Wellness 125 Cafeteria Plan for {company}"
    
    # Text body
    body_text = f"""Dear {company} Team,

I'm reaching out regarding your employee benefits program. 

Based on your company size ({employees} employees in {industry}), I wanted to introduce you to the Wellness 125 Cafeteria Plan.

The Wellness 125 Plan allows employees to pay for health insurance premiums, medical expenses, and dependent care with pre-tax dollars, reducing both employee taxable income and employer payroll taxes.

For a company of your size, this could mean estimated savings of {savings_display} annually through reduced FICA taxes and workers' compensation premiums.

Key benefits:
• Employees save 25-40% on healthcare costs (pre-tax dollars)
• Employers save 7.65% on FICA taxes for every dollar contributed
• Workers' compensation premiums reduced by up to 30%
• Improved employee retention and satisfaction
• No cost to implement (administration fees covered by savings)

The plan is particularly effective for companies with 20+ employees and has shown strong adoption in the {industry} sector.

Would you be open to a brief 15-minute call next week to discuss how this could benefit {company}?

{STANDARD_SIGNATURE}"""
    
    # HTML body (optional, same content)
    body_html = f"""<html>
<body>
<p>Dear {company} Team,</p>

<p>I'm reaching out regarding your employee benefits program.</p>

<p>Based on your company size (<strong>{employees} employees in {industry}</strong>), I wanted to introduce you to the <strong>Wellness 125 Cafeteria Plan</strong>.</p>

<p>The Wellness 125 Plan allows employees to pay for health insurance premiums, medical expenses, and dependent care with <strong>pre-tax dollars</strong>, reducing both employee taxable income and employer payroll taxes.</p>

<p>For a company of your size, this could mean estimated savings of <strong>{savings_display} annually</strong> through reduced FICA taxes and workers' compensation premiums.</p>

<h3>Key benefits:</h3>
<ul>
<li>Employees save 25-40% on healthcare costs (pre-tax dollars)</li>
<li>Employers save 7.65% on FICA taxes for every dollar contributed</li>
<li>Workers' compensation premiums reduced by up to 30%</li>
<li>Improved employee retention and satisfaction</li>
<li>No cost to implement (administration fees covered by savings)</li>
</ul>

<p>The plan is particularly effective for companies with <strong>20+ employees</strong> and has shown strong adoption in the {industry} sector.</p>

<p>Would you be open to a brief 15-minute call next week to discuss how this could benefit {company}?</p>

<p>{STANDARD_SIGNATURE.replace(chr(10), '<br>')}</p>
</body>
</html>"""
    
    return subject, body_text, body_html

def main():
    """Main function to send Wellness 125 outreach emails"""
    print("======================================================================")
    print("🏥 WELLNESS 125 OUTREACH - GMAIL SMTP VERSION")
    print("======================================================================")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load today's leads
    leads = load_todays_leads()
    
    if not leads:
        print("❌ No leads to process. Exiting.")
        return
    
    print(f"📊 Found {len(leads)} leads to process")
    print()
    
    # Initialize Gmail sender (using primary account: sam@cubiczan.com)
    sender = GmailSender(account_index=0, delay_seconds=3)
    print(f"📧 Using Gmail account: {sender.account['email']}")
    print(f"⏰ Delay between emails: {sender.delay_seconds} seconds")
    print()
    
    # Track results
    results = {
        "total": len(leads),
        "sent": 0,
        "failed": 0,
        "details": []
    }
    
    # Process each lead
    for i, lead in enumerate(leads, 1):
        company = lead.get('company', 'Unknown')
        email = lead.get('email', '')
        employees = lead.get('employees', 0)
        
        print(f"📨 Processing {i}/{len(leads)}: {company} ({employees} employees)")
        
        if not email:
            print(f"   ⚠️  Skipping: No email address for {company}")
            results["details"].append({
                "company": company,
                "status": "skipped",
                "reason": "No email address"
            })
            continue
        
        # Create email content
        subject, body_text, body_html = create_wellness125_email(lead)
        
        # Send email
        try:
            print(f"   📤 Sending to: {email}")
            
            result = sender.send_email(
                to_emails=email,
                subject=subject,
                body_text=body_text,
                body_html=body_html,
                cc_emails=["sam@impactquadrant.info"]
            )
            
            if result.get("success"):
                print(f"   ✅ Sent successfully")
                results["sent"] += 1
                results["details"].append({
                    "company": company,
                    "email": email,
                    "status": "sent",
                    "message_id": result.get("message_id", "")
                })
            else:
                print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
                results["failed"] += 1
                results["details"].append({
                    "company": company,
                    "email": email,
                    "status": "failed",
                    "error": result.get("error", "Unknown error")
                })
                
        except Exception as e:
            print(f"   ❌ Error sending to {company}: {e}")
            results["failed"] += 1
            results["details"].append({
                "company": company,
                "email": email,
                "status": "error",
                "error": str(e)
            })
        
        print()
    
    # Print summary
    print("======================================================================")
    print("📊 OUTREACH SUMMARY")
    print("======================================================================")
    print(f"Total leads: {results['total']}")
    print(f"Successfully sent: {results['sent']}")
    print(f"Failed: {results['failed']}")
    print(f"Success rate: {(results['sent']/results['total']*100):.1f}%" if results['total'] > 0 else "N/A")
    print()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    results_file = f"/Users/cubiczan/.openclaw/workspace/wellness-125-leads/outreach_results_{timestamp}.json"
    
    results_data = {
        "timestamp": datetime.now().isoformat(),
        "campaign": "Wellness 125 Outreach",
        "email_system": "Gmail SMTP",
        "from_email": sender.account['email'],
        "summary": {
            "total": results["total"],
            "sent": results["sent"],
            "failed": results["failed"]
        },
        "details": results["details"]
    }
    
    try:
        with open(results_file, 'w') as f:
            json.dump(results_data, f, indent=2)
        print(f"📄 Results saved to: {results_file}")
    except Exception as e:
        print(f"⚠️  Could not save results: {e}")
    
    print()
    print("✅ Wellness 125 outreach completed using Gmail SMTP")
    print("📧 From: sam@cubiczan.com")
    print("📋 CC: sam@impactquadrant.info")
    print("🎯 Standard signature with 'Agent Manager' title")
    print("======================================================================")

if __name__ == "__main__":
    main()