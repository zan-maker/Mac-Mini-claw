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
Dorada Resort Wave 2 Outreach - Send to Tier 2 investors
"""

import requests
import json

# Gmail SMTP (Cron) Configuration
# Removed old Gmail SMTP (Cron) API key
AGENTMAIL_INBOX = "Zane@cron_gmail.to"
CC_EMAIL = "sam@impactquadrant.info"
BASE_URL = "https://api.cron_gmail.to/v0"

# Wave 2 - Tier 2 Contacts
WAVE2_CONTACTS = [
    {
        "name": "Andrew Alley",
        "company": "Mitchell Family Office",
        "email": "aalley@mitchellfo.com",
        "version": "family_office"
    }
]

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

def create_dorada_family_office_email(contact):
    """Create FAMILY OFFICE VERSION email for Dorada Resort"""
    
    last_name = contact["name"].split()[-1]
    company = contact["company"]
    
    subject = "Multi-generational wellness asset in Costa Rica's Blue Zone"
    
    text_content = f"""Dear Mr. {last_name},

I'm reaching out regarding Dorada, a first-of-its-kind regenerative destination resort and residential community in one of the world's rare Blue Zone regions of Costa Rica.

Given {company}'s focus on real estate and hospitality investments, I believe Dorada aligns with your investment philosophy—particularly as a multi-generational legacy asset that combines:

• 300-acre protected bio-reserve with panoramic ocean views
• 40 private estate homes (1+ acre lots)
• Longevity & Human Performance Center offering personalized healthspan programs
• Fully off-grid with sustainable infrastructure
• Recurring revenue from wellness programs and memberships

Dorada is the vision of Dr. Vincent Giampapa, a globally recognized leader in anti-aging medicine and regenerative science. It's designed not as a hospitality project, but as a permanent wellness ecosystem for long-term ownership.

Why for family offices: Capital preservation with upside, intergenerational relevance, personal use optionality, and alignment with the $2.1T wellness economy (12.4% CAGR).

Would you be open to a brief call to discuss the opportunity? I'd be happy to share the full investor deck.

Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.
"""

    html_content = f"""<p>Dear Mr. {last_name},</p>

<p>I'm reaching out regarding <strong>Dorada</strong>, a first-of-its-kind regenerative destination resort and residential community in one of the world's rare Blue Zone regions of Costa Rica.</p>

<p>Given {company}'s focus on real estate and hospitality investments, I believe Dorada aligns with your investment philosophy—particularly as a multi-generational legacy asset that combines:</p>

<ul>
<li><strong>300-acre protected bio-reserve</strong> with panoramic ocean views</li>
<li><strong>40 private estate homes</strong> (1+ acre lots)</li>
<li><strong>Longevity & Human Performance Center</strong> offering personalized healthspan programs</li>
<li>Fully off-grid with sustainable infrastructure</li>
<li><strong>Recurring revenue</strong> from wellness programs and memberships</li>
</ul>

<p>Dorada is the vision of <strong>Dr. Vincent Giampapa</strong>, a globally recognized leader in anti-aging medicine and regenerative science. It's designed not as a hospitality project, but as a <strong>permanent wellness ecosystem</strong> for long-term ownership.</p>

<p><strong>Why for family offices:</strong> Capital preservation with upside, intergenerational relevance, personal use optionality, and alignment with the $2.1T wellness economy (12.4% CAGR).</p>

<p>Would you be open to a brief call to discuss the opportunity? I'd be happy to share the full investor deck.</p>

<p>Best regards,<br>
Zane<br>
Agent Manager<br>
Impact Quadrant</p>

<p>Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.</p>
"""

    return {
        "to": contact["email"],
        "subject": subject,
        "text": text_content,
        "html": html_content
    }

def main():
    print("\n" + "="*60)
    print("Dorada Resort - Wave 2 Outreach")
    print("="*60 + "\n")
    
    # Send to first Wave 2 contact (Andrew Alley)
    contact = WAVE2_CONTACTS[0]
    
    print(f"Sending to: {contact['name']} ({contact['company']})")
    print(f"Email: {contact['email']}")
    print(f"CC: {CC_EMAIL}")
    print(f"Template: FAMILY OFFICE VERSION\n")
    
    email_data = create_dorada_family_office_email(contact)
    
    result = send_email(
        to_email=email_data["to"],
        subject=email_data["subject"],
        text_content=email_data["text"],
        html_content=email_data["html"],
        cc=CC_EMAIL
    )
    
    if result['success']:
        print(f"✅ Email sent successfully!")
        print(f"Message ID: {result['message_id']}")
        print(f"\nWave 2 - Contact 1/5 completed")
        return 0
    else:
        print(f"❌ Error sending email: {result['error']}")
        return 1

if __name__ == "__main__":
    exit(main())
