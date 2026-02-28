#!/usr/bin/env python3
import requests

def quick_token_test(token):
    """Quick test for any Facebook token"""
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
    print("\n🔍 Testing current token...")
    quick_token_test(current_token)
    
    print("\n🔍 Test your new token:")
    new_token = input("Paste your new token (starts with EA...): ").strip()
    if new_token:
        quick_token_test(new_token)