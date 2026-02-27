#!/usr/bin/env python3
"""
Weekly Evolution Progress Report
"""

import sys
import os
import json
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from complete_agent import SkillEvolutionAgent

def main():
    print("="*60)
    print("WEEKLY EVOLUTION PROGRESS REPORT")
    print("="*60)
    
    agents = {}
    agent_dirs = {
        "trade-recommender": "/Users/cubiczan/mac-bot/skills/trade-recommender",
        "roi-analyst": "/Users/cubiczan/mac-bot/skills/roi-analyst",
        "lead-generator": "/Users/cubiczan/mac-bot/skills/lead-generator"
    }
    
    for agent_id, skill_dir in agent_dirs.items():
        if os.path.exists(skill_dir):
            agents[agent_id] = SkillEvolutionAgent(agent_id=agent_id, skill_dir=skill_dir)
    
    if not agents:
        print("❌ No agents found")
        return False
    
    weekly_report = {
        "generated_at": datetime.now().isoformat(),
        "agents": {},
        "summary": {}
    }
    
    total_executions = 0
    total_patterns = 0
    total_evolutions = 0
    
    print("\n📊 Agent Performance:")
    for agent_id, agent in agents.items():
        report = agent.get_evolution_report()
        
        weekly_report["agents"][agent_id] = report
        
        total_executions += report['total_executions']
        total_patterns += report['patterns_extracted']
        total_evolutions += report['skills_evolved']
        
        print(f"\n{agent_id.upper()}:")
        print(f"  Executions: {report['total_executions']}")
        print(f"  Success Rate: {report['success_rate']:.1%}")
        print(f"  Patterns: {report['patterns_extracted']}")
        print(f"  Evolutions: {report['skills_evolved']}")
        
        if report['top_skills']:
            print(f"  Top Skills:")
            for skill in report['top_skills'][:2]:
                print(f"    - {skill['skill']}: {skill['avg_score']:.2f} avg score")
    
    weekly_report["summary"] = {
        "total_executions": total_executions,
        "total_patterns": total_patterns,
        "total_evolutions": total_evolutions,
        "avg_success_rate": sum(r['success_rate'] for r in weekly_report["agents"].values()) / len(agents)
    }
    
    # Save report
    report_dir = "/Users/cubiczan/.openclaw/workspace/skill-evolution/weekly_reports"
    os.makedirs(report_dir, exist_ok=True)
    
    report_file = os.path.join(report_dir, f"evolution_report_{datetime.now().strftime('%Y%m%d')}.json")
    
    with open(report_file, 'w') as f:
        json.dump(weekly_report, f, indent=2)
    
    print(f"\n📈 WEEKLY SUMMARY:")
    print(f"   Total Executions: {total_executions}")
    print(f"   Total Patterns: {total_patterns}")
    print(f"   Total Evolutions: {total_evolutions}")
    print(f"   Average Success Rate: {weekly_report['summary']['avg_success_rate']:.1%}")
    
    print(f"\n📁 Report saved: {report_file}")
    print(f"\n✅ Weekly evolution report complete.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)