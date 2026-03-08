#!/bin/bash
# bdev_ai_gmail_pipeline.sh
# Bdev.ai → Gmail SMTP pipeline (replaces failing AgentMail)

cd /Users/cubiczan/.openclaw/workspace

LOG_DIR="logs/bdev_ai_gmail"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/pipeline_$TIMESTAMP.log"

echo "================================================" | tee -a "$LOG_FILE"
echo "Bdev.ai Gmail SMTP Pipeline" | tee -a "$LOG_FILE"
echo "Started: $(date)" | tee -a "$LOG_FILE"
echo "================================================" | tee -a "$LOG_FILE"

# Step 1: Check Gmail configuration
echo "🔍 Step 1: Checking Gmail configuration..." | tee -a "$LOG_FILE"
python3 -c "
import json
import os
try:
    config_path = 'gmail_config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        accounts = config.get('gmail_accounts', [])
        enabled = [a for a in accounts if a.get('enabled', True)]
        print(f'   Gmail accounts configured: {len(accounts)}')
        print(f'   Gmail accounts enabled: {len(enabled)}')
        for acc in enabled[:3]:  # Show first 3
            email = acc.get('email', 'Unknown')
            # Mask password for security
            pass_len = len(acc.get('password', ''))
            masked_pass = '*' * min(pass_len, 10) if pass_len > 0 else 'NOT SET'
            print(f'   • {acc.get(\"name\", \"Unnamed\")}: {email} (pass: {masked_pass})')
        
        if len(enabled) == 0:
            print('   ⚠️ WARNING: No Gmail accounts enabled!')
        elif any(acc.get('password', '') == 'YOUR_GMAIL_APP_PASSWORD_HERE' for acc in enabled):
            print('   ⚠️ WARNING: Default password detected! Update gmail_config.json')
    else:
        print('   ⚠️ Config file not found: gmail_config.json')
        print('   Creating default configuration...')
        # Create default config
        default_config = {
            'gmail_accounts': [
                {
                    'name': 'Primary',
                    'email': 'sam@cubiczan.com',
                    'password': 'YOUR_GMAIL_APP_PASSWORD_HERE',
                    'smtp_server': 'smtp.gmail.com',
                    'smtp_port': 587,
                    'from_name': 'Sam Desigan',
                    'daily_limit': 500,
                    'enabled': True
                }
            ]
        }
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        print('   ✅ Created default gmail_config.json')
        print('   ⚠️ IMPORTANT: Update with your Gmail App Password')
except Exception as e:
    print(f'   ❌ Error: {e}')
" 2>&1 | tee -a "$LOG_FILE"

# Step 2: Generate AI messages (same as before)
echo "🤖 Step 2: Bdev.ai AI Message Generation" | tee -a "$LOG_FILE"
python3 bdev_ai_openclaw_integration_final.py --batch-size 50 2>&1 | tee -a "$LOG_FILE"

# Step 3: Send via Gmail SMTP
echo "📧 Step 3: Gmail SMTP Integration" | tee -a "$LOG_FILE"
python3 bdev_ai_gmail_sender.py 2>&1 | tee -a "$LOG_FILE"

# Step 4: Create summary
echo "📊 Step 4: Pipeline Summary" | tee -a "$LOG_FILE"

# Count AI messages
AI_OUTPUT=$(ls -t bdev_ai_openclaw_*.csv 2>/dev/null | head -1)
if [ -n "$AI_OUTPUT" ]; then
    MSG_COUNT=$(wc -l < "$AI_OUTPUT" | awk '{print $1-1}')
    echo "AI Messages Generated: $MSG_COUNT" | tee -a "$LOG_FILE"
fi

# Check Gmail logs
if [ -f "bdev_ai_gmail_summary.json" ]; then
    LATEST_LOG=$(tail -1 bdev_ai_gmail_summary.json | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    sent = data['results']['sent']
    total = data['results']['total']
    failed = data['results']['failed']
    skipped = data['results']['skipped']
    
    if total > 0:
        success_rate = (sent/total*100) if total > 0 else 0
        print(f'Gmail Results: {sent}/{total} sent ({success_rate:.1f}%)')
        print(f'              : {failed} failed, {skipped} skipped')
    else:
        print('Gmail Results: No emails processed')
except Exception as e:
    print(f'Gmail Results: Error - {str(e)[:50]}')
" 2>/dev/null)
    echo "$LATEST_LOG" | tee -a "$LOG_FILE"
fi

# Show account usage
echo "👥 Gmail Account Usage:" | tee -a "$LOG_FILE"
python3 -c "
import json
import os
try:
    config_path = 'gmail_config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Check for Gmail usage logs
        import glob
        log_files = glob.glob('bdev_ai_gmail_log_*.json')
        if log_files:
            latest_log = max(log_files, key=lambda x: x.split('_')[-1].split('.')[0])
            with open(latest_log, 'r') as f:
                log_data = json.load(f)
            
            account_usage = log_data.get('account_usage', {})
            if account_usage:
                for acc_name, acc_stats in account_usage.items():
                    today = acc_stats.get('today_count', 0)
                    total = acc_stats.get('total_sent', 0)
                    errors = acc_stats.get('errors', 0)
                    print(f'   {acc_name}: Today: {today}, Total: {total}, Errors: {errors}')
            else:
                print('   No Gmail usage data in log')
        else:
            print('   No Gmail logs yet')
    else:
        print('   No Gmail configuration')
except Exception as e:
    print(f'   Error: {e}')
" 2>&1 | tee -a "$LOG_FILE"

echo "================================================" | tee -a "$LOG_FILE"
echo "Gmail SMTP pipeline completed!" | tee -a "$LOG_FILE"
echo "================================================" | tee -a "$LOG_FILE"