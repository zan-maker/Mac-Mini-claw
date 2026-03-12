#!/bin/bash
# Instagram Automation Script using PinchTab
# Requires: Already logged into Instagram

echo "📱 Instagram Automation"
echo "======================"

# Function to check login status
check_login() {
    echo "🔍 Checking login status..."
    pinchtab text > /tmp/instagram_status.json
    URL=$(jq -r '.url' /tmp/instagram_status.json 2>/dev/null)
    
    if [[ "$URL" == *"instagram.com"* ]] && [[ "$URL" != *"login"* ]]; then
        echo "✅ Logged into Instagram"
        return 0
    else
        echo "❌ Not logged in or on login page"
        return 1
    fi
}

# Function to monitor hashtag
monitor_hashtag() {
    local HASHTAG="${1:-AI}"
    local LIMIT="${2:-5}"
    
    echo "🔍 Monitoring #${HASHTAG}..."
    pinchtab nav "https://www.instagram.com/explore/tags/${HASHTAG}/"
    sleep 3
    
    # Take snapshot
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    SNAPSHOT_FILE="/tmp/instagram_${HASHTAG}_${TIMESTAMP}.txt"
    pinchtab snap -c > "$SNAPSHOT_FILE"
    
    # Extract post links
    echo "📊 Found posts with #${HASHTAG}:"
    grep -i "link \"" "$SNAPSHOT_FILE" | head -$LIMIT | while read line; do
        echo "  - $line"
    done
    
    # Count posts
    POST_COUNT=$(grep -c "link \"" "$SNAPSHOT_FILE" || echo "0")
    echo "📈 Total posts found: $POST_COUNT"
    
    # Take screenshot
    SCREENSHOT_FILE="/tmp/instagram_${HASHTAG}_${TIMESTAMP}.png"
    pinchtab ss -o "$SCREENSHOT_FILE"
    echo "📸 Screenshot saved: $SCREENSHOT_FILE"
}

# Function to like posts (simple demo)
like_posts() {
    local HASHTAG="${1:-AI}"
    local COUNT="${2:-3}"
    
    echo "❤️  Liking #${HASHTAG} posts..."
    pinchtab nav "https://www.instagram.com/explore/tags/${HASHTAG}/"
    sleep 3
    
    # Find like buttons (simplified - would need actual element refs)
    echo "⚠️  Note: Would click like buttons here"
    echo "   In production, would:"
    echo "   1. Find post elements"
    echo "   2. Click like button for each"
    echo "   3. Add delays between actions"
    
    # For now, just demonstrate capability
    echo "✅ Like functionality ready (needs element mapping)"
}

# Function to create post (placeholder)
create_post() {
    local IMAGE="$1"
    local CAPTION="$2"
    
    echo "📝 Creating post..."
    echo "  Image: $IMAGE"
    echo "  Caption: $CAPTION"
    
    echo "⚠️  Post creation steps:"
    echo "  1. Click 'Create' button (usually + icon)"
    echo "  2. Select image: $IMAGE"
    echo "  3. Add caption: $CAPTION"
    echo "  4. Add hashtags"
    echo "  5. Click 'Share'"
    
    echo "✅ Post workflow defined (needs element mapping)"
}

# Function to navigate to create page
go_to_create() {
    echo "➕ Navigating to create post page..."
    
    # Try different possible create button locations
    echo "Searching for create button..."
    
    # Method 1: Direct URL (might work)
    pinchtab nav "https://www.instagram.com/create/"
    sleep 2
    
    # Check if we're on create page
    pinchtab text > /tmp/create_check.json
    TITLE=$(jq -r '.title' /tmp/create_check.json 2>/dev/null)
    
    if [[ "$TITLE" == *"Create"* ]] || [[ "$TITLE" == *"New"* ]]; then
        echo "✅ On create post page"
        return 0
    else
        echo "❌ Could not reach create page directly"
        echo "   Might need to click create button manually"
        return 1
    fi
}

# Main execution
echo ""
echo "1. Checking login status..."
if check_login; then
    echo ""
    echo "2. Testing hashtag monitoring..."
    monitor_hashtag "AI" 3
    
    echo ""
    echo "3. Testing post creation navigation..."
    if go_to_create; then
        echo "🎉 Ready to create posts!"
        echo ""
        echo "Example post creation:"
        create_post "/path/to/image.jpg" "Check out our AI automation tools! #AI #Automation #Tech"
    else
        echo "⚠️  Could not access create page automatically"
        echo "   Manual element mapping required"
    fi
    
    echo ""
    echo "4. Engagement testing..."
    like_posts "AI" 2
    
    echo ""
    echo "📅 Scheduling example:"
    echo "  To run daily at 9 AM, 12 PM, 3 PM, 6 PM:"
    echo "  crontab -e"
    echo "  Add: 0 9,12,15,18 * * * $PWD/$0"
    
else
    echo "❌ Please log into Instagram first"
    echo "   Run: pinchtab nav https://www.instagram.com/"
    echo "   Log in manually, then run this script again"
fi

echo ""
echo "✅ Instagram automation script ready!"
echo "   Next: Map actual element references for full automation"