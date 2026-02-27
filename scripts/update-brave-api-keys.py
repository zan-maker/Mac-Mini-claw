#!/usr/bin/env python3
"""
Update Brave Search API key in all Python files
"""

import os
import re
from pathlib import Path

# Old and new API keys
OLD_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"
NEW_KEY = "BSA4VYA3FjSPQmTjZeKjsq5CqWvFy2u"

# Also update the other old key from .env
OLD_KEY2 = "BSA4zSBzD_rNrZVVc5V8b1agGEQE-tC"

# Files to update (found from grep search)
files_to_update = [
    "deal_origination_sellers_scrapling.py",
    "run_deal_origination.py", 
    "deal_origination_sellers_scrapling_fixed.py",
    "run_enhanced_lead_gen.py",
    "expense-leads/generate-leads-scrapling-first.py",
    # Scripts directory
    "scripts/defense-sector-lead-gen.py",  # Already updated
    # Scrapling integration files
    "scrapling-integration/update_key_crons.py",
    "scrapling-integration/update_cron_jobs.py",
    "scrapling-integration/update_crons_simple.py",
    "scrapling-integration/update_all_lead_jobs.py",
]

def update_file(file_path):
    """Update API key in a single file"""
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Count occurrences of old keys
        count_old1 = content.count(OLD_KEY)
        count_old2 = content.count(OLD_KEY2)
        
        if count_old1 == 0 and count_old2 == 0:
            print(f"⚠️  No old keys found in: {file_path}")
            return True
        
        # Replace old keys with new key
        new_content = content.replace(OLD_KEY, NEW_KEY)
        new_content = new_content.replace(OLD_KEY2, NEW_KEY)
        
        # Write back
        with open(file_path, 'w') as f:
            f.write(new_content)
        
        print(f"✅ Updated {file_path}: {count_old1 + count_old2} replacements")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {str(e)}")
        return False

def main():
    """Main execution"""
    
    print("=" * 60)
    print("BRAVE SEARCH API KEY UPDATE SCRIPT")
    print("=" * 60)
    print(f"Old key 1: {OLD_KEY}")
    print(f"Old key 2: {OLD_KEY2}")
    print(f"New key: {NEW_KEY}")
    print()
    
    workspace = "/Users/cubiczan/.openclaw/workspace"
    os.chdir(workspace)
    
    updated_count = 0
    total_files = len(files_to_update)
    
    for file_path in files_to_update:
        if update_file(file_path):
            updated_count += 1
    
    print(f"\n📊 Summary: Updated {updated_count}/{total_files} files")
    
    # Also check for any other occurrences
    print("\n🔍 Searching for other occurrences of old keys...")
    
    # Use grep to find any remaining old keys
    import subprocess
    
    try:
        # Search for old key 1
        result1 = subprocess.run(
            ["grep", "-r", OLD_KEY, "--include=*.py", "--include=*.sh", "--include=*.js", "."],
            capture_output=True,
            text=True
        )
        
        # Search for old key 2  
        result2 = subprocess.run(
            ["grep", "-r", OLD_KEY2, "--include=*.py", "--include=*.sh", "--include=*.js", "."],
            capture_output=True,
            text=True
        )
        
        remaining1 = len(result1.stdout.strip().split('\n')) if result1.stdout.strip() else 0
        remaining2 = len(result2.stdout.strip().split('\n')) if result2.stdout.strip() else 0
        
        if remaining1 > 0 or remaining2 > 0:
            print(f"⚠️  Found {remaining1 + remaining2} remaining occurrences of old keys")
            print("   Run this command to see them:")
            print(f'   grep -r "{OLD_KEY}" --include="*.py" --include="*.sh" --include="*.js" .')
            print(f'   grep -r "{OLD_KEY2}" --include="*.py" --include="*.sh" --include="*.js" .')
        else:
            print("✅ No remaining occurrences of old keys found!")
            
    except Exception as e:
        print(f"⚠️  Could not search for remaining keys: {str(e)}")
    
    print("\n🎯 Next steps:")
    print("1. Test lead generation with new key")
    print("2. Monitor rate limits")
    print("3. Update cron jobs if they reference specific script files")
    print("4. Commit changes to GitHub")

if __name__ == "__main__":
    main()