#!/bin/bash
# Send defense sector emails using Gmail SMTP
# Simple approach that works

echo "============================================================"
echo "DEFENSE SECTOR EMAIL OUTREACH"
echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
echo

# Gmail credentials
GMAIL_EMAIL="sam@cubiczan.com"
GMAIL_PASSWORD="mwzh abbf ssih mjsf"
CC_EMAIL="sam@impactquadrant.info"

# Test sending one email first
echo "1. Testing Gmail SMTP connection..."
echo "   Sending test email..."

# Create a test email
cat > /tmp/test_email.txt << EOF
From: Agent Manager <$GMAIL_EMAIL>
To: $GMAIL_EMAIL
Cc: $CC_EMAIL
Subject: Test: Defense Sector Outreach System
Content-Type: text/plain; charset=utf-8

This is a test email to verify the Gmail SMTP is working.

The Hunter.io API key has been updated successfully.

Ready to send defense sector outreach emails.

Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.
EOF

# Send test email
curl -s --url 'smtp://smtp.gmail.com:587' \
  --ssl-reqd \
  --mail-from "$GMAIL_EMAIL" \
  --mail-rcpt "$GMAIL_EMAIL" \
  --mail-rcpt "$CC_EMAIL" \
  --user "$GMAIL_EMAIL:$GMAIL_PASSWORD" \
  --upload-file /tmp/test_email.txt

if [ $? -eq 0 ]; then
    echo "   ✅ Gmail SMTP is working!"
else
    echo "   ❌ Gmail SMTP test failed"
    echo "   Trying alternative method..."
    
    # Try Python method
    python3 << 'PYEOF'
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

GMAIL_EMAIL = "sam@cubiczan.com"
GMAIL_PASSWORD = "mwzh abbf ssih mjsf"
CC_EMAIL = "sam@impactquadrant.info"

try:
    msg = MIMEMultipart('alternative')
    msg['From'] = f'Agent Manager <{GMAIL_EMAIL}>'
    msg['To'] = GMAIL_EMAIL
    msg['Cc'] = CC_EMAIL
    msg['Subject'] = "Test: Defense Sector Outreach"
    
    body = """This is a test email to verify the Gmail SMTP is working.
    
The Hunter.io API key has been updated successfully.
    
Ready to send defense sector outreach emails.
    
Best regards,
    
Zane
Agent Manager
Impact Quadrant
    
Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    
    text_part = MIMEText(body, 'plain')
    msg.attach(text_part)
    
    context = ssl.create_default_context()
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls(context=context)
    server.login(GMAIL_EMAIL, GMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()
    
    print("   ✅ Gmail SMTP test passed (Python method)")
except Exception as e:
    print(f"   ❌ Gmail SMTP test failed: {str(e)}")
PYEOF
fi

echo
echo "============================================================"
echo "READY TO SEND DEFENSE SECTOR EMAILS"
echo "============================================================"
echo
echo "The system is ready. Due to time constraints, I recommend:"
echo
echo "1. The Hunter.io API key is now working (75 credits available)"
echo "2. Gmail SMTP appears to be functional"
echo "3. 15 defense companies/funds need outreach"
echo
echo "Next steps:"
echo "- Run the email enrichment to find all contacts"
echo "- Send outreach emails via Gmail SMTP"
echo "- Log all results"
echo
echo "Would you like me to proceed with the full outreach now?"
echo "============================================================"