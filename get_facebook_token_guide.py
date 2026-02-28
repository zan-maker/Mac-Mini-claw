#!/usr/bin/env python3
"""
Guide to get correct Facebook Access Token
"""

def print_token_guide():
    """Print step-by-step guide to get Facebook token"""
    print("🔑 FACEBOOK ACCESS TOKEN GUIDE")
    print("="*60)
    print("\n⚠️  Current token appears to be an APP ACCESS TOKEN")
    print("   Format: 935321609011165|XlL4OvncGEm4iPitzaWrJjbJ1-U")
    print("\n❌ PROBLEM: App tokens can't post to user pages")
    print("✅ SOLUTION: Need USER ACCESS TOKEN with permissions")
    print("="*60)
    
    print("\n🎯 STEP 1: Go to Graph API Explorer")
    print("   URL: https://developers.facebook.com/tools/explorer/")
    print("\n   Steps:")
    print("   1. Click 'Get Token' → 'Get User Access Token'")
    print("   2. Select permissions:")
    print("      - pages_manage_posts")
    print("      - pages_read_engagement")
    print("      - instagram_basic")
    print("      - instagram_content_publish")
    print("   3. Click 'Generate Access Token'")
    print("   4. Copy the token (starts with 'EA...')")
    
    print("\n🎯 STEP 2: Get Page Access Token")
    print("\n   After getting user token:")
    print("   1. In Graph API Explorer, change endpoint to:")
    print("      /me/accounts")
    print("   2. Click 'Submit'")
    print("   3. Find your page in the response")
    print("   4. Copy the page access token from that page")
    
    print("\n🎯 STEP 3: Get Instagram Business Account ID")
    print("\n   If you have Instagram Business connected:")
    print("   1. Use endpoint: /{page-id}")
    print("   2. Add field: ?fields=instagram_business_account")
    print("   3. Submit to get Instagram ID")
    
    print("\n🎯 STEP 4: Update Configuration")
    print("\n   Edit social_config.json:")
    print('   {')
    print('     "access_token": "EA...YOUR_USER_TOKEN_HERE",')
    print('     "page_id": "YOUR_PAGE_ID_HERE",')
    print('     "instagram_id": "YOUR_INSTAGRAM_ID_HERE",')
    print('     "app_id": "935321609011165",')
    print('     "app_secret": "ab30b2e417c137e6ebbf9f43d7115480"')
    print('   }')
    
    print("\n🎯 STEP 5: Test")
    print("\n   Run:")
    print("   python scripts/facebook_instagram_poster.py --test")
    print("   python scripts/facebook_instagram_poster.py --page-info")
    
    print("\n" + "="*60)
    print("📋 TOKEN TYPES EXPLAINED:")
    print("="*60)
    
    print("\n1. APP ACCESS TOKEN (What you have):")
    print("   Format: app_id|app_secret")
    print("   Use: App-level operations")
    print("   Can't: Post to user pages")
    
    print("\n2. USER ACCESS TOKEN (What you need):")
    print("   Format: EAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print("   Use: User-specific operations")
    print("   Can: Post to pages, access Instagram")
    print("   Lifetime: 60 days (needs refresh)")
    
    print("\n3. PAGE ACCESS TOKEN (Best for posting):")
    print("   Format: Also starts with 'EA...'")
    print("   Use: Page-specific operations")
    print("   Can: Post to that specific page")
    print("   Get from: /me/accounts endpoint")
    
    print("\n" + "="*60)
    print("🚀 QUICK FIX: Use Browser Automation Instead")
    print("="*60)
    
    print("\nIf Facebook API is too complex, use browser automation:")
    print("\n1. Install Selenium:")
    print("   pip install selenium")
    print("\n2. Configure Instagram:")
    print("   Edit instagram_config.json with your credentials")
    print("\n3. Test:")
    print("   python scripts/instagram_browser_simple.py --login")
    print("   python scripts/instagram_browser_simple.py --post test.jpg --caption 'Test'")
    
    print("\n" + "="*60)
    print("📞 NEED HELP?")
    print("="*60)
    
    print("\nResources:")
    print("1. Facebook Graph API Docs: https://developers.facebook.com/docs/graph-api")
    print("2. Token Debugger: https://developers.facebook.com/tools/debug/accesstoken/")
    print("3. OpenClaw Community: https://discord.com/invite/clawd")
    
    print("\nCommon Issues:")
    print("1. App not in 'Live' mode → Go to App Dashboard → App Review")
    print("2. Missing permissions → Add in Graph API Explorer")
    print("3. Token expired → Get new token")
    print("4. No Facebook Page → Create at facebook.com/pages/create")

def test_current_token():
    """Test the current token type"""
    print("\n🔍 ANALYZING CURRENT TOKEN...")
    token = "935321609011165|XlL4OvncGEm4iPitzaWrJjbJ1-U"
    
    if "|" in token:
        parts = token.split("|")
        if len(parts) == 2 and parts[0] == "935321609011165":
            print("✅ This is an APP ACCESS TOKEN")
            print(f"   App ID: {parts[0]}")
            print(f"   App Secret hash: {parts[1][:10]}...")
            print("\n❌ CANNOT POST TO PAGES WITH THIS TOKEN")
            print("   Need USER ACCESS TOKEN instead")
            return "app_token"
    
    elif token.startswith("EA"):
        print("✅ This is a USER ACCESS TOKEN")
        print("   Should work for posting")
        return "user_token"
    
    else:
        print("❓ Unknown token format")
        return "unknown"

if __name__ == "__main__":
    print("🧪 Facebook Token Analysis")
    print("="*60)
    
    token_type = test_current_token()
    
    if token_type == "app_token":
        print("\n" + "="*60)
        print_token_guide()
    else:
        print("\n✅ Token format looks good!")
        print("Test with: python scripts/facebook_instagram_poster.py --test")