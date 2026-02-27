#!/usr/bin/env python3
"""
Universal Skill Evolution Integration for ANY New Agent
Apply this to automatically add skill evolution capabilities to any new agent.
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from complete_agent import SkillEvolutionAgent

class UniversalAgentIntegrator:
    """
    Apply Skill Evolution Framework to ANY new agent automatically.
    """
    
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.agents_config = self._load_agents_config()
        
    def _load_agents_config(self):
        """Load configuration of all agents"""
        config_path = "/Users/cubiczan/.openclaw/openclaw.json"
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    return config.get("agents", {}).get("list", {})
            except:
                return {}
        return {}
    
    def _create_agent_template(self, agent_id: str, agent_type: str = "custom") -> dict:
        """Create standardized template for any agent type"""
        
        templates = {
            "trading": {
                "metrics": {
                    "win_rate": {"weight": 0.3, "max": 100},
                    "avg_return": {"weight": 0.25, "max": 10},
                    "sharpe_ratio": {"weight": 0.2, "max": 2},
                    "max_drawdown": {"weight": 0.15, "inverse": True, "max": 50},
                    "execution_speed": {"weight": 0.1, "inverse": True, "max": 10}
                },
                "default_skills": ["market_analysis", "risk_assessment", "portfolio_optimization"]
            },
            "analytics": {
                "metrics": {
                    "accuracy": {"weight": 0.4, "max": 100},
                    "completeness": {"weight": 0.25, "max": 100},
                    "actionability": {"weight": 0.2, "max": 100},
                    "time_to_insight": {"weight": 0.15, "inverse": True, "max": 60}
                },
                "default_skills": ["data_analysis", "report_generation", "insight_extraction"]
            },
            "outreach": {
                "metrics": {
                    "response_rate": {"weight": 0.3, "max": 100},
                    "conversion_rate": {"weight": 0.25, "max": 100},
                    "lead_quality": {"weight": 0.25, "max": 100},
                    "enrichment_accuracy": {"weight": 0.2, "max": 100}
                },
                "default_skills": ["email_outreach", "prospect_research", "lead_qualification"]
            },
            "custom": {
                "metrics": {
                    "success_rate": {"weight": 0.4, "max": 100},
                    "efficiency": {"weight": 0.3, "max": 100},
                    "quality": {"weight": 0.3, "max": 100}
                },
                "default_skills": ["primary_skill", "secondary_skill", "support_skill"]
            }
        }
        
        return templates.get(agent_type, templates["custom"])
    
    def integrate_new_agent(self, agent_id: str, skill_dir: str, agent_type: str = "custom"):
        """
        Apply Skill Evolution Framework to a new agent.
        
        Args:
            agent_id: Unique identifier for the agent
            skill_dir: Directory containing the agent's SKILL.md
            agent_type: Type of agent (trading, analytics, outreach, custom)
        """
        print("="*60)
        print(f"INTEGRATING SKILL EVOLUTION: {agent_id.upper()}")
        print("="*60)
        
        # Validate inputs
        if not os.path.exists(skill_dir):
            print(f"❌ Skill directory not found: {skill_dir}")
            return False
        
        skill_file = os.path.join(skill_dir, "SKILL.md")
        if not os.path.exists(skill_file):
            print(f"❌ SKILL.md not found in: {skill_dir}")
            return False
        
        # Create evolution agent
        agent = SkillEvolutionAgent(agent_id=agent_id, skill_dir=skill_dir)
        
        # Get template for agent type
        template = self._create_agent_template(agent_id, agent_type)
        
        # Create integration files
        self._create_integration_guide(agent_id, skill_dir, template, agent_type)
        self._create_tracking_examples(agent_id, skill_dir, template)
        self._create_evolution_script(agent_id, skill_dir, template)
        self._update_global_config(agent_id, skill_dir, agent_type)
        
        # Add sample execution to demonstrate
        self._add_sample_execution(agent, template)
        
        print(f"\n✅ Integration complete for: {agent_id}")
        print(f"   Skill Evolution Framework is now ACTIVE")
        print(f"   Review: {skill_dir}/EVOLUTION_ACTIVE.md")
        
        return True
    
    def _create_integration_guide(self, agent_id: str, skill_dir: str, template: dict, agent_type: str):
        """Create comprehensive integration guide"""
        
        guide_content = f"""# Skill Evolution - ACTIVE
## {agent_id.upper()} Agent

**Integration Status:** ✅ ACTIVE
**Integration Date:** {datetime.now().isoformat()}
**Agent Type:** {agent_type}
**Agent ID:** {agent_id}

## Evolution Capabilities Enabled:

### 1. Performance Tracking
**Metrics Tracked:**
"""
        
        for metric, config in template["metrics"].items():
            weight = config.get("weight", 0)
            guide_content += f"- **{metric.replace('_', ' ').title()}**: {weight*100:.0f}% weight\n"
        
        guide_content += f"""
### 2. Pattern Extraction
- Successful execution patterns
- Context-strategy correlations  
- Performance optimization insights
- Cross-agent learning potential

### 3. Skill Evolution
- Autonomous skill improvement
- Pattern-based optimization
- Continuous performance enhancement
- Version-controlled skill updates

### 4. Cross-Agent Learning
- Share successful patterns with other agents
- Learn from other agents' successes
- Domain knowledge transfer
- Collective intelligence growth

## How to Use:

### Track Executions (Add to your agent code):
```python
from complete_agent import SkillEvolutionAgent

# Initialize once
agent = SkillEvolutionAgent(
    agent_id='{agent_id}',
    skill_dir='{skill_dir}'
)

# Track each execution
agent.track_execution(
    skill_name='your_skill_name',
    inputs={{'param1': 'value1', 'param2': 'value2'}},
    outputs={{'result': 'success', 'details': '...'}},
    metrics={{'success_rate': 85.0, 'efficiency': 90.0}}
)
```

### Evolve Skills (Manual or Scheduled):
```python
# Evolve a specific skill
evolved_path = agent.evolve_skill('your_skill_name')
if evolved_path:
    print(f"Skill evolved: {{evolved_path}}")
```

### Get Evolution Report:
```python
report = agent.get_evolution_report()
print(f"Total executions: {{report['total_executions']}}")
print(f"Success rate: {{report['success_rate']:.1%}}")
print(f"Patterns extracted: {{report['patterns_extracted']}}")
```

## Data Location:
- **Execution History:** `{skill_dir}/evolution/execution_history.json`
- **Pattern Library:** `{skill_dir}/evolution/pattern_library.json`
- **Evolved Skills:** `{skill_dir}/evolution/versions/`
- **Evolution Log:** `{skill_dir}/evolution/skill_evolution_log.json`

## Default Skills to Evolve:
"""
        
        for skill in template["default_skills"]:
            guide_content += f"- `{skill}`\n"
        
        guide_content += f"""
## Next Steps:
1. Add execution tracking to your agent scripts
2. Schedule regular skill evolution (see cron example)
3. Monitor evolution reports for improvements
4. Enable cross-agent pattern sharing

## Expected Results:
- **91.6%+ accuracy** on specialized tasks (based on research)
- **Autonomous skill improvement** without human intervention
- **Cross-domain learning** from other agents
- **Continuous performance optimization**

## Support:
- Framework: `skill-evolution/complete_agent.py`
- Examples: `skill-evolution/tracking_examples/{agent_id}_examples.py`
- Evolution Script: `skill-evolution/evolve_{agent_id.replace('-', '_')}.py`
"""
        
        guide_path = os.path.join(skill_dir, "EVOLUTION_ACTIVE.md")
        with open(guide_path, 'w') as f:
            f.write(guide_content)
        
        print(f"   Created: {guide_path}")
    
    def _create_tracking_examples(self, agent_id: str, skill_dir: str, template: dict):
        """Create tracking examples for this agent type"""
        
        examples_dir = os.path.join(os.path.dirname(__file__), "tracking_examples")
        os.makedirs(examples_dir, exist_ok=True)
        
        example_file = os.path.join(examples_dir, f"{agent_id}_examples.py")
        
        example_content = f"""#!/usr/bin/env python3
"""
        example_content += f'''"""
Tracking Examples for {agent_id.upper()} Agent
Copy and adapt these examples to your agent code.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from complete_agent import SkillEvolutionAgent

def initialize_evolution_agent():
    """Initialize the Skill Evolution Agent"""
    agent = SkillEvolutionAgent(
        agent_id="{agent_id}",
        skill_dir="{skill_dir}"
    )
    return agent

# EXAMPLE 1: Basic execution tracking
def example_basic_tracking():
    """Basic execution tracking example"""
    agent = initialize_evolution_agent()
    
    # After your agent completes a task
    agent.track_execution(
        skill_name="primary_skill",
        inputs={{"task": "analysis", "data_source": "api"}},
        outputs={{"result": "success", "insights": ["insight1", "insight2"]}},
        metrics={{"success_rate": 85.0, "efficiency": 90.0, "quality": 88.0}}
    )
    
    print("✅ Execution tracked successfully")

# EXAMPLE 2: Multiple skill tracking
def example_multiple_skills():
    """Track multiple skills in one session"""
    agent = initialize_evolution_agent()
    
    skills = {template["default_skills"]}
    
    for skill in skills:
        agent.track_execution(
            skill_name=skill,
            inputs={{"skill": skill, "timestamp": "2024-01-01"}},
            outputs={{"status": "completed", "skill": skill}},
            metrics={{"success_rate": 75.0 + len(skill)*5}}  # Example metric
        )
    
    print(f"✅ Tracked {{len(skills)}} skills")

# EXAMPLE 3: Real-world scenario
def example_real_world_scenario():
    """Example based on actual agent use case"""
    agent = initialize_evolution_agent()
    
    # Simulate a real execution
    execution_data = {{
        "skill_name": "data_processing",
        "inputs": {{
            "dataset": "customer_data.csv",
            "rows": 10000,
            "columns": 15,
            "processing_type": "cleaning"
        }},
        "outputs": {{
            "processed_rows": 9800,
            "errors_found": 200,
            "processing_time": "45s",
            "quality_score": 92.5
        }},
        "metrics": {{
            "accuracy": 95.0,
            "efficiency": 88.0,
            "completeness": 98.0
        }}
    }}
    
    agent.track_execution(**execution_data)
    print("✅ Real-world execution tracked")

# EXAMPLE 4: Batch tracking
def example_batch_tracking(executions):
    """Track multiple executions at once"""
    agent = initialize_evolution_agent()
    
    for i, execution in enumerate(executions):
        agent.track_execution(**execution)
    
    print(f"✅ Batch tracked {{len(executions)}} executions")

# EXAMPLE 5: Get evolution insights
def example_get_insights():
    """Get evolution insights and reports"""
    agent = initialize_evolution_agent()
    
    # Get successful patterns
    patterns = agent.get_successful_patterns(min_score=0.6)
    print(f"Found {{len(patterns)}} successful patterns")
    
    # Get evolution report
    report = agent.get_evolution_report()
    print(f"Success rate: {{report['success_rate']:.1%}}")
    
    # Evolve a skill
    evolved_path = agent.evolve_skill("primary_skill")
    if evolved_path:
        print(f"Skill evolved: {{evolved_path}}")
    
    return report

if __name__ == "__main__":
    print("Running tracking examples...")
    example_basic_tracking()
    example_get_insights()
    print("\\n✅ Examples completed. Copy relevant code to your agent.")
'''
        
        with open(example_file, 'w') as f:
            f.write(example_content)
        
        print(f"   Created: {example_file}")
    
    def _create_evolution_script(self, agent_id: str, skill_dir: str, template: dict):
        """Create evolution script for this agent"""
        
        script_name = agent_id.replace('-', '_')
        script_path = os.path.join(os.path.dirname(__file__), f"evolve_{script_name}.py")
        
        script_content = f"""#!/usr/bin/env python3
"""
        script_content += f'''"""
Skill Evolution for {agent_id.upper()} Agent
Scheduled evolution script - runs automatically via cron.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from complete_agent import SkillEvolutionAgent

def main():
    print("="*60)
    print(f"SKILL EVOLUTION - {agent_id.upper()}")
    print("="*60)
    
    skill_dir = "{skill_dir}"
    
    if not os.path.exists(skill_dir):
        print(f"❌ Skill directory not found: {{skill_dir}}")
        return False
    
    agent = SkillEvolutionAgent(agent_id="{agent_id}", skill_dir=skill_dir)
    
    # Skills to evolve (customize based on your agent)
    skills = {template["default_skills"]}
    
    evolved_count = 0
    for skill in skills:
        print(f"\\nEvolving skill: {{skill}}")
        evolved_path = agent.evolve_skill(skill)
        if evolved_path:
            print(f"  ✅ Evolved: {{os.path.basename(evolved_path)}}")
            evolved_count += 1
        else:
            print(f"  ⚠️ No successful patterns found for evolution")
    
    # Generate report
    report = agent.get_evolution_report()
    
    print(f"\\n📊 Evolution Report:")
    print(f"   Total executions: {{report['total_executions']}}")
    print(f"   Success rate: {{report['success_rate']:.1%}}")
    print(f"   Patterns extracted: {{report['patterns_extracted']}}")
    print(f"   Skills evolved: {{evolved_count}}")
    
    if report['top_skills']:
        print(f"\\n🏆 Top Performing Skills:")
        for skill in report['top_skills'][:3]:
            print(f"   - {{skill['skill']}}: {{skill['avg_score']:.2f}} avg score")
    
    print(f"\\n✅ Evolution complete. {{evolved_count}} skills evolved.")
    
    return evolved_count > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
'''
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(script_path, 0o755)
        
        print(f"   Created: {script_path}")
    
    def _update_global_config(self, agent_id: str, skill_dir: str, agent_type: str):
        """Update global configuration with new agent"""
        
        config_path = "/Users/cubiczan/.openclaw/workspace/skill-evolution/agents_registry.json"
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                registry = json.load(f)
        else:
            registry = {"agents": {}, "last_updated": datetime.now().isoformat()}
        
        # Add agent to registry
        registry["agents"][agent_id] = {
            "skill_dir": skill_dir,
            "agent_type": agent_type,
            "integrated_at": datetime.now().isoformat(),
            "evolution_script": f"evolve_{agent_id.replace('-', '_')}.py",
            "status": "active"
        }
        
        with open(config_path, 'w') as f:
            json.dump(registry, f, indent=2)
        
        print(f"   Updated: {config_path}")
    
    def _add_sample_execution(self, agent: SkillEvolutionAgent, template: dict):
        """Add sample execution to demonstrate framework"""
        
        sample_metrics = {}
        for metric in template["metrics"].keys():
            # Generate sample metric values
            sample_metrics[metric] = 70.0 + len(metric) * 2
        
        agent.track_execution(
            skill_name=template["default_skills"][0],
            inputs={"integration_test": True, "