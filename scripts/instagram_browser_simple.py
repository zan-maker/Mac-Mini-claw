#!/usr/bin/env python3
"""
Simple Instagram Browser Automation
Alternative method without Facebook API
"""

import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class InstagramBrowserPoster:
    """Post to Instagram using browser automation"""
    
    def __init__(self, config_path=None):
        self.config_path = config_path or "/Users/cubiczan/.openclaw/workspace/instagram_config.json"
        self.config = self._load_config()
        
        self.driver = None
        self.logged_in = False
        
    def _load_config(self):
        """Load configuration"""
        default_config = {
            "username": "",
            "password": "",
            "headless": False,
            "browser": "chrome",  # chrome, firefox, safari
            "wait_time": 10,
            "image_dir": "/Users/cubiczan/.openclaw/workspace/images",
            "log_dir": "/Users/cubiczan/.openclaw/workspace/logs"
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                print(f"⚠️  Error loading config: {e}")
        
        # Create directories
        os.makedirs(default_config["image_dir"], exist_ok=True)
        os.makedirs(default_config["log_dir"], exist_ok=True)
        
        return default_config
    
    def setup_driver(self):
        """Setup browser driver"""
        browser = self.config["browser"].lower()
        headless = self.config["headless"]
        
        try:
            if browser == "chrome":
                from selenium.webdriver.chrome.options import Options
                options = Options()
                if headless:
                    options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-notifications")
                options.add_argument("--start-maximized")
                
                self.driver = webdriver.Chrome(options=options)
                
            elif browser == "firefox":
                from selenium.webdriver.firefox.options import Options
                options = Options()
                if headless:
                    options.add_argument("--headless")
                
                self.driver = webdriver.Firefox(options=options)
                
            else:
                print(f"❌ Unsupported browser: {browser}")
                return False
            
            # Set implicit wait
            self.driver.implicitly_wait(self.config["wait_time"])
            
            print(f"✅ {browser.capitalize()} driver setup complete")
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup driver: {e}")
            print("Install ChromeDriver: https://chromedriver.chromium.org/")
            return False
    
    def login(self):
        """Login to Instagram"""
        if not self.driver:
            if not self.setup_driver():
                return False
        
        username = self.config["username"]
        password = self.config["password"]
        
        if not username or not password:
            print("❌ Instagram credentials not configured")
            print("Add to instagram_config.json:")
            print('  "username": "your_username",')
            print('  "password": "your_password"')
            return False
        
        try:
            # Navigate to Instagram
            print("🌐 Navigating to Instagram...")
            self.driver.get("https://www.instagram.com")
            time.sleep(3)
            
            # Check if already logged in
            try:
                self.driver.find_element(By.XPATH, "//img[@alt='Instagram']")
                print("✅ Already logged in")
                self.logged_in = True
                return True
            except:
                pass
            
            # Enter username
            print("🔑 Entering username...")
            username_field = self.driver.find_element(By.NAME, "username")
            username_field.clear()
            username_field.send_keys(username)
            time.sleep(1)
            
            # Enter password
            print("🔑 Entering password...")
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(password)
            time.sleep(1)
            
            # Click login
            print("🔄 Logging in...")
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            time.sleep(5)
            
            # Handle "Save Login Info" prompt
            try:
                not_now_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))
                )
                not_now_button.click()
                time.sleep(2)
            except:
                pass
            
            # Handle "Turn On Notifications" prompt
            try:
                not_now_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))
                )
                not_now_button.click()
                time.sleep(2)
            except:
                pass
            
            # Verify login
            try:
                self.driver.find_element(By.XPATH, "//img[@alt='Instagram']")
                print("✅ Login successful!")
                self.logged_in = True
                return True
            except:
                print("❌ Login verification failed")
                return False
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            # Take screenshot for debugging
            self._take_screenshot("login_error")
            return False
    
    def create_post(self, image_path, caption=""):
        """Create a new Instagram post"""
        if not self.logged_in:
            print("❌ Not logged in to Instagram")
            return False
        
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return False
        
        try:
            # Click create button
            print("🆕 Creating new post...")
            
            # Method 1: Try to find create button
            try:
                create_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[text()='Create']"))
                )
                create_button.click()
            except:
                # Method 2: Try plus icon
                try:
                    plus_icon = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//svg[@aria-label='New post']"))
                    )
                    plus_icon.click()
                except:
                    # Method 3: Direct navigation
                    self.driver.get("https://www.instagram.com/create/select/")
            
            time.sleep(3)
            
            # Upload image
            print("📸 Uploading image...")
            file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(os.path.abspath(image_path))
            time.sleep(5)  # Wait for upload
            
            # Click next
            print("➡️ Clicking next...")
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Next']"))
            )
            next_button.click()
            time.sleep(2)
            
            # Click next again (filters page)
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Next']"))
            )
            next_button.click()
            time.sleep(2)
            
            # Enter caption
            print("📝 Entering caption...")
            if caption:
                caption_field = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Write a caption...']"))
                )
                caption_field.click()
                caption_field.send_keys(caption)
                time.sleep(2)
            
            # Share post
            print("🚀 Sharing post...")
            share_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Share']"))
            )
            share_button.click()
            time.sleep(5)
            
            # Verify post was created
            try:
                self.driver.find_element(By.XPATH, "//h2[text()='Your post has been shared.']")
                print("✅ Post created successfully!")
                
                # Log the post
                self._log_post(image_path, caption)
                return True
            except:
                print("⚠️  Post may have been created (verification failed)")
                self._take_screenshot("post_created")
                return True
            
        except Exception as e:
            print(f"❌ Failed to create post: {e}")
            self._take_screenshot("post_error")
            return False
    
    def _take_screenshot(self, name):
        """Take screenshot for debugging"""
        try:
            screenshot_dir = os.path.join(self.config["log_dir"], "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)
            
            self.driver.save_screenshot(filepath)
            print(f"📸 Screenshot saved: {filepath}")
            
        except Exception as e:
            print(f"⚠️  Failed to take screenshot: {e}")
    
    def _log_post(self, image_path, caption):
        """Log post creation"""
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "image": os.path.basename(image_path),
            "caption": caption[:100] + "..." if len(caption) > 100 else caption,
            "status": "success"
        }
        
        log_file = os.path.join(self.config["log_dir"], "instagram_posts.json")
        
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
                
            print(f"📝 Logged Instagram post")
            
        except Exception as e:
            print(f"⚠️  Failed to log post: {e}")
    
    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            print("✅ Browser closed")
    
    def update_config(self, key, value):
        """Update configuration"""
        self.config[key] = value
        
        # Save to file
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"✅ Updated config: {key} = {value}")
        except Exception as e:
            print(f"❌ Failed to save config: {e}")


# Command-line interface
def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Instagram Browser Poster")
    parser.add_argument("--setup", action="store_true", help="Setup browser driver")
    parser.add_argument("--login", action="store_true", help="Login to Instagram")
    parser.add_argument("--post", help="Post image (path)")
    parser.add_argument("--caption", help="Caption for post")
    parser.add_argument("--set-username", help="Set Instagram username")
    parser.add_argument("--set-password", help="Set Instagram password")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    
    args = parser.parse_args()
    
    poster = InstagramBrowserPoster()
    
    if args.headless:
        poster.update_config("headless", True)
    
    if args.set_username:
        poster.update_config("username", args.set_username)
    
    if args.set_password:
        poster.update_config("password", args.set_password)
    
    if args.setup:
        print("🛠️ Setting up browser driver...")
        success = poster.setup_driver()
        if success:
            print("✅ Driver setup complete")
        else:
            print("❌ Driver setup failed")
    
    elif args.login:
        print("🔑 Logging in to Instagram...")
        success = poster.login()
        if success:
            print("✅ Login successful")
        else:
            print("❌ Login failed")
    
    elif args.post:
        if not args.caption:
            args.caption = "Posted by OpenClaw 🤖"
        
        print(f"📸 Posting image: {args.post}")
        print(f"📝 Caption: {args.caption}")
        
        # Ensure logged in
        if not poster.logged_in:
            print("🔄 Logging in first...")
            if not poster.login():
                print("❌ Cannot post without login")
                poster.close()
                return
        
        success = poster.create_post(args.post, args.caption)
        if success:
            print("✅ Post created successfully!")
        else:
            print("❌ Post creation failed")
    
    else:
        print("📱 Instagram Browser Poster")
        print("="*40)
        print("Commands:")
        print("  --setup                    Setup browser driver")
        print("  --login                    Login to Instagram")
        print("  --post /path/to/image.jpg  Post image (requires --caption)")
        print("  --caption \"Your caption\"    Caption for post")
        print("  --set-username USERNAME    Set Instagram username")
        print("  --set-password PASSWORD    Set Instagram password")
        print("  --headless                 Run in headless mode")
        print("\nExample:")
        print("  python instagram_browser_simple.py --setup")
        print("  python instagram_browser_simple.py --login")
        print("  python instagram_browser_simple.py --post image.jpg --caption \"Nice photo!\"")
    
    # Keep browser open for manual inspection
    if poster.driver and (args.setup or args.login or args.post):
        input("Press Enter to close browser...")
    
    poster.close()


if __name__ == "__main__":
    main()