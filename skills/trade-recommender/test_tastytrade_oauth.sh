#!/bin/bash
# Tastytrade OAuth Test Script
# Requires: Client Secret and Refresh Token

CLIENT_ID="0c7b8898-a2f1-49bb-a23d-843e47b68631"

echo "============================================================"
echo "TASTYTRADE OAUTH TEST"
echo "============================================================"
echo
echo "Client ID: $CLIENT_ID ✅"
echo
echo "⚠️  OAuth requires two additional credentials:"
echo "    1. Client Secret"
echo "    2. Refresh Token"
echo
echo "Please provide your credentials:"
echo
read -p "Client Secret: " CLIENT_SECRET
read -p "Refresh Token: " REFRESH_TOKEN
echo

# Test OAuth token exchange
echo "--- Testing OAuth Token Exchange ---"
RESULT=$(curl -s -X POST "https://api.tastyworks.com/oauth/token" \
  -H "Content-Type: application/json" \
  -d "{
    \"client_id\": \"$CLIENT_ID\",
    \"client_secret\": \"$CLIENT_SECRET\",
    \"refresh_token\": \"$REFRESH_TOKEN\",
    \"grant_type\": \"refresh_token\"
  }" 2>&1)

if echo "$RESULT" | grep -q "access_token"; then
  echo "✅ OAuth token exchange successful"
  echo
  echo "Session token received (valid for 15 minutes)"
  echo "$RESULT" | python3 -m json.tool 2>/dev/null | head -10
  echo
  echo "✅ Connection successful!"
  echo
  echo "Save these credentials for future use:"
  echo "  Client Secret: $CLIENT_SECRET"
  echo "  Refresh Token: $REFRESH_TOKEN"
  echo
  echo "Add to environment:"
  echo "  export TASTYTRADE_CLIENT_SECRET='$CLIENT_SECRET'"
  echo "  export TASTYTRADE_REFRESH_TOKEN='$REFRESH_TOKEN'"
elif echo "$RESULT" | grep -q "error\|invalid"; then
  echo "❌ OAuth failed"
  echo "$RESULT" | python3 -m json.tool 2>/dev/null || echo "$RESULT"
  echo
  echo "Common issues:"
  echo "  - Invalid client secret"
  echo "  - Expired/invalid refresh token"
  echo "  - OAuth app not properly configured"
else
  echo "⚠️  Unexpected response"
  echo "$RESULT"
fi

echo
echo "============================================================"
