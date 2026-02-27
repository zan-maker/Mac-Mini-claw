#!/usr/bin/env python3
# CRON JOB DEDICATED GMAIL ACCOUNT
CRON_GMAIL_EMAIL = "sam@cubiczan.com"
CRON_GMAIL_PASSWORD = "mwzh abbf ssih mjsf"
CRON_GMAIL_CC = "sam@impactquadrant.info"

STANDARD_SIGNATURE = """Best regards,

def send_cron_email(to_emails, subject, body_text, body_html=None, cc_emails=None):
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
B2B Referral Fee Engine - Gmail SMTP (Cron) Integration
Sends emails from Zander@cron_gmail.to with CC to sam@impactquadrant.info
Dual-sided outreach: prospects (demand) + service providers (supply)
"""

import requests
import json
from datetime import datetime

# Gmail SMTP (Cron) Configuration
# Removed old Gmail SMTP (Cron) API key
AGENTMAIL_INBOX = "Zander@cron_gmail.to"
CC_EMAIL = "sam@impactquadrant.info"

BASE_URL = "https://api.cron_gmail.to/v0"

def send_email(to_email, subject, text_content, html_content=None, cc=None):
    """Send email via Gmail SMTP (Cron) API"""
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
        response = send_cron_email(to_emails, subject, body_text)
        if response.status_code == 200:
            return {"success": True, "message_id": response.json().get("message_id")}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# DEMAND-SIDE: Prospect Outreach

def create_prospect_email(company_name, signal, service_needed, contact_name, contact_email):
    """Create email to prospect (business needing services)"""
    
    subject = f"Quick question about {signal}"
    
    text = f"""Hi {contact_name.split()[0] if contact_name else 'there'},

Congrats on {signal}. Companies at your stage typically start evaluating {service_needed} around this time.

I work with a network of vetted service providers and have helped similar companies find the right fit quickly. Happy to make a no-obligation introduction if this is on your radar.

Worth a quick chat?

Best,
Zander
"""
    
    html = f"""<p>Hi {contact_name.split()[0] if contact_name else 'there'},</p>

<p>Congrats on {signal}. Companies at your stage typically start evaluating {service_needed} around this time.</p>

<p>I work with a network of vetted service providers and have helped similar companies find the right fit quickly. Happy to make a no-obligation introduction if this is on your radar.</p>

<p>Worth a quick chat?</p>

<p>Best,<br>Zander</p>
"""
    
    return {"to": contact_email, "subject": subject, "text": text, "html": html, "cc": CC_EMAIL}

# SUPPLY-SIDE: Service Provider Outreach

def create_provider_email(firm_name, service_type, contact_name, contact_email, vertical):
    """Create email to service provider (seeking referral partnership)"""
    
    subject = f"Referral partnership — qualified {vertical} leads"
    
    text = f"""Hi {contact_name.split()[0] if contact_name else 'there'},

I run a business advisory network that connects growing companies with vetted {service_type} providers. We're currently working with companies showing strong buying signals for {service_type}.

We'd like to explore a referral partnership where we introduce qualified prospects to your firm in exchange for a standard referral fee on closed engagements.

Our introductions are pre-qualified — we only connect companies that have demonstrated clear intent and fit for your services.

Would you be open to a 15-minute call this week to discuss terms?

Best,
Zander
"""
    
    html = f"""<p>Hi {contact_name.split()[0] if contact_name else 'there'},</p>

<p>I run a business advisory network that connects growing companies with vetted {service_type} providers. We're currently working with companies showing strong buying signals for {service_type}.</p>

<p>We'd like to explore a <strong>referral partnership</strong> where we introduce qualified prospects to your firm in exchange for a standard referral fee on closed engagements.</p>

<p>Our introductions are pre-qualified — we only connect companies that have demonstrated clear intent and fit for your services.</p>

<p>Would you be open to a 15-minute call this week to discuss terms?</p>

<p>Best,<br>Zander</p>
"""
    
    return {"to": contact_email, "subject": subject, "text": text, "html": html, "cc": CC_EMAIL}

def send_prospect_outreach(prospect_data):
    """Send outreach to prospect"""
    email = create_prospect_email(
        company_name=prospect_data.get("company_name", ""),
        signal=prospect_data.get("signal", "your recent growth"),
        service_needed=prospect_data.get("service_needed", "professional services"),
        contact_name=prospect_data.get("contact_name", ""),
        contact_email=prospect_data.get("contact_email", "")
    )
    return send_email(email["to"], email["subject"], email["text"], email["html"], email["cc"])

def send_provider_outreach(provider_data):
    """Send outreach to service provider"""
    email = create_provider_email(
        firm_name=provider_data.get("firm_name", ""),
        service_type=provider_data.get("service_type", ""),
        contact_name=provider_data.get("contact_name", ""),
        contact_email=provider_data.get("contact_email", ""),
        vertical=provider_data.get("vertical", "")
    )
    return send_email(email["to"], email["subject"], email["text"], email["html"], email["cc"])

if __name__ == "__main__":
    print("\n" + "="*60)
    print("B2B Referral Fee Engine - Gmail SMTP (Cron) Integration")
    print("="*60 + "\n")
    
    print(f"From: {AGENTMAIL_INBOX}")
    print(f"CC: {CC_EMAIL}")
    print("\n✅ Integration configured and ready!")
    print("\n" + "="*60 + "\n")
