#!/bin/bash
# Quick download script for LinkedIn post content
# Run this to get the LinkedIn post file

echo "================================================"
echo "DOWNLOAD LINKEDIN POST CONTENT"
echo "================================================"
echo ""

# Check if curl is available
if ! command -v curl &> /dev/null; then
    echo "❌ curl is not installed. Please install curl first."
    exit 1
fi

# Create temp directory
TEMP_DIR=$(mktemp -d)
echo "📁 Created temp directory: $TEMP_DIR"
echo ""

# The content to download
CONTENT_URL="https://raw.githubusercontent.com/zan-maker/Mac-Mini-claw/main/social_media/LINKEDIN_POST_SAM.md"

echo "📥 Downloading LinkedIn post content..."
curl -s "$CONTENT_URL" -o "$TEMP_DIR/LINKEDIN_POST_SAM.md"

if [ $? -eq 0 ]; then
    echo "✅ Downloaded successfully!"
    echo ""
    echo "📋 File location: $TEMP_DIR/LINKEDIN_POST_SAM.md"
    echo ""
    echo "📝 Content preview:"
    echo "------------------------------------------------"
    head -20 "$TEMP_DIR/LINKEDIN_POST_SAM.md"
    echo "------------------------------------------------"
    echo ""
    echo "🚀 TO POST:"
    echo "1. Open the file: open $TEMP_DIR/LINKEDIN_POST_SAM.md"
    echo "2. Copy the content (lines 7-30)"
    echo "3. Go to LinkedIn → 'Start a post' → Paste → Post"
    echo ""
    echo "⏰ OPTIMAL TIME: RIGHT NOW (5:30-6:00 PM EST)"
else
    echo "❌ Download failed. GitHub may be blocking."
    echo ""
    echo "🔧 ALTERNATIVE: Get content directly:"
    echo "cat /Users/cubiczan/.openclaw/workspace/social_media/LINKEDIN_POST_SAM.md"
fi

echo ""
echo "================================================"
echo "🎯 READY TO POST - DO IT NOW!"
echo "================================================"