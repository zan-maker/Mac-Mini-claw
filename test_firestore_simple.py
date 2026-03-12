#!/usr/bin/env python3
"""
Simple Firestore Test
"""

import os
import sys
from datetime import datetime

print("🧪 SIMPLE FIRESTORE TEST")
print("="*50)
print(f"Project: project-651348c0-d39f-4cd5-b8a")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*50)

# Check authentication
print("\n🔍 Checking authentication...")
creds_path = os.path.expanduser("~/.config/gcloud/application_default_credentials.json")
if os.path.exists(creds_path):
    print(f"✅ ADC credentials found: {creds_path}")
else:
    print("❌ ADC credentials not found")
    sys.exit(1)

try:
    # Try to import
    print("\n🔧 Testing imports...")
    from google.cloud import firestore
    print("✅ google.cloud.firestore imported successfully")
    
    # Initialize client
    print("\n🚀 Initializing Firestore client...")
    client = firestore.Client(project="project-651348c0-d39f-4cd5-b8a")
    print(f"✅ Client initialized")
    print(f"   Project: {client.project}")
    
    # Test connection
    print("\n🔗 Testing connection...")
    collections = list(client.collections())
    print(f"✅ Connected successfully!")
    print(f"   Collections found: {len(collections)}")
    
    # Show free tier info
    print("\n📊 FREE TIER INFORMATION:")
    print("   Storage: 1GB free")
    print("   Reads/day: 50,000 free")
    print("   Writes/day: 20,000 free")
    print("   Deletes/day: 20,000 free")
    
    print("\n✅ FIRESTORE SETUP SUCCESSFUL!")
    print("\n" + "="*50)
    print("🎯 READY TO REPLACE SUPABASE")
    print("💸 MONTHLY SAVINGS: $50")
    print("📊 FREE TIER: 1GB storage, 50k reads/day")
    print("="*50)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\n🔧 Try: pip install google-cloud-firestore")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    print("\n🔧 Troubleshooting:")
    print("   1. Make sure Firestore API is enabled")
    print("   2. Check project permissions")
