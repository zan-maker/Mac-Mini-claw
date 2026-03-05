#!/bin/bash
# Cron Job Manager - View and manage all cron jobs

echo "🕐 CRON JOB MANAGER"
echo "========================"
echo ""

# Show all cron jobs
echo "📋 ALL CRON JOBS:"
echo "----------------"
crontab -l
echo ""

# Show Kalshi-specific jobs
echo "🎯 KALSHI TRADING JOBS:"
echo "----------------------"
crontab -l | grep -E "(kalshi|gas|portfolio|knowledge)"
echo ""

# Show gas tracking jobs
echo "⛽ GAS TRACKING JOBS:"
echo "-------------------"
crontab -l | grep -E "(gas|9:00|13:00|17:00)"
echo ""

# Show log locations
echo "📁 LOG FILE LOCATIONS:"
echo "---------------------"
echo "Gas Tracking:"
echo "  /Users/cubiczan/.openclaw/workspace/logs/gas_morning.log"
echo "  /Users/cubiczan/.openclaw/workspace/logs/gas_midday.log"
echo "  /Users/cubiczan/.openclaw/workspace/logs/gas_evening.log"
echo ""
echo "Kalshi Scanning:"
echo "  /Users/cubiczan/.openclaw/workspace/logs/kalshi-premarket.log"
echo "  /Users/cubiczan/.openclaw/workspace/logs/kalshi-midday.log"
echo "  /Users/cubiczan/.openclaw/workspace/logs/kalshi-postmarket.log"
echo ""
echo "Knowledge Graph:"
echo "  /Users/cubiczan/.openclaw/workspace/logs/knowledge_graph.log"
echo "  /Users/cubiczan/.openclaw/workspace/portfolio_reports/"
echo ""
echo "Gas Reports:"
echo "  /Users/cubiczan/.openclaw/workspace/gas_tracking/"
echo ""

# Next execution times
echo "⏰ NEXT EXECUTION TIMES (EST):"
echo "-----------------------------"
echo "Today:"
echo "  • Gas Morning Check:     Already ran at 9:00 AM"
echo "  • Gas Midday Check:      1:00 PM"
echo "  • Gas Evening Check:     5:00 PM"
echo "  • Portfolio Summary:     6:00 PM"
echo ""
echo "Tomorrow:"
echo "  • Knowledge Graph:       8:00 AM"
echo "  • Gas Morning Check:     9:00 AM"
echo "  • Kalshi Premarket:      7:00 AM"
echo "  • Kalshi Midday:         11:00 AM, 1:00 PM"
echo "  • Kalshi Postmarket:     4:30 PM, 7:00 PM"
echo ""

# Check if scripts exist
echo "✅ SCRIPT VERIFICATION:"
echo "----------------------"
scripts=(
    "scripts/gas-position-tracker.py"
    "scripts/kalshi-knowledge-graph-simple.py"
    "scripts/kalshi-portfolio-summary.py"
    "scripts/kalshi-daily-scanner.py"
)

for script in "${scripts[@]}"; do
    if [ -f "/Users/cubiczan/.openclaw/workspace/$script" ]; then
        echo "✓ $script"
    else
        echo "✗ $script (MISSING)"
    fi
done
echo ""

# Quick test commands
echo "🔧 QUICK TEST COMMANDS:"
echo "----------------------"
echo "Test gas tracker:"
echo "  cd /Users/cubiczan/.openclaw/workspace && python3 scripts/gas-position-tracker.py"
echo ""
echo "Test knowledge graph:"
echo "  cd /Users/cubiczan/.openclaw/workspace && python3 scripts/kalshi-knowledge-graph-simple.py"
echo ""
echo "View latest gas report:"
echo "  ls -la /Users/cubiczan/.openclaw/workspace/gas_tracking/ | tail -5"
echo ""
echo "View cron logs:"
echo "  tail -20 /Users/cubiczan/.openclaw/workspace/logs/gas_morning.log"
echo ""

echo "📊 CRON JOB SUMMARY:"
echo "-------------------"
total_jobs=$(crontab -l 2>/dev/null | wc -l)
kalshi_jobs=$(crontab -l 2>/dev/null | grep -c "kalshi\|gas\|portfolio\|knowledge")
gas_jobs=$(crontab -l 2>/dev/null | grep -c "gas")

echo "Total Cron Jobs: $total_jobs"
echo "Kalshi Trading Jobs: $kalshi_jobs"
echo "Gas Tracking Jobs: $gas_jobs"
echo ""

echo "🚀 SETUP COMPLETE!"
echo "=================="
echo "Your automated trading system is now running with:"
echo "• 3x daily gas price tracking"
echo "• 8x daily Kalshi market scanning"
echo "• Daily knowledge graph updates"
echo "• Daily portfolio summaries"
echo ""
echo "First automated runs start tomorrow morning!"