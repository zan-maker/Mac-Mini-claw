#!/usr/bin/env python3
"""
Auto-generated Evolution Script for TEST-AGENT
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from complete_agent import SkillEvolutionAgent

def main():
    print("="*60)
    print(f"EVOLUTION: TEST-AGENT")
    print("="*60)
    
    agent = SkillEvolutionAgent(
        agent_id="test-agent",
        skill_dir="/private/tmp/test-agent"
    )
    
    # Evolve all skills found in execution history
    report = agent.get_evolution_report()
    
    evolved_count = 0
    if report['top_skills']:
        for skill_data in report['top_skills'][:5]:  # Top 5 skills
            skill = skill_data['skill']
            print(f"\nEvolving: {skill}")
            evolved = agent.evolve_skill(skill)
            if evolved:
                print(f"  ✅ Evolved")
                evolved_count += 1
            else:
                print(f"  ⚠️ No patterns found")
    else:
        print("\n⚠️ No skills found to evolve. Track some executions first.")
    
    print(f"\n📊 Report:")
    print(f"   Executions: {report['total_executions']}")
    print(f"   Success Rate: {report['success_rate']:.1%}")
    print(f"   Patterns: {report['patterns_extracted']}")
    print(f"   Evolved Today: {evolved_count}")
    
    print(f"\n✅ Evolution complete.")
    return evolved_count > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
