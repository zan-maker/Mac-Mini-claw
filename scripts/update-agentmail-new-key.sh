#!/bin/bash
# Update all AgentMail API keys to new key provided by user

echo "Updating AgentMail API keys to new key..."
echo "=========================================="

OLD_API_KEY="am_us_6aa957b36fb69693140cb0787c894d90ec2e65ffe937049634b685b911c1ac14"
NEW_API_KEY="am_us_f03e762c50d6e353bbe7b4307b452bd73f58aed725bc0ef53f25d9f8e91c962a"

OLD_INBOX="zane@agentmail.to"
NEW_INBOX="Zander@agentmail.to"

echo "Old API Key: ${OLD_API_KEY:0:20}..."
echo "New API Key: ${NEW_API_KEY:0:20}..."
echo "Old Inbox: $OLD_INBOX"
echo "New Inbox: $NEW_INBOX"
echo

# Find and update all files
echo "Searching for files with old API key..."
find /Users/cubiczan/.openclaw/workspace -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" \) -exec grep -l "$OLD_API_KEY" {} \; 2>/dev/null | while read file; do
    echo "Updating: $file"
    
    # Update API key
    sed -i '' "s/$OLD_API_KEY/$NEW_API_KEY/g" "$file"
    
    # Update inbox if present
    if grep -q "$OLD_INBOX" "$file"; then
        sed -i '' "s/$OLD_INBOX/$NEW_INBOX/g" "$file"
    fi
    
    # Also update any uppercase variations
    sed -i '' "s/Zane@agentmail.to/Zander@agentmail.to/g" "$file"
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
            echo "  ⚠️ Has different API key - checking..."
            # Show the API key found
            grep -o "am_[a-f0-9]\{64\}" "$file" | head -1 | while read found_key; do
                if [ "$found_key" != "$NEW_API_KEY" ]; then
                    echo "  Found: ${found_key:0:20}..."
                    echo "  Updating to new key..."
                    sed -i '' "s/$found_key/$NEW_API_KEY/g" "$file"
                fi
            done
        fi
    fi
done

echo
echo "Testing new API key..."
# Quick test of new API key
curl -s -X GET "https://api.agentmail.to/v1/health" \
  -H "Authorization: Bearer $NEW_API_KEY" \
  -H "Content-Type: application/json" \
  --max-time 10 > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ API key appears valid (health check passed)"
else
    echo "⚠️ API key health check failed - key may be invalid or API down"
fi

echo
echo "=========================================="
echo "✅ AgentMail API key update complete!"
echo
echo "Changed from:"
echo "- API Key: ${OLD_API_KEY:0:20}..."
echo "- Inbox: $OLD_INBOX"
echo
echo "Changed to:"
echo "- API Key: ${NEW_API_KEY:0:20}..."
echo "- Inbox: $NEW_INBOX"
echo
echo "Note: According to WORKFLOW_AUTO.md, AgentMail is deprecated."
echo "Primary email method should be Gmail SMTP."
echo "=========================================="