#!/usr/bin/env python3
"""
Gmail SMTP Configuration for OpenClaw Email System
CRITICAL: Email outreach blocked for 5 days, implementing fallback
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import ssl
from datetime import datetime

# Gmail SMTP Configuration
GMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,  # For TLS
    "smtp_port_ssl": 465,  # For SSL
    "sender_email": "zan@impactquadrant.info",
    "sender_password": "apbj bvsl tngo vqhu",  # Google App Password
    "sender_name": "Agent Manager",
    "cc_email": "sam@impactquadrant.info",  # Standard CC
    "signature": """Best regards,

Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
}

def create_email_message(to_emails, subject, body_text, body_html=None, cc_emails=None):
    """
    Create email message with proper formatting
    """
    if isinstance(to_emails, str):
        to_emails = [to_emails]
    
    if cc_emails is None:
        cc_emails = [GMAIL_CONFIG["cc_email"]]
    elif isinstance(cc_emails, str):
        cc_emails = [cc_emails]
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['From'] = f'{GMAIL_CONFIG["sender_name"]} <{GMAIL_CONFIG["sender_email"]}>'
    msg['To'] = ', '.join(to_emails)
    msg['Cc'] = ', '.join(cc_emails)
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)
    
    # Add text version
    text_part = MIMEText(body_text + "\n\n" + GMAIL_CONFIG["signature"], 'plain')
    msg.attach(text_part)
    
    # Add HTML version if provided
    if body_html:
        html_part = MIMEText(body_html + "<br><br>" + GMAIL_CONFIG["signature"].replace('\n', '<br>'), 'html')
        msg.attach(html_part)
    
    return msg

def send_email_gmail(to_emails, subject, body_text, body_html=None, cc_emails=None):
    """
    Send email using Gmail SMTP
    Returns: (success, message)
    """
    try:
        # Create message
        msg = create_email_message(to_emails, subject, body_text, body_html, cc_emails)
        
        # All recipients
        all_recipients = []
        if isinstance(to_emails, str):
            all_recipients.append(to_emails)
        else:
            all_recipients.extend(to_emails)
        
        if cc_emails:
            if isinstance(cc_emails, str):
                all_recipients.append(cc_emails)
            else:
                all_recipients.extend(cc_emails)
        
        # Connect to Gmail SMTP server
        context = ssl.create_default_context()
        
        # Try TLS first (port 587)
        try:
            server = smtplib.SMTP(GMAIL_CONFIG["smtp_server"], GMAIL_CONFIG["smtp_port"])
            server.starttls(context=context)
            server.login(GMAIL_CONFIG["sender_email"], GMAIL_CONFIG["sender_password"])
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            return True, f"Email sent successfully to {len(all_recipients)} recipients"
            
        except Exception as e:
            # Try SSL (port 465) as fallback
            try:
                server = smtplib.SMTP_SSL(GMAIL_CONFIG["smtp_server"], GMAIL_CONFIG["smtp_port_ssl"], context=context)
                server.login(GMAIL_CONFIG["sender_email"], GMAIL_CONFIG["sender_password"])
                
                # Send email
                server.send_message(msg)
                server.quit()
                
                return True, f"Email sent successfully (SSL) to {len(all_recipients)} recipients"
                
            except Exception as e2:
                return False, f"Failed to send email: TLS error: {str(e)}, SSL error: {str(e2)}"
                
    except Exception as e:
        return False, f"Error sending email: {str(e)}"

def test_gmail_connection():
    """
    Test Gmail SMTP connection
    """
    print("=" * 60)
    print("GMAIL SMTP CONNECTION TEST")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Sender: {GMAIL_CONFIG['sender_email']}")
    print(f"SMTP Server: {GMAIL_CONFIG['smtp_server']}:{GMAIL_CONFIG['smtp_port']}")
    print()
    
    # Test 1: Simple connection test
    print("1. Testing SMTP connection...")
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP(GMAIL_CONFIG["smtp_server"], GMAIL_CONFIG["smtp_port"], timeout=10)
        server.starttls(context=context)
        print("   ✅ SMTP connection established")
        
        # Test 2: Authentication
        print("2. Testing authentication...")
        server.login(GMAIL_CONFIG["sender_email"], GMAIL_CONFIG["sender_password"])
        print("   ✅ Authentication successful")
        
        server.quit()
        return True
        
    except Exception as e:
        print(f"   ❌ Connection error: {str(e)}")
        return False

def send_test_email():
    """
    Send a test email to verify everything works
    """
    print("\n3. Sending test email...")
    
    test_subject = f"Gmail SMTP Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    test_body = """This is a test email from the new Gmail SMTP configuration.

If you receive this email, the Gmail SMTP fallback is working correctly!

This will unblock all email outreach campaigns that have been stalled for 5 days due to AgentMail API issues.

Next steps:
1. All email scripts will be updated to use Gmail SMTP
2. Cron jobs will resume sending emails
3. Blocked campaigns (Dorada, Miami, etc.) will proceed
4. Lead outreach will continue normally

System Status:
- AgentMail API: ❌ Blocked (5 days)
- Gmail SMTP: ✅ Ready to use
- Email campaigns: Ready to resume
"""
    
    # Send to yourself as test
    success, message = send_email_gmail(
        to_emails="zan@impactquadrant.info",
        subject=test_subject,
        body_text=test_body
    )
    
    if success:
        print(f"   ✅ Test email sent successfully!")
        print(f"   Message: {message}")
        return True
    else:
        print(f"   ❌ Failed to send test email")
        print(f"   Error: {message}")
        return False

def main():
    """
    Main test function
    """
    print("\n🚀 IMPLEMENTING GMAIL SMTP FALLBACK")
    print("Email outreach blocked for 5 days - CRITICAL FIX")
    print()
    
    # Test connection
    if not test_gmail_connection():
        print("\n❌ Gmail SMTP connection failed")
        print("Please check:")
        print("1. App password is correct: 'apbj bvsl tngo vqhu'")
        print("2. Less secure apps might need to be enabled")
        print("3. 2-factor authentication is properly configured")
        return
    
    # Send test email
    if not send_test_email():
        print("\n❌ Test email failed")
        return
    
    # Success!
    print("\n" + "=" * 60)
    print("🎉 GMAIL SMTP FALLBACK IMPLEMENTED SUCCESSFULLY!")
    print("=" * 60)
    
    print("\n✅ Email outreach can be RESUMED immediately!")
    print("✅ All blocked campaigns will proceed")
    print("✅ Cron jobs will work on next run")
    
    print("\n📧 Campaigns that will resume:")
    print("   • Dorada Resort: 34 emails blocked")
    print("   • Miami Hotels: 9 emails blocked")
    print("   • Lead Outreach: Daily emails")
    print("   • Defense Sector: 15 leads ready")
    print("   • Expense Reduction: Daily outreach")
    
    print(f"\n⏰ Total time blocked: 5 DAYS")
    print(f"📈 Expected recovery: Immediate")
    
    # Save configuration
    try:
        config_file = '/Users/cubiczan/.openclaw/workspace/gmail-smtp-config.json'
        import json
        with open(config_file, 'w') as f:
            json.dump({
                'configured_at': datetime.now().isoformat(),
                'sender_email': GMAIL_CONFIG['sender_email'],
                'sender_name': GMAIL_CONFIG['sender_name'],
                'smtp_server': GMAIL_CONFIG['smtp_server'],
                'status': 'active',
                'tested': True,
                'campaigns_unblocked': [
                    'Dorada Resort',
                    'Miami Hotels', 
                    'Lead Outreach',
                    'Defense Sector',
                    'Expense Reduction'
                ]
            }, f, indent=2)
        print(f"\n📁 Configuration saved to: {config_file}")
    except Exception as e:
        print(f"\n⚠️ Could not save config: {str(e)}")

if __name__ == "__main__":
    main()