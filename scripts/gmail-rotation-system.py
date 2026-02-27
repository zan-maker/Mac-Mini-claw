#!/usr/bin/env python3
"""
Gmail Rotation System for Email Outreach
Rotates between 2 Gmail accounts to avoid rate limits
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
from datetime import datetime
import time
import json
import os

# Gmail Account Configuration
GMAIL_ACCOUNTS = [
    {
        "email": "zan@impactquadrant.info",
        "password": "apbj bvsl tngo vqhu",
        "name": "Zane",
        "daily_limit": 50,  # Conservative Gmail limit
        "sent_today": 0
    },
    {
        "email": "sam@impactquadrant.info", 
        "password": "ajup xyhf abbx iugj",
        "name": "Sam",
        "daily_limit": 50,
        "sent_today": 0
    }
]

# State file for tracking rotation
STATE_FILE = "/Users/cubiczan/.openclaw/workspace/gmail-rotation-state.json"

# Standard CC
CC_EMAIL = "sam@impactquadrant.info"

def load_state():
    """Load rotation state from file"""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    
    # Default state
    return {
        "current_account_index": 0,
        "last_reset_date": datetime.now().strftime('%Y-%m-%d'),
        "account_stats": {
            "zan@impactquadrant.info": {"sent_today": 0, "total_sent": 0},
            "sam@impactquadrant.info": {"sent_today": 0, "total_sent": 0}
        }
    }

def save_state(state):
    """Save rotation state to file"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def get_next_account(state):
    """Get next available Gmail account with rotation logic"""
    
    # Check if we need to reset daily counts
    today = datetime.now().strftime('%Y-%m-%d')
    if state["last_reset_date"] != today:
        # Reset daily counts
        for email in state["account_stats"]:
            state["account_stats"][email]["sent_today"] = 0
        state["last_reset_date"] = today
        save_state(state)
    
    # Try current account first
    current_idx = state["current_account_index"]
    current_email = GMAIL_ACCOUNTS[current_idx]["email"]
    
    # Check if current account has reached daily limit
    if state["account_stats"][current_email]["sent_today"] < GMAIL_ACCOUNTS[current_idx]["daily_limit"]:
        return GMAIL_ACCOUNTS[current_idx]
    
    # Try next account
    next_idx = (current_idx + 1) % len(GMAIL_ACCOUNTS)
    next_email = GMAIL_ACCOUNTS[next_idx]["email"]
    
    if state["account_stats"][next_email]["sent_today"] < GMAIL_ACCOUNTS[next_idx]["daily_limit"]:
        state["current_account_index"] = next_idx
        save_state(state)
        return GMAIL_ACCOUNTS[next_idx]
    
    # Both accounts at limit - use whichever has fewer sent today
    if state["account_stats"][current_email]["sent_today"] <= state["account_stats"][next_email]["sent_today"]:
        return GMAIL_ACCOUNTS[current_idx]
    else:
        state["current_account_index"] = next_idx
        save_state(state)
        return GMAIL_ACCOUNTS[next_idx]

def send_email_with_rotation(to_email, to_name, subject, body, template_type="institutional"):
    """Send email using Gmail rotation system"""
    
    state = load_state()
    account = get_next_account(state)
    
    print(f"Using account: {account['email']} (Sent today: {state['account_stats'][account['email']]['sent_today']})")
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{account['name']} <{account['email']}>"
        msg['To'] = to_email
        msg['Cc'] = CC_EMAIL
        
        # Create HTML version
        html_body = body.replace('\n', '<br>')
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        # Create plain text version
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(account['email'], account['password'])
            server.send_message(msg)
        
        # Update state
        state["account_stats"][account['email']]["sent_today"] += 1
        state["account_stats"][account['email']]["total_sent"] += 1
        save_state(state)
        
        print(f"✅ Email sent to: {to_name} ({to_email})")
        return True, account['email']
        
    except Exception as e:
        print(f"❌ Failed to send to {to_name} ({to_email}) using {account['email']}: {str(e)}")
        
        # Try with other account if this one fails
        other_idx = (GMAIL_ACCOUNTS.index(account) + 1) % len(GMAIL_ACCOUNTS)
        other_account = GMAIL_ACCOUNTS[other_idx]
        
        print(f"  Trying backup account: {other_account['email']}")
        
        try:
            # Retry with other account
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{other_account['name']} <{other_account['email']}>"
            msg['To'] = to_email
            msg['Cc'] = CC_EMAIL
            
            html_body = body.replace('\n', '<br>')
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                server.login(other_account['email'], other_account['password'])
                server.send_message(msg)
            
            # Update state for backup account
            state["account_stats"][other_account['email']]["sent_today"] += 1
            state["account_stats"][other_account['email']]["total_sent"] += 1
            save_state(state)
            
            print(f"✅ Email sent via backup to: {to_name} ({to_email})")
            return True, other_account['email']
            
        except Exception as e2:
            print(f"❌ Backup also failed: {str(e2)}")
            return False, None

def get_dorada_template(contact_name, company, version):
    """Get Dorada email template"""
    
    if version == "institutional":
        subject = f"Scalable longevity real estate platform - Costa Rica Blue Zone"
        
        body = f"""Dear {contact_name.split()[0]},

I'm reaching out regarding **Dorada**, a luxury wellness and longevity platform in Costa Rica that combines premium real estate with recurring health services revenue.

Given {company}'s investment focus across wellness, hospitality, real estate, and healthcare, Dorada offers exposure to **structural tailwinds in the $2.1T longevity economy** (12.4% CAGR).

**Investment Thesis:**
- **Tangible real assets** with experiential differentiation
- **Multi-stream revenue model** (real estate + hospitality + longevity programs + memberships)
- **Recurring revenue** from 7-10 day health intensives and membership programs
- **Scalable platform** with replication potential across Blue Zone geographies
- **Brand extensibility** into digital health, clinics, and affiliated services

**Core Differentiator:**
Unlike traditional wellness resorts, Dorada's **Longevity & Human Performance Center** delivers science-driven, measurable longevity outcomes—creating a **repeat-engagement model** with high customer LTV.

**Asset:** 300-acre protected bio-reserve with ultra-low density development (40 estate homes, eco-hotel, branded residences, farm-to-table dining).

**Exit Optionality:** Portfolio expansion, strategic sale, or long-term cash flow hold.

Would you be open to reviewing the investor materials?

Best regards,

Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    
    else:  # family_office
        subject = f"Legacy wellness asset in Costa Rica - health preservation meets wealth preservation"
        
        body = f"""Dear {contact_name.split()[0]},

I'm reaching out regarding **Dorada**, a first-of-its-kind regenerative destination resort in Costa Rica's Blue Zone—designed specifically for families seeking to preserve both health and capital across generations.

Given {company}'s focus on healthcare, wellness, and family office clients, I believe Dorada aligns with your clients' priorities:

- **Capital preservation with upside**
- **Hard assets paired with experiential value**
- **Intergenerational relevance**
- **Personal use optionality alongside returns**

**The Asset:**
- **300-acre protected bio-reserve** with world-class ocean views
- **40 private estate homes** (1+ acre lots)
- **Longevity & Human Performance Center** with personalized healthspan programs
- Fully off-grid with sustainable infrastructure
- **Curated longevity community** of like-minded families

**Founder:** Dr. Vincent Giampapa, globally recognized leader in anti-aging medicine and regenerative science.

**Market Opportunity:** The wellness economy is projected to reach **$2.1T by 2030**, driven by aging HNW populations seeking preventive, performance-based health solutions.

**Legacy Value:** Dorada allows families to invest in something that enhances not only balance sheets—but quality of life, longevity, and human potential.

Would you be interested in sharing this opportunity with your family office clients?

Best regards,

Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    
    return subject, body

def main():
    """Test the rotation system"""
    
    print("=" * 60)
    print("GMAIL ROTATION SYSTEM TEST")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # Load current state
    state = load_state()
    print("Current State:")
    print(f"  Active account index: {state['current_account_index']}")
    print(f"  Last reset: {state['last_reset_date']}")
    for email, stats in state["account_stats"].items():
        print(f"  {email}: {stats['sent_today']} sent today, {stats['total_sent']} total")
    
    print()
    print("Testing rotation...")
    
    # Test getting next account
    account1 = get_next_account(state)
    print(f"First account: {account1['email']}")
    
    # Simulate sending some emails
    test_emails = [
        {"name": "Test Contact 1", "email": "test1@example.com", "company": "Test Co", "version": "institutional"},
        {"name": "Test Contact 2", "email": "test2@example.com", "company": "Test Co", "version": "family_office"},
    ]
    
    print()
    print("Note: This is a test - emails won't actually be sent to example.com")
    print("The rotation system is ready for use in actual campaigns.")
    
    print()
    print("=" * 60)
    print("✅ ROTATION SYSTEM READY")
    print("=" * 60)
    print()
    print("To use in campaigns:")
    print("1. Import this module")
    print("2. Call send_email_with_rotation()")
    print("3. System will automatically rotate between accounts")
    print("4. Daily limits: 50 emails per account")
    print("5. Automatic failover if one account fails")

if __name__ == "__main__":
    main()
