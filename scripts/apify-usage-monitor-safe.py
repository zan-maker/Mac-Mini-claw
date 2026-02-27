#!/usr/bin/env python3
"""
Monitor Apify API usage - SAFE VERSION (no API keys)
"""

import requests
import json
from datetime import datetime

# API token should be set as environment variable
# export APIFY_API_TOKEN="your_token_here"

def check_usage():
    """Check current Apify usage"""
    import os
    
    APIFY_API_TOKEN = os.environ.get("APIFY_API_TOKEN")
    
    if not APIFY_API_TOKEN:
        print("❌ APIFY_API_TOKEN environment variable not set")
        print("   Set it with: export APIFY_API_TOKEN='your_token_here'")
        return None
    
    headers = {
        "Authorization": f"Bearer {APIFY_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        # Get usage information
        response = requests.get(
            "https://api.apify.com/v2/users/me/usage",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            usage_data = response.json()
            usage_usd = usage_data.get("data", {}).get("usageUsd", 0)
            
            print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"💰 Usage: ${usage_usd:.2f}")
            print(f"💳 Remaining (Free Tier): ${5 - usage_usd:.2f}")
            
            if usage_usd > 4:
                print("⚠️  WARNING: Approaching free tier limit ($5)")
            elif usage_usd > 3:
                print("ℹ️  INFO: Moderate usage, monitor closely")
            else:
                print("✅ OK: Within safe usage limits")
                
            return usage_usd
        else:
            print(f"❌ Failed to get usage: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    check_usage()