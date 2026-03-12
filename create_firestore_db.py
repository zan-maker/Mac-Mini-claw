#!/usr/bin/env python3
"""
Attempt to create Firestore database
"""

import subprocess
import sys

print("🚀 Attempting to create Firestore database...")
print("Project: project-651348c0-d39f-4cd5-b8a")
print("Location: us-central1")
print("")

# Try gcloud command
try:
    result = subprocess.run(
        ["gcloud", "firestore", "databases", "create", "--location=us-central1"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Database creation command sent successfully!")
        print(result.stdout)
    else:
        print("⚠️  Database creation may require console setup")
        print("Error:", result.stderr)
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("")
    print("🔧 Please create database manually:")
    print("   1. Go to: https://console.cloud.google.com/firestore")
    print("   2. Click 'Create Database'")
    print("   3. Choose 'Native mode'")
    print("   4. Select location (us-central1)")
    print("   5. Click 'Create'")
