#!/usr/bin/env python3
# test-war-monitor-container.py
# Test war monitor in container

import sys
import os

print("🧪 TESTING WAR MONITOR IN CONTAINER")
print("=" * 50)

# Check Python
print(f"Python: {sys.version}")

# Check script exists
script_path = "scripts/war-crude-monitor.py"
if os.path.exists(script_path):
    with open(script_path, 'r') as f:
        content = f.read()
    print(f"✅ Script found ({len(content)} bytes)")
    
    # Check for required imports
    required = ['requests', 'pandas', 'numpy', 'dotenv']
    missing = []
    
    print("\nChecking dependencies:")
    for module in required:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            missing.append(module)
            print(f"  ❌ {module}")
    
    if missing:
        print(f"\nInstalling {len(missing)} missing dependencies...")
        import subprocess
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
            print("✅ Dependencies installed")
        except Exception as e:
            print(f"❌ Installation failed: {e}")
    else:
        print("✅ All dependencies available")
    
    # Test environment variables
    print("\nChecking environment:")
    env_vars = ['NEWSAPI_KEY', 'SERPER_API_KEY']
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: SET ({len(value)} chars)")
        else:
            print(f"  ⚠️  {var}: NOT SET")
    
    # Try to parse the script
    print("\nTesting script structure...")
    try:
        # Look for main function pattern
        if 'def main()' in content or 'if __name__' in content:
            print("✅ Script has proper structure")
        else:
            print("⚠️  Script structure unusual")
        
        # Look for API calls
        if 'requests.get' in content or 'requests.post' in content:
            print("✅ Contains API calls")
        
        # Look for logging
        if 'logging' in content or 'print(' in content:
            print("✅ Contains output/logging")
            
    except Exception as e:
        print(f"❌ Script analysis error: {e}")
        
else:
    print(f"❌ Script not found: {script_path}")

print("\n" + "=" * 50)
print("✅ CONTAINER TEST COMPLETE")
print("\nNext: Run actual war monitor with:")
print("~/container-test/simple-container.sh --cmd \\")
print("  \"python3 scripts/war-crude-monitor.py --test --safe-mode\"")