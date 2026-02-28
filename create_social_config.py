#!/usr/bin/env python3
"""
Create social media configuration files
"""

import os
import json

def create_config_files():
    """Create configuration files for social media"""
    config_dir = "/Users/cubiczan/.openclaw/workspace/config"
    os.makedirs(config_dir, exist_ok=True)
    
    # 1. Social Media Configuration
    social_config = {
        "platforms": {
            "instagram": {
                "enabled": True,
                "method": "browser_automation",
                "credentials": {
                    "username": "YOUR_INSTAGRAM_USERNAME",
                    "password": "YOUR_INSTAGRAM_PASSWORD"
                },
                "business_account": True,
                "post_types": ["feed", "stories"],
                "optimal_times": ["09:00", "12:00", "15:00", "18:00"]
            },
            "facebook": {
                "enabled": True,
                "method": "browser_automation",
                "credentials": {
                    "username": "YOUR_FACEBOOK_USERNAME",
                    "password": "YOUR_FACEBOOK_PASSWORD"
                },
                "pages": ["YOUR_PAGE_NAME"],
                "post_types": ["status", "photo", "video"],
                "optimal_times": ["10:00", "13:00", "16:00", "19:00"]
            },
            "twitter_x": {
                "enabled": False,  # Set to True after getting API keys
                "method": "api",
                "credentials": {
                    "api_key": "YOUR_API_KEY",
                    "api_secret": "YOUR_API_SECRET",
                    "access_token": "YOUR_ACCESS_TOKEN",
                    "access_secret": "YOUR_ACCESS_SECRET"
                },
                "post_types": ["tweet", "thread", "poll"],
                "optimal_times": ["08:00", "11:00", "14:00", "17:00", "20:00"]
            },
            "linkedin": {
                "enabled": False,  # Set to True after getting API access
                "method": "api",
                "credentials": {
                    "access_token": "YOUR_ACCESS_TOKEN",
                    "page_id": "YOUR_PAGE_ID"
                },
                "post_types": ["article", "image", "video"],
                "optimal_times": ["08:30", "12:30", "17:30"]
            },
            "bluesky": {
                "enabled": False,  # Set to True after setup
                "method": "api",
                "credentials": {
                    "handle": "YOUR_HANDLE.bsky.social",
                    "app_password": "YOUR_APP_PASSWORD"
                },
                "post_types": ["post", "thread"],
                "optimal_times": ["09:00", "13:00", "18:00"]
            }
        },
        "content_strategy": {
            "themes": ["lead_generation", "business_automation", "ai_agents", "investment"],
            "formats": ["blog_summary", "carousel", "video_clip", "case_study"],
            "posting_frequency": {
                "instagram": 2,
                "facebook": 2,
                "twitter_x": 5,
                "linkedin": 1,
                "bluesky": 3
            }
        },
        "automation": {
            "auto_schedule": True,
            "cross_posting": True,
            "analytics_tracking": True
        }
    }
    
    social_file = os.path.join(config_dir, "social_media_config.json")
    with open(social_file, "w") as f:
        json.dump(social_config, f, indent=2)
    
    print(f"✅ Created: {social_file}")
    
    # 2. Quick Start Guide
    guide = """# 🚀 QUICK START: SOCIAL MEDIA POSTING

## IMMEDIATE STEPS (Do Now):

### 1. Update Instagram Credentials:
Edit: /Users/cubiczan/.openclaw/workspace/config/social_media_config.json

Find "instagram" section and update:
```json
"instagram": {
  "enabled": true,
  "method": "browser_automation",
  "credentials": {
    "username": "YOUR_ACTUAL_INSTAGRAM_USERNAME",
    "password": "YOUR_ACTUAL_INSTAGRAM_PASSWORD"
  }
}
```

### 2. Update Facebook Credentials:
In the same file, find "facebook" section and update:
```json
"facebook": {
  "enabled": true,
  "method": "browser_automation",
  "credentials": {
    "username": "YOUR_ACTUAL_FACEBOOK_USERNAME",
    "password": "YOUR_ACTUAL_FACEBOOK_PASSWORD"
  },
  "pages": ["YOUR_PAGE_NAME"]
}
```

### 3. Install Required Packages:
```bash
pip install selenium webdriver-manager
```

### 4. Test Instagram Posting:
```bash
cd /Users/cubiczan/.openclaw/workspace
python3 test_instagram_posting.py
```

### 5. Test Facebook Posting:
```bash
python3 test_facebook_posting.py
```

### 6. Post Your First Campaign:
```bash
python3 immediate_social_poster.py
```

## FILES CREATED:

1. **Configuration:**
   - `/Users/cubiczan/.openclaw/workspace/config/social_media_config.json`

2. **Test Scripts:**
   - `test_instagram_posting.py` - Test Instagram login/posting
   - `test_facebook_posting.py` - Test Facebook login/posting
   - `immediate_social_poster.py` - Complete posting system

3. **Sample Content:**
   - Sample posts and content calendar ready

## NEXT STEPS:

1. **Today:** Test Instagram/Facebook posting
2. **This Week:** Set up Twitter/X API, LinkedIn API
3. **Ongoing:** Daily automated posting, analytics tracking

## READY TO POST! 🚀
"""
    
    guide_file = os.path.join(config_dir, "QUICK_START_GUIDE.md")
    with open(guide_file, "w") as f:
        f.write(guide)
    
    print(f"✅ Created: {guide_file}")
    
    print("\n" + "="*50)
    print("🎯 NEXT: Update your credentials and run tests!")
    print("="*50)
    
    return True

if __name__ == "__main__":
    create_config_files()