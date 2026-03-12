#!/usr/bin/env python3
"""
Social Media Automation Main File
"""

import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.social_media_automation import SocialMediaAutomation, LinkedInProfile

def main():
    """Main function to run social media automation"""
    print("🤖 SOCIAL MEDIA AUTOMATION WITH PINCHTAB")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("👥 Profiles: Sam Desigan & Shyam Desigan")
    print("🎯 Strategy: Dual LinkedIn Content & Engagement")
    print("=" * 60)
    
    # Create automation instance
    automation = SocialMediaAutomation()
    
    try:
        # Setup profiles
        print("\n1. Setting up LinkedIn profiles...")
        if automation.setup_profiles():
            print("✅ Profiles setup complete")
        else:
            print("⚠️  Profile setup had issues (manual login may be required)")
        
        # Run automation cycle
        print("\n2. Running automation cycle...")
        success = automation.run_automation_cycle()
        
        if success:
            print("✅ Automation cycle complete")
        else:
            print("⚠️  Automation cycle had issues")
        
        # Generate report
        print("\n3. Generating activity report...")
        report = automation.generate_report()
        
        if "error" in report:
            print(f"❌ Error generating report: {report['error']}")
        else:
            print("\n📊 SOCIAL MEDIA REPORT:")
            print("-" * 40)
            
            # Profile status
            profiles = report.get("profiles_setup", {})
            print(f"Profiles Setup:")
            print(f"  Sam Desigan: {'✅' if profiles.get('sam') else '❌'}")
            print(f"  Shyam Desigan: {'✅' if profiles.get('shyam') else '❌'}")
            
            # Posts today
            posts = report.get("posts_today", {})
            print(f"\nPosts Today:")
            print(f"  Sam: {posts.get('sam', 0)}/2 (daily limit)")
            print(f"  Shyam: {posts.get('shyam', 0)}/2 (daily limit)")
            
            # Next optimal times
            next_times = report.get("next_optimal_times", {})
            print(f"\nNext Optimal Posting Times:")
            print(f"  Sam: {next_times.get('sam', 'N/A')}")
            print(f"  Shyam: {next_times.get('shyam', 'N/A')}")
        
        # Save report
        report_file = "/Users/cubiczan/.openclaw/workspace/social_media_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Report saved to: {report_file}")
        
        # Next steps
        print("\n🎯 NEXT STEPS:")
        print("1. Review posts in linkedin_posts.json")
        print("2. Check cross-promotion content in cross_promotion.json")
        print("3. Schedule automation to run 2-3 times daily")
        print("4. Monitor engagement and adjust content strategy")
        
        # Integration options
        print("\n🤖 INTEGRATION OPTIONS:")
        print("To schedule automated posting:")
        print("  crontab -e")
        print("  Add: 0 9,12,17,20 * * * python3 /path/to/run_social_media.py")
        
        print("\n🎉 Social media automation setup complete!")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error in social media automation: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        # Cleanup
        print("\n🧹 Cleaning up resources...")
        automation.cleanup()
        print("✅ Cleanup complete")

if __name__ == "__main__":
    sys.exit(main())