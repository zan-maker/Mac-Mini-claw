#!/usr/bin/env python3
"""
QUICK INTEGRATION: Apply Skill Evolution to New Agent
Usage: ./quick_integrate.sh <agent_name> <skill_directory> [agent_type]

Example: ./quick_integrate.sh data-miner ~/skills/data-miner analytics
"""

import sys
import os

# Add to PATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "skill-evolution"))

try:
    from auto_integrate_new_agent import auto_integrate_agent
except ImportError:
    print("❌ Cannot import auto_integrate_new_agent.py")
    print("   Make sure you're in the workspace directory:")
    print("   cd /Users/cubiczan/.openclaw/workspace")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 quick_integrate.py <agent_id> <skill_dir> [agent_type]")
        print("Agent types: trading, analytics, outreach, custom (default)")
        sys.exit(1)
    
    agent_id = sys.argv[1]
    skill_dir = os.path.expanduser(sys.argv[2])
    agent_type = sys.argv[3] if len(sys.argv) > 3 else "custom"
    
    success = auto_integrate_agent(agent_id, skill_dir, agent_type)
    sys.exit(0 if success else 1)
