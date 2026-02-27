#!/usr/bin/env python3
"""
Send mining investor inquiry email to 500+ contacts
Asking what types of mines they're looking for
Using Gmail SMTP with sam@cubiczan.com
"""

import csv
import smtplib
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# Email configuration
SENDER_EMAIL = "sam@cubiczan.com"
SENDER_PASSWORD = "mwzh abbf ssih mjsf"  # Gmail app password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Files
CONTACTS_FILE = "/Users/cubiczan/.openclaw/workspace/mining-investors-enriched-20260227-000318.csv"
LOG_FILE = f"/Users/cubiczan/.openclaw/workspace/mining-inquiry-campaign-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
SUMMARY_FILE = f"/Users/cubiczan/.openclaw/workspace/mining-inquiry-summary-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"

def load_contacts():
    """Load investor contacts from CSV"""
    contacts = []
    
    try:
        with open(CONTACTS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
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
        
        print(f"✅ Loaded {len(contacts)} contacts with emails")
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
        msg['Subject'] = "Mining deal flow partnership – What are you looking for?"
        
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

def run_campaign():
    """Run the email campaign"""
    print("🚀 Starting Mining Investor Inquiry Campaign")
    print("="*60)
    print(f"Sender: {SENDER_EMAIL}")
    print(f"Contacts file: {CONTACTS_FILE}")
    print(f"Log file: {LOG_FILE}")
    print(f"Summary file: {SUMMARY_FILE}")
    print("="*60)
    
    # Load contacts
    contacts = load_contacts()
    if not contacts:
        print("❌ No contacts to process")
        return
    
    print(f"\n📧 Preparing to send emails to {len(contacts)} investors...")
    
    # Initialize counters
    total_sent = 0
    total_failed = 0
    sent_contacts = []
    failed_contacts = []
    
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
            sent_contacts.append(contact)
        else:
            total_failed += 1
            failed_contacts.append(contact)
        
        # Add delay to avoid rate limiting (2-4 seconds between emails)
        delay = random.uniform(2, 4)
        time.sleep(delay)
        
        # Progress update every 10 emails
        if i % 10 == 0:
            print(f"\n📊 Progress: {i}/{len(contacts)} | Sent: {total_sent} | Failed: {total_failed}")
    
    # Create summary report
    create_summary_report(contacts, total_sent, total_failed, sent_contacts, failed_contacts)
    
    print("\n" + "="*60)
    print("🎉 CAMPAIGN COMPLETE!")
    print("="*60)
    print(f"📊 Results:")
    print(f"   Total contacts: {len(contacts)}")
    print(f"   Emails sent: {total_sent} ({total_sent/len(contacts)*100:.1f}%)")
    print(f"   Failed: {total_failed} ({total_failed/len(contacts)*100:.1f}%)")
    print(f"\n📁 Files created:")
    print(f"   Log: {LOG_FILE}")
    print(f"   Summary: {SUMMARY_FILE}")
    print("\n🚀 Next: Monitor replies and follow up in 3-5 days")

def create_summary_report(all_contacts, sent_count, failed_count, sent_contacts, failed_contacts):
    """Create campaign summary report"""
    
    # Count by country
    country_stats = {}
    for contact in all_contacts:
        country = contact['country']
        country_stats[country] = country_stats.get(country, 0) + 1
    
    # Count sent by country
    sent_by_country = {}
    for contact in sent_contacts:
        country = contact['country']
        sent_by_country[country] = sent_by_country.get(country, 0) + 1
    
    with open(SUMMARY_FILE, 'w') as f:
        f.write(f"# Mining Investor Inquiry Campaign - Summary\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Sender:** {SENDER_EMAIL}\n")
        f.write(f"**Signature:** Sam Desigan, Sam@cubiczan.com\n")
        f.write(f"**Total Contacts:** {len(all_contacts)}\n")
        f.write(f"**Emails Sent:** {sent_count}\n")
        f.write(f"**Failed:** {failed_count}\n")
        f.write(f"**Success Rate:** {sent_count/len(all_contacts)*100:.1f}%\n\n")
        
        f.write("## 📊 Campaign Statistics\n\n")
        
        f.write("### By Country:\n")
        for country, count in sorted(country_stats.items(), key=lambda x: x[1], reverse=True):
            sent = sent_by_country.get(country, 0)
            success_rate = sent/count*100 if count > 0 else 0
            f.write(f"- **{country}:** {count} contacts ({sent} sent, {success_rate:.1f}% success)\n")
        
        f.write("\n### Email Template Used:\n")
        f.write("**Subject:** Mining deal flow partnership – What are you looking for?\n\n")
        f.write("**Key Points:**\n")
        f.write("- Partnership with mining deal-flow platform\n")
        f.write("- Early access to curated pipeline\n")
        f.write("- Request for investment criteria (metals, jurisdictions, stages)\n")
        f.write("- Reference to 8 sample projects from 2025\n")
        f.write("- Call to action: Reply with criteria or schedule call\n")
        
        f.write("\n### Sample Projects Referenced:\n")
        f.write("1. **Chile** - Large-scale copper development (Tier 1)\n")
        f.write("2. **Peru** - High-grade gold exploration\n")
        f.write("3. **Colombia** - Copper-gold porphyry system\n")
        f.write("4. **Mexico** - Gold heap-leach production\n")
        f.write("5. **USA** - Nevada gold portfolio\n")
        f.write("6. **Argentina** - Lithium brine exploration\n")
        f.write("7. **Ecuador** - Copper-molybdenum porphyry\n")
        f.write("8. **West Africa** - Near-surface placer coltan\n")
        
        f.write("\n## 📈 Expected Outcomes\n")
        f.write("Based on typical response rates for targeted B2B outreach:\n")
        f.write(f"- **Expected replies:** {int(sent_count * 0.15)}-{int(sent_count * 0.20)} (15-20%)\n")
        f.write(f"- **Expected meetings:** {int(sent_count * 0.05)}-{int(sent_count * 0.10)} (5-10%)\n")
        f.write(f"- **Qualified investors:** {int(sent_count * 0.03)}-{int(sent_count * 0.07)} (3-7%)\n")
        
        f.write("\n## 🚀 Next Steps\n")
        f.write("1. **Monitor replies** - Check inbox for responses\n")
        f.write("2. **Follow up** - Send reminder in 3-5 days if no response\n")
        f.write("3. **Segment responses** - Group by commodity/jurisdiction preference\n")
        f.write("4. **Schedule calls** - Set up introductory meetings\n")
        f.write("5. **Send deal flow** - Begin sending matched opportunities\n")
        
        f.write("\n## 📁 Files\n")
        f.write(f"- **Contacts:** {CONTACTS_FILE}\n")
        f.write(f"- **Log:** {LOG_FILE}\n")
        f.write(f"- **Summary:** {SUMMARY_FILE}\n")
        f.write(f"- **Sample Projects:** 61001f48-5b5b-4998-9387-039458a7b5e0.md\n")
        
        f.write("\n---\n")
        f.write(f"*Campaign completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    print(f"📄 Summary report created: {SUMMARY_FILE}")

def main():
    """Main execution"""
    print("="*60)
    print("MINING INVESTOR INQUIRY CAMPAIGN")
    print("="*60)
    print(f"📧 Sender: {SENDER_EMAIL}")
    print(f"📋 Signature: Sam Desigan, Sam@cubiczan.com")
    print(f"🎯 Goal: Ask 500+ investors what mines they're looking for")
    print(f"💡 Mention: Partnership with mining deal-flow platform")
    print(f"📄 Reference: 8 sample mining projects from 2025")
    print("="*60)
    
    # Confirm before sending
    confirm = input("\n⚠️  Ready to send emails to 500+ investors? (yes/no): ")
    
    if confirm.lower() == 'yes':
        run_campaign()
    else:
        print("❌ Campaign cancelled")
        print("\n💡 To run later, use: python3 send-mining-investor-inquiry.py")

if __name__ == "__main__":
    main()