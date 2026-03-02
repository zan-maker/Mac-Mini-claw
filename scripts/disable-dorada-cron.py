#!/usr/bin/env python3
"""
Disable all Dorada cron jobs since the campaign is 100% complete.
"""

import json
import sys

# Load the jobs.json file
with open('/Users/cubiczan/.openclaw/cron/jobs.json', 'r') as f:
    data = json.load(f)

# Count of Dorada jobs disabled
disabled_count = 0

# Disable all Dorada jobs
for job in data['jobs']:
    if 'Dorada' in job.get('name', ''):
        if job.get('enabled', False):
            job['enabled'] = False
            disabled_count += 1
            print(f"Disabled: {job['name']} (ID: {job['id']})")

# Save the updated file
with open('/Users/cubiczan/.openclaw/cron/jobs.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✅ Disabled {disabled_count} Dorada cron jobs")
print("Campaign is 100% complete - all waves have been sent.")

# Also update the backup file
with open('/Users/cubiczan/.openclaw/cron/jobs.json.bak', 'w') as f:
    json.dump(data, f, indent=2)

print("Backup updated as well.")
