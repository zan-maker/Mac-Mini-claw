#!/usr/bin/env python3
"""
Fix datetime serialization in AgentMail logging
"""

import json
from datetime import datetime

def datetime_serializer(obj):
    """Custom JSON serializer for datetime objects"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

# Test the fix
test_data = {
    "timestamp": datetime.now(),
    "account": {
        "last_used": datetime.now(),
        "created": datetime(2024, 1, 1)
    },
    "message": "Test with datetime objects"
}

print("Testing datetime serialization fix...")

# Without fix (will fail)
try:
    json.dumps(test_data)
    print("❌ Unexpected: Serialization worked without fix")
except TypeError as e:
    print(f"✅ Expected error: {e}")

# With fix
try:
    serialized = json.dumps(test_data, default=datetime_serializer)
    print(f"✅ Successfully serialized: {len(serialized)} characters")
    
    # Verify it can be loaded back
    loaded = json.loads(serialized)
    print(f"✅ Successfully loaded back")
    print(f"   Timestamp: {loaded['timestamp']}")
    print(f"   Last used: {loaded['account']['last_used']}")
    
except Exception as e:
    print(f"❌ Error with fix: {e}")

print("\n🔧 To apply fix to bdev_ai_agentmail_advanced.py:")
print("""
1. Add this function to the class:
   def datetime_serializer(self, obj):
       if isinstance(obj, datetime):
           return obj.isoformat()
       raise TypeError(f"Type {type(obj)} not serializable")

2. Update the save_results method:
   json.dump(log_data, f, indent=2, default=self.datetime_serializer)
""")

print("\n📋 Quick patch command:")
print("""
sed -i '' 's/json.dump(log_data, f, indent=2)/json.dump(log_data, f, indent=2, default=self.datetime_serializer)/' bdev_ai_agentmail_advanced.py
""")

print("\n✅ After applying fix, the logging will work correctly.")