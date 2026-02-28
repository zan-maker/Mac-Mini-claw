#!/usr/bin/env python3
"""
Facebook & Instagram Poster using Graph API
Simplified implementation for OpenClaw
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path

# Add workspace to path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace')

class SocialMediaPoster:
    """Post to Facebook and Instagram using Graph API"""
    
    def __init__(self, config_path=None):
        self.config_path = config_path or "/Users/cubiczan/.openclaw/workspace/social_config.json"
        self.config = self._load_config()
        
        # API endpoints
        self.graph_url = "https://graph.facebook.com/v18.0"
        
        # Credentials
        self.access_token = self.config.get("access_token")
        self.page_id = self.config.get("page_id")
        self.instagram_id = self.config.get("instagram_id")
        
        if not self.access_token:
            print("⚠️  No access token configured")
            print("Get one from: https://developers.facebook.com/tools/explorer/")
    
    def _load_config(self):
        """Load configuration from file"""
        default_config = {
            "access_token": "",
            "page_id": "",
            "instagram_id": "",
            "app_id": "",
            "app_secret": "",
            "default_caption": "Posted by OpenClaw 🤖",
            "image_dir": "/Users/cubiczan/.openclaw/workspace/images",
            "log_dir": "/Users/cubiczan/.openclaw/workspace/logs"
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    user_config = json.load(f)
                # Merge with defaults
                default_config.update(user_config)
            except Exception as e:
                print(f"⚠️  Error loading config: {e}")
        
        # Create directories if they don't exist
        os.makedirs(default_config["image_dir"], exist_ok=True)
        os.makedirs(default_config["log_dir"], exist_ok=True)
        
        return default_config
    
    def _save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Error saving config: {e}")
            return False
    
    def test_connection(self):
        """Test API connection"""
        if not self.access_token:
            return {"success": False, "error": "No access token"}
        
        try:
            url = f"{self.graph_url}/me"
            params = {"access_token": self.access_token}
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "user": data.get("name", "Unknown"),
                    "id": data.get("id", "Unknown")
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text[:100]}"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_page_info(self):
        """Get Facebook Page information"""
        if not self.page_id:
            return {"success": False, "error": "No page ID configured"}
        
        try:
            url = f"{self.graph_url}/{self.page_id}"
            params = {
                "access_token": self.access_token,
                "fields": "name,instagram_business_account"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "page_name": data.get("name", "Unknown"),
                    "instagram_account": data.get("instagram_business_account", {}).get("id", "Not connected")
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text[:100]}"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def post_to_facebook(self, message, image_path=None):
        """Post to Facebook Page"""
        if not self.page_id:
            return {"success": False, "error": "No page ID configured"}
        
        try:
            url = f"{self.graph_url}/{self.page_id}/photos" if image_path else f"{self.graph_url}/{self.page_id}/feed"
            
            params = {
                "access_token": self.access_token,
                "message": message
            }
            
            if image_path and os.path.exists(image_path):
                # Upload as photo
                with open(image_path, 'rb') as image_file:
                    files = {'source': image_file}
                    response = requests.post(url, params=params, files=files, timeout=30)
            else:
                # Text-only post
                response = requests.post(url, params=params, timeout=10)
            
            if response.status_code == 200:
                post_id = response.json().get('id', 'Unknown')
                self._log_post("facebook", post_id, message, image_path)
                return {
                    "success": True,
                    "post_id": post_id,
                    "platform": "facebook"
                }
            else:
                error_msg = f"HTTP {response.status_code}: {response.text[:200]}"
                self._log_error("facebook", error_msg, message, image_path)
                return {
                    "success": False,
                    "error": error_msg
                }
                
        except Exception as e:
            error_msg = str(e)
            self._log_error("facebook", error_msg, message, image_path)
            return {"success": False, "error": error_msg}
    
    def post_to_instagram(self, caption, image_path):
        """Post to Instagram Business Account"""
        if not self.instagram_id:
            return {"success": False, "error": "No Instagram ID configured"}
        
        if not image_path or not os.path.exists(image_path):
            return {"success": False, "error": f"Image not found: {image_path}"}
        
        try:
            # Step 1: Create media container
            create_url = f"{self.graph_url}/{self.instagram_id}/media"
            
            # For local file, we need to upload to a temporary URL first
            # This is simplified - in production, you'd upload to a CDN or use multipart
            
            params = {
                "access_token": self.access_token,
                "caption": caption,
                "image_url": f"file://{os.path.abspath(image_path)}"
            }
            
            create_response = requests.post(create_url, params=params, timeout=30)
            
            if create_response.status_code != 200:
                error_msg = f"Media creation failed: {create_response.text[:200]}"
                self._log_error("instagram", error_msg, caption, image_path)
                return {
                    "success": False,
                    "error": error_msg
                }
            
            creation_id = create_response.json().get('id')
            
            # Step 2: Publish media
            publish_url = f"{self.graph_url}/{self.instagram_id}/media_publish"
            publish_params = {
                "access_token": self.access_token,
                "creation_id": creation_id
            }
            
            publish_response = requests.post(publish_url, params=publish_params, timeout=10)
            
            if publish_response.status_code == 200:
                post_id = publish_response.json().get('id', 'Unknown')
                self._log_post("instagram", post_id, caption, image_path)
                return {
                    "success": True,
                    "post_id": post_id,
                    "platform": "instagram"
                }
            else:
                error_msg = f"Publish failed: {publish_response.text[:200]}"
                self._log_error("instagram", error_msg, caption, image_path)
                return {
                    "success": False,
                    "error": error_msg
                }
                
        except Exception as e:
            error_msg = str(e)
            self._log_error("instagram", error_msg, caption, image_path)
            return {"success": False, "error": error_msg}
    
    def _log_post(self, platform, post_id, message, image_path=None):
        """Log successful post"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "platform": platform,
            "post_id": post_id,
            "message": message[:100] + "..." if len(message) > 100 else message,
            "image": os.path.basename(image_path) if image_path else None,
            "status": "success"
        }
        
        log_file = os.path.join(self.config["log_dir"], f"posts_{datetime.now().strftime('%Y-%m')}.json")
        
        try:
            # Load existing logs
            logs = []
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            
            # Add new entry
            logs.append(log_entry)
            
            # Save logs
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
            print(f"📝 Logged {platform} post: {post_id}")
            
        except Exception as e:
            print(f"⚠️  Failed to log post: {e}")
    
    def _log_error(self, platform, error, message, image_path=None):
        """Log error"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "platform": platform,
            "error": error[:200],
            "message": message[:100] + "..." if len(message) > 100 else message,
            "image": os.path.basename(image_path) if image_path else None,
            "status": "error"
        }
        
        log_file = os.path.join(self.config["log_dir"], f"errors_{datetime.now().strftime('%Y-%m')}.json")
        
        try:
            # Load existing logs
            logs = []
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            
            # Add new entry
            logs.append(log_entry)
            
            # Save logs
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
            print(f"📝 Logged {platform} error: {error[:50]}...")
            
        except Exception as e:
            print(f"⚠️  Failed to log error: {e}")
    
    def update_config(self, key, value):
        """Update configuration"""
        self.config[key] = value
        self._save_config()
        print(f"✅ Updated config: {key} = {value}")
        
        # Update instance variables
        if key == "access_token":
            self.access_token = value
        elif key == "page_id":
            self.page_id = value
        elif key == "instagram_id":
            self.instagram_id = value


# Command-line interface
def main():
    """Command-line interface for testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Facebook & Instagram Poster")
    parser.add_argument("--test", action="store_true", help="Test API connection")
    parser.add_argument("--page-info", action="store_true", help="Get page information")
    parser.add_argument("--facebook", help="Post to Facebook (message)")
    parser.add_argument("--instagram", help="Post to Instagram (caption)")
    parser.add_argument("--image", help="Image path for post")
    parser.add_argument("--set-token", help="Set access token")
    parser.add_argument("--set-page", help="Set page ID")
    parser.add_argument("--set-instagram", help="Set Instagram ID")
    
    args = parser.parse_args()
    
    poster = SocialMediaPoster()
    
    if args.test:
        print("🔌 Testing API connection...")
        result = poster.test_connection()
        print(json.dumps(result, indent=2))
    
    elif args.page_info:
        print("📄 Getting page information...")
        result = poster.get_page_info()
        print(json.dumps(result, indent=2))
    
    elif args.set_token:
        poster.update_config("access_token", args.set_token)
    
    elif args.set_page:
        poster.update_config("page_id", args.set_page)
    
    elif args.set_instagram:
        poster.update_config("instagram_id", args.set_instagram)
    
    elif args.facebook:
        print("📘 Posting to Facebook...")
        result = poster.post_to_facebook(args.facebook, args.image)
        print(json.dumps(result, indent=2))
    
    elif args.instagram:
        if not args.image:
            print("❌ Instagram requires an image (use --image)")
        else:
            print("📸 Posting to Instagram...")
            result = poster.post_to_instagram(args.instagram, args.image)
            print(json.dumps(result, indent=2))
    
    else:
        print("📱 Facebook & Instagram Poster")
        print("="*40)
        print("Commands:")
        print("  --test                    Test API connection")
        print("  --page-info               Get page information")
        print("  --facebook \"message\"      Post to Facebook")
        print("  --instagram \"caption\"     Post to Instagram (requires --image)")
        print("  --image /path/to/image.jpg  Image for post")
        print("  --set-token TOKEN         Set access token")
        print("  --set-page PAGE_ID        Set Facebook page ID")
        print("  --set-instagram IG_ID     Set Instagram business ID")
        print("\nExample:")
        print("  python facebook_instagram_poster.py --test")
        print("  python facebook_instagram_poster.py --facebook \"Hello World!\"")
        print("  python facebook_instagram_poster.py --instagram \"Nice photo!\" --image photo.jpg")


if __name__ == "__main__":
    main()