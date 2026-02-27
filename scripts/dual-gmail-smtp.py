#!/usr/bin/env python3
"""
Dual Gmail SMTP Configuration for OpenClaw
Provides redundancy and higher sending capacity
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import random
from datetime import datetime

# DUAL GMAIL CONFIGURATION
GMAIL_ACCOUNTS = [
    {
        "email": "zan@impactquadrant.info",
        "password": "apbj bvsl tngo vqhu",
        "name": "Agent Manager",
        "status": "active",
        "tested": True
    },
    {
        "email": "sam@impactquadrant.info",
        "password": "ajup xyhf abbx iugj",
        "name": "Agent Manager",
        "status": "active",
        "tested": False  # Will test now
    }
]

# Standard configuration
STANDARD_CC = "sam@impactquadrant.info"  # Always CC Sam
STANDARD_SIGNATURE = """Best regards,

Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""

def test_gmail_account(account):
    """Test a Gmail account connection"""
    print(f"Testing {account['email']}...")
    
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls(context=context)
        server.login(account["email"], account["password"])
        server.quit()
        
        print(f"  ✅ Authentication successful")
        account["tested"] = True
        return True
        
    except Exception as e:
        print(f"  ❌ Authentication failed: {str(e)}")
        account["tested"] = False
        return False

def send_email_dual_gmail(to_emails, subject, body_text, body_html=None, cc_emails=None, preferred_account=None):
    """
    Send email using dual Gmail accounts with failover
    
    Args:
        to_emails: Single email or list
        subject: Email subject
        body_text: Plain text body
        body_html: HTML body (optional)
        cc_emails: CC emails (optional)
        preferred_account: "zan" or "sam" (optional)
    
    Returns:
        (success: bool, message: str, account_used: str)
    """
    
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
    
    # Select account
    if preferred_account == "zan":
        accounts_to_try = [GMAIL_ACCOUNTS[0]]
    elif preferred_account == "sam":
        accounts_to_try = [GMAIL_ACCOUNTS[1]]
    else:
        # Try both in order
        accounts_to_try = GMAIL_ACCOUNTS.copy()
    
    # Try each account
    for account in accounts_to_try:
        if not account.get("tested", False):
            # Test it first
            if not test_gmail_account(account):
                continue
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f'{account["name"]} <{account["email"]}>'
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
            
            # Connect and send
            context = ssl.create_default_context()
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls(context=context)
            server.login(account["email"], account["password"])
            server.send_message(msg)
            server.quit()
            
            return True, f"Email sent successfully using {account['email']}", account["email"]
            
        except Exception as e:
            print(f"  ⚠️  {account['email']} failed: {str(e)}")
            continue
    
    # All accounts failed
    return False, "All Gmail accounts failed", None

def test_both_accounts():
    """Test both Gmail accounts"""
    print("=" * 60)
    print("DUAL GMAIL ACCOUNT TEST")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test both accounts
    for account in GMAIL_ACCOUNTS:
        test_gmail_account(account)
    
    print()
    
    # Count active accounts
    active_accounts = [a for a in GMAIL_ACCOUNTS if a.get("tested", False)]
    
    if len(active_accounts) == 2:
        print("✅ BOTH Gmail accounts are working!")
        print("   • Redundancy: ✅ Available")
        print("   • Capacity: ✅ Increased")
        print("   • Reliability: ✅ High")
    elif len(active_accounts) == 1:
        print("⚠️  Only 1 Gmail account is working")
        print(f"   • Active: {active_accounts[0]['email']}")
        print("   • Redundancy: ⚠️ Limited")
    else:
        print("❌ No Gmail accounts are working")
        print("   • Check app passwords and permissions")
    
    return len(active_accounts)

def send_test_emails():
    """Send test emails from both accounts"""
    print("\n" + "=" * 60)
    print("SENDING TEST EMAILS")
    print("=" * 60)
    
    test_subject = f"Dual Gmail SMTP Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    test_body = """This is a test email from the new DUAL Gmail SMTP configuration.

System now has:
1. Primary account: zan@impactquadrant.info
2. Backup account: sam@impactquadrant.info

Benefits:
• Redundancy - if one account fails, other continues
• Higher sending capacity - can alternate between accounts
• Better deliverability - Google infrastructure
• No more AgentMail dependency

Email outreach that was blocked for 5 days is now UNBLOCKED!

Campaigns resuming:
• Dorada Resort (34 emails)
• Miami Hotels (9 emails)
• Lead Outreach (daily)
• Defense Sector (15 leads)
• Expense Reduction (daily)
"""
    
    results = []
    
    # Test with primary account
    print("\n1. Testing primary account (zan@impactquadrant.info)...")
    success1, message1, account1 = send_email_dual_gmail(
        to_emails="zan@impactquadrant.info",
        subject=f"[PRIMARY] {test_subject}",
        body_text=test_body,
        preferred_account="zan"
    )
    
    if success1:
        print(f"   ✅ {message1}")
        results.append(("Primary", True))
    else:
        print(f"   ❌ {message1}")
        results.append(("Primary", False))
    
    # Test with backup account
    print("\n2. Testing backup account (sam@impactquadrant.info)...")
    success2, message2, account2 = send_email_dual_gmail(
        to_emails="sam@impactquadrant.info",
        subject=f"[BACKUP] {test_subject}",
        body_text=test_body,
        preferred_account="sam"
    )
    
    if success2:
        print(f"   ✅ {message2}")
        results.append(("Backup", True))
    else:
        print(f"   ❌ {message2}")
        results.append(("Backup", False))
    
    return results

def main():
    """Main execution"""
    
    print("=" * 80)
    print("🚀 DUAL GMAIL SMTP CONFIGURATION")
    print("=" * 80)
    print("Email outreach blocked for 5 days - Implementing redundant solution")
    print()
    
    # Test both accounts
    active_count = test_both_accounts()
    
    if active_count == 0:
        print("\n❌ No working Gmail accounts found")
        print("Please check app passwords and try again")
        return
    
    # Send test emails
    results = send_test_emails()
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 DUAL GMAIL IMPLEMENTATION SUMMARY")
    print("=" * 80)
    
    successful_tests = sum(1 for _, success in results if success)
    
    if successful_tests == 2:
        print("🎉 DUAL GMAIL SMTP IMPLEMENTED SUCCESSFULLY!")
        print("✅ Both accounts tested and working")
        print("✅ Redundant email system ready")
        print("✅ Higher sending capacity available")
    elif successful_tests == 1:
        print("⚠️  SINGLE GMAIL ACCOUNT WORKING")
        print("✅ Email outreach can resume")
        print("⚠️  No redundancy available")
    else:
        print("❌ GMAIL CONFIGURATION FAILED")
        print("Need to fix app password configuration")
        return
    
    print("\n📧 Campaign Impact:")
    print("   • Dorada Resort: 34 emails - ✅ Ready")
    print("   • Miami Hotels: 9 emails - ✅ Ready")
    print("   • Lead Outreach: Daily - ✅ Ready")
    print("   • Defense Sector: 15 leads - ✅ Ready")
    print("   • Expense Reduction: Daily - ✅ Ready")
    
    print(f"\n⏰ Time blocked: 5 DAYS")
    print(f"🚀 Recovery: IMMEDIATE")
    
    print("\n🔧 Configuration:")
    print(f"   Primary: {GMAIL_ACCOUNTS[0]['email']}")
    print(f"   Backup: {GMAIL_ACCOUNTS[1]['email']}")
    print(f"   CC: {STANDARD_CC}")
    
    print("\n🎯 Next Steps:")
    print("1. Update all email scripts to use dual Gmail system")
    print("2. Monitor 2:00 PM cron jobs for email delivery")
    print("3. Implement load balancing between accounts")
    print("4. Track email deliverability and bounce rates")
    
    # Save configuration
    try:
        config_file = '/Users/cubiczan/.openclaw/workspace/dual-gmail-config.json'
        import json
        with open(config_file, 'w') as f:
            json.dump({
                'configured_at': datetime.now().isoformat(),
                'accounts': GMAIL_ACCOUNTS,
                'standard_cc': STANDARD_CC,
                'status': 'active',
                'redundancy': successful_tests == 2,
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
        print(f"\n⚠️  Could not save config: {str(e)}")

if __name__ == "__main__":
    main()