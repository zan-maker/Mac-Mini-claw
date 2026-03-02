#!/bin/bash
# Test AgentMail API

AGENTMAIL_API_KEY="am_us_6aa957b36fb69693140cb0787c894d90ec2e65ffe937049634b685b911c1ac14"
FROM_EMAIL="Zane@agentmail.to"
CC_EMAIL="sam@impactquadrant.info"

echo "Testing AgentMail API..."
echo "API Key: ${AGENTMAIL_API_KEY:0:10}..."
echo "From: $FROM_EMAIL"
echo

# Test 1: Check if endpoint exists
echo "Test 1: Checking /v1/emails endpoint"
curl -v -X POST "https://api.agentmail.to/v1/emails" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'"$FROM_EMAIL"'",
    "to": ["test@example.com"],
    "subject": "Test",
    "body": "Test email"
  }' 2>&1 | grep -E "(HTTP|< HTTP|{)" | head -20

echo
echo "---"
echo

# Test 2: Check /v0 endpoint
echo "Test 2: Checking /v0 endpoint"
curl -v -X GET "https://api.agentmail.to/v0/inboxes/Zane@agentmail.to" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" 2>&1 | grep -E "(HTTP|< HTTP|{)" | head -10