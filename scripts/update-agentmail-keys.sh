#!/bin/bash
# Update all AgentMail API keys from failing to working version

echo "Updating AgentMail API keys..."
echo "=========================================="

OLD_API_KEY="am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
NEW_API_KEY="am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"

OLD_INBOX="zane@agentmail.to"
NEW_INBOX="zane@agentmail.to"

# Find and update all files
find /Users/cubiczan/.openclaw/workspace -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" \) -exec grep -l "$OLD_API_KEY" {} \; 2>/dev/null | while read file; do
    echo "Updating: $file"
    
    # Update API key
    sed -i '' "s/$OLD_API_KEY/$NEW_API_KEY/g" "$file"
    
    # Update inbox if present
    if grep -q "$OLD_INBOX" "$file"; then
        sed -i '' "s/$OLD_INBOX/$NEW_INBOX/g" "$file"
    fi
    
    # Also update any uppercase zane@agentmail.to to lowercase
    sed -i '' "s/zane@agentmail.to/zane@agentmail.to/g" "$file"
done

echo
echo "Checking for other AgentMail configurations..."
# Check for files using AgentMail but might have different patterns
find /Users/cubiczan/.openclaw/workspace -type f \( -name "*.py" -o -name "*.sh" \) -exec grep -l "agentmail\|AgentMail" {} \; 2>/dev/null | while read file; do
    if grep -q "api.*key\|API.*KEY\|apikey\|APIKEY" "$file"; then
        echo "Found AgentMail in: $file"
        # Check if it has the new key already
        if grep -q "$NEW_API_KEY" "$file"; then
            echo "  ✅ Already using new API key"
        elif grep -q "am_" "$file"; then
            echo "  ⚠️ Has different API key"
        fi
    fi
done

echo
echo "=========================================="
echo "✅ AgentMail API key update complete!"
echo
echo "Changed from:"
echo "- API Key: $OLD_API_KEY"
echo "- Inbox: $OLD_INBOX"
echo
echo "Changed to:"
echo "- API Key: $NEW_API_KEY"
echo "- Inbox: $NEW_INBOX"
echo
echo "All cron jobs will now use the working AgentMail account."
echo "=========================================="