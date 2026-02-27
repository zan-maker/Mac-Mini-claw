#!/bin/bash
# Test script for Miami Hotels cron job fix
# Tests AgentMail API with a single email

AGENTMAIL_API_KEY="am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
FROM_EMAIL="zane@agentmail.to"
CC_EMAIL="sam@impactquadrant.info"

echo "Testing Miami Hotels cron job fix..."
echo "====================================="

# Test email to a test address (or your own email)
TEST_EMAIL="test@example.com"  # Change this to your email for real test
SUBJECT="Test - Miami Hotels Cron Job Fix"

BODY="This is a test email to verify the Miami Hotels cron job fix is working.

The cron jobs were timing out because:
1. Agent didn't have clear instructions on HOW to send emails
2. Timeouts were too short (180-600 seconds)
3. No specific API or script usage instructions

Now fixed with:
- Clear AgentMail API instructions
- Increased timeout to 1200 seconds
- Step-by-step email sending process

Best regards,

Zane
Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."

echo
echo "Sending test email to: $TEST_EMAIL"
echo "Subject: $SUBJECT"
echo

# Send test email
response=$(curl -s -w "\n%{http_code}" -X POST "https://api.agentmail.to/v1/emails" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'"$FROM_EMAIL"'",
    "to": ["'"$TEST_EMAIL"'"],
    "cc": ["'"$CC_EMAIL"'"],
    "subject": "'"$SUBJECT"'",
    "body": "'"$BODY"'"
  }')

# Extract HTTP status code
http_code=$(echo "$response" | tail -n1)
response_body=$(echo "$response" | sed '$d')

echo "HTTP Status Code: $http_code"
echo "Response: $response_body"
echo

if [ "$http_code" = "200" ] || [ "$http_code" = "201" ]; then
    echo "✅ SUCCESS: Test email sent successfully!"
    echo "The Miami Hotels cron job fix should work."
else
    echo "❌ FAILED: Could not send test email."
    echo "Possible issues:"
    echo "1. AgentMail API key might be invalid"
    echo "2. API endpoint might have changed"
    echo "3. Network or authentication issue"
    echo
    echo "Alternative: Use Gmail SMTP scripts instead"
fi

echo
echo "====================================="
echo "Next steps:"
echo "1. Update cron job instructions with fixed payload"
echo "2. Increase timeout to 1200 seconds"
echo "3. Test with real email address"
echo "4. Monitor next scheduled run"
echo "====================================="