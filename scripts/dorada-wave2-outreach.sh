#!/bin/bash
# Dorada Resort Wave 2 Outreach - Send to Andrew Alley
# Using curl to send email via AgentMail API

API_KEY="am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
INBOX="zane@agentmail.to"
CC_EMAIL="sam@impactquadrant.info"
TO_EMAIL="aalley@mitchellfo.com"
SUBJECT="Multi-generational wellness asset in Costa Rica's Blue Zone"

# Create JSON payload with email content
JSON_PAYLOAD=$(cat <<EOF
{
  "inbox_id": "$INBOX",
  "to": ["$TO_EMAIL"],
  "cc": ["$CC_EMAIL"],
  "subject": "$SUBJECT",
  "text": "Dear Mr. Alley,\n\nI'm reaching out regarding Dorada, a first-of-its-kind regenerative destination resort and residential community in one of the world's rare Blue Zone regions of Costa Rica.\n\nGiven Mitchell Family Office's focus on real estate and hospitality investments, I believe Dorada aligns with your investment philosophy—particularly as a multi-generational legacy asset that combines:\n\n• 300-acre protected bio-reserve with panoramic ocean views\n• 40 private estate homes (1+ acre lots)\n• Longevity & Human Performance Center offering personalized healthspan programs\n• Fully off-grid with sustainable infrastructure\n• Recurring revenue from wellness programs and memberships\n\nDorada is the vision of Dr. Vincent Giampapa, a globally recognized leader in anti-aging medicine and regenerative science. It's designed not as a hospitality project, but as a permanent wellness ecosystem for long-term ownership.\n\nWhy for family offices: Capital preservation with upside, intergenerational relevance, personal use optionality, and alignment with the \$2.1T wellness economy (12.4% CAGR).\n\nWould you be open to a brief call to discuss the opportunity? I'd be happy to share the full investor deck.\n\nBest regards,\n\nClaw\nOpenClaw AI Assistant\nsam@impactquadrant.info",
  "html": "<p>Dear Mr. Alley,</p>\n\n<p>I'm reaching out regarding <strong>Dorada</strong>, a first-of-its-kind regenerative destination resort and residential community in one of the world's rare Blue Zone regions of Costa Rica.</p>\n\n<p>Given Mitchell Family Office's focus on real estate and hospitality investments, I believe Dorada aligns with your investment philosophy—particularly as a multi-generational legacy asset that combines:</p>\n\n<ul>\n<li><strong>300-acre protected bio-reserve</strong> with panoramic ocean views</li>\n<li><strong>40 private estate homes</strong> (1+ acre lots)</li>\n<li><strong>Longevity & Human Performance Center</strong> offering personalized healthspan programs</li>\n<li>Fully off-grid with sustainable infrastructure</li>\n<li><strong>Recurring revenue</strong> from wellness programs and memberships</li>\n</ul>\n\n<p>Dorada is the vision of <strong>Dr. Vincent Giampapa</strong>, a globally recognized leader in anti-aging medicine and regenerative science. It's designed not as a hospitality project, but as a <strong>permanent wellness ecosystem</strong> for long-term ownership.</p>\n\n<p><strong>Why for family offices:</strong> Capital preservation with upside, intergenerational relevance, personal use optionality, and alignment with the \$2.1T wellness economy (12.4% CAGR).</p>\n\n<p>Would you be open to a brief call to discuss the opportunity? I'd be happy to share the full investor deck.</p>\n\n<p>Best regards,<br>\nClaw<br>\nOpenClaw AI Assistant<br>\nsam@impactquadrant.info</p>"
}
EOF
)

echo "========================================"
echo "Dorada Resort - Wave 2 Outreach"
echo "========================================"
echo ""
echo "Sending to: Andrew Alley (Mitchell Family Office)"
echo "Email: $TO_EMAIL"
echo "CC: $CC_EMAIL"
echo "Template: FAMILY OFFICE VERSION"
echo ""

# Send email via AgentMail API
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  "https://api.agentmail.to/v0/inboxes/$INBOX/messages" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD")

# Extract HTTP status code and response body
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    echo "✅ Email sent successfully!"
    echo "Response: $BODY"
    echo ""
    echo "Wave 2 - Contact 1/5 completed"
    echo "========================================"
    exit 0
else
    echo "❌ Error sending email"
    echo "HTTP Status: $HTTP_CODE"
    echo "Response: $BODY"
    echo "========================================"
    exit 1
fi
