#!/usr/bin/env python3
"""
LinkedIN Posting Instructions - Non-interactive
Provides clear instructions for manual posting
"""

import os
import json
from datetime import datetime

def generate_post_instructions():
    """Generate posting instructions for today"""
    print("🚀 LINKEDIN POSTING INSTRUCTIONS")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Pinchtab API has issues. Use these manual instructions.")
    print("=" * 60)
    
    # Today's posts
    todays_posts = [
        {
            "profile": "shyam-desigan",
            "display_name": "Shyam Desigan",
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
            "display_name": "Sam Desigan",
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
    print("")
    
    for i, post in enumerate(todays_posts):
        print(f"{i+1}. {post['display_name']} - {post['time']}")
        print(f"   Topic: {post['topic']}")
        
        # Check if it's time to post
        post_hour = int(post['time'].split(":")[0])
        post_minute = int(post['time'].split(":")[1])
        current_hour = int(current_time.split(":")[0])
        current_minute = int(current_time.split(":")[1])
        
        time_diff = abs((current_hour * 60 + current_minute) - (post_hour * 60 + post_minute))
        
        if time_diff <= 30:
            status = "✅ POST NOW"
        else:
            status = f"⏰ Post at {post['time']} ({time_diff} minutes from now)"
        
        print(f"   Status: {status}")
        print("")
    
    print("=" * 60)
    print("🔧 POSTING INSTRUCTIONS FOR EACH PROFILE:")
    print("=" * 60)
    
    for post in todays_posts:
        print(f"\n🎯 {post['display_name'].upper()} ({post['time']}):")
        print("-" * 40)
        
        # Chrome command
        profile_dir = f"/Users/cubiczan/.pinchtab/profiles/{post['profile']}"
        
        print(f"1. Open Chrome with {post['display_name']} profile:")
        print(f"   open -a \"Google Chrome\" --args --user-data-dir=\"{profile_dir}\" --profile-directory=\"{post['display_name']} LinkedIn\"")
        print("")
        print("2. Go to: https://www.linkedin.com/feed/")
        print("")
        print("3. Click 'Start a post'")
        print("")
        print("4. Copy this content:")
        print("=" * 40)
        print(post['content'])
        if post['hashtags']:
            print(" ".join(post['hashtags']))
        print("=" * 40)
        print("")
        print("5. Click 'Post'")
        print("")
        print("6. Verify post appears in feed")
        print("")
        print("7. Close browser")
        print("-" * 40)
    
    print("\n" + "=" * 60)
    print("🎯 ACTION PLAN:")
    print("=" * 60)
    print("1. Post Shyam Desigan content NOW (8:00 AM scheduled)")
    print("2. Post Sam Desigan content at 9:00 AM")
    print("3. We'll fix automation for tomorrow")
    print("4. Setup cron jobs once fixed")
    
    print("\n⚡ QUICK COMMANDS:")
    print("=" * 60)
    print("# Post Shyam Desigan (run now):")
    print(f"open -a \"Google Chrome\" --args --user-data-dir=\"/Users/cubiczan/.pinchtab/profiles/shyam-desigan\" --profile-directory=\"Shyam Desigan LinkedIn\"")
    print("")
    print("# Post Sam Desigan (run at 9:00 AM):")
    print(f"open -a \"Google Chrome\" --args --user-data-dir=\"/Users/cubiczan/.pinchtab/profiles/sam-desigan\" --profile-directory=\"Sam Desigan LinkedIn\"")
    
    print("\n📊 POST HISTORY:")
    print("cat /Users/cubiczan/.openclaw/workspace/linkedin_posts_history.json | jq '.[-2:]'")
    
    print("\n✅ READY FOR MANUAL POSTING!")

def main():
    """Main function"""
    generate_post_instructions()

if __name__ == "__main__":
    main()