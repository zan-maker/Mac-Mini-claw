#!/bin/bash
# Start LinkedIn automation with Pinchtab profiles

echo "🚀 STARTING LINKEDIN AUTOMATION SETUP"
echo "=========================================="

# Check if Pinchtab server is running
if curl -s http://localhost:9867/health > /dev/null; then
    echo "✅ Pinchtab server is running"
else
    echo "❌ Starting Pinchtab server..."
    /Users/cubiczan/.pinchtab/bin/pinchtab &
    sleep 3
fi

echo ""
echo "👤 CREATING LINKEDIN PROFILES..."
echo "=========================================="

# Create profile directories if they don't exist
mkdir -p /Users/cubiczan/.pinchtab/profiles/sam-desigan
mkdir -p /Users/cubiczan/.pinchtab/profiles/shyam-desigan

echo "✅ Profile directories created:"
echo "   • /Users/cubiczan/.pinchtab/profiles/sam-desigan"
echo "   • /Users/cubiczan/.pinchtab/profiles/shyam-desigan"

echo ""
echo "🔐 LOGIN TO LINKEDIN (ONE-TIME)"
echo "=========================================="
echo "We'll start browsers for each profile. You need to:"
echo "1. Login to LinkedIn in each browser"
echo "2. Wait for feed to load"
echo "3. Close browser when done"
echo ""
echo "Press Enter to start Sam Desigan login..."
read

# Start Sam Desigan browser
echo "🌐 Starting Sam Desigan browser..."
open -a "Google Chrome" --args \
  --user-data-dir="/Users/cubiczan/.pinchtab/profiles/sam-desigan" \
  --profile-directory="Sam Desigan LinkedIn" \
  https://www.linkedin.com

echo ""
echo "✅ Sam Desigan browser opened."
echo "   • Login to LinkedIn as Sam Desigan"
echo "   • Wait for feed to load"
echo "   • Close browser when done"
echo ""
echo "Press Enter when Sam Desigan login is complete..."
read

# Start Shyam Desigan browser
echo "🌐 Starting Shyam Desigan browser..."
open -a "Google Chrome" --args \
  --user-data-dir="/Users/cubiczan/.pinchtab/profiles/shyam-desigan" \
  --profile-directory="Shyam Desigan LinkedIn" \
  https://www.linkedin.com

echo ""
echo "✅ Shyam Desigan browser opened."
echo "   • Login to LinkedIn as Shyam Desigan"
echo "   • Wait for feed to load"
echo "   • Close browser when done"
echo ""
echo "Press Enter when Shyam Desigan login is complete..."
read

echo ""
echo "🎯 TESTING AUTOMATION..."
echo "=========================================="
cd /Users/cubiczan/.openclaw/workspace
python3 scripts/pinchtab_social_media.py

echo ""
echo "✅ SETUP COMPLETE!"
echo "=========================================="
echo "LinkedIn automation is ready to run."
echo ""
echo "⏰ TODAY'S SCHEDULED POSTS:"
echo "   • 8:00 AM - Shyam Desigan: Tech Innovation Frameworks"
echo "   • 9:00 AM - Sam Desigan: AI Finance Trends"
echo ""
echo "⚡ RUN AUTOMATION MANUALLY:"
echo "   python3 scripts/pinchtab_social_media.py"
echo ""
echo "📊 CHECK POST HISTORY:"
echo "   cat /Users/cubiczan/.openclaw/workspace/linkedin_posts_history.json | jq '.[-2:]'"