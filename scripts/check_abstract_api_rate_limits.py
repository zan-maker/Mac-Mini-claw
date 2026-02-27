#!/usr/bin/env python3
"""
Check and update scripts for Abstract API rate limiting
"""

import os
import re
import sys

def find_abstract_api_scripts(workspace_path):
    """Find scripts that might use Abstract API"""
    
    scripts_to_check = []
    
    # Look for common patterns
    patterns = [
        r"abstractapi\.com",
        r"companyenrichment",
        r"ABSTRACT_API",
        r"company.*enrich",
        r"enrich.*company"
    ]
    
    for root, dirs, files in os.walk(workspace_path):
        for file in files:
            if file.endswith(('.py', '.sh')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                    # Check for Abstract API patterns
                    for pattern in patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            scripts_to_check.append(file_path)
                            break
                            
                except Exception as e:
                    print(f"  Error reading {file_path}: {e}")
    
    return scripts_to_check

def check_script_for_rate_limiting(script_path):
    """Check if a script has rate limiting for Abstract API"""
    
    with open(script_path, 'r') as f:
        content = f.read()
    
    # Check for rate limiting patterns
    rate_limit_patterns = [
        r"time\.sleep\(1\)",
        r"sleep\(1\)",
        r"rate.*limit",
        r"wait.*second",
        r"delay.*second"
    ]
    
    has_rate_limiting = False
    for pattern in rate_limit_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            has_rate_limiting = True
            break
    
    return has_rate_limiting

def main():
    workspace = "/Users/cubiczan/.openclaw/workspace"
    
    print("=" * 60)
    print("ABSTRACT API RATE LIMIT CHECK")
    print("=" * 60)
    print("\nChecking for scripts that might use Abstract API...")
    
    scripts = find_abstract_api_scripts(workspace)
    
    if not scripts:
        print("No scripts found with Abstract API patterns.")
        print("\nIf you have scripts using Abstract API, ensure they:")
        print("1. Include at least 1 second delay between requests")
        print("2. Use the rate_limiter utility in scripts/abstract_api_rate_limiter.py")
        return
    
    print(f"\nFound {len(scripts)} scripts to check:")
    
    needs_update = []
    for script in scripts:
        has_limiting = check_script_for_rate_limiting(script)
        status = "✅ Has rate limiting" if has_limiting else "❌ Needs rate limiting"
        print(f"  {os.path.basename(script)}: {status}")
        
        if not has_limiting:
            needs_update.append(script)
    
    if needs_update:
        print(f"\n⚠️  {len(needs_update)} scripts need rate limiting updates:")
        for script in needs_update:
            print(f"  - {script}")
        
        print("\n📋 Recommended actions:")
        print("1. Import the rate limiter utility:")
        print("   from scripts.abstract_api_rate_limiter import rate_limited, make_abstract_api_request")
        print("\n2. Decorate Abstract API functions:")
        print("   @rate_limited")
        print("   def get_company_info(domain):")
        print("       # Your Abstract API call here")
        print("\n3. Or use the helper function:")
        print("   result = make_abstract_api_request(url, params)")
        print("\n4. For batch processing:")
        print("   from scripts.abstract_api_rate_limiter import batch_process_with_rate_limit")
        print("   results = batch_process_with_rate_limit(items, process_func)")
    else:
        print("\n✅ All scripts appear to have rate limiting!")
    
    print("\n" + "=" * 60)
    print("RATE LIMITING REQUIREMENTS:")
    print("- Abstract API: 1 request per second")
    print("- Minimum delay between requests: 1 second")
    print("- Use time.sleep(1) or the rate_limiter utility")
    print("=" * 60)

if __name__ == "__main__":
    main()
