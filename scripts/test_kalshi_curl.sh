#!/bin/bash
# Test Kalshi API with curl commands

echo "🔗 TESTING KALSHI API WITH CURL"
echo "=========================================="

# Load credentials from config
CONFIG_FILE="/Users/cubiczan/.openclaw/workspace/secrets/kalshi_config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Config file not found"
    exit 1
fi

KEY_ID=$(jq -r '.key_id' "$CONFIG_FILE")
PRIVATE_KEY=$(jq -r '.private_key' "$CONFIG_FILE")

echo "✅ Credentials loaded"
echo "📋 Key ID: ${KEY_ID:0:8}..."
echo "🔑 Private Key: ${#PRIVATE_KEY} chars"

# Try different API endpoints
ENDPOINTS=(
    "https://api.kalshi.com/v1"
    "https://api.elections.kalshi.com/v1"
    "https://trading-api.kalshi.com/v1"
)

echo ""
echo "🌐 TESTING ENDPOINTS:"
echo "=========================================="

for ENDPOINT in "${ENDPOINTS[@]}"; do
    echo "Testing: $ENDPOINT"
    
    # Simple GET request
    RESPONSE=$(curl -s -w "%{http_code}" "$ENDPOINT" 2>/dev/null)
    STATUS=${RESPONSE: -3}
    BODY=${RESPONSE:0:${#RESPONSE}-3}
    
    echo "  Status: $STATUS"
    
    if [ "$STATUS" = "200" ]; then
        echo "  ✅ Endpoint available"
        echo "  Response: $BODY"
        WORKING_ENDPOINT="$ENDPOINT"
        break
    elif [ "$STATUS" = "404" ]; then
        echo "  ❌ 404 Not Found"
    elif [ "$STATUS" = "401" ]; then
        echo "  ⚠️  401 Unauthorized (needs auth)"
        WORKING_ENDPOINT="$ENDPOINT"
        break
    else
        echo "  ❌ Error: $BODY"
    fi
    
    echo ""
done

echo ""
echo "🎯 MANUAL TESTING INSTRUCTIONS:"
echo "=========================================="
echo "1. Go to Kalshi.com and login"
echo "2. Navigate to Account → API Settings"
echo "3. Check if your API key is active"
echo "4. Look for API documentation/endpoints"
echo ""
echo "📋 COMMANDS TO TRY:"
echo "=========================================="
echo "# Test with timestamp (replace with actual signature)"
echo "TIMESTAMP=\$(date +%s)"
echo "curl -X GET https://api.kalshi.com/v1/account \\"
echo "  -H 'KALSHI-ACCESS-KEY: $KEY_ID' \\"
echo "  -H 'KALSHI-ACCESS-SIGNATURE: test_signature' \\"
echo "  -H 'KALSHI-ACCESS-TIMESTAMP: \$TIMESTAMP'"
echo ""
echo "💡 TROUBLESHOOTING:"
echo "=========================================="
echo "1. Check Kalshi API documentation"
echo "2. Verify API key has trading permissions"
echo "3. Try generating signature with Python cryptography"
echo "4. Start with $1 test trades once API works"

echo ""
echo "🚀 QUICK CHECK:"
echo "=========================================="
echo "# Check if we can at least reach Kalshi"
curl -s -I "https://kalshi.com" | head -1
echo ""
echo "# Check current gas prices (public endpoint)"
curl -s "https://gasprices.aaa.com/?state=NY" | grep -o "national avg.*[0-9]\.[0-9][0-9]" | head -1 || echo "Could not fetch gas prices"