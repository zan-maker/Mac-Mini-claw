#!/bin/bash
# Create Kalshi cron jobs
# This script adds all Kalshi scanning cron jobs to crontab

echo "Creating Kalshi cron jobs..."
echo "=============================="

# Define cron jobs
CRON_JOBS=(
  # Premarket Scan (7:00 AM EST)
  "0 7 * * * cd /Users/cubiczan/.openclaw/workspace && /usr/bin/python3 scripts/kalshi-daily-scanner.py premarket >> /Users/cubiczan/.openclaw/workspace/logs/kalshi-premarket.log 2>&1"
  
  # Market Open Scan (9:30 AM EST)
  "30 9 * * * cd /Users/cubiczan/.openclaw/workspace && /usr/bin/python3 scripts/kalshi-daily-scanner.py midday >> /Users/cubiczan/.openclaw/workspace/logs/kalshi-market-open.log 2>&1"
  
  # Midday Scan (11:00 AM EST)
  "0 11 * * * cd /Users/cubiczan/.openclaw/workspace && /usr/bin/python3 scripts/kalshi-daily-scanner.py midday >> /Users/cubiczan/.openclaw/workspace/logs/kalshi-midday.log 2>&1"
  
  # Afternoon Scan (1:00 PM EST)
  "0 13 * * * cd /Users/cubiczan/.openclaw/workspace && /usr/bin/python3 scripts/kalshi-daily-scanner.py midday >> /Users/cubiczan/.openclaw/workspace/logs/kalshi-afternoon.log 2>&1"
  
  # Post-market Scan (4:30 PM EST)
  "30 16 * * * cd /Users/cubiczan/.openclaw/workspace && /usr/bin/python3 scripts/kalshi-daily-scanner.py postmarket >> /Users/cubiczan/.openclaw/workspace/logs/kalshi-postmarket.log 2>&1"
  
  # Evening Scan (7:00 PM EST)
  "0 19 * * * cd /Users/cubiczan/.openclaw/workspace && /usr/bin/python3 scripts/kalshi-daily-scanner.py postmarket >> /Users/cubiczan/.openclaw/workspace/logs/kalshi-evening.log 2>&1"
  
  # Every 2 Hours (9 AM - 5 PM)
  "0 9-17/2 * * * cd /Users/cubiczan/.openclaw/workspace && /usr/bin/python3 scripts/kalshi-daily-scanner.py midday >> /Users/cubiczan/.openclaw/workspace/logs/kalshi-2hour.log 2>&1"
)

# Create log directory
mkdir -p /Users/cubiczan/.openclaw/workspace/logs

# Add each cron job
echo "Adding cron jobs to crontab..."
for job in "${CRON_JOBS[@]}"; do
  # Check if job already exists
  if ! crontab -l 2>/dev/null | grep -F "$job" > /dev/null; then
    (crontab -l 2>/dev/null; echo "$job") | crontab -
    echo "✅ Added: $(echo "$job" | cut -d' ' -f1-5)"
  else
    echo "⚠️ Already exists: $(echo "$job" | cut -d' ' -f1-5)"
  fi
done

echo ""
echo "=============================="
echo "CRON JOBS CREATED SUCCESSFULLY"
echo "=============================="
echo ""
echo "Schedule Summary:"
echo "----------------"
echo "7:00 AM  - Premarket scan"
echo "9:30 AM  - Market open scan"
echo "11:00 AM - Midday scan"
echo "1:00 PM  - Afternoon scan"
echo "4:30 PM  - Post-market scan"
echo "7:00 PM  - Evening scan"
echo "Every 2h - Real-time monitoring (9 AM - 5 PM)"
echo ""
echo "Log files: /Users/cubiczan/.openclaw/workspace/logs/"
echo "Output files: kalshi-scan-{time}-{timestamp}.json"
echo ""
echo "First scan will run at the next scheduled time."
echo "To run manually: python3 scripts/kalshi-daily-scanner.py [premarket|midday|postmarket]"