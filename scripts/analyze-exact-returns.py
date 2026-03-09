#!/usr/bin/env python3
"""
WTI Trade Exact Return Analysis - 1.33x Multiplier
"""

import os
from datetime import datetime

def analyze_exact_returns():
    """Calculate exact returns with 1.33x multiplier"""
    print("🛢️  WTI OIL TRADE - EXACT RETURN ANALYSIS")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    # Trade parameters
    investment = 25.00
    multiplier = 1.33
    win_probability = 0.95  # 95%
    
    print("📊 TRADE PARAMETERS:")
    print("-" * 60)
    print(f"• Investment: ${investment:.2f}")
    print(f"• Multiplier if WIN: {multiplier}x")
    print(f"• Win Probability: {win_probability*100:.1f}%")
    print(f"• Loss Probability: {(1-win_probability)*100:.1f}%")
    print("")
    
    # Return calculations
    win_return = investment * multiplier
    profit = win_return - investment
    loss_return = 0.00  # Lose entire investment if wrong
    max_loss = investment
    
    print("💰 RETURN CALCULATIONS:")
    print("-" * 60)
    print(f"• If WIN: ${win_return:.2f} (${profit:.2f} profit)")
    print(f"• If LOSE: ${loss_return:.2f} (${max_loss:.2f} loss)")
    print(f"• Profit Percentage: +{(multiplier-1)*100:.1f}%")
    print(f"• Max Loss Percentage: -100%")
    print("")
    
    # Expected Value
    expected_value = (win_probability * profit) + ((1-win_probability) * (-max_loss))
    roi_per_trade = (expected_value / investment) * 100
    
    print("🎯 EXPECTED VALUE ANALYSIS:")
    print("-" * 60)
    print(f"• Expected Value per Trade: ${expected_value:.2f}")
    print(f"• ROI per Trade: {roi_per_trade:.1f}%")
    print(f"• Risk/Reward Ratio: 1:{profit/max_loss:.2f}")
    print("")
    
    # Comparison to alternatives
    print("📈 COMPARISON TO ALTERNATIVES:")
    print("-" * 60)
    
    alternatives = [
        {"name": "This WTI Trade", "prob": 95, "multiplier": 1.33, "ev": expected_value},
        {"name": "Gasoline >$2.75", "prob": 75, "multiplier": 2.00, "ev": 25*(0.75*1.00 - 0.25)},
        {"name": "S&P 500 Trade", "prob": 60, "multiplier": 2.50, "ev": 25*(0.60*1.50 - 0.40)},
        {"name": "Cash (No Trade)", "prob": 100, "multiplier": 1.00, "ev": 0.00}
    ]
    
    for alt in alternatives:
        ev = alt["ev"] if "ev" in alt else investment * (alt["prob"]/100 * (alt["multiplier"]-1) - (100-alt["prob"])/100)
        print(f"{alt['name']}:")
        print(f"  Probability: {alt['prob']}% | Multiplier: {alt['multiplier']}x")
        print(f"  Expected Value: ${ev:.2f}")
        print("")
    
    # Portfolio impact
    print("📊 PORTFOLIO IMPACT:")
    print("-" * 60)
    portfolio_size = 1000.00  # Example $1000 portfolio
    position_percentage = (investment / portfolio_size) * 100
    
    print(f"• Portfolio Size: ${portfolio_size:.2f}")
    print(f"• Position Size: {position_percentage:.1f}% of portfolio")
    print(f"• Max Portfolio Impact: -{position_percentage:.1f}% if lose")
    print(f"• Expected Portfolio Gain: +{(expected_value/portfolio_size)*100:.2f}%")
    print("")
    
    # Trade assessment
    print("✅ TRADE ASSESSMENT:")
    print("-" * 60)
    
    if expected_value > 0:
        if roi_per_trade > 20:
            assessment = "✅ EXCELLENT - High expected return"
        elif roi_per_trade > 10:
            assessment = "✅ GOOD - Positive expected value"
        elif roi_per_trade > 0:
            assessment = "⚠️  MARGINAL - Slightly positive"
        else:
            assessment = "❌ POOR - Negative expected value"
    else:
        assessment = "❌ AVOID - Negative expected value"
    
    print(assessment)
    print(f"Expected ROI: {roi_per_trade:.1f}%")
    print("")
    
    # Save analysis
    trade_record = {
        "timestamp": datetime.now().isoformat(),
        "trade": {
            "asset": "WTI Crude >$98",
            "position": "BUY YES",
            "investment": investment,
            "multiplier": multiplier,
            "win_probability": win_probability,
            "win_return": win_return,
            "profit": profit,
            "max_loss": max_loss,
            "expected_value": expected_value,
            "roi_per_trade": roi_per_trade,
            "assessment": assessment
        }
    }
    
    os.makedirs("logs/trades", exist_ok=True)
    trade_file = f"logs/trades/wti-exact-returns-{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    
    import json
    with open(trade_file, "w") as f:
        json.dump(trade_record, f, indent=2)
    
    print(f"✅ Analysis saved to: {trade_file}")
    print("=" * 60)
    print("🚀 TRADE EXECUTED - MONITOR DAILY")

if __name__ == "__main__":
    analyze_exact_returns()