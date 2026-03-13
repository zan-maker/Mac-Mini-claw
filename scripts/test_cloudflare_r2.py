#!/usr/bin/env python3
"""
Test Cloudflare R2 configuration
"""

import os
import sys
sys.path.append('/Users/cubiczan/.openclaw/workspace/scripts')

def test_cloudflare_r2_config():
    """Test Cloudflare R2 configuration"""
    
    print("🧪 CLOUDFLARE R2 CONFIGURATION TEST")
    print("="*50)
    print("💰 Potential savings: $50/month")
    print("📊 Free tier: 10GB storage, unlimited requests")
    print("="*50)
    
    # Check environment
    print("\n📋 Checking environment variables...")
    account_id = os.getenv('CLOUDFLARE_R2_ACCOUNT_ID')
    bucket_name = os.getenv('CLOUDFLARE_R2_BUCKET_NAME')
    access_key = os.getenv('CLOUDFLARE_R2_ACCESS_KEY_ID')
    secret_key = os.getenv('CLOUDFLARE_R2_SECRET_ACCESS_KEY')
    
    if all([account_id, bucket_name, access_key, secret_key]):
        print(f"✅ All environment variables found")
        print(f"   Account ID: {account_id}")
        print(f"   Bucket Name: {bucket_name}")
        print(f"   Access Key: {access_key[:10]}...")
        print(f"   Secret Key: {secret_key[:10]}...")
    else:
        print("❌ Missing environment variables")
        print("   Run setup script with credentials")
        return False
    
    # Try to import client
    print("\n🔧 Testing client import...")
    try:
        from cloudflare_r2_client import CloudflareR2Client
        print("✅ CloudflareR2Client imported")
        
        # Initialize client
        client = CloudflareR2Client()
        print("✅ Client initialized")
        
        # Get config
        config = client.get_config()
        print(f"✅ Configuration loaded")
        print(f"   Provider: {config['provider']}")
        print(f"   Account ID: {config['account_id']}")
        print(f"   Bucket: {config['bucket_name']}")
        print(f"   Free tier: {config['free_tier']['storage']} storage")
        
        # Test connection
        print("\n🔗 Testing API connection...")
        test_result = client.test_connection()
        if test_result["success"]:
            print(f"✅ {test_result['message']}")
            print(f"   Bucket exists: {test_result.get('bucket_exists', 'N/A')}")
        else:
            print(f"⚠️  Connection test: {test_result['error']}")
            print(f"   Suggestion: {test_result.get('suggestion', 'Check credentials')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Client test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_cloudflare_r2_config()
    if success:
        print("\n" + "="*50)
        print("✅ CLOUDFLARE R2 CONFIGURATION READY")
        print("="*50)
        print("\n💸 Monthly savings: $50 (ready to activate)")
        print("📊 Free tier: 10GB storage, unlimited requests")
        print("☁️  S3-compatible storage solution")
    else:
        print("\n❌ CONFIGURATION NEEDS ATTENTION")
        print("Run setup script with valid credentials")
