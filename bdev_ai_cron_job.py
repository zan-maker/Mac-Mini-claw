#!/usr/bin/env python3
"""
OpenClaw Cron Job: Bdev.ai + DeepSeek Daily Integration
To be scheduled via OpenClaw cron system
"""

import subprocess
import sys
from datetime import datetime

def main():
    print(f"Bdev.ai + DeepSeek Integration - {datetime.now()}")
    print("="*60)
    
    try:
        # Run the integration
        result = subprocess.run(
            [sys.executable, "bdev_ai_deepseek_integration.py", "--batch-size", "50"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Integration successful")
            print(result.stdout)
        else:
            print("❌ Integration failed")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("="*60)
    print(f"Completed: {datetime.now()}")

if __name__ == "__main__":
    main()
