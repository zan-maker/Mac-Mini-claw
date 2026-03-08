#!/bin/bash

# Setup cron jobs for metals monitoring

echo "⏰ Setting up Metals Monitoring Cron Jobs"
echo "========================================="

CRON_JOBS=(
    # Every 15 minutes: Monitor all metals
    "*/15 * * * * cd $HOME/.openclaw/workspace/metals_monitoring && python3 metals-monitor.py >> monitoring.log 2>&1"
    
    # 9:00 AM daily: Morning metals report
    "0 9 * * * cd $HOME/.openclaw/workspace/metals_monitoring && python3 daily-report.py >> daily_reports.log 2>&1"
    
    # 4:00 PM daily: End of day summary
    "0 16 * * * cd $HOME/.openclaw/workspace/metals_monitoring && python3 daily-report.py --end-of-day >> eod_reports.log 2>&1"
    
    # Monday 6:00 AM: Weekly metals outlook
    "0 6 * * 1 cd $HOME/.openclaw/workspace/metals_monitoring && python3 weekly-outlook.py >> weekly_outlook.log 2>&1"
)

# Add to crontab
for job in "${CRON_JOBS[@]}"; do
    (crontab -l 2>/dev/null | grep -F "$job") || (crontab -l 2>/dev/null; echo "$job") | crontab -
    echo "✅ Added: $job"
done

echo ""
echo "📋 Cron Jobs Summary:"
echo "   1. Every 15 minutes: Real-time metals monitoring"
echo "   2. 9:00 AM daily: Morning trading report"
echo "   3. 4:00 PM daily: End-of-day summary"
echo "   4. Monday 6:00 AM: Weekly outlook"
echo ""
echo "📁 Log files in: $HOME/.openclaw/workspace/metals_monitoring/"
echo "   - monitoring.log (15-minute updates)"
echo "   - daily_reports.log (morning reports)"
echo "   - eod_reports.log (end-of-day)"
echo "   - weekly_outlook.log (weekly outlook)"
