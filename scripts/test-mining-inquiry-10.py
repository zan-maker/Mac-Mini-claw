#!/usr/bin/env python3
"""
Test mining investor inquiry with 10 emails first
"""

import csv
import smtplib
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Email configuration
SENDER_EMAIL = "sam@cubiczan.com"
SENDER_PASSWORD = "mwzh abbf ssih mjsf"  # Gmail app password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Files
CONTACTS_FILE = "/Users/cubiczan/.openclaw/workspace/mining-investors-enriched-20260227-000318.csv"
timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
LOG_FILE = f"/Users/cubiczan/.openclaw/workspace/test-mining-inquiry-{timestamp}.log"

def load_first_10_contacts():
    """Load first 10 investor contacts from CSV"""
    contacts = []
    
    try:
        with open(CONTACTS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= 10:  # Only first 10
                    break
                    
                # Only include contacts with email
                if row.get('Email') and '@' in row['Email']:
                    contacts.append({
                        'id': row.get('ID'),
                        'name': row.get('Name'),
                        'title': row.get('Title'),
                        'firm': row.get('Firm'),
                        'country': row.get('Country'),
                        'focus': row.get('Focus'),
                        'email': row['Email'].strip(),
                        'deal_size': row.get('Deal Size'),
                        'stage_focus': row.get('Stage Focus')
                    })
        
        print(f"✅ Loaded {len(contacts)} contacts for test")
        return contacts
    except Exception as e:
        print(f"❌ Error loading contacts: {e}")
        return []

def create_email_body(first_name, country):
    """Create personalized email body"""
    
    # Extract first name
    if first_name:
        salutation = f"Hi {first_name},"
    else:
        salutation = "Hi there,"
    
    email_body = f"""{salutation}

I hope this message finds you well.

We are partnered with a leading mining deal-flow and asset intelligence platform that gives us structured access to a curated pipeline of pre-vetted junior exploration and development-stage opportunities globally.

The platform aggregates live listings, operator-submitted project data, and independently verified resource disclosures — giving us early visibility on assets before they reach mainstream investor attention.

**To better align our sourcing with your investment mandate, could you please let us know:**

1. **Primary metals/commodities** you are focused on (e.g., copper, gold, lithium, nickel, etc.)
2. **Preferred jurisdictions** (e.g., Tier 1 like Canada/US/Australia, or emerging markets like Latin America/West Africa)
3. **Project stage** preference (exploration, development, production)
4. **Deal size range** you typically participate in
5. Any specific **geological models or deposit types** of interest

**Sample of recent opportunities we have sourced (2025):**

- **Large-scale copper development in Chile** (Tier 1 jurisdiction) — Development stage, JORC-compliant large tonnage
- **High-grade gold exploration in Peru** — Advanced exploration, high-grade gold-silver epithermal system
- **Copper-gold porphyry system in Colombia** — Exploration stage, multi-target porphyry system confirmed
- **Gold heap-leach production asset in Mexico** — Production stage, meaningful production track record
- **Nevada gold portfolio (USA)** — Development/advanced exploration, Tier 1 jurisdiction
- **Lithium brine exploration in Argentina** — Exploration stage, Lithium Triangle with confirmed brine
- **Copper-molybdenum porphyry in Ecuador** — Advanced exploration, large porphyry system
- **Near-surface placer coltan in West Africa** — Advanced exploration, near-surface placer deposit

Once we understand your specific criteria, we can immediately start filtering the live pipeline and sending you anonymised project summaries that match your mandate.

Please reply directly to this email with your investment criteria, or feel free to schedule a brief call if you prefer to discuss.

Best regards,

Sam Desigan
Sam@cubiczan.com
"""
    
    return email_body

def send_email(to_email, to_name, email_body, email_id):
    """Send email via Gmail SMTP"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"Sam Desigan <{SENDER_EMAIL}>"
        msg['To'] = to_email
        msg['Subject'] = "TEST: Mining deal flow partnership – What are you looking for?"
  # Added TEST prefix
        
        # Add body
        msg.attach(MIMEText(email_body, 'plain'))
        
        # Connect to SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},SENT,{email_id},{to_name},{to_email}"
        print(f"   ✅ Email {email_id} sent to: {to_name} ({to_email})")
        
        return True, log_message
        
    except Exception as e:
        error_msg = str(e)
        log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},FAILED,{email_id},{to_name},{to_email},{error_msg[:100]}"
        print(f"   ❌ Failed to send email {email_id} to {to_name}: {error_msg[:100]}")
        
        return False, log_message

def run_test():
    """Run test with 10 emails"""
    print("🧪 TEST: Mining Investor Inquiry (10 emails)")
    print("="*60)
    print(f"Sender: {SENDER_EMAIL}")
    print(f"Signature: Sam Desigan, Sam@cubiczan.com")
    print(f"Subject: TEST: Mining deal flow partnership...")
    print("="*60)
    
    # Load contacts
    contacts = load_first_10_contacts()
    if not contacts:
        print("❌ No contacts to process")
        return
    
    print(f"\n📧 Preparing to send TEST emails to {len(contacts)} investors...")
    
    # Initialize counters
    total_sent = 0
    total_failed = 0
    
    # Create log file
    with open(LOG_FILE, 'w') as log:
        log.write("timestamp,status,contact_id,name,email,error\n")
    
    # Process each contact
    for i, contact in enumerate(contacts, 1):
        print(f"\n[{i}/{len(contacts)}] Processing: {contact['name']} ({contact['email']})")
        
        # Extract first name
        first_name = contact['name'].split()[0] if contact['name'] else ""
        
        # Create personalized email
        email_body = create_email_body(first_name, contact['country'])
        
        # Send email
        success, log_message = send_email(
            contact['email'],
            contact['name'],
            email_body,
            contact['id']
        )
        
        # Log result
        with open(LOG_FILE, 'a') as log:
            log.write(log_message + "\n")
        
        if success:
            total_sent += 1
        else:
            total_failed += 1
        
        # Add small delay
        time.sleep(2)
    
    print("\n" + "="*60)
    print("🧪 TEST COMPLETE!")
    print("="*60)
    print(f"📊 Results:")
    print(f"   Total test emails: {len(contacts)}")
    print(f"   Emails sent: {total_sent}")
    print(f"   Failed: {total_failed}")
    print(f"   Log file: {LOG_FILE}")
    
    if total_sent > 0:
        print("\n✅ TEST SUCCESSFUL! Ready to send full campaign.")
        print("💡 Remove 'TEST:' prefix from subject line for production.")
    else:
        print("\n❌ TEST FAILED! Check Gmail credentials and SMTP settings.")

def main():
    """Main execution"""
    print("="*60)
    print("MINING INVESTOR INQUIRY - TEST (10 emails)")
    print("="*60)
    print(f"📧 Sender: {SENDER_EMAIL}")
    print(f"📋 Signature: Sam Desigan, Sam@cubiczan.com")
    print(f"🎯 Test: 10 emails with 'TEST:' prefix in subject")
    print("="*60)
    
    # Auto-start test
    print("\n⚠️  Starting test in 3 seconds...")
    time.sleep(3)
    
    run_test()

if __name__ == "__main__":
    main()