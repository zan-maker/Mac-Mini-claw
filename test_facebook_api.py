#!/usr/bin/env python3
"""Test Facebook Graph API credentials"""

import requests
import json
import sys

def test_app_credentials(app_id, app_secret, access_token):
    """Test Facebook App credentials"""
    print("🔑 Testing Facebook App Credentials...")
    print(f"App ID: {app_id}")
    print(f"App Secret: {app_secret[:10]}...")
    print(f"Access Token: {access_token[:30]}...")
    print("="*60)
    
    # Test 1: Test app access
    print("\n1️⃣ Testing App Access...")
    try:
        url = f"https://graph.facebook.com/v18.0/{app_id}"
        params = {
            "access_token": f"{app_id}|{app_secret}"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS! App verified")
            print(f"   App Name: {data.get('name', 'Unknown')}")
            print(f"   App ID: {data.get('id', 'Unknown')}")
        else:
            print(f"   ❌ FAILED: HTTP {response.status_code}")
            print(f"   Error: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False
    
    # Test 2: Test user access token
    print("\n2️⃣ Testing User Access Token...")
    try:
        url = "https://graph.facebook.com/v18.0/me"
        params = {
            "access_token": access_token
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS! Token valid")
            print(f"   User ID: {data.get('id', 'Unknown')}")
            print(f"   Name: {data.get('name', 'Unknown')}")
            
            # Check token permissions
            debug_url = "https://graph.facebook.com/v18.0/debug_token"
            debug_params = {
                "input_token": access_token,
                "access_token": f"{app_id}|{app_secret}"
            }
            
            debug_response = requests.get(debug_url, params=debug_params, timeout=10)
            if debug_response.status_code == 200:
                debug_data = debug_response.json().get('data', {})
                print(f"   Expires at: {debug_data.get('expires_at', 'Never')}")
                print(f"   Scopes: {', '.join(debug_data.get('scopes', []))}")
                
                # Check for required permissions
                required_scopes = ['pages_manage_posts', 'instagram_content_publish']
                current_scopes = debug_data.get('scopes', [])
                missing = [s for s in required_scopes if s not in current_scopes]
                
                if missing:
                    print(f"   ⚠️  Missing permissions: {', '.join(missing)}")
                else:
                    print(f"   ✅ All required permissions present")
            
        else:
            print(f"   ❌ FAILED: HTTP {response.status_code}")
            print(f"   Error: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False
    
    # Test 3: Get pages
    print("\n3️⃣ Getting Facebook Pages...")
    try:
        url = "https://graph.facebook.com/v18.0/me/accounts"
        params = {
            "access_token": access_token
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            pages = data.get('data', [])
            
            if pages:
                print(f"   ✅ Found {len(pages)} page(s):")
                for i, page in enumerate(pages):
                    print(f"   {i+1}. {page.get('name', 'Unknown')} (ID: {page.get('id', 'Unknown')})")
                    
                    # Check if page has Instagram connected
                    if page.get('instagram_business_account'):
                        print(f"      📸 Instagram connected: {page['instagram_business_account']['id']}")
            else:
                print(f"   ⚠️  No pages found")
                print(f"   You need a Facebook Page to post")
                print(f"   Create one at: https://www.facebook.com/pages/create/")
                
        else:
            print(f"   ❌ FAILED: HTTP {response.status_code}")
            print(f"   Error: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    return True

def test_page_post(page_id, access_token):
    """Test posting to a page"""
    if not page_id:
        print("\n⚠️  No page ID configured for posting test")
        return False
    
    print(f"\n4️⃣ Testing Page Post (ID: {page_id})...")
    
    try:
        # First, get page access token
        url = f"https://graph.facebook.com/v18.0/{page_id}"
        params = {
            "access_token": access_token,
            "fields": "access_token"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            page_data = response.json()
            page_token = page_data.get('access_token')
            
            if page_token:
                print(f"   ✅ Got page access token")
                
                # Test a simple post
                post_url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
                post_params = {
                    "access_token": page_token,
                    "message": "Test post from OpenClaw API 🤖",
                    "published": "false"  # Don't actually publish
                }
                
                post_response = requests.post(post_url, params=post_params, timeout=10)
                
                if post_response.status_code == 200:
                    print(f"   ✅ Post test successful (not published)")
                    print(f"   Post ID: {post_response.json().get('id', 'Unknown')}")
                    return True
                else:
                    print(f"   ❌ Post test failed: HTTP {post_response.status_code}")
                    print(f"   Error: {post_response.text[:200]}")
                    return False
            else:
                print(f"   ❌ Could not get page access token")
                return False
        else:
            print(f"   ❌ Could not access page: HTTP {response.status_code}")
            print(f"   Error: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Facebook Graph API Credentials Test")
    print("="*60)
    
    # Credentials from user
    app_id = "935321609011165"
    app_secret = "ab30b2e417c137e6ebbf9f43d7115480"
    access_token = "935321609011165|XlL4OvncGEm4iPitzaWrJjbJ1-U"
    
    # Test credentials
    credentials_ok = test_app_credentials(app_id, app_secret, access_token)
    
    print("\n" + "="*60)
    
    if credentials_ok:
        print("✅ CREDENTIALS ARE VALID!")
        print("\n🎯 Next steps:")
        print("   1. Create a Facebook Page (if you don't have one)")
        print("   2. Get your Page ID")
        print("   3. Update social_config.json with Page ID")
        print("   4. Connect Instagram Business account to Page")
        print("   5. Test posting with facebook_instagram_poster.py")
        
        # Check if we should test with a page
        print("\n🔧 To test with a page:")
        print("   python test_facebook_api.py --page-id YOUR_PAGE_ID")
        
    else:
        print("❌ CREDENTIALS NEED ATTENTION")
        print("\n🔧 Check:")
        print("   1. App is created in Facebook Developer")
        print("   2. App is in 'Live' mode (not Development)")
        print("   3. Token has required permissions")
        print("   4. App Secret is correct")

if __name__ == "__main__":
    main()