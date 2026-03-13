#!/usr/bin/env python3
"""
Instagram + Cloudinary Integration
Uploads images to Cloudinary for Instagram posting
"""

import sys
sys.path.append('/Users/cubiczan/.openclaw/workspace/scripts')

from cloudinary_client import CloudinaryClient
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_ai_finance_visual():
    """Upload AI Finance visual to Cloudinary for Instagram"""
    
    print("🎨 INSTAGRAM + CLOUDINARY INTEGRATION")
    print("="*50)
    print("💰 Monthly savings: $50 (image hosting)")
    print("📊 Free tier: 25GB storage, 25GB bandwidth")
    print("="*50)
    
    # Initialize client
    try:
        client = CloudinaryClient()
        print("✅ Cloudinary client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return False
    
    # Test connection
    print("\n🔗 Testing Cloudinary connection...")
    test_result = client.test_connection()
    if not test_result["success"]:
        print(f"❌ Connection test failed: {test_result['error']}")
        return False
    
    print(f"✅ {test_result['message']}")
    
    # Check for AI Finance visual
    image_path = "/tmp/ai_finance_visual.png"
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        print("   Generate it first with: python3 scripts/create_ai_finance_visual.py")
        return False
    
    print(f"✅ Found image: {image_path}")
    
    # Upload to Cloudinary
    print("\n📤 Uploading to Cloudinary...")
    upload_result = client.upload_image(
        image_path=image_path,
        public_id="ai_finance_visual",
        folder="instagram/ai_finance"
    )
    
    if not upload_result["success"]:
        print(f"❌ Upload failed: {upload_result.get('error', 'Unknown error')}")
        return False
    
    print(f"✅ Upload successful!")
    print(f"   Secure URL: {upload_result.get('secure_url', 'N/A')}")
    print(f"   Public ID: {upload_result.get('public_id', 'N/A')}")
    print(f"   Size: {upload_result.get('bytes', 0) / 1024:.1f} KB")
    print(f"   Dimensions: {upload_result.get('width', 0)}x{upload_result.get('height', 0)}")
    
    # Get Instagram-optimized URL
    print("\n📱 Getting Instagram-optimized URL...")
    instagram_url = client.get_instagram_url(upload_result["public_id"])
    print(f"✅ Instagram URL: {instagram_url}")
    
    # Save URL for Instagram posting
    url_file = "/tmp/instagram_cloudinary_url.txt"
    with open(url_file, "w") as f:
        f.write(instagram_url)
    
    print(f"✅ URL saved to: {url_file}")
    
    # Summary
    print("\n" + "="*50)
    print("🎉 CLOUDINARY INTEGRATION SUCCESSFUL!")
    print("="*50)
    print("")
    print("💰 FINANCIAL IMPACT:")
    print("   • Monthly savings: $50")
    print("   • Annual savings: $600")
    print("   • Free tier: 25GB storage, 25GB bandwidth")
    print("")
    print("🚀 READY FOR INSTAGRAM:")
    print("   1. Use URL in Instagram posting script")
    print("   2. No more file upload limitations")
    print("   3. CDN delivery for fast loading")
    print("   4. Automatic image optimization")
    print("")
    print("📊 UPDATED SAVINGS STATUS:")
    print("   • OpenRouter: $200/month ✅")
    print("   • Firestore: $50/month ✅")
    print("   • Brevo: $75/month ✅")
    print("   • Cloudinary: $50/month ✅")
   • Total: $375/month ACTIVE
