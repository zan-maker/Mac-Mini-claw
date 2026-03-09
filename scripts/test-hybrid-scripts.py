#!/usr/bin/env python3
"""
Test all hybrid monitoring scripts
"""

import subprocess
import sys
import os
from datetime import datetime

WORKSPACE = "/Users/cubiczan/.openclaw/workspace"
SCRIPTS = [
    "scripts/hybrid-token-monitor.py",
    "scripts/hybrid-critical-alert.py", 
    "scripts/hybrid-api-monitor.py",
    "scripts/hybrid-heartbeat.py"
]

def test_script(script_path):
    """Test a single hybrid script"""
    print(f"\n{'='*60}")
    print(f"Testing: {os.path.basename(script_path)}")
    print(f"{'='*60}")
    
    full_path = os.path.join(WORKSPACE, script_path)
    
    if not os.path.exists(full_path):
        print(f"❌ Script not found: {full_path}")
        return False
    
    try:
        # Make executable
        os.chmod(full_path, 0o755)
        
        # Run script
        result = subprocess.run(
            [sys.executable, full_path],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=WORKSPACE
        )
        
        print(f"Exit code: {result.returncode}")
        print(f"Output:\n{result.stdout}")
        
        if result.stderr:
            print(f"Errors:\n{result.stderr}")
        
        # Check for success indicators
        success_indicators = [
            "COST OPTIMIZATION SUMMARY",
            "Local model checks",
            "API checks", 
            "Estimated savings"
        ]
        
        has_indicators = any(indicator in result.stdout for indicator in success_indicators)
        
        if has_indicators:
            print(f"✅ {os.path.basename(script_path)} - TEST PASSED")
            return True
        else:
            print(f"⚠️ {os.path.basename(script_path)} - Missing success indicators")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ {os.path.basename(script_path)} - TIMEOUT (60 seconds)")
        return False
    except Exception as e:
        print(f"❌ {os.path.basename(script_path)} - ERROR: {e}")
        return False

def check_local_model():
    """Check if local model is available"""
    print(f"\n{'='*60}")
    print("Checking Local Model Availability")
    print(f"{'='*60}")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        
        if response.status_code == 200:
            print("✅ Local model service is running")
            data = response.json()
            models = data.get('models', [])
            if models:
                print(f"Available models: {', '.join([m.get('name', 'unknown') for m in models])}")
            return True
        else:
            print(f"⚠️ Local model service returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Local model service not available: {e}")
        print("Note: Scripts will use API fallback")
        return False

def main():
    print(f"{'='*60}")
    print(f"HYBRID MONITORING SCRIPTS TEST - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    
    # Check local model
    local_model_available = check_local_model()
    
    # Test all scripts
    results = []
    for script in SCRIPTS:
        success = test_script(script)
        results.append((os.path.basename(script), success))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"Local model available: {'✅ Yes' if local_model_available else '⚠️ No (API fallback will be used)'}")
    print(f"Scripts tested: {total}")
    print(f"Scripts passed: {passed}")
    print(f"Success rate: {passed}/{total} ({passed/total*100:.1f}%)")
    
    print(f"\nDetailed results:")
    for script_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} - {script_name}")
    
    print(f"\n{'='*60}")
    print("NEXT STEPS:")
    print(f"{'='*60}")
    
    if passed == total:
        print("✅ All scripts ready for cron job deployment!")
        print("\nTo deploy, add these lines to crontab (crontab -e):")
        print("""
# Token Limit Monitor (every 30 minutes)
*/30 * * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/hybrid-token-monitor.py >> logs/token-monitor.log 2>&1

# Critical API Alert (every 12 hours)
0 */12 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/hybrid-critical-alert.py >> logs/critical-alert.log 2>&1

# Daily API Usage Check (daily at 9 AM)
0 9 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/hybrid-api-monitor.py >> logs/api-usage.log 2>&1

# Heartbeat Check (every 30 minutes)
*/30 * * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/hybrid-heartbeat.py >> logs/heartbeat.log 2>&1
""")
    else:
        print("⚠️ Some scripts failed. Check errors above before deployment.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())