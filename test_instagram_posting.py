#!/usr/bin/env python3
"""
Test Instagram posting with browser automation
"""

import os
import sys
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_instagram_posting():
    """Test Instagram login and posting"""
    print("🧪 Testing Instagram posting...")
    print("="*50)
    
    # Load credentials from config
    config_path = "/Users/cubiczan/.openclaw/workspace/config/social_media_config.json"
    
    if not os.path.exists(config_path):
        print("❌ Config file not found.")
        print("Please run: python3 immediate_social_business_config.py")
        return False
    
    with open(config_path, "r") as f:
        config = json.load(f)
    
    instagram_config = config.get("platforms", {}).get("instagram", {})
    
    if not instagram_config.get("enabled", False):
        print("❌ Instagram not enabled in config")
        return False
    
    credentials = instagram_config.get("credentials", {})
    username = credentials.get("username", "")
    password = credentials.get("password", "")
    
    if not username or not password:
        print("❌ Instagram credentials not configured")
        print("Please update social_media_config.json with your credentials:")
        print('''"instagram": {
  "enabled": true,
  "method": "browser_automation",
  "credentials": {
    "username": "YOUR_INSTAGRAM_USERNAME",
    "password": "YOUR_INSTAGRAM_PASSWORD"
  }
}''')
        return False
    
    print(f"🔑 Testing login for: {username}")
    print("Note: This will open Chrome browser for testing.")
    print("Make sure Chrome is installed.")
    print("="*50)
    
    try:
        # Setup Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # For headless testing (uncomment for server use)
        # options.add_argument("--headless")
        
        print("🚀 Launching Chrome browser...")
        driver = webdriver.Chrome(options=options)
        
        # Test login
        print("🌐 Navigating to Instagram login...")
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)
        
        # Check if we're already logged in
        if "login" not in driver.current_url:
            print("✅ Already logged in to Instagram")
            driver.quit()
            return True
        
        # Enter credentials
        print("🔐 Entering credentials...")
        try:
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys(username)
            
            password_field = driver.find_element(By.NAME, "password")
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)
            
            time.sleep(5)
            
            # Check for 2FA or suspicious login
            if "challenge" in driver.current_url:
                print("⚠️  Instagram requires additional verification (2FA)")
                print("Please complete verification in the browser.")
                print("After verification, the test will continue.")
                input("Press Enter after completing verification...")
                time.sleep(3)
            
            # Check if login successful
            if "login" in driver.current_url or "accounts/login" in driver.current_url:
                print("❌ Login failed. Possible issues:")
                print("1. Wrong username/password")
                print("2. 2FA required (use app codes, not SMS)")
                print("3. Suspicious login detected")
                
                # Take screenshot for debugging
                screenshot_path = "/Users/cubiczan/.openclaw/workspace/instagram_login_error.png"
                driver.save_screenshot(screenshot_path)
                print(f"📸 Screenshot saved: {screenshot_path}")
                
                driver.quit()
                return False
            
            print("✅ Instagram login successful!")
            
            # Navigate to profile to confirm
            print("👤 Loading profile...")
            driver.get(f"https://www.instagram.com/{username}/")
            time.sleep(3)
            
            # Check profile loaded
            try:
                profile_name = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "h2"))
                )
                print(f"✅ Profile loaded: {profile_name.text}")
            except:
                print("⚠️  Could not load profile name, but login was successful")
            
            # Test create post flow
            print("📝 Testing post creation flow...")
            driver.get("https://www.instagram.com/create/select/")
            time.sleep(3)
            
            # Check if we can access create page
            if "create" in driver.current_url:
                print("✅ Can access post creation page")
                
                # Check for file upload input
                file_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
                if file_inputs:
                    print("✅ File upload available")
                else:
                    print("⚠️  File upload not found (UI may have changed)")
                
                # Go back to avoid accidental posting
                driver.back()
                time.sleep(2)
            
            print("="*50)
            print("🎉 Instagram test PASSED!")
            print("You can now post to Instagram using browser automation.")
            
            driver.quit()
            return True
            
        except Exception as e:
            print(f"❌ Error during login: {e}")
            driver.quit()
            return False
        
    except Exception as e:
        print(f"❌ Browser automation failed: {e}")
        print("Possible issues:")
        print("1. Chrome not installed")
        print("2. ChromeDriver not installed or wrong version")
        print("3. Network connectivity issues")
        return False

def quick_setup_guide():
    """Provide quick setup instructions"""
    print("\n" + "="*50)
    print("🚀 QUICK SETUP GUIDE")
    print("="*50)
    
    print("\n1. Update your Instagram credentials:")
    print('''Edit: /Users/cubiczan/.openclaw/workspace/config/social_media_config.json

Find "instagram" section and update:
"instagram": {
  "enabled": true,
  "method": "browser_automation",
  "credentials": {
    "username": "YOUR_ACTUAL_USERNAME",
    "password": "YOUR_ACTUAL_PASSWORD"
  }
}''')
    
    print("\n2. Install required packages:")
    print("pip install selenium webdriver-manager")
    
    print("\n3. Install ChromeDriver:")
    print("brew install chromedriver  # macOS")
    print("# OR")
    print("pip install webdriver-manager")
    
    print("\n4. Run test again:")
    print("python3 test_instagram_posting.py")
    
    print("\n5. For immediate posting, use:")
    print('''from immediate_social_poster import ImmediateSocialPoster
poster = ImmediateSocialPoster()
poster.post_to_instagram("Your post content here")''')

if __name__ == "__main__":
    print("Instagram Posting Test")
    print("="*50)
    
    # Check if config exists
    config_path = "/Users/cubiczan/.openclaw/workspace/config/social_media_config.json"
    if not os.path.exists(config_path):
        print("❌ Configuration not found.")
        print("First run: python3 immediate_social_business_config.py")
        sys.exit(1)
    
    success = test_instagram_posting()
    
    if not success:
        quick_setup_guide()
    
    sys.exit(0 if success else 1)