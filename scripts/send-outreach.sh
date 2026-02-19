#!/bin/bash
# Lead Outreach - AgentMail Integration
# Date: 2026-02-18

API_KEY="am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
INBOX="Zane@agentmail.to"
CC="sam@impactquadrant.info"

echo "=========================================="
echo "Lead Outreach - 2026-02-18 2:00 PM"
echo "=========================================="

# Email 1: Staley Steel LLC
echo ""
echo "Sending to: Staley Steel LLC"
echo "To: info@staleysteel.com"
echo "Savings: \$103,875 (125 employees)"

curl -s -X POST "https://api.agentmail.to/v0/inboxes/${INBOX}/messages" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["info@staleysteel.com"],
    "subject": "$103,875 annual savings for Staley Steel LLC (zero cost to implement)",
    "text": "Hi,\n\nI noticed Staley Steel LLC has about 125 employees, which positions you for significant annual savings through a compliant Section 125 wellness program.\n\nOrganizations your size are typically saving:\n• $681 per employee annually in FICA savings\n• 30-60% reduction in workers comp premiums\n• Total savings: $103,875\n\nOne medical transportation company with 66 employees saved over $140,000 last year.\n\nThe program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.\n\nWould you be open to a 10-minute call this week to see the numbers for Staley Steel LLC?\n\nBest,\nZane\nZane@agentmail.to\nWellness 125 Cafeteria Plan",
    "html": "<p>Hi,</p><p>I noticed Staley Steel LLC has about 125 employees, which positions you for significant annual savings through a compliant Section 125 wellness program.</p><p><strong>Organizations your size are typically saving:</strong></p><ul><li>$681 per employee annually in FICA savings</li><li>30-60% reduction in workers comp premiums</li><li><strong>Total savings: $103,875</strong></li></ul><p>One medical transportation company with 66 employees saved over $140,000 last year.</p><p>The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.</p><p>Would you be open to a 10-minute call this week to see the numbers for Staley Steel LLC?</p><p>Best,<br>Zane<br>Zane@agentmail.to<br>Wellness 125 Cafeteria Plan</p>",
    "cc": ["sam@impactquadrant.info"]
  }'

echo ""
echo ""

# Email 2: Precision Machining Company, LLC
echo "Sending to: Precision Machining Company, LLC"
echo "To: admin@precisionmachiningtexas.com"
echo "Savings: \$49,050 (50 employees)"

curl -s -X POST "https://api.agentmail.to/v0/inboxes/${INBOX}/messages" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["admin@precisionmachiningtexas.com"],
    "subject": "$49,050 annual savings for Precision Machining Company (zero cost to implement)",
    "text": "Hi,\n\nI noticed Precision Machining Company has about 50 employees, which positions you for significant annual savings through a compliant Section 125 wellness program.\n\nOrganizations your size are typically saving:\n• $681 per employee annually in FICA savings\n• 30-60% reduction in workers comp premiums\n• Total savings: $49,050\n\nOne medical transportation company with 66 employees saved over $140,000 last year.\n\nThe program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.\n\nWould you be open to a 10-minute call this week to see the numbers for Precision Machining Company?\n\nBest,\nZane\nZane@agentmail.to\nWellness 125 Cafeteria Plan",
    "html": "<p>Hi,</p><p>I noticed Precision Machining Company has about 50 employees, which positions you for significant annual savings through a compliant Section 125 wellness program.</p><p><strong>Organizations your size are typically saving:</strong></p><ul><li>$681 per employee annually in FICA savings</li><li>30-60% reduction in workers comp premiums</li><li><strong>Total savings: $49,050</strong></li></ul><p>One medical transportation company with 66 employees saved over $140,000 last year.</p><p>The program also increases employee take-home pay by $50-$400/month while adding 24/7 virtual healthcare - at zero cost to you or your employees.</p><p>Would you be open to a 10-minute call this week to see the numbers for Precision Machining Company?</p><p>Best,<br>Zane<br>Zane@agentmail.to<br>Wellness 125 Cafeteria Plan</p>",
    "cc": ["sam@impactquadrant.info"]
  }'

echo ""
echo ""
echo "=========================================="
echo "Outreach Complete"
echo "=========================================="
