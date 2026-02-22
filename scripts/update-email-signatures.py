#!/usr/bin/env python3
"""
Update email signatures in campaign files to include "Agent Manager" 
and Sam Desigan contact information.
"""

import os
import re

def update_dorada_campaign():
    """Update Dorada Resort campaign file signatures"""
    file_path = "/Users/cubiczan/.openclaw/workspace/deals/dorada-outreach-campaign.md"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern to find "Best regards,\n\n[Your Name]" and replace with new signature
    old_pattern = r'(Best regards,)\s*\n\s*\n\s*(\[Your Name\])'
    new_signature = r"""Best regards,

\2
Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    
    # Replace all occurrences
    updated_content = re.sub(old_pattern, new_signature, content, flags=re.MULTILINE)
    
    # Also handle variations
    variations = [
        (r'Best regards,\s*\n\s*\[Your Name\]', new_signature),
        (r'Best regards,\s*\n\s*\n\s*\[Your Name\]', new_signature),
    ]
    
    for old, new in variations:
        updated_content = re.sub(old, new, updated_content, flags=re.MULTILINE)
    
    # Write back
    with open(file_path, 'w') as f:
        f.write(updated_content)
    
    print(f"✅ Updated Dorada campaign file: {file_path}")
    return updated_content != content

def update_miami_campaign():
    """Update Miami Hotels campaign file signatures"""
    file_path = "/Users/cubiczan/.openclaw/workspace/deals/miami-hotels-outreach-campaign.md"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern to find "Best regards,\n\n[Your Name]" and replace with new signature
    old_pattern = r'(Best regards,)\s*\n\s*\n\s*(\[Your Name\])'
    new_signature = r"""Best regards,

\2
Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    
    # Replace all occurrences
    updated_content = re.sub(old_pattern, new_signature, content, flags=re.MULTILINE)
    
    # Also handle variations
    variations = [
        (r'Best regards,\s*\n\s*\[Your Name\]', new_signature),
        (r'Best regards,\s*\n\s*\n\s*\[Your Name\]', new_signature),
    ]
    
    for old, new in variations:
        updated_content = re.sub(old, new, updated_content, flags=re.MULTILINE)
    
    # Write back
    with open(file_path, 'w') as f:
        f.write(updated_content)
    
    print(f"✅ Updated Miami Hotels campaign file: {file_path}")
    return updated_content != content

def update_lead_generator_skill():
    """Update lead generator skill file signatures"""
    file_path = "/Users/cubiczan/mac-bot/skills/lead-generator/SKILL.md"
    
    if not os.path.exists(file_path):
        print(f"⚠️ Lead generator skill file not found: {file_path}")
        return False
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Look for email templates in the skill file
    # This is more complex as the structure varies
    # We'll look for common patterns in email templates
    
    # Pattern 1: Standard email template with Best regards
    pattern1 = r'(Best regards,)\s*\n\s*\n\s*([A-Z][a-z]+(?: [A-Z][a-z]+)*)'
    replacement1 = r"""Best regards,

\2
Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    
    updated_content = re.sub(pattern1, replacement1, content, flags=re.MULTILINE)
    
    # Pattern 2: With [Your Name] placeholder
    pattern2 = r'(Best regards,)\s*\n\s*\n\s*(\[Your Name\])'
    replacement2 = r"""Best regards,

\2
Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    
    updated_content = re.sub(pattern2, replacement2, updated_content, flags=re.MULTILINE)
    
    if updated_content != content:
        with open(file_path, 'w') as f:
            f.write(updated_content)
        print(f"✅ Updated lead generator skill file: {file_path}")
        return True
    else:
        print(f"⚠️ No changes needed in lead generator skill file")
        return False

def update_agentmail_scripts():
    """Update AgentMail integration scripts"""
    scripts = [
        "/Users/cubiczan/.openclaw/workspace/scripts/agentmail-integration.py",
        "/Users/cubiczan/.openclaw/workspace/scripts/expense-reduction-agentmail.py",
        "/Users/cubiczan/.openclaw/workspace/scripts/send-remaining-leads.sh",
    ]
    
    updated_count = 0
    
    for script_path in scripts:
        if not os.path.exists(script_path):
            print(f"⚠️ Script not found: {script_path}")
            continue
        
        with open(script_path, 'r') as f:
            content = f.read()
        
        # Look for email body generation patterns
        # This will vary by script, so we'll do simple string replacements
        
        # Common patterns in email bodies
        patterns = [
            (r'Best regards,\s*\n\s*Zane', 'Best regards,\n\nZane\nAgent Manager\n\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.'),
            (r'Best regards,\s*\n\s*Zander', 'Best regards,\n\nZander\nAgent Manager\n\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.'),
            (r'Best regards,\s*\n\s*\[Your Name\]', 'Best regards,\n\n[Your Name]\nAgent Manager\n\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.'),
        ]
        
        updated_content = content
        for pattern, replacement in patterns:
            updated_content = re.sub(pattern, replacement, updated_content, flags=re.MULTILINE)
        
        if updated_content != content:
            with open(script_path, 'w') as f:
                f.write(updated_content)
            print(f"✅ Updated script: {script_path}")
            updated_count += 1
    
    return updated_count > 0

def main():
    """Main execution"""
    print("=" * 60)
    print("UPDATING EMAIL SIGNATURES FOR ALL OUTREACH")
    print("=" * 60)
    print()
    
    changes_made = False
    
    # Update campaign files
    if update_dorada_campaign():
        changes_made = True
    
    if update_miami_campaign():
        changes_made = True
    
    # Update skill file
    if update_lead_generator_skill():
        changes_made = True
    
    # Update scripts
    if update_agentmail_scripts():
        changes_made = True
    
    print()
    print("=" * 60)
    if changes_made:
        print("✅ SIGNATURE UPDATES COMPLETE")
        print()
        print("All email templates now include:")
        print("- Signature: 'Agent Manager'")
        print("- Note: 'Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up'")
    else:
        print("⚠️ No changes were made (signatures may already be updated)")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
