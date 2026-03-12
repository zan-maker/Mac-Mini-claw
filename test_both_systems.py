#!/usr/bin/env python3
"""Test both Firecrawl and OpenUtter setups"""
import os
import subprocess
import sys

print("🧪 Testing Firecrawl & OpenUtter Setups")
print("="*50)

# Test 1: Firecrawl CLI
print("\n1. Testing Firecrawl CLI...")
try:
    result = subprocess.run(["firecrawl", "--version"], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print(f"   ✅ Firecrawl CLI: {result.stdout.strip()}")
    else:
        print(f"   ❌ Firecrawl CLI failed: {result.stderr[:100]}")
except FileNotFoundError:
    print("   ❌ Firecrawl CLI not found")

# Test 2: Firecrawl API Key
print("\n2. Testing Firecrawl API Key...")
api_key = "fc-3ba22d7b419a490da37f7fb0255ef581"
if api_key.startswith("fc-"):
    print(f"   ✅ API Key format correct: {api_key[:10]}...")
else:
    print(f"   ❌ API Key format incorrect")

# Test 3: OpenUtter CLI
print("\n3. Testing OpenUtter CLI...")
try:
    result = subprocess.run(["npx", "openutter", "--help"], 
                          capture_output=True, text=True, timeout=10)
    if "OpenUtter" in result.stdout or "OpenUtter" in result.stderr:
        print("   ✅ OpenUtter CLI accessible")
    else:
        print("   ⚠️  OpenUtter output unexpected")
except subprocess.TimeoutExpired:
    print("   ❌ OpenUtter timed out")
except Exception as e:
    print(f"   ❌ OpenUtter error: {e}")

# Test 4: Workspace
print("\n4. Checking workspace...")
workspace = "/Users/cubiczan/.openclaw/workspace"
files = [
    "agent_web_scraper.py",
    "investor_event_monitor.py",
    "SETUP_COMPLETION_GUIDE.md"
]

for file in files:
    path = os.path.join(workspace, file)
    if os.path.exists(path):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} (missing)")

print("\n" + "="*50)
print("🎯 NEXT ACTIONS:")
print("1. Complete OpenUtter setup (wait for script or run manually)")
print("2. Authenticate: npx openutter auth")
print("3. Add investor events to JSON file")
print("4. Test Firecrawl: python3 agent_web_scraper.py")
print("="*50)
