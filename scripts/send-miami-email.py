#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

# Email configuration
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "zan@impactquadrant.info"
SMTP_PASS = "cqma sflq nsfv itke"

def send_email(to, subject, body):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = to
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        text = msg.as_string()
        server.sendmail(SMTP_USER, to, text)
        server.quit()
        print(f"✅ Email sent successfully to {to}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: send-miami-email.py <to> <subject>")
        sys.exit(1)
    
    to = sys.argv[1]
    subject = sys.argv[2]
    
    # Read body from stdin
    body = sys.stdin.read()
    
    send_email(to, subject, body)
