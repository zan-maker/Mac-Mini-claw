#!/bin/bash
# bdev_ai_advanced_pipeline.sh
# Advanced Bdev.ai → AgentMail pipeline with multiple accounts

cd /Users/cubiczan/.openclaw/workspace

LOG_DIR="logs/bdev_ai_advanced"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/pipeline_$TIMESTAMP.log"

echo "================================================" | tee -a "$LOG_FILE"
echo "Bdev.ai Advanced Pipeline" | tee -a "$LOG_FILE"
echo "Started: $(date)" | tee -a "$LOG_FILE"
echo "================================================" | tee -a "$LOG_FILE"

# Step 1: Check AgentMail accounts
echo "🔍 Step 1: Checking AgentMail accounts..." | tee -a "$LOG_FILE"
python3 -c "
import json
try:
    with open('agentmail_config.json', 'r') as f:
        config = json.load(f)
    enabled = [a for a in config['agentmail_accounts'] if a['enabled']]
    print(f'   Accounts configured: {len(config[\"agentmail_accounts\"])}')
    print(f'   Accounts enabled: {len(enabled)}')
    for acc in enabled:
        print(f'   • {acc[\"name\"]}: {acc[\"from_email\"]}')
except Exception as e:
    print(f'   ❌ Error: {e}')
" 2>&1 | tee -a "$LOG_FILE"

# Step 2: Generate AI messages
echo "🤖 Step 2: Bdev.ai AI Message Generation" | tee -a "$LOG_FILE"
python3 bdev_ai_openclaw_integration_final.py --batch-size 50 2>&1 | tee -a "$LOG_FILE"

# Step 3: Send via AgentMail (advanced)
echo "📧 Step 3: Advanced AgentMail Integration" | tee -a "$LOG_FILE"
python3 bdev_ai_agentmail_advanced.py --limit 50 2>&1 | tee -a "$LOG_FILE"

# Step 4: Create summary
echo "📊 Step 4: Pipeline Summary" | tee -a "$LOG_FILE"

# Count AI messages
AI_OUTPUT=$(ls -t bdev_ai_openclaw_*.csv 2>/dev/null | head -1)
if [ -n "$AI_OUTPUT" ]; then
    MSG_COUNT=$(wc -l < "$AI_OUTPUT" | awk '{print $1-1}')
    echo "AI Messages Generated: $MSG_COUNT" | tee -a "$LOG_FILE"
fi

# Check AgentMail logs
if [ -f "bdev_ai_agentmail_summary.json" ]; then
    LATEST_LOG=$(tail -1 bdev_ai_agentmail_summary.json | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    sent = data['results']['sent']
    total = data['results']['total']
    print(f'AgentMail Results: {sent}/{total} sent ({sent/total*100:.1f}%)')
except:
    print('AgentMail Results: Check log')
" 2>/dev/null)
    echo "$LATEST_LOG" | tee -a "$LOG_FILE"
fi

# Show account usage
echo "👥 Account Usage:" | tee -a "$LOG_FILE"
python3 -c "
import json
try:
    with open('agentmail_config.json', 'r') as f:
        config = json.load(f)
    
    # Check for usage logs
    import glob
    log_files = glob.glob('bdev_ai_agentmail_log_*.json')
    if log_files:
        latest_log = max(log_files, key=lambda x: x.split('_')[-1].split('.')[0])
        with open(latest_log, 'r') as f:
            log_data = json.load(f)
        
        stats = log_data.get('stats', {})
        if 'accounts' in stats:
            for acc_name, acc_stats in stats['accounts'].items():
                today = acc_stats.get('today', 0)
                limit = acc_stats.get('limit', 1000)
                pct = (today/limit*100) if limit > 0 else 0
                print(f'   {acc_name}: {today}/{limit} ({pct:.1f}%)')
    else:
        print('   No usage data yet')
except Exception as e:
    print(f'   Error: {e}')
" 2>&1 | tee -a "$LOG_FILE"

echo "================================================" | tee -a "$LOG_FILE"
echo "Advanced pipeline completed!" | tee -a "$LOG_FILE"
echo "================================================" | tee -a "$LOG_FILE"