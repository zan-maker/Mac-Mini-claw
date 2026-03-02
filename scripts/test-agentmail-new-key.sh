#!/bin/bash
# Test AgentMail API with new key

AGENTMAIL_API_KEY="am_us_f03e762c50d6e353bbe7b4307b452bd73f58aed725bc0ef53f25d9f8e91c962a"
FROM_EMAIL="Zane@agentmail.to"
TEST_EMAIL="test@example.com"  # Change to a real email for actual test

echo "Testing AgentMail API with new key..."
echo "API Key: ${AGENTMAIL_API_KEY:0:20}..."
echo

# Test 1: Check API connectivity
echo "Test 1: Checking API connectivity..."
curl -s -X GET "https://api.agentmail.to/v1/health" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  --max-time 10

echo
echo

# Test 2: Send test email (commented out for safety)
echo "Test 2: Sending test email (commented out - uncomment to test)"
echo "To send actual test email, uncomment the curl command below and set TEST_EMAIL to a real address"
echo

# Uncomment to actually send test email:
# curl -s -X POST "https://api.agentmail.to/v1/emails" \
#   -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "from": "'"$FROM_EMAIL"'",
#     "to": ["'"$TEST_EMAIL"'"],
#     "subject": "AgentMail API Test - New Key Working",
#     "body": "This is a test email sent using the new AgentMail API key.\n\nIf you receive this, the new API key is working correctly!\n\nBest regards,\n\nTest System"
#   }' && echo "✅ Test email sent to $TEST_EMAIL" || echo "❌ Failed to send test email"

echo
echo "Test complete. If no errors above, API key appears valid."
echo "Note: Actual email sending is commented out for safety."