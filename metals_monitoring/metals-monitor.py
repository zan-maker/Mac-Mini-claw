#!/usr/bin/env python3
"""
Main Metals Monitoring Script - Run by cron jobs
"""

import sys
import os
from datetime import datetime

# Add workspace to path
sys.path.append(os.path.expanduser('~/.openclaw/workspace/scripts'))

try:
    from metals_monitoring_daemon import MetalsMonitoringDaemon
    
    print(f"🔍 Metals Monitoring - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Initialize daemon
    daemon = MetalsMonitoringDaemon()
    
    # Run monitoring
    daemon.monitor_all_metals()
    
    print("✅ Monitoring complete")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
