#!/bin/bash
# bdev_ai_deepseek_cron.sh
# Daily Bdev.ai + DeepSeek integration cron job

cd /Users/cubiczan/.openclaw/workspace

echo "========================================="
echo "Bdev.ai + DeepSeek Daily Integration"
echo "Started: $(date)"
echo "========================================="

# Run DeepSeek integration
python3 bdev_ai_deepseek_integration.py --batch-size 50

# Check if output was created
if ls bdev_ai_deepseek_*.csv 1> /dev/null 2>&1; then
    echo "✅ Integration completed successfully"
    LATEST_CSV=$(ls -t bdev_ai_deepseek_*.csv | head -1)
    echo "📊 Output: $LATEST_CSV"
    
    # Optional: Send to outreach system
    # python3 send_to_agentmail.py "$LATEST_CSV"
    
else
    echo "❌ Integration failed - no output created"
    exit 1
fi

echo "========================================="
echo "Completed: $(date)"
echo "========================================="
