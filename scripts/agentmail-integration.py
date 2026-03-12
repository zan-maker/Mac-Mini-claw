#!/usr/bin/env python3
"""
AgentMail Integration for Lead Outreach
Sends personalized outreach emails with CC to sam@impactquadrant.info
"""

import requests
import json
from datetime import datetime

# AgentMail Configuration
AGENTMAIL_API_KEY = "am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
AGENTMAIL_INBOX = "zane@agentmail.to"  # Use lowercase
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

    # Add HTML version if provided
    if html_content:
        payload["html"] = html_content

    # Add CC if provided
    if cc:
        payload["cc"] = [cc] if isinstance(cc, str) else cc

    try:
        # Correct endpoint: /v0/inboxes/{inbox_id}/messages/send
        response = requests.post(
            f"{BASE_URL}/inboxes/{AGENTMAIL_INBOX}/messages/send",
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

def create_outreach_email(company_name, employee_count, industry, decision_maker_name, decision_maker_email):
    """Create personalized outreach email for Wellness 125"""

    # Calculate potential savings
    fica_savings = employee_count * 681
    workers_comp_savings = employee_count * 500 * 0.30
    total_savings = fica_savings + workers_comp_savings

    # Subject line
    subject = f"${total_savings:,} annual savings for {company_name} (zero cost to implement)"

    # Plain text version
    text_content = f"""Hi {decision_maker_name.split()[0] if decision_maker_name else 'there'},

I noticed {company_name} has about {employee_count} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.

Organizations your size are typically saving:
• $681 per employee annually in FICA savings
• 30-60% reduction in workers' comp premiums
• Total savings: ${total_savings:,}

One medical transportation company with 66 employees saved over $140,000 last year.

The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.

Would you be open to a 10-minute call this week to see the numbers for {company_name}?

Best,
Zane
Zane@agentmail.to
Wellness 125 Cafeteria Plan
"""

    # HTML version
    html_content = f"""<p>Hi {decision_maker_name.split()[0] if decision_maker_name else 'there'},</p>

<p>I noticed {company_name} has about {employee_count} employees, which positions you for significant annual savings through a compliant Section 125 wellness program.</p>

<p><strong>Organizations your size are typically saving:</strong></p>
<ul>
<li>$681 per employee annually in FICA savings</li>
<li>30-60% reduction in workers' comp premiums</li>
<li><strong>Total savings: ${total_savings:,}</strong></li>
</ul>

<p>One medical transportation company with 66 employees saved over $140,000 last year.</p>

<p>The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.</p>

<p>Would you be open to a 10-minute call this week to see the numbers for {company_name}?</p>

<p>Best,<br>
Zane<br>
Zane@agentmail.to<br>
Wellness 125 Cafeteria Plan</p>
"""

    return {
        "to": decision_maker_email,
        "subject": subject,
        "text": text_content,
        "html": html_content,
        "cc": CC_EMAIL
    }

def send_initial_outreach(lead_data):
    """Send initial outreach email to a lead"""

    email_data = create_outreach_email(
        company_name=lead_data.get("company_name", "Company"),
        employee_count=lead_data.get("employees_count", 0),
        industry=lead_data.get("industry", ""),
        decision_maker_name=lead_data.get("decision_maker", {}).get("name", "Decision Maker"),
        decision_maker_email=lead_data.get("decision_maker", {}).get("email", "")
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

    subject = f"Re: {lead_data.get('potential_savings', {}).get('total', 0):,} annual savings for {lead_data.get('company_name', 'Company')}"

    text = f"""Hi {lead_data.get('decision_maker', {}).get('name', '').split()[0] if lead_data.get('decision_maker', {}).get('name') else 'there'},

Just following up on my note about the Wellness 125 program. Happy to run a quick savings analysis based on your actual payroll data - takes about 5 minutes to share, shows exact savings broken down by employee count and wage bands.

No cost, no commitment. Just a clear view of what you could save.

Worth a quick call?

Best,
Zane
"""

    html = f"""<p>Hi {lead_data.get('decision_maker', {}).get('name', '').split()[0] if lead_data.get('decision_maker', {}).get('name') else 'there'},</p>

<p>Just following up on my note about the Wellness 125 program. Happy to run a quick savings analysis based on your actual payroll data - takes about 5 minutes to share, shows exact savings broken down by employee count and wage bands.</p>

<p><strong>No cost, no commitment.</strong> Just a clear view of what you could save.</p>

<p>Worth a quick call?</p>

<p>Best,<br>Zane</p>
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
    print("AgentMail Integration Test - Wellness 125 Outreach")
    print("="*60 + "\n")

    # Test with sample lead
    sample_lead = {
        "company_name": "Test Company Inc",
        "employees_count": 50,
        "industry": "Healthcare",
        "decision_maker": {
            "name": "John Smith",
            "email": "test@example.com"  # Replace with actual test email
        },
        "potential_savings": {
            "total": 34050
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
