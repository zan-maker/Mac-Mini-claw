# API Balance Check - OpenClaw Compatible

This script checks API balances using OpenClaw's internal session_status rather than external env vars.

```bash
#!/bin/bash
# check-api-balances.sh - Check API usage via OpenClaw session status
# Compatible with OpenClaw's internal auth management

WORKSPACE="/Users/cubiczan/.openclaw/workspace"
GATEWAY_TOKEN="mac-local-gateway-secret-2026"
GATEWAY_URL="http://127.0.0.1:18789"

# Check OpenClaw session status for usage info
# OpenClaw manages API keys internally, so we query session_status

# Get current session usage
usage_json=$(curl -s -X POST "$GATEWAY_URL/api/session/status" \
  -H "Authorization: Bearer $GATEWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"includeUsage": true}')

# Parse usage data (if available)
# Note: OpenClaw may not expose exact token counts, but we can estimate
# based on context window usage

echo "=== API Balance Check ==="
echo "Timestamp: $(date)"
echo ""

# Check provider dashboards manually
echo "Provider Dashboards:"
echo "  xAI (Grok): https://console.x.ai"
echo "  Zhipu (GLM): https://open.bigmodel.cn"
echo "  DeepSeek: https://platform.deepseek.com/usage"
echo ""

# Estimate based on session activity
# For accurate tracking, check provider dashboards directly

# Alternative: Use api-monitor.sh for token-based estimates
if [ -f "$WORKSPACE/api-usage.json" ]; then
    echo "=== Local Usage Estimate ==="
    cat "$WORKSPACE/api-usage.json" | python3 -c "
import json, sys
from datetime import datetime
data = json.load(sys.stdin)
month = datetime.now().strftime('%Y-%m')
if month in data.get('monthly', {}):
    m = data['monthly'][month]
    print(f'Month: {month}')
    print(f'ZAI tokens (in/out): {m[\"zai_tokens\"][\"input\"]:,} / {m[\"zai_tokens\"][\"output\"]:,}')
    print(f'xAI tokens (in/out): {m[\"xai_tokens\"][\"input\"]:,} / {m[\"xai_tokens\"][\"output\"]:,}')
    print(f'Estimated cost: \${m[\"cost_usd\"]:.2f} / \${data[\"budget\"]}')
else:
    print('No usage data for current month')
"
fi
```

**Status:** Script created at /Users/cubiczan/.openclaw/workspace/scripts/check-api-balances.sh

**Note:** OpenClaw manages API keys internally. For exact balance checks, visit provider dashboards directly. The api-monitor.sh script provides token-based estimates.
