#!/bin/bash

# 🚀 Google Cloud Firestore Setup with Application Default Credentials
# No service account key needed!

set -e

echo "========================================="
echo "🚀 GOOGLE CLOUD FIRESTORE SETUP (ADC)"
echo "========================================="
echo "Method: Application Default Credentials"
echo "No service account key needed!"
echo "Free: 1GB storage, 50k reads/day"
echo "Savings: \$50/month"
echo "========================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK not found"
    echo ""
    echo "📦 Installing Google Cloud SDK..."
    
    # For macOS
    if [[ "$(uname)" == "Darwin" ]]; then
        echo "   Download Google Cloud SDK for macOS:"
        echo "   https://cloud.google.com/sdk/docs/install#mac"
        echo ""
        echo "   Or install via Homebrew:"
        echo "   brew install --cask google-cloud-sdk"
        echo ""
        read -p "Install via Homebrew? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            brew install --cask google-cloud-sdk
        else
            echo "⚠️  Please install Google Cloud SDK manually"
            exit 1
        fi
    else
        echo "⚠️  Please install Google Cloud SDK for your OS"
        exit 1
    fi
fi

echo ""
echo "🔐 Step 1: Authenticate with Google Cloud"
echo "   This will open a browser for you to login..."
echo ""
read -p "Ready to authenticate? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Authentication required"
    exit 1
fi

# Authenticate
gcloud auth application-default login

echo ""
echo "✅ Authentication complete!"
echo ""

# Get project list
echo "📋 Step 2: Select Google Cloud Project"
echo ""
echo "Your Google Cloud projects:"
gcloud projects list --format="table(projectId,name)"

echo ""
echo "📝 Enter your Project ID (e.g., 'my-project-123456'):"
read -r PROJECT_ID

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Project ID required"
    exit 1
fi

# Set project
gcloud config set project "$PROJECT_ID"

# Enable Firestore API
echo ""
echo "🔧 Step 3: Enabling Firestore API..."
gcloud services enable firestore.googleapis.com

# Create configuration
CONFIG_DIR="/Users/cubiczan/.openclaw/workspace/config"
mkdir -p "$CONFIG_DIR"

cat > "$CONFIG_DIR/firestore_adc_config.json" << EOL
{
    "provider": "google-cloud-firestore",
    "method": "application_default_credentials",
    "project_id": "$PROJECT_ID",
    "configured_at": "$(date -Iseconds)",
    "free_tier": "1GB storage, 50k reads/day, 20k writes/day",
    "note": "Using Application Default Credentials - no key file needed"
}
EOL

echo "✅ Configuration saved: $CONFIG_DIR/firestore_adc_config.json"

# Create environment file
ENV_FILE="$CONFIG_DIR/.env"
echo "GOOGLE_CLOUD_PROJECT=$PROJECT_ID" >> "$ENV_FILE"
echo "GOOGLE_APPLICATION_CREDENTIALS=adc" >> "$ENV_FILE"
echo "✅ Environment variables updated"

# Create simple test script
TEST_FILE="/Users/cubiczan/.openclaw/workspace/scripts/test_firestore_adc.py"

cat > "$TEST_FILE" << 'EOL'
#!/usr/bin/env python3
"""
Test Firestore with Application Default Credentials
"""

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""  # Use ADC

from google.cloud import firestore

def test_firestore_adc():
    """Test Firestore with ADC"""
    print("🧪 Testing Firestore with Application Default Credentials")
    print("="*50)
    
    try:
        # Initialize client (uses ADC automatically)
        client = firestore.Client()
        
        print("✅ Firestore client initialized with ADC")
        
        # Test connection by listing collections
        collections = list(client.collections())
        print(f"✅ Connected to project: {client.project}")
        print(f"   Collections found: {len(collections)}")
        
        # Create a test document
        test_data = {
            "name": "ADC Test",
            "timestamp": "now",
            "test": True
        }
        
        doc_ref = client.collection("adc_tests").document()
        doc_ref.set(test_data)
        
        print(f"✅ Test document created: {doc_ref.id}")
        
        # Retrieve the document
        doc = doc_ref.get()
        if doc.exists:
            print(f"✅ Document retrieved: {doc.to_dict().get('name')}")
        
        # Delete test document
        doc_ref.delete()
        print("✅ Test document cleaned up")
        
        print("\n📊 Free Tier Information:")
        print("   Storage: 1GB free")
        print("   Reads/day: 50,000 free")
        print("   Writes/day: 20,000 free")
        print("   Deletes/day: 20,000 free")
        
        print("\n✅ Firestore ADC test complete!")
        print("🎯 Ready to replace Supabase")
        print("💸 Monthly savings: $50")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Run: gcloud auth application-default login")
        print("   2. Make sure Firestore API is enabled")
        print("   3. Check project permissions")
        return False

if __name__ == "__main__":
    success = test_firestore_adc()
    if success:
        print("\n" + "="*50)
        print("✅ FIRESTORE ADC SETUP COMPLETE")
        print("="*50)
    else:
        print("\n❌ FIRESTORE ADC SETUP FAILED")
EOL

chmod +x "$TEST_FILE"
echo "✅ Test script created: $TEST_FILE"

echo ""
echo "========================================="
echo "✅ FIRESTORE ADC SETUP COMPLETE!"
echo "========================================="
echo ""
echo "🎯 What's ready:"
echo "   1. ✅ Authenticated with Google Cloud"
echo "   2. ✅ Project set: $PROJECT_ID"
echo "   3. ✅ Firestore API enabled"
echo "   4. ✅ Configuration saved"
echo "   5. ✅ Test script ready"
echo ""
echo "🚀 Next steps:"
echo "   1. Run test: python3 scripts/test_firestore_adc.py"
echo "   2. Start migrating data from Supabase"
echo "   3. Update scripts to use Firestore"
echo ""
echo "💸 Monthly savings: \$50 (replaces Supabase)"
echo ""
echo "Ready to test? 🚀"
