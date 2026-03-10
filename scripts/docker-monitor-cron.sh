#!/bin/bash
# docker-monitor-cron.sh
# Cron job to monitor Docker system health and report issues

set -e

LOG_FILE="/tmp/docker-monitor-$(date +%Y%m%d).log"
HEALTH_SCRIPT="/Users/cubiczan/.openclaw/workspace/scripts/docker-health-check.sh"

echo "=========================================" >> "$LOG_FILE"
echo "Docker Monitor - $(date)" >> "$LOG_FILE"
echo "=========================================" >> "$LOG_FILE"

# Run health check and capture output
if [ -f "$HEALTH_SCRIPT" ]; then
    bash "$HEALTH_SCRIPT" >> "$LOG_FILE" 2>&1
else
    echo "ERROR: Health script not found at $HEALTH_SCRIPT" >> "$LOG_FILE"
fi

# Check for critical issues
CRITICAL_ISSUES=0

# Check if Docker daemon is responding
if ! docker ps > /dev/null 2>&1; then
    echo "CRITICAL: Docker daemon not responding" >> "$LOG_FILE"
    CRITICAL_ISSUES=1
fi

# Check disk usage (warning if > 10GB)
TOTAL_SIZE=$(docker system df --format '{{.Size}}' | head -1 | sed 's/[^0-9]*//g' 2>/dev/null || echo "0")
if [ "$TOTAL_SIZE" -gt 10000 ]; then  # More than 10GB
    echo "WARNING: High disk usage: ${TOTAL_SIZE}MB" >> "$LOG_FILE"
fi

# Check if container wrapper exists
if [ ! -f "/Users/cubiczan/container-test/simple-container.sh" ]; then
    echo "WARNING: Container wrapper script missing" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
echo "Summary:" >> "$LOG_FILE"
if [ "$CRITICAL_ISSUES" -eq 0 ]; then
    echo "✅ All systems normal" >> "$LOG_FILE"
else
    echo "⚠️  $CRITICAL_ISSUES critical issue(s) detected" >> "$LOG_FILE"
fi

echo "Log file: $LOG_FILE" >> "$LOG_FILE"
echo "=========================================" >> "$LOG_FILE"

# If critical issues, send notification (placeholder for Discord/webhook)
if [ "$CRITICAL_ISSUES" -gt 0 ]; then
    echo "ALERT: Docker system issues detected" > /tmp/docker-alert.txt
    echo "Check log: $LOG_FILE" >> /tmp/docker-alert.txt
    # In future: Send to Discord webhook
    # curl -X POST -H "Content-Type: application/json" -d @/tmp/docker-alert.txt $DISCORD_WEBHOOK
fi

# Keep only last 7 days of logs
find /tmp/docker-monitor-*.log -mtime +7 -delete 2>/dev/null || true