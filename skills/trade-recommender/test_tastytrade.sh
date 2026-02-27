#!/bin/bash
# Tastytrade API Test Script
# Quick connection test using curl

API_KEY="80e479d6235f546b188f9c86ec53bf80019c4bff"
BASE_URL="https://api.tastyworks.com"

echo "============================================================"
echo "TASTYTRADE API CONNECTION TEST"
echo "============================================================"
echo

# Test 1: Get User Info
echo -n "1. Testing authentication... "
RESULT=$(curl -s "$BASE_URL/customers/me" \
  -H "Authorization: $API_KEY" \
  -H "Content-Type: application/json" 2>&1)

if echo "$RESULT" | grep -q "email\|data"; then
  echo "✅ OK"
  echo "$RESULT" | python3 -m json.tool 2>/dev/null | head -10
else
  echo "❌ FAILED"
  echo "$RESULT" | head -5
fi

echo

# Test 2: Get Accounts
echo -n "2. Getting accounts... "
RESULT=$(curl -s "$BASE_URL/customers/me/accounts" \
  -H "Authorization: $API_KEY" \
  -H "Content-Type: application/json" 2>&1)

if echo "$RESULT" | grep -q "items\|account"; then
  echo "✅ OK"
  echo "$RESULT" | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'Found {len(data.get(\"data\", {}).get(\"items\", []))} account(s)')" 2>/dev/null || echo "Could not parse"
else
  echo "❌ FAILED"
  echo "$RESULT" | head -5
fi

echo

# Test 3: Get Account Balance
echo -n "3. Getting account balance... "
# First extract account number from previous response
ACCOUNT_NUM=$(echo "$RESULT" | python3 -c "import sys,json; data=json.load(sys.stdin); items=data.get('data',{}).get('items',[]); print(items[0]['account']['account-number'] if items else '')" 2>/dev/null)

if [ -n "$ACCOUNT_NUM" ]; then
  BALANCE=$(curl -s "$BASE_URL/accounts/$ACCOUNT_NUM/balances" \
    -H "Authorization: $API_KEY" \
    -H "Content-Type: application/json" 2>&1)

  if echo "$BALANCE" | grep -q "cash\|buying"; then
    echo "✅ OK"
    echo "$BALANCE" | python3 -c "import sys,json; data=json.load(sys.stdin); b=data['data']['buying-power']; print(f'Buying Power: ${b:,.2f}')" 2>/dev/null || echo "Could not parse"
  else
    echo "❌ FAILED"
  fi
else
  echo "⚠️ No account number found"
fi

echo
echo "============================================================"
echo "API test complete"
echo "============================================================"
