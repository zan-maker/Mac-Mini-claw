#!/bin/bash
# Copy LinkedIn post content to clipboard

echo "================================================"
echo "COPYING LINKEDIN POST CONTENT TO CLIPBOARD"
echo "================================================"
echo ""

# Copy the main post content (lines 7-30)
CONTENT=$(sed -n '7,30p' /Users/cubiczan/.openclaw/workspace/social_media/LINKEDIN_POST_SAM.md)

echo "$CONTENT" | pbcopy

echo "✅ Content copied to clipboard!"
echo ""
echo "📋 TO POST:"
echo "1. Open Chrome → LinkedIn (logged in as Sam Desigan)"
echo "2. Click 'Start a post'"
echo "3. Paste (Cmd+V)"
echo "4. Click 'Post'"
echo ""
echo "⏰ OPTIMAL TIME: RIGHT NOW (5:30-6:00 PM EST)"
echo ""
echo "👥 SHYAM'S ENGAGEMENT (Do immediately after):"
echo "1. Switch to Shyam's LinkedIn"
echo "2. Find Sam's post"
echo "3. Like it"
echo "4. Comment with:"
echo "   'Great insights Sam! The AI expense analysis case study is"
echo "   particularly compelling. At Impact Quadrant, we're seeing"
echo "   similar results with our clients.'"
echo ""
echo "================================================"
echo "🎯 READY TO POST - DO IT NOW!"
echo "================================================"