#!/bin/bash
# War Crude Monitor Cron Setup
# Sets up continuous monitoring of crude/gasoline prices for Kalshi trading

echo "🛢️  WAR CRUDE MONITOR CRON SETUP"
echo "================================"
echo ""

WORKSPACE="/Users/cubiczan/.openclaw/workspace"
WAR_LOGS="$WORKSPACE/logs/war_monitor"
mkdir -p "$WAR_LOGS"

echo "📁 Creating log directory: $WAR_LOGS"
echo ""

# Make script executable
chmod +x "$WORKSPACE/scripts/war-crude-monitor.py"

# Create cron jobs for continuous monitoring
WAR_CRON_JOBS=""

# During trading hours - intensive monitoring
# 8:00 AM EST - Pre-market check
WAR_CRON_JOBS+="0 8 * * * cd $WORKSPACE && source .env && python3 scripts/war-crude-monitor.py >> $WAR_LOGS/morning-\$(date +\%Y\%m\%d).log 2>&1\n"

# Every 2 hours during day (10, 12, 14, 16, 18 EST)
WAR_CRON_JOBS+="0 10 * * * cd $WORKSPACE && source .env && python3 scripts/war-crude-monitor.py >> $WAR_LOGS/midmorning-\$(date +\%Y\%m\%d).log 2>&1\n"
WAR_CRON_JOBS+="0 12 * * * cd $WORKSPACE && source .env && python3 scripts/war-crude-monitor.py >> $WAR_LOGS/noon-\$(date +\%Y\%m\%d).log 2>&1\n"
WAR_CRON_JOBS+="0 14 * * * cd $WORKSPACE && source .env && python3 scripts/war-crude-monitor.py >> $WAR_LOGS/afternoon-\$(date +\%Y\%m\%d).log 2>&1\n"
WAR_CRON_JOBS+="0 16 * * * cd $WORKSPACE && source .env && python3 scripts/war-crude-monitor.py >> $WAR_LOGS/late-\$(date +\%Y\%m\%d).log 2>&1\n"
WAR_CRON_JOBS+="0 18 * * * cd $WORKSPACE && source .env && python3 scripts/war-crude-monitor.py >> $WAR_LOGS/evening-\$(date +\%Y\%m\%d).log 2>&1\n"

# Evening check for overnight developments
WAR_CRON_JOBS+="0 22 * * * cd $WORKSPACE && source .env && python3 scripts/war-crude-monitor.py >> $WAR_LOGS/night-\$(date +\%Y\%m\%d).log 2>&1\n"

# Early morning check for Asian/European market moves
WAR_CRON_JOBS+="0 2 * * * cd $WORKSPACE && source .env && python3 scripts/war-crude-monitor.py >> $WAR_LOGS/overnight-\$(date +\%Y\%m\%d).log 2>&1\n"

# Emergency alert script (runs every 30 minutes during volatility)
WAR_CRON_JOBS+="*/30 8-20 * * * cd $WORKSPACE && source .env && python3 scripts/war-crude-monitor.py --quick >> $WAR_LOGS/alert-\$(date +\%Y\%m\%d_\%H\%M).log 2>&1\n"

echo "📋 WAR MONITOR CRON JOBS:"
echo "------------------------"
echo -e "$WAR_CRON_JOBS"
echo ""

# Add to crontab
echo "➕ Adding war monitor to crontab..."
(crontab -l 2>/dev/null; echo -e "$WAR_CRON_JOBS") | crontab -

if [ $? -eq 0 ]; then
    echo "✅ War monitor cron jobs added!"
    echo ""
    
    echo "⏰ CONTINUOUS MONITORING SCHEDULE (EST):"
    echo "--------------------------------------"
    echo "2:00 AM  - Overnight market check"
    echo "8:00 AM  - Pre-market analysis"
    echo "10:00 AM - Morning update"
    echo "12:00 PM - Noon check"
    echo "2:00 PM  - Afternoon update"
    echo "4:00 PM  - Late afternoon"
    echo "6:00 PM  - Evening summary"
    echo "10:00 PM - Night check"
    echo ""
    echo "🚨 EMERGENCY ALERTS: Every 30 minutes 8AM-8PM"
    echo ""
    
    echo "🎯 MONITORING FOCUS:"
    echo "------------------"
    echo "• Crude oil price movements (WTI, Brent)"
    echo "• Gasoline/RBOB futures"
    echo "• Geopolitical news (war, conflicts, sanctions)"
    echo "• OPEC announcements"
    echo "• Refinery disruptions"
    echo "• Inventory reports"
    echo ""
    
    echo "💰 KALSHI OPPORTUNITY TYPES:"
    echo "---------------------------"
    echo "1. Gasoline price thresholds (>$2.75, >$3.00, etc.)"
    echo "2. Crude oil price levels ($80, $85, $90 barriers)"
    echo "3. Volatility spikes from news events"
    echo "4. Inventory report binary outcomes"
    echo "5. OPEC meeting decisions"
    echo ""
    
    echo "🔧 TEST THE MONITOR:"
    echo "------------------"
    echo "cd $WORKSPACE"
    echo "source .env"
    echo "python3 scripts/war-crude-monitor.py"
    echo ""
    
    echo "📊 EXPECTED OUTPUT:"
    echo "-----------------"
    echo "• Current crude/gasoline prices"
    echo "• Volatility assessment"
    echo "• Kalshi trading recommendations"
    echo "• High-impact news alerts"
    echo "• Confidence scores for each opportunity"
    echo ""
    
    echo "🚨 WAR-DRIVEN VOLATILITY ADVANTAGE:"
    echo "---------------------------------"
    echo "Geopolitical tensions create:"
    echo "• Higher volatility = More trading opportunities"
    echo "• Clearer binary outcomes (prices spike or crash)"
    echo "• News-driven momentum (easy to track catalysts)"
    echo "• Emotional trading = Inefficiencies to exploit"
    echo ""
    
    echo "🛢️  WAR CRUDE MONITOR ACTIVATED!"
    echo "================================"
    
else
    echo "❌ Failed to add war monitor cron jobs"
    exit 1
fi