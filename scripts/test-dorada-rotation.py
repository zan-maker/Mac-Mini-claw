#!/usr/bin/env python3
"""
Test updated Dorada script with rotation
"""

import sys
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scripts')

# Import the rotation function
from gmail_rotation_simple import send_email_with_rotation

print("Testing Dorada script with Gmail rotation...")
print()

# Test sending with rotation
success, message, account = send_email_with_rotation(
    to_emails="zan@impactquadrant.info",
    subject="Dorada Rotation Test - Campaign Ready",
    body_text="""This is a test of the Dorada campaign script with Gmail rotation.

The script now uses intelligent account rotation between:
1. zan@impactquadrant.info (Primary - 40%)
2. sam@impactquadrant.info (Backup - 30%)
3. sam@cubiczan.com (Cron Specialist - 30%)

Benefits:
• Avoids Gmail sending limits
• Improves deliverability
• Automatic failover
• Load balancing

Dorada campaign (34 emails) will use rotation when it runs tomorrow at 10:00 AM EST.

Campaign was blocked for 5 days, now UNBLOCKED with maximum reliability!""",
    force_account=None  # Let rotation decide
)

if success:
    print(f"\n🎉 DORADA ROTATION TEST SUCCESSFUL!")
    print(f"✅ Used account: {account}")
    print(f"✅ Message: {message}")
    print("\n📊 Campaign ready for tomorrow:")
    print("   • Time: 10:00 AM EST")
    print("   • Emails: 34 pending")
    print("   • System: Gmail rotation (3 accounts)")
    print("   • Status: UNBLOCKED after 5 days")
else:
    print(f"\n❌ Rotation test failed: {message}")

# Check rotation state
import json
state_file = "/Users/cubiczan/.openclaw/workspace/gmail-rotation-state.json"
if os.path.exists(state_file):
    with open(state_file, 'r') as f:
        state = json.load(f)
    
    print(f"\n📈 Rotation Statistics:")
    print(f"   Total sends: {state.get('total_sends', 0)}")
    print(f"   Last updated: {state.get('last_updated', 'Never')}")
    
    print("\n📊 Account Usage:")
    for email, data in state.get('accounts', {}).items():
        print(f"   • {email}: {data.get('sent_count', 0)} sends")