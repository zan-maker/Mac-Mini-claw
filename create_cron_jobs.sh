#!/bin/bash

# Create cron jobs for Skill Evolution Framework

echo "Creating Skill Evolution Cron Jobs..."

# Add to crontab
(crontab -l 2>/dev/null; echo "") | crontab -
(crontab -l 2>/dev/null; echo "# =================================================") | crontab -
(crontab -l 2>/dev/null; echo "# SKILL EVOLUTION FRAMEWORK - AUTONOMOUS IMPROVEMENT") | crontab -
(crontab -l 2>/dev/null; echo "# =================================================") | crontab -
(crontab -l 2>/dev/null; echo "") | crontab -
(crontab -l 2>/dev/null; echo "# Daily: Trade Recommender evolution (2 AM)") | crontab -
(crontab -l 2>/dev/null; echo "0 2 * * * cd /Users/cubiczan/.openclaw/workspace && python3 skill-evolution/evolve_trade_recommender.py >> ~/.openclaw/logs/evolution_trade.log 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "") | crontab -
(crontab -l 2>/dev/null; echo "# Weekly: ROI Analyst evolution (3 AM Monday)") | crontab -
(crontab -l 2>/dev/null; echo "0 3 * * 1 cd /Users/cubiczan/.openclaw/workspace && python3 skill-evolution/evolve_roi_analyst.py >> ~/.openclaw/logs/evolution_roi.log 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "") | crontab -
(crontab -l 2>/dev/null; echo "# Daily: Lead Generator evolution (4 AM)") | crontab -
(crontab -l 2>/dev/null; echo "0 4 * * * cd /Users/cubiczan/.openclaw/workspace && python3 skill-evolution/evolve_lead_generator.py >> ~/.openclaw/logs/evolution_lead.log 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "") | crontab -
(crontab -l 2>/dev/null; echo "# Weekly: Cross-agent pattern sharing (5 AM Sunday)") | crontab -
(crontab -l 2>/dev/null; echo "0 5 * * 0 cd /Users/cubiczan/.openclaw/workspace && python3 skill-evolution/share_patterns_across_agents.py >> ~/.openclaw/logs/evolution_sharing.log 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "") | crontab -
(crontab -l 2>/dev/null; echo "# Weekly: Evolution progress report (6 AM Monday)") | crontab -
(crontab -l 2>/dev/null; echo "0 6 * * 1 cd /Users/cubiczan/.openclaw/workspace && python3 skill-evolution/generate_evolution_report.py >> ~/.openclaw/logs/evolution_report.log 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "") | crontab -
(crontab -l 2>/dev/null; echo "# =================================================") | crontab -

echo "✅ Cron jobs created successfully!"
echo ""
echo "📅 Schedule Summary:"
echo "  2 AM Daily    - Trade Recommender evolution"
echo "  3 AM Monday   - ROI Analyst evolution"
echo "  4 AM Daily    - Lead Generator evolution"
echo "  5 AM Sunday   - Cross-agent pattern sharing"
echo "  6 AM Monday   - Weekly evolution report"
echo ""
echo "📁 Log files will be saved to ~/.openclaw/logs/"
