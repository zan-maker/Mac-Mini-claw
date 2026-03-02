#!/bin/bash
# Update all AgentMail API keys in the workspace

NEW_API_KEY="am_us_6aa957b36fb69693140cb0787c894d90ec2e65ffe937049634b685b911c1ac14"

echo "Updating AgentMail API keys..."
echo "New key: $NEW_API_KEY"
echo "=========================================="

# Find all files with old AgentMail API keys
find /Users/cubiczan/.openclaw/workspace -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "*.json" \) -exec grep -l "am_" {} \; 2>/dev/null | while read file; do
    echo "Checking: $file"
    
    # Skip certain files
    if [[ "$file" == *"update-agentmail-keys.sh" ]] || \
       [[ "$file" == *"test-updated-dorada.py" ]] || \
       [[ "$file" == *"test_full_system.py" ]] || \
       [[ "$file" == *"quick-gmail-update.py" ]] || \
       [[ "$file" == *"test-agentmail-api.py" ]] || \
       [[ "$file" == *"update-cron-scripts.py" ]]; then
        echo "  Skipping (update/test script): $file"
        continue
    fi
    
    # Check if file contains old API keys
    if grep -q "am_us_6aa957b36fb69693140cb0787c894d90ec2e65ffe937049634b685b911c1ac14" "$file" || \
       grep -q "am_us_6aa957b36fb69693140cb0787c894d90ec2e65ffe937049634b685b911c1ac14" "$file"; then
        
        echo "  Updating old API keys in: $file"
        
        # Update first key
        sed -i '' "s/am_us_6aa957b36fb69693140cb0787c894d90ec2e65ffe937049634b685b911c1ac14/$NEW_API_KEY/g" "$file"
        
        # Update second key
        sed -i '' "s/am_us_6aa957b36fb69693140cb0787c894d90ec2e65ffe937049634b685b911c1ac14/$NEW_API_KEY/g" "$file"
        
        echo "  ✅ Updated"
    elif grep -q "am_us_" "$file" && ! grep -q "$NEW_API_KEY" "$file"; then
        echo "  ⚠️ Contains other am_us_ key (not our new one): $file"
    else
        echo "  ✓ Already has new key or no API key"
    fi
done

echo
echo "=========================================="
echo "Verification..."
echo "=========================================="

# Check for any remaining old keys
echo "Checking for any remaining old API keys..."
OLD_KEYS_FOUND=0

for old_key in "am_us_6aa957b36fb69693140cb0787c894d90ec2e65ffe937049634b685b911c1ac14" "am_us_6aa957b36fb69693140cb0787c894d90ec2e65ffe937049634b685b911c1ac14"; do
    echo "Searching for: $old_key"
    find /Users/cubiczan/.openclaw/workspace -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "*.json" \) -exec grep -l "$old_key" {} \; 2>/dev/null | while read file; do
        # Skip test/update scripts
        if [[ "$file" != *"update-agentmail-keys.sh" ]] && \
           [[ "$file" != *"test-updated-dorada.py" ]] && \
           [[ "$file" != *"test_full_system.py" ]] && \
           [[ "$file" != *"quick-gmail-update.py" ]] && \
           [[ "$file" != *"test-agentmail-api.py" ]] && \
           [[ "$file" != *"update-cron-scripts.py" ]]; then
            echo "  ❌ Found in: $file"
            OLD_KEYS_FOUND=1
        fi
    done
done

echo
echo "=========================================="
if [ $OLD_KEYS_FOUND -eq 0 ]; then
    echo "✅ All AgentMail API keys updated successfully!"
    echo "New key: $NEW_API_KEY"
else
    echo "⚠️ Some old API keys may still exist (check skipped files)"
fi
echo "=========================================="