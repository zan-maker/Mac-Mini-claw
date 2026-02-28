# Facebook & Instagram Posting Implementation Guide

## 🎯 Overview
This guide provides step-by-step instructions to implement Facebook and Instagram posting capabilities in OpenClaw using three different methods.

## 📋 Prerequisites

### 1. Facebook Developer Account
- **Go to:** https://developers.facebook.com
- **Create App:** Business type
- **Get Credentials:**
  - **APP ID**
  - **APP SECRET**
  - **ACCESS TOKEN** (with required permissions)

### 2. Instagram Business Account
- **Convert** personal account to Business account
- **Connect** to Facebook Page
- **Enable** Instagram Graph API access

### 3. Required Permissions
```
pages_manage_posts
pages_read_engagement
instagram_basic
instagram_content_publish
```

---

## 🚀 METHOD 1: Using `upload-post` Skill (API-Based)

### Step 1: Install the Skill
```bash
# Check if skill exists
npx clawdhub@latest search upload-post

# Install if available
npx clawdhub@latest install upload-post
```

### Step 2: Configure Environment Variables
Create `/Users/cubiczan/.openclaw/workspace/.env`:
```env
# Facebook/Instagram API Credentials
FACEBOOK_APP_ID=your_app_id_here
FACEBOOK_APP_SECRET=your_app_secret_here
FACEBOOK_ACCESS_TOKEN=your_access_token_here
FACEBOOK_PAGE_ID=your_page_id_here
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_instagram_account_id

# Optional: Scheduling
TIMEZONE=America/New_York
POST_SCHEDULE_CRON=0 9 * * *  # Daily at 9 AM
```

### Step 3: Create Posting Script
Create `/Users/cubiczan/.openclaw/workspace/scripts/social_poster.py`:
```python
#!/usr/bin/env python3
"""
Facebook & Instagram Posting Script
Uses Facebook Graph API for automated posting
"""

import os
import requests
import json
from datetime import datetime
from pathlib import Path

class SocialMediaPoster:
    def __init__(self):
        self.app_id = os.getenv('FACEBOOK_APP_ID')
        self.app_secret = os.getenv('FACEBOOK_APP_SECRET')
        self.access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.page_id = os.getenv('FACEBOOK_PAGE_ID')
        self.instagram_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        
        self.graph_url = "https://graph.facebook.com/v18.0"
        
    def post_to_facebook(self, message: str, image_path: str = None):
        """Post to Facebook Page"""
        url = f"{self.graph_url}/{self.page_id}/feed"
        
        params = {
            "access_token": self.access_token,
            "message": message
        }
        
        if image_path and os.path.exists(image_path):
            # Upload image first
            media_url = f"{self.graph_url}/{self.page_id}/photos"
            files = {'source': open(image_path, 'rb')}
            media_params = {
                "access_token": self.access_token,
                "published": "false"
            }
            
            media_response = requests.post(media_url, params=media_params, files=files)
            if media_response.status_code == 200:
                media_id = media_response.json().get('id')
                params['attached_media'] = json.dumps([{"media_fbid": media_id}])
        
        response = requests.post(url, params=params)
        
        if response.status_code == 200:
            print(f"✅ Facebook post successful: {response.json().get('id')}")
            return True
        else:
            print(f"❌ Facebook post failed: {response.text}")
            return False
    
    def post_to_instagram(self, caption: str, image_path: str):
        """Post to Instagram Business Account"""
        if not image_path or not os.path.exists(image_path):
            print("❌ Image file required for Instagram")
            return False
        
        # Step 1: Create media container
        create_url = f"{self.graph_url}/{self.instagram_id}/media"
        
        params = {
            "access_token": self.access_token,
            "caption": caption,
            "image_url": f"file://{os.path.abspath(image_path)}"
        }
        
        create_response = requests.post(create_url, params=params)
        
        if create_response.status_code != 200:
            print(f"❌ Instagram media creation failed: {create_response.text}")
            return False
        
        creation_id = create_response.json().get('id')
        
        # Step 2: Publish media
        publish_url = f"{self.graph_url}/{self.instagram_id}/media_publish"
        publish_params = {
            "access_token": self.access_token,
            "creation_id": creation_id
        }
        
        publish_response = requests.post(publish_url, params=publish_params)
        
        if publish_response.status_code == 200:
            print(f"✅ Instagram post successful: {publish_response.json().get('id')}")
            return True
        else:
            print(f"❌ Instagram publish failed: {publish_response.text}")
            return False
    
    def schedule_post(self, platform: str, message: str, image_path: str = None, schedule_time: str = None):
        """Schedule a post for later"""
        # Implementation depends on API capabilities
        pass

# Example usage
if __name__ == "__main__":
    poster = SocialMediaPoster()
    
    # Test post
    test_message = "Hello from OpenClaw! 🤖 Automated social media posting test."
    test_image = "/path/to/image.jpg"  # Replace with actual image path
    
    # Post to Facebook
    # poster.post_to_facebook(test_message, test_image)
    
    # Post to Instagram
    # poster.post_to_instagram(test_message, test_image)
    
    print("✅ Social Media Poster ready!")
```

### Step 4: Create Skill Definition
Create `/Users/cubiczan/.openclaw/workspace/skills/social-poster/SKILL.md`:
```markdown
# Social Poster Skill

Post to Facebook and Instagram using Graph API.

## Commands
- `/facebook-post "message" [image_path]` - Post to Facebook
- `/instagram-post "caption" image_path` - Post to Instagram
- `/schedule-post platform "message" image_path "YYYY-MM-DD HH:MM"` - Schedule post

## Configuration
Set environment variables in `.env`:
- FACEBOOK_APP_ID
- FACEBOOK_APP_SECRET  
- FACEBOOK_ACCESS_TOKEN
- FACEBOOK_PAGE_ID
- INSTAGRAM_BUSINESS_ACCOUNT_ID

## Image Requirements
- **Facebook:** JPG, PNG, GIF (max 4MB)
- **Instagram:** JPG, 1080x1080 recommended
```

---

## 🚀 METHOD 2: Using `insta-post` Skill (Browser Automation)

### Step 1: Set Up Browser Automation
```bash
# Install required packages
pip install selenium playwright
playwright install chromium

# Or use existing agent-browser
npm install -g agent-browser@latest
```

### Step 2: Create Browser Automation Script
Create `/Users/cubiczan/.openclaw/workspace/scripts/instagram_browser_poster.py`:
```python
#!/usr/bin/env python3
"""
Instagram Browser Automation Poster
Uses browser automation to post to Instagram
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InstagramBrowserPoster:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.driver = None
        
    def login(self):
        """Login to Instagram"""
        self.driver = webdriver.Chrome()  # Or Firefox/Safari
        
        # Go to Instagram
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)
        
        # Enter username
        username_field = self.driver.find_element(By.NAME, "username")
        username_field.send_keys(self.username)
        
        # Enter password
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys(self.password)
        
        # Click login
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        time.sleep(5)
        
        # Handle "Save Login Info" prompt
        try:
            not_now_button = self.driver.find_element(By.XPATH, "//button[text()='Not Now']")
            not_now_button.click()
            time.sleep(2)
        except:
            pass
        
        print("✅ Logged in to Instagram")
    
    def create_post(self, image_path: str, caption: str):
        """Create a new post"""
        if not self.driver:
            print("❌ Not logged in")
            return False
        
        # Click create button
        try:
            create_button = self.driver.find_element(By.XPATH, "//div[text()='Create']")
            create_button.click()
            time.sleep(2)
        except:
            # Alternative: Click plus icon
            try:
                plus_icon = self.driver.find_element(By.XPATH, "//svg[@aria-label='New post']")
                plus_icon.click()
                time.sleep(2)
            except Exception as e:
                print(f"❌ Could not find create button: {e}")
                return False
        
        # Upload image
        try:
            file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(os.path.abspath(image_path))
            time.sleep(3)
        except Exception as e:
            print(f"❌ Could not upload image: {e}")
            return False
        
        # Click next
        try:
            next_button = self.driver.find_element(By.XPATH, "//div[text()='Next']")
            next_button.click()
            time.sleep(2)
            
            next_button_2 = self.driver.find_element(By.XPATH, "//div[text()='Next']")
            next_button_2.click()
            time.sleep(2)
        except Exception as e:
            print(f"❌ Could not navigate: {e}")
            return False
        
        # Enter caption
        try:
            caption_field = self.driver.find_element(By.XPATH, "//div[@aria-label='Write a caption...']")
            caption_field.send_keys(caption)
            time.sleep(2)
        except Exception as e:
            print(f"❌ Could not enter caption: {e}")
            return False
        
        # Share post
        try:
            share_button = self.driver.find_element(By.XPATH, "//div[text()='Share']")
            share_button.click()
            time.sleep(5)
        except Exception as e:
            print(f"❌ Could not share post: {e}")
            return False
        
        print("✅ Instagram post created via browser")
        return True
    
    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()

# Example usage
if __name__ == "__main__":
    # Set credentials in environment or config file
    username = os.getenv('INSTAGRAM_USERNAME', 'your_username')
    password = os.getenv('INSTAGRAM_PASSWORD', 'your_password')
    
    poster = InstagramBrowserPoster(username, password)
    
    try:
        poster.login()
        # poster.create_post("/path/to/image.jpg", "Test caption from OpenClaw! 🤖")
    finally:
        poster.close()
```

### Step 3: Create Skill with Browser Agent
Create `/Users/cubiczan/.openclaw/workspace/skills/insta-post/SKILL.md`:
```markdown
# Instagram Browser Poster Skill

Post to Instagram using browser automation.

## Requirements
- Chrome/Firefox browser installed
- Instagram account credentials
- Images in JPG format (1080x1080 recommended)

## Setup
1. Set environment variables:
   - INSTAGRAM_USERNAME
   - INSTAGRAM_PASSWORD
2. Install dependencies: `pip install selenium`
3. Download ChromeDriver

## Usage
- `/insta-post "caption" /path/to/image.jpg` - Post to Instagram
- `/insta-login` - Login to Instagram (first time)

## Image Requirements
- Format: JPG
- Size: 1080x1080 pixels (square)
- Max: 8MB
```

---

## 🚀 METHOD 3: Using OpenClaw Agent Browser (Port 18800)

### Step 1: Set Up Agent Browser
```bash
# Install agent-browser globally
npm install -g agent-browser@latest

# Start agent-browser on port 18800
agent-browser start --port 18800

# Or run as service
nohup agent-browser start --port 18800 > /tmp/agent-browser.log 2>&1 &
```

### Step 2: Create OpenClaw Integration
Create `/Users/cubiczan/.openclaw/workspace/scripts/agent_browser_social.py`:
```python
#!/usr/bin/env python3
"""
Social Media Posting using Agent Browser
Uses OpenClaw's browser automation capabilities
"""

import requests
import json
import time
import os

class AgentBrowserSocialPoster:
    def __init__(self, agent_browser_url="http://localhost:18800"):
        self.agent_browser_url = agent_browser_url
        
    def post_to_instagram(self, image_path: str, caption: str):
        """Post to Instagram using agent-browser"""
        
        # Step 1: Navigate to Instagram
        navigate_cmd = {
            "command": "navigate",
            "url": "https://www.instagram.com"
        }
        
        response = requests.post(f"{self.agent_browser_url}/command", json=navigate_cmd)
        
        if response.status_code != 200:
            print(f"❌ Navigation failed: {response.text}")
            return False
        
        time.sleep(3)
        
        # Step 2: Check if logged in (simplified example)
        # In reality, you'd need to handle login state
        
        # Step 3: Upload image
        upload_cmd = {
            "command": "upload",
            "selector": "input[type='file']",
            "files": [image_path]
        }
        
        response = requests.post(f"{self.agent_browser_url}/command", json=upload_cmd)
        
        if response.status_code != 200:
            print(f"❌ Upload failed: {response.text}")
            return False
        
        time.sleep(2)
        
        # Step 4: Enter caption
        caption_cmd = {
            "command": "type",
            "selector": "div[aria-label='Write a caption...']",
            "text": caption
        }
        
        response = requests.post(f"{self.agent_browser_url}/command", json=caption_cmd)
        
        if response.status_code != 200:
            print(f"❌ Caption failed: {response.text}")
            return False
        
        time.sleep(1)
        
        # Step 5: Click share
        share_cmd = {
            "command": "click",
            "selector": "div:contains('Share')"
        }
        
        response = requests.post(f"{self.agent_browser_url}/command", json=share_cmd)
        
        if response.status_code != 200:
            print(f"❌ Share failed: {response.text}")
            return False
        
        print("✅ Instagram post created via Agent Browser")
        return True

# Example usage
if __name__ == "__main__":
    poster = AgentBrowserSocialPoster()
    
    # Test with agent-browser running
    # poster.post_to_instagram("/path/to/image.jpg", "Test from Agent Browser")
    
    print("✅ Agent Browser Social Poster ready!")
```

### Step 3: Create OpenClaw Skill
Create `/Users/cubiczan/mac-bot/skills/instagram-poster/SKILL.md`:
```markdown
# Instagram Poster Skill for OpenClaw

Post to Instagram using OpenClaw's browser capabilities.

## Setup
1. Start agent-browser: `agent-browser start --port 18800`
2. Login to Instagram in the browser
3. Keep browser session active

## Usage in OpenClaw
```bash
# Post to Instagram
openclaw instagram-post --image /path/to/image.jpg --caption "Your caption"

# Or use in agent session
/instagram-post "Your caption" /path/to/image.jpg
```

## Requirements
- agent-browser running on port 18800
- Logged into Instagram in browser
- JPG images (1080x1080 recommended)
```

---

## 🎯 RECOMMENDED APPROACH

### **For Reliability: METHOD 1 (Graph API)**
- **Pros:** Most reliable, official API, scheduling support
- **Cons:** Requires Facebook Developer account, token management
- **Best for:** Production use, scheduled posts

### **For Simplicity: METHOD 2 (Browser Automation)**
- **Pros:** No API approval needed, works with personal accounts
- **Cons:** Less reliable, breaks with UI changes
- **Best for:** Personal accounts, quick setup

### **For OpenClaw Integration: METHOD 3 (Agent Browser)**
- **Pros:** Integrated with OpenClaw, uses existing infrastructure
- **Cons:** Requires browser session management
- **Best for:** Existing OpenClaw setups

---

## 🔧 Implementation Steps

### **Week 1: Setup & Testing**
1. **Day 1:** Create Facebook Developer App
2. **Day 2:** Get API credentials and permissions
3. **Day 3:** Implement Graph API posting (Method 1)
4. **Day 4:** Test with sample posts
5. **Day 5:** Set up environment variables

### **Week 2: Automation & Integration**
1. **Day 6:** Create OpenClaw skill
2. **Day 7:** Set up cron jobs for scheduling
3. **Day 8:** Implement image processing
4. **Day 9:** Add error handling and logging
5. **Day 10:** Deploy to production

---

## 📁 File Structure
```
.openclaw/workspace/
├── .env                    # API credentials
├── scripts/
│   ├── social_poster.py    # Graph API implementation
│   ├── instagram_browser_poster.py  # Browser automation
│   └── agent_browser_social.py      # Agent browser integration
├── skills/
│   ├── social-poster/      # API-based skill
│   ├── insta-post/         # Browser automation skill
│   └── instagram-poster/   # Agent browser skill
├── images/                 # Post images (JPG format)
│   ├── processed/          # Resized images
│   └── scheduled/          # Images for scheduled posts
└── logs/                   # Posting logs
```

---

## 🛠️ Quick Start Implementation

### **Option A: Fastest Path (Browser Automation)**
1. **Install Selenium:** `pip install selenium`
2. **Download ChromeDriver:** https://chromedriver.chromium.org/
3. **Create config file:** `/Users/cubiczan/.openclaw/workspace/social_config.json`
4. **Run test:** `python scripts/instagram_browser_poster.py`

### **Option B: Most Professional (Graph API)**
1. **Create Facebook App:** https://developers.facebook.com
2. **Get Page Access Token:** with `pages_manage_posts` permission
3. **Connect Instagram:** Business account to Facebook Page
4. **Test API:** Using Graph API Explorer

### **Option C: OpenClaw Native (Agent Browser)**
1. **Install agent-browser:** `npm install -g agent-browser`
2. **Start service:** `agent-browser start --port 18800`
3. **Login manually:** to Instagram in the browser
4. **Test posting:** using the agent-browser API

---

## 🚨 Troubleshooting

### **Common Issues:**
1. **API Errors:** Check token permissions and expiration
2. **Browser Issues:** Update ChromeDriver, check selectors
3. **Image Issues:** Ensure JPG format, correct dimensions
4. **Login Issues:** Handle 2FA, session cookies

### **Debugging:**
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Take screenshots on error
driver.save_screenshot('error.png')
```

---

## 📈 Monitoring & Analytics

### **Track Performance:**
1. **Post success rate**
2. **Engagement metrics** (likes, comments)
3. **Best posting times**
4. **Content performance**

### **Logging:**
```python
import logging
from datetime import datetime

logging.basicConfig(
    filename=f'/Users/cubiczan/.openclaw/workspace/logs/social_{datetime.now().strftime("%Y-%m")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

---

## 🎯 Next Steps

### **Immediate (Today):**
1. Choose implementation method (recommend: Method 1 for API)
2. Set up Facebook Developer account
3. Create test app and get credentials

### **Short-term (This Week):**
1. Implement basic posting functionality
2. Test with sample images and captions
3. Create OpenClaw skill wrapper

### **Long-term (Next Month):**
1. Add scheduling capabilities
2. Implement content calendar
3. Add analytics and reporting
4. Create multi-account support

---

## 📞 Support

### **Facebook/API Issues:**
- **Facebook Developer Docs:** https://developers.facebook.com/docs
- **Graph API Reference:** https://developers.facebook.com/docs/graph-api
- **Instagram API Docs:** https://developers.facebook.com/docs/instagram-api

### **OpenClaw Integration:**
- **OpenClaw Docs:** https://docs.openclaw.ai
- **Agent Browser Docs:** Check installed skill documentation
- **Community:** https://discord.com/invite/clawd

---

**Ready to implement? Start with Step 1: Create Facebook Developer App!** 🚀