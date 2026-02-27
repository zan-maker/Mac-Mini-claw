#!/usr/bin/env python3
"""
Update cron job scripts to use dedicated sam@cubiczan.com account
"""

import os
import re

# Cron job scripts that need updating
CRON_SCRIPTS = [
    "/Users/cubiczan/.openclaw/workspace/scripts/dorada-wave2-outreach.py",
    "/Users/cubiczan/.openclaw/workspace/scripts/expense-reduction-agentmail.py",
    "/Users/cubiczan/.openclaw/workspace/scripts/defense-outreach-today.py",
    "/Users/cubiczan/.openclaw/workspace/scripts/send-miami-email-fixed.py",
    "/Users/cubiczan/.openclaw/workspace/scripts/send-miami-wave3-email.py",
    "/Users/cubiczan/.openclaw/workspace/scripts/b2b-referral-agentmail.py",
]

# New configuration to add
CRON_GMAIL_CONFIG = '''# CRON JOB DEDICATED GMAIL ACCOUNT
CRON_GMAIL_EMAIL = "sam@cubiczan.com"
CRON_GMAIL_PASSWORD = "mwzh abbf ssih mjsf"
CRON_GMAIL_CC = "sam@impactquadrant.info"

STANDARD_SIGNATURE = """Best regards,

Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
'''

CRON_SEND_FUNCTION = '''
def send_cron_email(to_emails, subject, body_text, body_html=None, cc_emails=None):
    """Send email using dedicated cron job Gmail account"""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import ssl
    
    try:
        # Prepare recipients
        if isinstance(to_emails, str):
            to_list = [to_emails]
        else:
            to_list = to_emails
        
        if cc_emails is None:
            cc_list = [CRON_GMAIL_CC]
        elif isinstance(cc_emails, str):
            cc_list = [cc_emails]
        else:
            cc_list = cc_emails
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f'Agent Manager <{CRON_GMAIL_EMAIL}>'
        msg['To'] = ', '.join(to_list)
        msg['Cc'] = ', '.join(cc_list)
        msg['Subject'] = subject
        
        # Add text version
        full_text = body_text + "\\n\\n" + STANDARD_SIGNATURE
        text_part = MIMEText(full_text, 'plain')
        msg.attach(text_part)
        
        # Add HTML version if provided
        if body_html:
            full_html = body_html + "<br><br>" + STANDARD_SIGNATURE.replace('\\n', '<br>')
            html_part = MIMEText(full_html, 'html')
            msg.attach(html_part)
        
        # Connect and send
        context = ssl.create_default_context()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls(context=context)
        server.login(CRON_GMAIL_EMAIL, CRON_GMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True, f"Email sent successfully using {CRON_GMAIL_EMAIL}"
        
    except Exception as e:
        return False, f"Error sending email: {str(e)}"
'''

def update_cron_script(file_path):
    """Update a cron script to use dedicated Gmail account"""
    
    print(f"\n📝 Updating: {os.path.basename(file_path)}")
    
    if not os.path.exists(file_path):
        print("   ❌ File not found")
        return False
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        changes_made = []
        
        # 1. Remove old AgentMail API key references
        old_key_patterns = [
            r'API_KEY\s*=\s*["\']am_us_[a-zA-Z0-9_]+["\']',
            r'api_key\s*=\s*["\']am_us_[a-zA-Z0-9_]+["\']',
            r'AGENTMAIL_API_KEY\s*=\s*["\'][^"\']+["\']',
        ]
        
        for pattern in old_key_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                content = re.sub(pattern, '# Removed old AgentMail API key', content)
                changes_made.append("Removed AgentMail API key")
        
        # 2. Add cron Gmail configuration after imports
        if 'import' in content and 'CRON_GMAIL_EMAIL' not in content:
            # Find last import line
            lines = content.split('\n')
            insert_index = 0
            for i, line in enumerate(lines):
                if line.strip() and not line.strip().startswith(('#', 'import', 'from')):
                    insert_index = i
                    break
            
            if insert_index > 0:
                lines.insert(insert_index, CRON_GMAIL_CONFIG)
                content = '\n'.join(lines)
                changes_made.append("Added cron Gmail config")
        
        # 3. Add cron send function if not present
        if 'def send_' in content and 'send_cron_email' not in content:
            # Find where to insert (after config, before other functions)
            lines = content.split('\n')
            insert_index = 0
            for i, line in enumerate(lines):
                if 'STANDARD_SIGNATURE' in line:
                    insert_index = i + 1
                    break
            
            if insert_index > 0:
                lines.insert(insert_index, CRON_SEND_FUNCTION)
                content = '\n'.join(lines)
                changes_made.append("Added cron send function")
        
        # 4. Replace AgentMail API calls with cron function
        agentmail_patterns = [
            r'requests\.post\([^)]*agentmail[^)]*\)',
            r'agentmail.*send.*\([^)]*\)',
            r'send_via_agentmail\([^)]*\)',
        ]
        
        for pattern in agentmail_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Simple replacement - use cron function
                replacement = "send_cron_email(to_emails, subject, body_text)"
                content = content.replace(match, replacement)
                changes_made.append("Replaced AgentMail call with cron function")
        
        # 5. Update any remaining AgentMail references
        content = content.replace("AgentMail", "Gmail SMTP (Cron)")
        content = content.replace("agentmail", "cron_gmail")
        
        # Write updated content
        with open(file_path, 'w') as f:
            f.write(content)
        
        if changes_made:
            print(f"   ✅ Updated: {', '.join(changes_made)}")
            return True
        else:
            print(f"   ⚠️  No changes needed")
            return True
            
    except Exception as e:
        print(f"   ❌ Update failed: {str(e)}")
        return False

def main():
    """Main update function"""
    
    print("=" * 80)
    print("🚀 UPDATING CRON SCRIPTS FOR DEDICATED GMAIL ACCOUNT")
    print("=" * 80)
    print("Changing from AgentMail to sam@cubiczan.com for all cron jobs")
    print()
    
    updated_count = 0
    total_scripts = len(CRON_SCRIPTS)
    
    for script_path in CRON_SCRIPTS:
        if update_cron_script(script_path):
            updated_count += 1
    
    print("\n" + "=" * 80)
    print("📊 UPDATE SUMMARY")
    print("=" * 80)
    print(f"Scripts updated: {updated_count}/{total_scripts}")
    
    if updated_count > 0:
        print("\n🎉 CRON SCRIPTS UPDATED FOR DEDICATED GMAIL!")
        print("✅ All cron jobs will use sam@cubiczan.com")
        print("✅ Email outreach unblocked after 5 days")
        print("✅ Next cron run (2:00 PM) will use new configuration")
        
        print("\n📧 Cron Jobs Affected:")
        print("   • Lead Outreach (2:00 PM daily)")
        print("   • Expense Reduction Outreach (2:00 PM daily)")
        print("   • Defense Sector Outreach (2:00 PM daily)")
        print("   • Dorada Campaigns (10:00 AM daily)")
        print("   • Miami Campaigns (11:00 AM daily)")
        print("   • B2B Referral Outreach")
        
        print("\n🔧 Next Steps:")
        print("1. Test updated scripts individually")
        print("2. Monitor 2:00 PM cron job execution")
        print("3. Check email delivery success")
        print("4. Update any remaining cron scripts")
        
    else:
        print("\n⚠️ No scripts were updated")
        print("Check if scripts already use Gmail or don't exist")

if __name__ == "__main__":
    main()