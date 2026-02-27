#!/usr/bin/env python3
"""
Test Gmail SMTP credentials for cubiczan email
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Credentials from b2b-referral-agentmail.py
CRON_GMAIL_EMAIL = "sam@cubiczan.com"
CRON_GMAIL_PASSWORD = "mwzh abbf ssih mjsf"
CRON_GMAIL_CC = "sam@impactquadrant.info"

def test_gmail_smtp():
    """Test Gmail SMTP connection"""
    
    print("Testing Gmail SMTP credentials...")
    print(f"Email: {CRON_GMAIL_EMAIL}")
    print(f"Password: {'*' * len(CRON_GMAIL_PASSWORD)}")
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f'Agent Manager <{CRON_GMAIL_EMAIL}>'
        msg['To'] = CRON_GMAIL_CC  # Send to ourselves for testing
        msg['Subject'] = "Test: Gmail SMTP Credentials Working"
        
        # Add text version
        text_content = """This is a test email to verify Gmail SMTP credentials are working.

If you receive this, the credentials are valid and can be used for Wave 5 outreach.

Best regards,

Agent Manager
"""
        text_part = MIMEText(text_content, 'plain')
        msg.attach(text_part)
        
        # Connect and send
        context = ssl.create_default_context()
        
        print("Connecting to Gmail SMTP server...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            print("Logging in...")
            server.login(CRON_GMAIL_EMAIL, CRON_GMAIL_PASSWORD)
            print("Sending test email...")
            server.sendmail(CRON_GMAIL_EMAIL, [CRON_GMAIL_CC], msg.as_string())
        
        print("✅ SUCCESS: Test email sent!")
        print(f"Check inbox of: {CRON_GMAIL_CC}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_gmail_smtp()
    exit(0 if success else 1)
