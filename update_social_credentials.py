#!/usr/bin/env python3
"""
Quick script to update social media credentials
"""

import os
import json
import sys

def update_credentials():
    """Update social media credentials"""
    print("🔧 Social Media Credentials Updater")
    print("="*60)
    
    config_path = "/Users/cubiczan/.openclaw/workspace/config/social_media_config.json"
    
    if not os.path.exists(config_path):
        print(f"❌ Config file not found: {config_path}")
        return False
    
    # Load current config
    with open(config_path, "r") as f:
        config = json.load(f)
    
    print("\n📋 CURRENT CONFIGURATION STATUS:")
    print("-"*40)
    
    platforms = config.get("platforms", {})
    
    for platform, settings in platforms.items():
        enabled = settings.get("enabled", False)
        creds = settings.get("credentials", {})
        
        print(f"\n{platform.upper()}:")
        print(f"  Enabled: {'✅' if enabled else '❌'}")
        
        if platform == "twitter_x":
            username = creds.get("username", "NOT SET")
            password_set = bool(creds.get("password")) and creds.get("password") != "YOUR_TWITTER_PASSWORD"
            print(f"  Username: {username}")
            print(f"  Password: {'✅ SET' if password_set else '❌ NOT SET'}")
            print(f"  API Key: {'✅ SET' if creds.get('api_key') else '❌ NOT SET'}")
        
        elif platform in ["instagram", "facebook"]:
            username = creds.get("username", "NOT SET")
            password_set = bool(creds.get("password")) and "YOUR_" not in str(creds.get("password", ""))
            print(f"  Username: {username}")
            print(f"  Password: {'✅ SET' if password_set else '❌ NOT SET'}")
    
    print("\n" + "="*60)
    print("🔄 UPDATE CREDENTIALS")
    print("="*60)
    
    update_choice = input("\nUpdate credentials? (y/n): ").lower()
    
    if update_choice != 'y':
        print("No changes made.")
        return True
    
    # Update Twitter credentials
    print("\n🐦 TWITTER/X CREDENTIALS:")
    print("-"*40)
    
    twitter_username = input("Twitter username (@username): ").strip()
    twitter_password = input("Twitter password: ").strip()
    
    if twitter_username and twitter_password:
        config["platforms"]["twitter_x"]["credentials"]["username"] = twitter_username
        config["platforms"]["twitter_x"]["credentials"]["password"] = twitter_password
        print("✅ Twitter credentials updated")
    
    # Update Instagram credentials
    print("\n📸 INSTAGRAM CREDENTIALS:")
    print("-"*40)
    
    instagram_username = input("Instagram username: ").strip()
    instagram_password = input("Instagram password: ").strip()
    
    if instagram_username and instagram_password:
        config["platforms"]["instagram"]["credentials"]["username"] = instagram_username
        config["platforms"]["instagram"]["credentials"]["password"] = instagram_password
        print("✅ Instagram credentials updated")
    
    # Update Facebook credentials
    print("\n📘 FACEBOOK CREDENTIALS:")
    print("-"*40)
    
    facebook_username = input("Facebook username/email: ").strip()
    facebook_password = input("Facebook password: ").strip()
    facebook_page = input("Facebook page name (optional): ").strip()
    
    if facebook_username and facebook_password:
        config["platforms"]["facebook"]["credentials"]["username"] = facebook_username
        config["platforms"]["facebook"]["credentials"]["password"] = facebook_password
        
        if facebook_page:
            config["platforms"]["facebook"]["pages"] = [facebook_page]
            print(f"✅ Facebook page set to: {facebook_page}")
        
        print("✅ Facebook credentials updated")
    
    # Save updated config
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Configuration saved to: {config_path}")
    
    # Show updated status
    print("\n" + "="*60)
    print("📊 UPDATED CONFIGURATION STATUS:")
    print("="*60)
    
    for platform, settings in config.get("platforms", {}).items():
        if platform in ["twitter_x", "instagram", "facebook"]:
            enabled = settings.get("enabled", False)
            creds = settings.get("credentials", {})
            
            print(f"\n{platform.upper()}:")
            print(f"  Enabled: {'✅' if enabled else '❌'}")
            
            if platform == "twitter_x":
                username = creds.get("username", "NOT SET")
                password_set = bool(creds.get("password")) and creds.get("password") != "YOUR_TWITTER_PASSWORD"
                print(f"  Username: {username}")
                print(f"  Password: {'✅ SET' if password_set else '❌ NOT SET'}")
            
            elif platform in ["instagram", "facebook"]:
                username = creds.get("username", "NOT SET")
                password_set = bool(creds.get("password")) and "YOUR_" not in str(creds.get("password", ""))
                print(f"  Username: {username}")
                print(f"  Password: {'✅ SET' if password_set else '❌ NOT SET'}")
    
    print("\n" + "="*60)
    print("🚀 NEXT STEPS:")
    print("="*60)
    
    print("\n1. Test Twitter browser automation:")
    print("   python3 test_twitter_browser.py")
    
    print("\n2. Test Instagram posting:")
    print("   python3 test_instagram_posting.py")
    
    print("\n3. Test Facebook posting:")
    print("   python3 test_facebook_posting.py")
    
    print("\n4. Run complete system:")
    print("   python3 immediate_social_poster.py")
    
    print("\n5. Generate AI-powered content:")
    print("   python3 xai_integration.py")
    
    return True

def main():
    """Main function"""
    success = update_credentials()
    
    if success:
        print("\n🎉 Credentials updated successfully!")
        print("\nRemember:")
        print("• Keep your credentials secure")
        print("• Test each platform individually first")
        print("• Start with test posts before full automation")
    else:
        print("\n⚠️  Credentials update failed")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()