#!/usr/bin/env python3
"""
Test the updated Dorada campaign script with dedicated cron Gmail
"""

import sys
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scripts')

# Import the updated function from dorada script
try:
    # We'll test by importing and calling the function directly
    print("Testing updated Dorada campaign script...")
    
    # Read the script to verify updates
    with open('/Users/cubiczan/.openclaw/workspace/scripts/dorada-wave2-outreach.py', 'r') as f:
        content = f.read()
    
    # Check for key updates
    checks = [
        ("CRON_GMAIL_EMAIL", "sam@cubiczan.com" in content),
        ("CRON_GMAIL_PASSWORD", "mwzh abbf ssih mjsf" in content),
        ("send_cron_email function", "def send_cron_email" in content),
        ("STANDARD_SIGNATURE", "STANDARD_SIGNATURE" in content),
        ("AgentMail removed", "am_us_" not in content),
    ]
    
    print("\n📋 Update Verification:")
    all_passed = True
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"   {status} {check_name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 Dorada script successfully updated for cron Gmail!")
        print("✅ Ready for tomorrow's 10:00 AM campaign")
        print("✅ Will use sam@cubiczan.com for sending")
        print("✅ Email outreach unblocked after 5 days")
        
        print("\n📊 Campaign Details:")
        print("   • Emails pending: 34")
        print("   • Schedule: Tomorrow 10:00 AM EST")
        print("   • Account: sam@cubiczan.com (dedicated cron)")
        print("   • CC: sam@impactquadrant.info")
        
    else:
        print("\n⚠️ Some updates missing from script")
        print("Need to manually fix the script")
        
except Exception as e:
    print(f"❌ Test failed: {str(e)}")

# Also test the actual send function
print("\n" + "=" * 60)
print("TESTING ACTUAL EMAIL SEND")
print("=" * 60)

# Create a simple test using the same logic
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

CRON_GMAIL_EMAIL = "sam@cubiczan.com"
CRON_GMAIL_PASSWORD = "mwzh abbf ssih mjsf"
CRON_GMAIL_CC = "sam@impactquadrant.info"

STANDARD_SIGNATURE = """Best regards,

Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""

def test_send():
    """Test sending an email"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f'Agent Manager <{CRON_GMAIL_EMAIL}>'
        msg['To'] = 'zan@impactquadrant.info'
        msg['Cc'] = CRON_GMAIL_CC
        msg['Subject'] = f"Dorada Script Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Add text
        body_text = "This is a test of the updated Dorada campaign script.\n\nScript now uses dedicated cron Gmail account: sam@cubiczan.com"
        full_text = body_text + "\n\n" + STANDARD_SIGNATURE
        text_part = MIMEText(full_text, 'plain')
        msg.attach(text_part)
        
        # Connect and send
        context = ssl.create_default_context()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls(context=context)
        server.login(CRON_GMAIL_EMAIL, CRON_GMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print("✅ Test email sent successfully!")
        print("📧 Check your inbox for the test email")
        return True
        
    except Exception as e:
        print(f"❌ Test email failed: {str(e)}")
        return False

from datetime import datetime
if test_send():
    print("\n🎉 DORADA CAMPAIGN READY FOR TOMORROW!")
    print("✅ Script updated successfully")
    print("✅ Email sending confirmed working")
    print("✅ Campaign will resume after 5-day blockage")
else:
    print("\n⚠️ Need to fix email sending configuration")