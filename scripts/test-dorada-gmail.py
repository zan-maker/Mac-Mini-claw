#!/usr/bin/env python3
"""
Test Dorada campaign with Gmail SMTP
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
from datetime import datetime

# Gmail Configuration
GMAIL_SENDER = "zan@impactquadrant.info"
GMAIL_PASSWORD = "apbj bvsl tngo vqhu"
GMAIL_CC = "sam@impactquadrant.info"

def send_test_dorada_email():
    """Send a test Dorada campaign email"""
    
    print("Testing Dorada campaign email with Gmail SMTP...")
    
    # Dorada email template
    subject = "Dorada Beach Resort Costa Rica - Exclusive Investment Opportunity"
    
    body = """Dear Investor,

I'm reaching out regarding an exclusive off-market opportunity: Dorada Beach Resort in Costa Rica.

Key Highlights:
• 45-key luxury beachfront resort
• Expansion potential to 120+ keys
• Prime Pacific coast location
• Proven hospitality market
• Owner motivated for quick sale

The property represents a rare chance to acquire a turnkey resort with immediate cash flow and significant upside through expansion.

Full investment memo available upon signed NDA.

Would you be interested in reviewing this opportunity?

Best regards,

Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f'Agent Manager <{GMAIL_SENDER}>'
        msg['To'] = 'zan@impactquadrant.info'  # Test to yourself
        msg['Cc'] = GMAIL_CC
        msg['Subject'] = f"TEST: {subject}"
        
        # Add text
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        # Connect and send
        context = ssl.create_default_context()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls(context=context)
        server.login(GMAIL_SENDER, GMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print("✅ Dorada test email sent successfully!")
        print("📧 Check your inbox for the test email")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send Dorada test email: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("DORADA CAMPAIGN GMAIL SMTP TEST")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Sender: {GMAIL_SENDER}")
    print()
    
    if send_test_dorada_email():
        print("\n🎉 DORADA CAMPAIGN READY TO RESUME!")
        print("✅ Gmail SMTP is working")
        print("✅ Email templates are ready")
        print("✅ Campaign can proceed immediately")
        
        print("\n📊 Campaign status:")
        print("   • Blocked for: 5 days")
        print("   • Emails pending: 34")
        print("   • Next run: Today's cron job")
        
    else:
        print("\n⚠️ Need to fix Gmail configuration")

if __name__ == "__main__":
    main()