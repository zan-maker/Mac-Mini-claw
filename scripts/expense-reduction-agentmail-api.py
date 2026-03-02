#!/usr/bin/env python3
"""
Expense Reduction Outreach via AgentMail API
Sends personalized outreach emails for OPEX reduction services
"""

import requests
import json
from datetime import datetime

# AgentMail Configuration
AGENTMAIL_API_KEY = "am_us_f03e762c50d6e353bbe7b4307b452bd73f58aed725bc0ef53f25d9f8e91c962a"
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

    # Add HTML version if provided
    if html_content:
        payload["html"] = html_content

    # Add CC if provided
    if cc:
        payload["cc"] = [cc] if isinstance(cc, str) else cc

    try:
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

def create_initial_outreach_email(company_name, employee_count, industry, estimated_opex, decision_maker_name=None):
    """Create Day 1: Initial outreach email"""

    # Calculate potential savings (15-30% of OPEX)
    savings_low = int(estimated_opex * 0.15)
    savings_high = int(estimated_opex * 0.30)
    
    # Personalize subject
    subject = f"Reduce {company_name}'s OPEX by 15-30% with success-based pricing"
    
    # Get first name for personalization
    first_name = decision_maker_name.split()[0] if decision_maker_name else "there"

    # Plain text version
    text_content = f"""Hi {first_name},

I noticed {company_name} is at a growth stage where expense management becomes critical to margins. Most companies your size are overspending on SaaS, telecom, and vendor contracts—but lack the bandwidth to continuously optimize.

We offer a technology-led expense reduction service that:
- Identifies savings across OPEX categories (SaaS, telecom, logistics, vendors)
- Uses automation to continuously surface opportunities
- Charges success fees ONLY on verified savings you can see in your own financials

If we don't deliver savings, you pay only a modest admin fee. No risk.

Organizations typically see 15-30% OPEX reduction within 6 months.

Worth a 15-minute call to see what this could look like for {company_name}?

Best,
Zander

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info
"""

    # HTML version
    html_content = f"""<p>Hi {first_name},</p>

<p>I noticed {company_name} is at a growth stage where expense management becomes critical to margins. Most companies your size are overspending on SaaS, telecom, and vendor contracts—but lack the bandwidth to continuously optimize.</p>

<p><strong>We offer a technology-led expense reduction service that:</strong></p>
<ul>
<li>Identifies savings across OPEX categories (SaaS, telecom, logistics, vendors)</li>
<li>Uses automation to continuously surface opportunities</li>
<li>Charges success fees ONLY on verified savings you can see in your own financials</li>
</ul>

<p>If we don't deliver savings, you pay only a modest admin fee. <strong>No risk.</strong></p>

<p>Organizations typically see 15-30% OPEX reduction within 6 months.</p>

<p>Worth a 15-minute call to see what this could look like for {company_name}?</p>

<p>Best,<br>
Zander</p>

<hr>
<p><em>For further information, reach Sam Desigan (Agent Manager)<br>
sam@impactquadrant.info</em></p>
"""

    return {
        "to": None,  # Will be set when sending
        "subject": subject,
        "text": text_content,
        "html": html_content,
        "cc": CC_EMAIL,
        "potential_savings": f"${savings_low:,} - ${savings_high:,}"
    }

def create_followup_day4(company_name, decision_maker_name=None):
    """Create Day 4: Follow-up #1"""
    
    first_name = decision_maker_name.split()[0] if decision_maker_name else "there"
    subject = f"Re: OPEX reduction for {company_name}"

    text = f"""Hi {first_name},

Quick follow-up on expense reduction.

Most CFOs we talk to are spending 10-20 hours per month on vendor reviews, contract renewals, and spend analysis—tasks that are important but don't scale.

Our automation handles the heavy lifting:
- Continuous monitoring of spend patterns
- Automated identification of savings opportunities
- Clear reporting on what's been saved (in your numbers, not ours)

The model is simple: modest admin fee + success fees only on verified savings.

Open to a quick call to see the math?

Best,
Zander

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info
"""

    html = f"""<p>Hi {first_name},</p>

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

<hr>
<p><em>For further information, reach Sam Desigan (Agent Manager)<br>
sam@impactquadrant.info</em></p>
"""

    return {"subject": subject, "text": text, "html": html, "cc": CC_EMAIL}

def create_followup_day7(company_name, decision_maker_name=None):
    """Create Day 7: Follow-up #2 (one question)"""
    
    first_name = decision_maker_name.split()[0] if decision_maker_name else "there"
    subject = f"{company_name} expense reduction - one quick question"

    text = f"""Hi {first_name},

One question: if we could reduce your OPEX by 15-30% and you only paid when you saw the savings in your own financials, would that be worth exploring?

If yes, let's chat.

If no timing-wise, I'll stop reaching out.

Best,
Zander

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info
"""

    html = f"""<p>Hi {first_name},</p>

<p><strong>One question:</strong> if we could reduce your OPEX by 15-30% and you only paid when you saw the savings in your own financials, would that be worth exploring?</p>

<p>If yes, let's chat.</p>

<p>If no timing-wise, I'll stop reaching out.</p>

<p>Best,<br>Zander</p>

<hr>
<p><em>For further information, reach Sam Desigan (Agent Manager)<br>
sam@impactquadrant.info</em></p>
"""

    return {"subject": subject, "text": text, "html": html, "cc": CC_EMAIL}

def create_breakup_email(company_name, decision_maker_name=None):
    """Create Day 14: Break-up email"""
    
    first_name = decision_maker_name.split()[0] if decision_maker_name else "there"
    subject = f"Last note: {company_name} expense reduction"

    text = f"""Hi {first_name},

I'll stop reaching out after this, but wanted to leave the door open.

If OPEX becomes a focus area down the road—whether it's SaaS creep, vendor renegotiations, or travel policy—our model is worth a look. Technology-led, success-based, zero risk.

Here if you need it.

Best,
Zander

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info
"""

    html = f"""<p>Hi {first_name},</p>

<p>I'll stop reaching out after this, but wanted to leave the door open.</p>

<p>If OPEX becomes a focus area down the road—whether it's SaaS creep, vendor renegotiations, or travel policy—our model is worth a look. Technology-led, success-based, zero risk.</p>

<p>Here if you need it.</p>

<p>Best,<br>Zander</p>

<hr>
<p><em>For further information, reach Sam Desigan (Agent Manager)<br>
sam@impactquadrant.info</em></p>
"""

    return {"subject": subject, "text": text, "html": html, "cc": CC_EMAIL}

def send_initial_outreach(lead_data):
    """Send initial outreach email to a lead"""
    
    email_template = create_initial_outreach_email(
        company_name=lead_data.get("company_name", "Company"),
        employee_count=lead_data.get("employees", 0),
        industry=lead_data.get("industry", ""),
        estimated_opex=lead_data.get("estimated_opex", 0),
        decision_maker_name=lead_data.get("contact_name", None)
    )
    
    result = send_email(
        to_email=lead_data.get("contact_email", ""),
        subject=email_template["subject"],
        text_content=email_template["text"],
        html_content=email_template["html"],
        cc=email_template["cc"]
    )
    
    result["potential_savings"] = email_template["potential_savings"]
    return result

def send_followup(lead_data, day_sequence):
    """Send follow-up email based on day sequence"""
    
    company_name = lead_data.get("company_name", "Company")
    contact_name = lead_data.get("contact_name", None)
    contact_email = lead_data.get("contact_email", "")
    
    if day_sequence == 4:
        email_template = create_followup_day4(company_name, contact_name)
    elif day_sequence == 7:
        email_template = create_followup_day7(company_name, contact_name)
    elif day_sequence == 14:
        email_template = create_breakup_email(company_name, contact_name)
    else:
        return {"success": False, "error": f"Invalid day sequence: {day_sequence}"}
    
    result = send_email(
        to_email=contact_email,
        subject=email_template["subject"],
        text_content=email_template["text"],
        html_content=email_template["html"],
        cc=email_template["cc"]
    )
    
    result["day"] = day_sequence
    return result

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Expense Reduction AgentMail API - Ready")
    print("="*60)
    print(f"From: {AGENTMAIL_INBOX}")
    print(f"CC: {CC_EMAIL}")
    print(f"API Key: {AGENTMAIL_API_KEY[:20]}...")
    print("\n" + "="*60 + "\n")
