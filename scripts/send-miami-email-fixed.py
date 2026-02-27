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
Fixed Miami Hotels email sender using Gmail SMTP (Cron) API instead of Gmail SMTP
"""

import sys
import requests
import json

# Gmail SMTP (Cron) API configuration
# Removed old Gmail SMTP (Cron) API key
FROM_EMAIL = "zane@cron_gmail.to"
CC_EMAILS = ["cubiczan1@gmail.com", "sam@impactquadrant.info"]

def send_cron_gmail_email(to_email, subject, body):
    """Send email via Gmail SMTP (Cron) API"""
    
    url = "https://api.cron_gmail.to/v1/emails"
    
    headers = {
        "Authorization": f"Bearer {AGENTMAIL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "from": FROM_EMAIL,
        "to": [to_email],
        "cc": CC_EMAILS,
        "subject": subject,
        "body": body
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        print(f"✅ Email sent successfully to {to_email}")
        return {"success": True, "response": response.json()}
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {str(e)}")
        return {"success": False, "error": str(e)}

def main():
    """Main execution"""
    if len(sys.argv) < 3:
        print("Usage: send-miami-email-fixed.py <to> <subject>")
        print("Body is read from stdin")
        sys.exit(1)
    
    to_email = sys.argv[1]
    subject = sys.argv[2]
    
    # Read body from stdin
    body = sys.stdin.read()
    
    # Send email
    result = send_cron_gmail_email(to_email, subject, body)
    
    # Log result
    log_entry = {
        "to": to_email,
        "subject": subject,
        "success": result["success"],
        "timestamp": "2026-02-25T10:30:00Z"
    }
    
    if not result["success"]:
        log_entry["error"] = result["error"]
    
    # Append to log file
    try:
        with open("/Users/cubiczan/.openclaw/workspace/deals/miami-hotels-send-log.md", "a") as f:
            f.write(f"\n- {to_email}: {'✅ Sent' if result['success'] else '❌ Failed'}")
    except:
        pass
    
    sys.exit(0 if result["success"] else 1)

if __name__ == "__main__":
    main()
