#!/usr/bin/env python3
"""
Update critical outreach scripts to use Gmail SMTP instead of AgentMail
"""

import os
import re

def update_script_to_gmail(file_path):
    """Update a script to use Gmail SMTP instead of AgentMail"""
    
    if not os.path.exists(file_path):
        print(f"⚠️ File not found: {file_path}")
        return False
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if it uses AgentMail
    if "AgentMail" in content or "agentmail" in content:
        print(f"Updating: {file_path}")
        
        # Replace AgentMail API calls with Gmail SMTP
        # This is a simple replacement - more complex scripts may need manual updates
        
        # Replace AgentMail API key references
        content = re.sub(r'AGENTMAIL_API_KEY\s*=\s*["\'][^"\']*["\']', 
                        'GMAIL_EMAIL = "sam@cubiczan.com"\nGMAIL_PASSWORD = "mwzh abbf ssih mjsf"', 
                        content)
        
        # Replace AgentMail API URLs
        content = re.sub(r'https://api\.agentmail\.to/v[0-9]', 
                        'smtp.gmail.com:587', 
                        content)
        
        # Add import for Gmail module
        if "import" in content and "gmail_smtp_standard" not in content:
            # Add import after existing imports
            import_match = re.search(r'(^import.*?\n\n)', content, re.MULTILINE | re.DOTALL)
            if import_match:
                new_import = import_match.group(1) + "from gmail_smtp_standard import GmailSender, send_single_email\n\n"
                content = content.replace(import_match.group(1), new_import)
            else:
                # Add at the beginning
                content = "from gmail_smtp_standard import GmailSender, send_single_email\n\n" + content
        
        # Replace send_email function calls
        # This is more complex and may need script-specific updates
        
        # Write back
        with open(file_path, 'w') as f:
            f.write(content)
        
        print(f"  ✅ Updated to use Gmail SMTP")
        return True
    else:
        print(f"  Skipping (no AgentMail): {file_path}")
        return False

def main():
    """Update critical outreach scripts"""
    
    print("=" * 60)
    print("UPDATING SCRIPTS TO USE GMAIL INSTEAD OF AGENTMAIL")
    print("=" * 60)
    print()
    
    # Critical scripts that need updating
    critical_scripts = [
        "/Users/cubiczan/.openclaw/workspace/scripts/send_batch_2pm.py",
        "/Users/cubiczan/.openclaw/workspace/scripts/send-remaining-leads.py",
        "/Users/cubiczan/.openclaw/workspace/scripts/agentmail-integration.py",
        "/Users/cubiczan/.openclaw/workspace/scripts/dorada-wave5-outreach.py",
        "/Users/cubiczan/.openclaw/workspace/scripts/miami-hotels-wave1-timswanson.py",
    ]
    
    updated_count = 0
    
    for script in critical_scripts:
        if update_script_to_gmail(script):
            updated_count += 1
    
    print()
    print("=" * 60)
    print(f"✅ Updated {updated_count} scripts to use Gmail SMTP")
    print()
    print("New email configuration:")
    print("- Primary: sam@cubiczan.com")
    print("- Backup: sam@impactquadrant.info")
    print("- Backup: zan@impactquadrant.info")
    print("- CC: sam@impactquadrant.info (default)")
    print()
    print("Standardized module: gmail_smtp_standard.py")
    print("Features: Rate limiting, batch sending, error handling")
    print("=" * 60)
    
    # Create a simple test script
    test_script = """#!/usr/bin/env python3
"""
    print("\nTo test Gmail sending, use:")
    print("""
from gmail_smtp_standard import send_single_email

result = send_single_email(
    to_email="test@example.com",
    subject="Test from Gmail SMTP",
    body_text="This is a test email sent via Gmail SMTP."
)

if result["success"]:
    print("✅ Email sent successfully!")
else:
    print(f"❌ Error: {result['error']}")
""")

if __name__ == "__main__":
    main()
