import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
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
Gmail SMTP (Cron) Integration for Expense Reduction Outreach
Sends emails from Zander@cron_gmail.to with CC to sam@impactquadrant.info
"""

import requests
import json
from datetime import datetime

# Gmail SMTP (Cron) Configuration for Expense Reduction
# Removed old Gmail SMTP (Cron) API key
AGENTMAIL_INBOX = "Zander@cron_gmail.to"
CC_EMAIL = "sam@impactquadrant.info"

# Base URL for Gmail SMTP (Cron) API
BASE_URL = "https://api.cron_gmail.to/v0"

def send_email(to_email, subject, text_content, html_content=None, cc=None):
    """Send an email via Gmail SMTP (Cron) API"""

    headers = {
        "Authorization": f"Bearer {AGENTMAIL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inbox_id": AGENTMAIL_INBOX,
        "to": [to_email],
        "subject": subject,
        "text": text_content
    }

    if html_content:
        payload["html"] = html_content

    if cc:
        payload["cc"] = [cc] if isinstance(cc, str) else cc

    try:
        response = send_email_with_rotation(to_emails, subject, body_text)

        if response.status_code == 200:
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

def create_expense_reduction_email(company_name, employee_count, industry, decision_maker_name, decision_maker_email, savings_estimate):
    """Create personalized outreach email for expense reduction"""

    # Subject line
    subject = f"Reduce {company_name}'s OPEX by 15-30% with success-based pricing"

    # Calculate savings range
    savings_low = int(savings_estimate * 0.15)
    savings_high = int(savings_estimate * 0.30)

    # Plain text version
    text_content = f"""Hi {decision_maker_name.split()[0] if decision_maker_name else 'there'},

I noticed {company_name} is at a growth stage where expense management becomes critical to margins. Most companies your size are overspending on SaaS, telecom, and vendor contracts—but lack the bandwidth to continuously optimize.

We offer a technology-led expense reduction service that:
• Identifies savings across OPEX categories (SaaS, telecom, logistics, vendors)
• Uses automation to continuously surface opportunities
• Charges success fees ONLY on verified savings you can see in your own financials

For a company with {employee_count} employees, we typically see:
• ${savings_low:,} - ${savings_high:,} annual OPEX reduction
• 15-30% savings across key cost categories

If we don't deliver savings, you pay only a modest admin fee. No risk.

Worth a 15-minute call to see what this could look like for {company_name}?

Best,
Zander
Zander@cron_gmail.to
Expense Reduction Services
"""

    # HTML version
    html_content = f"""<p>Hi {decision_maker_name.split()[0] if decision_maker_name else 'there'},</p>

<p>I noticed {company_name} is at a growth stage where expense management becomes critical to margins. Most companies your size are overspending on SaaS, telecom, and vendor contracts—but lack the bandwidth to continuously optimize.</p>

<p><strong>We offer a technology-led expense reduction service that:</strong></p>
<ul>
<li>Identifies savings across OPEX categories (SaaS, telecom, logistics, vendors)</li>
<li>Uses automation to continuously surface opportunities</li>
<li>Charges success fees ONLY on verified savings you can see in your own financials</li>
</ul>

<p><strong>For a company with {employee_count} employees, we typically see:</strong></p>
<ul>
<li>${savings_low:,} - ${savings_high:,} annual OPEX reduction</li>
<li>15-30% savings across key cost categories</li>
</ul>

<p><em>If we don't deliver savings, you pay only a modest admin fee. No risk.</em></p>

<p>Worth a 15-minute call to see what this could look like for {company_name}?</p>

<p>Best,<br>
Zander<br>
Zander@cron_gmail.to<br>
Expense Reduction Services</p>
"""

    return {
        "to": decision_maker_email,
        "subject": subject,
        "text": text_content,
        "html": html_content,
        "cc": CC_EMAIL
    }

def send_initial_outreach(lead_data):
    """Send initial outreach email to an expense reduction lead"""

    savings_estimate = lead_data.get('potential_savings', {}).get('annual_opex', 0)
    
    email_data = create_expense_reduction_email(
        company_name=lead_data.get("company_name", "Company"),
        employee_count=lead_data.get("employees_count", 0),
        industry=lead_data.get("industry", ""),
        decision_maker_name=lead_data.get("decision_maker", {}).get("name", "Decision Maker"),
        decision_maker_email=lead_data.get("decision_maker", {}).get("email", ""),
        savings_estimate=savings_estimate
    )

    result = send_email(
        to_email=email_data["to"],
        subject=email_data["subject"],
        text_content=email_data["text"],
        html_content=email_data["html"],
        cc=email_data["cc"]
    )

    return result

def send_follow_up_day4(lead_data):
    """Send Day 4 follow-up"""

    subject = f"Re: OPEX reduction for {lead_data.get('company_name', 'Company')}"

    text = f"""Hi {lead_data.get('decision_maker', {}).get('name', '').split()[0] if lead_data.get('decision_maker', {}).get('name') else 'there'},

Quick follow-up on expense reduction.

Most CFOs we talk to are spending 10-20 hours per month on vendor reviews, contract renewals, and spend analysis—tasks that are important but don't scale.

Our automation handles the heavy lifting:
• Continuous monitoring of spend patterns
• Automated identification of savings opportunities
• Clear reporting on what's been saved (in your numbers, not ours)

The model is simple: modest admin fee + success fees only on verified savings.

Open to a quick call to see the math?

Best,
Zander
"""

    html = f"""<p>Hi {lead_data.get('decision_maker', {}).get('name', '').split()[0] if lead_data.get('decision_maker', {}).get('name') else 'there'},</p>

<p>Quick follow-up on expense reduction.</p>

<p>Most CFOs we talk to are spending 10-20 hours per month on vendor reviews, contract renewals, and spend analysis—tasks that are important but don't scale.</p>

<p><strong>Our automation handles the heavy lifting:</strong></p>
<ul>
<li>Continuous monitoring of spend patterns</li>
<li>Automated identification of savings opportunities</li>
<li>Clear reporting on what's been saved (in your numbers, not ours)</li>
</ul>

<p>The model is simple: modest admin fee + success fees only on verified savings.</p>

<p>Open to a quick call to see the math?</p>

<p>Best,<br>Zander</p>
"""

    return send_email(
        to_email=lead_data.get("decision_maker", {}).get("email", ""),
        subject=subject,
        text_content=text,
        html_content=html,
        cc=CC_EMAIL
    )

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Gmail SMTP (Cron) Integration Test - Expense Reduction Outreach")
    print("="*60 + "\n")

    # Test with sample lead
    sample_lead = {
        "company_name": "Test Tech Company",
        "employees_count": 75,
        "industry": "Technology - SaaS",
        "decision_maker": {
            "name": "Sarah Johnson",
            "email": "test@example.com"
        },
        "potential_savings": {
            "annual_opex": 900000,
            "savings_low": 135000,
            "savings_high": 270000
        }
    }

    print(f"Sending test email to: {sample_lead['decision_maker']['email']}")
    print(f"CC: {CC_EMAIL}")
    print(f"From: {AGENTMAIL_INBOX}")

    # Send test email (commented out to prevent accidental sends)
    # result = send_initial_outreach(sample_lead)

    # if result['success']:
    #     print(f"✅ Email sent successfully! Message ID: {result['message_id']}")
    # else:
    #     print(f"❌ Error sending email: {result['error']}")

    print("\nEmail integration configured and ready!")
    print(" Uncomment the send code above to test with real email addresses.")
    print("\n" + "="*60 + "\n")
