#!/usr/bin/env python3
"""
Gas Price Monitor - SECURE VERSION
Uses environment variables
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_env_var(name):
    value = os.environ.get(name)
    if not value:
        print(f"❌ {name} not set in .env")
        sys.exit(1)
    return value

def main():
    print("⛽ GAS PRICE MONITOR")
    print("=" * 50)
    
    # Get API keys securely
    news_key = get_env_var("NEWS_API_KEY")
    serper_key = get_env_var("SERPER_API_KEY")
    
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔑 API Keys loaded: {news_key[:10]}..., {serper_key[:10]}...")
    print("")
    
    # Mock gas price analysis (replace with real API calls)
    print("📊 GAS MARKET ANALYSIS:")
    print("-" * 50)
    print("1. Current Price: $3.20/gallon")
    print("2. Target (Kalshi): >$3.50")
    print("3. Needed Move: +$0.30")
    print("4. Days Remaining: 25")
    print("5. Health Score: 60/100")
    print("")
    print("🎯 RECOMMENDATION: HOLD position")
    print("💰 POTENTIAL PROFIT: $8-12 if target hit")
    print("")
    print("📰 RECENT CATALYSTS:")
    print("- OPEC meeting this week")
    print("- Inventory report tomorrow")
    print("- Weather affecting demand")
    
    print("=" * 50)
    print("✅ Monitor complete")

if __name__ == "__main__":
    main()
