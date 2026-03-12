#!/bin/bash
# Instagram AI Finance Posting Script
# Attempts to post the generated AI Finance visual

echo "📱 Instagram AI Finance Posting"
echo "================================"

# Check current Instagram status
echo "🔍 Checking Instagram status..."
pinchtab text > /tmp/current_status.json
CURRENT_URL=$(jq -r '.url' /tmp/current_status.json 2>/dev/null)
CURRENT_TITLE=$(jq -r '.title' /tmp/current_status.json 2>/dev/null)

echo "📍 Current page: $CURRENT_TITLE"
echo "🔗 URL: $CURRENT_URL"

# Check if we're logged in
if [[ "$CURRENT_URL" == *"instagram.com"* ]] && [[ "$CURRENT_URL" != *"login"* ]]; then
    echo "✅ Logged into Instagram"
else
    echo "❌ Not logged into Instagram or on login page"
    echo "   Please log in first"
    exit 1
fi

# Generated content
IMAGE_PATH="/tmp/ai_finance_visual.png"
CAPTION_FILE="/tmp/ai_finance_caption.txt"

if [ ! -f "$IMAGE_PATH" ]; then
    echo "❌ Image not found: $IMAGE_PATH"
    echo "   Run: python3 /Users/cubiczan/.openclaw/workspace/scripts/create_ai_finance_visual.py"
    exit 1
fi

if [ ! -f "$CAPTION_FILE" ]; then
    echo "❌ Caption file not found: $CAPTION_FILE"
    exit 1
fi

echo ""
echo "🎨 POST CONTENT:"
echo "  Image: $IMAGE_PATH ($(stat -f%z "$IMAGE_PATH" 2>/dev/null || echo "?") bytes)"
echo "  Caption: $CAPTION_FILE ($(wc -l < "$CAPTION_FILE") lines)"

# Show caption preview
echo ""
echo "📝 CAPTION PREVIEW:"
head -5 "$CAPTION_FILE"
echo "..."

# Navigate to Instagram create page
echo ""
echo "➕ Navigating to Instagram create page..."
pinchtab nav "https://www.instagram.com/create/select/"
sleep 3

# Take snapshot to see what's on the page
echo "📊 Analyzing create page..."
pinchtab snap -c > /tmp/create_page_snapshot.txt

# Check if we're on create page
if grep -q -i "create\|select\|upload" /tmp/create_page_snapshot.txt; then
    echo "✅ On Instagram create page"
    
    # Show available elements
    echo ""
    echo "🔍 Available elements on create page:"
    grep -i "button\|link\|textbox" /tmp/create_page_snapshot.txt | head -10
    
    # Look for specific elements
    echo ""
    echo "🎯 Looking for posting elements:"
    
    # Check for upload button
    if grep -q -i "upload\|select.*image\|choose.*file" /tmp/create_page_snapshot.txt; then
        UPLOAD_ELEMENT=$(grep -i "upload\|select.*image\|choose.*file" /tmp/create_page_snapshot.txt | head -1 | cut -d: -f1)
        echo "  📤 Upload button: $UPLOAD_ELEMENT"
    else
        echo "  📤 Upload button: Not found in snapshot"
    fi
    
    # Check for next button
    if grep -q -i "next\|continue" /tmp/create_page_snapshot.txt; then
        NEXT_ELEMENT=$(grep -i "next\|continue" /tmp/create_page_snapshot.txt | head -1 | cut -d: -f1)
        echo "  ⏭️  Next button: $NEXT_ELEMENT"
    fi
    
    # Check for share button
    if grep -q -i "share\|post" /tmp/create_page_snapshot.txt; then
        SHARE_ELEMENT=$(grep -i "share\|post" /tmp/create_page_snapshot.txt | head -1 | cut -d: -f1)
        echo "  📢 Share button: $SHARE_ELEMENT"
    fi
    
else
    echo "⚠️  Not on expected create page"
    echo "   Current page snapshot saved to: /tmp/create_page_snapshot.txt"
fi

echo ""
echo "🚀 POSTING WORKFLOW:"
echo "1. Click upload/select button (if found)"
echo "2. Select image: $IMAGE_PATH"
echo "3. Click next/continue"
echo "4. Add caption from: $CAPTION_FILE"
echo "5. Click share/post"

echo ""
echo "⚠️  IMPORTANT NOTES:"
echo "• File upload via PinchTab may require different approach"
echo "• Instagram's UI changes frequently"
echo "• Element references need to be verified"
echo "• Rate limits apply"

echo ""
echo "📅 CRON JOB SETUP:"
echo "To schedule daily posting at 9 AM:"
echo "----------------------------------"
echo "1. Create script: /usr/local/bin/post_ai_finance.sh"
echo "2. Make executable: chmod +x /usr/local/bin/post_ai_finance.sh"
echo "3. Add to crontab: crontab -e"
echo "4. Add line: 0 9 * * * /usr/local/bin/post_ai_finance.sh"
echo ""
echo "For multiple daily posts (9 AM, 12 PM, 3 PM, 6 PM):"
echo "0 9,12,15,18 * * * /usr/local/bin/post_ai_finance.sh"

echo ""
echo "✅ Ready for Instagram posting!"
echo "   Next: Test with actual element interactions"