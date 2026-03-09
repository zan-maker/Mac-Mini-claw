#!/bin/bash
# Kalshi Profit Cron Job Setup
# Creates immediate profit-generating cron jobs

echo "🎯 KALSHI PROFIT CRON JOB SETUP"
echo "================================"
echo ""

WORKSPACE="/Users/cubiczan/.openclaw/workspace"
LOGS_DIR="$WORKSPACE/logs/kalshi"
mkdir -p "$LOGS_DIR"

echo "📁 Creating log directory: $LOGS_DIR"
echo ""

# Create the cron jobs
CRON_JOBS=""

# 1. Premarket Scan (7:00 AM EST) - Before market open
CRON_JOBS+="0 7 * * * cd $WORKSPACE && python3 scripts/kalshi-profit-scanner-secure.py --time premarket >> $LOGS_DIR/premarket-\$(date +\%Y\%m\%d).log 2>&1\n"

# 2. Morning Scan (9:00 AM EST) - After market open
CRON_JOBS+="0 9 * * * cd $WORKSPACE && python3 scripts/kalshi-profit-scanner-secure.py --time morning >> $LOGS_DIR/morning-\$(date +\%Y\%m\%d).log 2>&1\n"

# 3. Midday Scan (1:00 PM EST) - Lunchtime opportunities
CRON_JOBS+="0 13 * * * cd $WORKSPACE && python3 scripts/kalshi-profit-scanner-secure.py --time midday >> $LOGS_DIR/midday-\$(date +\%Y\%m\%d).log 2>&1\n"

# 4. Afternoon Scan (3:00 PM EST) - Late day moves
CRON_JOBS+="0 15 * * * cd $WORKSPACE && python3 scripts/kalshi-profit-scanner-secure.py --time afternoon >> $LOGS_DIR/afternoon-\$(date +\%Y\%m\%d).log 2>&1\n"

# 5. Postmarket Scan (5:00 PM EST) - After close analysis
CRON_JOBS+="0 17 * * * cd $WORKSPACE && python3 scripts/kalshi-profit-scanner-secure.py --time postmarket >> $LOGS_DIR/postmarket-\$(date +\%Y\%m\%d).log 2>&1\n"

# 6. Evening Scan (8:00 PM EST) - Overnight opportunities
CRON_JOBS+="0 20 * * * cd $WORKSPACE && python3 scripts/kalshi-profit-scanner-secure.py --time evening >> $LOGS_DIR/evening-\$(date +\%Y\%m\%d).log 2>&1\n"

# 7. Daily Profit Summary (6:00 PM EST)
CRON_JOBS+="0 18 * * * cd $WORKSPACE && python3 scripts/kalshi-portfolio-summary.py >> $LOGS_DIR/summary-\$(date +\%Y\%m\%d).log 2>&1\n"

echo "📋 CRON JOBS TO BE ADDED:"
echo "-------------------------"
echo -e "$CRON_JOBS"
echo ""

# Add to crontab
echo "➕ Adding to crontab..."
(crontab -l 2>/dev/null; echo -e "$CRON_JOBS") | crontab -

if [ $? -eq 0 ]; then
    echo "✅ Cron jobs added successfully!"
    echo ""
    
    echo "⏰ SCHEDULE (EST):"
    echo "----------------"
    echo "7:00 AM  - Premarket scan"
    echo "9:00 AM  - Morning scan"
    echo "1:00 PM  - Midday scan"
    echo "3:00 PM  - Afternoon scan"
    echo "5:00 PM  - Postmarket scan"
    echo "8:00 PM  - Evening scan"
    echo "6:00 PM  - Daily profit summary"
    echo ""
    
    echo "📊 EXPECTED RESULTS:"
    echo "------------------"
    echo "• 6 scans per day"
    echo "• Real-time opportunity detection"
    echo "• Daily profit tracking"
    echo "• Immediate trade execution"
    echo ""
    
    echo "🔧 NEXT STEPS:"
    echo "-------------"
    echo "1. Add your API keys to .env file:"
    echo "   NEWS_API_KEY=your_key"
    echo "   SERPER_API_KEY=your_key"
    echo "2. Test the scanner:"
    echo "   python3 scripts/kalshi-profit-scanner-secure.py"
    echo "3. Monitor logs:"
    echo "   tail -f $LOGS_DIR/*.log"
    echo ""
    
    echo "💰 IMMEDIATE PROFIT FOCUS ACTIVATED!"
    
else
    echo "❌ Failed to add cron jobs"
    exit 1
fi