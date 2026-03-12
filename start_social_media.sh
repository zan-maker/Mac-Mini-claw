#!/bin/bash
# Quick Start Script for Social Media Outreach

echo "🚀 SOCIAL MEDIA OUTREACH QUICK START"
echo "========================================"

# Check prerequisites
echo "1. Checking prerequisites..."
if ! command -v pinchtab &> /dev/null; then
    echo "❌ Pinchtab not installed"
    echo "   Install with: curl -fsSL https://pinchtab.com/install.sh | sh"
    exit 1
fi

if ! curl -s http://localhost:9867/health &> /dev/null; then
    echo "⚠️  Pinchtab server not running"
    echo "   Start with: pinchtab start"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Generate strategy
echo "2. Generating weekly strategy..."
python3 /Users/cubiczan/.openclaw/workspace/scripts/social_media_orchestrator.py

# Check content calendar
echo "3. Checking content calendar..."
if [ -f "/Users/cubiczan/.openclaw/workspace/social_media_outreach/content_calendar_*.json" ]; then
    echo "✅ Content calendar generated"
else
    echo "❌ Content calendar not found"
    exit 1
fi

# Test automation
echo "4. Testing automation..."
python3 /Users/cubiczan/.openclaw/workspace/scripts/pinchtab_social_media.py

echo ""
echo "🎉 QUICK START COMPLETE!"
echo "========================================"
echo "Next steps:"
echo "1. Review generated content calendar"
echo "2. Configure Pinchtab profiles if needed"
echo "3. Schedule automation with cron"
echo "4. Monitor performance daily"
echo ""
echo "For detailed setup, see: SOCIAL_MEDIA_SETUP_GUIDE.md"
