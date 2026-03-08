#!/usr/bin/env python3
"""
LinkedIn Auto-Poster using Selenium
Run this script to automatically post to LinkedIn
"""

import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class LinkedInAutoPoster:
    """Automate LinkedIn posting using Selenium"""
    
    def __init__(self, headless=False):
        self.workspace = "/Users/cubiczan/.openclaw/workspace"
        self.content_file = os.path.join(self.workspace, "social_media/sam_post_1_ai_finance.json")
        
        # Chrome options
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        # User data directory for persistent login
        user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome")
        if os.path.exists(user_data_dir):
            options.add_argument(f'--user-data-dir={user_data_dir}')
            options.add_argument('--profile-directory=Default')
        
        print("🚀 Starting Chrome driver...")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        
        print("✅ Chrome driver started")
    
    def load_content(self):
        """Load post content from JSON file"""
        with open(self.content_file, 'r') as f:
            data = json.load(f)
        
        print(f"📝 Loaded content: {data['title']}")
        return data
    
    def login_to_linkedin(self, email=None, password=None):
        """Log in to LinkedIn"""
        print("🔐 Logging in to LinkedIn...")
        
        self.driver.get("https://www.linkedin.com/login")
        time.sleep(3)
        
        # Check if already logged in
        if "feed" in self.driver.current_url or "LinkedIn" in self.driver.title:
            print("✅ Already logged in")
            return True
        
        # Try to log in if credentials provided
        if email and password:
            try:
                email_field = self.wait.until(
                    EC.presence_of_element_located((By.ID, "username"))
                )
                password_field = self.driver.find_element(By.ID, "password")
                
                email_field.send_keys(email)
                password_field.send_keys(password)
                password_field.send_keys(Keys.RETURN)
                
                time.sleep(5)
                
                # Check for successful login
                if "feed" in self.driver.current_url:
                    print("✅ Login successful")
                    return True
                else:
                    print("❌ Login may have failed")
                    return False
                    
            except Exception as e:
                print(f"❌ Login error: {e}")
                return False
        
        # Manual login required
        print("⚠️ Please log in manually in the browser window...")
        print("   After logging in, press Enter here to continue.")
        input("   Press Enter when ready: ")
        
        return True
    
    def create_post(self, content_data):
        """Create and publish a LinkedIn post"""
        print("📝 Creating new post...")
        
        # Navigate to home feed
        self.driver.get("https://www.linkedin.com/feed/")
        time.sleep(3)
        
        try:
            # Find and click "Start a post" button
            post_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.share-box-feed-entry__trigger"))
            )
            post_button.click()
            time.sleep(2)
            
            # Find post text area
            post_area = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.ql-editor"))
            )
            
            # Clear and enter post content
            post_area.click()
            post_area.clear()
            post_area.send_keys(content_data["content"])
            
            print("✅ Post content entered")
            time.sleep(2)
            
            # Click Post button
            post_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.share-actions__primary-action"))
            )
            post_button.click()
            
            print("✅ Post published!")
            time.sleep(5)
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating post: {e}")
            return False
    
    def post_as_sam(self):
        """Post as Sam Desigan"""
        print("\n" + "="*60)
        print("POSTING AS SAM DESIGAN")
        print("="*60)
        
        # Load content
        content = self.load_content()
        
        # Log in (will use existing session or prompt for manual login)
        if self.login_to_linkedin():
            # Create post
            if self.create_post(content):
                print(f"\n🎉 SUCCESS: Posted '{content['title']}' as Sam Desigan")
                print(f"📊 Check: https://www.linkedin.com/in/sam-desigan-198a742a7/")
                return True
            else:
                print("❌ Failed to create post")
                return False
        else:
            print("❌ Failed to log in")
            return False
    
    def run(self):
        """Main execution"""
        try:
            success = self.post_as_sam()
            
            if success:
                print("\n" + "="*60)
                print("✅ AUTOMATED POSTING COMPLETE")
                print("="*60)
                print("\nNext steps:")
                print("1. Have Shyam Desigan like and comment on the post")
                print("2. Both respond to comments within 24 hours")
                print("3. Run this script tomorrow for Shyam's post")
            else:
                print("\n❌ Automated posting failed")
                print("Try manual posting with the content file:")
                print(f"   cat {self.content_file} | jq '.content'")
            
            # Keep browser open for inspection
            print("\nBrowser will remain open for 60 seconds...")
            print("Close it manually or wait for auto-close.")
            time.sleep(60)
            
        finally:
            self.driver.quit()
            print("\n🚪 Browser closed")

def main():
    """Main function with user prompts"""
    
    print("="*60)
    print("LINKEDIN AUTO-POSTER")
    print("="*60)
    print("\nThis script will:")
    print("1. Open Chrome browser")
    print("2. Log in to LinkedIn (use existing session or manual)")
    print("3. Post the AI Finance article as Sam Desigan")
    print("4. Keep browser open for verification")
    
    print("\n⚠️  IMPORTANT:")
    print("• Make sure Chrome is not already running")
    print("• If not logged in, you'll need to log in manually")
    print("• The script will wait for you to complete login")
    
    response = input("\nContinue? (y/n): ").strip().lower()
    
    if response == 'y':
        poster = LinkedInAutoPoster(headless=False)
        poster.run()
    else:
        print("\nManual posting instructions:")
        print(f"1. View content: cat {os.path.join('/Users/cubiczan/.openclaw/workspace', 'social_media/sam_post_1_ai_finance.json')} | jq '.content'")
        print("2. Go to: https://www.linkedin.com/in/sam-desigan-198a742a7/")
        print("3. Click 'Start a post'")
        print("4. Copy/paste content")
        print("5. Post at 5:30 PM EST (optimal time)")

if __name__ == "__main__":
    main()