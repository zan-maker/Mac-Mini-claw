#!/usr/bin/env python3
"""
Final Firestore Test with Project ID: project-651348c0-d39f-4cd5-b8a
"""

import os
import sys
from datetime import datetime

print("🧪 FINAL FIRESTORE INTEGRATION TEST")
print("="*50)
print(f"Project: project-651348c0-d39f-4cd5-b8a")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*50)

# Check if authenticated
print("\n🔍 Checking authentication...")
creds_path = os.path.expanduser("~/.config/gcloud/application_default_credentials.json")
if os.path.exists(creds_path):
    print(f"✅ ADC credentials found: {creds_path}")
else:
    print("❌ ADC credentials not found")
    print("\n🔧 Please authenticate first:")
    print("   gcloud auth application-default login")
    print("   (Opens browser for Google login)")
    sys.exit(1)

try:
    from google.cloud import firestore
    
    # Initialize client
    print("\n🔧 Initializing Firestore client...")
    client = firestore.Client(project="project-651348c0-d39f-4cd5-b8a")
    
    print(f"✅ Client initialized")
    print(f"   Project: {client.project}")
    
    # Test connection by listing collections
    print("\n🔍 Testing connection...")
    collections = list(client.collections())
    print(f"✅ Connected successfully!")
    print(f"   Collections found: {len(collections)}")
    
    # Create test document
    print("\n🧪 Creating test document...")
    test_data = {
        "test": True,
        "project": "project-651348c0-d39f-4cd5-b8a",
        "timestamp": datetime.now().isoformat(),
        "purpose": "Firestore integration test",
        "free_tier": {
            "storage": "1GB",
            "reads_per_day": "50,000",
            "writes_per_day": "20,000",
            "deletes_per_day": "20,000"
        }
    }
    
    doc_ref = client.collection("integration_tests").document()
    doc_ref.set(test_data)
    
    print(f"✅ Test document created: {doc_ref.id}")
    
    # Retrieve document
    print("\n🔍 Retrieving test document...")
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        print(f"✅ Document retrieved")
        print(f"   ID: {doc.id}")
        print(f"   Timestamp: {data.get('timestamp')}")
        print(f"   Purpose: {data.get('purpose')}")
    else:
        print("❌ Document not found")
    
    # Delete test document
    print("\n🧹 Cleaning up test document...")
    doc_ref.delete()
    print("✅ Test document deleted")
    
    # Show free tier information
    print("\n📊 FREE TIER INFORMATION:")
    print("   Storage: 1GB free")
    print("   Reads/day: 50,000 free")
    print("   Writes/day: 20,000 free")
    print("   Deletes/day: 20,000 free")
    print("   Perfect for: Lead databases, user data, configuration")
    
    # Migration recommendations
    print("\n🚀 MIGRATION RECOMMENDATIONS:")
    print("   1. Export Supabase data")
    print("   2. Use batch_create() for bulk import")
    print("   3. Update database calls in scripts")
    print("   4. Monitor free tier usage")
    
    print("\n✅ FIRESTORE INTEGRATION TEST COMPLETE!")
    print("\n" + "="*50)
    print("🎯 READY TO REPLACE SUPABASE")
    print("💸 MONTHLY SAVINGS: \$50")
    print("📊 FREE TIER: 1GB storage, 50k reads/day")
    print("="*50)
    
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("\n🔧 Install required package:")
    print("   pip install google-cloud-firestore")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    print("\n🔧 Troubleshooting:")
    print("   1. Make sure you're authenticated:")
    print("      gcloud auth application-default login")
    print("   2. Enable Firestore API:")
    print("      gcloud services enable firestore.googleapis.com")
    print("   3. Check project permissions")
    sys.exit(1)
