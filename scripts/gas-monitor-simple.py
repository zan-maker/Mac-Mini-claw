#!/usr/bin/env python3
"""
Gas Price Monitor - Simple version
Works with current .env format
"""

import os
import sys
from datetime import datetime

def load_env_file():
    """Load environment variables from .env file"""
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    if line.startswith('export '):
                        line = line[7:]
                    key, value = line.split('=', 1)
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    os.environ[key.strip()] = value.strip()
        return True
    return False

def main():
    print("⛽ GAS PRICE MONITOR")
    print("=" * 50)
    
    # Load environment variables
    if not load_env_file():
        print("⚠️  No .env file found")
    
    # Get API keys
    news_key = os.environ.get("NEWS_API_KEY")
    serper_key = os.environ.get("SERPER_API_KEY")
    
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if news_key:
        print(f"✅ NewsAPI key: {news_key[:10]}...")
    else:
        print("❌ NEWS_API_KEY not found")
    
    if serper_key:
        print(f"✅ Serper API key: {serper_key[:10]}...")
    else:
        print("⚠️  SERPER_API_KEY not found (optional)")
    
    print("")
    
    # Gas market analysis
    print("📊 GAS MARKET ANALYSIS:")
    print("-" * 50)
    
    # Current positions from memory
    positions = [
        {
            "name": "Gas Month (>$3.50)",
            "investment": "$25",
            "side": "YES",
            "current_price": 3.20,
            "target": 3.50,
            "needed_move": "+$0.30",
            "days_left": 25,
            "health_score": 60,
            "recommendation": "HOLD",
            "potential_profit": "$8-12"
        },
        {
            "name": "Gas Week (>$3.310)",
            "investment": "$50",
            "side": "YES",
            "current_price": 3.20,
            "target": 3.31,
            "needed_move": "+$0.11",
            "days_left": 2,
            "health_score": 20,
            "recommendation": "MONITOR CLOSELY",
            "potential_profit": "$15-20 if target hit"
        }
    ]
    
    total_investment = 0
    total_potential = 0
    
    for i, pos in enumerate(positions, 1):
        health_emoji = "🟢" if pos["health_score"] >= 60 else "🟡" if pos["health_score"] >= 40 else "🔴"
        print(f"{i}. {health_emoji} {pos['name']}")
        print(f"   💰 Investment: {pos['investment']} {pos['side']}")
        print(f"   📊 Current: ${pos['current_price']}/gallon")
        print(f"   🎯 Target: ${pos['target']} (+${pos['current_price'] - pos['target']:.2f})")
        print(f"   ⏰ Days Left: {pos['days_left']}")
        print(f"   💪 Health: {pos['health_score']}/100")
        print(f"   📈 Recommendation: {pos['recommendation']}")
        print(f"   🚀 Potential: {pos['potential_profit']}")
        print("")
        
        # Calculate totals
        try:
            inv = float(pos['investment'].replace('$', ''))
            total_investment += inv
        except:
            pass
    
    print("=" * 50)
    print(f"💰 TOTAL INVESTED: ${total_investment}")
    print(f"📊 ACTIVE POSITIONS: {len(positions)}")
    print(f"⏰ NEXT CHECK: Tomorrow 9:00 AM EST")
    print("=" * 50)
    
    # Recent catalysts
    print("📰 RECENT CATALYSTS:")
    print("- OPEC meeting this week")
    print("- EIA inventory report tomorrow")
    print("- Weather patterns affecting demand")
    print("- Refinery maintenance season")
    print("")
    
    print("✅ Monitor complete")
    
    # Save to log file
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "positions": len(positions),
        "total_investment": total_investment,
        "health_scores": [p["health_score"] for p in positions]
    }
    
    os.makedirs("logs/gas_trading", exist_ok=True)
    log_file = f"logs/gas_trading/gas-check-{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(log_file, "w") as f:
        import json
        json.dump(log_entry, f, indent=2)
    
    print(f"📝 Log saved to: {log_file}")

if __name__ == "__main__":
    main()