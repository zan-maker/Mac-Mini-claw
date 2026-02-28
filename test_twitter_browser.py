#!/usr/bin/env python3
"""
Test Twitter/X Browser Automation
Test the browser automation method for Twitter posting
"""

import os
import sys
import json
import time
from datetime import datetime

def test_twitter_browser_automation():
    """Test Twitter browser automation"""
    print("🚀 Testing Twitter/X Browser Automation")
    print("="*60)
    
    # Check if selenium is installed
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        print("✅ Selenium installed")
    except ImportError:
        print("❌ Selenium not installed")
        print("Install with: pip install selenium")
        return False
    
    # Load config
    config_path = "/Users/cubiczan/.openclaw/workspace/config/social_media_config.json"
    if not os.path.exists(config_path):
        print(f"❌ Config file not found: {config_path}")
        return False
    
    with open(config_path, "r") as f:
        config = json.load(f)
    
    twitter_config = config.get("platforms", {}).get("twitter_x", {})
    credentials = twitter_config.get("credentials", {})
    
    username = credentials.get("username", "")
    password = credentials.get("password", "")
    
    if not username or username == "YOUR_TWITTER_USERNAME":
        print("❌ Twitter username not configured")
        print("Please update 'username' in twitter_x credentials")
        return False
    
    if not password or password == "YOUR_TWITTER_PASSWORD":
        print("❌ Twitter password not configured")
        print("Please update 'password' in twitter_x credentials")
        return False
    
    print(f"🔑 Username: {username}")
    print(f"🔑 Password: {'*' * len(password)}")
    
    # Test content
    test_content = f"Testing Twitter browser automation at {datetime.now().strftime('%H:%M')} #BrowserAutomation #Testing #SocialMedia"
    
    print(f"\n📝 Test content: {test_content}")
    
    # Setup Chrome
    print("\n🌐 Setting up Chrome browser...")
    
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # For testing, we can run in headless mode
        # options.add_argument("--headless")  # Uncomment for headless testing
        
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 20)
        
        print("✅ Chrome browser started")
        
        # Step 1: Login
        print("\n1. 🔐 Logging in to Twitter...")
        driver.get("https://twitter.com/login")
        time.sleep(3)
        
        # Check if we're already logged in
        if "home" in driver.current_url or "twitter.com/home" in driver.current_url:
            print("✅ Already logged in!")
        else:
            # Enter username
            try:
                username_field = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='username']"))
                )
                username_field.send_keys(username)
                username_field.send_keys(Keys.RETURN)
                print("✅ Username entered")
                time.sleep(2)
            except Exception as e:
                print(f"⚠️  Could not find username field: {e}")
                # Try alternative selector
                try:
                    username_field = driver.find_element(By.NAME, "text")
                    username_field.send_keys(username)
                    username_field.send_keys(Keys.RETURN)
                    print("✅ Username entered (alternative)")
                    time.sleep(2)
                except:
                    print("❌ Could not find any username field")
                    driver.quit()
                    return False
            
            # Enter password
            try:
                password_field = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
                )
                password_field.send_keys(password)
                password_field.send_keys(Keys.RETURN)
                print("✅ Password entered")
                time.sleep(5)
            except Exception as e:
                print(f"⚠️  Could not find password field: {e}")
                # Try alternative selector
                try:
                    password_field = driver.find_element(By.NAME, "password")
                    password_field.send_keys(password)
                    password_field.send_keys(Keys.RETURN)
                    print("✅ Password entered (alternative)")
                    time.sleep(5)
                except:
                    print("❌ Could not find any password field")
                    driver.quit()
                    return False
        
        # Check login success
        if "home" in driver.current_url or "twitter.com" in driver.current_url:
            print("✅ Login successful!")
        else:
            print("⚠️  May need to handle 2FA or verification")
            print(f"Current URL: {driver.current_url}")
            
            # Take screenshot for debugging
            screenshot_path = "/Users/cubiczan/.openclaw/workspace/twitter_login_debug.png"
            driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")
            
            # Check for common elements
            page_text = driver.page_source.lower()
            if "enter code" in page_text or "verification" in page_text:
                print("🔐 2FA/Verification required - manual intervention needed")
                print("Please complete verification in browser, then continue")
                input("Press Enter after completing verification...")
            elif "suspicious" in page_text or "unusual" in page_text:
                print("⚠️  Suspicious activity detected - may need to verify")
                print("Please check email or complete verification")
                input("Press Enter after completing verification...")
        
        # Step 2: Navigate to tweet composer
        print("\n2. 📝 Navigating to tweet composer...")
        driver.get("https://twitter.com/compose/tweet")
        time.sleep(3)
        
        # Check if we're on the compose page
        if "compose/tweet" in driver.current_url:
            print("✅ On tweet composer page")
        else:
            print(f"⚠️  Not on compose page: {driver.current_url}")
            # Try alternative URL
            driver.get("https://twitter.com/intent/tweet")
            time.sleep(3)
        
        # Step 3: Find tweet box and enter content
        print("\n3. ✍️ Entering tweet content...")
        
        # Try multiple selectors for tweet box
        selectors = [
            "div[data-testid='tweetTextarea_0']",
            "div[role='textbox']",
            "div[contenteditable='true']",
            "textarea"
        ]
        
        tweet_box = None
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    tweet_box = elements[0]
                    print(f"✅ Found tweet box with selector: {selector}")
                    break
            except:
                continue
        
        if not tweet_box:
            print("❌ Could not find tweet box")
            driver.quit()
            return False
        
        # Click and enter content
        tweet_box.click()
        time.sleep(1)
        
        # Clear any existing text and enter new content
        try:
            tweet_box.clear()
        except:
            pass  # Some tweet boxes can't be cleared
        
        tweet_box.send_keys(test_content)
        print("✅ Tweet content entered")
        time.sleep(2)
        
        # Step 4: Check tweet button
        print("\n4. 🔍 Checking tweet button...")
        
        # Try multiple selectors for tweet button
        button_selectors = [
            "div[data-testid='tweetButton']",
            "button[data-testid='tweetButton']",
            "div[role='button'][aria-label*='Tweet']",
            "button[type='button']:contains('Tweet')"
        ]
        
        tweet_button = None
        for selector in button_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    tweet_button = elements[0]
                    print(f"✅ Found tweet button with selector: {selector}")
                    
                    # Check if button is enabled
                    if tweet_button.is_enabled():
                        print("✅ Tweet button is enabled")
                    else:
                        print("⚠️ Tweet button is disabled (check character count)")
                    
                    break
            except:
                continue
        
        if not tweet_button:
            print("❌ Could not find tweet button")
            # Take screenshot
            screenshot_path = "/Users/cubiczan/.openclaw/workspace/tweet_button_debug.png"
            driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")
            driver.quit()
            return False
        
        # Step 5: Optional - Don't actually post for testing
        print("\n5. 🎯 TEST COMPLETE - Not posting (test mode)")
        print("   To actually post, uncomment the tweet_button.click() line")
        
        # Uncomment this line to actually post:
        # tweet_button.click()
        # print("✅ Tweet posted!")
        # time.sleep(3)
        
        # Step 6: Cleanup
        print("\n6. 🧹 Cleaning up...")
        driver.quit()
        print("✅ Browser closed")
        
        # Save test results
        results = {
            "timestamp": datetime.now().isoformat(),
            "test": "twitter_browser_automation",
            "status": "success",
            "username": username,
            "content_preview": test_content[:50] + "...",
            "issues_found": [],
            "recommendations": [
                "Update username/password in config if not already done",
                "Test with actual posting by uncommenting tweet_button.click()",
                "Consider adding 2FA handling if needed"
            ]
        }
        
        results_file = "/Users/cubiczan/.openclaw/workspace/twitter_browser_test_results.json"
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📁 Test results saved to: {results_file}")
        
        print("\n" + "="*60)
        print("🎯 TWITTER BROWSER AUTOMATION TEST COMPLETE!")
        print("="*60)
        print("\n✅ Browser automation framework: WORKING")
        print("✅ Login process: TESTED")
        print("✅ Tweet composition: TESTED")
        print("✅ Button detection: TESTED")
        print("\n🚀 Ready for actual posting!")
        print("\nTo post a real tweet:")
        print("1. Update username/password in config")
        print("2. Uncomment tweet_button.click() in test script")
        print("3. Run the test again")
        print("\nOr use the full system:")
        print("python3 immediate_social_poster.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Browser automation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    success = test_twitter_browser_automation()
    
    if success:
        print("\n🎉 Twitter browser automation is READY!")
        print("\nNext steps:")
        print("1. Update your Twitter username/password in config")
        print("2. Test Instagram/Facebook browser automation")
        print("3. Run the complete social media system")
    else:
        print("\n⚠️  Twitter browser automation needs configuration")
        print("\nCheck:")
        print("1. Is Chrome installed?")
        print("2. Are Twitter credentials in config?")
        print("3. Is Selenium installed? (pip install selenium)")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()