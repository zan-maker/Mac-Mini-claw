#!/usr/bin/env python3
"""
LinkedIn API Integration
Using provided Client ID and Client Secret
"""

import os
import json
import requests
import webbrowser
from datetime import datetime
from typing import Dict, Any, Optional

class LinkedInIntegration:
    """LinkedIn API integration for social media posting"""
    
    def __init__(self):
        self.workspace = "/Users/cubiczan/.openclaw/workspace"
        self.config_path = os.path.join(self.workspace, "config/social_media_config.json")
        
        # LinkedIn API credentials
        self.client_id = "78doynwi86n2js"
        self.client_secret = "WPL_AP1.cxC0h4KruYgMBDFe.r9aIBg=="
        
        # OAuth endpoints
        self.auth_url = "https://www.linkedin.com/oauth/v2/authorization"
        self.token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        self.api_base = "https://api.linkedin.com/v2"
        
        # Load configuration
        self.config = self.load_config()
        
        # Get stored tokens
        self.access_token = None
        self.page_id = None
        self.load_tokens()
        
        print("🔗 LinkedIn Integration Initialized")
        print(f"📋 Client ID: {self.client_id[:8]}...")
        print(f"🔐 Client Secret: {self.client_secret[:8]}...")
        print("="*60)
    
    def load_config(self):
        """Load social media configuration"""
        if not os.path.exists(self.config_path):
            print(f"❌ Config file not found: {self.config_path}")
            return {}
        
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return {}
    
    def load_tokens(self):
        """Load stored access tokens"""
        tokens_path = os.path.join(self.workspace, "config/linkedin_tokens.json")
        
        if os.path.exists(tokens_path):
            try:
                with open(tokens_path, "r") as f:
                    tokens = json.load(f)
                
                self.access_token = tokens.get("access_token")
                self.page_id = tokens.get("page_id")
                
                if self.access_token:
                    print(f"✅ Loaded access token: {self.access_token[:20]}...")
                if self.page_id:
                    print(f"✅ Loaded page ID: {self.page_id}")
                    
            except Exception as e:
                print(f"⚠️ Error loading tokens: {e}")
    
    def save_tokens(self, access_token: str, page_id: str = None):
        """Save access tokens to file"""
        tokens_path = os.path.join(self.workspace, "config/linkedin_tokens.json")
        
        tokens = {
            "access_token": access_token,
            "page_id": page_id,
            "updated_at": datetime.now().isoformat(),
            "client_id": self.client_id
        }
        
        os.makedirs(os.path.dirname(tokens_path), exist_ok=True)
        
        with open(tokens_path, "w") as f:
            json.dump(tokens, f, indent=2)
        
        self.access_token = access_token
        self.page_id = page_id
        
        print(f"✅ Tokens saved to: {tokens_path}")
        return tokens_path
    
    def get_auth_url(self, redirect_uri: str = "https://localhost:8000") -> str:
        """Generate LinkedIn OAuth authorization URL"""
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "scope": "w_member_social",  # Permission to post on user's behalf
            "state": "linkedin_auth_state"
        }
        
        auth_url = f"{self.auth_url}?response_type={params['response_type']}"
        auth_url += f"&client_id={params['client_id']}"
        auth_url += f"&redirect_uri={params['redirect_uri']}"
        auth_url += f"&scope={params['scope']}"
        auth_url += f"&state={params['state']}"
        
        return auth_url
    
    def exchange_code_for_token(self, authorization_code: str, redirect_uri: str = "https://localhost:8000") -> Optional[Dict]:
        """Exchange authorization code for access token"""
        print("🔄 Exchanging authorization code for access token...")
        
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": redirect_uri,
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
                access_token = token_data.get("access_token")
                expires_in = token_data.get("expires_in", 5184000)  # 60 days default
                
                print(f"✅ Access token obtained (expires in {expires_in//86400} days)")
                print(f"   Token: {access_token[:30]}...")
                
                return {
                    "access_token": access_token,
                    "expires_in": expires_in,
                    "token_type": token_data.get("token_type", "Bearer"),
                    "scope": token_data.get("scope", ""),
                    "success": True
                }
            else:
                print(f"❌ Token exchange failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Token exchange error: {e}")
            return None
    
    def get_user_profile(self) -> Optional[Dict]:
        """Get current user's LinkedIn profile"""
        if not self.access_token:
            print("❌ No access token available")
            return None
        
        url = f"{self.api_base}/me"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                profile = response.json()
                print(f"✅ User profile retrieved: {profile.get('localizedFirstName')} {profile.get('localizedLastName')}")
                return profile
            else:
                print(f"❌ Profile request failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Profile request error: {e}")
            return None
    
    def get_user_pages(self) -> Optional[Dict]:
        """Get LinkedIn pages the user administers"""
        if not self.access_token:
            print("❌ No access token available")
            return None
        
        url = f"{self.api_base}/organizationAcls"
        params = {
            "q": "roleAssignee",
            "role": "ADMINISTRATOR",
            "state": "APPROVED"
        }
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                pages = response.json()
                elements = pages.get("elements", [])
                
                print(f"✅ Found {len(elements)} pages you administer")
                
                for page in elements:
                    org = page.get("organization", "~")
                    print(f"   • {org}")
                
                return pages
            else:
                print(f"❌ Pages request failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Pages request error: {e}")
            return None
    
    def post_to_personal(self, content: str, visibility: str = "PUBLIC") -> Optional[Dict]:
        """Post to personal LinkedIn profile"""
        if not self.access_token:
            print("❌ No access token available")
            return None
        
        url = f"{self.api_base}/ugcPosts"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        payload = {
            "author": f"urn:li:person:{self.get_user_id()}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": content
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 201:
                post_data = response.json()
                print(f"✅ Post published successfully!")
                print(f"   Post ID: {post_data.get('id', 'Unknown')}")
                return post_data
            else:
                print(f"❌ Post failed: {response.status_code}")
                print(f"   Error: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"❌ Post error: {e}")
            return None
    
    def post_to_page(self, content: str, page_id: str = None, visibility: str = "PUBLIC") -> Optional[Dict]:
        """Post to LinkedIn company page"""
        if not self.access_token:
            print("❌ No access token available")
            return None
        
        target_page_id = page_id or self.page_id
        if not target_page_id:
            print("❌ No page ID specified")
            return None
        
        url = f"{self.api_base}/ugcPosts"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        payload = {
            "author": f"urn:li:organization:{target_page_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": content
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 201:
                post_data = response.json()
                print(f"✅ Page post published successfully!")
                print(f"   Post ID: {post_data.get('id', 'Unknown')}")
                return post_data
            else:
                print(f"❌ Page post failed: {response.status_code}")
                print(f"   Error: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"❌ Page post error: {e}")
            return None
    
    def get_user_id(self) -> str:
        """Extract user ID from profile"""
        profile = self.get_user_profile()
        if profile:
            # LinkedIn returns URN like "urn:li:person:12345678"
            urn = profile.get("id", "")
            if ":" in urn:
                return urn.split(":")[-1]
        return ""
    
    def test_connection(self) -> bool:
        """Test LinkedIn API connection"""
        print("🔗 Testing LinkedIn API connection...")
        
        if not self.access_token:
            print("❌ No access token - need to authenticate first")
            return False
        
        profile = self.get_user_profile()
        if profile:
            print(f"✅ Connection successful!")
            print(f"   User: {profile.get('localizedFirstName')} {profile.get('localizedLastName')}")
            print(f"   Headline: {profile.get('headline', 'Not specified')}")
            return True
        else:
            print("❌ Connection failed")
            return False
    
    def update_config(self, enabled: bool = True):
        """Update social media config with LinkedIn settings"""
        if "platforms" not in self.config:
            self.config["platforms"] = {}
        
        self.config["platforms"]["linkedin"] = {
            "enabled": enabled,
            "method": "api",
            "credentials": {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "access_token": self.access_token if self.access_token else "YOUR_ACCESS_TOKEN",
                "page_id": self.page_id if self.page_id else "YOUR_PAGE_ID"
            },
            "post_types": ["article", "image", "video"],
            "optimal_times": ["08:30", "12:30", "17:30"]
        }
        
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)
        
        print(f"✅ LinkedIn configuration updated in: {self.config_path}")

def main():
    """Main LinkedIn integration function"""
    print("🔗 LinkedIn API Integration")
    print("="*60)
    
    # Initialize integration
    linkedin = LinkedInIntegration()
    
    print("\n🎯 OPTIONS:")
    print("="*60)
    print("1. Get OAuth authorization URL")
    print("2. Exchange code for access token")
    print("3. Test API connection")
    print("4. Get user profile")
    print("5. Get user pages")
    print("6. Post to personal profile")
    print("7. Post to company page")
    print("8. Update configuration")
    print("9. Exit")
    
    choice = input("\nSelect option (1-9): ")
    
    if choice == "1":
        redirect_uri = input("Redirect URI [https://localhost:8000]: ") or "https://localhost:8000"
        auth_url = linkedin.get_auth_url(redirect_uri)
        
        print(f"\n🔗 Authorization URL:")
        print(f"   {auth_url}")
        
        open_browser = input("\nOpen in browser? (y/n): ").lower()
        if open_browser == "y":
            webbrowser.open(auth_url)
        
        print("\n📝 After authorizing, you'll get redirected with a code parameter.")
        print("   Copy that code and use option 2 to exchange for access token.")
    
    elif choice == "2":
        auth_code = input("Authorization code: ").strip()
        redirect_uri = input("Redirect URI [https://localhost:8000]: ") or "https://localhost:8000"
        
        token_data = linkedin.exchange_code_for_token(auth_code, redirect_uri)
        
        if token_data and token_data.get("success"):
            page_id = input("LinkedIn Page ID (optional, press Enter to skip): ").strip()
            linkedin.save_tokens(token_data["access_token"], page_id)
    
    elif choice == "3":
        linkedin.test_connection()
    
    elif choice == "4":
        profile = linkedin.get_user_profile()
        if profile:
            print(f"\n📋 Profile Details:")
            print(f"   Name: {profile.get('localizedFirstName')} {profile.get('localizedLastName')}")
            print(f"   Headline: {profile.get('headline', 'Not specified')}")
            print(f"   ID: {profile.get('id', 'Unknown')}")
    
    elif choice == "5":
        pages = linkedin.get_user_pages()
    
    elif choice == "6":
        content = input("Post content: ").strip()
        if content:
            result = linkedin.post_to_personal(content)
            if result:
                print(f"\n✅ Post published: {result.get('id', 'Unknown')}")
    
    elif choice == "7":
        content = input("Page post content: ").strip()
        page_id = input("Page ID (press Enter to use saved): ").strip() or linkedin.page_id
        
        if content and page_id:
            result = linkedin.post_to_page(content, page_id)
            if result:
                print(f"\n✅ Page post published: {result.get('id', 'Unknown')}")
    
    elif choice == "8":
        linkedin.update_config()
    
    elif choice == "9":
        print("Exiting...")
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()