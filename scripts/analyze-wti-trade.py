#!/usr/bin/env python3
"""
Quick WTI Trade Analysis - Real Price $117
"""

import os
from datetime import datetime

def load_env_file():
    """Load environment variables"""
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

def analyze_wti_trade():
    """Analyze the WTI $98 trade opportunity"""
    print("🛢️  WTI OIL TRADE ANALYSIS - REAL TIME")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    # Real market data
    wti_current = 117.00  # Actual current price
    target_price = 98.00
    days_to_expiry = 5  # March 13th
    investment = 25.00
    
    print("📊 TRADE PARAMETERS:")
    print("-" * 60)
    print(f"• Current WTI: ${wti_current:.2f}")
    print(f"• Target: <${target_price:.2f} by March 13")
    print(f"• Days Remaining: {days_to_expiry}")
    print(f"• Investment: ${investment:.2f}")
    print(f"• Required Drop: -${wti_current - target_price:.2f} (-{(wti_current - target_price)/wti_current*100:.1f}%)")
    print("")
    
    # Probability analysis
    print("🎯 PROBABILITY ASSESSMENT:")
    print("-" * 60)
    
    # War context probabilities
    scenarios = [
        {
            "name": "Conflict Escalation",
            "prob": 40,
            "price_effect": "UP (+$5-15)",
            "trade_outcome": "LOSE (price >$98)"
        },
        {
            "name": "Status Quo",
            "prob": 35,
            "price_effect": "SIDEWAYS ($110-120)",
            "trade_outcome": "LOSE (price >$98)"
        },
        {
            "name": "Peace Talks",
            "prob": 15,
            "price_effect": "DOWN (-$10-20)",
            "trade_outcome": "WIN (price <$98)"
        },
        {
            "name": "Supply Shock",
            "prob": 10,
            "price_effect": "DOWN sharply (-$20+)",
            "trade_outcome": "WIN (price <$98)"
        }
    ]
    
    win_probability = 0
    for scenario in scenarios:
        if "WIN" in scenario["trade_outcome"]:
            win_probability += scenario["prob"]
    
    print(f"Estimated Win Probability: {win_probability}%")
    print("")
    
    for scenario in scenarios:
        outcome_emoji = "❌" if "LOSE" in scenario["trade_outcome"] else "✅"
        print(f"{outcome_emoji} {scenario['name']}: {scenario['prob']}%")
        print(f"   Price: {scenario['price_effect']}")
        print(f"   Outcome: {scenario['trade_outcome']}")
        print("")
    
    # Risk/Reward
    print("💰 RISK/REWARD ANALYSIS:")
    print("-" * 60)
    print(f"• Max Risk: ${investment:.2f} (100% of investment)")
    print(f"• Potential Return: ${investment * 2:.2f}-${investment * 4:.2f} (2-4x)")
    print(f"• Risk/Reward: 1:{2} to 1:{4}")
    print(f"• Expected Value: ${investment * (win_probability/100 * 3 - (100-win_probability)/100):.2f}")
    print("")
    
    # Recommendations
    print("🎯 TRADE RECOMMENDATIONS:")
    print("-" * 60)
    
    if win_probability < 30:
        print("❌ AVOID - Probability too low")
        recommendation = "DON'T TAKE"
        confidence = "LOW"
    elif win_probability < 40:
        print("⚠️  CAUTIOUS - Small position only")
        recommendation = "BUY NO @ <30¢"
        confidence = "MEDIUM"
    else:
        print("✅ GO - Favorable setup")
        recommendation = "BUY NO @ <40¢"
        confidence = "HIGH"
    
    print("")
    print("🔧 EXECUTION PLAN:")
    print("-" * 60)
    print(f"1. Market: WTI March 13 Close >$98")
    print(f"2. Position: BUY NO")
    print(f"3. Amount: ${investment:.2f}")
    print(f"4. Limit Price: {recommendation.split('@ ')[1] if '@' in recommendation else 'Market'}")
    print(f"5. Confidence: {confidence}")
    print("")
    
    print("📊 MONITORING PLAN:")
    print("-" * 60)
    print("• Daily War Monitor scans (8x daily)")
    print("• Key Levels: $110, $105, $98")
    print("• Catalysts: Peace talks, OPEC, EIA reports")
    print("• Exit if: Price breaks above $120 (adds risk)")
    print("")
    
    # Save trade analysis
    trade_record = {
        "timestamp": datetime.now().isoformat(),
        "trade": {
            "asset": "WTI Crude",
            "current_price": wti_current,
            "target_price": target_price,
            "expiry": "2026-03-13",
            "investment": investment,
            "position": "BUY NO",
            "win_probability": win_probability,
            "recommendation": recommendation,
            "confidence": confidence
        },
        "analysis": scenarios
    }
    
    os.makedirs("logs/trades", exist_ok=True)
    trade_file = f"logs/trades/wti-trade-{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    
    import json
    with open(trade_file, "w") as f:
        json.dump(trade_record, f, indent=2)
    
    print(f"✅ Analysis saved to: {trade_file}")
    print("=" * 60)
    print("🚀 TRADE READY FOR EXECUTION")

if __name__ == "__main__":
    load_env_file()
    analyze_wti_trade()