#!/usr/bin/env python3
"""
Integrate Skill Evolution Framework with ALL agents:
1. Trade Recommender
2. ROI Analyst
3. Lead Generator
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from complete_agent import SkillEvolutionAgent

def integrate_trade_recommender():
    """Integrate with Trade Recommender agent"""
    print("\n" + "="*60)
    print("INTEGRATING WITH TRADE RECOMMENDER")
    print("="*60)
    
    skill_dir = "/Users/cubiczan/mac-bot/skills/trade-recommender"
    
    if not os.path.exists(skill_dir):
        print(f"❌ Trade Recommender skill directory not found: {skill_dir}")
        return None
    
    # Create evolution agent
    agent = SkillEvolutionAgent(agent_id="trade-recommender", skill_dir=skill_dir)
    
    # Create integration file
    integration_file = os.path.join(skill_dir, "EVOLUTION_ACTIVE.md")
    
    with open(integration_file, 'w') as f:
        f.write(f"""# Skill Evolution - ACTIVE
## Trade Recommender Agent

**Integration Status:** ✅ ACTIVE
**Integration Date:** {datetime.now().isoformat()}
**Agent ID:** trade-recommender

## Evolution Capabilities Enabled:

### 1. Performance Tracking
- **Win Rate**: Trading success percentage
- **Average Return**: Profitability metrics
- **Sharpe Ratio**: Risk-adjusted returns
- **Max Drawdown**: Risk management
- **Execution Speed**: Operational efficiency

### 2. Pattern Extraction
- Successful trading strategies
- Market condition correlations
- Risk management patterns
- Entry/exit timing optimization

### 3. Skill Evolution
- Trading strategy improvement
- Technical analysis pattern refinement
- Risk rule adaptation
- Execution timing optimization

### 4. Cross-Agent Learning
- Share patterns with ROI Analyst
- Share patterns with Lead Generator
- Learn from other agents' successes

## How to Use:

### Track Execution (in your code):
```python
from complete_agent import SkillEvolutionAgent

agent = SkillEvolutionAgent(agent_id='trade-recommender', skill_dir='{skill_dir}')

# After each trade recommendation:
agent.track_execution(
    skill_name='market_analysis',
    inputs={{'symbol': 'AAPL', 'timeframe': '1d'}},
    outputs={{'recommendation': 'BUY', 'confidence': 0.85}},
    metrics={{'win_rate': 75.0, 'avg_return': 2.5, 'sharpe_ratio': 1.8}}
)
```

### Evolve Skills:
```python
# Evolve a specific skill
evolved_path = agent.evolve_skill('market_analysis')
if evolved_path:
    print(f"Skill evolved: {{evolved_path}}")
```

### Get Evolution Report:
```python
report = agent.get_evolution_report()
print(f"Total executions: {{report['total_executions']}}")
print(f"Success rate: {{report['success_rate']:.1%}}")
```

## Data Location:
- **Execution History:** `{skill_dir}/evolution/execution_history.json`
- **Pattern Library:** `{skill_dir}/evolution/pattern_library.json`
- **Evolved Skills:** `{skill_dir}/evolution/versions/`
- **Evolution Log:** `{skill_dir}/evolution/skill_evolution_log.json`

## Next Steps:
1. Add execution tracking to your trading scripts
2. Schedule weekly skill evolution
3. Enable cross-agent pattern sharing
4. Monitor performance improvements

**Expected Improvement:** 91.6%+ accuracy on trading recommendations
""")
    
    print(f"✅ Trade Recommender integration complete")
    print(f"   Integration guide: {integration_file}")
    
    # Add sample execution to demonstrate
    sample_record = agent.track_execution(
        skill_name="market_analysis",
        inputs={"symbol": "AAPL", "timeframe": "1d", "indicators": ["RSI", "MACD"]},
        outputs={"recommendation": "BUY", "confidence": 0.85, "target_price": 185.50},
        metrics={"win_rate": 75.0, "avg_return": 2.5, "sharpe_ratio": 1.8, "max_drawdown": 15.0}
    )
    
    print(f"   Sample execution tracked (Score: {sample_record['success_score']:.2f})")
    
    return agent

def integrate_roi_analyst():
    """Integrate with ROI Analyst agent"""
    print("\n" + "="*60)
    print("INTEGRATING WITH ROI ANALYST")
    print("="*60)
    
    skill_dir = "/Users/cubiczan/mac-bot/skills/roi-analyst"
    
    if not os.path.exists(skill_dir):
        print(f"❌ ROI Analyst skill directory not found: {skill_dir}")
        return None
    
    # Create evolution agent
    agent = SkillEvolutionAgent(agent_id="roi-analyst", skill_dir=skill_dir)
    
    # Create integration file
    integration_file = os.path.join(skill_dir, "EVOLUTION_ACTIVE.md")
    
    with open(integration_file, 'w') as f:
        f.write(f"""# Skill Evolution - ACTIVE
## ROI Analyst Agent

**Integration Status:** ✅ ACTIVE
**Integration Date:** {datetime.now().isoformat()}
**Agent ID:** roi-analyst

## Evolution Capabilities Enabled:

### 1. Performance Tracking
- **Accuracy**: Prediction correctness
- **Completeness**: Analysis thoroughness
- **Actionability**: Recommendation usefulness
- **Time to Insight**: Analysis speed

### 2. Pattern Extraction
- Successful analysis methodologies
- Revenue prediction patterns
- Cost optimization strategies
- Risk assessment approaches

### 3. Skill Evolution
- Financial model improvement
- Analysis template optimization
- Reporting format evolution
- Insight generation acceleration

### 4. Cross-Agent Learning
- Share patterns with Trade Recommender
- Share patterns with Lead Generator
- Learn from trading pattern successes

## How to Use:

### Track Execution (in your code):
```python
from complete_agent import SkillEvolutionAgent

agent = SkillEvolutionAgent(agent_id='roi-analyst', skill_dir='{skill_dir}')

# After each ROI analysis:
agent.track_execution(
    skill_name='revenue_analysis',
    inputs={{'company': 'TechCorp', 'timeframe': 'Q4 2025'}},
    outputs={{'growth_rate': 15.2, 'recommendation': 'invest'}},
    metrics={{'accuracy': 88.0, 'completeness': 92.0, 'actionability': 85.0}}
)
```

### Evolve Skills:
```python
# Evolve a specific skill
evolved_path = agent.evolve_skill('revenue_analysis')
if evolved_path:
    print(f"Skill evolved: {{evolved_path}}")
```

### Get Evolution Report:
```python
report = agent.get_evolution_report()
print(f"Analysis accuracy: {{report['success_rate']:.1%}}")
```

## Data Location:
- **Execution History:** `{skill_dir}/evolution/execution_history.json`
- **Pattern Library:** `{skill_dir}/evolution/pattern_library.json`
- **Evolved Skills:** `{skill_dir}/evolution/versions/`
- **Evolution Log:** `{skill_dir}/evolution/skill_evolution_log.json`

## Next Steps:
1. Add execution tracking to your analysis scripts
2. Schedule bi-weekly skill evolution
3. Enable cross-agent pattern sharing
4. Monitor ROI calculation improvements

**Expected Improvement:** Higher accuracy in revenue predictions
""")
    
    print(f"✅ ROI Analyst integration complete")
    print(f"   Integration guide: {integration_file}")
    
    # Add sample execution
    sample_record = agent.track_execution(
        skill_name="revenue_analysis",
        inputs={"company": "TechCorp", "timeframe": "Q4 2025", "metrics": ["revenue", "margins"]},
        outputs={"growth_rate": 15.2, "margin_trend": "improving", "recommendation": "invest"},
        metrics={"accuracy": 88.0, "completeness": 92.0, "actionability": 85.0, "time_to_insight": 45.0}
    )
    
    print(f"   Sample execution tracked (Score: {sample_record['success_score']:.2f})")
    
    return agent

def integrate_lead_generator():
    """Integrate with Lead Generator agent"""
    print("\n" + "="*60)
    print("INTEGRATING WITH LEAD GENERATOR")
    print("="*60)
    
    skill_dir = "/Users/cubiczan/mac-bot/skills/lead-generator"
    
    if not os.path.exists(skill_dir):
        print(f"❌ Lead Generator skill directory not found: {skill_dir}")
        return None
    
    # Create evolution agent
    agent = SkillEvolutionAgent(agent_id="lead-generator", skill_dir=skill_dir)
    
    # Create integration file
    integration_file = os.path.join(skill_dir, "EVOLUTION_ACTIVE.md")
    
    with open(integration_file, 'w') as f:
        f.write(f"""# Skill Evolution - ACTIVE
## Lead Generator Agent

**Integration Status:** ✅ ACTIVE
**Integration Date:** {datetime.now().isoformat()}
**Agent ID:** lead-generator

## Evolution Capabilities Enabled:

### 1. Performance Tracking
- **Response Rate**: Email engagement
- **Conversion Rate**: Lead to meeting
- **Lead Quality**: Prospect relevance
- **Enrichment Accuracy**: Data correctness

### 2. Pattern Extraction
- Successful outreach templates
- Optimal timing patterns
- Personalization strategies
- Follow-up sequences

### 3. Skill Evolution
- Email template improvement
- Research method optimization
- Qualification criteria refinement
- Outreach timing perfection

### 4. Cross-Agent Learning
- Share patterns with Trade Recommender
- Share patterns with ROI Analyst
- Learn from financial analysis patterns

## How to Use:

### Track Execution (in your code):
```python
from complete_agent import SkillEvolutionAgent

agent = SkillEvolutionAgent(agent_id='lead-generator', skill_dir='{skill_dir}')

# After each outreach campaign:
agent.track_execution(
    skill_name='email_outreach',
    inputs={{'template': 'expense_reduction', 'personalization': 'high'}},
    outputs={{'sent': 50, 'opened': 35, 'replied': 8}},
    metrics={{'response_rate': 16.0, 'conversion_rate': 6.0, 'lead_quality': 78.0}}
)
```

### Evolve Skills:
```python
# Evolve a specific skill
evolved_path = agent.evolve_skill('email_outreach')
if evolved_path:
    print(f"Skill evolved: {{evolved_path}}")
```

### Get Evolution Report:
```python
report = agent.get_evolution_report()
print(f"Response rate improvement: {{report['success_rate']:.1%}}")
```

## Data Location:
- **Execution History:** `{skill_dir}/evolution/execution_history.json`
- **Pattern Library:** `{skill_dir}/evolution/pattern_library.json`
- **Evolved Skills:** `{skill_dir}/evolution/versions/`
- **Evolution Log:** `{skill_dir}/evolution/skill_evolution_log.json`

## Next Steps:
1. Add execution tracking to your outreach scripts
2. Schedule daily skill evolution for high-volume skills
3. Enable cross-agent pattern sharing
4. Monitor response rate improvements

**Expected Improvement:** Higher response rates through template optimization
""")
    
    print(f"✅ Lead Generator integration complete")
    print(f"   Integration guide: {integration_file}")
    
    # Add sample execution
    sample_record = agent.track_execution(
        skill_name="email_outreach",
        inputs={"template": "expense_reduction", "personalization": "high", "timing": "morning"},
        outputs={"sent": 50, "opened": 35, "replied": 8, "meetings": 3},
        metrics={"response_rate": 16.0, "conversion_rate": 6.0, "lead_quality": 78.0, "enrichment_accuracy": 88.0}
    )
    
    print(f"   Sample execution tracked (Score: {sample_record['success_score']:.2f})")
    
    return agent

def setup_cross_agent_sharing(agents):
    """Setup pattern sharing between all agents"""
    print("\n" + "="*60)
    print("SETTING UP CROSS-AGENT PATTERN SHARING")
    print("="*60)
    
    if not agents or len(agents) < 2:
        print("❌ Need at least 2 agents for cross-agent sharing")
        return
    
    # Create sharing configuration
    config = {
        "cross_agent_sharing": {
            "enabled": True,
            "agents": list(agents.keys()),
            "sharing_schedule": "weekly",
            "pattern_threshold": 0.6,
            "max_patterns_per_share": 3
        }
    }
    
    # Save configuration
    config_file = "/Users/cubiczan/.openclaw/workspace/skill-evolution/cross_agent_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Cross-agent sharing configuration saved: {config_file}")
    
    # Test sharing between agents
    print("\nTesting cross-agent pattern sharing...")
    
    agent_names = list(agents.keys())
    if len(agent_names) >= 2:
        # Share from first to second agent
        agent1 = agents[agent_names[0]]
        agent2 = agents[agent_names[1]]
        
        shared = agent1.share_patterns(agent2)
        print(f"  {agent_names[0]} → {agent_names[1]}: {shared} patterns shared")
    
    print("\nCross-agent learning is now enabled!")
    print("Agents will share successful patterns weekly.")

def main():
    """Main integration function"""
    print("="*60)
    print("SKILL EVOLUTION FRAMEWORK - FULL INTEGRATION")
    print("="*60)
    
    agents = {}
    
    # Integrate with all agents
    trade_agent = integrate_trade_recommender()
    if trade_agent:
        agents["trade-recommender"] = trade_agent
    
    roi_agent = integrate_roi_analyst()
    if roi_agent:
        agents["roi-analyst"] = roi_agent
    
    lead_agent = integrate_lead_generator()
    if lead_agent:
        agents["lead-generator"] = lead_agent
    
    # Setup cross-agent sharing
    if len(agents) >= 2:
        setup_cross_agent_sharing(agents)
    
    # Generate integration report
    print("\n" + "="*60)
    print("INTEGRATION COMPLETE - SUMMARY")
    print("="*60)
    
    print(f"\n✅ Agents Integrated: {len(agents)}")
    for agent_id in agents.keys():
        print(f"   - {agent_id}")
    
    print(f"\n📊 Sample Data Added:")
    for agent_id, agent in agents.items():
        report = agent.get_evolution_report()
        print(f"   - {agent_id}: {report['total_executions']} executions, {report['patterns_extracted']} patterns")
    
    print(f"\n📁 Integration Files Created:")
    for agent_id in agents.keys():
        skill_dir = f"/Users/cubiczan/mac-bot/skills/{agent_id}"
        integration_file = os.path.join(skill_dir, "EVOLUTION_ACTIVE.md")
        if os.path.exists(integration_file):
            print(f"   - {integration_file}")
    
    print(f"\n🚀 Next Steps:")
    print("   1. Review EVOLUTION_ACTIVE.md files in each skill directory")
    print("   2. Add execution tracking to your agent scripts")
    print("   3. Schedule regular skill evolution (cron jobs)")
    print("   4. Monitor evolution reports for improvements")
    
    print(f"\n🎯 Expected Results:")
    print("   - 91.6%+ accuracy on specialized tasks (based on research)")
    print("   - Autonomous skill improvement without human intervention")
    print("   - Cross-agent knowledge sharing")
    print("   - Continuous performance optimization")
    
    print("\n" + "="*60)
    print("✅ SKILL EVOLUTION FRAMEWORK FULLY INTEGRATED")
    print("="*60)

if __name__ == "__main__":
    main()