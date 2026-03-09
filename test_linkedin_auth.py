#!/usr/bin/env python3
"""
Test LinkedIn posting with existing credentials
"""

import os
import json
import requests
from datetime import datetime

# Load configuration
config_path = "/Users/cubiczan/.openclaw/workspace/config/social_media_config.json"
with open(config_path, 'r') as f:
    config = json.load(f)

linkedin_config = config['platforms']['linkedin']
print("LinkedIn Configuration:")
print(f"Enabled: {linkedin_config['enabled']}")
print(f"Method: {linkedin_config['method']}")
print(f"Credentials keys: {list(linkedin_config['credentials'].keys())}")
print()

# Check for access token
access_token = linkedin_config['credentials'].get('access_token')
if access_token and access_token != "YOUR_ACCESS_TOKEN":
    print(f"✅ Access token found: {access_token[:20]}...")
    
    # Test API connection
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Try to get user profile
    try:
        response = requests.get(
            'https://api.linkedin.com/v2/me',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            profile = response.json()
            print(f"✅ LinkedIn API connection successful!")
            print(f"👤 User: {profile.get('localizedFirstName')} {profile.get('localizedLastName')}")
            print(f"📧 Email: {profile.get('emailAddress')}")
        else:
            print(f"⚠️ API returned status {response.status_code}")
            print(f"Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        
else:
    print("❌ No valid access token found")
    print("Note: Browser automation method is configured as backup")

print()
print("="*60)
print("POSTING OPTIONS:")
print("="*60)
print()
print("Since browser automation is configured as the primary method,")
print("we can use Selenium/Playwright to post directly to LinkedIn.")
print()
print("Alternative: Use the existing linkedin_integration.py script")
print("which already has a working access token.")
print()
print("Next steps:")
print("1. Run: python3 linkedin_integration.py")
print("2. Select option 6 (Post to personal profile)")
print("3. Use the content from linkedin_post_ai_finance.md")