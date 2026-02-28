#!/usr/bin/env python3
"""
Get Correct Facebook Token - Step by Step Guide
"""

import webbrowser
import json
import os

def open_graph_api_explorer():
    """Open Graph API Explorer in browser"""
    print("🚀 Opening Graph API Explorer...")
    url = "https://developers.facebook.com/tools/explorer/"
    webbrowser.open(url)
    print("✅ Browser opened")
    print("\nFollow these steps:")

def step_by_step_guide():
    """Step by step guide to get correct token"""
    print("\n" + "="*60)
    print("📋 STEP-BY-STEP GUIDE TO GET CORRECT TOKEN")
    print("="*60)
    
    print("\n1️⃣ **Go to Graph API Explorer**")
    print("   URL: https://developers.facebook.com/tools/explorer/")
    
    print("\n2️⃣ **Select Your App**")
    print("   Dropdown: Select 'FinbridgeAI' (ID: 935321609011165)")
    
    print("\n3️⃣ **Get User Token**")
    print("   Click: 'Get Token' → 'Get User Access Token'")
    
    print("\n4️⃣ **Select Permissions**")
    print("   Check these boxes:")
    print("   - pages_manage_posts (REQUIRED for posting)")
    print("   - pages_read_engagement")
    print("   - instagram_basic (for Instagram)")
    print("   - instagram_content_publish (for posting to Instagram)")
    
    print("\n5️⃣ **Generate Token**")
    print("   Click: 'Generate Access Token'")
    print("   Copy the token (starts with 'EA...')")
    
    print("\n6️⃣ **Get Page ID**")
    print("   In Graph API Explorer, run:")
    print("   Endpoint: /me/accounts")
    print("   Click: 'Submit'")
    print("   Find your page and copy the Page ID")
    
    print("\n7️⃣ **Get Instagram ID (if needed)**")
    print("   Endpoint: /{page_id}?fields=instagram_business_account")
    print("   Copy the Instagram Business Account ID")
    
    print("\n8️⃣ **Update Configuration**")
    print("   Edit: /Users/cubiczan/.openclaw/workspace/social_config.json")
    print("   Add:")
    print('   {')
    print('     "access_token": "EA...YOUR_NEW_TOKEN_HERE",')
    print('     "page_id": "YOUR_PAGE_ID_HERE",')
    print('     "instagram_id": "YOUR_INSTAGRAM_ID_HERE",')
    print('     "app_id": "935321609011165",')
    print('     "app_secret": "ab30b2e417c137e6ebbf9f43d7115480"')
    print('   }')

def test_with_browser_automation():
    """Test browser automation as alternative"""
    print("\n" + "="*60)
    print("🎯 ALTERNATIVE: BROWSER AUTOMATION (WORKS TODAY)")
    print("="*60)
    
    print("\n✅ **Instagram Browser Automation READY:**")
    print("   File: scripts/instagram_browser_simple.py")
    print("   Status: Production-ready")
    print("   Time to post: 5 minutes")
    
    print("\n📋 **Commands to run:**")
    print("   1. Install Selenium: pip install selenium")
    print("   2. Configure: python scripts/instagram_browser_simple.py --set-username YOUR_USERNAME")
    print("   3. Configure: python scripts/instagram_browser_simple.py --set-password YOUR_PASSWORD")
    print("   4. Test login: python scripts/instagram_browser_simple.py --login")
    print("   5. Post: python scripts/instagram_browser_simple.py --post image.jpg --caption 'Test'")
    
    print("\n🎯 **Why browser automation first?**")
    print("   - Works TODAY (no API approval needed)")
    print("   - Uses personal/business accounts")
    print("   - No token management")
    print("   - Posting works immediately")

def check_app_status():
    """Check app status in Facebook Developer"""
    print("\n" + "="*60)
    print("🔍 CHECK APP STATUS")
    print("="*60)
    
    print("\n**App Dashboard:** https://developers.facebook.com/apps/935321609011165/dashboard/")
    
    print("\n**Check these settings:**")
    print("1. **App Mode:** Should be 'Live' (not Development)")
    print("2. **Permissions:** Add 'pages_manage_posts' to Basic Settings")
    print("3. **App Review:** May need to submit for review")
    print("4. **Test Users:** Can create test users for development")
    
    print("\n**Common Issues:**")
    print("❌ App in Development mode → Switch to Live")
    print("❌ Missing permissions → Add in Basic Settings")
    print("❌ Need App Review → Submit for review")
    print("❌ Token expired → Get new User Token")

def create_quick_test():
    """Create quick test script"""
    print("\n" + "="*60)
    print("🧪 QUICK TEST SCRIPT")
    print("="*60)
    
    test_script = """#!/usr/bin/env python3
import requests

def quick_token_test(token):
    \"\"\"Quick test for any Facebook token\"\"\"
    print(f"Testing token: {token[:30]}...")
    
    # Test 1: What type of token?
    debug_url = "https://graph.facebook.com/v18.0/debug_token"
    debug_params = {
        "input_token": token,
        "access_token": token
    }
    
    try:
        response = requests.get(debug_url, params=debug_params, timeout=10)
        if response.status_code == 200:
            data = response.json().get('data', {})
            token_type = data.get('type', 'Unknown')
            scopes = data.get('scopes', [])
            
            print(f"✅ Token Type: {token_type}")
            print(f"✅ Scopes: {', '.join(scopes)}")
            
            if token_type == 'USER' and 'pages_manage_posts' in scopes:
                print("🎉 THIS IS A VALID USER TOKEN FOR POSTING!")
                return True
            elif token_type == 'PAGE':
                print("🎉 THIS IS A PAGE TOKEN!")
                return True
            else:
                print("⚠️  Token missing required permissions")
                return False
        else:
            print(f"❌ Debug failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # Test current token
    current_token = "935321609011165|XlL4OvncGEm4iPitzaWrJjbJ1-U"
    print("\\n🔍 Testing current token...")
    quick_token_test(current_token)
    
    print("\\n🔍 Test your new token:")
    new_token = input("Paste your new token (starts with EA...): ").strip()
    if new_token:
        quick_token_test(new_token)
"""
    
    script_path = "/Users/cubiczan/.openclaw/workspace/quick_token_test.py"
    with open(script_path, 'w') as f:
        f.write(test_script)
    
    os.chmod(script_path, 0o755)
    print(f"✅ Quick test script created: {script_path}")
    print(f"   Run: python quick_token_test.py")

def main():
    """Main function"""
    print("🔑 Facebook Token Guide")
    print("="*60)
    
    print("\n**CURRENT TOKEN:** `935321609011165|XlL4OvncGEm4iPitzaWrJjbJ1-U`")
    print("**TYPE:** App Access Token (cannot post to pages)")
    print("**ISSUE:** Token has empty scopes (no permissions)")
    
    # Open browser
    open_graph_api_explorer()
    
    # Show guide
    step_by_step_guide()
    
    # Show alternative
    test_with_browser_automation()
    
    # Check app status
    check_app_status()
    
    # Create test script
    create_quick_test()
    
    print("\n" + "="*60)
    print("🎯 RECOMMENDED PATH:")
    print("="*60)
    
    print("\n**Option A: Get User Token (Best for API)**")
    print("   1. Get User Token from Graph API Explorer (2 minutes)")
    print("   2. Test with quick_token_test.py")
    print("   3. Update social_config.json")
    print("   4. Post with facebook_instagram_poster.py")
    
    print("\n**Option B: Browser Automation (Works TODAY)**")
    print("   1. Install Selenium: pip install selenium")
    print("   2. Test Instagram posting (5 minutes)")
    print("   3. Get posting working TODAY")
    print("   4. Get Facebook token later")
    
    print("\n" + "="*60)
    print("🚀 IMMEDIATE ACTION:")
    print("="*60)
    print("\nRun: python quick_token_test.py")
    print("Or:  pip install selenium && python scripts/instagram_browser_simple.py --login")

if __name__ == "__main__":
    main()