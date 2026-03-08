#!/usr/bin/env python3
"""
Kalshi Market Research - Find specific markets for identified opportunities
Based on news analysis results
"""

import json
import os
from datetime import datetime

def load_latest_analysis():
    """Load the latest news analysis results"""
    analysis_dir = "/Users/cubiczan/.openclaw/workspace/kalshi_opportunities"
    
    if not os.path.exists(analysis_dir):
        print(f"❌ Analysis directory not found: {analysis_dir}")
        return None
    
    # Find latest analysis file
    analysis_files = [f for f in os.listdir(analysis_dir) if f.startswith("analysis_") and f.endswith(".json")]
    if not analysis_files:
        print("❌ No analysis files found")
        return None
    
    latest_file = max(analysis_files)  # Gets latest by filename
    file_path = os.path.join(analysis_dir, latest_file)
    
    try:
        with open(file_path, 'r') as f:
            analysis = json.load(f)
        print(f"✅ Loaded analysis: {latest_file}")
        return analysis
    except Exception as e:
        print(f"❌ Error loading analysis: {e}")
        return None

def get_kalshi_market_suggestions(category, title):
    """Get specific Kalshi market suggestions based on category and news title"""
    
    suggestions = {
        "ENERGY_COMMODITIES": [
            "Will the average US gas price be above $3.50 on March 31?",
            "Will WTI crude oil close above $80 this week?",
            "Will the EIA report show crude inventory draw this week?",
            "Will OPEC+ announce production cuts at next meeting?",
            "Will natural gas prices rise 5%+ this week?"
        ],
        "POLITICAL": [
            "Will the crypto regulation bill pass Congress this month?",
            "Will Trump's approval rating be above 45% in next poll?",
            "Will the Supreme Court rule on [specific case] by end of month?",
            "Will Congress pass a budget before government shutdown deadline?",
            "Will [specific legislation] pass the House/Senate?"
        ],
        "ECONOMIC": [
            "Will March CPI be above 3% year-over-year?",
            "Will the Fed cut rates at the March meeting?",
            "Will unemployment rate be below 4% in next report?",
            "Will GDP growth be above 2% for Q1?",
            "Will retail sales increase month-over-month?"
        ],
        "WEATHER_CLIMATE": [
            "Will a named hurricane form in Atlantic before June 1?",
            "Will average US temperature be above normal this week?",
            "Will California drought conditions improve this month?",
            "Will there be a major flood event in [region] this month?",
            "Will snowfall be above average in Northeast this week?"
        ],
        "TECH_EARNINGS": [
            "Will Apple beat earnings estimates next quarter?",
            "Will Tesla stock close above $X by end of week?",
            "Will Microsoft announce AI product this month?",
            "Will Amazon revenue grow 10%+ next quarter?",
            "Will Google announce major acquisition this month?"
        ],
        "INTERNATIONAL": [
            "Will [country] elections result in [outcome]?",
            "Will peace talks between [countries] succeed this month?",
            "Will trade sanctions be imposed on [country]?",
            "Will diplomatic relations improve between [countries]?",
            "Will there be a ceasefire in [conflict zone] this week?"
        ]
    }
    
    # Return suggestions for the category, or general if not found
    return suggestions.get(category, [
        f"Will {title[:50]}... result in market movement?",
        f"Will this news impact related markets this week?",
        "Check Kalshi for markets related to this news category"
    ])

def create_execution_plan(analysis):
    """Create detailed execution plan for Kalshi trades"""
    
    if not analysis:
        return None
    
    available_capital = analysis.get("available_capital", 220)
    opportunities = analysis.get("trading_plan", {}).get("opportunities", [])
    
    print("======================================================================")
    print("🎯 KALSHI EXECUTION PLAN - $220 TO DEPLOY")
    print("======================================================================")
    print(f"💰 Available Capital: ${available_capital}")
    print(f"📊 Opportunities: {len(opportunities)}")
    print()
    
    execution_plan = {
        "timestamp": datetime.now().isoformat(),
        "available_capital": available_capital,
        "total_to_deploy": 0,
        "trades": []
    }
    
    print("📋 RECOMMENDED TRADES:")
    print("="*70)
    
    for i, opp in enumerate(opportunities[:5], 1):
        category = opp["category"]
        title = opp["title"]
        allocation = opp["allocation"]
        confidence = opp["confidence"]
        
        # Get specific market suggestions
        market_suggestions = get_kalshi_market_suggestions(category, title)
        
        print(f"\n#{i} - {category} (${allocation})")
        print(f"   📰 News: {title[:80]}...")
        print(f"   🎯 Confidence: {confidence*100:.0f}%")
        print(f"   💰 Allocation: ${allocation}")
        print(f"   📈 Suggested Kalshi Markets:")
        
        for j, market in enumerate(market_suggestions[:3], 1):
            print(f"      {j}. {market}")
        
        # Create trade entry
        trade = {
            "id": f"trade_{i:02d}",
            "category": category,
            "allocation": allocation,
            "confidence": confidence,
            "news_title": title,
            "suggested_markets": market_suggestions[:3],
            "recommended_action": "BUY YES" if confidence >= 0.7 else "MONITOR",
            "timeframe": opp.get("timeframe", "1-2 weeks"),
            "risk_level": "MEDIUM" if confidence >= 0.7 else "HIGH",
            "notes": f"Based on news: {title[:100]}..."
        }
        
        execution_plan["trades"].append(trade)
        execution_plan["total_to_deploy"] += allocation
    
    print("\n" + "="*70)
    print("💰 CAPITAL ALLOCATION SUMMARY:")
    print("="*70)
    
    total_allocated = execution_plan["total_to_deploy"]
    remaining = available_capital - total_allocated
    
    print(f"\nTotal Available: ${available_capital}")
    print(f"Recommended Deployment: ${total_allocated:.2f}")
    print(f"Remaining Reserve: ${remaining:.2f}")
    
    print("\n📊 By Category:")
    category_totals = {}
    for trade in execution_plan["trades"]:
        category = trade["category"]
        category_totals[category] = category_totals.get(category, 0) + trade["allocation"]
    
    for category, total in category_totals.items():
        percentage = (total / available_capital) * 100
        print(f"   • {category}: ${total:.2f} ({percentage:.1f}%)")
    
    print("\n⚡ EXECUTION STEPS:")
    print("="*70)
    
    steps = [
        "1. LOGIN to Kalshi platform",
        "2. SEARCH for suggested markets (use search bar)",
        "3. CHECK current YES/NO prices for each market",
        "4. ANALYZE probability vs. current market price",
        "5. PLACE ORDERS with recommended allocations",
        "6. SET price alerts for major moves",
        "7. DOCUMENT trades in portfolio tracker",
        "8. MONITOR news catalysts daily"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print("\n🎯 SPECIFIC MARKET SEARCH TERMS:")
    print("="*70)
    
    search_terms = []
    for trade in execution_plan["trades"]:
        category = trade["category"]
        if category == "ENERGY_COMMODITIES":
            search_terms.extend(["gas prices", "oil prices", "EIA report", "OPEC"])
        elif category == "POLITICAL":
            search_terms.extend(["Congress", "bill", "election", "Trump", "Supreme Court"])
        elif category == "ECONOMIC":
            search_terms.extend(["Fed", "CPI", "inflation", "jobs report", "GDP"])
    
    unique_terms = list(set(search_terms))
    print("   " + ", ".join(unique_terms[:10]))
    
    print("\n⚠️  RISK MANAGEMENT:")
    print("="*70)
    
    risk_rules = [
        "• Maximum 20% of capital on any single trade",
        "• Maximum 50% of capital in any single category",
        "• Set mental stop-loss at 50% of position",
        "• Take profit at 100% return or better",
        "• Re-evaluate positions if news catalyst changes",
        "• Never risk more than comfortable losing"
    ]
    
    for rule in risk_rules:
        print(f"   {rule}")
    
    print("\n📅 TIMELINE:")
    print("="*70)
    
    timeline = [
        "TODAY: Research and place initial orders",
        "DAILY: Check news catalysts and price movements",
        "WEEKLY: Review all positions every Monday",
        "EOW: Close or adjust expiring positions",
        "MONTHLY: Review performance and adjust strategy"
    ]
    
    for item in timeline:
        print(f"   {item}")
    
    # Save execution plan
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    plan_file = f"/Users/cubiczan/.openclaw/workspace/kalshi_opportunities/execution_plan_{timestamp}.json"
    
    try:
        with open(plan_file, 'w') as f:
            json.dump(execution_plan, f, indent=2)
        print(f"\n📄 Execution plan saved to: {plan_file}")
    except Exception as e:
        print(f"\n⚠️  Could not save execution plan: {e}")
    
    print("\n" + "="*70)
    print("✅ EXECUTION PLAN READY")
    print("="*70)
    print("\n🎯 Next: Login to Kalshi and search for suggested markets")
    print("💰 Goal: Deploy $220 across high-probability opportunities")
    print("📊 Target: 20-50% return on deployed capital")
    
    return execution_plan

def main():
    """Main function"""
    print("Kalshi Market Research - Execution Plan Generator")
    print("Based on latest news analysis")
    print()
    
    # Load latest analysis
    analysis = load_latest_analysis()
    
    if not analysis:
        print("❌ Cannot proceed without analysis data")
        return
    
    # Create execution plan
    execution_plan = create_execution_plan(analysis)
    
    if execution_plan:
        print(f"\n✅ Execution plan created for ${execution_plan['available_capital']}")
        print(f"📊 {len(execution_plan['trades'])} trades recommended")
        print(f"💰 Total to deploy: ${execution_plan['total_to_deploy']:.2f}")

if __name__ == "__main__":
    main()