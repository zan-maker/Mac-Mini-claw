#!/usr/bin/env python3
"""
Cron Job Email Sender - Uses dedicated sam@cubiczan.com account
For all automated cron job email sending
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
from datetime import datetime

# CRON JOB DEDICATED ACCOUNT
CRON_GMAIL = {
    "email": "sam@cubiczan.com",
    "password": "mwzh abbf ssih mjsf",
    "name": "Agent Manager",
    "purpose": "Cron Job Specialist"
}

# Standard configuration
STANDARD_CC = "sam@impactquadrant.info"
STANDARD_SIGNATURE = """Best regards,

Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""

def send_cron_email(to_emails, subject, body_text, body_html=None, cc_emails=None):
    """
    Send email using dedicated cron job Gmail account
    
    Args:
        to_emails: Single email or list
        subject: Email subject
        body_text: Plain text body
        body_html: HTML body (optional)
        cc_emails: CC emails (optional)
    
    Returns:
        (success: bool, message: str)
    """
    
    print(f"📧 Cron job sending email via {CRON_GMAIL['email']}")
    print(f"   To: {to_emails}")
    print(f"   Subject: {subject}")
    
    try:
        # Prepare recipients
        if isinstance(to_emails, str):
            to_list = [to_emails]
        else:
            to_list = to_emails
        
        if cc_emails is None:
            cc_list = [STANDARD_CC]
        elif isinstance(cc_emails, str):
            cc_list = [cc_emails]
        else:
            cc_list = cc_emails
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f'{CRON_GMAIL["name"]} <{CRON_GMAIL["email"]}>'
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
        
        # All recipients
        all_recipients = to_list + cc_list
        
        # Connect and send using dedicated cron account
        context = ssl.create_default_context()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls(context=context)
        server.login(CRON_GMAIL["email"], CRON_GMAIL["password"])
        server.send_message(msg)
        server.quit()
        
        message = f"✅ Cron email sent successfully using {CRON_GMAIL['email']} to {len(all_recipients)} recipients"
        print(f"   {message}")
        return True, message
        
    except Exception as e:
        error_msg = f"❌ Cron email failed: {str(e)}"
        print(f"   {error_msg}")
        return False, error_msg

def test_cron_account():
    """Test the dedicated cron job account"""
    print("=" * 60)
    print("CRON JOB GMAIL ACCOUNT TEST")
    print("=" * 60)
    print(f"Account: {CRON_GMAIL['email']}")
    print(f"Purpose: {CRON_GMAIL['purpose']}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test connection
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls(context=context)
        server.login(CRON_GMAIL["email"], CRON_GMAIL["password"])
        server.quit()
        print("✅ Authentication successful")
        return True
    except Exception as e:
        print(f"❌ Authentication failed: {str(e)}")
        return False

def send_cron_test_email():
    """Send a test email using the cron job account"""
    print("\n" + "=" * 60)
    print("CRON JOB TEST EMAIL")
    print("=" * 60)
    
    test_subject = f"Cron Job Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    test_body = """This is a test email from the dedicated Cron Job Gmail account.

Account: sam@cubiczan.com
Purpose: Dedicated to all automated cron job email sending

This account will be used for:
• Daily lead outreach (2:00 PM)
• Campaign emails (Dorada, Miami, etc.)
• Expense reduction outreach
• Defense sector outreach
• All other automated email sending

Benefits:
• Separation from manual email sending
• Better tracking of automated vs manual
• Dedicated rate limits
• Cleaner analytics

Email outreach that was blocked for 5 days is now UNBLOCKED with dedicated infrastructure!

Next cron job run: Today at 2:00 PM EST
"""
    
    success, message = send_cron_email(
        to_emails="zan@impactquadrant.info",
        subject=test_subject,
        body_text=test_body
    )
    
    return success

def main():
    """Main execution"""
    
    print("=" * 80)
    print("🚀 CRON JOB DEDICATED GMAIL ACCOUNT")
    print("=" * 80)
    print("Setting up sam@cubiczan.com for all automated email sending")
    print()
    
    # Test account
    if not test_cron_account():
        print("\n❌ Cron account test failed")
        return
    
    # Send test email
    if not send_cron_test_email():
        print("\n❌ Cron test email failed")
        return
    
    # Success!
    print("\n" + "=" * 80)
    print("🎉 CRON JOB GMAIL ACCOUNT READY!")
    print("=" * 80)
    
    print("\n✅ Dedicated cron account configured and tested")
    print("✅ All cron jobs should use this account")
    print("✅ Email outreach unblocked after 5 days")
    
    print("\n📊 Account Assignment:")
    print(f"   • Cron Jobs: {CRON_GMAIL['email']} (dedicated)")
    print(f"   • Campaigns: zan@impactquadrant.info (primary)")
    print(f"   • Backup: sam@impactquadrant.info (backup)")
    
    print("\n🎯 Next Steps for Cron Jobs:")
    print("1. Update all cron job scripts to use this function")
    print("2. Change sender to: sam@cubiczan.com")
    print("3. Test with today's 2:00 PM batch")
    print("4. Monitor deliverability and bounce rates")
    
    print("\n⏰ Today's Cron Schedule (EST):")
    print("   • 2:00 PM: Lead Outreach (will use this account)")
    print("   • 2:00 PM: Expense Reduction Outreach")
    print("   • 2:00 PM: Defense Sector Outreach")
    print("   • 4:00 PM: Options Report")
    
    # Save cron configuration
    try:
        config_file = '/Users/cubiczan/.openclaw/workspace/cron-gmail-config.json'
        import json
        with open(config_file, 'w') as f:
            json.dump({
                'configured_at': datetime.now().isoformat(),
                'cron_account': CRON_GMAIL,
                'standard_cc': STANDARD_CC,
                'status': 'active',
                'purpose': 'dedicated_cron_job_sending',
                'cron_jobs_using_this': [
                    'Lead Outreach (2:00 PM daily)',
                    'Expense Reduction Outreach (2:00 PM daily)',
                    'Defense Sector Outreach (2:00 PM daily)',
                    'Dorada Campaigns (10:00 AM daily)',
                    'Miami Campaigns (11:00 AM daily)',
                    'Options Report (4:00 PM daily)'
                ]
            }, f, indent=2)
        print(f"\n📁 Cron configuration saved to: {config_file}")
    except Exception as e:
        print(f"\n⚠️  Could not save config: {str(e)}")

if __name__ == "__main__":
    main()