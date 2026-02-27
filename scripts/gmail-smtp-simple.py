#!/usr/bin/env python3
"""
Gmail SMTP Email Sending - Use instead of AgentMail
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

# Configuration
GMAIL_SENDER = "zan@impactquadrant.info"
GMAIL_PASSWORD = "apbj bvsl tngo vqhu"
GMAIL_CC = "sam@impactquadrant.info"

def send_email_gmail(to_emails, subject, body_text, body_html=None):
    """Send email using Gmail SMTP"""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = f'Agent Manager <{GMAIL_SENDER}>'
        msg['To'] = ', '.join(to_emails) if isinstance(to_emails, list) else to_emails
        msg['Cc'] = GMAIL_CC
        msg['Subject'] = subject
        
        # Add text
        full_text = body_text + "\n\nBest regards,\n\nAgent Manager\n\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."
        text_part = MIMEText(full_text, 'plain')
        msg.attach(text_part)
        
        # Connect and send
        context = ssl.create_default_context()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls(context=context)
        server.login(GMAIL_SENDER, GMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True, "Email sent"
        
    except Exception as e:
        return False, str(e)
