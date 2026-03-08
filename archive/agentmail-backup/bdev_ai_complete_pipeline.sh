#!/bin/bash
# bdev_ai_complete_pipeline.sh
# Complete Bdev.ai → AgentMail pipeline

cd /Users/cubiczan/.openclaw/workspace

LOG_DIR="logs/bdev_ai"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/pipeline_$TIMESTAMP.log"

echo "========================================" | tee -a "$LOG_FILE"
echo "Bdev.ai Complete Pipeline" | tee -a "$LOG_FILE"
echo "Started: $(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

# Step 1: Generate AI messages
echo "🤖 Step 1: Bdev.ai Message Generation" | tee -a "$LOG_FILE"
python3 bdev_ai_openclaw_integration_final.py --batch-size 50 2>&1 | tee -a "$LOG_FILE"

# Step 2: Send via AgentMail
echo "📧 Step 2: AgentMail Integration" | tee -a "$LOG_FILE"
python3 bdev_ai_to_agentmail.py 2>&1 | tee -a "$LOG_FILE"

# Step 3: Create summary
echo "📊 Step 3: Pipeline Summary" | tee -a "$LOG_FILE"
echo "Completed: $(date)" | tee -a "$LOG_FILE"

# Count results
AI_OUTPUT=$(ls -t bdev_ai_openclaw_*.csv 2>/dev/null | head -1)
if [ -n "$AI_OUTPUT" ]; then
    MSG_COUNT=$(wc -l < "$AI_OUTPUT" | awk '{print $1-1}')
    echo "AI Messages Generated: $MSG_COUNT" | tee -a "$LOG_FILE"
fi

if [ -f "bdev_ai_agentmail_log.json" ]; then
    LATEST_LOG=$(tail -1 bdev_ai_agentmail_log.json | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'AgentMail Sent: {data["messages_sent"]}')" 2>/dev/null || echo "AgentMail Sent: Check log")
    echo "$LATEST_LOG" | tee -a "$LOG_FILE"
fi

echo "========================================" | tee -a "$LOG_FILE"
echo "Pipeline completed successfully!" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
