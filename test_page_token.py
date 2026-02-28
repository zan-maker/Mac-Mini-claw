#!/usr/bin/env python3
"""Test if token is actually a Page Access Token"""

import requests
import json

def test_token_type():
    """Test what type of token this is"""
    print("🔍 Testing Token Type")
    print("="*60)
    
    token = "935321609011165|XlL4OvncGEm4iPitzaWrJjbJ1-U"
    
    print(f"Token: {token[:30]}...")
    print("="*60)
    
    # Test 1: Debug token
    print("\n1️⃣ Debugging Token...")
    try:
        url = "https://graph.facebook.com/v18.0/debug_token"
        params = {
            "input_token": token,
            "access_token": token
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            print(f"   ✅ Token debug successful")
            print(f"   App ID: {data.get('app_id', 'Unknown')}")
            print(f"   Type: {data.get('type', 'Unknown')}")
            print(f"   Is Valid: {data.get('is_valid', False)}")
            print(f"   Scopes: {', '.join(data.get('scopes', []))}")
            
            token_type = data.get('type', '')
            if token_type == 'PAGE':
                print(f"   🎉 THIS IS A PAGE ACCESS TOKEN!")
            elif token_type == 'APP':
                print(f"   ⚠️  This is an APP ACCESS TOKEN (not Page)")
            elif token_type == 'USER':
                print(f"   🎉 THIS IS A USER ACCESS TOKEN!")
            else:
                print(f"   ❓ Unknown token type: {token_type}")
                
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Error: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Try to get pages (if it's a user token)
    print("\n2️⃣ Testing Page Access...")
    try:
        url = "https://graph.facebook.com/v18.0/me/accounts"
        params = {"access_token": token}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            pages = data.get('data', [])
            
            if pages:
                print(f"   ✅ Found {len(pages)} page(s) you can access:")
                for i, page in enumerate(pages[:3]):
                    print(f"   {i+1}. {page.get('name', 'Unknown')}")
                    print(f"      ID: {page.get('id', 'Unknown')}")
                    print(f"      Page Token: {page.get('access_token', 'Unknown')[:30]}...")
                    
                    # Test if we can post to this page
                    page_id = page.get('id')
                    page_token = page.get('access_token')
                    
                    if page_id and page_token:
                        test_post_url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
                        test_params = {
                            "access_token": page_token,
                            "message": "Test post from OpenClaw",
                            "published": False  # Don't actually publish
                        }
                        
                        test_response = requests.post(test_post_url, params=test_params, timeout=10)
                        if test_response.status_code == 200:
                            print(f"      ✅ Can post to this page!")
                        else:
                            print(f"      ❌ Cannot post: {test_response.status_code}")
            else:
                print(f"   ⚠️  No pages found or token doesn't have page access")
                
        elif response.status_code == 400:
            print(f"   ❌ Invalid request - token likely doesn't have 'pages_manage_posts' permission")
        elif response.status_code == 403:
            print(f"   ❌ Permission denied - token can't access pages")
        else:
            print(f"   ⚠️  HTTP {response.status_code}: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Try to post directly (if it's a page token)
    print("\n3️⃣ Testing Direct Post...")
    try:
        # First get page ID if it's a page token
        url = "https://graph.facebook.com/v18.0/me"
        params = {"access_token": token}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            page_id = data.get('id')
            page_name = data.get('name', 'Unknown')
            
            print(f"   ✅ Token belongs to: {page_name} (ID: {page_id})")
            
            # Try to post
            post_url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
            post_params = {
                "access_token": token,
                "message": "Test post from OpenClaw - NOT PUBLISHED",
                "published": False  # Don't actually publish
            }
            
            post_response = requests.post(post_url, params=post_params, timeout=10)
            
            if post_response.status_code == 200:
                print(f"   🎉 CAN POST TO PAGE! (test post created as draft)")
                post_id = post_response.json().get('id', 'Unknown')
                print(f"   Post ID: {post_id}")
            else:
                print(f"   ❌ Cannot post: {post_response.status_code}")
                print(f"   Error: {post_response.text[:200]}")
                
        else:
            print(f"   ❌ Cannot get page info: {response.status_code}")
            print(f"   Error: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Check Instagram connection
    print("\n4️⃣ Checking Instagram Connection...")
    try:
        # If we have a page, check if it has Instagram
        url = "https://graph.facebook.com/v18.0/me"
        params = {
            "access_token": token,
            "fields": "instagram_business_account"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            instagram_id = data.get('instagram_business_account', {}).get('id')
            
            if instagram_id:
                print(f"   ✅ Instagram Business Account connected!")
                print(f"   Instagram ID: {instagram_id}")
                
                # Try to get Instagram info
                insta_url = f"https://graph.facebook.com/v18.0/{instagram_id}"
                insta_params = {
                    "access_token": token,
                    "fields": "username,name,profile_picture_url"
                }
                
                insta_response = requests.get(insta_url, params=insta_params, timeout=10)
                if insta_response.status_code == 200:
                    insta_data = insta_response.json()
                    print(f"   Username: @{insta_data.get('username', 'Unknown')}")
                    print(f"   Name: {insta_data.get('name', 'Unknown')}")
            else:
                print(f"   ⚠️  No Instagram Business Account connected to this page")
                
        else:
            print(f"   ❌ Cannot check Instagram: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    """Main test function"""
    print("🧪 Facebook Token Type Test")
    print("="*60)
    
    test_token_type()
    
    print("\n" + "="*60)
    print("🎯 RECOMMENDATIONS:")
    print("="*60)
    
    print("\nIf token is APP ACCESS TOKEN (format: app_id|app_secret):")
    print("   1. Go to Graph API Explorer")
    print("   2. Get User Token with permissions")
    print("   3. Use that token for posting")
    
    print("\nIf token is PAGE ACCESS TOKEN:")
    print("   1. Test posting with facebook_instagram_poster.py")
    print("   2. Check Instagram connection")
    print("   3. Start posting!")
    
    print("\nIf token is USER ACCESS TOKEN:")
    print("   1. Get pages with /me/accounts")
    print("   2. Use page token for posting")
    print("   3. Check Instagram connection")
    
    print("\n" + "="*60)
    print("🚀 Quick Test:")
    print("="*60)
    print("\nRun: python scripts/facebook_instagram_poster.py --test")
    print("Or:  python test_facebook_api.py")

if __name__ == "__main__":
    main()