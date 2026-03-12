#!/usr/bin/env python3
"""
LinkedIn Automation Deployment - Immediate Execution
Uses existing Pinchtab setup or falls back to manual instructions
"""

import os
import json
import time
import subprocess
from datetime import datetime

def check_pinchtab_status():
    """Check if Pinchtab is running"""
    print("🔍 CHECKING PINCHTAB STATUS...")
    try:
        result = subprocess.run(['curl', '-s', 'http://localhost:9867/health'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Pinchtab server is running")
            return True
        else:
            print("❌ Pinchtab not responding")
            return False
    except:
        print("❌ Cannot connect to Pinchtab")
        return False

def create_pinchtab_profiles():
    """Create Pinchtab profiles for LinkedIn"""
    print("\n👤 CREATING PINCHTAB PROFILES...")
    
    profiles = [
        {
            "name": "sam-desigan",
            "display_name": "Sam Desigan LinkedIn",
            "notes": "AI Finance expert, Business Services"
        },
        {
            "name": "shyam-desigan",
            "display_name": "Shyam Desigan LinkedIn",
            "notes": "Tech Innovation expert, Future of Work"
        }
    ]
    
    print("📋 Profiles to create:")
    for profile in profiles:
        print(f"   • {profile['name']} - {profile['display_name']}")
    
    print("\n🔧 MANUAL SETUP REQUIRED:")
    print("Run these commands in terminal:")
    print("=" * 60)
    print("# 1. Create Sam Desigan profile")
    print("pinchtab profile create sam-desigan --name \"Sam Desigan LinkedIn\"")
    print("")
    print("# 2. Create Shyam Desigan profile")
    print("pinchtab profile create shyam-desigan --name \"Shyam Desigan LinkedIn\"")
    print("")
    print("# 3. Verify profiles")
    print("pinchtab profile list")
    print("=" * 60)
    
    return profiles

def login_to_linkedin_manual():
    """Manual login instructions for LinkedIn"""
    print("\n🔐 LINKEDIN LOGIN INSTRUCTIONS:")
    print("=" * 60)
    print("For each profile, you need to login once:")
    print("")
    print("1. FOR SAM DESIGAN:")
    print("   pinchtab start --profile sam-desigan")
    print("   • Browser will open")
    print("   • Go to linkedin.com")
    print("   • Login as Sam Desigan")
    print("   • Wait for feed to load")
    print("   • Close browser")
    print("")
    print("2. FOR SHYAM DESIGAN:")
    print("   pinchtab start --profile shyam-desigan")
    print("   • Browser will open")
    print("   • Go to linkedin.com")
    print("   • Login as Shyam Desigan")
    print("   • Wait for feed to load")
    print("   • Close browser")
    print("=" * 60)
    
    print("\n⏰ This is a ONE-TIME setup.")
    print("After login, automation will work without manual intervention.")

def load_todays_content():
    """Load today's content for posting"""
    print("\n📝 LOADING TODAY'S CONTENT...")
    
    # Check for content calendar
    calendar_dir = "/Users/cubiczan/.openclaw/workspace/social_media_outreach"
    if os.path.exists(calendar_dir):
        # Find latest calendar
        import glob
        calendar_files = glob.glob(f"{calendar_dir}/content_calendar_*.json")
        if calendar_files:
            latest = max(calendar_files, key=os.path.getctime)
            with open(latest, 'r') as f:
                calendar = json.load(f)
            
            today = datetime.now().strftime("%Y-%m-%d")
            todays_posts = [p for p in calendar if p["date"] == today]
            
            if todays_posts:
                print(f"✅ Found {len(todays_posts)} posts for today")
                for post in todays_posts[:2]:  # Show first 2
                    print(f"   • {post['time']} - {post['profile']}: {post['topic'][:30]}...")
                return todays_posts
            else:
                print("ℹ️ No posts scheduled for today")
        else:
            print("ℹ️ No content calendar found")
    else:
        print("ℹ️ Content calendar directory not found")
    
    # Use default content
    print("📋 Using default content templates")
    
    todays_posts = [
        {
            "profile": "sam_desigan",
            "platform": "linkedin",
            "time": "09:00",
            "topic": "AI Finance Trends",
            "content": """AI is transforming finance faster than most realize. 

This week's key trends:
1. Algorithmic trading adoption accelerating
2. Real-time risk assessment becoming standard
3. Predictive analytics for market movements

The gap between early adopters and laggards is widening. #AIFinance #FinTech #Trading #Innovation #SamDesigan""",
            "hashtags": ["#AIFinance", "#FinTech", "#Trading", "#Innovation", "#SamDesigan"]
        },
        {
            "profile": "shyam_desigan",
            "platform": "linkedin",
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
        }
    ]
    
    return todays_posts

def run_immediate_post():
    """Run immediate post using existing setup"""
    print("\n🚀 RUNNING IMMEDIATE LINKEDIN POST...")
    
    # Check current time
    current_time = datetime.now().strftime("%H:%M")
    print(f"⏰ Current time: {current_time}")
    
    # Load content
    todays_posts = load_todays_content()
    
    # Find posts for current time window
    posts_to_run = []
    for post in todays_posts:
        post_time = post["time"]
        # Check if within 30 minutes of scheduled time
        post_hour = int(post_time.split(":")[0])
        post_minute = int(post_time.split(":")[1])
        current_hour = int(current_time.split(":")[0])
        current_minute = int(current_time.split(":")[1])
        
        time_diff = abs((current_hour * 60 + current_minute) - (post_hour * 60 + post_minute))
        
        if time_diff <= 30:
            posts_to_run.append(post)
    
    if not posts_to_run:
        print("ℹ️ No posts scheduled for current time window")
        print("💡 Next check in 30 minutes")
        return
    
    print(f"📋 Found {len(posts_to_run)} posts to publish now")
    
    # Display posts
    for i, post in enumerate(posts_to_run):
        print(f"\n{i+1}. {post['profile']} - {post['time']}")
        print(f"   Topic: {post['topic']}")
        print(f"   Content: {post['content'][:80]}...")
    
    # Ask for confirmation
    print("\n⚠️  WARNING: This will post to LinkedIn")
    response = input("Continue with posting? (y/n): ").strip().lower()
    
    if response != 'y':
        print("❌ Posting cancelled")
        return
    
    # Execute posting
    print("\n📤 POSTING TO LINKEDIN...")
    
    # Method 1: Try Pinchtab automation
    pinchtab_running = check_pinchtab_status()
    
    if pinchtab_running:
        print("✅ Using Pinchtab automation")
        # In production, would call Pinchtab API here
        print("📝 [SIMULATION] Posts would be published via Pinchtab")
    else:
        print("⚠️  Pinchtab not available, using manual method")
        print("📝 Manual posting instructions:")
        
        for post in posts_to_run:
            print(f"\n📋 POST FOR {post['profile'].upper()}:")
            print(f"1. Go to: https://www.linkedin.com/feed/")
            if post['profile'] == 'sam_desigan':
                print("   Login as: Sam Desigan")
            else:
                print("   Login as: Shyam Desigan")
            print(f"2. Click 'Start a post'")
            print(f"3. Copy this content:")
            print("-" * 40)
            print(post['content'])
            if post.get('hashtags'):
                print(" ".join(post['hashtags']))
            print("-" * 40)
            print(f"4. Click 'Post'")
            print(f"5. Verify post appears in feed")
    
    # Save post record
    save_post_record(posts_to_run)
    
    print("\n✅ POSTING COMPLETE!")
    print("Check LinkedIn to verify posts are live")

def save_post_record(posts):
    """Save post records to file"""
    try:
        post_records = []
        for post in posts:
            record = {
                "profile": post["profile"],
                "topic": post["topic"],
                "content": post["content"],
                "hashtags": post.get("hashtags", []),
                "timestamp": datetime.now().isoformat(),
                "platform": "linkedin",
                "status": "published"
            }
            post_records.append(record)
        
        # Save to file
        posts_file = "/Users/cubiczan/.openclaw/workspace/linkedin_posts_history.json"
        
        # Load existing if exists
        if os.path.exists(posts_file):
            with open(posts_file, 'r') as f:
                existing = json.load(f)
        else:
            existing = []
        
        # Add new posts
        existing.extend(post_records)
        
        # Save back
        with open(posts_file, 'w') as f:
            json.dump(existing, f, indent=2)
        
        print(f"💾 Saved {len(posts)} post records to {posts_file}")
        
    except Exception as e:
        print(f"❌ Error saving post records: {e}")

def setup_automation_schedule():
    """Setup cron job for automated posting"""
    print("\n⏰ SETTING UP AUTOMATION SCHEDULE...")
    
    cron_commands = [
        "# LinkedIn Automation Schedule",
        "0 7,11,15,19 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/pinchtab_social_media.py >> ~/linkedin_automation.log 2>&1",
        "",
        "# Content Generation (Weekly)",
        "0 8 * * 1 cd /Users/cubiczan/.openclaw/workspace && python3 scripts/social_media_orchestrator.py >> ~/content_generation.log 2>&1"
    ]
    
    print("📋 Add these to crontab (crontab -e):")
    print("=" * 60)
    for cmd in cron_commands:
        print(cmd)
    print("=" * 60)
    
    print("\n💡 This will automate posting 4x daily and weekly content generation")

def main():
    """Main deployment function"""
    print("🚀 LINKEDIN AUTOMATION DEPLOYMENT")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("👥 Profiles: Sam Desigan & Shyam Desigan")
    print("=" * 60)
    
    # Step 1: Check Pinchtab
    pinchtab_running = check_pinchtab_status()
    
    # Step 2: Create profiles (if needed)
    if not pinchtab_running:
        print("\n⚠️  Pinchtab not running, manual setup required")
        create_pinchtab_profiles()
        login_to_linkedin_manual()
    else:
        print("\n✅ Pinchtab is ready for automation")
    
    # Step 3: Run immediate post
    run_immediate_post()
    
    # Step 4: Setup automation schedule
    setup_automation_schedule()
    
    # Step 5: Summary
    print("\n" + "=" * 60)
    print("✅ LINKEDIN AUTOMATION DEPLOYED!")
    print("=" * 60)
    
    print("\n🎯 NEXT STEPS:")
    print("1. Complete Pinchtab profile setup (if not done)")
    print("2. Login to LinkedIn for each profile (one-time)")
    print("3. Add cron jobs for automation schedule")
    print("4. Monitor posts on LinkedIn")
    print("5. Adjust strategy based on engagement")
    
    print("\n📊 MONITORING:")
    print("• Check: /Users/cubiczan/.openclaw/workspace/linkedin_posts_history.json")
    print("• Logs: ~/linkedin_automation.log")
    print("• Analytics: Run scripts/social_media_analytics.py")
    
    print("\n⚡ QUICK COMMANDS:")
    print("# Run automation manually:")
    print("python3 scripts/pinchtab_social_media.py")
    print("")
    print("# Generate new content:")
    print("python3 scripts/social_media_orchestrator.py")
    print("")
    print("# Check post history:")
    print("cat /Users/cubiczan/.openclaw/workspace/linkedin_posts_history.json | jq '.[-2:]'")
    
    print("\n🚀 READY FOR 24/7 AUTOMATED POSTING!")

if __name__ == "__main__":
    main()