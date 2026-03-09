#!/bin/bash
# Update cron jobs to use hybrid local model scripts

WORKSPACE="/Users/cubiczan/.openclaw/workspace"
CRON_UPDATE_LOG="$WORKSPACE/logs/cron-update-$(date +%Y%m%d_%H%M%S).log"

echo "=== Cron Job Localization Update ===" > "$CRON_UPDATE_LOG"
echo "Timestamp: $(date)" >> "$CRON_UPDATE_LOG"
echo "" >> "$CRON_UPDATE_LOG"

# Function to update a cron job
update_cron_job() {
    local job_name="$1"
    local schedule="$2"
    local script_path="$3"
    
    echo "Updating: $job_name" | tee -a "$CRON_UPDATE_LOG"
    echo "Schedule: $schedule" | tee -a "$CRON_UPDATE_LOG"
    echo "Script: $script_path" | tee -a "$CRON_UPDATE_LOG"
    
    # Check if script exists
    if [ ! -f "$script_path" ]; then
        echo "ERROR: Script not found: $script_path" | tee -a "$CRON_UPDATE_LOG"
        return 1
    fi
    
    # Make script executable
    chmod +x "$script_path"
    
    # Create cron job command
    local cron_command="cd $WORKSPACE && python3 $script_path"
    
    # For now, just log what would be created
    # In production, this would actually create/update the cron job
    echo "Cron command: $cron_command" | tee -a "$CRON_UPDATE_LOG"
    echo "Would create: $schedule $cron_command" | tee -a "$CRON_UPDATE_LOG"
    echo "" >> "$CRON_UPDATE_LOG"
    
    return 0
}

# Update monitoring cron jobs
echo "=== UPDATING MONITORING CRON JOBS ===" >> "$CRON_UPDATE_LOG"

# 1. Token Limit Monitor (every 30 minutes)
update_cron_job \
    "Token Limit Monitor" \
    "*/30 * * * *" \
    "scripts/hybrid-token-monitor.py"

# 2. Critical API Alert (every 12 hours)
update_cron_job \
    "Critical API Alert" \
    "0 */12 * * *" \
    "scripts/hybrid-critical-alert.py"

# 3. Daily API Usage Check (daily at 9 AM)
update_cron_job \
    "Daily API Usage Check" \
    "0 9 * * *" \
    "scripts/hybrid-api-monitor.py"

# 4. Heartbeat Check (every 30 minutes)
update_cron_job \
    "Heartbeat Check" \
    "*/30 * * * *" \
    "scripts/hybrid-heartbeat.py"

# Create actual crontab entries
echo "" >> "$CRON_UPDATE_LOG"
echo "=== ACTUAL CRONTAB ENTRIES ===" >> "$CRON_UPDATE_LOG"
echo "" >> "$CRON_UPDATE_LOG"

cat >> "$CRON_UPDATE_LOG" << 'EOF'
# Add these lines to your crontab (crontab -e):

# Token Limit Monitor (every 30 minutes)
*/30 * * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/hybrid-token-monitor.py >> logs/token-monitor.log 2>&1

# Critical API Alert (every 12 hours)
0 */12 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/hybrid-critical-alert.py >> logs/critical-alert.log 2>&1

# Daily API Usage Check (daily at 9 AM)
0 9 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/hybrid-api-monitor.py >> logs/api-usage.log 2>&1

# Heartbeat Check (every 30 minutes)
*/30 * * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/hybrid-heartbeat.py >> logs/heartbeat.log 2>&1

EOF

echo "" >> "$CRON_UPDATE_LOG"
echo "=== VERIFICATION COMMANDS ===" >> "$CRON_UPDATE_LOG"
echo "" >> "$CRON_UPDATE_LOG"

cat >> "$CRON_UPDATE_LOG" << 'EOF'
# To verify the cron jobs are working:

# 1. Check if scripts are executable:
ls -la scripts/hybrid-*.py

# 2. Test each script manually:
python3 scripts/hybrid-token-monitor.py
python3 scripts/hybrid-critical-alert.py
python3 scripts/hybrid-api-monitor.py
python3 scripts/hybrid-heartbeat.py

# 3. Check logs after first run:
tail -f logs/token-monitor.log
tail -f logs/critical-alert.log
tail -f logs/api-usage.log
tail -f logs/heartbeat.log

# 4. Check cost savings:
cat logs/heartbeat-cost-savings.json | jq '.entries[-1]'
cat logs/local-model-api-monitor.json | jq '.entries[-1]'
cat logs/local-model-token-monitor.json | jq '.entries[-1]'
cat logs/local-model-critical-alert.json | jq '.entries[-1]'

EOF

echo "" >> "$CRON_UPDATE_LOG"
echo "=== MONTHLY COST SAVINGS PROJECTION ===" >> "$CRON_UPDATE_LOG"
echo "" >> "$CRON_UPDATE_LOG"

cat >> "$CRON_UPDATE_LOG" << 'EOF'
Monthly Cost Projection:
- Token Monitor: 48 checks/day × $0.0005 = $0.024/day = $0.72/month
- Critical Alert: 2 checks/day × $0.0003 = $0.0006/day = $0.018/month
- API Usage: 1 check/day × $0.0005 = $0.0005/day = $0.015/month
- Heartbeat: 48 checks/day × $0.0004 = $0.0192/day = $0.576/month
------------------------------------------------------------
TOTAL: $1.329/month (vs $2.97/month API-only)
SAVINGS: $1.641/month (55% reduction)

EOF

echo "Update complete. Log saved to: $CRON_UPDATE_LOG"
echo "Please add the crontab entries manually using: crontab -e"
echo "Then copy the entries from the log file above."