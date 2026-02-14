#!/bin/bash
# API Balance Checker for OpenClaw
# Checks xAI and Zhipu AI balances and alerts if below thresholds

# Thresholds
REMINDER_THRESHOLD=25  # percent
CRITICAL_THRESHOLD=5   # percent

# Discord channel to alert
DISCORD_CHANNEL="1471933082297831545"  # #mac-mini1

# Log file
LOG_FILE="/Users/cubiczan/.openclaw/logs/api-balance-check.log"

# Function to log
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Function to check xAI balance
check_xai_balance() {
    # xAI API endpoint for usage/balance
    # The API key should be available in the environment
    if [ -z "$XAI_API_KEY" ]; then
        log "ERROR: XAI_API_KEY not set"
        return 1
    fi
    
    # Try to get balance from xAI API
    # Note: xAI may not have a direct balance endpoint, so we might need to
    # check their dashboard or use a different method
    RESPONSE=$(curl -s -H "Authorization: Bearer $XAI_API_KEY" \
        "https://api.x.ai/v1/usage" 2>/dev/null)
    
    if [ $? -eq 0 ] && [ -n "$RESPONSE" ]; then
        echo "$RESPONSE"
    else
        log "WARNING: Could not fetch xAI balance"
        echo '{"error": "Could not fetch balance"}'
    fi
}

# Function to check Zhipu AI balance
check_zhipu_balance() {
    if [ -z "$ZHIPU_API_KEY" ]; then
        log "ERROR: ZHIPU_API_KEY not set"
        return 1
    fi
    
    # Zhipu AI balance endpoint
    RESPONSE=$(curl -s -H "Authorization: Bearer $ZHIPU_API_KEY" \
        "https://open.bigmodel.cn/api/paas/v4/balance" 2>/dev/null)
    
    if [ $? -eq 0 ] && [ -n "$RESPONSE" ]; then
        echo "$RESPONSE"
    else
        log "WARNING: Could not fetch Zhipu AI balance"
        echo '{"error": "Could not fetch balance"}'
    fi
}

# Function to send Discord alert
send_alert() {
    local level="$1"
    local message="$2"
    
    log "ALERT [$level]: $message"
    
    # Use OpenClaw message tool to send to Discord
    # This will be called from the cron job which has access to the gateway
    curl -s -X POST "http://localhost:18789/api/message" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $OPENCLAW_GATEWAY_TOKEN" \
        -d "{
            \"action\": \"send\",
            \"channel\": \"discord\",
            \"to\": \"$DISCORD_CHANNEL\",
            \"message\": \"$message\"
        }" 2>/dev/null
}

# Main check function
main() {
    log "Starting API balance check..."
    
    ALERTS=""
    
    # Check xAI
    XAI_BALANCE=$(check_xai_balance)
    log "xAI balance response: $XAI_BALANCE"
    
    # Check Zhipu
    ZHIPU_BALANCE=$(check_zhipu_balance)
    log "Zhipu balance response: $ZHIPU_BALANCE"
    
    # Parse balances and check thresholds
    # This is a placeholder - actual parsing depends on API response format
    
    # Send alerts if needed
    if [ -n "$ALERTS" ]; then
        send_alert "REMINDER" "$ALERTS"
    fi
    
    log "Balance check complete"
}

main "$@"
