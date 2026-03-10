#!/bin/bash
# setup-docker-monitoring.sh
# Setup cron jobs for Docker system monitoring

set -e

echo "🔧 SETTING UP DOCKER MONITORING CRON JOBS"
echo "=========================================="

# Create directories
mkdir -p ~/.openclaw/workspace/logs/docker-monitor

# Make scripts executable
chmod +x ~/.openclaw/workspace/scripts/docker-health-check.sh
chmod +x ~/.openclaw/workspace/scripts/docker-monitor-cron.sh

echo ""
echo "1. Daily Health Check (8:00 AM):"
CRON_DAILY="0 8 * * * ~/.openclaw/workspace/scripts/docker-health-check.sh >> ~/.openclaw/workspace/logs/docker-monitor/daily-\$(date +\%Y\%m\%d).log 2>&1"
echo "   $CRON_DAILY"

echo ""
echo "2. Weekly Summary (Monday 9:00 AM):"
CRON_WEEKLY="0 9 * * 1 ~/.openclaw/workspace/scripts/docker-monitor-cron.sh"
echo "   $CRON_WEEKLY"

echo ""
echo "3. Disk Cleanup (1st of month, 2:00 AM):"
CRON_CLEANUP="0 2 1 * * docker system prune -a --volumes --force >> ~/.openclaw/workspace/logs/docker-monitor/cleanup-\$(date +\%Y\%m\%d).log 2>&1"
echo "   $CRON_CLEANUP"

echo ""
echo "📋 TO ADD THESE TO CRONTAB:"
echo "============================"
echo "1. Edit crontab:"
echo "   crontab -e"
echo ""
echo "2. Add these lines:"
echo ""
echo "# Docker Monitoring"
echo "0 8 * * * ~/.openclaw/workspace/scripts/docker-health-check.sh >> ~/.openclaw/workspace/logs/docker-monitor/daily-\$(date +\\%Y\\%m\\%d).log 2>&1"
echo "0 9 * * 1 ~/.openclaw/workspace/scripts/docker-monitor-cron.sh"
echo "0 2 1 * * docker system prune -a --volumes --force >> ~/.openclaw/workspace/logs/docker-monitor/cleanup-\$(date +\\%Y\\%m\\%d).log 2>&1"
echo ""
echo "3. Save and exit"
echo ""
echo "📊 MONITORING OUTPUT:"
echo "===================="
echo "Logs will be saved to:"
echo "  ~/.openclaw/workspace/logs/docker-monitor/"
echo ""
echo "Files:"
echo "  - daily-YYYYMMDD.log    (Daily health checks)"
echo "  - docker-monitor-*.log  (Weekly monitor logs)"
echo "  - cleanup-YYYYMMDD.log  (Monthly cleanup logs)"
echo ""
echo "🔍 MANUAL TESTING:"
echo "================="
echo "Test health check:"
echo "  ~/.openclaw/workspace/scripts/docker-health-check.sh"
echo ""
echo "Test monitor script:"
echo "  ~/.openclaw/workspace/scripts/docker-monitor-cron.sh"
echo ""
echo "Check logs:"
echo "  ls -la ~/.openclaw/workspace/logs/docker-monitor/"
echo ""
echo "🎯 NEXT STEPS:"
echo "=============="
echo "1. Review the cron jobs above"
echo "2. Add to crontab if desired"
echo "3. Test manually first"
echo "4. Monitor logs for issues"
echo ""
echo "⚠️  NOTE:"
echo "========"
echo "These cron jobs are optional but recommended for"
echo "maintaining a healthy Docker system. They provide:"
echo "- Daily health monitoring"
echo "- Weekly performance tracking"
echo "- Monthly cleanup automation"
echo ""
echo "For Firecracker monitoring (future):"
echo "See FIRECRACKER_READINESS.md for research status"