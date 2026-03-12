#!/usr/bin/env python3
"""Simple OpenUtter test"""
import subprocess
import sys

print("🧪 Testing OpenUtter installation...")

# Test 1: Check if npx openutter works
try:
    result = subprocess.run(["npx", "openutter", "--help"], 
                          capture_output=True, text=True, timeout=10)
    if result.returncode == 0:
        print("✅ OpenUtter CLI is accessible")
    else:
        print("❌ OpenUtter CLI not working")
        print(f"   Error: {result.stderr[:200]}")
except FileNotFoundError:
    print("❌ npx not found")
except subprocess.TimeoutExpired:
    print("❌ OpenUtter help timed out")

# Test 2: Check workspace
import os
workspace = "/Users/cubiczan/.openclaw/workspace/openutter"
if os.path.exists(workspace):
    print(f"✅ Workspace exists: {workspace}")
else:
    print(f"⚠️  Workspace not found: {workspace}")

print("\n📋 Quick setup check complete!")
print("Run './setup_openutter.sh' for full installation")
