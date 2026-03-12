#!/bin/bash
# Instagram Hashtag Monitor using PinchTab CLI
# Doesn't require login for public hashtag pages

HASHTAG="${1:-AI}"
OUTPUT_DIR="/tmp/instagram_monitor"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "🔍 Monitoring Instagram hashtag: #${HASHTAG}"
echo "=========================================="

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Navigate to hashtag page
echo "🌐 Navigating to Instagram hashtag page..."
pinchtab nav "https://www.instagram.com/explore/tags/${HASHTAG}/"

# Wait for page to load
sleep 5

# Take snapshot
echo "📊 Taking snapshot of page structure..."
SNAPSHOT_FILE="${OUTPUT_DIR}/hashtag_${HASHTAG}_${TIMESTAMP}.txt"
pinchtab snap -c > "$SNAPSHOT_FILE"
echo "  ✅ Snapshot saved to: $SNAPSHOT_FILE"

# Extract text content
echo "📝 Extracting text content..."
TEXT_FILE="${OUTPUT_DIR}/hashtag_${HASHTAG}_${TIMESTAMP}_text.json"
pinchtab text > "$TEXT_FILE"
echo "  ✅ Text extracted to: $TEXT_FILE"

# Take screenshot
echo "📸 Capturing screenshot..."
SCREENSHOT_FILE="${OUTPUT_DIR}/hashtag_${HASHTAG}_${TIMESTAMP}.png"
pinchtab ss -o "$SCREENSHOT_FILE"
echo "  ✅ Screenshot saved to: $SCREENSHOT_FILE"

# Analyze results
echo ""
echo "📊 ANALYSIS RESULTS:"
echo "===================="

# Count elements in snapshot
ELEMENT_COUNT=$(grep -c "^e[0-9]:" "$SNAPSHOT_FILE" || echo "0")
echo "📈 Elements found: $ELEMENT_COUNT"

# Extract page title
TITLE=$(grep "^# " "$SNAPSHOT_FILE" | head -1 | sed 's/^# //' || echo "Unknown")
echo "🏷️  Page title: $TITLE"

# Extract URL from text output
URL=$(jq -r '.url' "$TEXT_FILE" 2>/dev/null || echo "N/A")
echo "🔗 URL: $URL"

# Count mentions of hashtag
HASHTAG_MENTIONS=$(grep -o -i "$HASHTAG" "$SNAPSHOT_FILE" "$TEXT_FILE" 2>/dev/null | wc -l || echo "0")
echo "🏷️  #${HASHTAG} mentions: $HASHTAG_MENTIONS"

echo ""
echo "📁 Output files:"
echo "  - Snapshot: $SNAPSHOT_FILE"
echo "  - Text: $TEXT_FILE"
echo "  - Screenshot: $SCREENSHOT_FILE"

echo ""
echo "⏰ To schedule monitoring (every hour):"
echo "  crontab -e"
echo "  Add: 0 * * * * $PWD/$0 $HASHTAG"
echo ""
echo "✅ Hashtag monitoring complete!"