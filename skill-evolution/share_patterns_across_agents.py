#!/usr/bin/env python3
"""
Weekly Cross-Agent Pattern Sharing
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from complete_agent import SkillEvolutionAgent

def main():
    print("="*60)
    print("WEEKLY CROSS-AGENT PATTERN SHARING")
    print("="*60)
    
    # Load all agents
    agents = {}
    agent_dirs = {
        "trade-recommender": "/Users/cubiczan/mac-bot/skills/trade-recommender",
        "roi-analyst": "/Users/cubiczan/mac-bot/skills/roi-analyst",
        "lead-generator": "/Users/cubiczan/mac-bot/skills/lead-generator"
    }
    
    for agent_id, skill_dir in agent_dirs.items():
        if os.path.exists(skill_dir):
            agents[agent_id] = SkillEvolutionAgent(agent_id=agent_id, skill_dir=skill_dir)
            print(f"✅ Loaded: {agent_id}")
        else:
            print(f"❌ Skipped: {agent_id} (directory not found)")
    
    if len(agents) < 2:
        print("\n❌ Need at least 2 agents for cross-agent sharing")
        return False
    
    total_shared = 0
    
    # Share patterns in a circle: Trade → ROI → Lead → Trade
    print("\nSharing patterns between agents...")
    
    # Trade Recommender → ROI Analyst
    if "trade-recommender" in agents and "roi-analyst" in agents:
        shared = agents["trade-recommender"].share_patterns(agents["roi-analyst"])
        print(f"  Trade → ROI: {shared} patterns shared")
        total_shared += shared
    
    # ROI Analyst → Lead Generator
    if "roi-analyst" in agents and "lead-generator" in agents:
        shared = agents["roi-analyst"].share_patterns(agents["lead-generator"])
        print(f"  ROI → Lead: {shared} patterns shared")
        total_shared += shared
    
    # Lead Generator → Trade Recommender
    if "lead-generator" in agents and "trade-recommender" in agents:
        shared = agents["lead-generator"].share_patterns(agents["trade-recommender"])
        print(f"  Lead → Trade: {shared} patterns shared")
        total_shared += shared
    
    print(f"\n✅ Total patterns shared across agents: {total_shared}")
    
    # Generate sharing report
    print(f"\n📊 Agent Pattern Counts:")
    for agent_id, agent in agents.items():
        patterns = agent.get_successful_patterns(min_score=0.6)
        print(f"  {agent_id}: {len(patterns)} successful patterns")
    
    return total_shared > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)