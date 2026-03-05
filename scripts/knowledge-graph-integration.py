#!/usr/bin/env python3
"""
Knowledge Graph Integration for Kalshi Trading System
"""

import json
from datetime import datetime
from simple_knowledge_graph import SimpleKnowledgeGraph

def initialize_knowledge_graph():
    """Initialize and populate the knowledge graph with current data"""
    kg = SimpleKnowledgeGraph()
    
    print("🧠 Initializing Kalshi Knowledge Graph...")
    print("=" * 60)
    
    # Add Paxton trade (352% winner!)
    paxton_trade = {
        "market": "Paxton short position",
        "direction": "short",
        "size": 25,
        "entry": "low",
        "exit": "high",
        "profit": 88,
        "return_pct": 352,
        "catalysts": ["Political uncertainty", "Election volatility"]
    }
    
    kg.add_trade(paxton_trade)
    print("✅ Added Paxton trade (352% return)")
    
    # Add current gas trades
    gas_month_trade = {
        "market": "Gas prices in the US this month > $3.50",
        "direction": "YES",
        "size": 25,
        "entry": "<50¢",
        "exit": "pending",
        "profit": 0,
        "catalysts": ["Iran conflict", "Geopolitical risk"]
    }
    
    kg.add_trade(gas_month_trade)
    print("✅ Added Gas Month trade")
    
    gas_week_trade = {
        "market": "US gas prices this week > $3.310",
        "direction": "YES",
        "size": 50,
        "entry": "<60¢",
        "exit": "pending",
        "profit": 0,
        "catalysts": ["Iran conflict", "Current price already above target"]
    }
    
    kg.add_trade(gas_week_trade)
    print("✅ Added Gas Week trade")
    
    # Add current catalysts
    current_catalysts = [
        {
            "description": "Iran drone strikes on Amazon data centers",
            "category": "geopolitical",
            "impact": "high",
            "affected_markets": ["Gas Prices"],
            "strength": 0.8,
            "direction": "bullish",
            "source": "News API"
        },
        {
            "description": "Fed rate pause odds near 95%",
            "category": "economic",
            "impact": "medium",
            "affected_markets": ["Fed Decisions"],
            "strength": 0.6,
            "direction": "neutral",
            "source": "Cointelegraph"
        },
        {
            "description": "Texas primary election results",
            "category": "political",
            "impact": "medium",
            "affected_markets": ["Political Markets"],
            "strength": 0.7,
            "direction": "bullish",
            "source": "Local news"
        }
    ]
    
    for catalyst in current_catalysts:
        kg.add_catalyst(catalyst)
    print("✅ Added current catalysts")
    
    return kg

def analyze_portfolio_with_knowledge_graph(kg):
    """Analyze current portfolio using knowledge graph"""
    print("\n📊 Portfolio Analysis with Knowledge Graph")
    print("=" * 60)
    
    # Current portfolio
    portfolio = [
        {"market": "Gas prices in the US this month > $3.50", "size": 25, "type": "gas"},
        {"market": "US gas prices this week > $3.310", "size": 50, "type": "gas"},
    ]
    
    total_investment = sum(trade["size"] for trade in portfolio)
    print(f"Total Investment: ${total_investment}")
    
    # Analyze each trade
    for trade in portfolio:
        print(f"\n🔍 Analyzing: {trade['market']}")
        insights = kg.get_market_insights(trade["market"])
        
        if "error" not in insights:
            print(f"  Market Type: {insights['market_type']}")
            
            if insights["historical_performance"]:
                perf = insights["historical_performance"]
                print(f"  Historical Success Rate: {perf['success_rate']:.0%}")
                print(f"  Average Return: {perf['average_return']:.0f}%")
            
            if insights["related_catalysts"]:
                print(f"  Active Catalysts: {len(insights['related_catalysts'])}")
                for cat in insights["related_catalysts"][:2]:
                    print(f"    • {cat['catalyst']} ({cat['direction']})")
            
            if insights["recommendations"]:
                for rec in insights["recommendations"]:
                    print(f"  Recommendation: {rec['action']} (confidence: {rec['confidence']:.0%})")
                    print(f"    Reasoning: {rec['reasoning']}")
    
    # Find patterns
    print("\n🔍 Trading Patterns Discovered:")
    patterns = kg.find_success_patterns(days_back=90)
    for pattern in patterns:
        print(f"  • {pattern['description']}")
        print(f"    Confidence: {pattern['confidence']:.0%} (based on {pattern['sample_size']} trades)")

def generate_trading_recommendations(kg):
    """Generate new trading recommendations based on knowledge graph"""
    print("\n🎯 Knowledge Graph Trading Recommendations")
    print("=" * 60)
    
    # Markets to analyze
    markets_to_analyze = [
        "Texas Senate matchup? (Talarico vs. Cornyn)",
        "Fed decision in March? (maintain rate)",
        "Gas prices in Texas this year > $3.00",
        "US Strategic Petroleum Reserve level"
    ]
    
    recommendations = []
    
    for market in markets_to_analyze:
        insights = kg.get_market_insights(market)
        
        if "error" not in insights and insights["recommendations"]:
            for rec in insights["recommendations"]:
                recommendations.append({
                    "market": market,
                    "action": rec["action"],
                    "confidence": rec["confidence"],
                    "reasoning": rec["reasoning"],
                    "market_type": insights["market_type"]
                })
    
    # Sort by confidence
    recommendations.sort(key=lambda x: x["confidence"], reverse=True)
    
    if recommendations:
        print(f"Found {len(recommendations)} high-confidence opportunities:\n")
        
        for i, rec in enumerate(recommendations[:5], 1):
            print(f"{i}. {rec['market'][:50]}...")
            print(f"   Action: {rec['action']}")
            print(f"   Confidence: {rec['confidence']:.0%}")
            print(f"   Market Type: {rec['market_type']}")
            print(f"   Reasoning: {rec['reasoning']}")
            print()
    else:
        print("No high-confidence recommendations found.")
        print("Consider waiting for clearer catalysts or market movements.")

def create_knowledge_graph_report(kg):
    """Create a comprehensive knowledge graph report"""
    print("\n📋 Knowledge Graph Report")
    print("=" * 60)
    
    # Stats
    stats = kg.stats()
    print("📊 Graph Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Export to markdown
    report_path = "/Users/cubiczan/.openclaw/workspace/knowledge_graph/report.md"
    kg.export_to_markdown(report_path)
    print(f"\n📄 Report saved to: {report_path}")
    
    # Success rate analysis
    successful_trades = [
        attrs for attrs in kg.nodes.values()
        if attrs.get("type") == "trade" and attrs.get("profit", 0) > 0
    ]
    
    total_trades = [attrs for attrs in kg.nodes.values() if attrs.get("type") == "trade"]
    
    if total_trades:
        success_rate = len(successful_trades) / len(total_trades)
        avg_profit = sum(t.get("profit", 0) for t in successful_trades) / len(successful_trades) if successful_trades else 0
        
        print(f"\n💰 Trading Performance:")
        print(f"  Total Trades: {len(total_trades)}")
        print(f"  Successful Trades: {len(successful_trades)}")
        print(f"  Success Rate: {success_rate:.0%}")
        print(f"  Average Profit per Win: ${avg_profit:.2f}")
        
        if successful_trades:
            best_trade = max(successful_trades, key=lambda x: x.get("profit", 0))
            print(f"  Best Trade: {best_trade.get('market', 'Unknown')}")
            print(f"    Profit: ${best_trade.get('profit', 0):.2f}")
            print(f"    Return: {best_trade.get('return_pct', 0):.0f}%")

def main():
    """Main function"""
    print("🧠 KALSHI KNOWLEDGE GRAPH INTEGRATION")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Initialize knowledge graph
    kg = initialize_knowledge_graph()
    
    # Analyze current portfolio
    analyze_portfolio_with_knowledge_graph(kg)
    
    # Generate recommendations
    generate_trading_recommendations(kg)
    
    # Create report
    create_knowledge_graph_report(kg)
    
    print("\n" + "=" * 60)
    print("✅ Knowledge Graph Integration Complete")
    print()
    print("Next Steps:")
    print("1. Review knowledge graph report")
    print("2. Consider high-confidence recommendations")
    print("3. Add new trades to build graph intelligence")
    print("4. Monitor catalyst developments")
    print()
    print("The knowledge graph will improve with every trade!")
    print("Current intelligence: Basic → Learning from Paxton success")

if __name__ == "__main__":
    # Import the simple knowledge graph
    import sys
    sys.path.insert(0, "/Users/cubiczan/.openclaw/workspace/scripts")
    
    try:
        from simple_knowledge_graph import SimpleKnowledgeGraph
        main()
    except ImportError as e:
        print(f"Error: {e}")
        print("Make sure simple_knowledge_graph.py is in the scripts directory")
