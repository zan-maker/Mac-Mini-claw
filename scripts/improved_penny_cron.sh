#!/bin/bash
# IMPROVED Penny Stock Cron Script
# With better error handling and Discord notifications

WORKSPACE="/Users/cubiczan/.openclaw/workspace"
LOG_DIR="$WORKSPACE/logs/trade-recommender"
LOG_FILE="$LOG_DIR/daily_analysis_$(date +%Y-%m-%d).log"
DISCORD_SCRIPT="$WORKSPACE/scripts/send_discord_alert.sh"

# Create log directory
mkdir -p "$LOG_DIR"

echo "========================================" >> "$LOG_FILE"
echo "PENNY STOCK ANALYSIS - $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Step 1: Run analysis
echo "Step 1: Running Reddit analysis..." >> "$LOG_FILE"
cd /Users/cubiczan/mac-bot/skills/trade-recommender

if /usr/bin/python3 daily_reddit_analysis.py >> "$LOG_FILE" 2>&1; then
    echo "✅ Analysis completed successfully" >> "$LOG_FILE"
    
    # Step 2: Send Discord notification
    echo "Step 2: Sending Discord notification..." >> "$LOG_FILE"
    
    # Find latest report
    REPORT_FILE=$(find "$WORKSPACE/trades" -name "daily-recommendations-$(date +%Y-%m-%d)*.json" -o -name "daily-recommendations-$(date +%Y-%m-%d)*.md" | head -1)
    
    if [ -n "$REPORT_FILE" ]; then
        echo "📄 Found report: $REPORT_FILE" >> "$LOG_FILE"
        
        # Use enhanced Discord notification
        if /usr/bin/python3 enhanced_discord_notification.py >> "$LOG_FILE" 2>&1; then
            echo "✅ Discord notification prepared" >> "$LOG_FILE"
            
            # Actually send to Discord
            TODAY=$(date +%Y-%m-%d)
            MESSAGE="🎯 Penny stock analysis complete for $TODAY. Check #mac-mini5 for recommendations."
            
            openclaw message send --channel discord --target 1476397048889872424 --message "$MESSAGE" >> "$LOG_FILE" 2>&1
            
            echo "✅ Discord message sent" >> "$LOG_FILE"
        else
            echo "❌ Discord notification failed" >> "$LOG_FILE"
        fi
    else
        echo "❌ No report file found" >> "$LOG_FILE"
    fi
else
    echo "❌ Analysis failed" >> "$LOG_FILE"
    
    # Send error notification
    ERROR_MSG="❌ Penny stock analysis failed for $(date +%Y-%m-%d). Check logs."
    openclaw message send --channel discord --target 1476397048889872424 --message "$ERROR_MSG" >> "$LOG_FILE" 2>&1
fi

echo "========================================" >> "$LOG_FILE"
echo "CRON JOB COMPLETED" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Display last 10 lines of log
echo "Log file: $LOG_FILE"
tail -10 "$LOG_FILE"
