#!/usr/bin/env python3
"""Test what an App Access Token CAN do"""

import requests
import json

def test_app_token_capabilities():
    """Test capabilities of App Access Token"""
    print("🔍 Testing App Access Token Capabilities")
    print("="*60)
    
    app_id = "935321609011165"
    app_secret = "ab30b2e417c137e6ebbf9f43d7115480"
    app_token = f"{app_id}|{app_secret}"
    
    print(f"App ID: {app_id}")
    print(f"App Token: {app_token[:30]}...")
    print("="*60)
    
    # Test 1: Get app info
    print("\n1️⃣ Getting App Information...")
    try:
        url = f"https://graph.facebook.com/v18.0/{app_id}"
        params = {"access_token": app_token}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ App info retrieved")
            print(f"   Name: {data.get('name', 'Unknown')}")
            print(f"   Category: {data.get('category', 'Unknown')}")
            print(f"   Link: {data.get('link', 'Unknown')}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Error: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Debug token
    print("\n2️⃣ Debugging Token...")
    try:
        url = "https://graph.facebook.com/v18.0/debug_token"
        params = {
            "input_token": app_token,
            "access_token": app_token
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            print(f"   ✅ Token debug successful")
            print(f"   App ID: {data.get('app_id', 'Unknown')}")
            print(f"   Type: {data.get('type', 'Unknown')}")
            print(f"   Is Valid: {data.get('is_valid', False)}")
            print(f"   Scopes: {', '.join(data.get('scopes', []))}")
            
            # Check what this token can do
            scopes = data.get('scopes', [])
            if 'pages_manage_posts' in scopes:
                print(f"   ✅ CAN post to pages")
            else:
                print(f"   ❌ CANNOT post to pages (missing pages_manage_posts)")
                
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Error: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Try to get test users (for development)
    print("\n3️⃣ Checking for Test Users...")
    try:
        url = f"https://graph.facebook.com/v18.0/{app_id}/accounts/test-users"
        params = {"access_token": app_token}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            test_users = data.get('data', [])
            
            if test_users:
                print(f"   ✅ Found {len(test_users)} test user(s)")
                for i, user in enumerate(test_users[:3]):
                    print(f"   {i+1}. ID: {user.get('id', 'Unknown')}")
                    print(f"      Access Token: {user.get('access_token', 'Unknown')[:30]}...")
                    
                    # Test if test user token works
                    test_user_token = user.get('access_token')
                    if test_user_token:
                        test_user_url = "https://graph.facebook.com/v18.0/me"
                        test_params = {"access_token": test_user_token}
                        
                        test_response = requests.get(test_user_url, params=test_params, timeout=5)
                        if test_response.status_code == 200:
                            print(f"      ✅ Test user token works")
                        else:
                            print(f"      ❌ Test user token invalid")
            else:
                print(f"   ⚠️  No test users found")
                print(f"   Create test users in App Dashboard → Roles → Test Users")
                
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Error: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Try app-specific endpoints
    print("\n4️⃣ Testing App-Specific Endpoints...")
    
    endpoints_to_test = [
        ("Get app events", f"{app_id}/events"),
        ("Get app subscriptions", f"{app_id}/subscriptions"),
        ("Get app roles", f"{app_id}/roles"),
    ]
    
    for name, endpoint in endpoints_to_test:
        try:
            url = f"https://graph.facebook.com/v18.0/{endpoint}"
            params = {"access_token": app_token}
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ {name}: Success")
                # Don't print full data to keep output clean
            elif response.status_code == 403:
                print(f"   ❌ {name}: Permission denied")
            else:
                print(f"   ⚠️  {name}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {name}: Error - {e}")
    
    # Test 5: Check if we can generate a user token
    print("\n5️⃣ Checking Token Generation Options...")
    print("   With App Token, you can:")
    print("   - Access app settings")
    print("   - Manage test users")
    print("   - View app insights")
    print("   - Manage app roles")
    print("\n   You CANNOT:")
    print("   - Post to user pages")
    print("   - Access user data")
    print("   - Post to Instagram")
    print("\n   Solution: Need User Access Token")
    print("   Get from: https://developers.facebook.com/tools/explorer/")

def check_app_mode():
    """Check if app is in Development or Live mode"""
    print("\n🔧 Checking App Mode...")
    
    app_id = "935321609011165"
    app_token = f"{app_id}|ab30b2e417c137e6ebbf9f43d7115480"
    
    try:
        # Try to get app settings
        url = f"https://graph.facebook.com/v18.0/{app_id}"
        params = {
            "access_token": app_token,
            "fields": "name,category,link"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            print("   ✅ App is accessible")
            print("   If app is in Development mode:")
            print("   - Only test users/admins can use it")
            print("   - Need to switch to Live mode for production")
            print("\n   Check: https://developers.facebook.com/apps/935321609011165/dashboard/")
            
    except Exception as e:
        print(f"   ❌ Error checking app mode: {e}")

def main():
    """Main test function"""
    print("🧪 App Access Token Capability Test")
    print("="*60)
    
    test_app_token_capabilities()
    check_app_mode()
    
    print("\n" + "="*60)
    print("🎯 RECOMMENDATIONS:")
    print("="*60)
    
    print("\nOption A: Get User Access Token (Recommended)")
    print("   1. Go to Graph API Explorer")
    print("   2. Get User Token with permissions")
    print("   3. Use that token for posting")
    
    print("\nOption B: Use Test Users (Development Only)")
    print("   1. Create test users in App Dashboard")
    print("   2. Use test user tokens")
    print("   3. Only works in Development mode")
    
    print("\nOption C: Switch to Browser Automation")
    print("   1. Install Selenium")
    print("   2. Use Instagram browser automation")
    print("   3. No API tokens needed")
    
    print("\n" + "="*60)
    print("🚀 Quickest Path to Posting:")
    print("="*60)
    print("\n1. Install Selenium: pip install selenium")
    print("2. Configure instagram_config.json")
    print("3. Run: python scripts/instagram_browser_simple.py --login")
    print("4. Post: python scripts/instagram_browser_simple.py --post image.jpg")

if __name__ == "__main__":
    main()