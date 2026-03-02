#!/usr/bin/env python3
"""
Send First ClawReceptionist Campaign
Send personalized emails to salon leads from outreach queue
"""

import os
import json
import sys
import time
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("🚀 SENDING FIRST CLAWRECEPTIONIST CAMPAIGN")
print("="*60)
print("🎯 Target: Salon & Spa Businesses")
print("📍 Location: New York")
print("📧 Method: Personalized Email Outreach")
print("💰 Offer: 14-day Free Trial of ClawReceptionist")
print("="*60)

# Step 1: Check outreach queue
outreach_dir = "/Users/cubiczan/.openclaw/workspace/outreach_queue"
if not os.path.exists(outreach_dir):
    print("❌ ERROR: outreach_queue directory not found")
    sys.exit(1)

# Find latest salon outreach file
json_files = []
for file in os.listdir(outreach_dir):
    if file.endswith(".json") and file.startswith("outreach_") and "salons_spas" in file:
        json_files.append(file)

if not json_files:
    print("❌ ERROR: No salon outreach files found")
    sys.exit(1)

# Get latest file
latest_file = sorted(json_files)[-1]
filepath = os.path.join(outreach_dir, latest_file)
print(f"📁 Using outreach file: {latest_file}")

# Load leads
with open(filepath, 'r') as f:
    data = json.load(f)

leads = data.get("outreach_leads", [])
metadata = data.get("metadata", {})

if not leads:
    print("❌ ERROR: No leads found in file")
    sys.exit(1)

print(f"📊 Found {len(leads)} salon leads")
print()

# Step 2: Filter for email leads
email_leads = [lead for lead in leads if lead.get("email")]
print(f"📧 {len(email_leads)} leads have email addresses")

if not email_leads:
    print("❌ ERROR: No leads with email addresses")
    sys.exit(1)

# Step 3: Prepare to send (first 5 for testing)
test_leads = email_leads[:5]
print(f"🎯 Sending to first {len(test_leads)} leads for testing")
print()

# Step 4: Show what will be sent
print("📝 EMAIL TEMPLATE:")
print("-"*40)
print("Subject: Reduce no-shows & fill last-minute cancellations")
print()
print("Body:")
print("Hi there,")
print()
print("I noticed {business_name} provides salon/spa services.")
print()
print("Do you struggle with no-shows or last-minute cancellations?")
print()
print("Most salons lose 20-30% of revenue to:")
print("• No-shows and cancellations")
print("• Missed calls/texts after hours")
print("• Lost leads in Instagram DMs")
print("• Empty chairs from cancellations")
print()
print("Our AI receptionist for salons:")
print("• Sends smart reminders (72h, 24h, 2h)")
print("• Captures leads 24/7 from calls/texts/DMs")
print("• Fills cancellations automatically from waitlist")
print("• Books appointments with staff approval")
print()
print("It pays for itself by filling just 2-3 cancellation gaps per month.")
print()
print("Would you have 15 minutes next week to see how it works?")
print()
print("Best,")
print("Sam")
print("ClawReceptionist")
print("-"*40)
print()

# Step 5: Show leads that will receive emails
print("🎯 LEADS TO CONTACT:")
for i, lead in enumerate(test_leads, 1):
    print(f"{i}. {lead['business_name']}")
    print(f"   📞 Phone: {lead.get('phone', 'N/A')}")
    print(f"   📧 Email: {lead['email']}")
    print(f"   🎯 Score: {lead.get('lead_score', 0)}/100")
    print(f"   📍 Location: {lead.get('location', 'N/A')}")
    print()

# Step 6: Ask for confirmation
print("="*60)
print("⚠️  IMPORTANT: This will send REAL emails")
print("="*60)

confirmation = input("Send these emails? (yes/no): ").strip().lower()

if confirmation != "yes":
    print("❌ Campaign cancelled")
    sys.exit(0)

print()
print("🚀 SENDING EMAILS...")
print()

# Step 7: Send emails using existing Gmail SMTP
try:
    from scripts.gmail_smtp_standard import GmailSender, STANDARD_SIGNATURE
    
    # Initialize Gmail sender
    gmail_sender = GmailSender(account_index=0, delay_seconds=3)
    
    sent_count = 0
    failed_count = 0
    
    for i, lead in enumerate(test_leads, 1):
        try:
            # Prepare email
            business_name = lead.get("business_name", "your salon")
            email = lead["email"]
            
            # Create personalized message
            subject = "Reduce no-shows & fill last-minute cancellations"
            
            body = f"""Hi there,

I noticed {business_name} provides salon/spa services.

Do you struggle with no-shows or last-minute cancellations?

Most salons lose 20-30% of revenue to:
• No-shows and cancellations
• Missed calls/texts after hours
• Lost leads in Instagram DMs
• Empty chairs from cancellations

Our AI receptionist for salons:
• Sends smart reminders (72h, 24h, 2h)
• Captures leads 24/7 from calls/texts/DMs
• Fills cancellations automatically from waitlist
• Books appointments with staff approval

It pays for itself by filling just 2-3 cancellation gaps per month.

Would you have 15 minutes next week to see how it works?

{STANDARD_SIGNATURE}"""
            
            # Send email
            print(f"📧 Sending to {email} ({i}/{len(test_leads)})...")
            gmail_sender.send_email(
                to_email=email,
                subject=subject,
                body=body,
                sender_name="Agent Manager",
                cc_emails=["sam@impactquadrant.info"]
            )
            
            sent_count += 1
            print(f"✅ Email sent to {email}")
            
            # Add delay between emails
            if i < len(test_leads):
                time.sleep(3)
            
        except Exception as e:
            print(f"❌ Failed to send to {lead.get('email', 'unknown')}: {e}")
            failed_count += 1
    
    print()
    print("="*60)
    print("✅ CAMPAIGN COMPLETE!")
    print("="*60)
    print(f"📊 RESULTS:")
    print(f"   Total Attempted: {len(test_leads)}")
    print(f"   Sent Successfully: {sent_count}")
    print(f"   Failed: {failed_count}")
    print(f"   Success Rate: {(sent_count / len(test_leads) * 100):.1f}%")
    print()
    
    # Save campaign results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = "/Users/cubiczan/.openclaw/workspace/campaign_results"
    os.makedirs(results_dir, exist_ok=True)
    
    results_file = os.path.join(results_dir, f"first_campaign_{timestamp}.json")
    results_data = {
        "campaign": "First Salon Outreach",
        "timestamp": timestamp,
        "leads_targeted": len(test_leads),
        "emails_sent": sent_count,
        "emails_failed": failed_count,
        "leads": test_leads,
        "metadata": metadata
    }
    
    with open(results_file, 'w') as f:
        json.dump(results_data, f, indent=2)
    
    print(f"📁 Results saved to: {results_file}")
    print()
    
    # Move outreach file to sent directory
    sent_dir = "/Users/cubiczan/.openclaw/workspace/outreach_sent"
    os.makedirs(sent_dir, exist_ok=True)
    
    import shutil
    archive_path = os.path.join(sent_dir, "archived", latest_file)
    os.makedirs(os.path.dirname(archive_path), exist_ok=True)
    shutil.copy2(filepath, archive_path)
    os.remove(filepath)
    
    print(f"📁 Outreach file archived to: {archive_path}")
    print()
    
    # Next steps
    print("🎯 NEXT STEPS:")
    print("1. Monitor email replies in sam@cubiczan.com inbox")
    print("2. Check spam folder for replies")
    print("3. Schedule demos with interested leads")
    print("4. Follow up in 2-3 days if no response")
    print("5. Track conversions in campaign_results/ directory")
    print()
    print("⏰ Expected timeline:")
    print("   • Replies: Within 24-48 hours")
    print("   • Demos: 2-3 from 5 emails (40-60% response rate)")
    print("   • Conversions: 1-2 customers from demos")
    print()
    print("💰 Potential MRR from this batch: $599-$1,198")
    print()
    print("🚀 READY FOR DEMOS AND CONVERSIONS!")
    
except ImportError as e:
    print(f"❌ ERROR: Could not import Gmail SMTP module: {e}")
    print("Please ensure scripts/gmail_smtp_standard.py exists")
    sys.exit(1)
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)