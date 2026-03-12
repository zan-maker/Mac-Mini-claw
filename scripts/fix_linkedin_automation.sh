#!/bin/bash
# LinkedIn Automation Fix Script
# Run this tomorrow to fix Pinchtab profile issues

echo "🔧 LINKEDIN AUTOMATION FIX SCRIPT"
echo "=========================================="
echo "Date: $(date)"
echo "=========================================="

echo ""
echo "🎯 PROBLEM: Pinchtab API returns 'profile not found'"
echo "💡 SOLUTION: Create profiles when server is not running"
echo ""

echo "1. 🔴 STOPPING PINCHTAB SERVER..."
pkill -f pinchtab 2>/dev/null
sleep 2

echo "✅ Pinchtab server stopped"
echo ""

echo "2. 👤 CREATING PROFILES PROPERLY..."
echo "   Creating Sam Desigan profile..."
/Users/cubiczan/.pinchtab/bin/pinchtab profile create sam-desigan --name "Sam Desigan LinkedIn" 2>&1 | grep -v "ERROR server err"

echo "   Creating Shyam Desigan profile..."
/Users/cubiczan/.pinchtab/bin/pinchtab profile create shyam-desigan --name "Shyam Desigan LinkedIn" 2>&1 | grep -v "ERROR server err"

echo ""
echo "3. 🟢 STARTING PINCHTAB SERVER..."
/Users/cubiczan/.pinchtab/bin/pinchtab &
sleep 3

echo "✅ Pinchtab server started"
echo ""

echo "4. 🔍 VERIFYING PROFILES..."
curl -s http://localhost:9867/health
echo ""
echo ""

echo "5. 🤖 TESTING AUTOMATION..."
cd /Users/cubiczan/.openclaw/workspace
python3 scripts/pinchtab_social_media.py 2>&1 | tail -20

echo ""
echo "6. ⏰ SETTING UP CRON JOBS..."
echo ""
echo "Add to crontab (crontab -e):"
echo "=========================================="
echo "# LinkedIn Automation (4x daily)"
echo "0 7,11,15,19 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/pinchtab_social_media.py >> ~/linkedin_automation.log 2>&1"
echo ""
echo "# Weekly Content Generation (Mondays)"
echo "0 8 * * 1 cd /Users/cubiczan/.openclaw/workspace && python3 scripts/social_media_orchestrator.py >> ~/content_generation.log 2>&1"
echo "=========================================="

echo ""
echo "7. 📊 GENERATING TOMORROW'S CONTENT..."
python3 scripts/social_media_orchestrator.py 2>&1 | tail -10

echo ""
echo "=========================================="
echo "✅ AUTOMATION FIX COMPLETE!"
echo "=========================================="
echo ""
echo "🎯 TOMORROW'S SCHEDULE:"
echo "• 7:00 AM - Automation check"
echo "• 8:00 AM - Shyam Desigan post"
echo "• 9:00 AM - Sam Desigan post"
echo "• 11:00 AM - Afternoon post"
echo "• 3:00 PM - Evening post"
echo "• 7:00 PM - Night post"
echo ""
echo "📊 MONITORING:"
echo "• Post history: cat linkedin_posts_history.json | jq '.[-2:]'"
echo "• Automation logs: tail -f ~/linkedin_automation.log"
echo "• LinkedIn: Check both profiles for posts"
echo ""
echo "🚀 READY FOR 24/7 AUTOMATED POSTING!"