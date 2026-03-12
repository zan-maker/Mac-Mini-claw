#!/usr/bin/env python3
"""
LinkedIn Manual Posting Workaround
Use direct Chrome profiles instead of Pinchtab API
"""

import os
import json
import time
import subprocess
from datetime import datetime

def post_to_linkedin_manual(profile_name, content, hashtags=None):
    """Post to LinkedIn using manual Chrome profile"""
    print(f"📝 POSTING TO LINKEDIN AS {profile_name.upper()}")
    print("=" * 60)
    
    # Profile directory
    profile_dir = f"/Users/cubiczan/.pinchtab/profiles/{profile_name}"
    
    if not os.path.exists(profile_dir):
        print(f"❌ Profile directory not found: {profile_dir}")
        return False
    
    # Create full content with hashtags
    full_content = content
    if hashtags:
        full_content += f"\n\n{' '.join(hashtags)}"
    
    print(f"🔧 Profile: {profile_name}")
    print(f"📁 Directory: {profile_dir}")
    print(f"📋 Content length: {len(full_content)} chars")
    print(f"🏷️  Hashtags: {hashtags}")
    
    # Save content to temporary file
    temp_file = f"/tmp/linkedin_post_{profile_name}_{int(time.time())}.txt"
    with open(temp_file, 'w') as f:
        f.write(full_content)
    
    print(f"\n📋 POST CONTENT:")
    print("-" * 40)
    print(full_content)
    print("-" * 40)
    
    print(f"\n💾 Content saved to: {temp_file}")
    
    # Instructions for manual posting
    print("\n🔧 MANUAL POSTING INSTRUCTIONS:")
    print("=" * 60)
    
    if profile_name == "sam-desigan":
        print("1. Open Chrome with Sam Desigan profile:")
        print(f"   open -a \"Google Chrome\" --args --user-data-dir=\"{profile_dir}\" --profile-directory=\"Sam Desigan LinkedIn\"")
    else:
        print("1. Open Chrome with Shyam Desigan profile:")
        print(f"   open -a \"Google Chrome\" --args --user-data-dir=\"{profile_dir}\" --profile-directory=\"Shyam Desigan LinkedIn\"")
    
    print("2. Go to: https://www.linkedin.com/feed/")
    print("3. Click 'Start a post'")
    print("4. Copy the content from above")
    print("5. Click 'Post'")
    print("6. Verify post appears in feed")
    print("7. Close browser")
    
    # Save post record
    save_post_record(profile_name, content, hashtags)
    
    return True

def save_post_record(profile_name, content, hashtags):
    """Save post record to history"""
    try:
        post_record = {
            "profile": profile_name,
            "content": content,
            "hashtags": hashtags or [],
            "timestamp": datetime.now().isoformat(),
            "platform": "linkedin",
            "method": "manual_chrome_profile"
        }
        
        # Load existing posts
        posts_file = "/Users/cubiczan/.openclaw/workspace/linkedin_posts_history.json"
        if os.path.exists(posts_file):
            with open(posts_file, 'r') as f:
                posts = json.load(f)
        else:
            posts = []
        
        # Add new post
        posts.append(post_record)
        
        # Save back to file
        with open(posts_file, 'w') as f:
            json.dump(posts, f, indent=2)
        
        print(f"\n💾 Post record saved to: {posts_file}")
        
    except Exception as e:
        print(f"❌ Error saving post record: {e}")

def post_todays_content():
    """Post today's scheduled content"""
    print("🚀 POSTING TODAY'S LINKEDIN CONTENT")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Today's posts
    todays_posts = [
        {
            "profile": "shyam-desigan",
            "time": "08:00",
            "topic": "Tech Innovation Frameworks",
            "content": """Technology innovation frameworks that actually work:

1. Problem-First Approach
   Start with the pain point, not the technology

2. Cross-Disciplinary Application
   Apply solutions from other industries

3. Iterative Validation
   Test small, learn fast, scale what works

What framework do you use? #TechInnovation #BusinessTech #Innovation #Methodology #ShyamDesigan""",
            "hashtags": ["#TechInnovation", "#BusinessTech", "#Innovation", "#Methodology", "#ShyamDesigan"]
        },
        {
            "profile": "sam-desigan",
            "time": "09:00",
            "topic": "AI Finance Trends",
            "content": """AI is transforming finance faster than most realize.

This week's key trends:
1. Algorithmic trading adoption accelerating
2. Real-time risk assessment becoming standard
3. Predictive analytics for market movements

The gap between early adopters and laggards is widening. #AIFinance #FinTech #Trading #Innovation #SamDesigan""",
            "hashtags": ["#AIFinance", "#FinTech", "#Trading", "#Innovation", "#SamDesigan"]
        }
    ]
    
    current_time = datetime.now().strftime("%H:%M")
    
    print(f"⏰ Current time: {current_time}")
    print(f"📋 {len(todays_posts)} posts scheduled for today")
    
    # Post each one
    for post in todays_posts:
        print(f"\n🎯 POST: {post['profile']} - {post['time']}")
        print(f"   Topic: {post['topic']}")
        
        # Check if it's time to post
        post_hour = int(post['time'].split(":")[0])
        post_minute = int(post['time'].split(":")[1])
        current_hour = int(current_time.split(":")[0])
        current_minute = int(current_time.split(":")[1])
        
        time_diff = abs((current_hour * 60 + current_minute) - (post_hour * 60 + post_minute))
        
        if time_diff <= 30:  # Within 30 minutes of scheduled time
            print(f"   ⏰ Time to post: YES (within {time_diff} minutes)")
            
            # Ask for confirmation
            response = input(f"\nPost for {post['profile']} now? (y/n): ").strip().lower()
            
            if response == 'y':
                success = post_to_linkedin_manual(
                    profile_name=post['profile'],
                    content=post['content'],
                    hashtags=post['hashtags']
                )
                
                if success:
                    print(f"\n✅ POST READY FOR {post['profile'].upper()}")
                    print("Follow the manual instructions above to post.")
                else:
                    print(f"\n❌ Failed to prepare post for {post['profile']}")
            else:
                print(f"\n⏸️  Skipping post for {post['profile']}")
        else:
            print(f"   ⏰ Time to post: NO ({time_diff} minutes from scheduled time)")
    
    print("\n" + "=" * 60)
    print("✅ TODAY'S POSTING COMPLETE!")
    print("=" * 60)
    
    print("\n🎯 NEXT STEPS:")
    print("1. Follow manual instructions for each post")
    print("2. Verify posts appear on LinkedIn")
    print("3. Monitor engagement")
    print("4. We'll fix automation for tomorrow")
    
    print("\n📊 CHECK POST HISTORY:")
    print("cat /Users/cubiczan/.openclaw/workspace/linkedin_posts_history.json | jq '.[-2:]'")

def main():
    """Main function"""
    print("🚀 LINKEDIN MANUAL POSTING WORKAROUND")
    print("=" * 60)
    print("Since Pinchtab API has issues, we'll use direct Chrome profiles.")
    print("This is a temporary workaround until automation is fixed.")
    print("=" * 60)
    
    post_todays_content()

if __name__ == "__main__":
    main()