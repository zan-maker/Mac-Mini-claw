#!/usr/bin/env python3
"""
WTI Trade Analysis - YES Position (Price >$98)
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

def analyze_wti_yes_trade():
    """Analyze the WTI YES >$98 trade"""
    print("🛢️  WTI OIL TRADE - YES POSITION ANALYSIS")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    # Market data
    wti_current = 117.00
    strike_price = 98.00
    days_to_expiry = 5
    investment = 25.00
    
    print("📊 TRADE PARAMETERS:")
    print("-" * 60)
    print(f"• Position: BUY YES on WTI >${strike_price:.2f}")
    print(f"• Current WTI: ${wti_current:.2f}")
    print(f"• Cushion: +${wti_current - strike_price:.2f} above strike")
    print(f"• Required Drop to Lose: -${wti_current - strike_price:.2f} (-{(wti_current - strike_price)/wti_current*100:.1f}%)")
    print(f"• Days to Expiry: {days_to_expiry}")
    print(f"• Investment: ${investment:.2f}")
    print("")
    
    # Probability analysis - YES position (price stays >$98)
    print("🎯 PROBABILITY ASSESSMENT (YES POSITION):")
    print("-" * 60)
    
    scenarios = [
        {
            "name": "Conflict Escalation",
            "prob": 40,
            "price_effect": "UP (+$5-15)",
            "trade_outcome": "WIN (price >$98)",
            "impact": "STRONGLY POSITIVE"
        },
        {
            "name": "Status Quo",
            "prob": 35,
            "price_effect": "SIDEWAYS ($110-120)",
            "trade_outcome": "WIN (price >$98)",
            "impact": "POSITIVE"
        },
        {
            "name": "Peace Talks Begin",
            "prob": 20,
            "price_effect": "DOWN (-$5-15)",
            "trade_outcome": "WIN (price >$98) - still above $98",
            "impact": "STILL WINNING"
        },
        {
            "name": "Major Peace Deal + Supply Surge",
            "prob": 5,
            "price_effect": "DOWN sharply (-$20+)",
            "trade_outcome": "LOSE (price <$98)",
            "impact": "NEGATIVE"
        }
    ]
    
    win_probability = 0
    for scenario in scenarios:
        if "WIN" in scenario["trade_outcome"]:
            win_probability += scenario["prob"]
    
    print(f"Estimated Win Probability: {win_probability}%")
    print("")
    
    for scenario in scenarios:
        outcome_emoji = "✅" if "WIN" in scenario["trade_outcome"] else "❌"
        print(f"{outcome_emoji} {scenario['name']}: {scenario['prob']}%")
        print(f"   Price: {scenario['price_effect']}")
        print(f"   Outcome: {scenario['trade_outcome']}")
        print(f"   Impact: {scenario['impact']}")
        print("")
    
    # Risk/Reward for YES position
    print("💰 RISK/REWARD ANALYSIS:")
    print("-" * 60)
    
    # Typical Kalshi pricing for YES position with high probability
    # If market thinks 95% chance YES wins, YES might trade at 90-95¢
    # Your $25 buys ~27-28 shares at 90¢
    
    entry_price = 0.90  # 90¢ per share (estimate)
    shares = investment / entry_price
    max_loss = investment
    potential_return = shares * (1.00 - entry_price)  # If settles at $1
    
    print(f"• Entry Price (est): {entry_price*100:.0f}¢ per share")
    print(f"• Shares Purchased: {shares:.1f}")
    print(f"• Max Risk: ${max_loss:.2f} (100% of investment)")
    print(f"• Potential Return: ${potential_return:.2f} (+{potential_return/investment*100:.1f}%)")
    print(f"• Risk/Reward: 1:{potential_return/investment:.2f}")
    print(f"• Expected Value: ${investment * (win_probability/100 * (potential_return/investment) - (100-win_probability)/100):.2f}")
    print("")
    
    # Trade recommendations
    print("🎯 TRADE ASSESSMENT:")
    print("-" * 60)
    
    if win_probability >= 90:
        assessment = "✅ EXCELLENT - High probability trade"
        confidence = "VERY HIGH"
        recommendation = "BUY YES @ <92¢"
    elif win_probability >= 80:
        assessment = "✅ GOOD - Favorable setup"
        confidence = "HIGH"
        recommendation = "BUY YES @ <90¢"
    elif win_probability >= 70:
        assessment = "⚠️  MODERATE - Acceptable risk"
        confidence = "MEDIUM"
        recommendation = "BUY YES @ <85¢"
    else:
        assessment = "❌ POOR - High risk"
        confidence = "LOW"
        recommendation = "AVOID or reduce size"
    
    print(assessment)
    print(f"Confidence: {confidence}")
    print("")
    
    print("🔧 EXECUTION PLAN:")
    print("-" * 60)
    print(f"1. Market: WTI March 13 Close >${strike_price:.2f}")
    print(f"2. Position: BUY YES")
    print(f"3. Amount: ${investment:.2f}")
    print(f"4. Limit Price: {recommendation.split('@ ')[1] if '@' in recommendation else 'Market'}")
    print(f"5. Expected Win Probability: {win_probability}%")
    print("")
    
    print("📊 RISK MANAGEMENT:")
    print("-" * 60)
    print("• Key Support Levels: $110, $105, $98")
    print(f"• Cushion: ${wti_current - strike_price:.2f} above strike")
    print("• Monitor: Daily war scans for peace developments")
    print("• Exit Consideration: If price breaks below $105")
    print("• Worst Case: Major peace deal + supply surge")
    print("")
    
    # War context advantage
    print("⚔️  WAR CONTEXT ADVANTAGE:")
    print("-" * 60)
    print("✅ YES position benefits from:")
    print("   • War premium supports prices")
    print("   • Geopolitical uncertainty = upward bias")
    print("   • $19 cushion provides margin of safety")
    print("   • Only 5% scenario causes loss (major peace)")
    print("")
    
    # Save analysis
    trade_record = {
        "timestamp": datetime.now().isoformat(),
        "trade": {
            "asset": "WTI Crude",
            "position": "BUY YES",
            "strike": strike_price,
            "current_price": wti_current,
            "cushion": wti_current - strike_price,
            "expiry": "2026-03-13",
            "investment": investment,
            "win_probability": win_probability,
            "recommendation": recommendation,
            "confidence": confidence,
            "expected_value": investment * (win_probability/100 * (potential_return/investment) - (100-win_probability)/100)
        },
        "scenarios": scenarios
    }
    
    os.makedirs("logs/trades", exist_ok=True)
    trade_file = f"logs/trades/wti-yes-trade-{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    
    import json
    with open(trade_file, "w") as f:
        json.dump(trade_record, f, indent=2)
    
    print(f"✅ Analysis saved to: {trade_file}")
    print("=" * 60)
    print(f"🚀 {'GOOD TRADE - EXECUTE' if win_probability >= 80 else 'CAUTIOUS - CONSIDER REDUCING SIZE' if win_probability >= 70 else 'RECONSIDER - HIGH RISK'}")

if __name__ == "__main__":
    load_env_file()
    analyze_wti_yes_trade()