#!/usr/bin/env python3
"""
LinkedIn Token Helper - Generate new access token with correct permissions
"""

import webbrowser
import requests
import json
import os
from urllib.parse import urlencode

class LinkedInTokenHelper:
    """Helper to generate LinkedIn access tokens"""
    
    def __init__(self):
        self.client_id = "78doynwi86n2js"
        self.client_secret = "WPL_AP1.cxC0h4KruYgMBDFe.r9aIBg=="
        self.redirect_uri = "https://localhost:8000"
        
        self.auth_url = "https://www.linkedin.com/oauth/v2/authorization"
        self.token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        
        print("🔗 LinkedIn Token Helper")
        print("="*60)
        print(f"Client ID: {self.client_id}")
        print(f"Redirect URI: {self.redirect_uri}")
        print("="*60)
    
    def generate_auth_url(self):
        """Generate OAuth authorization URL"""
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "w_member_social",  # CRITICAL: Posting permission
            "state": "linkedin_auth_" + os.urandom(8).hex()
        }
        
        auth_url = f"{self.auth_url}?{urlencode(params)}"
        return auth_url
    
    def exchange_code(self, authorization_code):
        """Exchange authorization code for access token"""
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        try:
            response = requests.post(self.token_url, data=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                token_data = response.json()
                return {
                    "success": True,
                    "access_token": token_data.get("access_token"),
                    "expires_in": token_data.get("expires_in"),
                    "token_type": token_data.get("token_type"),
                    "scope": token_data.get("scope")
                }
            else:
                return {
                    "success": False,
                    "error": f"Status {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def save_token(self, access_token, page_id=None):
        """Save access token to file"""
        tokens_path = "/Users/cubiczan/.openclaw/workspace/config/linkedin_tokens.json"
        
        tokens = {
            "access_token": access_token,
            "page_id": page_id,
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "w_member_social"
        }
        
        os.makedirs(os.path.dirname(tokens_path), exist_ok=True)
        
        with open(tokens_path, "w") as f:
            json.dump(tokens, f, indent=2)
        
        print(f"✅ Token saved to: {tokens_path}")
        return tokens_path
    
    def test_token(self, access_token):
        """Test if access token is valid"""
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get("https://api.linkedin.com/v2/me", headers=headers, timeout=10)
            
            if response.status_code == 200:
                profile = response.json()
                return {
                    "valid": True,
                    "user": f"{profile.get('localizedFirstName')} {profile.get('localizedLastName')}",
                    "headline": profile.get("headline", ""),
                    "id": profile.get("id", "")
                }
            else:
                return {
                    "valid": False,
                    "error": f"Status {response.status_code}: {response.text[:200]}"
                }
                
        except Exception as e:
            return {
                "valid": False,
                "error": str(e)
            }

def main():
    """Main function"""
    helper = LinkedInTokenHelper()
    
    print("\n🎯 OPTIONS:")
    print("="*60)
    print("1. Generate new authorization URL")
    print("2. Exchange code for token")
    print("3. Test existing token")
    print("4. Save token manually")
    print("5. Exit")
    
    choice = input("\nSelect option (1-5): ")
    
    if choice == "1":
        auth_url = helper.generate_auth_url()
        
        print(f"\n🔗 Authorization URL:")
        print(f"   {auth_url}")
        
        print("\n📋 IMPORTANT: This URL requests 'w_member_social' permission")
        print("   This allows posting to LinkedIn on your behalf")
        
        open_browser = input("\nOpen in browser? (y/n): ").lower()
        if open_browser == "y":
            webbrowser.open(auth_url)
        
        print("\n📝 After authorizing, you'll be redirected to:")
        print(f"   {helper.redirect_uri}?code=AUTHORIZATION_CODE")
        print("\n   Copy the 'code=' value and use option 2")
    
    elif choice == "2":
        auth_code = input("Authorization code: ").strip()
        
        print("\n🔄 Exchanging code for access token...")
        result = helper.exchange_code(auth_code)
        
        if result["success"]:
            print(f"✅ Token obtained!")
            print(f"   Access Token: {result['access_token'][:30]}...")
            print(f"   Expires in: {result['expires_in']} seconds ({result['expires_in']//86400} days)")
            print(f"   Scope: {result.get('scope', 'Not specified')}")
            
            page_id = input("\nLinkedIn Page ID (optional, press Enter to skip): ").strip()
            helper.save_token(result["access_token"], page_id)
            
            # Test the new token
            print("\n🔗 Testing new token...")
            test_result = helper.test_token(result["access_token"])
            if test_result["valid"]:
                print(f"✅ Token is valid!")
                print(f"   User: {test_result['user']}")
                print(f"   Headline: {test_result['headline']}")
            else:
                print(f"❌ Token test failed: {test_result['error']}")
        else:
            print(f"❌ Failed to get token: {result['error']}")
    
    elif choice == "3":
        # Load existing token
        tokens_path = "/Users/cubiczan/.openclaw/workspace/config/linkedin_tokens.json"
        
        if os.path.exists(tokens_path):
            with open(tokens_path, "r") as f:
                tokens = json.load(f)
            
            access_token = tokens.get("access_token")
            if access_token:
                print(f"\n🔗 Testing existing token: {access_token[:30]}...")
                result = helper.test_token(access_token)
                
                if result["valid"]:
                    print(f"✅ Token is valid!")
                    print(f"   User: {result['user']}")
                    print(f"   Headline: {result['headline']}")
                else:
                    print(f"❌ Token is invalid: {result['error']}")
                    print("\n💡 Recommendation: Generate new token with option 1")
            else:
                print("❌ No access token found in file")
        else:
            print("❌ Token file not found")
    
    elif choice == "4":
        access_token = input("Access token: ").strip()
        page_id = input("Page ID (optional): ").strip() or None
        
        helper.save_token(access_token, page_id)
        
        # Test the token
        print("\n🔗 Testing token...")
        result = helper.test_token(access_token)
        if result["valid"]:
            print(f"✅ Token is valid!")
            print(f"   User: {result['user']}")
            print(f"   Headline: {result['headline']}")
        else:
            print(f"❌ Token is invalid: {result['error']}")
    
    elif choice == "5":
        print("Exiting...")
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()