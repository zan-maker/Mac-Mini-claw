#!/usr/bin/env python3
"""
Send Dorada Wave 5 investor outreach email
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "sam@impactquadrant.info"
EMAIL_PASSWORD = "ajup xyhf abbx iugj"  # App password

# Recipient details for Wave 5
RECIPIENTS = [
    {
        "name": "Matt Atkin",
        "email": "matkin@bluelionglobal.com",
        "company": "Blue Lion",
        "sectors": "real estate, food & beverage, and hospitality"
    }
]

def create_email(recipient):
    """Create personalized email for Wave 5 contact"""
    
    subject = "Luxury hospitality platform in Costa Rica - Multi-stream revenue opportunity"
    
    body = f"""Dear Mr. {recipient['name'].split()[-1]},

I'm reaching out regarding Dorada, a category-defining luxury wellness and longevity platform in Costa Rica's Blue Zone.

Given {recipient['company']}'s focus on {recipient['sectors']}, I believe Dorada represents a strategic opportunity as a multi-stream revenue platform:

**Revenue Streams:**
- Luxury real estate sales and appreciation
- Hospitality and branded residence income
- High-margin longevity and performance programs (7-10 day intensives)
- Membership-based recurring revenues
- Farm-to-table dining and experiential services

**Core Differentiator:**
The Longevity & Human Performance Center delivers personalized, data-driven healthspan interventions—transforming Dorada from a destination into a lifetime engagement model with materially higher customer LTV.

**Asset Overview:**
- 300-acre protected bio-reserve with panoramic ocean views
- 40 private estate homes (1+ acre lots)
- Ultra-low density, premium positioning
- Replicable model across Blue Zone geographies
- Brand extensibility into digital health and affiliated clinics

The global wellness and longevity economy is projected to reach $2.1T by 2030 (12.4% CAGR). Dorada is positioned at the intersection of this trend with defensible scientific credibility.

Would you be open to reviewing the investor deck?

Best,

Sam Desigan

---
For further information, reach Sam Desigan (Agent Manager)
sam@impactquadrant.info
"""
    
    return subject, body

def send_email(recipient):
    """Send email to recipient"""
    
    subject, body = create_email(recipient)
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient['email']
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Connect to SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        # Send email
        server.sendmail(EMAIL_ADDRESS, recipient['email'], msg.as_string())
        server.quit()
        
        print(f"✅ Email sent successfully to {recipient['name']} at {recipient['email']}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email to {recipient['name']}: {str(e)}")
        return False

def main():
    """Send Wave 5 emails (one per day)"""
    
    print("=" * 60)
    print("DORADA RESORT - WAVE 5 INVESTOR OUTREACH")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Send first recipient only (one email per day)
    recipient = RECIPIENTS[0]
    
    print(f"\nSending email to: {recipient['name']} ({recipient['company']})")
    print(f"Email: {recipient['email']}")
    
    success = send_email(recipient)
    
    if success:
        print("\n✅ Wave 5 email sent successfully for today!")
        print(f"Next recipient: Colin Bosa (Bosa Properties) - cbosa@bosaproperties.com")
    else:
        print("\n❌ Failed to send Wave 5 email")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
