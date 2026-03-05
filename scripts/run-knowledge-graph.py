#!/usr/bin/env python3
"""
Standalone Knowledge Graph Runner
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

class SimpleKnowledgeGraph:
    """Simple knowledge graph using dictionaries"""
    
    def __init__(self, data_dir="/Users/cubiczan/.openclaw/workspace/knowledge_graph"):
        self.data_dir = data_dir
        self.nodes = {}  # node_id -> attributes
        self.edges = defaultdict(list)  # source -> [(target, attributes)]
        self.load()
        
        # Initialize with core concepts
        if not self.nodes:
            self.initialize_core_concepts()
    
    def initialize_core_concepts(self):
        """Initialize with core trading relationships"""
        core_nodes = {
            # Market Types
            "Gas Prices": {"type": "commodity", "category": "energy"},
            "Fed Decisions": {"type": "macro", "category": "economics"},
            "Political Markets": {"type": "political", "category": "elections"},
            "Weather Markets": {"type": "weather", "category": "environment"},
            
            # Catalysts
            "Geopolitical Events": {"type": "catalyst", "category": "risk"},
            "Economic Data": {"type": "catalyst", "category": "fundamentals"},
            "Election Results": {"type": "catalyst", "category": "political"},
            "Weather Events": {"type": "catalyst", "category": "environment"},
            
            # Specific catalysts
            "Iran Conflict": {"type": "geopolitical", "category": "risk"},
            "OPEC Decisions": {"type": "supply", "category": "energy"},
            "Inflation Data": {"type": "economic", "category": "fundamentals"},
            "Primary Elections": {"type": "political", "category": "elections"},
        }
        
        for node_id, attrs in core_nodes.items():
            self.add_node(node_id, **attrs)
        
        # Core relationships
        relationships = [
            # Geopolitical → Gas Prices
            ("Iran Conflict", "Gas Prices", {"strength": 0.8, "lag": "1-3 days"}),
            ("OPEC Decisions", "Gas Prices", {"strength": 0.9, "lag": "immediate"}),
            
            # Economic → Fed Decisions
            ("Inflation Data", "Fed Decisions", {"strength": 0.7, "lag": "2-4 weeks"}),
            
            # Political → Election Markets
            ("Primary Elections", "Political Markets", {"strength": 0.6, "lag": "immediate"}),
            
            # Weather → Weather Markets
            ("Weather Events", "Weather Markets", {"strength": 0.9, "lag": "immediate"}),
            
            # Cross-market relationships
            ("Fed Decisions", "Gas Prices", {"strength": 0.4, "lag": "1-2 weeks"}),
            ("Gas Prices", "Inflation Data", {"strength": 0.5, "lag": "1 month"}),
        ]
        
        for source, target, attrs in relationships:
            self.add_edge(source, target, **attrs)
    
    def add_node(self, node_id, **attrs):
        """Add a node to the graph"""
        if node_id not in self.nodes:
            self.nodes[node_id] = attrs
        else:
            self.nodes[node_id].update(attrs)
    
    def add_edge(self, source, target, **attrs):
        """Add an edge to the graph"""
        self.edges[source].append((target, attrs))
    
    def add_trade(self, trade_data):
        """Add a trade to the knowledge graph"""
        trade_id = f"trade_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Add trade node
        self.add_node(trade_id, **{
            "type": "trade",
            "market": trade_data.get("market"),
            "direction": trade_data.get("direction"),
            "size": trade_data.get("size"),
            "entry": trade_data.get("entry"),
            "exit": trade_data.get("exit"),
            "profit": trade_data.get("profit"),
            "timestamp": datetime.now().isoformat(),
            "return_pct": trade_data.get("return_pct", 0)
        })
        
        # Connect to relevant catalysts
        catalysts = trade_data.get("catalysts", [])
        for catalyst in catalysts:
            if catalyst in self.nodes:
                self.add_edge(catalyst, trade_id, {
                    "relationship": "catalyst",
                    "strength": 0.7
                })
        
        # Connect to market type
        market_type = self.get_market_type(trade_data.get("market"))
        if market_type:
            self.add_edge(market_type, trade_id, {
                "relationship": "market_category",
                "strength": 0.9
            })
        
        self.save()
        return trade_id
    
    def get_market_type(self, market_name):
        """Determine market type from name"""
        if not market_name:
            return None
            
        market_lower = market_name.lower()
        
        if any(word in market_lower for word in ["gas", "oil", "energy"]):
            return "Gas Prices"
        elif any(word in market_lower for word in ["fed", "rate", "inflation", "cpi"]):
            return "Fed Decisions"
        elif any(word in market_lower for word in ["election", "senate", "congress", "trump", "paxton"]):
            return "Political Markets"
        elif any(word in market_lower for word in ["weather", "temperature", "rain"]):
            return "Weather Markets"
        
        return None
    
    def add_catalyst(self, catalyst_data):
        """Add a catalyst event"""
        catalyst_id = f"catalyst_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.add_node(catalyst_id, **{
            "type": "catalyst_event",
            "description": catalyst_data.get("description"),
            "category": catalyst_data.get("category"),
            "impact": catalyst_data.get("impact", "medium"),
            "timestamp": datetime.now().isoformat(),
            "source": catalyst_data.get("source")
        })
        
        # Connect to affected markets
        affected_markets = catalyst_data.get("affected_markets", [])
        for market in affected_markets:
            if market in self.nodes:
                self.add_edge(catalyst_id, market, {
                    "relationship": "affects",
                    "strength": catalyst_data.get("strength", 0.5),
                    "direction": "positive" if catalyst_data.get("direction") == "bullish" else "negative"
                })
        
        self.save()
        return catalyst_id
    
    def find_success_patterns(self, days_back=90):
        """Find patterns in successful trades"""
        patterns = []
        
        # Get recent successful trades
        recent_trades = [
            (node_id, attrs) for node_id, attrs in self.nodes.items()
            if attrs.get("type") == "trade" 
            and attrs.get("profit", 0) > 0
            and self.is_recent(attrs.get("timestamp"), days_back)
        ]
        
        if not recent_trades:
            return patterns
        
        # Analyze catalysts for successful trades
        catalyst_counts = defaultdict(int)
        for trade_id, trade_attrs in recent_trades:
            # Find catalysts connected to this trade
            for source, targets in self.edges.items():
                for target, edge_attrs in targets:
                    if target == trade_id and edge_attrs.get("relationship") == "catalyst":
                        source_attrs = self.nodes.get(source, {})
                        if source_attrs.get("type") == "catalyst_event":
                            desc = source_attrs.get("description", "")
                            catalyst_counts[desc] += 1
        
        if catalyst_counts:
            top_catalysts = sorted(catalyst_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            patterns.append({
                "type": "success_pattern",
                "description": f"Successful trades often follow: {', '.join([c[0] for c in top_catalysts])}",
                "confidence": min(0.9, len(recent_trades) / 10),
                "sample_size": len(recent_trades)
            })
        
        return patterns
    
    def get_market_insights(self, market_name):
        """Get insights for a specific market"""
        market_type = self.get_market_type(market_name)
        if not market_type:
            return {"error": f"Unknown market type for: {market_name}"}
        
        insights = {
            "market": market_name,
            "market_type": market_type,
            "related_catalysts": [],
            "historical_performance": {},
            "recommendations": []
        }
        
        # Find catalysts affecting this market
        for source, targets in self.edges.items():
            source_attrs = self.nodes.get(source, {})
            if source_attrs.get("type") == "catalyst_event":
                for target, edge_attrs in targets:
                    if target == market_type:
                        insights["related_catalysts"].append({
                            "catalyst": source_attrs.get("description"),
                            "strength": edge_attrs.get("strength", 0.5),
                            "direction": edge_attrs.get("direction", "unknown")
                        })
        
        # Find historical trades for this market type
        market_trades = [
            attrs for attrs in self.nodes.values()
            if attrs.get("type") == "trade" 
            and self.get_market_type(attrs.get("market")) == market_type
        ]
        
        if market_trades:
            successful = [t for t in market_trades if t.get("profit", 0) > 0]
            total_profit = sum(t.get("profit", 0) for t in market_trades)
            avg_return = sum(t.get("return_pct", 0) for t in market_trades) / len(market_trades) if market_trades else 0
            
            insights["historical_performance"] = {
                "total_trades": len(market_trades),
                "successful_trades": len(successful),
                "success_rate": len(successful) / len(market_trades) if market_trades else 0,
                "total_profit": total_profit,
                "average_return": avg_return
            }
        
        # Generate recommendations
        if insights["related_catalysts"]:
            current_catalysts = [
                c for c in insights["related_catalysts"]
                if self.is_recent(self.get_catalyst_timestamp(c["catalyst"]), 7)
            ]
            
            if current_catalysts:
                bullish_catalysts = [c for c in current_catalysts if c["direction"] == "positive"]
                bearish_catalysts = [c for c in current_catalysts if c["direction"] == "negative"]
                
                if bullish_catalysts and not bearish_catalysts:
                    insights["recommendations"].append({
                        "action": "BUY YES",
                        "confidence": max(c["strength"] for c in bullish_catalysts),
                        "reasoning": f"Bullish catalysts: {', '.join([c['catalyst'] for c in bullish_catalysts])}"
                    })
                elif bearish_catalysts and not bullish_catalysts:
                    insights["recommendations"].append({
                        "action": "BUY NO",
                        "confidence": max(c["strength"] for c in bearish_catalysts),
                        "reasoning": f"Bearish catalysts: {', '.join([c['catalyst'] for c in bearish_catalysts])}"
                    })
        
        return insights
    
    def get_catalyst_timestamp(self, catalyst_description):
        """Find timestamp for a catalyst by description"""
        for node_id, attrs in self.nodes.items():
            if attrs.get("type") == "catalyst_event" and attrs.get("description") == catalyst_description:
                return attrs.get("timestamp")
        return None
    
    def is_recent(self, timestamp_str, days_back):
        """Check if timestamp is within days_back"""
        if not timestamp_str:
            return False
        
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            cutoff = datetime.now() - timedelta(days=days_back)
            return timestamp > cutoff
        except:
            return False
    
    def save(self):
        """Save graph to disk"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        data = {
            "nodes": self.nodes,
            "edges": {k: v for k, v in self.edges.items()}  # Convert defaultdict
        }
        
        with open(os.path.join(self.data_dir, "simple_graph.json"), "w") as f:
            json.dump(data, f, indent=2, default=str)
    
    def load(self):
        """Load graph from disk"""
        file_path = os.path.join(self.data_dir, "simple_graph.json")
        
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                self.nodes = data.get("nodes", {})
                self.edges = defaultdict(list, data.get("edges", {}))
                print(f"Loaded knowledge graph with {len(self.nodes)} nodes")
            except Exception as e:
                print(f"Could not load graph: {e}")
                self.nodes = {}
                self.edges = defaultdict(list)
        else:
            self.nodes = {}
            self.edges = defaultdict(list)
    
    def stats(self):
        """Get graph statistics"""
        trade_nodes = [n for n, attrs in self.nodes.items() if attrs.get("type") == "trade"]
        catalyst_nodes = [n for n, attrs in self.nodes.items() if attrs.get("type") == "catalyst_event"]
        market_nodes = [n for n, attrs in self.nodes.items() if attrs.get("type") in ["commodity", "macro", "political", "weather"]]
        
        total_edges = sum(len(targets) for targets in self.edges.values())
        
        return {
            "total_nodes": len(self.nodes),
            "total_edges": total_edges,
            "trade_nodes": len(trade_nodes),
            "catalyst_nodes": len(catalyst_nodes),
            "market_nodes": len(market_nodes)
        }

def main():
    """Main function"""
    print("🧠 KALSHI KNOWLEDGE GRAPH SYSTEM")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Initialize knowledge graph
    kg = SimpleKnowledgeGraph()
    
    print("📊 Initializing with current trading data...")
    
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
    gas_trades = [
        {
            "market": "Gas prices in the US this month > $3.50",
            "direction": "YES",
            "size": 25,
            "entry": "<50¢",
            "exit": "pending",
            "profit": 0,
            "catalysts": ["Iran conflict", "Geopolitical risk"]
        },
        {
            "market": "US gas prices this week > $3.310",
            "direction": "YES",
            "size": 50,
            "entry": "<60¢",
            "exit": "pending",
            "profit": 0,
            "catalysts": ["Iran conflict", "Current price already above target"]
        }
    ]
    
    for trade in gas_trades:
        kg.add_trade(trade)
    print("✅ Added current gas trades")
    
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
        }
    ]
    
    for catalyst in current_catalysts:
        kg.add_catalyst(catalyst)
    print("✅ Added current catalysts")
    
    print()
    print("📈 KNOWLEDGE GRAPH ANALYSIS")
    print("=" * 60)
    
    # Stats
    stats = kg.stats()
    print("Graph Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Portfolio analysis
    print("\n🔍 Portfolio Analysis:")
    portfolio_markets = [
        "Gas prices in the US this month > $3.50",
        "US gas prices this week > $3.310"
    ]
    
    for market in portfolio_markets:
        print(f"\nAnalyzing: {market}")
        insights = kg.get_market_insights(market)
        
        if "error" not in insights:
            print(f"  Market Type: {insights['market_type']}")
            
            if insights["historical_performance"]:
                perf = insights["historical_performance"]
                if perf["total_trades"] > 0:
                    print(f"  Historical Success Rate: {perf['success_rate']:.0%}")
                    print(f"  Average Return: {perf['average_return']:.0f}%")
            
            if insights["related_catalysts"]:
                print(f"  Active Catalysts: {len(insights['related_catalysts'])}")
                for cat in insights["related_catalysts"][:2]:
                    print(f"    • {