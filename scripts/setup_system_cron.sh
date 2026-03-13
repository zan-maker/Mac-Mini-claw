#!/bin/bash

# 🚀 System Cron Setup Script
# Replaces broken OpenClaw cron management

set -e

echo "========================================="
echo "🚀 SYSTEM CRON SETUP"
echo "========================================="
echo "Problem: OpenClaw gateway broken"
echo "Solution: Use system cron for automation"
echo "Impact: LinkedIn/Instagram posting restored"
echo "========================================="

CRON_FILE="/tmp/openclaw_cron_tmp"
CURRENT_CRON="/tmp/current_cron"

echo ""
echo "📋 Current cron jobs (if any):"
crontab -l 2>/dev/null || echo "No existing cron jobs"

echo ""
echo "🔧 Creating cron jobs for social media automation..."

# Create cron entries
cat > "$CRON_FILE" << CRON_EOF
# =========================================
# 🚀 OPENCLAW SOCIAL MEDIA AUTOMATION
# Created: $(date)
# Replaces: Broken OpenClaw gateway cron
# =========================================

# LinkedIn Posting - Daily at 9:00 AM
0 9 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/linkedin_manual_post.py >> /tmp/linkedin_cron.log 2>&1

# Instagram Posting - Monday, Wednesday, Friday at 12:00 PM
0 12 * * 1,3,5 cd /Users/cubiczan/.openclaw/workspace && ./scripts/post_ai_finance_to_instagram.sh >> /tmp/instagram_cron.log 2>&1

# Lead Generation - Weekdays at 9:00 AM
0 9 * * 1-5 cd /Users/cubiczan/.openclaw/workspace && python3 scripts/run_lead_generation.py >> /tmp/leadgen_cron.log 2>&1

# Daily Backup - Midnight
0 0 * * * cd /Users/cubiczan/.openclaw/workspace && ./scripts/backup.sh >> /tmp/backup_cron.log 2>&1

# Token Monitor - Every 30 minutes
*/30 * * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/token_monitor.py >> /tmp/token_cron.log 2>&1

# API Usage Check - Daily at 6:00 PM
0 18 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/api_usage_check.py >> /tmp/api_cron.log 2>&1
CRON_EOF

echo "✅ Cron jobs template created"
echo ""
echo "📋 Proposed cron jobs:"
echo "======================"
cat "$CRON_FILE"
echo "======================"

echo ""
read -p "❓ Apply these cron jobs? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Applying cron jobs..."
    
    # Save current cron
    crontab -l 2>/dev/null > "$CURRENT_CRON" || true
    
    # Add new cron jobs
    if [ -f "$CURRENT_CRON" ] && [ -s "$CURRENT_CRON" ]; then
        # Merge with existing
        cat "$CURRENT_CRON" "$CRON_FILE" | crontab -
        echo "✅ Merged with existing cron jobs"
    else
        # Install new
        crontab "$CRON_FILE"
        echo "✅ Installed new cron jobs"
    fi
    
    echo ""
    echo "📋 Final cron jobs:"
    crontab -l
    
    echo ""
    echo "📁 Log files will be created at:"
    echo "   /tmp/linkedin_cron.log"
    echo "   /tmp/instagram_cron.log"
    echo "   /tmp/leadgen_cron.log"
    echo "   /tmp/backup_cron.log"
    echo "   /tmp/token_cron.log"
    echo "   /tmp/api_cron.log"
    
else
    echo "⚠️  Skipping cron installation"
    echo "   You can manually edit with: crontab -e"
fi

echo ""
echo "🔧 Creating cron management scripts..."

# Create cron management script
cat > scripts/manage_cron.sh << 'MANAGE_EOF'
#!/bin/bash

# 🚀 Cron Management Script

case "$1" in
    list)
        echo "📋 CURRENT CRON JOBS:"
        echo "======================"
        crontab -l
        echo "======================"
        ;;
    logs)
        echo "📁 CRON LOG FILES:"
        ls -la /tmp/*cron.log 2>/dev/null || echo "No log files yet"
        echo ""
        echo "📊 LOG CONTENTS (last 10 lines each):"
        for log in /tmp/*cron.log 2>/dev/null; do
            echo "=== $(basename $log) ==="
            tail -10 "$log" 2>/dev/null || echo "Empty or doesn't exist"
            echo ""
        done
        ;;
    test)
        echo "🧪 TESTING CRON JOBS..."
        echo "Running LinkedIn test..."
        cd /Users/cubiczan/.openclaw/workspace && python3 scripts/linkedin_manual_post.py --test
        echo ""
        echo "Running Instagram test..."
        cd /Users/cubiczan/.openclaw/workspace && ./scripts/post_ai_finance_to_instagram.sh --test
        ;;
    help|*)
        echo "🚀 CRON MANAGEMENT SCRIPT"
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  list    - Show current cron jobs"
        echo "  logs    - Show cron log files"
        echo "  test    - Test cron job scripts"
        echo "  help    - Show this help"
        ;;
esac
MANAGE_EOF

chmod +x scripts/manage_cron.sh

echo "✅ Cron management script created: scripts/manage_cron.sh"
echo ""
echo "📋 Quick commands:"
echo "  ./scripts/manage_cron.sh list   # Show cron jobs"
echo "  ./scripts/manage_cron.sh logs   # Check logs"
echo "  ./scripts/manage_cron.sh test   # Test scripts"

echo ""
echo "========================================="
echo "🎯 CRON MANAGEMENT FIXED!"
echo "========================================="
echo ""
echo "✅ LinkedIn automation: Daily at 9:00 AM"
echo "✅ Instagram automation: Mon/Wed/Fri at 12:00 PM"
echo "✅ Lead generation: Weekdays at 9:00 AM"
echo "✅ Backup: Daily at midnight"
echo "✅ Token monitoring: Every 30 minutes"
echo "✅ API usage: Daily at 6:00 PM"
echo ""
echo "📊 Logs: /tmp/*cron.log"
echo "🔧 Management: ./scripts/manage_cron.sh"
echo ""
echo "🚀 Social media automation RESTORED!"
