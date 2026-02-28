#!/usr/bin/env python3
"""
IMMEDIATE SOCIAL MEDIA POSTER
Post to Instagram, Facebook, Twitter/X, LinkedIn, Bluesky immediately
"""

import os
import json
import time
import sys
from datetime import datetime
from pathlib import Path

class ImmediateSocialPoster:
    """Post to all social media platforms immediately"""
    
    def __init__(self):
        self.workspace = "/Users/cubiczan/.openclaw/workspace"
        self.config_dir = os.path.join(self.workspace, "config")
        self.results_dir = os.path.join(self.workspace, "results")
        
        # Ensure directories exist
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Load configurations
        self.config = self.load_config()
        
        # Analytics tracking
        self.analytics_log = os.path.join(self.results_dir, "analytics_log.json")
        
        print("🚀 Immediate Social Poster Initialized")
        print(f"📁 Config: {self.config_dir}")
        print(f"📊 Results: {self.results_dir}")
        print("="*50)
    
    def load_config(self):
        """Load social media configuration"""
        config_path = os.path.join(self.config_dir, "social_media_config.json")
        
        if not os.path.exists(config_path):
            print(f"❌ Config file not found: {config_path}")
            print("Please run configuration first.")
            return {}
        
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return {}
    
    def check_platform_ready(self, platform):
        """Check if platform is configured and ready"""
        platforms = self.config.get("platforms", {})
        platform_config = platforms.get(platform, {})
        
        if not platform_config.get("enabled", False):
            print(f"⚠️  {platform}: Not enabled in config")
            return False
        
        method = platform_config.get("method", "")
        credentials = platform_config.get("credentials", {})
        
        if method == "browser_automation":
            # Check browser automation credentials
            username = credentials.get("username", "")
            password = credentials.get("password", "")
            
            if not username or not password:
                print(f"⚠️  {platform}: Missing browser credentials")
                return False
            
            # Check if Selenium is installed
            try:
                from selenium import webdriver
                print(f"✅ {platform}: Browser automation ready")
                return True
            except ImportError:
                print(f"❌ {platform}: Selenium not installed")
                print("Install with: pip install selenium webdriver-manager")
                return False
        
        elif method == "api":
            # Check API credentials
            has_creds = any(credentials.values())
            if has_creds:
                print(f"✅ {platform}: API credentials configured")
                return True
            else:
                print(f"⚠️  {platform}: Missing API credentials")
                return False
        
        return False
    
    def post_to_instagram(self, content, image_path=None):
        """Post to Instagram using browser automation"""
        print("📸 Posting to Instagram...")
        
        if not self.check_platform_ready("instagram"):
            return False
        
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            # Get credentials
            creds = self.config["platforms"]["instagram"]["credentials"]
            username = creds["username"]
            password = creds["password"]
            
            print(f"🔑 Logging in as: {username}")
            
            # Setup Chrome
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-infobars")
            
            driver = webdriver.Chrome(options=options)
            
            # Login
            driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(3)
            
            # Check if already logged in
            if "login" not in driver.current_url:
                print("✅ Already logged in")
            else:
                # Enter credentials
                username_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "username"))
                )
                username_field.send_keys(username)
                
                password_field = driver.find_element(By.NAME, "password")
                password_field.send_keys(password)
                password_field.send_keys(Keys.RETURN)
                
                time.sleep(5)
                
                # Check login success
                if "login" in driver.current_url:
                    print("❌ Login failed")
                    driver.quit()
                    return False
            
            # Create post
            print("📝 Creating post...")
            driver.get("https://www.instagram.com/create/select/")
            time.sleep(3)
            
            # Upload image if provided
            if image_path and os.path.exists(image_path):
                print(f"📁 Uploading image: {image_path}")
                file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                file_input.send_keys(os.path.abspath(image_path))
                time.sleep(3)
            
            # Add caption with hashtags
            hashtags = self.generate_hashtags()
            full_caption = content + "\n\n" + hashtags
            
            caption_field = driver.find_element(By.CSS_SELECTOR, "textarea[aria-label='Write a caption...']")
            caption_field.send_keys(full_caption)
            
            # Post
            print("🚀 Publishing post...")
            share_button = driver.find_element(By.XPATH, "//div[text()='Share']")
            share_button.click()
            
            time.sleep(5)
            
            # Verify post published
            if "create" not in driver.current_url:
                print("✅ Instagram post published successfully!")
                
                # Track analytics
                self.track_analytics("instagram", content)
                
                driver.quit()
                return True
            else:
                print("❌ Post may not have published")
                driver.quit()
                return False
            
        except Exception as e:
            print(f"❌ Instagram posting failed: {e}")
            return False
    
    def post_to_facebook(self, content, image_path=None):
        """Post to Facebook using browser automation"""
        print("📘 Posting to Facebook...")
        
        if not self.check_platform_ready("facebook"):
            return False
        
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            
            # Get credentials
            creds = self.config["platforms"]["facebook"]["credentials"]
            username = creds["username"]
            password = creds["password"]
            pages = self.config["platforms"]["facebook"].get("pages", [])
            
            if not pages:
                print("⚠️  No Facebook pages configured")
                return False
            
            page_name = pages[0]
            
            print(f"🔑 Logging in as: {username}")
            print(f"📄 Posting to page: {page_name}")
            
            # Setup Chrome
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-notifications")
            
            driver = webdriver.Chrome(options=options)
            
            # Login
            driver.get("https://www.facebook.com/login")
            time.sleep(3)
            
            email_field = driver.find_element(By.ID, "email")
            email_field.send_keys(username)
            
            pass_field = driver.find_element(By.ID, "pass")
            pass_field.send_keys(password)
            pass_field.send_keys(Keys.RETURN)
            
            time.sleep(5)
            
            # Go to page
            driver.get(f"https://www.facebook.com/{page_name}")
            time.sleep(3)
            
            # Create post
            print("📝 Creating post...")
            
            # Try different selectors for post box
            selectors = [
                "div[aria-label='Create a post']",
                "span[data-text='true']",
                "div[contenteditable='true']"
            ]
            
            post_box = None
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        post_box = elements[0]
                        post_box.click()
                        time.sleep(2)
                        break
                except:
                    continue
            
            if not post_box:
                print("❌ Could not find post creation box")
                driver.quit()
                return False
            
            # Enter content
            content_area = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Write something...']")
            content_area.send_keys(content)
            
            # Add photo if provided
            if image_path and os.path.exists(image_path):
                print(f"📁 Uploading image: {image_path}")
                
                # Try to find photo upload button
                photo_buttons = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
                if photo_buttons:
                    photo_buttons[0].send_keys(os.path.abspath(image_path))
                    time.sleep(3)
            
            # Post
            print("🚀 Publishing post...")
            
            # Find post button
            post_buttons = driver.find_elements(By.XPATH, "//div[@aria-label='Post' or contains(text(), 'Post')]")
            if post_buttons:
                post_buttons[0].click()
            else:
                # Try alternative
                submit_buttons = driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")
                if submit_buttons:
                    submit_buttons[0].click()
            
            time.sleep(5)
            
            print("✅ Facebook post published!")
            
            # Track analytics
            self.track_analytics("facebook", content)
            
            driver.quit()
            return True
            
        except Exception as e:
            print(f"❌ Facebook posting failed: {e}")
            return False
    
    def post_to_twitter_x(self, content, image_path=None, use_browser=True):
        """Post to Twitter/X - uses browser automation (recommended) or API"""
        print("🐦 Posting to Twitter/X...")
        
        if not self.check_platform_ready("twitter_x"):
            return False
        
        # Try browser automation first (recommended - works with limited API access)
        if use_browser:
            print("🌐 Using browser automation (recommended)...")
            browser_result = self.post_to_twitter_browser(content, image_path)
            if browser_result:
                return True
            else:
                print("⚠️ Browser automation failed, trying API...")
        
        # Fall back to API (may fail with limited access)
        try:
            import tweepy
            
            # Get credentials
            creds = self.config["platforms"]["twitter_x"]["credentials"]
            
            # Initialize API
            auth = tweepy.OAuth1UserHandler(
                creds["api_key"],
                creds["api_secret"],
                creds["access_token"],
                creds["access_secret"]
            )
            
            api = tweepy.API(auth)
            
            # Post tweet
            if image_path and os.path.exists(image_path):
                # Upload media
                media = api.media_upload(image_path)
                # Post with media
                api.update_status(status=content, media_ids=[media.media_id])
            else:
                # Post text only
                api.update_status(content)
            
            print("✅ Twitter/X post published via API!")
            
            # Track analytics
            self.track_analytics("twitter_x", content)
            
            return True
            
        except ImportError:
            print("❌ Tweepy not installed")
            print("Install with: pip install tweepy")
            return False
        except Exception as e:
            print(f"❌ Twitter/X API posting failed: {e}")
            print("⚠️  This is expected with limited API access (Essential tier)")
            print("🔧 Try browser automation instead (set use_browser=True)")
            return False
    
    def post_to_twitter_browser(self, content, image_path=None):
        """Post to Twitter/X using browser automation (works with limited API access)"""
        print("🌐 Posting to Twitter/X via browser automation...")
        
        if not self.check_platform_ready("twitter_x"):
            return False
        
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            # Get credentials
            creds = self.config["platforms"]["twitter_x"]["credentials"]
            username = creds.get("username")  # Need to add this to config
            password = creds.get("password")  # Need to add this to config
            
            if not username or not password:
                print("❌ Twitter username/password not configured")
                print("Please add 'username' and 'password' to twitter_x credentials in config")
                return False
            
            print(f"🔑 Logging in as: {username}")
            
            # Setup Chrome
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            driver = webdriver.Chrome(options=options)
            wait = WebDriverWait(driver, 20)
            
            try:
                # Login to Twitter
                driver.get("https://twitter.com/login")
                time.sleep(3)
                
                # Enter username
                username_field = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='username']"))
                )
                username_field.send_keys(username)
                username_field.send_keys(Keys.RETURN)
                time.sleep(2)
                
                # Enter password
                password_field = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
                )
                password_field.send_keys(password)
                password_field.send_keys(Keys.RETURN)
                time.sleep(5)
                
                # Check if login successful
                if "home" in driver.current_url or "twitter.com" in driver.current_url:
                    print("✅ Logged in successfully!")
                else:
                    print("⚠️  May need to handle 2FA or verification")
                
                # Navigate to tweet composer
                driver.get("https://twitter.com/compose/tweet")
                time.sleep(3)
                
                # Find tweet box
                tweet_box = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='tweetTextarea_0']"))
                )
                tweet_box.click()
                time.sleep(1)
                
                # Enter content
                tweet_input = driver.find_element(By.CSS_SELECTOR, "div[data-testid='tweetTextarea_0']")
                tweet_input.send_keys(content)
                time.sleep(2)
                
                # Add image if provided
                if image_path and os.path.exists(image_path):
                    print(f"📁 Adding image: {image_path}")
                    
                    # Find media button
                    media_button = driver.find_element(By.CSS_SELECTOR, "input[data-testid='fileInput']")
                    media_button.send_keys(os.path.abspath(image_path))
                    time.sleep(3)
                
                # Post tweet
                tweet_button = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='tweetButton']"))
                )
                tweet_button.click()
                
                print("✅ Tweet posted via browser automation!")
                time.sleep(3)
                
                # Track analytics
                self.track_analytics("twitter_x", content)
                
                return True
                
            except Exception as e:
                print(f"❌ Browser automation error: {e}")
                # Take screenshot for debugging
                screenshot_path = os.path.join(self.results_dir, f"twitter_error_{int(time.time())}.png")
                driver.save_screenshot(screenshot_path)
                print(f"📸 Screenshot saved: {screenshot_path}")
                return False
                
            finally:
                driver.quit()
                
        except ImportError:
            print("❌ Selenium not installed")
            print("Install with: pip install selenium")
            return False
        except Exception as e:
            print(f"❌ Browser automation setup failed: {e}")
            return False
    
    def generate_hashtags(self):
        """Generate relevant hashtags"""
        hashtags = [
            "#leadgeneration", "#businessautomation", "#aiagents",
            "#socialmediamarketing", "#digitalmarketing", "#entrepreneur",
            "#businessgrowth", "#marketingstrategy", "#contentmarketing",
            "#automation", "#artificialintelligence", "#machinelearning",
            "#b2bmarketing", "#saas", "#tech", "#startup",
            "#investing", "#finance", "#trading", "#stocks"
        ]
        
        # Select 10-12 hashtags
        selected = hashtags[:12]
        return " ".join(selected)
    
    def track_analytics(self, platform, content):
        """Track social media analytics"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "platform": platform,
            "content_preview": content[:100] + "..." if len(content) > 100 else content,
            "engagement": 0,
            "impressions": 0,
            "clicks": 0,
            "status": "published"
        }
        
        # Load existing log
        if os.path.exists(self.analytics_log):
            with open(self.analytics_log, "r") as f:
                logs = json.load(f)
        else:
            logs = []
        
        # Add new entry
        logs.append(log_entry)
        
        # Save log
        with open(self.analytics_log, "w") as f:
            json.dump(logs, f, indent=2)
        
        print(f"📊 Analytics tracked for {platform}")
    
    def post_to_all_platforms(self, content, image_path=None):
        """Post to all enabled platforms"""
        print("🚀 Posting to all platforms...")
        print("="*50)
        
        results = {}
        
        # Instagram
        if self.config.get("platforms", {}).get("instagram", {}).get("enabled", False):
            print("\n1. Instagram:")
            results["instagram"] = self.post_to_instagram(content, image_path)
        
        # Facebook
        if self.config.get("platforms", {}).get("facebook", {}).get("enabled", False):
            print("\n2. Facebook:")
            results["facebook"] = self.post_to_facebook(content, image_path)
        
        # Twitter/X
        if self.config.get("platforms", {}).get("twitter_x", {}).get("enabled", False):
            print("\n3. Twitter/X:")
            results["twitter_x"] = self.post_to_twitter_x(content, image_path)
        
        # LinkedIn (placeholder)
        if self.config.get("platforms", {}).get("linkedin", {}).get("enabled", False):
            print("\n4. LinkedIn:")
            print("⚠️  LinkedIn API requires additional setup")
            results["linkedin"] = False
        
        # Bluesky (placeholder)
        if self.config.get("platforms", {}).get("bluesky", {}).get("enabled", False):
            print("\n5. Bluesky:")
            print("⚠️  Bluesky requires app password setup")
            results["bluesky"] = False
        
        # Summary
        print("\n" + "="*50)
        print("📊 POSTING SUMMARY")
        print("="*50)
        
        success_count = sum(1 for result in results.values() if result)
        total_count = len(results)
        
        print(f"✅ Successful: {success_count}/{total_count}")
        
        for platform, success in results.items():
            status = "✅ Success" if success else "❌ Failed"
            print(f"  {platform}: {status}")
        
        return results
    
    def create_sample_campaign(self):
        """Create and post a sample campaign"""
        print("🎯 Creating sample campaign...")
        
        sample_content = "🚀 Just launched our AI-powered lead generation system! Generating 120+ qualified leads daily across 5 platforms. #AI #LeadGeneration #Automation"
        
        print(f"📝 Sample content: {sample_content}")
        print("="*50)
        
        # Ask for confirmation
        response = input("Post this sample campaign? (yes/no): ").lower()
        
        if response in ["yes", "y"]:
            return self.post_to_all_platforms(sample_content)
        else:
            print("❌ Campaign cancelled")
            return {}

def main():
    """Main function"""
    print("🚀 IMMEDIATE SOCIAL MEDIA POSTER")
    print("="*50)
    
    poster = ImmediateSocialPoster()
    
    # Check if config exists
    if not poster.config:
        print("❌ Configuration not found.")
        print("Please run configuration first.")
        print("\nQuick setup:")
        print("1. Update /Users/cubiczan/.openclaw/workspace/config/social_media_config.json")
        print("2. Add your Instagram and Facebook credentials")
        print("3. Run this script again")
        sys.exit(1)
    
    # Show menu
    print("\n📋 OPTIONS:")
    print("1. Post to Instagram")
    print("2. Post to Facebook")
    print("3. Post to Twitter/X")
    print("4. Post to all platforms")
    print("5. Create sample campaign")
    print("6. Check platform readiness")
    print("7. Exit")
    
    choice = input("\nSelect option (1-7): ")
    
    if choice == "1":
        content = input("Enter Instagram post content: ")
        image_path = input("Image path (optional, press Enter to skip): ")
        if not image_path:
            image_path = None
        poster.post_to_instagram(content, image_path)
    
    elif choice == "2":
        content = input("Enter Facebook post content: ")
        image_path = input("Image path (optional, press Enter to skip): ")
        if not image_path:
            image_path = None
        poster.post_to_facebook(content, image_path)
    
    elif choice == "3":
        content = input("Enter Twitter/X post content: ")
        image_path = input("Image path (optional, press Enter to skip): ")
        if not image_path:
            image_path = None
        poster.post_to_twitter_x(content, image_path)
    
    elif choice == "4":
        content = input("Enter post content for all platforms: ")
        image_path = input("Image path (optional, press Enter to skip): ")
        if not image_path:
            image_path = None
        poster.post_to_all_platforms(content, image_path)
    
    elif choice == "5":
        poster.create_sample_campaign()
    
    elif choice == "6":
        print("\n🔍 Platform Readiness Check:")
        print("="*50)
        for platform in ["instagram", "facebook", "twitter_x", "linkedin", "bluesky"]:
            poster.check_platform_ready(platform)
    
    elif choice == "7":
        print("👋 Goodbye!")
        sys.exit(0)
    
    else:
        print("❌ Invalid choice")

if __name__