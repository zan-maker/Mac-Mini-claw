#!/usr/bin/env python3
"""
Position Monitoring Script for Kalshi Trading
Tracks positions nearing settlement and alerts on at-risk positions
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

# Position data (from MEMORY.md)
POSITIONS = [
    {
        "name": "Copper Position 1",
        "market": "Copper Mar 2025",
        "target": "$5.69-5.74",
        "current": 5.84,
        "invested": 25,
        "max_return": 335,
        "multiplier": 13.4,
        "settlement": "2025-03-31",
        "status": "profitable",
        "margin": 0.10,  # $0.10 above target
        "margin_pct": 2.72
    },
    {
        "name": "Copper Position 2",
        "market": "Copper Mar 2025",
        "target": "$5.63-5.68",
        "current": 5.84,
        "invested": 25,
        "max_return": 213.75,
        "multiplier": 8.55,
        "settlement": "2025-03-31",
        "status": "profitable",
        "margin": 0.16,  # $0.16 above target
        "margin_pct": 3.81
    },
    {
        "name": "Silver Position 1",
        "market": "Silver Weekly",
        "target": "Above $84.49",
        "current": 84.46,
        "invested": 25,
        "max_return": 44,
        "multiplier": 1.76,
        "settlement": "2026-03-13",
        "status": "at_risk",
        "margin": -0.03,  # $0.03 below target
        "margin_pct": -0.04
    },
    {
        "name": "Silver Position 2",
        "market": "Silver Weekly",
        "target": "Above $85.49",
        "current": 84.46,
        "invested": 25,
        "max_return": 47.50,
        "multiplier": 1.9,
        "settlement": "2026-03-13",
        "status": "at_risk",
        "margin": -1.03,  # $1.03 below target
        "margin_pct": -1.22
    },
    {
        "name": "Gold Position",
        "market": "Gold Weekly",
        "target": "Above $5,159",
        "current": 5172,
        "invested": 50,
        "max_return": None,  # TBD
        "multiplier": None,
        "settlement": "2026-03-13",
        "status": "profitable",
        "margin": 13,  # $13 above target
        "margin_pct": 0.25
    }
]

def calculate_days_to_settlement(settlement_date):
    """Calculate days remaining until settlement"""
    settlement = datetime.strptime(settlement_date, "%Y-%m-%d")
    today = datetime.now()
    delta = settlement - today
    return delta.days

def analyze_positions():
    """Analyze all positions and generate report"""
    
    print("=" * 80)
    print("KALSHI POSITION MONITOR - " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("=" * 80)
    print()
    
    # Portfolio summary
    total_invested = sum(p["invested"] for p in POSITIONS)
    profitable_invested = sum(p["invested"] for p in POSITIONS if p["status"] == "profitable")
    at_risk_invested = sum(p["invested"] for p in POSITIONS if p["status"] == "at_risk")
    max_potential_return = sum(p["max_return"] for p in POSITIONS if p["max_return"])
    
    print("📊 PORTFOLIO SUMMARY")
    print("-" * 80)
    print(f"Total Invested:        ${total_invested}")
    print(f"Profitable Positions:  ${profitable_invested} ({len([p for p in POSITIONS if p['status'] == 'profitable'])} positions)")
    print(f"At-Risk Positions:     ${at_risk_invested} ({len([p for p in POSITIONS if p['status'] == 'at_risk'])} positions)")
    print(f"Max Potential Return:  ${max_potential_return:.2f}+")
    print()
    
    # Positions by settlement date
    print("📅 POSITIONS BY SETTLEMENT DATE")
    print("-" * 80)
    
    # Group by settlement
    settlements = {}
    for pos in POSITIONS:
        date = pos["settlement"]
        if date not in settlements:
            settlements[date] = []
        settlements[date].append(pos)
    
    for settlement_date in sorted(settlements.keys()):
        days = calculate_days_to_settlement(settlement_date)
        positions = settlements[settlement_date]
        
        urgency = "🔴 URGENT" if days <= 3 else "🟡 SOON" if days <= 7 else "🟢 OK"
        print(f"\n{settlement_date} ({days} days) {urgency}")
        
        for pos in positions:
            status_emoji = "✅" if pos["status"] == "profitable" else "⚠️"
            margin_str = f"+${abs(pos['margin']):.2f}" if pos["margin"] >= 0 else f"-${abs(pos['margin']):.2f}"
            margin_pct_str = f"+{pos['margin_pct']:.2f}%" if pos["margin_pct"] >= 0 else f"{pos['margin_pct']:.2f}%"
            
            print(f"  {status_emoji} {pos['name']}")
            print(f"     Target: {pos['target']} | Current: ${pos['current']:.2f}")
            print(f"     Margin: {margin_str} ({margin_pct_str})")
            print(f"     Invested: ${pos['invested']} | Max Return: ${pos['max_return'] if pos['max_return'] else 'TBD'}")
    
    print()
    print("=" * 80)
    
    # At-risk positions alert
    at_risk = [p for p in POSITIONS if p["status"] == "at_risk"]
    if at_risk:
        print("\n⚠️  AT-RISK POSITIONS - IMMEDIATE ATTENTION")
        print("-" * 80)
        for pos in at_risk:
            days = calculate_days_to_settlement(pos["settlement"])
            movement_needed = abs(pos["margin"])
            movement_pct = abs(pos["margin_pct"])
            
            print(f"\n  {pos['name']} (Settles in {days} days)")
            print(f"  Current:  ${pos['current']:.2f}")
            print(f"  Target:   {pos['target']}")
            print(f"  Gap:      ${movement_needed:.2f} ({movement_pct:.2f}%)")
            print(f"  Risk:     ${pos['invested']} investment")
            
            # Probability assessment
            if movement_pct < 0.5:
                prob = "HIGH (70-80%)"
            elif movement_pct < 1.5:
                prob = "MEDIUM (50-60%)"
            else:
                prob = "LOW (30-40%)"
            
            print(f"  Probability of hitting target: {prob}")
            print(f"  Action: {'Monitor hourly' if days <= 3 else 'Monitor daily'}")
    
    print()
    print("=" * 80)
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS")
    print("-" * 80)
    
    # Check silver positions specifically
    silver_positions = [p for p in POSITIONS if "Silver" in p["name"]]
    if silver_positions:
        days_to_settlement = calculate_days_to_settlement(silver_positions[0]["settlement"])
        
        if days_to_settlement <= 5:
            print("\n  🔴 CRITICAL: Silver positions settle in 5 days")
            print("     - Monitor silver prices every 4-6 hours")
            print("     - Set price alerts at $84.50 and $85.50")
            print("     - Consider partial exit if positions become profitable")
            print("     - Total at risk: $50")
    
    # Check profitable positions
    profitable = [p for p in POSITIONS if p["status"] == "profitable"]
    if profitable:
        print("\n  ✅ PROFITABLE POSITIONS: Maintain current strategy")
        print("     - Copper positions: Hold until closer to settlement")
        print("     - Gold position: Hold, strong margin (+0.25%)")
        print("     - Total profitable: $100 invested")
    
    print()
    print("=" * 80)
    print("\nNext check recommended: " + (datetime.now() + timedelta(hours=6)).strftime("%Y-%m-%d %H:%M"))
    print()

def generate_json_report():
    """Generate JSON report for programmatic use"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_invested": sum(p["invested"] for p in POSITIONS),
            "profitable_count": len([p for p in POSITIONS if p["status"] == "profitable"]),
            "at_risk_count": len([p for p in POSITIONS if p["status"] == "at_risk"]),
            "max_potential_return": sum(p["max_return"] for p in POSITIONS if p["max_return"])
        },
        "positions": []
    }
    
    for pos in POSITIONS:
        days = calculate_days_to_settlement(pos["settlement"])
        pos_report = {
            **pos,
            "days_to_settlement": days,
            "urgency": "urgent" if days <= 3 else "soon" if days <= 7 else "ok"
        }
        report["positions"].append(pos_report)
    
    return report

if __name__ == "__main__":
    # Run analysis
    analyze_positions()
    
    # Optionally save JSON report
    output_dir = Path(__file__).parent / "position_reports"
    output_dir.mkdir(exist_ok=True)
    
    report = generate_json_report()
    output_file = output_dir / f"position_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📁 JSON report saved to: {output_file}")
