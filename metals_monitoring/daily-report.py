#!/usr/bin/env python3
"""
Daily Metals Trading Report
"""

import sys
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add workspace to path
sys.path.append(os.path.expanduser('~/.openclaw/workspace/scripts'))

try:
    from metals_monitoring_daemon import MetalsMonitoringDaemon
    
    print(f"📊 Daily Metals Report - {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 60)
    
    # Initialize daemon
    daemon = MetalsMonitoringDaemon()
    
    # Generate report
    report = daemon.run_daily_report()
    
    # Save report
    report_file = Path(daemon.monitoring_dir) / f"daily_report_{datetime.now().strftime('%Y%m%d')}.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"✅ Report saved: {report_file}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
