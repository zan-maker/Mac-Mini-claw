#!/usr/bin/env python3
"""
Security Verification Script
Checks for hardcoded secrets in files
"""

import os
import re
import sys

def check_for_secrets(content, filepath):
    """Check content for secret patterns"""
    patterns = [
        (r'ghp_[A-Za-z0-9]{36}', "GitHub Token"),
        (r'sk-[A-Za-z0-9]{48}', "OpenAI Key"),
        (r'am_[a-z0-9]{64}', "AgentMail Key"),
        (r'Bearer\s+[A-Za-z0-9._-]{20,}', "Bearer Token"),
        (r'api_key\s*=\s*["\'][A-Za-z0-9._-]{20,}["\']', "API Key Assignment"),
        (r'secret\s*=\s*["\'][A-Za-z0-9._-]{20,}["\']', "Secret Assignment"),
        (r'token\s*=\s*["\'][A-Za-z0-9._-]{20,}["\']', "Token Assignment"),
    ]
    
    issues = []
    for pattern, name in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            # Show first 2 matches only
            samples = matches[:2]
            issues.append(f"{name}: {len(matches)} found (e.g., {samples[0][:20]}...)")
    
    return issues

def scan_directory(directory="."):
    """Scan directory for files with secrets"""
    print("🔒 SECURITY SCAN")
    print("=" * 60)
    
    files_with_issues = 0
    total_issues = 0
    
    for root, dirs, files in os.walk(directory):
        # Skip git directory and virtual environments
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'venv', '.venv', 'node_modules']]
        
        for file in files:
            if file.endswith(('.py', '.json', '.md', '.sh', '.yaml', '.yml', '.txt')):
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    issues = check_for_secrets(content, filepath)
                    if issues:
                        files_with_issues += 1
                        total_issues += len(issues)
                        
                        print(f"\n⚠️  {filepath}:")
                        for issue in issues:
                            print(f"   - {issue}")
                            
                except Exception as e:
                    print(f"   ⚠️  Could not read {filepath}: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 SCAN RESULTS:")
    print(f"   Files scanned: {sum(1 for _ in os.walk(directory))}")
    print(f"   Files with issues: {files_with_issues}")
    print(f"   Total issues found: {total_issues}")
    
    if total_issues == 0:
        print("✅ No secrets found!")
        return 0
    else:
        print("❌ Secrets found - review and fix above files")
        return 1

def main():
    """Main function"""
    # Get directory to scan (default current)
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    
    print(f"Scanning directory: {os.path.abspath(directory)}")
    print("Looking for: GitHub tokens, API keys, Bearer tokens, etc.")
    print("")
    
    exit_code = scan_directory(directory)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()