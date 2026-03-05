#!/bin/bash
# Setup Gas Tracking Cron Jobs

echo "⛽ Setting up Gas Tracking Cron Jobs..."
echo "=========================================="

# Create log directory
mkdir -p /Users/cubiczan/.openclaw/workspace/logs
mkdir -p /Users/cubiczan/.openclaw/workspace/gas_tracking

# Add gas tracking cron jobs
echo "Adding gas tracking cron jobs..."

# Morning check (9:00 AM)
(crontab -l 2>/dev/null | grep -v "gas-position-tracker.py.*morning"; echo "0 9 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/gas-position-tracker.py >> /Users/cubiczan/.openclaw/workspace/logs/gas_morning.log 2>&1") | crontab -

# Midday check (1:00 PM)
(crontab -l 2>/dev/null | grep -v "gas-position-tracker.py.*midday"; echo "0 13 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/gas-position-tracker.py >> /Users/cubiczan/.openclaw/workspace/logs/gas_midday.log 2>&1") | crontab -

# Evening check (5:00 PM)
(crontab -l 2>/dev/null | grep -v "gas-position-tracker.py.*evening"; echo "0 17 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/gas-position-tracker.py >> /Users/cubiczan/.openclaw/workspace/logs/gas_evening.log 2>&1") | crontab -

# Knowledge Graph update (8:00 AM daily)
(crontab -l 2>/dev/null | grep -v "kalshi-knowledge-graph-simple.py"; echo "0 8 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/kalshi-knowledge-graph-simple.py >> /Users/cubiczan/.openclaw/workspace/logs/knowledge_graph.log 2>&1") | crontab -

# Portfolio summary (6:00 PM daily)
(crontab -l 2>/dev/null | grep -v "kalshi-portfolio-summary.py"; echo "0 18 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/kalshi-portfolio-summary.py >> /Users/cubiczan/.openclaw/workspace/logs/portfolio_summary.log 2>&1") | crontab -

echo "✅ Gas tracking cron jobs added!"
echo ""
echo "📅 Schedule:"
echo "  • 8:00 AM - Knowledge Graph Update"
echo "  • 9:00 AM - Gas Morning Check"
echo "  • 1:00 PM - Gas Midday Check"
echo "  • 5:00 PM - Gas Evening Check"
echo "  • 6:00 PM - Portfolio Summary"
echo ""
echo "📁 Logs will be saved to:"
echo "  /Users/cubiczan/.openclaw/workspace/logs/"
echo "  /Users/cubiczan/.openclaw/workspace/gas_tracking/"
echo ""
echo "To view all cron jobs: crontab -l"
echo "To edit cron jobs: crontab -e"