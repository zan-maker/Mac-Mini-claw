#!/bin/bash
# Twitter/X Hashtag Monitor using PinchTab CLI
# Public hashtag pages don't require login

HASHTAG="${1:-AI}"
OUTPUT_DIR="/tmp/twitter_monitor"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "🔍 Monitoring Twitter/X hashtag: #${HASHTAG}"
echo "=========================================="

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Navigate to hashtag page
echo "🌐 Navigating to Twitter/X hashtag page..."
pinchtab nav "https://twitter.com/hashtag/${HASHTAG}"

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

# Simple analysis
echo ""
echo "📊 QUICK ANALYSIS:"
echo "=================="

# Show first few lines of text content
echo "📝 First 200 chars of content:"
head -c 200 "$TEXT_FILE" 2>/dev/null | cat
echo ""
echo "..."

# File sizes
echo ""
echo "📁 File sizes:"
echo "  Snapshot: $(wc -l < "$SNAPSHOT_FILE" 2>/dev/null || echo 0) lines"
echo "  Text: $(jq '.text | length' "$TEXT_FILE" 2>/dev/null || echo 0) chars"
echo "  Screenshot: $(stat -f%z "$SCREENSHOT_FILE" 2>/dev/null || echo 0) bytes"

echo ""
echo "✅ Twitter/X hashtag monitoring complete!"
echo "   Output directory: $OUTPUT_DIR"