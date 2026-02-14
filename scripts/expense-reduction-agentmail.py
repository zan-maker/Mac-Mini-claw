#!/usr/bin/env python3
"""
AgentMail Integration for Expense Reduction Outreach
Sends emails from Zander@agentmail.to with CC to sam@impactquadrant.info
"""

import requests
import json
from datetime import datetime

# AgentMail Configuration for Expense Reduction
AGENTMAIL_API_KEY = "am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f"
AGENTMAIL_INBOX = "Zander@agentmail.to"
CC_EMAIL = "sam@impactquadrant.info"

# Base URL for AgentMail API
BASE_URL = "https://api.agentmail.to/v0"

def send_email(to_email, subject, text_content, html_content=None, cc=None):
    """Send an email via AgentMail API"""

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
        response = requests.post(
            f"{BASE_URL}/inboxes/{AGENTMAIL_INBOX}/messages",
            headers=headers,
            json=payload
        )

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
Zander@agentmail.to
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
Zander@agentmail.to<br>
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
    print("AgentMail Integration Test - Expense Reduction Outreach")
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
