#!/usr/bin/env python3
"""
Simple Knowledge Graph for Kalshi Trading
No external dependencies
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

class KalshiKnowledgeGraph:
    """Simple knowledge graph for tracking trading patterns"""
    
    def __init__(self, data_dir="/Users/cubiczan/.openclaw/workspace/knowledge_graph"):
        self.data_dir = data_dir
        self.trades = []
        self.catalysts = []
        self.patterns = []
        self.load()
    
    def add_trade(self, market, size, profit, catalysts=None, notes=""):
        """Add a trade to the knowledge graph"""
        trade = {
            "id": f"trade_{len(self.trades)+1}",
            "market": market,
            "size": size,
            "profit": profit,
            "return_pct": (profit / size * 100) if size > 0 else 0,
            "catalysts": catalysts or [],
            "notes": notes,
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        self.trades.append(trade)
        self.save()
        return trade["id"]
    
    def add_catalyst(self, description, category, impact, affected_markets, direction="neutral"):
        """Add a catalyst event"""
        catalyst = {
            "id": f"catalyst_{len(self.catalysts)+1}",
            "description": description,
            "category": category,
            "impact": impact,
            "affected_markets": affected_markets,
            "direction": direction,
            "timestamp": datetime.now().isoformat()
        }
        
        self.catalysts.append(catalyst)
        self.save()
        return catalyst["id"]
    
    def analyze_patterns(self):
        """Analyze trading patterns"""
        if not self.trades:
            return []
        
        # Group by market type
        market_groups = defaultdict(list)
        for trade in self.trades:
            market_type = self._get_market_type(trade["market"])
            market_groups[market_type].append(trade)
        
        patterns = []
        
        # Analyze success rates by market type
        for market_type, trades in market_groups.items():
            if len(trades) >= 2:  # Need at least 2 trades for pattern
                successful = [t for t in trades if t["profit"] > 0]
                success_rate = len(successful) / len(trades)
                
                if success_rate >= 0.7:
                    patterns.append({
                        "type": "high_success_market",
                        "market_type": market_type,
                        "success_rate": success_rate,
                        "sample_size": len(trades),
                        "description": f"{market_type} markets have {success_rate:.0%} success rate"
                    })
        
        # Analyze catalyst effectiveness
        catalyst_effectiveness = defaultdict(lambda: {"wins": 0, "total": 0})
        
        for trade in self.trades:
            for catalyst_desc in trade.get("catalysts", []):
                key = catalyst_desc
                catalyst_effectiveness[key]["total"] += 1
                if trade["profit"] > 0:
                    catalyst_effectiveness[key]["wins"] += 1
        
        for catalyst, stats in catalyst_effectiveness.items():
            if stats["total"] >= 2:
                win_rate = stats["wins"] / stats["total"]
                if win_rate >= 0.8:
                    patterns.append({
                        "type": "effective_catalyst",
                        "catalyst": catalyst,
                        "win_rate": win_rate,
                        "sample_size": stats["total"],
                        "description": f"Catalyst '{catalyst}' leads to {win_rate:.0%} win rate"
                    })
        
        self.patterns = patterns
        self.save()
        return patterns
    
    def get_recommendations(self, market_name):
        """Get trading recommendations for a market"""
        market_type = self._get_market_type(market_name)
        
        # Find similar historical trades
        similar_trades = [
            t for t in self.trades
            if self._get_market_type(t["market"]) == market_type
        ]
        
        # Find current catalysts
        current_catalysts = [
            c for c in self.catalysts
            if market_type in c["affected_markets"]
            and self._is_recent(c["timestamp"], days=7)
        ]
        
        recommendations = []
        
        # Historical performance
        if similar_trades:
            successful = [t for t in similar_trades if t["profit"] > 0]
            success_rate = len(successful) / len(similar_trades)
            avg_return = sum(t["return_pct"] for t in similar_trades) / len(similar_trades)
            
            if success_rate >= 0.7:
                action = "BUY YES" if "YES" in market_name.upper() else "BUY"
                recommendations.append({
                    "type": "historical_pattern",
                    "action": action,
                    "confidence": min(0.9, success_rate),
                    "reasoning": f"Historical success rate: {success_rate:.0%} (avg return: {avg_return:.0f}%)",
                    "sample_size": len(similar_trades)
                })
        
        # Catalyst-based
        if current_catalysts:
            bullish = [c for c in current_catalysts if c["direction"] in ["bullish", "positive"]]
            bearish = [c for c in current_catalysts if c["direction"] in ["bearish", "negative"]]
            
            if bullish and not bearish:
                recommendations.append({
                    "type": "catalyst_based",
                    "action": "BUY YES",
                    "confidence": 0.7,
                    "reasoning": f"Bullish catalysts: {', '.join([c['description'][:30] for c in bullish])}",
                    "catalyst_count": len(bullish)
                })
            elif bearish and not bullish:
                recommendations.append({
                    "type": "catalyst_based",
                    "action": "BUY NO",
                    "confidence": 0.7,
                    "reasoning": f"Bearish catalysts: {', '.join([c['description'][:30] for c in bearish])}",
                    "catalyst_count": len(bearish)
                })
        
        return recommendations
    
    def _get_market_type(self, market_name):
        """Determine market type from name"""
        if not market_name:
            return "unknown"
        
        market_lower = market_name.lower()
        
        if any(word in market_lower for word in ["gas", "oil", "energy"]):
            return "energy"
        elif any(word in market_lower for word in ["fed", "rate", "inflation", "cpi"]):
            return "economics"
        elif any(word in market_lower for word in ["election", "senate", "congress", "trump", "paxton"]):
            return "politics"
        elif any(word in market_lower for word in ["weather", "temperature"]):
            return "weather"
        
        return "other"
    
    def _is_recent(self, timestamp_str, days=7):
        """Check if timestamp is within days"""
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            cutoff = datetime.now() - timedelta(days=days)
            return timestamp > cutoff
        except:
            return False
    
    def save(self):
        """Save knowledge graph to disk"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        data = {
            "trades": self.trades,
            "catalysts": self.catalysts,
            "patterns": self.patterns,
            "last_updated": datetime.now().isoformat()
        }
        
        with open(os.path.join(self.data_dir, "kalshi_knowledge.json"), "w") as f:
            json.dump(data, f, indent=2, default=str)
    
    def load(self):
        """Load knowledge graph from disk"""
        file_path = os.path.join(self.data_dir, "kalshi_knowledge.json")
        
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                self.trades = data.get("trades", [])
                self.catalysts = data.get("catalysts", [])
                self.patterns = data.get("patterns", [])
                print(f"Loaded knowledge graph: {len(self.trades)} trades, {len(self.catalysts)} catalysts")
            except Exception as e:
                print(f"Could not load knowledge graph: {e}")
                self.trades = []
                self.catalysts = []
                self.patterns = []
        else:
            self.trades = []
            self.catalysts = []
            self.patterns = []
    
    def generate_report(self):
        """Generate a knowledge graph report"""
        report = []
        report.append("# Kalshi Knowledge Graph Report")
        report.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        report.append("")
        
        # Summary
        report.append("## 📊 Summary")
        report.append(f"- Total Trades: {len(self.trades)}")
        report.append(f"- Total Catalysts: {len(self.catalysts)}")
        report.append(f"- Discovered Patterns: {len(self.patterns)}")
        report.append("")
        
        # Successful trades
        successful_trades = [t for t in self.trades if t["profit"] > 0]
        if successful_trades:
            report.append("## 🏆 Successful Trades")
            total_profit = sum(t["profit"] for t in successful_trades)
            avg_return = sum(t["return_pct"] for t in successful_trades) / len(successful_trades)
            
            report.append(f"- Successful Trades: {len(successful_trades)}")
            report.append(f"- Total Profit: ${total_profit:.2f}")
            report.append(f"- Average Return: {avg_return:.0f}%")
            report.append("")
            
            # Top 3 trades
            report.append("### Top Performers")
            top_trades = sorted(successful_trades, key=lambda x: x["return_pct"], reverse=True)[:3]
            for i, trade in enumerate(top_trades, 1):
                report.append(f"{i}. **{trade['market'][:40]}...**")
                report.append(f"   - Profit: ${trade['profit']:.2f}")
                report.append(f"   - Return: {trade['return_pct']:.0f}%")
                report.append(f"   - Date: {trade['date']}")
                if trade.get("catalysts"):
                    report.append(f"   - Catalysts: {', '.join(trade['catalysts'])}")
                report.append("")
        
        # Patterns
        if self.patterns:
            report.append("## 🔍 Discovered Patterns")
            for pattern in self.patterns[:5]:
                report.append(f"### {pattern['type'].replace('_', ' ').title()}")
                report.append(f"{pattern['description']}")
                report.append(f"*Confidence: Based on {pattern.get('sample_size', 0)} samples*")
                report.append("")
        
        # Current catalysts
        recent_catalysts = [c for c in self.catalysts if self._is_recent(c["timestamp"], days=3)]
        if recent_catalysts:
            report.append("## ⚡ Recent Catalysts (Last 3 Days)")
            for catalyst in recent_catalysts:
                report.append(f"### {catalyst['description'][:50]}...")
                report.append(f"- Category: {catalyst['category']}")
                report.append(f"- Impact: {catalyst['impact']}")
                report.append(f"- Direction: {catalyst['direction']}")
                report.append(f"- Affects: {', '.join(catalyst['affected_markets'])}")
                report.append("")
        
        return "\n".join(report)

def main():
    """Test the knowledge graph"""
    kg = KalshiKnowledgeGraph()
    
    print("🧠 Kalshi Knowledge Graph")
    print("=" * 60)
    
    # Add Paxton trade (your 352% winner!)
    kg.add_trade(
        market="Paxton short position",
        size=25,
        profit=88,
        catalysts=["Political uncertainty", "Election volatility"],
        notes="352% return - First major success!"
    )
    
    # Add current gas trades
    kg.add_trade(
        market="Gas prices in the US this month > $3.50",
        size=25,
        profit=0,
        catalysts=["Iran conflict", "Geopolitical risk"],
        notes="Active trade - settlement Mar 31"
    )
    
    kg.add_trade(
        market="US gas prices this week > $3.310",
        size=50,
        profit=0,
        catalysts=["Iran conflict", "Price already above target"],
        notes="Active trade - settlement Mar 8"
    )
    
    # Add current catalysts
    kg.add_catalyst(
        description="Iran drone strikes on Amazon data centers",
        category="geopolitical",
        impact="high",
        affected_markets=["energy"],
        direction="bullish"
    )
    
    kg.add_catalyst(
        description="Fed rate pause odds near 95%",
        category="economics",
        impact="medium",
        affected_markets=["economics"],
        direction="neutral"
    )
    
    # Analyze patterns
    print("🔍 Analyzing trading patterns...")
    patterns = kg.analyze_patterns()
    
    if patterns:
        print(f"Found {len(patterns)} patterns:")
        for pattern in patterns:
            print(f"• {pattern['description']}")
    else:
        print("No patterns found yet (need more data)")
    
    # Get recommendations for current markets
    print("\n🎯 Trading Recommendations:")
    markets_to_analyze = [
        "Gas prices in the US this month > $3.50",
        "Texas Senate matchup? (Talarico vs. Cornyn)",
        "Fed decision in March? (maintain rate)"
    ]
    
    for market in markets_to_analyze:
        print(f"\n{market}:")
        recs = kg.get_recommendations(market)
        if recs:
            for rec in recs:
                print(f"  {rec['action']} (confidence: {rec['confidence']:.0%})")
                print(f"    {rec['reasoning']}")
        else:
            print("  No recommendations yet")
    
    # Generate report
    print("\n📋 Generating knowledge graph report...")
    report = kg.generate_report()
    
    report_path = "/Users/cubiczan/.openclaw/workspace/knowledge_graph/report.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, "w") as f:
        f.write(report)
    
    print(f"✅ Report saved to: {report_path}")
    print(f"✅ Knowledge graph updated: {len(kg.trades)} trades, {len(kg.catalysts)} catalysts")

if __name__ == "__main__":
    main()
