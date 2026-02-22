#!/usr/bin/env python3
"""
Update email signatures in campaign files to include "Agent Manager" 
and Sam Desigan contact information.
"""

import os

def update_file_signatures(file_path, old_signature, new_signature):
    """Update signatures in a file"""
    if not os.path.exists(file_path):
        print(f"⚠️ File not found: {file_path}")
        return False
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    if old_signature in content:
        updated_content = content.replace(old_signature, new_signature)
        with open(file_path, 'w') as f:
            f.write(updated_content)
        print(f"✅ Updated: {file_path}")
        return True
    else:
        print(f"⚠️ Signature not found in: {file_path}")
        return False

def main():
    """Main execution"""
    print("=" * 60)
    print("UPDATING EMAIL SIGNATURES FOR ALL OUTREACH")
    print("=" * 60)
    print()
    
    # Define the old and new signatures
    old_signature_v1 = """Best regards,

[Your Name]"""

    old_signature_v2 = """Best regards,

Zane"""

    old_signature_v3 = """Best regards,

Zander"""
    
    new_signature = """Best regards,

[Your Name]
Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    
    new_signature_zane = """Best regards,

Zane
Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    
    new_signature_zander = """Best regards,

Zander
Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    
    # Files to update
    files_to_update = [
        # Campaign files
        ("/Users/cubiczan/.openclaw/workspace/deals/dorada-outreach-campaign.md", old_signature_v1, new_signature),
        ("/Users/cubiczan/.openclaw/workspace/deals/miami-hotels-outreach-campaign.md", old_signature_v1, new_signature),
        
        # Script files
        ("/Users/cubiczan/.openclaw/workspace/scripts/send-remaining-leads.sh", old_signature_v2, new_signature_zane),
    ]
    
    changes_made = False
    
    for file_path, old_sig, new_sig in files_to_update:
        if update_file_signatures(file_path, old_sig, new_sig):
            changes_made = True
    
    # Also check for variations
    print()
    print("Checking for other signature variations...")
    
    # Check Dorada file for other patterns
    dorada_file = "/Users/cubiczan/.openclaw/workspace/deals/dorada-outreach-campaign.md"
    if os.path.exists(dorada_file):
        with open(dorada_file, 'r') as f:
            content = f.read()
        
        # Check if there are still old signatures
        if "Best regards,\n\n[Your Name]" in content and "Agent Manager" not in content:
            print(f"⚠️ Old signatures still found in Dorada file")
            # Do a more aggressive replacement
            updated = content.replace("Best regards,\n\n[Your Name]", new_signature)
            with open(dorada_file, 'w') as f:
                f.write(updated)
            print(f"✅ Force-updated Dorada file")
            changes_made = True
    
    # Check Miami file
    miami_file = "/Users/cubiczan/.openclaw/workspace/deals/miami-hotels-outreach-campaign.md"
    if os.path.exists(miami_file):
        with open(miami_file, 'r') as f:
            content = f.read()
        
        if "Best regards,\n\n[Your Name]" in content and "Agent Manager" not in content:
            print(f"⚠️ Old signatures still found in Miami file")
            updated = content.replace("Best regards,\n\n[Your Name]", new_signature)
            with open(miami_file, 'w') as f:
                f.write(updated)
            print(f"✅ Force-updated Miami file")
            changes_made = True
    
    print()
    print("=" * 60)
    if changes_made:
        print("✅ SIGNATURE UPDATES COMPLETE")
        print()
        print("All email templates now include:")
        print("- Signature: 'Agent Manager'")
        print("- Note: 'Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up'")
        print()
        print("Affected files:")
        print("- Dorada Resort campaign")
        print("- Miami Hotels campaign")
        print("- Lead outreach scripts")
    else:
        print("⚠️ No changes were made (signatures may already be updated)")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
