#!/usr/bin/env python3
"""
EIA Inventory Report Analyzer
Analyzes EIA data impact on gas prices and Kalshi positions
"""

import json
from datetime import datetime
import os

def analyze_eia_impact(eia_data):
    """
    Analyze EIA report impact on gas prices
    eia_data should contain: crude_change, gasoline_change, refinery_util, vs_expectations
    """
    print("======================================================================")
    print("📊 EIA INVENTORY REPORT ANALYSIS")
    print("======================================================================")
    print(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Default data if not provided
    if not eia_data:
        print("⚠️  No EIA data provided. Using template analysis.")
        print()
        print("📋 EXPECTATIONS FOR TODAY'S REPORT:")
        print("   • Crude inventories: Expected -1.5M to -2.5M barrels")
        print("   • Gasoline inventories: Expected -1.0M to -2.0M barrels")
        print("   • Refinery utilization: Expected 85-87%")
        print()
        print("🎯 IMPACT ON GAS PRICES:")
        print("   BULLISH if: Crude draw >2.5M, Gasoline draw >2.0M")
        print("   BEARISH if: Crude build, Gasoline build, Low refinery util")
        return
    
    crude_change = eia_data.get('crude_change', 0)
    gasoline_change = eia_data.get('gasoline_change', 0)
    refinery_util = eia_data.get('refinery_util', 0)
    vs_expectations = eia_data.get('vs_expectations', 'in-line')
    
    print("📈 REPORT DATA:")
    print(f"   • Crude inventories: {crude_change:+,} barrels")
    print(f"   • Gasoline inventories: {gasoline_change:+,} barrels")
    print(f"   • Refinery utilization: {refinery_util}%")
    print(f"   • Vs. expectations: {vs_expectations}")
    print()
    
    # Determine bullish/bearish
    bullish_score = 0
    bearish_score = 0
    
    # Crude analysis
    if crude_change < -2000000:  # Large draw
        print("   ✅ CRUDE: Large draw (BULLISH)")
        bullish_score += 2
    elif crude_change < -1000000:  # Moderate draw
        print("   ⚠️  CRUDE: Moderate draw (slightly bullish)")
        bullish_score += 1
    elif crude_change > 1000000:  # Build
        print("   ❌ CRUDE: Inventory build (BEARISH)")
        bearish_score += 2
    else:
        print("   ➖ CRUDE: Neutral change")
    
    # Gasoline analysis
    if gasoline_change < -1500000:  # Large draw
        print("   ✅ GASOLINE: Large draw (BULLISH for gas prices)")
        bullish_score += 3  # Higher weight for gasoline
    elif gasoline_change < -500000:  # Moderate draw
        print("   ⚠️  GASOLINE: Moderate draw (slightly bullish)")
        bullish_score += 2
    elif gasoline_change > 500000:  # Build
        print("   ❌ GASOLINE: Inventory build (BEARISH for gas prices)")
        bearish_score += 3  # Higher weight for gasoline
    else:
        print("   ➖ GASOLINE: Neutral change")
    
    # Refinery analysis
    if refinery_util > 87:
        print("   ✅ REFINERIES: High utilization (BULLISH - strong demand)")
        bullish_score += 1
    elif refinery_util < 83:
        print("   ❌ REFINERIES: Low utilization (BEARISH - weak demand)")
        bearish_score += 1
    else:
        print("   ➖ REFINERIES: Normal utilization")
    
    print()
    print("🎯 OVERALL ASSESSMENT:")
    
    if bullish_score > bearish_score + 2:
        print("   🟢 STRONGLY BULLISH for gas prices")
        sentiment = "strongly_bullish"
    elif bullish_score > bearish_score:
        print("   🟡 MODERATELY BULLISH for gas prices")
        sentiment = "bullish"
    elif bearish_score > bullish_score + 2:
        print("   🔴 STRONGLY BEARISH for gas prices")
        sentiment = "strongly_bearish"
    elif bearish_score > bullish_score:
        print("   🟠 MODERATELY BEARISH for gas prices")
        sentiment = "bearish"
    else:
        print("   ⚪ NEUTRAL for gas prices")
        sentiment = "neutral"
    
    print(f"   Bullish score: {bullish_score}, Bearish score: {bearish_score}")
    print()
    
    # Impact on Kalshi positions
    print("💰 IMPACT ON KALSHI GAS POSITIONS:")
    print()
    
    gas_positions = [
        {
            "name": "Gas Month (>$3.50)",
            "size": 33,
            "current_price": 3.20,
            "target": 3.50,
            "days_left": 25
        },
        {
            "name": "Gas Week (>$3.310)",
            "size": 50,
            "current_price": 3.20,
            "target": 3.31,
            "days_left": 2
        }
    ]
    
    for position in gas_positions:
        print(f"   {position['name']}:")
        print(f"     • Size: ${position['size']}")
        print(f"     • Current: ${position['current_price']}")
        print(f"     • Target: ${position['target']}")
        print(f"     • Days left: {position['days_left']}")
        
        if sentiment == "strongly_bullish":
            print(f"     🟢 EIA IMPACT: Very positive - increases chance of hitting target")
            print(f"     💡 ACTION: Consider adding to position")
        elif sentiment == "bullish":
            print(f"     🟡 EIA IMPACT: Positive - helpful for position")
            print(f"     💡 ACTION: Hold position, monitor price action")
        elif sentiment == "neutral":
            print(f"     ⚪ EIA IMPACT: Neutral - no major help or harm")
            print(f"     💡 ACTION: Base decision on other factors")
        elif sentiment == "bearish":
            print(f"     🟠 EIA IMPACT: Negative - makes target harder")
            print(f"     💡 ACTION: Consider reducing position")
        elif sentiment == "strongly_bearish":
            print(f"     🔴 EIA IMPACT: Very negative - significantly hurts position")
            print(f"     💡 ACTION: Strongly consider exiting or hedging")
        
        print()
    
    # Trading recommendations
    print("🎯 TRADING RECOMMENDATIONS:")
    print()
    
    if sentiment in ["strongly_bullish", "bullish"]:
        print("   1. ✅ Hold gas positions")
        print("   2. ✅ Consider adding to Gas Month position")
        print("   3. ✅ Monitor Gas Week closely (only 2 days left)")
        print("   4. ✅ Watch for price spike in next 30-60 minutes")
        print("   5. ✅ Set profit targets if price moves favorably")
    elif sentiment == "neutral":
        print("   1. ⚪ Hold positions but don't add")
        print("   2. ⚪ Focus on other catalysts (Iran news, etc.)")
        print("   3. ⚪ Wait for price reaction before deciding")
        print("   4. ⚪ Consider Gas Week position risk (2 days left)")
    else:  # bearish
        print("   1. 🔴 Consider reducing gas positions")
        print("   2. 🔴 Gas Week at high risk (exit if bearish)")
        print("   3. 🔴 Monitor for price drop in next 30-60 minutes")
        print("   4. 🔴 Set stop losses to protect capital")
        print("   5. 🔴 Consider short opportunities if available")
    
    print()
    print("📱 QUICK ACTIONS:")
    print("   1. Check AAA gas price update")
    print("   2. Monitor Kalshi YES price movements")
    print("   3. Check news headlines for EIA interpretation")
    print("   4. Update gas position tracker with new data")
    print("   5. Make trading decisions within 30 minutes of report")
    
    # Save analysis
    analysis_file = f"/Users/cubiczan/.openclaw/workspace/eia_analysis/eia_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    os.makedirs(os.path.dirname(analysis_file), exist_ok=True)
    
    analysis_data = {
        "timestamp": datetime.now().isoformat(),
        "eia_data": eia_data,
        "sentiment": sentiment,
        "bullish_score": bullish_score,
        "bearish_score": bearish_score,
        "gas_positions": gas_positions,
        "recommendations": sentiment
    }
    
    with open(analysis_file, 'w') as f:
        json.dump(analysis_data, f, indent=2)
    
    print()
    print(f"📄 Analysis saved to: {analysis_file}")
    print("======================================================================")

def main():
    """Main function - can be run manually or via cron"""
    print("EIA Report Analyzer - Gas Price Impact Assessment")
    print("Run this script after EIA report release (11:00 AM EST Wednesdays)")
    print()
    
    # For manual run, prompt for data
    print("Enter EIA data (press Enter to use template):")
    
    try:
        crude = input("Crude inventory change (barrels, e.g., -2500000): ")
        gasoline = input("Gasoline inventory change (barrels, e.g., -1500000): ")
        refinery = input("Refinery utilization (% e.g., 86.5): ")
        vs_exp = input("Vs. expectations (bullish/bearish/in-line): ")
        
        eia_data = {}
        if crude:
            eia_data['crude_change'] = int(crude)
        if gasoline:
            eia_data['gasoline_change'] = int(gasoline)
        if refinery:
            eia_data['refinery_util'] = float(refinery)
        if vs_exp:
            eia_data['vs_expectations'] = vs_exp
        
        analyze_eia_impact(eia_data)
        
    except (ValueError, KeyboardInterrupt):
        print("\n⚠️  Using template analysis")
        analyze_eia_impact({})

if __name__ == "__main__":
    main()