#!/usr/bin/env python3
"""
Kalshi Knowledge Graph System
Lightweight implementation for tracking trading relationships and patterns
"""

import json
import networkx as nx
from datetime import datetime, timedelta
import pickle
import os
from collections import defaultdict

class KalshiKnowledgeGraph:
    """Knowledge graph for Kalshi trading relationships"""
    
    def __init__(self, data_dir="/Users/cubiczan/.openclaw/workspace/knowledge_graph"):
        self.data_dir = data_dir
        self.graph = nx.DiGraph()
        self.load()
        
        # Initialize with core trading concepts
        self.initialize_core_concepts()
    
    def initialize_core_concepts(self):
        """Initialize with core trading relationships"""
        core_nodes = [
            # Market Types
            ("Gas Prices", {"type": "commodity", "category": "energy"}),
            ("Fed Decisions", {"type": "macro", "category": "economics"}),
            ("Political Markets", {"type": "political", "category": "elections"}),
            ("Weather Markets", {"type": "weather", "category": "environment"}),
            
            # Catalysts
            ("Geopolitical Events", {"type": "catalyst", "category": "risk"}),
            ("Economic Data", {"type": "catalyst", "category": "fundamentals"}),
            ("Election Results", {"type": "catalyst", "category": "political"}),
            ("Weather Events", {"type": "catalyst", "category": "environment"}),
            
            # Relationships
            ("Iran Conflict", {"type": "geopolitical", "category": "risk"}),
            ("OPEC Decisions", {"type": "supply", "category": "energy"}),
            ("Inflation Data", {"type": "economic", "category": "fundamentals"}),
            ("Primary Elections", {"type": "political", "category": "elections"}),
        ]
        
        for node, attrs in core_nodes:
            if node not in self.graph:
                self.graph.add_node(node, **attrs)
        
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
            if not self.graph.has_edge(source, target):
                self.graph.add_edge(source, target, **attrs)
    
    def add_trade(self, trade_data):
        """Add a trade to the knowledge graph"""
        trade_id = f"trade_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Add trade node
        self.graph.add_node(trade_id, **{
            "type": "trade",
            "market": trade_data.get("market"),
            "direction": trade_data.get("direction"),
            "size": trade_data.get("size"),
            "entry": trade_data.get("entry"),
            "exit": trade_data.get("exit"),
            "profit": trade_data.get("profit"),
            "timestamp": datetime.now().isoformat()
        })
        
        # Connect to relevant catalysts
        catalysts = trade_data.get("catalysts", [])
        for catalyst in catalysts:
            if catalyst in self.graph:
                self.graph.add_edge(catalyst, trade_id, {
                    "relationship": "catalyst",
                    "strength": 0.7
                })
        
        # Connect to market type
        market_type = self.get_market_type(trade_data.get("market"))
        if market_type:
            self.graph.add_edge(market_type, trade_id, {
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
        elif any(word in market_lower for word in ["election", "senate", "congress", "trump"]):
            return "Political Markets"
        elif any(word in market_lower for word in ["weather", "temperature", "rain"]):
            return "Weather Markets"
        
        return None
    
    def add_catalyst(self, catalyst_data):
        """Add a catalyst event"""
        catalyst_id = f"catalyst_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.graph.add_node(catalyst_id, **{
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
            if market in self.graph:
                self.graph.add_edge(catalyst_id, market, {
                    "relationship": "affects",
                    "strength": catalyst_data.get("strength", 0.5),
                    "direction": "positive" if catalyst_data.get("direction") == "bullish" else "negative"
                })
        
        self.save()
        return catalyst_id
    
    def find_patterns(self, market_type=None, days_back=30):
        """Find trading patterns"""
        patterns = []
        
        # Get recent trades
        recent_trades = [
            n for n, attrs in self.graph.nodes(data=True)
            if attrs.get("type") == "trade" 
            and self.is_recent(attrs.get("timestamp"), days_back)
        ]
        
        if not recent_trades:
            return patterns
        
        # Analyze success patterns
        successful_trades = []
        failed_trades = []
        
        for trade_id in recent_trades:
            attrs = self.graph.nodes[trade_id]
            profit = attrs.get("profit", 0)
            
            if profit > 0:
                successful_trades.append(trade_id)
            else:
                failed_trades.append(trade_id)
        
        # Find common catalysts in successful trades
        success_catalysts = defaultdict(int)
        for trade_id in successful_trades:
            predecessors = list(self.graph.predecessors(trade_id))
            for pred in predecessors:
                pred_attrs = self.graph.nodes[pred]
                if pred_attrs.get("type") == "catalyst_event":
                    desc = pred_attrs.get("description", "")
                    success_catalysts[desc] += 1
        
        # Find common catalysts in failed trades
        fail_catalysts = defaultdict(int)
        for trade_id in failed_trades:
            predecessors = list(self.graph.predecessors(trade_id))
            for pred in predecessors:
                pred_attrs = self.graph.nodes[pred]
                if pred_attrs.get("type") == "catalyst_event":
                    desc = pred_attrs.get("description", "")
                    fail_catalysts[desc] += 1
        
        # Generate pattern insights
        if success_catalysts:
            top_success = sorted(success_catalysts.items(), key=lambda x: x[1], reverse=True)[:3]
            patterns.append({
                "type": "success_pattern",
                "description": f"Successful trades often follow: {', '.join([c[0] for c in top_success])}",
                "confidence": min(0.9, len(successful_trades) / 10)
            })
        
        if fail_catalysts:
            top_fail = sorted(fail_catalysts.items(), key=lambda x: x[1], reverse=True)[:3]
            patterns.append({
                "type": "failure_pattern",
                "description": f"Failed trades often follow: {', '.join([c[0] for c in top_fail])}",
                "confidence": min(0.9, len(failed_trades) / 10)
            })
        
        return patterns
    
    def predict_impact(self, catalyst_description, market_type):
        """Predict impact of a catalyst on a market"""
        # Find similar historical catalysts
        similar_catalysts = [
            n for n, attrs in self.graph.nodes(data=True)
            if attrs.get("type") == "catalyst_event"
            and any(word in attrs.get("description", "").lower() 
                   for word in catalyst_description.lower().split()[:3])
        ]
        
        if not similar_catalysts:
            return {
                "predicted_impact": "unknown",
                "confidence": 0.3,
                "reasoning": "No similar catalysts in history"
            }
        
        # Analyze historical impacts
        impacts = []
        for cat_id in similar_catalysts:
            # Find connected trades
            successors = list(self.graph.successors(cat_id))
            for succ in successors:
                succ_attrs = self.graph.nodes[succ]
                if succ_attrs.get("type") == "trade":
                    profit = succ_attrs.get("profit", 0)
                    impacts.append(1 if profit > 0 else -1)
        
        if not impacts:
            return {
                "predicted_impact": "unknown",
                "confidence": 0.4,
                "reasoning": "Similar catalysts found but no trade data"
            }
        
        avg_impact = sum(impacts) / len(impacts)
        
        if avg_impact > 0.3:
            prediction = "positive"
        elif avg_impact < -0.3:
            prediction = "negative"
        else:
            prediction = "neutral"
        
        return {
            "predicted_impact": prediction,
            "confidence": min(0.8, abs(avg_impact) * 2),
            "historical_samples": len(impacts),
            "avg_impact": avg_impact,
            "reasoning": f"Based on {len(impacts)} historical trades with similar catalysts"
        }
    
    def get_recommendations(self, market_type=None):
        """Get trading recommendations based on knowledge graph"""
        recommendations = []
        
        # Find current catalysts
        recent_catalysts = [
            n for n, attrs in self.graph.nodes(data=True)
            if attrs.get("type") == "catalyst_event"
            and self.is_recent(attrs.get("timestamp"), 7)  # Last 7 days
        ]
        
        for cat_id in recent_catalysts:
            cat_attrs = self.graph.nodes[cat_id]
            
            # Find affected markets
            successors = list(self.graph.successors(cat_id))
            for market in successors:
                market_attrs = self.graph.nodes[market]
                
                if market_attrs.get("type") in ["commodity", "macro", "political", "weather"]:
                    # Check if we have historical data
                    prediction = self.predict_impact(
                        cat_attrs.get("description", ""),
                        market
                    )
                    
                    if prediction["confidence"] > 0.6:
                        recommendations.append({
                            "market": market,
                            "catalyst": cat_attrs.get("description"),
                            "prediction": prediction["predicted_impact"],
                            "confidence": prediction["confidence"],
                            "reasoning": prediction["reasoning"]
                        })
        
        return recommendations
    
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
        
        # Save as pickle
        with open(os.path.join(self.data_dir, "graph.pkl"), "wb") as f:
            pickle.dump(self.graph, f)
        
        # Save as JSON for readability
        json_data = {
            "nodes": [
                {"id": n, **attrs} for n, attrs in self.graph.nodes(data=True)
            ],
            "edges": [
                {"source": u, "target": v, **attrs} 
                for u, v, attrs in self.graph.edges(data=True)
            ]
        }
        
        with open(os.path.join(self.data_dir, "graph.json"), "w") as f:
            json.dump(json_data, f, indent=2, default=str)
    
    def load(self):
        """Load graph from disk"""
        pkl_path = os.path.join(self.data_dir, "graph.pkl")
        
        if os.path.exists(pkl_path):
            try:
                with open(pkl_path, "rb") as f:
                    self.graph = pickle.load(f)
                print(f"Loaded knowledge graph with {len(self.graph.nodes)} nodes, {len(self.graph.edges)} edges")
            except:
                print("Could not load graph, starting fresh")
                self.graph = nx.DiGraph()
        else:
            self.graph = nx.DiGraph()
    
    def visualize(self, output_path=None):
        """Create a visualization of the graph"""
        try:
            import matplotlib.pyplot as plt
            
            plt.figure(figsize=(12, 8))
            
            # Layout
            pos = nx.spring_layout(self.graph, k=2, iterations=50)
            
            # Node colors by type
            node_colors = []
            for n in self.graph.nodes():
                node_type = self.graph.nodes[n].get("type", "unknown")
                if node_type == "trade":
                    node_colors.append("green")
                elif node_type == "catalyst_event":
                    node_colors.append("orange")
                elif node_type in ["commodity", "macro", "political", "weather"]:
                    node_colors.append("blue")
                else:
                    node_colors.append("gray")
            
            # Draw
            nx.draw_networkx_nodes(self.graph, pos, node_color=node_colors, node_size=300)
            nx.draw_networkx_edges(self.graph, pos, alpha=0.5)
            nx.draw_networkx_labels(self.graph, pos, font_size=8)
            
            plt.title("Kalshi Knowledge Graph")
            plt.axis("off")
            
            if output_path:
                plt.savefig(output_path, dpi=300, bbox_inches="tight")
                print(f"Graph saved to {output_path}")
            else:
                plt.show()
                
        except ImportError:
            print("Matplotlib not installed. Install with: pip install matplotlib")
    
    def stats(self):
        """Get graph statistics"""
        return {
            "total_nodes": len(self.graph.nodes),
            "total_edges": len(self.graph.edges),
            "trade_nodes": len([n for n, attrs in self.graph.nodes(data=True) 
                               if attrs.get("type") == "trade"]),
            "catalyst_nodes": len([n for n, attrs in self.graph.nodes(data=True) 
                                  if attrs.get("type") == "catalyst_event"]),
            "market_nodes": len([n for n, attrs in self.graph.nodes(data=True) 
                                if attrs.get("type") in ["commodity", "macro", "political", "weather"]]),
            "density": nx.density(self.graph),
            "is_connected": nx.is_weakly_connected(self.graph)
        }

def main():
    """Test the knowledge graph"""
    kg = KalshiKnowledgeGraph()
    
    print("📊 Kalshi Knowledge Graph System")
    print("=" * 60)
    
    # Add Paxton trade (your success!)
    paxton_trade = {
        "market": "Paxton short position",
        "direction": "short",
        "size": 25,
        "entry": "low",
        "exit": "high",
        "profit": 88,
        "catalysts": ["Political catalyst", "Election uncertainty"]
    }
    
    trade_id = kg.add_trade(paxton_trade)
    print(f"Added trade: {trade_id}")
    
    # Add current catalysts
    iran_catalyst = {
        "description": "Iran drone strikes on Amazon data centers",
        "category": "geopolitical",
        "impact": "high",
        "affected_markets": ["Gas Prices"],
        "strength": 0.8,
        "direction": "bullish",
        "source": "News API"
    }
    
    catalyst_id = kg.add_catalyst(iran_catalyst)
    print(f"Added catalyst: {catalyst_id}")
    
    # Get stats
    stats = kg.stats()
    print(f"\n📈 Graph Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Get recommendations
    print(f"\n🎯 Trading Recommendations:")
    recs = kg.get_recommendations()
    for i, rec in enumerate(recs[:5], 1):
        print(f"{i}. {rec['market']}")
        print(f"   Catalyst: {rec['catalyst']}")
        print(f"   Prediction: {rec['prediction']} (confidence: {rec['confidence']:.0%})")
        print(f"   Reasoning: {rec['reasoning']}")
        print()
    
    # Find patterns
    print(f"\n🔍 Trading Patterns:")
    patterns = kg.find_patterns(days_back=90)
    for pattern in patterns:
        print(f"• {pattern['description']}")
        print(f"  Confidence: