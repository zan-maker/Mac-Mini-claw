#!/bin/bash
# LinkedIn Automation Quick Setup Script
# Run this to setup Pinchtab profiles and test automation

echo "🚀 LINKEDIN AUTOMATION QUICK SETUP"
echo "=========================================="

# Check if Pinchtab is installed
if ! command -v pinchtab &> /dev/null; then
    echo "❌ Pinchtab not found. Please install it first."
    echo "   Visit: https://github.com/pinchtab/pinchtab"
    exit 1
fi

echo "✅ Pinchtab is installed"

# Check if Pinchtab server is running
if curl -s http://localhost:9867/health > /dev/null; then
    echo "✅ Pinchtab server is running"
else
    echo "❌ Pinchtab server not running"
    echo "   Start it with: pinchtab start"
    exit 1
fi

echo ""
echo "🔧 SETTING UP PROFILES..."
echo "=========================================="

# Create Sam Desigan profile
echo "Creating Sam Desigan profile..."
pinchtab profile create sam-desigan --name "Sam Desigan LinkedIn"
if [ $? -eq 0 ]; then
    echo "✅ Sam Desigan profile created"
else
    echo "⚠️  Sam Desigan profile may already exist"
fi

# Create Shyam Desigan profile
echo "Creating Shyam Desigan profile..."
pinchtab profile create shyam-desigan --name "Shyam Desigan LinkedIn"
if [ $? -eq 0 ]; then
    echo "✅ Shyam Desigan profile created"
else
    echo "⚠️  Shyam Desigan profile may already exist"
fi

echo ""
echo "📋 VERIFYING PROFILES..."
echo "=========================================="
pinchtab profile list

echo ""
echo "🔐 LOGIN INSTRUCTIONS:"
echo "=========================================="
echo "For each profile, you need to login to LinkedIn once:"
echo ""
echo "1. FOR SAM DESIGAN:"
echo "   pinchtab start --profile sam-desigan"
echo "   • Browser will open"
echo "   • Go to linkedin.com"
echo "   • Login as Sam Desigan"
echo "   • Wait for feed to load"
echo "   • Close browser"
echo ""
echo "2. FOR SHYAM DESIGAN:"
echo "   pinchtab start --profile shyam-desigan"
echo "   • Browser will open"
echo "   • Go to linkedin.com"
echo "   • Login as Shyam Desigan"
echo "   • Wait for feed to load"
echo "   • Close browser"
echo ""
echo "⏰ This is a ONE-TIME setup."

echo ""
echo "🤖 TESTING AUTOMATION..."
echo "=========================================="
cd /Users/cubiczan/.openclaw/workspace
python3 scripts/pinchtab_social_media.py

echo ""
echo "⏰ SCHEDULING AUTOMATION..."
echo "=========================================="
echo "Add these to crontab (crontab -e):"
echo ""
echo "# LinkedIn Automation (4x daily)"
echo "0 7,11,15,19 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/pinchtab_social_media.py >> ~/linkedin_automation.log 2>&1"
echo ""
echo "# Weekly Content Generation (Mondays)"
echo "0 8 * * 1 cd /Users/cubiczan/.openclaw/workspace && python3 scripts/social_media_orchestrator.py >> ~/content_generation.log 2>&1"

echo ""
echo "🎯 TODAY'S SCHEDULED POSTS:"
echo "=========================================="
echo "• 8:00 AM - Shyam Desigan: 'Automation Success Stories'"
echo "• 9:00 AM - Sam Desigan: 'Business Expense Reduction'"

echo ""
echo "📊 MONITORING:"
echo "=========================================="
echo "• Post history: /Users/cubiczan/.openclaw/workspace/linkedin_posts_history.json"
echo "• Automation logs: ~/linkedin_automation.log"
echo "• Run analytics: python3 scripts/social_media_analytics.py"

echo ""
echo "🚀 SETUP COMPLETE!"
echo "=========================================="
echo "Next steps:"
echo "1. Login to LinkedIn for both profiles (one-time)"
echo "2. Add cron jobs for automation"
echo "3. Monitor today's 8:00 AM and 9:00 AM posts"
echo "4. Adjust strategy based on engagement"

echo ""
echo "⚡ QUICK COMMANDS:"
echo "=========================================="
echo "# Run automation manually:"
echo "python3 scripts/pinchtab_social_media.py"
echo ""
echo "# Generate new content:"
echo "python3 scripts/social_media_orchestrator.py"
echo ""
echo "# Check post history:"
echo "cat /Users/cubiczan/.openclaw/workspace/linkedin_posts_history.json | jq '.[-2:]'"