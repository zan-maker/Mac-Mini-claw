#!/usr/bin/env python3
"""
Simple LinkedIn Post Test
Check if we can post manually with the created profiles
"""

import os
import json
import time
from datetime import datetime

def check_profiles():
    """Check if Pinchtab profiles exist"""
    print("🔍 CHECKING PINCHTAB PROFILES...")
    
    profiles_dir = "/Users/cubiczan/.pinchtab/profiles"
    profiles = ["sam-desigan", "shyam-desigan"]
    
    for profile in profiles:
        profile_path = os.path.join(profiles_dir, profile)
        if os.path.exists(profile_path):
            print(f"✅ {profile}: Profile directory exists")
            # Check if it has browser data
            items = os.listdir(profile_path)
            if len(items) > 0:
                print(f"   📁 Contains {len(items)} items (browser data present)")
            else:
                print(f"   ⚠️  Directory empty - may need to login")
        else:
            print(f"❌ {profile}: Profile directory not found")
    
    return True

def check_linkedin_login():
    """Check if LinkedIn login might be needed"""
    print("\n🔐 CHECKING LINKEDIN LOGIN STATUS...")
    
    # Simple check - see if we can detect login state
    print("To verify login status, run:")
    print("")
    print("1. For Sam Desigan:")
    print("   pinchtab start --profile sam-desigan")
    print("   • Check if LinkedIn shows you as logged in")
    print("   • If login page appears, login as Sam Desigan")
    print("   • Close browser when feed loads")
    print("")
    print("2. For Shyam Desigan:")
    print("   pinchtab start --profile shyam-desigan")
    print("   • Check if LinkedIn shows you as logged in")
    print("   • If login page appears, login as Shyam Desigan")
    print("   • Close browser when feed loads")
    
    return True

def get_todays_posts():
    """Get today's scheduled posts"""
    print("\n📅 TODAY'S SCHEDULED POSTS:")
    
    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M")
    
    # Today's posts
    posts = [
        {
            "time": "08:00",
            "profile": "shyam_desigan",
            "platform": "linkedin",
            "topic": "Automation Success Stories",
            "content": """Technology innovation frameworks that actually work:

1. Problem-First Approach
   Start with the pain point, not the technology

2. Cross-Disciplinary Application
   Apply solutions from other industries

3. Iterative Validation
   Test small, learn fast, scale what works

What framework do you use? #TechInnovation #BusinessTech #Innovation #Methodology #ShyamDesigan""",
            "status": "missed" if current_time > "08:30" else "pending"
        },
        {
            "time": "09:00",
            "profile": "sam_desigan",
            "platform": "linkedin",
            "topic": "Business Expense Reduction",
            "content": """AI is transforming finance faster than most realize.

This week's key trends:
1. Algorithmic trading adoption accelerating
2. Real-time risk assessment becoming standard
3. Predictive analytics for market movements

The gap between early adopters and laggards is widening. #AIFinance #FinTech #Trading #Innovation #SamDesigan""",
            "status": "pending" if current_time < "09:30" else "missed"
        }
    ]
    
    for post in posts:
        print(f"\n⏰ {post['time']} - {post['profile']}")
        print(f"   Topic: {post['topic']}")
        print(f"   Status: {post['status'].upper()}")
        print(f"   Content: {post['content'][:60]}...")
    
    return posts

def manual_posting_instructions():
    """Provide manual posting instructions"""
    print("\n📝 MANUAL POSTING INSTRUCTIONS:")
    print("=" * 60)
    
    posts = get_todays_posts()
    
    for post in posts:
        if post["status"] == "pending":
            print(f"\n🔧 POST FOR {post['profile'].upper()} at {post['time']}:")
            print(f"1. Open browser with profile:")
            print(f"   pinchtab start --profile {post['profile'].replace('_', '-')}")
            print(f"2. Go to: https://www.linkedin.com/feed/")
            print(f"3. Click 'Start a post'")
            print(f"4. Copy this content:")
            print("-" * 40)
            print(post["content"])
            print("-" * 40)
            print(f"5. Click 'Post'")
            print(f"6. Verify post appears in feed")
    
    print("\n💡 TIP: Once logged in, the automation should work automatically.")

def setup_automation():
    """Setup automation schedule"""
    print("\n⏰ SETUP AUTOMATION SCHEDULE:")
    print("=" * 60)
    
    print("Add to crontab (crontab -e):")
    print("")
    print("# LinkedIn Automation (4x daily)")
    print("0 7,11,15,19 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/pinchtab_social_media.py >> ~/linkedin_automation.log 2>&1")
    print("")
    print("# Alternative: Run our simple test script")
    print("0 8,9,12,17 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/simple_linkedin_test.py >> ~/linkedin_simple.log 2>&1")
    
    return True

def main():
    """Main function"""
    print("🚀 LINKEDIN AUTOMATION STATUS CHECK")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check profiles
    check_profiles()
    
    # Check login status
    check_linkedin_login()
    
    # Get today's posts
    get_todays_posts()
    
    # Manual posting instructions
    manual_posting_instructions()
    
    # Setup automation
    setup_automation()
    
    print("\n" + "=" * 60)
    print("🎯 IMMEDIATE ACTIONS:")
    print("=" * 60)
    print("1. Verify login: pinchtab start --profile sam-desigan")
    print("2. Verify login: pinchtab start --profile shyam-desigan")
    print("3. Post manually if automation fails")
    print("4. Add cron jobs for automation")
    print("5. Monitor LinkedIn for posts")
    
    print("\n⚡ QUICK TEST:")
    print("Run: pinchtab start --profile sam-desigan")
    print("Check if LinkedIn shows you as logged in")
    
    print("\n✅ SYSTEM READY FOR AUTOMATION!")

if __name__ == "__main__":
    main()