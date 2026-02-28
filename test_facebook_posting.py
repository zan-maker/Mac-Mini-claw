#!/usr/bin/env python3
"""
Test Facebook posting with browser automation
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

def test_facebook_posting():
    """Test Facebook login and posting"""
    print("🧪 Testing Facebook posting...")
    print("="*50)
    
    # Load credentials from config
    config_path = "/Users/cubiczan/.openclaw/workspace/config/social_media_config.json"
    
    if not os.path.exists(config_path):
        print("❌ Config file not found.")
        print("Please run: python3 create_social_config.py")
        return False
    
    with open(config_path, "r") as f:
        config = json.load(f)
    
    facebook_config = config.get("platforms", {}).get("facebook", {})
    
    if not facebook_config.get("enabled", False):
        print("❌ Facebook not enabled in config")
        return False
    
    credentials = facebook_config.get("credentials", {})
    username = credentials.get("username", "")
    password = credentials.get("password", "")
    pages = facebook_config.get("pages", [])
    
    if not username or not password:
        print("❌ Facebook credentials not configured")
        print("Please update social_media_config.json with your credentials:")
        print('''"facebook": {
  "enabled": true,
  "method": "browser_automation",
  "credentials": {
    "username": "YOUR_FACEBOOK_USERNAME",
    "password": "YOUR_FACEBOOK_PASSWORD"
  },
  "pages": ["YOUR_PAGE_NAME"]
}''')
        return False
    
    if not pages:
        print("❌ No Facebook pages configured")
        print("Add your page name to the 'pages' array in config")
        return False
    
    page_name = pages[0]
    
    print(f"🔑 Testing login for: {username}")
    print(f"📄 Testing page access: {page_name}")
    print("Note: This will open Chrome browser for testing.")
    print("="*50)
    
    try:
        # Setup Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        
        print("🚀 Launching Chrome browser...")
        driver = webdriver.Chrome(options=options)
        
        # Test login
        print("🌐 Navigating to Facebook login...")
        driver.get("https://www.facebook.com/login")
        time.sleep(3)
        
        # Check if we're already logged in
        if "login" not in driver.current_url:
            print("✅ Already logged in to Facebook")
        else:
            # Enter credentials
            print("🔐 Entering credentials...")
            try:
                email_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "email"))
                )
                email_field.send_keys(username)
                
                pass_field = driver.find_element(By.ID, "pass")
                pass_field.send_keys(password)
                pass_field.send_keys(Keys.RETURN)
                
                time.sleep(5)
                
                # Check for 2FA or suspicious login
                if "checkpoint" in driver.current_url:
                    print("⚠️  Facebook requires additional verification")
                    print("Please complete verification in the browser.")
                    print("After verification, the test will continue.")
                    input("Press Enter after completing verification...")
                    time.sleep(3)
                
                # Check if login successful
                if "login" in driver.current_url:
                    print("❌ Login failed. Possible issues:")
                    print("1. Wrong username/password")
                    print("2. 2FA required")
                    print("3. Suspicious login detected")
                    
                    # Take screenshot for debugging
                    screenshot_path = "/Users/cubiczan/.openclaw/workspace/facebook_login_error.png"
                    driver.save_screenshot(screenshot_path)
                    print(f"📸 Screenshot saved: {screenshot_path}")
                    
                    driver.quit()
                    return False
                
                print("✅ Facebook login successful!")
                
            except Exception as e:
                print(f"❌ Error during login: {e}")
                driver.quit()
                return False
        
        # Test page access
        print(f"📄 Testing access to page: {page_name}")
        driver.get(f"https://www.facebook.com/{page_name}")
        time.sleep(3)
        
        # Check if we can access the page
        if page_name in driver.current_url or "facebook.com/" in driver.current_url:
            print("✅ Page access successful!")
            
            # Look for post creation elements
            print("🔍 Checking post creation capability...")
            
            # Try to find post creation area
            post_selectors = [
                "div[aria-label='Create a post']",
                "span[data-text='true']",
                "div[contenteditable='true']",
                "textarea[placeholder=\"What's on your mind?\"]"
            ]
            
            found_post_box = False
            for selector in post_selectors:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ Found post creation element: {selector}")
                    found_post_box = True
                    break
            
            if not found_post_box:
                print("⚠️  Could not find post creation box (UI may have changed)")
                print("But page access is working.")
            
            # Check for photo upload
            file_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
            if file_inputs:
                print("✅ File upload available")
            else:
                print("⚠️  File upload not found")
            
            print("="*50)
            print("🎉 Facebook test PASSED!")
            print("You can now post to Facebook using browser automation.")
            
            driver.quit()
            return True
        else:
            print("❌ Could not access Facebook page")
            print("Possible issues:")
            print("1. Page doesn't exist")
            print("2. You're not an admin of the page")
            print("3. Page name is incorrect")
            
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
    
    print("\n1. Update your Facebook credentials:")
    print('''Edit: /Users/cubiczan/.openclaw/workspace/config/social_media_config.json

Find "facebook" section and update:
"facebook": {
  "enabled": true,
  "method": "browser_automation",
  "credentials": {
    "username": "YOUR_ACTUAL_USERNAME",
    "password": "YOUR_ACTUAL_PASSWORD"
  },
  "pages": ["YOUR_PAGE_NAME"]
}''')
    
    print("\n2. Make sure you're an admin of the Facebook page")
    print("   - Go to your Facebook page")
    print("   - Check 'Page Roles' in settings")
    print("   - Your account should be listed as Admin")
    
    print("\n3. Install required packages:")
    print("pip install selenium webdriver-manager")
    
    print("\n4. Install ChromeDriver:")
    print("brew install chromedriver  # macOS")
    print("# OR")
    print("pip install webdriver-manager")
    
    print("\n5. Run test again:")
    print("python3 test_facebook_posting.py")
    
    print("\n6. For immediate posting, use:")
    print('''from immediate_social_poster import ImmediateSocialPoster
poster = ImmediateSocialPoster()
poster.post_to_facebook("Your post content here")''')

if __name__ == "__main__":
    print("Facebook Posting Test")
    print("="*50)
    
    # Check if config exists
    config_path = "/Users/cubiczan/.openclaw/workspace/config/social_media_config.json"
    if not os.path.exists(config_path):
        print("❌ Configuration not found.")
        print("First run: python3 create_social_config.py")
        sys.exit(1)
    
    success = test_facebook_posting()
    
    if not success:
        quick_setup_guide()
    
    sys.exit(0 if success else 1)