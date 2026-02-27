#!/usr/bin/env python3
"""
Gmail Account Rotation System (Simple Version)
Rotates between all three Gmail accounts without numpy dependency
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import random
from datetime import datetime
import json
import os

# ROTATION CONFIGURATION
GMAIL_ROTATION = [
    {
        "email": "zan@impactquadrant.info",
        "password": "apbj bvsl tngo vqhu",
        "name": "Agent Manager",
        "purpose": "Primary",
        "weight": 40,  # 40% of sends
        "sent_count": 0,
        "last_used": None,
        "active": True
    },
    {
        "email": "sam@impactquadrant.info",
        "password": "ajup xyhf abbx iugj",
        "name": "Agent Manager",
        "purpose": "Backup",
        "weight": 30,  # 30% of sends
        "sent_count": 0,
        "last_used": None,
        "active": True
    },
    {
        "email": "sam@cubiczan.com",
        "password": "mwzh abbf ssih mjsf",
        "name": "Agent Manager",
        "purpose": "Cron Specialist",
        "weight": 30,  # 30% of sends
        "sent_count": 0,
        "last_used": None,
        "active": True
    }
]

# Standard configuration
STANDARD_CC = "sam@impactquadrant.info"
STANDARD_SIGNATURE = """Best regards,

Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""

# Rotation state file
ROTATION_STATE_FILE = "/Users/cubiczan/.openclaw/workspace/gmail-rotation-state.json"

def load_rotation_state():
    """Load rotation state from file"""
    if os.path.exists(ROTATION_STATE_FILE):
        try:
            with open(ROTATION_STATE_FILE, 'r') as f:
                state = json.load(f)
            
            # Update accounts with saved state
            for account in GMAIL_ROTATION:
                email = account["email"]
                if email in state.get("accounts", {}):
                    account["sent_count"] = state["accounts"][email].get("sent_count", 0)
                    account["last_used"] = state["accounts"][email].get("last_used")
                    account["active"] = state["accounts"][email].get("active", True)
            
            print(f"📊 Loaded rotation state: {state.get('total_sends', 0)} total sends")
            return state
        except Exception as e:
            print(f"⚠️ Could not load rotation state: {str(e)}")
    
    return {"total_sends": 0, "accounts": {}}

def save_rotation_state():
    """Save rotation state to file"""
    try:
        state = {
            "last_updated": datetime.now().isoformat(),
            "total_sends": sum(a["sent_count"] for a in GMAIL_ROTATION),
            "accounts": {}
        }
        
        for account in GMAIL_ROTATION:
            state["accounts"][account["email"]] = {
                "sent_count": account["sent_count"],
                "last_used": account["last_used"],
                "purpose": account["purpose"],
                "weight": account["weight"],
                "active": account["active"]
            }
        
        with open(ROTATION_STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
        
        print(f"💾 Rotation state saved: {state['total_sends']} total sends")
        return True
    except Exception as e:
        print(f"⚠️ Could not save rotation state: {str(e)}")
        return False

def select_account_for_send():
    """
    Simple account selection without numpy
    Uses weighted random selection
    """
    
    # Create list of accounts with their weights
    accounts = []
    weights = []
    
    for account in GMAIL_ROTATION:
        if not account.get("active", True):
            continue  # Skip inactive accounts
        
        base_weight = account["weight"]
        
        # Adjust weight based on recent usage
        if account["last_used"]:
            try:
                last_used = datetime.fromisoformat(account["last_used"])
                hours_since = (datetime.now() - last_used).total_seconds() / 3600
                if hours_since < 1:
                    # Used recently, reduce weight
                    base_weight = max(5, base_weight * 0.5)
            except:
                pass
        
        # Favor accounts with fewer sends
        min_sends = min(a["sent_count"] for a in GMAIL_ROTATION if a.get("active", True))
        if account["sent_count"] > min_sends:
            base_weight = max(10, base_weight * 0.8)
        
        accounts.append(account)
        weights.append(base_weight)
    
    if not accounts:
        print("❌ No active accounts available")
        return None
    
    # Simple weighted random selection
    total_weight = sum(weights)
    if total_weight == 0:
        # All weights zero, use equal probability
        weights = [1] * len(accounts)
        total_weight = len(accounts)
    
    # Generate random number and select account
    rand = random.uniform(0, total_weight)
    cumulative = 0
    
    for i, weight in enumerate(weights):
        cumulative += weight
        if rand <= cumulative:
            selected_account = accounts[i]
            
            # Update account stats
            selected_account["sent_count"] += 1
            selected_account["last_used"] = datetime.now().isoformat()
            
            print(f"🔄 Selected: {selected_account['email']} ({selected_account['purpose']})")
            print(f"   Weight: {selected_account['weight']}%, Sent: {selected_account['sent_count']} times")
            
            return selected_account
    
    # Fallback to first account
    selected_account = accounts[0]
    selected_account["sent_count"] += 1
    selected_account["last_used"] = datetime.now().isoformat()
    return selected_account

def send_email_with_rotation(to_emails, subject, body_text, body_html=None, cc_emails=None, force_account=None):
    """
    Send email using Gmail account rotation
    
    Args:
        to_emails: Single email or list
        subject: Email subject
        body_text: Plain text body
        body_html: HTML body (optional)
        cc_emails: CC emails (optional)
        force_account: "zan", "sam", "cron", or None for rotation
    
    Returns:
        (success: bool, message: str, account_used: str)
    """
    
    # Load current state
    load_rotation_state()
    
    # Select account
    if force_account == "zan":
        account = GMAIL_ROTATION[0]
    elif force_account == "sam":
        account = GMAIL_ROTATION[1]
    elif force_account == "cron":
        account = GMAIL_ROTATION[2]
    else:
        account = select_account_for_send()
    
    if not account:
        return False, "No active Gmail accounts available", None
    
    print(f"📧 Sending via {account['email']} ({account['purpose']})")
    
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
        
        # Connect and send
        context = ssl.create_default_context()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls(context=context)
        server.login(account["email"], account["password"])
        server.send_message(msg)
        server.quit()
        
        # Save state
        save_rotation_state()
        
        message = f"✅ Email sent successfully using {account['email']} ({account['purpose']})"
        print(f"   {message}")
        return True, message, account["email"]
        
    except Exception as e:
        error_msg = f"❌ Email failed with {account['email']}: {str(e)}"
        print(f"   {error_msg}")
        
        # Mark account as potentially problematic
        account["active"] = False
        save_rotation_state()
        
        # Try another account if this one fails (unless forced)
        if not force_account:
            print("   🔄 Attempting failover to another account...")
            # Try with rotation again (will skip inactive account)
            return send_email_with_rotation(to_emails, subject, body_text, body_html, cc_emails, force_account=None)
        
        return False, error_msg, account["email"]

def test_rotation():
    """Simple rotation test"""
    print("=" * 60)
    print("🔄 GMAIL ROTATION TEST")
    print("=" * 60)
    
    # Clear state for clean test
    if os.path.exists(ROTATION_STATE_FILE):
        os.remove(ROTATION_STATE_FILE)
    
    # Send 3 test emails
    for i in range(3):
        print(f"\n📨 Test {i+1}/3:")
        
        success, message, account = send_email_with_rotation(
            to_emails="zan@impactquadrant.info",
            subject=f"Rotation Test {i+1}",
            body_text=f"Test email #{i+1} from rotation system.",
            force_account=None
        )
    
    print("\n📊 Test Complete!")
    print("Accounts should have been rotated automatically")

def main():
    """Main function"""
    print("Gmail Rotation System - Simple Version")
    print("Rotating between three Gmail accounts")
    print()
    
    test_rotation()
    
    print("\n" + "=" * 60)
    print("🎯 HOW TO USE IN CRON SCRIPTS:")
    print("=" * 60)
    
    usage_example = '''
# In your cron scripts, replace:
# Old: send_cron_email(to, subject, body)
# New: 
import sys
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scripts')
from gmail_rotation_simple import send_email_with_rotation

success, message, account = send_email_with_rotation(
    to_emails="recipient@example.com",
    subject="Your Subject",
    body_text="Your email body",
    force_account=None  # Let rotation decide
)
'''
    
    print(usage_example)
    
    print("\n🔧 Benefits of Rotation:")
    print("• Avoids Gmail sending limits")
    print("• Improves deliverability")
    print("• Automatic failover")
    print("• Load balancing")
    
    print(f"\n📁 State file: {ROTATION_STATE_FILE}")
    print("   Tracks usage and automatically adjusts")

if __name__ == "__main__":
    main()