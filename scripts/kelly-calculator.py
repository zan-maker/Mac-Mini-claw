#!/usr/bin/env python3
"""
Kelly Criterion Calculator for Prediction Markets
Simple version without external dependencies
"""

import os
import sys
import json
from datetime import datetime
import math

def calculate_ev(p_model, decimal_odds):
    """Expected Value: EV = p · b − (1 − p)"""
    b = decimal_odds - 1
    ev = p_model * b - (1 - p_model)
    return ev

def calculate_edge(p_model, p_market):
    """Market Edge: edge = p_model − p_market"""
    return p_model - p_market

def kelly_criterion(p_model, decimal_odds):
    """Kelly Criterion: f* = (p · b − q) / b"""
    b = decimal_odds - 1
    if b <= 0:
        return 0
    q = 1 - p_model
    f_star = (p_model * b - q) / b
    return max(0, f_star)  # Cannot bet negative

def fractional_kelly(f_star, alpha=0.25):
    """Fractional Kelly: f = α · f*"""
    return alpha * f_star

def calculate_position_size(p_model, decimal_odds, bankroll=1000.0, alpha=0.25):
    """Calculate optimal position size"""
    f_star = kelly_criterion(p_model, decimal_odds)
    f_frac = fractional_kelly(f_star, alpha)
    position = f_frac * bankroll
    return position, f_star, f_frac

def validate_trade(p_model, p_market, decimal_odds, current_exposure=0, bankroll=1000.0):
    """Validate trade against all risk rules"""
    
    # Calculate metrics
    edge = calculate_edge(p_model, p_market)
    ev = calculate_ev(p_model, decimal_odds)
    position, f_star, f_frac = calculate_position_size(p_model, decimal_odds, bankroll)
    
    # Rule 1: Minimum edge (4%)
    rule1 = edge > 0.04
    
    # Rule 2: Positive expected value
    rule2 = ev > 0
    
    # Rule 3: Position size within Kelly
    rule3 = position <= f_star * bankroll
    
    # Rule 4: Exposure limit (10% max)
    new_exposure_pct = (current_exposure + position) / bankroll
    rule4 = new_exposure_pct <= 0.10
    
    # Rule 5: Minimum confidence (55%)
    rule5 = p_model > 0.55
    
    # Rule 6: Maximum single position (5%)
    rule6 = position <= bankroll * 0.05
    
    all_rules = [rule1, rule2, rule3, rule4, rule5, rule6]
    passed = all(all_rules)
    
    return {
        "passed": passed,
        "edge": edge,
        "expected_value": ev,
        "position_size": position,
        "kelly_fraction": f_star,
        "fractional_kelly": f_frac,
        "new_exposure_pct": new_exposure_pct,
        "rules": {
            "min_edge_4pct": rule1,
            "positive_ev": rule2,
            "kelly_size": rule3,
            "exposure_limit_10pct": rule4,
            "min_confidence_55pct": rule5,
            "max_position_5pct": rule6
        }
    }

def main():
    """Main function - analyze a trade opportunity"""
    print("🎯 KELLY CRITERION CALCULATOR")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    # Default parameters (can be overridden with command line args)
    bankroll = 1000.0
    
    # Example trade analysis
    trades = [
        {
            "name": "WTI >$98 (Your Trade)",
            "p_model": 0.95,
            "decimal_odds": 1.33,  # 1.33x multiplier
            "p_market": 1/1.33,  # Market implied probability
            "current_exposure": 0
        },
        {
            "name": "Gasoline >$2.75",
            "p_model": 0.75,
            "decimal_odds": 2.00,
            "p_market": 0.50,
            "current_exposure": 0
        },
        {
            "name": "High Risk Example",
            "p_model": 0.60,
            "decimal_odds": 3.00,
            "p_market": 0.33,
            "current_exposure": 0.05  # 5% current exposure
        }
    ]
    
    print(f"💰 Bankroll: ${bankroll:.2f}")
    print(f"📊 Fractional Kelly Alpha: 0.25 (conservative)")
    print("")
    
    for trade in trades:
        print(f"\n📈 {trade['name']}:")
        print("-" * 40)
        
        print(f"   Model Probability: {trade['p_model']:.1%}")
        print(f"   Market Probability: {trade['p_market']:.1%}")
        print(f"   Decimal Odds: {trade['decimal_odds']:.2f}x")
        print(f"   Current Exposure: {trade['current_exposure']:.1%}")
        
        # Calculate position
        position, f_star, f_frac = calculate_position_size(
            trade['p_model'], trade['decimal_odds'], bankroll
        )
        
        print(f"   Kelly Fraction: {f_star:.1%}")
        print(f"   Fractional Kelly: {f_frac:.1%}")
        print(f"   Position Size: ${position:.2f}")
        
        # Validate trade
        validation = validate_trade(
            trade['p_model'], trade['p_market'], trade['decimal_odds'],
            trade['current_exposure'] * bankroll, bankroll
        )
        
        if validation['passed']:
            print(f"   ✅ TRADE VALID - All rules passed")
        else:
            print(f"   ❌ TRADE INVALID - Failed rules:")
            for rule_name, rule_passed in validation['rules'].items():
                if not rule_passed:
                    print(f"      - {rule_name}")
        
        # Show edge and EV
        edge = calculate_edge(trade['p_model'], trade['p_market'])
        ev = calculate_ev(trade['p_model'], trade['decimal_odds'])
        print(f"   ⚖️  Edge: {edge:.2%}")
        print(f"   💰 Expected Value: {ev:.3f}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 RISK PARAMETERS SUMMARY:")
    print("-" * 60)
    print("• Minimum Edge: 4%")
    print("• Minimum Confidence: 55%")
    print("• Max Single Position: 5% of bankroll")
    print("• Max Total Exposure: 10% of bankroll")
    print("• Fractional Kelly: 25% of full Kelly")
    print("• Bankroll: $1,000.00")
    print("")
    
    print("🎯 RECOMMENDATIONS:")
    print("-" * 60)
    print("1. Only execute VALID trades")
    print("2. Use calculated position sizes")
    print("3. Monitor exposure limits")
    print("4. Track performance metrics")
    print("5. Adjust bankroll as needed")
    
    # Save analysis
    analysis = {
        "timestamp": datetime.now().isoformat(),
        "bankroll": bankroll,
        "trades_analyzed": len(trades),
        "trades": trades
    }
    
    os.makedirs("logs/kelly_calculator", exist_ok=True)
    output_file = f"logs/kelly_calculator/analysis-{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(output_file, "w") as f:
        json.dump(analysis, f, indent=2)
    
    print(f"\n✅ Analysis saved to: {output_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()