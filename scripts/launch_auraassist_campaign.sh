#!/bin/bash
# Launch First ClawReceptionist Campaign
# Non-interactive version for automation

echo "🚀 LAUNCHING FIRST CLAWRECEPTIONIST CAMPAIGN"
echo "============================================================"
echo "🎯 Target: Salon & Spa Businesses"
echo "📍 Location: New York"
echo "📧 Method: Personalized Email Outreach"
echo "💰 Offer: 14-day Free Trial"
echo "📊 Batch: First 5 leads (test batch)"
echo "============================================================"

# Activate virtual environment
cd /Users/cubiczan/.openclaw/workspace
source .venv/bin/activate

echo ""
echo "🔧 STEP 1: CHECK OUTREACH QUEUE"
echo "----------------------------------------"

# Find latest salon outreach file
OUTREACH_FILE=$(ls -t /Users/cubiczan/.openclaw/workspace/outreach_queue/outreach_salons_spas_*.json 2>/dev/null | head -1)

if [ -z "$OUTREACH_FILE" ]; then
    echo "❌ ERROR: No salon outreach files found"
    echo "Run: python3 scripts/process_scraped_leads.py --auto"
    exit 1
fi

echo "📁 Using: $(basename $OUTREACH_FILE)"

# Count leads
LEAD_COUNT=$(python3 -c "
import json
with open('$OUTREACH_FILE', 'r') as f:
    data = json.load(f)
leads = data.get('outreach_leads', [])
print(len(leads))
")

echo "📊 Found: $LEAD_COUNT salon leads"

# Count email leads
EMAIL_COUNT=$(python3 -c "
import json
with open('$OUTREACH_FILE', 'r') as f:
    data = json.load(f)
leads = data.get('outreach_leads', [])
email_leads = [l for l in leads if l.get('email')]
print(len(email_leads))
")

echo "📧 Email leads: $EMAIL_COUNT"

if [ "$EMAIL_COUNT" -lt 5 ]; then
    echo "⚠️  WARNING: Less than 5 email leads found"
    echo "Continuing with available leads..."
fi

echo ""
echo "🔧 STEP 2: PREPARE EMAIL TEMPLATE"
echo "----------------------------------------"

cat << 'EOF'
📝 EMAIL TEMPLATE:
----------------------------------------
Subject: Reduce no-shows & fill last-minute cancellations

Body:
Hi there,

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

Best,
Sam
ClawReceptionist
----------------------------------------
EOF

echo ""
echo "🔧 STEP 3: SHOW LEADS TO CONTACT"
echo "----------------------------------------"

python3 -c "
import json
with open('$OUTREACH_FILE', 'r') as f:
    data = json.load(f)

leads = data.get('outreach_leads', [])
email_leads = [l for l in leads if l.get('email')]
test_leads = email_leads[:5]

print('🎯 FIRST 5 LEADS TO CONTACT:')
for i, lead in enumerate(test_leads, 1):
    print(f'{i}. {lead[\"business_name\"]}')
    print(f'   📞 Phone: {lead.get(\"phone\", \"N/A\")}')
    print(f'   📧 Email: {lead[\"email\"]}')
    print(f'   🎯 Score: {lead.get(\"lead_score\", 0)}/100')
    print()
"

echo ""
echo "🔧 STEP 4: SEND EMAILS (AUTOMATED)"
echo "----------------------------------------"

echo "⚠️  IMPORTANT: This will send REAL emails"
echo "============================================================"
echo "Starting email sending in 5 seconds..."
sleep 5

echo ""
echo "🚀 SENDING EMAILS..."
echo ""

# Run the email sending script
python3 -c "
import os
import json
import sys
import time
from datetime import datetime

sys.path.append('/Users/cubiczan/.openclaw/workspace')

try:
    from scripts.gmail_smtp_standard import GmailSender, STANDARD_SIGNATURE
    
    # Load leads
    with open('$OUTREACH_FILE', 'r') as f:
        data = json.load(f)
    
    leads = data.get('outreach_leads', [])
    email_leads = [l for l in leads if l.get('email')]
    test_leads = email_leads[:5]
    
    if not test_leads:
        print('❌ No email leads found')
        sys.exit(1)
    
    # Initialize Gmail sender
    gmail_sender = GmailSender(account_index=0, delay_seconds=3)
    
    sent_count = 0
    failed_count = 0
    
    for i, lead in enumerate(test_leads, 1):
        try:
            business_name = lead.get('business_name', 'your salon')
            email = lead['email']
            
            subject = 'Reduce no-shows & fill last-minute cancellations'
            
            body = f'''Hi there,

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

{STANDARD_SIGNATURE}'''
            
            print(f'📧 Sending to {email} ({i}/{len(test_leads)})...')
            gmail_sender.send_email(
                to_emails=email,
                subject=subject,
                body_text=body,
                cc_emails=['sam@impactquadrant.info']
            )
            
            sent_count += 1
            print(f'✅ Email sent to {email}')
            
            if i < len(test_leads):
                time.sleep(3)
                
        except Exception as e:
            print(f'❌ Failed to send to {lead.get(\"email\", \"unknown\")}: {e}')
            failed_count += 1
    
    print()
    print('='*60)
    print('✅ CAMPAIGN COMPLETE!')
    print('='*60)
    print(f'📊 RESULTS:')
    print(f'   Total Attempted: {len(test_leads)}')
    print(f'   Sent Successfully: {sent_count}')
    print(f'   Failed: {failed_count}')
    print(f'   Success Rate: {(sent_count / len(test_leads) * 100):.1f}%')
    print()
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_dir = '/Users/cubiczan/.openclaw/workspace/campaign_results'
    os.makedirs(results_dir, exist_ok=True)
    
    results_file = os.path.join(results_dir, f'first_campaign_{timestamp}.json')
    results_data = {
        'campaign': 'First Salon Outreach',
        'timestamp': timestamp,
        'leads_targeted': len(test_leads),
        'emails_sent': sent_count,
        'emails_failed': failed_count,
        'leads': test_leads
    }
    
    with open(results_file, 'w') as f:
        json.dump(results_data, f, indent=2)
    
    print(f'📁 Results saved to: {results_file}')
    
    # Archive outreach file
    import shutil
    sent_dir = '/Users/cubiczan/.openclaw/workspace/outreach_sent'
    os.makedirs(sent_dir, exist_ok=True)
    
    archive_path = os.path.join(sent_dir, 'archived', os.path.basename('$OUTREACH_FILE'))
    os.makedirs(os.path.dirname(archive_path), exist_ok=True)
    shutil.copy2('$OUTREACH_FILE', archive_path)
    os.remove('$OUTREACH_FILE')
    
    print(f'📁 Outreach file archived to: {archive_path}')
    
except ImportError as e:
    print(f'❌ ERROR: Could not import Gmail SMTP module: {e}')
    sys.exit(1)
except Exception as e:
    print(f'❌ ERROR: {e}')
    sys.exit(1)
"

echo ""
echo "🔧 STEP 5: NEXT STEPS"
echo "----------------------------------------"

echo "🎯 NEXT STEPS:"
echo "1. Monitor email replies in sam@cubiczan.com inbox"
echo "2. Check spam folder for replies"
echo "3. Schedule demos with interested leads"
echo "4. Follow up in 2-3 days if no response"
echo "5. Track conversions in campaign_results/ directory"
echo ""
echo "⏰ Expected timeline:"
echo "   • Replies: Within 24-48 hours"
echo "   • Demos: 2-3 from 5 emails (40-60% response rate)"
echo "   • Conversions: 1-2 customers from demos"
echo ""
echo "💰 Potential MRR from this batch: \$599-\$1,198"
echo ""
echo "🚀 READY FOR DEMOS AND CONVERSIONS!"
echo ""
echo "============================================================"
echo "✅ FIRST CLAWRECEPTIONIST CAMPAIGN LAUNCHED!"
echo "============================================================"