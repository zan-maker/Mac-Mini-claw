#!/usr/bin/env python3
"""
Send email to Jon Flood at Roseview
Miami Hotels Portfolio - Template 3 (Both Assets)
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Email configuration
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = "zan@impactquadrant.info"
FROM_PASSWORD = "cqma sflq nsfv itke"  # App password
TO_EMAIL = "jon.flood@madisonmarquette.com"
CC_EMAIL = "sam@impactquadrant.info"

# Create message
msg = MIMEMultipart()
msg['From'] = FROM_EMAIL
msg['To'] = TO_EMAIL
msg['Cc'] = CC_EMAIL
msg['Subject'] = "Two Miami hospitality opportunities - Oceanfront trophy + Mixed-use campus"

# Email body
body = """Dear Jon,

I'm reaching out with two distinct Miami hospitality opportunities that may align with Roseview's investment focus:

**1. Tides South Beach & Tides Village**
- 45 luxury oceanfront suites (South Beach)
- 95-key expansion opportunity
- Direct beachfront with grandfathered rights
- Trophy positioning, ADR upside potential

**2. Thesis Hotel Miami**
- 245 hotel + 204 multifamily + 30K retail
- $315M asking, $18.1M NOI
- Student housing conversion potential
- Adjacent to University of Miami

Both assets offer:
- Strong Miami tourism fundamentals (12M+ visitors, $17B spend)
- Limited new supply dynamics
- Multiple exit pathways
- Institutional-scale opportunities

Would you like to review the confidential materials for either or both assets?

Best regards,

Sam Desigan
Agent Manager

Please reach out to Sam Desigan (sam@impactquadrant.info) for further follow up.
"""

msg.attach(MIMEText(body, 'plain'))

# Send email
try:
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    server.login(FROM_EMAIL, FROM_PASSWORD)
    
    # Send to both TO and CC
    recipients = [TO_EMAIL, CC_EMAIL]
    server.sendmail(FROM_EMAIL, recipients, msg.as_string())
    server.quit()
    
    print(f"✅ Email sent successfully to {TO_EMAIL}")
    print(f"   CC: {CC_EMAIL}")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
except Exception as e:
    print(f"❌ Error sending email: {e}")
    exit(1)
