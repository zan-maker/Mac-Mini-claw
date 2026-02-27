#!/usr/bin/env python3
"""
Auto-Integrate Skill Evolution Framework for ANY New Agent
Run this when creating a new agent to automatically apply skill evolution.
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from complete_agent import SkillEvolutionAgent

def auto_integrate_agent(agent_id: str, skill_dir: str, agent_type: str = "custom"):
    """
    Automatically apply Skill Evolution Framework to any new agent.
    
    Usage: python3 auto_integrate_new_agent.py <agent_id> <skill_dir> [agent_type]
    
    Example: python3 auto_integrate_new_agent.py data-analyzer /path/to/skills/data-analyzer analytics
    """
    
    print("="*60)
    print(f"AUTO-INTEGRATE SKILL EVOLUTION: {agent_id.upper()}")
    print("="*60)
    
    # Validate
    if not os.path.exists(skill_dir):
        print(f"❌ Creating skill directory: {skill_dir}")
        os.makedirs(skill_dir, exist_ok=True)
    
    skill_file = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_file):
        print(f"⚠️  SKILL.md not found, creating template...")
        with open(skill_file, 'w') as f:
            f.write(f"# {agent_id.replace('-', ' ').title()} Agent\n\n## Description\n\nThis agent uses the Skill Evolution Framework for autonomous improvement.\n")
    
    # Create evolution agent
    agent = SkillEvolutionAgent(agent_id=agent_id, skill_dir=skill_dir)
    
    # Create integration files
    create_integration_files(agent_id, skill_dir, agent_type)
    create_evolution_script(agent_id, skill_dir)
    update_global_registry(agent_id, skill_dir, agent_type)
    
    # Add sample execution
    add_sample_execution(agent, agent_type)
    
    print(f"\n✅ AUTO-INTEGRATION COMPLETE!")
    print(f"   Agent: {agent_id}")
    print(f"   Type: {agent_type}")
    print(f"   Skill Dir: {skill_dir}")
    print(f"\n📁 Files Created:")
    print(f"   - {skill_dir}/EVOLUTION_ACTIVE.md")
    print(f"   - skill-evolution/evolve_{agent_id.replace('-', '_')}.py")
    print(f"   - skill-evolution/agents_registry.json (updated)")
    print(f"\n🚀 Next Steps:")
    print(f"   1. Review {skill_dir}/EVOLUTION_ACTIVE.md")
    print(f"   2. Add execution tracking to your agent code")
    print(f"   3. Schedule evolution via cron (see guide)")
    print(f"   4. Monitor evolution progress")
    
    return True

def create_integration_files(agent_id: str, skill_dir: str, agent_type: str):
    """Create all integration files"""
    
    # EVOLUTION_ACTIVE.md
    guide = f"""# Skill Evolution - AUTO-INTEGRATED
## {agent_id.upper()} Agent

**Status:** ✅ ACTIVE (Auto-integrated)
**Date:** {datetime.now().isoformat()}
**Type:** {agent_type}

## Quick Start:

1. **Add tracking to your agent:**
```python
from complete_agent import SkillEvolutionAgent
agent = SkillEvolutionAgent(agent_id='{agent_id}', skill_dir='{skill_dir}')
agent.track_execution(skill_name='your_skill', inputs={{...}}, outputs={{...}}, metrics={{...}})
```

2. **Schedule evolution (add to crontab):**
```bash
# Daily at 1 AM
0 1 * * * cd /Users/cubiczan/.openclaw/workspace && python3 skill-evolution/evolve_{agent_id.replace('-', '_')}.py >> ~/.openclaw/logs/evolution_{agent_id}.log 2>&1
```

3. **Monitor progress:**
```bash
# Check logs
tail -f ~/.openclaw/logs/evolution_{agent_id}.log

# Get evolution report
cd /Users/cubiczan/.openclaw/workspace && python3 -c "from complete_agent import SkillEvolutionAgent; agent = SkillEvolutionAgent('{agent_id}', '{skill_dir}'); print(agent.get_evolution_report())"
```

## Files Created:
- `evolve_{agent_id.replace('-', '_')}.py` - Evolution script
- `{skill_dir}/evolution/` - Evolution data directory
- `agents_registry.json` - Global agent registry

## Support:
- Framework: `skill-evolution/complete_agent.py`
- Examples: See existing agents (trade-recommender, roi-analyst, lead-generator)
- Documentation: `skill-evolution/README.md`

**Your agent now has autonomous skill evolution capabilities!** 🚀
"""
    
    with open(os.path.join(skill_dir, "EVOLUTION_ACTIVE.md"), 'w') as f:
        f.write(guide)
    
    print(f"✅ Created: {skill_dir}/EVOLUTION_ACTIVE.md")

def create_evolution_script(agent_id: str, skill_dir: str):
    """Create evolution script for this agent"""
    
    script_name = f"evolve_{agent_id.replace('-', '_')}.py"
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    
    script = f"""#!/usr/bin/env python3
\"\"\"
Auto-generated Evolution Script for {agent_id.upper()}
\"\"\"

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from complete_agent import SkillEvolutionAgent

def main():
    print("="*60)
    print(f"EVOLUTION: {agent_id.upper()}")
    print("="*60)
    
    agent = SkillEvolutionAgent(
        agent_id="{agent_id}",
        skill_dir="{skill_dir}"
    )
    
    # Evolve all skills found in execution history
    report = agent.get_evolution_report()
    
    evolved_count = 0
    if report['top_skills']:
        for skill_data in report['top_skills'][:5]:  # Top 5 skills
            skill = skill_data['skill']
            print(f"\\nEvolving: {{skill}}")
            evolved = agent.evolve_skill(skill)
            if evolved:
                print(f"  ✅ Evolved")
                evolved_count += 1
            else:
                print(f"  ⚠️ No patterns found")
    else:
        print("\\n⚠️ No skills found to evolve. Track some executions first.")
    
    print(f"\\n📊 Report:")
    print(f"   Executions: {{report['total_executions']}}")
    print(f"   Success Rate: {{report['success_rate']:.1%}}")
    print(f"   Patterns: {{report['patterns_extracted']}}")
    print(f"   Evolved Today: {{evolved_count}}")
    
    print(f"\\n✅ Evolution complete.")
    return evolved_count > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
"""
    
    with open(script_path, 'w') as f:
        f.write(script)
    
    os.chmod(script_path, 0o755)
    print(f"✅ Created: {script_path}")

def update_global_registry(agent_id: str, skill_dir: str, agent_type: str):
    """Update global agent registry"""
    
    registry_path = "/Users/cubiczan/.openclaw/workspace/skill-evolution/agents_registry.json"
    
    if os.path.exists(registry_path):
        with open(registry_path, 'r') as f:
            registry = json.load(f)
    else:
        registry = {
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "agents": {},
            "evolution_schedule": {
                "trade-recommender": "0 2 * * *",
                "roi-analyst": "0 3 * * 1",
                "lead-generator": "0 4 * * *",
                "default": "0 1 * * *"
            }
        }
    
    # Add agent
    registry["agents"][agent_id] = {
        "skill_dir": skill_dir,
        "type": agent_type,
        "integrated": datetime.now().isoformat(),
        "evolution_script": f"evolve_{agent_id.replace('-', '_')}.py",
        "cron_schedule": registry["evolution_schedule"].get(agent_type, "0 1 * * *"),
        "status": "active"
    }
    
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)
    
    print(f"✅ Updated: {registry_path}")

def add_sample_execution(agent: SkillEvolutionAgent, agent_type: str):
    """Add sample execution to demonstrate"""
    
    # Sample metrics based on agent type
    samples = {
        "trading": {"win_rate": 75.0, "avg_return": 2.5, "sharpe_ratio": 1.8},
        "analytics": {"accuracy": 88.0, "completeness": 92.0, "actionability": 85.0},
        "outreach": {"response_rate": 16.0, "conversion_rate": 6.0, "lead_quality": 78.0},
        "custom": {"success_rate": 80.0, "efficiency": 85.0, "quality": 90.0}
    }
    
    metrics = samples.get(agent_type, samples["custom"])
    
    agent.track_execution(
        skill_name="integration_test",
        inputs={"agent_id": agent.agent_id, "integration_date": datetime.now().isoformat()},
        outputs={"status": "success", "framework": "skill_evolution"},
        metrics=metrics
    )
    
    print(f"✅ Added sample execution (Score: {sum(metrics.values())/len(metrics):.1f})")

def create_quick_integration_script():
    """Create a quick-integration script for future use"""
    
    quick_script = """#!/usr/bin/env python3
"""
    quick_script += '''"""
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
'''
    
    quick_path = "/Users/cubiczan/.openclaw/workspace/quick_integrate.py"
    with open(quick_path, 'w') as f:
        f.write(quick_script)
    
    os.chmod(quick_path, 0o755)
    print(f"\n✅ Created quick integration script: {quick_path}")
    print(f"   Usage: python3 {quick_path} <agent_name> <skill_dir> [agent_type]")

if __name__ == "__main__":
    # If called directly, show usage
    if len(sys.argv) < 3:
        print("Usage: python3 auto_integrate_new_agent.py <agent_id> <skill_dir> [agent_type]")
        print("\nExamples:")
        print("  python3 auto_integrate_new_agent.py data-analyzer /path/to/skills/data-analyzer analytics")
        print("  python3 auto_integrate_new_agent.py content-writer /path/to/skills/content-writer outreach")
        print("  python3 auto_integrate_new_agent.py custom-agent /path/to/skills/custom-agent")
        print("\nAgent types: trading, analytics, outreach, custom (default)")
        sys.exit(1)
    
    agent_id = sys.argv[1]
    skill_dir = os.path.expanduser(sys.argv[2])
    agent_type = sys.argv[3] if len(sys.argv) > 3 else "custom"
    
    success = auto_integrate_agent(agent_id, skill_dir, agent_type)
    
    # Create quick integration script for future use
    create_quick_integration_script()
    
    sys.exit(0 if success else 1)