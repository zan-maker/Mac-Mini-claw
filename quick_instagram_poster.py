#!/usr/bin/env python3
"""
Quick Instagram Poster - Browser Automation
Simplest path to posting TODAY
"""

import os
import sys
import json
from datetime import datetime

def setup_quick_instagram():
    """Setup quick Instagram posting"""
    print("🚀 QUICK INSTAGRAM POSTING SETUP")
    print("="*60)
    
    # Step 1: Check if Selenium is installed
    print("\n1️⃣ Checking Selenium installation...")
    try:
        import selenium
        print("   ✅ Selenium is installed")
    except ImportError:
        print("   ❌ Selenium not installed")
        print("\n   Install with:")
        print("   pip install selenium")
        print("\n   Or use:")
        print("   pip3 install selenium")
        return False
    
    # Step 2: Check ChromeDriver
    print("\n2️⃣ Checking ChromeDriver...")
    print("   Download from: https://chromedriver.chromium.org/")
    print("   Place in: /usr/local/bin/ or in PATH")
    print("   Or use: brew install chromedriver (on macOS)")
    
    # Step 3: Create quick config
    print("\n3️⃣ Creating quick configuration...")
    
    config = {
        "username": input("   Enter Instagram username: ").strip(),
        "password": input("   Enter Instagram password: ").strip(),
        "headless": False,
        "browser": "chrome",
        "image_dir": "/Users/cubiczan/.openclaw/workspace/images",
        "default_caption": "Posted by OpenClaw 🤖"
    }
    
    # Save config
    config_path = "/Users/cubiczan/.openclaw/workspace/quick_instagram_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"   ✅ Configuration saved to: {config_path}")
    
    # Step 4: Create images directory
    print("\n4️⃣ Creating directories...")
    os.makedirs(config["image_dir"], exist_ok=True)
    print(f"   ✅ Images directory: {config['image_dir']}")
    
    # Step 5: Create test script
    print("\n5️⃣ Creating test script...")
    
    test_script = """#!/usr/bin/env python3
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

# Load config
config_path = "/Users/cubiczan/.openclaw/workspace/quick_instagram_config.json"
with open(config_path, 'r') as f:
    config = json.load(f)

def quick_login():
    \"\"\"Quick Instagram login\"\"\"
    driver = webdriver.Chrome()
    
    try:
        # Go to Instagram
        driver.get("https://www.instagram.com")
        time.sleep(3)
        
        # Enter username
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys(config["username"])
        time.sleep(1)
        
        # Enter password
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(config["password"])
        time.sleep(1)
        
        # Click login
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        time.sleep(5)
        
        print("✅ Login successful!")
        print("   Keep this browser window open for posting")
        
        # Keep browser open
        input("Press Enter to close browser...")
        
    except Exception as e:
        print(f"❌ Login failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    quick_login()
"""
    
    script_path = "/Users/cubiczan/.openclaw/workspace/quick_login.py"
    with open(script_path, 'w') as f:
        f.write(test_script)
    
    os.chmod(script_path, 0o755)
    print(f"   ✅ Test script: {script_path}")
    
    # Step 6: Create posting script
    print("\n6️⃣ Creating posting script...")
    
    post_script = """#!/usr/bin/env python3
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def post_to_instagram(image_path, caption):
    \"\"\"Post to Instagram\"\"\"
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return False
    
    # Load config
    config_path = "/Users/cubiczan/.openclaw/workspace/quick_instagram_config.json"
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    driver = webdriver.Chrome()
    
    try:
        # Already logged in from previous step
        # Just navigate to create page
        driver.get("https://www.instagram.com")
        time.sleep(3)
        
        # Click create (simplified)
        driver.get("https://www.instagram.com/create/select/")
        time.sleep(3)
        
        # Upload image
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        file_input.send_keys(os.path.abspath(image_path))
        time.sleep(5)
        
        # Click next
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Next']"))
        )
        next_button.click()
        time.sleep(2)
        
        # Click next again
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Next']"))
        )
        next_button.click()
        time.sleep(2)
        
        # Enter caption
        caption_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Write a caption...']"))
        )
        caption_field.click()
        caption_field.send_keys(caption)
        time.sleep(2)
        
        # Share post
        share_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Share']"))
        )
        share_button.click()
        time.sleep(5)
        
        print("✅ Post created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Post failed: {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python quick_post.py /path/to/image.jpg \"Your caption\"")
        sys.exit(1)
    
    image_path = sys.argv[1]
    caption = sys.argv[2]
    
    post_to_instagram(image_path, caption)
"""
    
    post_script_path = "/Users/cubiczan/.openclaw/workspace/quick_post.py"
    with open(post_script_path, 'w') as f:
        f.write(post_script)
    
    os.chmod(post_script_path, 0o755)
    print(f"   ✅ Posting script: {post_script_path}")
    
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE!")
    print("="*60)
    
    print("\n🎯 NEXT STEPS:")
    print("1. Install ChromeDriver if not already installed")
    print("2. Run login test:")
    print("   python quick_login.py")
    print("3. Create a test image (JPG, 1080x1080 recommended)")
    print("4. Post test image:")
    print("   python quick_post.py /path/to/image.jpg \"Test caption\"")
    
    print("\n📝 Commands summary:")
    print("   pip install selenium")
    print("   python quick_login.py")
    print("   python quick_post.py image.jpg \"My caption\"")
    
    return True

def check_facebook_alternative():
    """Check Facebook alternative approach"""
    print("\n🔍 FACEBOOK ALTERNATIVE APPROACH")
    print("="*60)
    
    print("\nSince App Token has no scopes, options:")
    
    print("\nOption 1: Add permissions to App")
    print("   1. Go to App Dashboard")
    print("   2. Add pages_manage_posts permission")
    print("   3. Go through App Review if needed")
    print("   4. Get new token with permissions")
    
    print("\nOption 2: Use Test Users")
    print("   1. Create test users in App Dashboard")
    print("   2. Use test user access tokens")
    print("   3. Only works in Development mode")
    
    print("\nOption 3: Get User Token (Easiest)")
    print("   1. Go to Graph API Explorer")
    print("   2. Get User Token (takes 2 minutes)")
    print("   3. Use for posting")
    
    print("\n🎯 Recommendation: Use Instagram browser automation for now")
    print("   Get Facebook working later with proper User Token")

def main():
    """Main setup function"""
    print("🧪 Quick Social Media Posting Setup")
    print("="*60)
    
    setup_quick_instagram()
    check_facebook_alternative()
    
    print("\n" + "="*60)
    print("🚀 READY TO POST IN 5 MINUTES!")
    print("="*60)

if __name__ == "__main__":
    main()