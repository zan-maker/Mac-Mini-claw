#!/usr/bin/env python3
"""
Create Pinchtab LinkedIn profiles for social media automation
"""

import requests
import json
import time
from datetime import datetime

def create_pinchtab_profiles():
    """Create LinkedIn profiles in Pinchtab"""
    print("👤 CREATING PINCHTAB LINKEDIN PROFILES")
    print("=" * 60)
    
    base_url = "http://localhost:9867"
    
    # Check server status
    print("1. 🔍 CHECKING PINCHTAB SERVER...")
    try:
        health = requests.get(f"{base_url}/health", timeout=5)
        if health.status_code == 200:
            print(f"   ✅ Pinchtab server is running")
            print(f"   📊 Mode: {health.json().get('mode', 'unknown')}")
        else:
            print(f"   ❌ Server error: {health.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Cannot connect to Pinchtab: {e}")
        return False
    
    # Create profiles
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
    
    print("\n2. 🛠️ CREATING PROFILES...")
    created_profiles = []
    
    for profile in profiles:
        print(f"   📋 Creating: {profile['name']} - {profile['display_name']}")
        
        # Try to create via API
        try:
            # Note: Pinchtab API may have different endpoint structure
            # This is a placeholder for the actual API call
            print(f"   ⚠️  Profile creation would happen via Pinchtab API")
            print(f"   💡 Manual command: pinchtab profile create {profile['name']} --name \"{profile['display_name']}\"")
            
            # For now, just note what needs to be done
            created_profiles.append(profile['name'])
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n   ✅ Profiles to create: {', '.join(created_profiles)}")
    
    # Manual setup instructions
    print("\n3. 📋 MANUAL SETUP INSTRUCTIONS:")
    print("   Run these commands in terminal:")
    print("   ---------------------------------")
    print("   # Create Sam Desigan profile")
    print("   pinchtab profile create sam-desigan --name \"Sam Desigan LinkedIn\"")
    print("")
    print("   # Create Shyam Desigan profile")  
    print("   pinchtab profile create shyam-desigan --name \"Shyam Desigan LinkedIn\"")
    print("")
    print("   # Verify profiles")
    print("   pinchtab profile list")
    print("")
    print("   # Start browser with profile")
    print("   pinchtab start --profile sam-desigan")
    print("   # Then manually login to LinkedIn")
    print("   # Close when done")
    print("   # Repeat for shyam-desigan")
    
    return True

def check_existing_profiles():
    """Check if profiles already exist"""
    print("\n4. 🔍 CHECKING EXISTING PROFILES...")
    try:
        # Try to list profiles
        result = requests.get("http://localhost:9867/api/profiles", timeout=5)
        if result.status_code == 200:
            profiles = result.json()
            print(f"   📊 Found {len(profiles)} profiles")
            for profile in profiles:
                print(f"   👤 {profile.get('name', 'unknown')}: {profile.get('display_name', 'no name')}")
        else:
            print(f"   ℹ️  Could not list profiles (API may be different)")
    except:
        print("   ℹ️  Could not check existing profiles")

def main():
    """Main function"""
    print("🚀 PINCHTAB LINKEDIN PROFILE SETUP")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Create profiles
    success = create_pinchtab_profiles()
    
    # Check existing
    check_existing_profiles()
    
    print("\n" + "=" * 60)
    print("🎯 ACTION 2 COMPLETE: Pinchtab profile setup ready")
    print("   Next: Action 3 - Fix portfolio tracking")
    print("=" * 60)
    
    print("\n📋 QUICK START COMMANDS:")
    print("1. Create profiles:")
    print("   pinchtab profile create sam-desigan --name \"Sam Desigan LinkedIn\"")
    print("   pinchtab profile create shyam-desigan --name \"Shyam Desigan LinkedIn\"")
    print("")
    print("2. Login to LinkedIn (one-time):")
    print("   pinchtab start --profile sam-desigan")
    print("   # Login manually, then close")
    print("   # Repeat for shyam-desigan")
    print("")
    print("3. Test automation:")
    print("   python3 /Users/cubiczan/.openclaw/workspace/scripts/run_social_media.py")

if __name__ == "__main__":
    main()