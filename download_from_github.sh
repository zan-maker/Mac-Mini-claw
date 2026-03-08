#!/bin/bash
# Download LinkedIn post from GitHub

echo "================================================"
echo "DOWNLOAD LINKEDIN POST FROM GITHUB"
echo "================================================"
echo ""

GITHUB_URL="https://raw.githubusercontent.com/zan-maker/Mac-Mini-claw/main/social_media/LINKEDIN_POST_SAM.md"

echo "📥 Downloading from GitHub..."
curl -s "$GITHUB_URL" -o "LINKEDIN_POST_SAM.md"

if [ $? -eq 0 ]; then
    echo "✅ Downloaded successfully!"
    echo ""
    echo "📋 File: LINKEDIN_POST_SAM.md"
    echo ""
    echo "📝 Content preview:"
    echo "------------------------------------------------"
    head -20 "LINKEDIN_POST_SAM.md"
    echo "------------------------------------------------"
    echo ""
    echo "🚀 TO POST (RIGHT NOW - Optimal Time 5:30-6:00 PM EST):"
    echo "1. Copy lines 7-30 from the file"
    echo "2. Open LinkedIn (logged in as Sam Desigan)"
    echo "3. Click 'Start a post'"
    echo "4. Paste content"
    echo "5. Click 'Post'"
    echo ""
    echo "👥 SHYAM'S ENGAGEMENT (Within 5 minutes):"
    echo "1. Switch to Shyam's LinkedIn"
    echo "2. Find Sam's post"
    echo "3. Like and comment:"
    echo "   'Great insights Sam! The AI expense analysis case study is"
    echo "   particularly compelling. At Impact Quadrant, we're seeing"
    echo "   similar results with our clients.'"
else
    echo "❌ Download failed."
    echo ""
    echo "🔧 ALTERNATIVE: View directly in browser:"
    echo "https://github.com/zan-maker/Mac-Mini-claw/blob/main/social_media/LINKEDIN_POST_SAM.md"
fi

echo ""
echo "================================================"
echo "🎯 READY TO POST - DO IT NOW!"
echo "================================================"