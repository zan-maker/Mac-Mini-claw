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
Miami Hotels Wave 3 - Email Sender
Sends personalized outreach emails via SMTP
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# SMTP Configuration
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "zan@impactquadrant.info"
SMTP_PASS = "cqma sflq nsfv itke"

# Sender info
FROM_EMAIL = SMTP_USER
FROM_NAME = "Claw"

def send_email(to_email: str, to_name: str, subject: str, body: str) -> bool:
    """Send email via SMTP"""
    if not SMTP_USER or not SMTP_PASS:
        print("ERROR: SMTP credentials not configured")
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg['To'] = to_email
        
        # Plain text version
        text_body = body.replace('**', '').replace('*', '')
        msg.attach(MIMEText(text_body, 'plain'))
        
        # HTML version
        html_body = body.replace('\n', '<br>')
        msg.attach(MIMEText(html_body, 'html'))
        
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        
        print(f"✅ Email sent successfully to {to_name} <{to_email}>")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
        return False

# Wave 3 - Jeffrey Silverman (Agman) - Template 1 (Tides)
EMAIL_DATA = {
    "to_email": "jeffrey.silverman@agmanpartners.com",
    "to_name": "Jeffrey Silverman",
    "subject": "Trophy oceanfront asset - Miami Beach (45 suites + 95-key expansion)",
    "body": """Dear Jeffrey,

I'm reaching out regarding a rare oceanfront hospitality opportunity in Miami Beach—The Tides South Beach & Tides Village.

Key Highlights:
• Prime Location: 1220 Ocean Drive, direct beachfront on Miami Beach
• Current Asset: 45 luxury suites (100% oceanfront, avg 652 sq ft)
• Expansion Opportunity: 95 additional keys across three parcels
• Grandfathered Beach Rights: Exclusive beach service (chairs, umbrellas, F&B)
• Recent Renovation: $18M capital program ($400K/key)
• Market Position: Luxury segment, one of highest RevPAR markets in US

Investment Thesis:
• Trophy oceanfront positioning with expansion potential
• ADR upside via rebranding (currently underperforming comp set)
• Mixed-use opportunity with new F&B/retail components
• Scale to 140 total keys post-expansion

Miami Beach Market:
• 12M+ annual visitors
• $17B tourism spend
• Limited new supply due to zoning constraints

Would you be interested in reviewing the confidential offering memorandum?

Best,
Claw

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info"""
}

if __name__ == "__main__":
    print(f"\n📧 Miami Hotels Wave 3 - Sending email")
    print(f"   To: {EMAIL_DATA['to_name']} ({EMAIL_DATA['to_email']})")
    print(f"   Subject: {EMAIL_DATA['subject']}")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    success = send_email(
        EMAIL_DATA['to_email'],
        EMAIL_DATA['to_name'],
        EMAIL_DATA['subject'],
        EMAIL_DATA['body']
    )
    
    if success:
        print(f"\n✅ Wave 3 email #1 sent successfully!")
    else:
        print(f"\n❌ Failed to send Wave 3 email")
