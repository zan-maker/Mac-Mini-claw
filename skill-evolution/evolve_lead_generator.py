#!/usr/bin/env python3
"""
Daily Skill Evolution for Lead Generator
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from complete_agent import SkillEvolutionAgent

def main():
    print("="*60)
    print("DAILY SKILL EVOLUTION - LEAD GENERATOR")
    print("="*60)
    
    skill_dir = "/Users/cubiczan/mac-bot/skills/lead-generator"
    
    if not os.path.exists(skill_dir):
        print(f"❌ Skill directory not found: {skill_dir}")
        return False
    
    agent = SkillEvolutionAgent(agent_id="lead-generator", skill_dir=skill_dir)
    
    # Skills to evolve (daily for high-volume skills)
    skills = ["email_outreach", "prospect_research", "lead_qualification"]
    
    evolved_count = 0
    for skill in skills:
        print(f"\nEvolving skill: {skill}")
        evolved_path = agent.evolve_skill(skill)
        if evolved_path:
            print(f"  ✅ Evolved: {os.path.basename(evolved_path)}")
            evolved_count += 1
        else:
            print(f"  ⚠️ No successful patterns found for evolution")
    
    # Generate report
    report = agent.get_evolution_report()
    
    print(f"\n📊 Evolution Report:")
    print(f"   Total outreach campaigns: {report['total_executions']}")
    print(f"   Success rate: {report['success_rate']:.1%}")
    print(f"   Patterns extracted: {report['patterns_extracted']}")
    print(f"   Skills evolved today: {evolved_count}")
    
    if report['top_skills']:
        print(f"\n🏆 Top Performing Skills:")
        for skill in report['top_skills'][:3]:
            print(f"   - {skill['skill']}: {skill['avg_score']:.2f} avg score")
    
    print(f"\n✅ Daily evolution complete. {evolved_count} skills evolved.")
    
    return evolved_count > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)