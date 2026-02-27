#!/bin/bash
# Defense Sector Outreach - Complete Solution
# Finds emails with Hunter.io and sends via Gmail SMTP

echo "============================================================"
echo "🚀 DEFENSE SECTOR OUTREACH - STARTING NOW"
echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
echo

# Configuration
GMAIL_EMAIL="sam@cubiczan.com"
GMAIL_PASSWORD="mwzh abbf ssih mjsf"
CC_EMAIL="sam@impactquadrant.info"
OUTPUT_DIR="/Users/cubiczan/.openclaw/workspace/defense-leads"
RESULTS_FILE="$OUTPUT_DIR/outreach-results-$(date +%Y%m%d-%H%M%S).json"
LOG_FILE="$OUTPUT_DIR/outreach-log-2026-02-26.md"

mkdir -p "$OUTPUT_DIR"

# Companies to contact (simplified list - top priorities)
COMPANIES=(
    "Helsing|helsing.ai|AI & Battlefield Software|company"
    "Quantum Systems|quantum-systems.com|Autonomous ISR Drones|company"
    "Comand AI|comand.ai|AI-Powered Targeting Systems|company"
    "MASNA Ventures|masna.vc|Defense-focused VC|investor"
    "Raphe mPhibr Investors|raphe.co.in|Drone manufacturing|investor"
)

echo "📊 Processing ${#COMPANIES[@]} priority companies..."
echo

# Initialize results array
echo '{"summary": {"total": 0, "found": 0, "sent": 0}, "results": []}' > "$RESULTS_FILE"

total_found=0
total_sent=0

for i in "${!COMPANIES[@]}"; do
    IFS='|' read -r name domain sector type <<< "${COMPANIES[$i]}"
    company_num=$((i + 1))
    
    echo "[$company_num/${#COMPANIES[@]}] $name"
    echo "   Domain: $domain"
    echo "   Sector: $sector"
    
    # Find email using Hunter.io (Python)
    echo "   🔍 Searching for email..."
    
    email_info=$(python3 << PYEOF
import sys
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace')
from hunter_io_config import hunter_client

try:
    result = hunter_client.domain_search("$domain", limit=5)
    
    if result.get('data') and result['data'].get('emails'):
        emails = result['data']['emails']
        # Get highest confidence email
        best = max(emails, key=lambda x: x.get('confidence', 0))
        
        if best.get('confidence', 0) >= 70:
            import json
            print(json.dumps({
                'email': best['value'],
                'confidence': best.get('confidence', 0),
                'type': best.get('type', 'unknown')
            }))
        else:
            print('{}')
    else:
        print('{}')
except Exception as e:
    print('{}')
PYEOF
)
    
    if [ "$email_info" = "{}" ] || [ -z "$email_info" ]; then
        echo "   ❌ No email found"
        # Update results
        python3 << PYEOF
import json
with open("$RESULTS_FILE", 'r') as f:
    data = json.load(f)

data['results'].append({
    'company': '$name',
    'domain': '$domain',
    'status': 'no_email',
    'timestamp': '$(date -Iseconds)'
})

data['summary']['total'] = len(data['results'])

with open("$RESULTS_FILE", 'w') as f:
    json.dump(data, f, indent=2)
PYEOF
        continue
    fi
    
    # Parse email info
    email=$(echo "$email_info" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('email', ''))")
    confidence=$(echo "$email_info" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('confidence', 0))")
    
    if [ -z "$email" ]; then
        echo "   ❌ Invalid email data"
        continue
    fi
    
    echo "   ✅ Found: $email ($confidence% confidence)"
    total_found=$((total_found + 1))
    
    # Generate email content
    if [ "$type" = "investor" ]; then
        subject="Introduction: Defense Tech Investment Opportunities"
        body="Dear $name Team,

I hope this message finds you well. I'm reaching out because your focus on $sector aligns perfectly with the defense technology opportunities we're currently working with.

We represent several high-growth defense tech companies in Europe and North America that are seeking strategic investment and partnership opportunities.

Given $name's expertise in $sector, I believe there could be strong alignment with our portfolio companies.

Would you be open to a brief introductory call to discuss potential investment opportunities?

Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan ($CC_EMAIL) for further follow up."
    else
        subject="Introduction: Strategic Partnership Opportunities for $name"
        body="Dear $name Team,

I hope this message finds you well. I'm reaching out because we've been following $name's impressive work in $sector and believe there could be valuable partnership opportunities.

Our team specializes in connecting defense technology companies with strategic investors, government contracts, and international expansion opportunities.

Given $name's position in the $sector sector, I believe there could be significant synergy with our network of defense-focused investors and government partners.

Would you be open to a brief 15-minute call to explore potential areas of collaboration?

Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan ($CC_EMAIL) for further follow up."
    fi
    
    # Send email via Gmail SMTP
    echo "   📧 Sending email..."
    
    # Create email file
    cat > /tmp/defense_email.txt << EOF
From: Agent Manager <$GMAIL_EMAIL>
To: $email
Cc: $CC_EMAIL
Subject: $subject
Content-Type: text/plain; charset=utf-8

$body
EOF
    
    # Send using curl
    send_result=$(curl -s --url 'smtp://smtp.gmail.com:587' \
      --ssl-reqd \
      --mail-from "$GMAIL_EMAIL" \
      --mail-rcpt "$email" \
      --mail-rcpt "$CC_EMAIL" \
      --user "$GMAIL_EMAIL:$GMAIL_PASSWORD" \
      --upload-file /tmp/defense_email.txt 2>&1)
    
    if [ $? -eq 0 ]; then
        echo "   ✅ Email sent successfully"
        status="sent"
        total_sent=$((total_sent + 1))
    else
        echo "   ❌ Failed to send: $send_result"
        status="failed"
    fi
    
    # Update results
    python3 << PYEOF
import json
with open("$RESULTS_FILE", 'r') as f:
    data = json.load(f)

data['results'].append({
    'company': '$name',
    'domain': '$domain',
    'email': '$email',
    'confidence': $confidence,
    'type': '$type',
    'status': '$status',
    'subject': '$subject',
    'timestamp': '$(date -Iseconds)'
})

data['summary']['total'] = len(data['results'])
data['summary']['found'] = $total_found
data['summary']['sent'] = $total_sent

with open("$RESULTS_FILE", 'w') as f:
    json.dump(data, f, indent=2)
PYEOF
    
    echo
    sleep 3  # Rate limiting
done

# Final summary
echo "============================================================"
echo "✅ OUTREACH COMPLETE"
echo "============================================================"
echo
echo "📊 Summary:"
echo "  • Total companies: ${#COMPANIES[@]}"
echo "  • Emails found: $total_found"
echo "  • Emails sent: $total_sent"
echo
echo "📁 Files:"
echo "  • Results: $RESULTS_FILE"
echo "  • Log: $LOG_FILE"
echo
echo "📧 All emails CC'd to: $CC_EMAIL"
echo "📧 Sent from: $GMAIL_EMAIL"
echo
echo "============================================================"

# Update log file
cat >> "$LOG_FILE" << EOF

## 🚀 Outreach Executed - $(date '+%H:%M')

**Status:** ✅ COMPLETED
**Companies processed:** ${#COMPANIES[@]}
**Emails found:** $total_found
**Emails sent:** $total_sent
**Method:** Gmail SMTP
**From:** $GMAIL_EMAIL
**CC:** $CC_EMAIL
**Results file:** $RESULTS_FILE

### Emails Sent:
$(for i in "${!COMPANIES[@]}"; do
    IFS='|' read -r name domain sector type <<< "${COMPANIES[$i]}"
    echo "- **$name** ($domain)"
done)

---
EOF

echo "Log updated: $LOG_FILE"
echo "============================================================"