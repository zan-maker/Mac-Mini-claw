#!/bin/bash
# Backup System Health Check

set -e

HEALTH_LOG="$HOME/backups/openclaw/logs/health_check.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "=== Health Check Started at $TIMESTAMP ===" >> "$HEALTH_LOG"

# Run health check
export BBACKUP_OUTPUT=json
HEALTH_RESULT=$(bbman health --output json 2>&1)

echo "$HEALTH_RESULT" >> "$HEALTH_LOG"

# Parse JSON result
if echo "$HEALTH_RESULT" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if not data.get('success', False):
        print('HEALTH_CHECK_FAILED')
        sys.exit(1)
except Exception as e:
    print('PARSE_ERROR', str(e))
    sys.exit(1)
"; then
    echo "Health check passed" >> "$HEALTH_LOG"
else
    echo "Health check failed" >> "$HEALTH_LOG"
    # Send alert (uncomment to enable)
    # echo "Backup health check failed at $TIMESTAMP" | mail -s "Backup Alert" sam@cubiczan.com
fi

echo "=== Health Check Completed ===" >> "$HEALTH_LOG"
echo "" >> "$HEALTH_LOG"
