#!/bin/bash
# API Usage Monitor for OpenClaw
# Tracks token usage and alerts when approaching limits

WORKSPACE="/Users/cubiczan/.openclaw/workspace"
USAGE_FILE="$WORKSPACE/api-usage.json"
ALERT_LOG="$WORKSPACE/api-alerts.log"
DISCORD_WEBHOOK=""  # Set if needed, or use message tool

# API Pricing (per 1M tokens)
# Update these based on your actual plans
ZAI_INPUT_COST=0.40
ZAI_OUTPUT_COST=1.50
XAI_INPUT_COST=2.00  # Estimate - verify actual pricing
XAI_OUTPUT_COST=10.00  # Estimate - verify actual pricing

# Thresholds
LOW_THRESHOLD=20  # Alert when 20% of budget remaining
CRITICAL_THRESHOLD=10  # Alert when 10% of budget remaining

# Monthly budget (adjust based on your actual limits)
MONTHLY_BUDGET=50  # USD

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Get current date
TODAY=$(date +%Y-%m-%d)
MONTH=$(date +%Y-%m)

# Initialize usage file if it doesn't exist
if [ ! -f "$USAGE_FILE" ]; then
    cat > "$USAGE_FILE" << EOF
{
  "monthly": {
    "$MONTH": {
      "zai_tokens": {"input": 0, "output": 0},
      "xai_tokens": {"input": 0, "output": 0},
      "cost_usd": 0
    }
  },
  "budget": $MONTHLY_BUDGET,
  "last_check": "$TODAY"
}
EOF
fi

# Function to get session usage (calls OpenClaw session_status)
# This is a placeholder - in reality, OpenClaw would need to expose usage stats
get_session_usage() {
    # For now, estimate based on typical daily usage
    # In production, this would query actual API usage from OpenClaw
    
    # Example: If we had access to session_status output
    # usage=$(openclaw session-status --json 2>/dev/null)
    
    # Placeholder: Estimate 2M tokens/day for GLM-5, 0.5M for Grok
    echo "zai_input=1500000,zai_output=500000,xai_input=200000,xai_output=100000"
}

# Parse current usage
usage_data=$(get_session_usage)

# Extract values
zai_input=$(echo "$usage_data" | grep -o 'zai_input=[0-9]*' | cut -d= -f2)
zai_output=$(echo "$usage_data" | grep -o 'zai_output=[0-9]*' | cut -d= -f2)
xai_input=$(echo "$usage_data" | grep -o 'xai_input=[0-9]*' | cut -d= -f2)
xai_output=$(echo "$usage_data" | grep -o 'xai_output=[0-9]*' | cut -d= -f2)

# Calculate costs
zai_cost=$(echo "scale=2; ($zai_input / 1000000 * $ZAI_INPUT_COST) + ($zai_output / 1000000 * $ZAI_OUTPUT_COST)" | bc)
xai_cost=$(echo "scale=2; ($xai_input / 1000000 * $XAI_INPUT_COST) + ($xai_output / 1000000 * $XAI_OUTPUT_COST)" | bc)
total_daily_cost=$(echo "scale=2; $zai_cost + $xai_cost" | bc)

# Update usage file (append to monthly totals)
# Using Python for JSON manipulation
python3 << EOF
import json
import sys

try:
    with open('$USAGE_FILE', 'r') as f:
        data = json.load(f)
    
    month = '$MONTH'
    if month not in data['monthly']:
        data['monthly'][month] = {
            'zai_tokens': {'input': 0, 'output': 0},
            'xai_tokens': {'input': 0, 'output': 0},
            'cost_usd': 0
        }
    
    # Add daily usage to monthly totals
    data['monthly'][month]['zai_tokens']['input'] += $zai_input
    data['monthly'][month]['zai_tokens']['output'] += $zai_output
    data['monthly'][month]['xai_tokens']['input'] += $xai_input
    data['monthly'][month]['xai_tokens']['output'] += $xai_output
    data['monthly'][month]['cost_usd'] += $total_daily_cost
    data['last_check'] = '$TODAY'
    
    with open('$USAGE_FILE', 'w') as f:
        json.dump(data, f, indent=2)
    
    # Calculate percentage of budget used
    budget = data['budget']
    spent = data['monthly'][month]['cost_usd']
    percent_used = (spent / budget) * 100
    percent_remaining = 100 - percent_used
    
    # Output status
    print(f"BUDGET_STATUS:{percent_remaining:.1f}:{spent:.2f}:{budget}")
    
    # Check thresholds
    if percent_remaining <= $CRITICAL_THRESHOLD:
        print(f"CRITICAL:{percent_remaining:.1f}")
        sys.exit(2)
    elif percent_remaining <= $LOW_THRESHOLD:
        print(f"LOW:{percent_remaining:.1f}")
        sys.exit(1)
    else:
        print(f"OK:{percent_remaining:.1f}")
        sys.exit(0)
        
except Exception as e:
    print(f"ERROR:{str(e)}")
    sys.exit(3)
EOF

exit_code=$?

# Read output from Python
output=$(python3 << 'PYEOF'
import json
with open('/Users/cubiczan/.openclaw/workspace/api-usage.json', 'r') as f:
    data = json.load(f)
    month = '$MONTH'
    if month in data['monthly']:
        spent = data['monthly'][month]['cost_usd']
        budget = data['budget']
        remaining_pct = ((budget - spent) / budget) * 100
        print(f"{remaining_pct:.1f}:{spent:.2f}:{budget}")
PYEOF
)

remaining_pct=$(echo "$output" | cut -d: -f1)
spent=$(echo "$output" | cut -d: -f2)
budget=$(echo "$output" | cut -d: -f3)

# Log the check
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Budget check: ${remaining_pct}% remaining (\$${spent} spent of \$${budget})" >> "$ALERT_LOG"

# Generate alerts
if [ $exit_code -eq 2 ]; then
    # CRITICAL
    alert_msg="🚨 CRITICAL: API budget at ${remaining_pct}% (\$${spent} spent of \$${budget}). Top up immediately!"
    echo -e "${RED}$alert_msg${NC}"
    
    # Store alert for OpenClaw to send
    echo "$alert_msg" > "$WORKSPACE/.api-alert-critical"
    
elif [ $exit_code -eq 1 ]; then
    # LOW
    alert_msg="⚠️ WARNING: API budget at ${remaining_pct}% (\$${spent} spent of \$${budget}). Consider topping up soon."
    echo -e "${YELLOW}$alert_msg${NC}"
    
    # Store alert for OpenClaw to send
    echo "$alert_msg" > "$WORKSPACE/.api-alert-low"
    
else
    # OK
    echo -e "${GREEN}✓ API budget healthy: ${remaining_pct}% remaining (\$${spent} spent of \$${budget})${NC}"
fi

exit $exit_code
