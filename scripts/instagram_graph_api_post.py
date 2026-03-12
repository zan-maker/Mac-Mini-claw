#!/usr/bin/env python3
"""
Post to Instagram via Graph API
Using the provided API token
"""

import requests
import json
import os
from datetime import datetime

# API Configuration
ACCESS_TOKEN = "935321609011165|XlL4OvncGEm4iPitzaWrJjbJ1-U"
INSTAGRAM_BUSINESS_ACCOUNT_ID = None  # We need to find this

def test_api_token():
    """Test if the API token is valid"""
    print("🔍 Testing Instagram Graph API token...")
    
    # Test with a simple Graph API call
    url = f"https://graph.facebook.com/v18.0/me"
    params = {
        "access_token": ACCESS_TOKEN,
        "fields": "id,name"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "error" in data:
            print(f"❌ Token error: {data['error']['message']}")
            return False
        else:
            print(f"✅ Token valid! User: {data.get('name', 'Unknown')} (ID: {data.get('id', 'Unknown')})")
            return True
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def get_instagram_business_account():
    """Get Instagram Business Account ID linked to Facebook Page"""
    print("\n🔍 Finding Instagram Business Account...")
    
    # First, get pages managed by user
    url = f"https://graph.facebook.com/v18.0/me/accounts"
    params = {
        "access_token": ACCESS_TOKEN,
        "fields": "id,name,instagram_business_account"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "error" in data:
            print(f"❌ Error getting pages: {data['error']['message']}")
            return None
            
        pages = data.get("data", [])
        if not pages:
            print("❌ No Facebook Pages found")
            return None
            
        print(f"✅ Found {len(pages)} Facebook Page(s):")
        for page in pages:
            print(f"   - {page.get('name')} (ID: {page.get('id')})")
            instagram_id = page.get("instagram_business_account", {}).get("id")
            if instagram_id:
                print(f"     📱 Instagram Business Account: {instagram_id}")
                return instagram_id
        
        print("❌ No Instagram Business Account linked to Facebook Pages")
        return None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def create_media_container(instagram_account_id, image_path, caption):
    """Create media container for Instagram post"""
    print(f"\n📦 Creating media container for Instagram post...")
    
    # First, upload image to Facebook
    print("📤 Uploading image to Facebook...")
    
    # Read image file
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return None
    
    with open(image_path, 'rb') as image_file:
        files = {'file': image_file}
        
        # Create media container
        url = f"https://graph.facebook.com/v18.0/{instagram_account_id}/media"
        params = {
            "access_token": ACCESS_TOKEN,
            "caption": caption,
            "image_url": f"file://{image_path}"  # This won't work - need actual upload
        }
        
        try:
            response = requests.post(url, params=params, files=files)
            data = response.json()
            
            if "error" in data:
                print(f"❌ Media creation error: {data['error']['message']}")
                print(f"   Details: {data['error']}")
                return None
            else:
                print(f"✅ Media container created: {data.get('id')}")
                return data.get('id')
                
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return None

def publish_media(instagram_account_id, media_container_id):
    """Publish the media container"""
    print(f"\n📢 Publishing media...")
    
    url = f"https://graph.facebook.com/v18.0/{instagram_account_id}/media_publish"
    params = {
        "access_token": ACCESS_TOKEN,
        "creation_id": media_container_id
    }
    
    try:
        response = requests.post(url, params=params)
        data = response.json()
        
        if "error" in data:
            print(f"❌ Publish error: {data['error']['message']}")
            return False
        else:
            print(f"✅ Media published successfully!")
            print(f"   Post ID: {data.get('id')}")
            return True
            
    except Exception as e:
        print(f"❌ Publish error: {e}")
        return False

def post_via_api_direct():
    """Alternative: Try direct posting if above doesn't work"""
    print("\n🔄 Trying alternative posting method...")
    
    # This is a simplified approach that might work for some setups
    caption = """🚀 AI is transforming finance!

From algorithmic trading to automated analysis, AI tools are revolutionizing how we approach financial markets.

🤖 What we're covering:
• AI-powered trading strategies
• Claude Code for financial automation  
• GitHub repos for finance tasks
• Real-time market analysis

🌐 Learn more: www.impactquadrant.info

Follow for daily insights into AI + Finance!

#AIFinance #AlgorithmicTrading #ClaudeCode #FinancialAI #TradingBots #GitHub #FinTech #Automation #Python #DataScience"""
    
    print("📝 Using caption with impactquadrant.info")
    print(f"📸 Image: /Users/cubiczan/Desktop/ai_finance_instagram_post.png")
    
    # Note: Direct image upload via API requires different approach
    # Usually needs image hosted online or special upload endpoint
    
    return False

def main():
    """Main function"""
    print("=" * 60)
    print("INSTAGRAM GRAPH API POSTING")
    print("=" * 60)
    
    # Test the API token
    if not test_api_token():
        print("\n❌ Cannot proceed with invalid token")
        return
    
    # Get Instagram Business Account ID
    instagram_account_id = get_instagram_business_account()
    
    if not instagram_account_id:
        print("\n⚠️  Could not find Instagram Business Account")
        print("   Trying alternative method...")
        post_via_api_direct()
        return
    
    # Prepare content
    image_path = "/Users/cubiczan/Desktop/ai_finance_instagram_post.png"
    caption_path = "/tmp/ai_finance_caption_updated.txt"
    
    if not os.path.exists(image_path):
        print(f"\n❌ Image not found: {image_path}")
        return
    
    # Read caption
    caption = ""
    if os.path.exists(caption_path):
        with open(caption_path, 'r') as f:
            caption = f.read()
    else:
        caption = "AI Finance visual - Generated by AI"
    
    # Create and publish media
    media_id = create_media_container(instagram_account_id, image_path, caption)
    
    if media_id:
        success = publish_media(instagram_account_id, media_id)
        if success:
            print("\n🎉 POST SUCCESSFUL VIA INSTAGRAM GRAPH API!")
            print("   Your AI Finance visual is now on Instagram!")
        else:
            print("\n❌ Failed to publish media")
    else:
        print("\n❌ Failed to create media container")
        print("\n💡 Alternative: Use Instagram Content Publishing API")
        print("   Requires: Instagram Business Account with connected Facebook Page")
        print("   Steps: 1. Upload image 2. Create media container 3. Publish")

if __name__ == "__main__":
    main()