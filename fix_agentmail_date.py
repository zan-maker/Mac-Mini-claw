#!/usr/bin/env python3
"""
Quick fix for AgentMail date serialization issue
"""

import json
from datetime import datetime, date

def date_serializer(obj):
    """JSON serializer for datetime and date objects"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

# Read the original script
with open('/Users/cubiczan/.openclaw/workspace/bdev_ai_agentmail_sender_fixed.py', 'r') as f:
    content = f.read()

# Replace the json.dump calls to use custom serializer
content = content.replace('json.dump(log_data, f, indent=2)', 
                         'json.dump(log_data, f, indent=2, default=date_serializer)')
content = content.replace('json.dump(summary, f, indent=2)',
                         'json.dump(summary, f, indent=2, default=date_serializer)')

# Write the fixed version
with open('/Users/cubiczan/.openclaw/workspace/bdev_ai_agentmail_sender_fixed_fixed.py', 'w') as f:
    f.write(content)

print("Fixed script created: bdev_ai_agentmail_sender_fixed_fixed.py")