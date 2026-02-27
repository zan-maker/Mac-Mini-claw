#!/bin/bash
# Setup Craigslist referral fee cron jobs

echo "========================================="
echo "CRAIGSLIST REFERRAL FEE CRON SETUP"
echo "========================================="
echo ""

# Check if running as correct user
CURRENT_USER=$(whoami)
EXPECTED_USER="cubiczan"

if [ "$CURRENT_USER" != "$EXPECTED_USER" ]; then
    echo "⚠️  Warning: Running as $CURRENT_USER, expected $EXPECTED_USER"
    echo "   Some paths may not work correctly."
    echo ""
fi

# Create log directory
LOG_DIR="/Users/cubiczan/.openclaw/workspace/craigslist-leads/logs"
echo "Creating log directory: $LOG_DIR"
mkdir -p "$LOG_DIR"

# Make scripts executable
echo ""
echo "Making scripts executable..."
chmod +x /Users/cubiczan/.openclaw/workspace/scripts/*.sh

# Check current crontab
echo ""
echo "Current crontab:"
crontab -l 2>/dev/null | grep -v "^#" | head -10 || echo "  (empty)"

# Add Craigslist cron jobs
echo ""
echo "Adding Craigslist cron jobs..."

# Remove any existing Craigslist jobs
TEMP_CRON=$(mktemp)
crontab -l 2>/dev/null | grep -v "Craigslist" | grep -v "run_craigslist" > "$TEMP_CRON"

# Add new jobs
echo "# =========================================" >> "$TEMP_CRON"
echo "# CRAIGSLIST REFERRAL FEE SYSTEM" >> "$TEMP_CRON"
echo "# =========================================" >> "$TEMP_CRON"
echo "# Morning scraper - 9:00 AM daily" >> "$TEMP_CRON"
echo "0 9 * * * /Users/cubiczan/.openclaw/workspace/scripts/run_craigslist_scraper.sh >> $LOG_DIR/scraper.log 2>&1" >> "$TEMP_CRON"
echo "" >> "$TEMP_CRON"
echo "# Afternoon processor - 2:00 PM daily" >> "$TEMP_CRON"
echo "0 14 * * * /Users/cubiczan/.openclaw/workspace/scripts/run_lead_processor.sh >> $LOG_DIR/processor.log 2>&1" >> "$TEMP_CRON"
echo "" >> "$TEMP_CRON"
echo "# Weekly cleanup - Sunday at 3:00 AM" >> "$TEMP_CRON"
echo "0 3 * * 0 find /Users/cubiczan/.openclaw/workspace/craigslist-leads -name '*.log' -mtime +30 -delete" >> "$TEMP_CRON"

# Install new crontab
crontab "$TEMP_CRON"
rm "$TEMP_CRON"

echo "✅ Cron jobs added successfully!"
echo ""

# Show new crontab
echo "Updated crontab (Craigslist jobs only):"
crontab -l | grep -A5 "CRAIGSLIST"

echo ""
echo "========================================="
echo "SETUP COMPLETE"
echo "========================================="
echo ""
echo "📅 Scheduled Jobs:"
echo "  • 9:00 AM  - Craigslist scraper (find opportunities)"
echo "  • 2:00 PM  - Lead processor (send outreach emails)"
echo "  • 3:00 AM Sun - Log cleanup (30+ day logs)"
echo ""
echo "📁 Logs will be saved to:"
echo "  $LOG_DIR/scraper.log"
echo "  $LOG_DIR/processor.log"
echo ""
echo "🔧 To test manually:"
echo "  cd /Users/cubiczan/.openclaw/workspace"
echo "  ./scripts/run_craigslist_scraper.sh"
echo "  ./scripts/run_lead_processor.sh"
echo ""
echo "📊 To monitor:"
echo "  tail -f $LOG_DIR/scraper.log"
echo "  tail -f $LOG_DIR/processor.log"
echo ""
echo "❌ To remove cron jobs:"
echo "  crontab -e"
echo "  (delete the Craigslist section)"
echo ""
echo "========================================="