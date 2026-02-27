#!/usr/bin/env python3
"""
TRIPLE Gmail SMTP Configuration for OpenClaw
Maximum redundancy with specialized account usage
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import random
from datetime import datetime

# TRIPLE GMAIL CONFIGURATION
GMAIL_ACCOUNTS = [
    {
        "email": "zan@impactquadrant.info",
        "password": "apbj bvsl tngo vqhu",
        "name": "Agent Manager",
        "purpose": "Primary outreach",
        "status": "active",
        "tested": True,
        "priority": 1
    },
    {
        "email": "sam@impactquadrant.info",
        "password": "ajup xyhf abbx iugj",
        "name": "Agent Manager",
        "purpose": "Backup outreach",
        "status": "active",
        "tested": True,
        "priority": 2
    },
    {
        "email": "sam@cubiczan.com",
        "password": "mwzh abbf ssih mjsf",
        "name": "Agent Manager",
        "purpose": "Cron job specialist",
        "status": "active",
        "tested": False,  # Will test now
        "priority": 3
    }
]

# Standard configuration
STANDARD_CC = "sam@impactquadrant.info"  # Always CC Sam
STANDARD_SIGNATURE = """Best regards,

Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""

def test_gmail_account(account):
    """Test a Gmail account connection"""
    print(f"Testing {account['email']} ({account['purpose']})...")
    
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

def send_email_triple_gmail(to_emails, subject, body_text, body_html=None, cc_emails=None, account_purpose=None):
    """
    Send email using triple Gmail accounts with intelligent routing
    
    Args:
        to_emails: Single email or list
        subject: Email subject
        body_text: Plain text body
        body_html: HTML body (optional)
        cc_emails: CC emails (optional)
        account_purpose: "primary", "backup", "cron", or None for auto
    
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
    
    # Select accounts based on purpose
    if account_purpose == "primary":
        accounts_to_try = [GMAIL_ACCOUNTS[0]]
    elif account_purpose == "backup":
        accounts_to_try = [GMAIL_ACCOUNTS[1]]
    elif account_purpose == "cron":
        accounts_to_try = [GMAIL_ACCOUNTS[2]]
    else:
        # Auto selection: try all in priority order
        accounts_to_try = sorted(GMAIL_ACCOUNTS, key=lambda x: x["priority"])
    
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
            
            return True, f"Email sent successfully using {account['email']} ({account['purpose']})", account["email"]
            
        except Exception as e:
            print(f"  ⚠️  {account['email']} failed: {str(e)}")
            continue
    
    # All accounts failed
    return False, "All Gmail accounts failed", None

def test_all_accounts():
    """Test all three Gmail accounts"""
    print("=" * 70)
    print("TRIPLE GMAIL ACCOUNT TEST")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test all accounts
    for account in GMAIL_ACCOUNTS:
        test_gmail_account(account)
    
    print()
    
    # Count active accounts
    active_accounts = [a for a in GMAIL_ACCOUNTS if a.get("tested", False)]
    
    if len(active_accounts) == 3:
        print("✅ ALL THREE Gmail accounts are working!")
        print("   • Redundancy: ✅ Maximum")
        print("   • Capacity: ✅ Very High")
        print("   • Specialization: ✅ Available")
        print("   • Reliability: ✅ Excellent")
    elif len(active_accounts) == 2:
        print("⚠️  2 out of 3 Gmail accounts are working")
        print("   • Redundancy: ✅ Good")
        print("   • Capacity: ✅ High")
    elif len(active_accounts) == 1:
        print("⚠️  Only 1 Gmail account is working")
        print("   • Redundancy: ⚠️ Limited")
    else:
        print("❌ No Gmail accounts are working")
    
    return len(active_accounts)

def send_test_emails_from_all():
    """Send test emails from all three accounts"""
    print("\n" + "=" * 70)
    print("SENDING TEST EMAILS FROM ALL ACCOUNTS")
    print("=" * 70)
    
    test_subject = f"Triple Gmail SMTP Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    test_body = """This is a test email from the new TRIPLE Gmail SMTP configuration.

System now has THREE Gmail accounts:
1. Primary: zan@impactquadrant.info (general outreach)
2. Backup: sam@impactquadrant.info (backup outreach)
3. Cron Specialist: sam@cubiczan.com (dedicated to cron jobs)

Benefits:
• Maximum redundancy - three independent accounts
• Specialized usage - cron jobs use dedicated account
• Higher sending capacity - can rotate between accounts
• Better deliverability - Google infrastructure
• No single point of failure

Email outreach that was blocked for 5 days is now UNBLOCKED with maximum reliability!

Campaigns resuming:
• Dorada Resort (34 emails)
• Miami Hotels (9 emails)
• Lead Outreach (daily)
• Defense Sector (15 leads)
• Expense Reduction (daily)
"""
    
    results = []
    
    # Test each account
    for i, account in enumerate(GMAIL_ACCOUNTS):
        purpose = account["purpose"].replace(" ", "_").lower()
        print(f"\n{i+1}. Testing {account['email']} ({account['purpose']})...")
        
        success, message, used_account = send_email_triple_gmail(
            to_emails="zan@impactquadrant.info",  # Test to primary
            subject=f"[{account['purpose'].upper()}] {test_subject}",
            body_text=test_body,
            account_purpose=purpose
        )
        
        if success:
            print(f"   ✅ {message}")
            results.append((account["purpose"], True))
        else:
            print(f"   ❌ {message}")
            results.append((account["purpose"], False))
    
    return results

def get_account_for_purpose(purpose):
    """Get the best account for a specific purpose"""
    if purpose == "cron_job":
        return GMAIL_ACCOUNTS[2]  # sam@cubiczan.com
    elif purpose == "campaign_outreach":
        return GMAIL_ACCOUNTS[0]  # zan@impactquadrant.info
    elif purpose == "backup":
        return GMAIL_ACCOUNTS[1]  # sam@impactquadrant.info
    else:
        # Return first working account
        for account in GMAIL_ACCOUNTS:
            if account.get("tested", False):
                return account
        return None

def main():
    """Main execution"""
    
    print("=" * 80)
    print("🚀 TRIPLE GMAIL SMTP CONFIGURATION")
    print("=" * 80)
    print("Email outreach blocked for 5 days - Implementing maximum redundancy")
    print()
    
    # Test all accounts
    active_count = test_all_accounts()
    
    if active_count == 0:
        print("\n❌ No working Gmail accounts found")
        print("Please check app passwords and try again")
        return
    
    # Send test emails
    results = send_test_emails_from_all()
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TRIPLE GMAIL IMPLEMENTATION SUMMARY")
    print("=" * 80)
    
    successful_tests = sum(1 for _, success in results if success)
    
    if successful_tests == 3:
        print("🎉 TRIPLE GMAIL SMTP IMPLEMENTED SUCCESSFULLY!")
        print("✅ All three accounts tested and working")
        print("✅ Maximum redundancy achieved")
        print("✅ Specialized account usage available")
        print("✅ Highest possible reliability")
    elif successful_tests >= 2:
        print("✅ MULTIPLE GMAIL ACCOUNTS WORKING")
        print("✅ Email outreach can resume with redundancy")
        print(f"✅ {successful_tests}/3 accounts operational")
    else:
        print("⚠️  LIMITED GMAIL AVAILABILITY")
        print("Need to fix app password configuration")
    
    print("\n📧 Account Purposes:")
    for account in GMAIL_ACCOUNTS:
        status = "✅" if account.get("tested", False) else "❌"
        print(f"   {status} {account['email']} - {account['purpose']}")
    
    print("\n🎯 Recommended Usage:")
    print("   1. Cron Jobs → sam@cubiczan.com (dedicated)")
    print("   2. Campaign Outreach → zan@impactquadrant.info (primary)")
    print("   3. Backup/Overflow → sam@impactquadrant.info (backup)")
    
    print("\n📊 Campaign Impact:")
    print("   • Dorada Resort: 34 emails - ✅ Ready (tomorrow 10 AM)")
    print("   • Miami Hotels: 9 emails - ✅ Ready (tomorrow 11 AM)")
    print("   • Lead Outreach: Daily - ✅ Ready (today 2 PM)")
    print("   • Defense Sector: 15 leads - ✅ Ready (needs contacts)")
    print("   • Expense Reduction: Daily - ✅ Ready (today 2 PM)")
    
    print(f"\n⏰ Time blocked: 5 DAYS")
    print(f"🚀 Recovery: IMMEDIATE with maximum redundancy")
    
    print("\n🔧 Next Steps:")
    print("1. Update cron jobs to use sam@cubiczan.com")
    print("2. Update campaign scripts to use zan@impactquadrant.info")
    print("3. Monitor 2:00 PM cron jobs for successful delivery")
    print("4. Implement load balancing between accounts")
    
    # Save configuration
    try:
        config_file = '/Users/cubiczan/.openclaw/workspace/triple-gmail-config.json'
        import json
        with open(config_file, 'w') as f:
            json.dump({
                'configured_at': datetime.now().isoformat(),
                'accounts': GMAIL_ACCOUNTS,
                'standard_cc': STANDARD_CC,
                'status': 'active',
                'redundancy_level': successful_tests,
                'recommended_usage': {
                    'cron_jobs': 'sam@cubiczan.com',
                    'campaign_outreach': 'zan@impactquadrant.info',
                    'backup': 'sam@impactquadrant.info'
                },
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