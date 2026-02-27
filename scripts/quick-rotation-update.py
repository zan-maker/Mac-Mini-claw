#!/usr/bin/env python3
"""
Quick update to add rotation to cron scripts
"""

import os

# Cron scripts to update
scripts = [
    "/Users/cubiczan/.openclaw/workspace/scripts/dorada-wave2-outreach.py",
    "/Users/cubiczan/.openclaw/workspace/scripts/expense-reduction-agentmail.py",
    "/Users/cubiczan/.openclaw/workspace/scripts/defense-outreach-today.py",
]

rotation_import = '''
# Gmail Rotation System
import sys
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scripts')
from gmail_rotation_simple import send_email_with_rotation
'''

for script in scripts:
    if os.path.exists(script):
        print(f"\n📝 Updating {os.path.basename(script)}...")
        
        with open(script, 'r') as f:
            content = f.read()
        
        # Check if already has rotation
        if 'gmail_rotation_simple' in content:
            print(f"   ⚠️ Already has rotation, skipping")
            continue
        
        # Add import at the top (after other imports)
        lines = content.split('\n')
        insert_index = 0
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith(('#', 'import', 'from')):
                insert_index = i
                break
        
        if insert_index > 0:
            lines.insert(insert_index, rotation_import)
            content = '\n'.join(lines)
        
        # Replace function calls
        if 'send_cron_email(' in content:
            old_count = content.count('send_cron_email(')
            content = content.replace('send_cron_email(', 'send_email_with_rotation(')
            new_count = content.count('send_email_with_rotation(')
            print(f"   ✅ Replaced {old_count} function calls")
        
        # Write back
        with open(script, 'w') as f:
            f.write(content)

print("\n✅ Cron scripts updated for rotation!")
print("🎯 Next cron run will rotate between Gmail accounts automatically")
print("\n📊 Rotation will:")
print("   • Distribute sends across 3 accounts")
print("   • Avoid Gmail rate limits")
print("   • Improve deliverability")
print("   • Provide automatic failover")