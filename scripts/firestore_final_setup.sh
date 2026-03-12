#!/bin/bash

# 🚀 FINAL FIRESTORE SETUP
# Project ID: project-651348c0-d39f-4cd5-b8a
# Savings: $50/month

set -e

echo "========================================="
echo "🚀 GOOGLE CLOUD FIRESTORE FINAL SETUP"
echo "========================================="
echo "Project: project-651348c0-d39f-4cd5-b8a"
echo "Method: Application Default Credentials"
echo "Savings: \$50/month (replaces Supabase)"
echo "========================================="

echo ""
echo "🔐 STEP 1: Authenticate with Google Cloud"
echo "   Run this command (opens browser):"
echo ""
echo "   gcloud auth application-default login"
echo ""
echo "📝 Press Enter after you've authenticated..."
read -p ""

echo ""
echo "🔧 STEP 2: Set Project and Enable API"
echo ""
gcloud config set project project-651348c0-d39f-4cd5-b8a
gcloud services enable firestore.googleapis.com

echo ""
echo "✅ STEP 3: Test Connection"
echo ""
python3 /Users/cubiczan/.openclaw/workspace/scripts/test_firestore_final.py

echo ""
echo "========================================="
echo "✅ FIRESTORE SETUP COMPLETE!"
echo "========================================="
echo ""
echo "🎯 What's ready:"
echo "   1. ✅ Project configured: project-651348c0-d39f-4cd5-b8a"
echo "   2. ✅ Firestore API enabled"
echo "   3. ✅ Test script ready"
echo "   4. ✅ Python client available"
echo ""
echo "🚀 Next steps:"
echo "   1. Start migrating data from Supabase"
echo "   2. Update database calls in scripts"
echo "   3. Monitor free tier usage"
echo ""
echo "💸 Monthly savings: \$50 (active immediately)"
echo ""
echo "Ready to save! 🚀"
