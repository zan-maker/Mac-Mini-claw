#!/usr/bin/env python3
"""
LinkedIn Diagnostic Tool
Tests tokens and provides specific fix instructions
"""

import requests
import json
import os

def test_token(token, token_name="Token"):
    """Test a LinkedIn token and provide detailed diagnostics"""
    print(f"\n🔍 Testing {token_name}: {token[:30]}...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Test 1: Basic profile access
        response = requests.get('https://api.linkedin.com/v2/me', headers=headers, timeout=10)
        
        if response.status_code == 200:
            profile = response.json()
            print(f"   ✅ VALID - Status: {response.status_code}")
            print(f"   👤 User: {profile.get('localizedFirstName', '')} {profile.get('localizedLastName', '')}")
            print(f"   💼 Headline: {profile.get('headline', '')}")
            print(f"   🆔 ID: {profile.get('id', '')}")
            return True, profile
        
        elif response.status_code == 401:
            error_data = response.json()
            error_code = error_data.get('serviceErrorCode', '')
            error_message = error_data.get('message', '')
            
            print(f"   ❌ INVALID - Status: {response.status_code}")
            print(f"   📋 Error Code: {error_code}")
            print(f"   📝 Message: {error_message}")
            
            # Provide specific fixes based on error
            if "INVALID_ACCESS_TOKEN" in error_message:
                print(f"   🔧 Likely Issues:")
                print(f"      1. Token expired or revoked")
                print(f"      2. Missing w_member_social scope")
                print(f"      3. App not authorized")
                print(f"      4. App missing 'Share on LinkedIn' product")
            
            return False, error_data
        
        else:
            print(f"   ⚠️ UNEXPECTED - Status: {response.status_code}")
            print(f"   📋 Response: {response.text[:200]}")
            return False, {"status": response.status_code, "text": response.text}
            
    except Exception as e:
        print(f"   ❌ EXCEPTION: {e}")
        return False, {"exception": str(e)}

def check_app_configuration():
    """Provide app configuration checklist"""
    print("\n" + "="*60)
    print("🔧 LINKEDIN APP CONFIGURATION CHECKLIST")
    print("="*60)
    
    print("\n1. Go to: https://www.linkedin.com/developers/apps")
    print("2. Select your app: 78doynwi86n2js")
    print("\n3. Check these settings:")
    
    print("\n   📋 AUTH TAB:")
    print("   - [ ] OAuth 2.0: Enabled")
    print("   - [ ] Redirect URLs: https://localhost:8000")
    print("   - [ ] Scopes: Includes 'w_member_social'")
    
    print("\n   📋 PRODUCTS TAB:")
    print("   - [ ] Share on LinkedIn: ENABLED (CRITICAL)")
    print("   - [ ] Sign In with LinkedIn: Optional")
    print("   - [ ] Marketing Developer Platform: Optional")
    
    print("\n   📋 SETTINGS TAB:")
    print("   - [ ] Business Email: Verified")
    print("   - [ ] Privacy Policy URL: Set")
    print("   - [ ] Terms of Service URL: Set")
    
    print("\n4. Generate NEW token with correct permissions:")
    print("   - Use OAuth URL with scope=w_member_social")
    print("   - Authorize app in browser")
    print("   - Exchange code for token")

def generate_correct_oauth_url():
    """Generate correct OAuth URL"""
    print("\n" + "="*60)
    print("🔗 CORRECT OAUTH URL")
    print("="*60)
    
    client_id = "78doynwi86n2js"
    redirect_uri = "https://localhost:8000"
    
    auth_url = f"https://www.linkedin.com/oauth/v2/authorization"
    auth_url += f"?response_type=code"
    auth_url += f"&client_id={client_id}"
    auth_url += f"&redirect_uri={redirect_uri}"
    auth_url += f"&scope=w_member_social"  # CRITICAL
    auth_url += f"&state=linkedin_auth"
    
    print(f"\n📋 URL: {auth_url}")
    print("\n📝 Steps:")
    print("1. Open this URL in browser")
    print("2. Authorize with 'w_member_social' permission")
    print("3. You'll be redirected with code=XXXXX")
    print("4. Use that code to get valid token")

def browser_automation_workaround():
    """Provide browser automation workaround"""
    print("\n" + "="*60)
    print("🚀 BROWSER AUTOMATION WORKAROUND")
    print("="*60)
    
    print("\n🎯 RECOMMENDATION: Use browser automation while fixing API")
    print("\n✅ Benefits:")
    print("   - Works immediately (no API approval)")
    print("   - No rate limits")
    print("   - More reliable for posting")
    print("   - Already implemented in our system")
    
    print("\n🔧 Already Configured In:")
    print("   - immediate_social_poster.py")
    print("   - Social media configuration")
    print("   - AI content generation pipeline")
    
    print("\n🚀 Quick Start:")
    print("   1. Run: python3 update_social_credentials.py")
    print("   2. Enter LinkedIn username/password")
    print("   3. Run: python3 immediate_social_poster.py")
    print("   4. Start posting AI finance content TODAY")

def main():
    """Main diagnostic function"""
    print("🔗 LinkedIn Diagnostic Tool")
    print("="*60)
    
    # Test all 3 tokens
    tokens = [
        ("Token 1", "AQUqYLG-MVMSsPEAxkoW8Saf4lDABs54t76jthfzwEUfa24mFIJ4zQkZxiCpFMKDwvgi1TI0gfgeSVP6C0VU6eKOJ2oPZHIowAC9Zb3LdaxTksEGG_KBry9_73oYmHuFA5k5aoOKQB4aRuvnvNtvji2BPF7iILRLapnQKdr8N6bhEkoW2bilepfT_0ME_mdvFeMu_NVuqiDe6C15z-NXS4Md_UCjRNgNK_w0SVUqrK3us6xAEJTZBjovz5xe5MsEkMeGVsvRZm_lMUP_aLA6INDT4T8zx0WT30Q_nezmCStAv132fsfUZvlb_nxO8V_LnAG2576t0m0KHi7oPwETcW8C1w47dQ"),
        ("Token 2", "AQUxmmzaWgp7sr3z1jcBNltMqMAd2Ll54kI2P9h__suW5aVGIymOMa6vQjMNCYkmTs7GbPx0of1jslRawLMi-qkW8vzCubEG4l4jzLTxpRDSkhIP0Cy2Zbe5G5KuHHhRAWD_xYq3ZdmKde1iybGtKjcT9JEuIYQFptjPuOWY5ixWaRUdzr5kJl5TAJoOlu_g-dD_q6qiIuLp4mE_XHfYvKdCKOpkYsfMLgMjrUOo_yzPUCp5UhwejzAb7xMch3zXN8L8YhQ4JcpgJQSy3p5Uq-Z6UJREvj3dzAo4APrwy0NQuENN4RJKJ4KhDLDQFJlyFaDUEZ639LW2yhXR9lrXFOk8FojkmA"),
        ("Token 3", "AQVmHeSLtfVOObQqZyKBbjtGijJI4tR2uxhzFsBbleFIQjB0ISxbv6I4ijKk8pOmVVqQQUNLjtW1g_uKNXkWsRMxpzcpAyK256GQJOzc5oFHRFoPu0I8FdXhGa7Co7IOCE5QuMF9EY37oTQ1DLa2z8xs18n8XKyX7a_gX0sJZlJUOwqt-xw6Lh-fdl1wIY9AHA_gA9XNgIx_Vxsyvsl9qzRgGixwvM4om62Adh4V-g8F5QDxpBom7vNWONvcDXcbHWroDNsS78oGQ9R_focmnWxIdYzRJhE7DC-s666Feu22BUxEAsDtuEorJfz8m_obi5Sb7izV1q8RwvQGcTSo98Xyx4PtMA")
    ]
    
    all_invalid = True
    for token_name, token in tokens:
        valid, _ = test_token(token, token_name)
        if valid:
            all_invalid = False
    
    if all_invalid:
        print("\n" + "="*60)
        print("❌ ALL TOKENS INVALID - App Configuration Issue")
        print("="*60)
        
        # Provide configuration help
        check_app_configuration()
        generate_correct_oauth_url()
        browser_automation_workaround()
        
        print("\n" + "="*60)
        print("🎯 IMMEDIATE ACTION PLAN")
        print("="*60)
        
        print("\n1. Check LinkedIn app configuration (see checklist above)")
        print("2. Generate new token with correct OAuth URL")
        print("3. OR use browser automation workaround (recommended)")
        print("\n🔧 Quick fix commands:")
        print("   python3 update_social_credentials.py")
        print("   python3 immediate_social_poster.py")
    
    else:
        print("\n" + "="*60)
        print("✅ Some tokens are valid!")
        print("="*60)
        print("\n🚀 Ready to post finance AI content!")

if __name__ == "__main__":
    main()