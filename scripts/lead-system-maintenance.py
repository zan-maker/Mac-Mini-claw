#!/usr/bin/env python3
"""
Weekly Lead System Maintenance
Runs diagnostics and fixes common issues
"""

import os
import sys

# Add workspace to path
workspace = "/Users/cubiczan/.openclaw/workspace"
sys.path.insert(0, workspace)

# Run diagnostics
os.system(f"cd {workspace} && source .env && python3 scripts/diagnose-lead-system.py")

# Run maintenance
os.system(f"cd {workspace} && python3 scripts/run-maintenance.py")

print("✅ Weekly maintenance completed")
