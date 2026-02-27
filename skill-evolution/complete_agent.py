#!/usr/bin/env python3
"""
Complete Skill Evolution Agent - Fixed Implementation
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional

class SkillEvolutionAgent:
    """Complete Skill Evolution Agent with all methods fixed."""
    
    def __init__(self, agent_id: str, skill_dir: str):
        self.agent_id = agent_id
        self.skill_dir = skill_dir
        self.evolution_dir = os.path.join(skill_dir, "evolution")
        
        # Create directories
        os.makedirs(self.evolution_dir, exist_ok=True)
        os.makedirs(os.path.join(self.evolution_dir, "patterns"), exist_ok=True)
        os.makedirs(os.path.join(self.evolution_dir, "versions"), exist_ok=True)
        
        # Load data
        self.execution_history = self._load_json("execution_history", [])
        self.pattern_library = self._load_json("pattern_library", [])
        self.skill_evolution_log = self._load_json("skill_evolution_log", [])
        
        # FIXED: Lower threshold for better learning
        self.pattern_threshold = 0.5
    
    def _load_json(self, filename: str, default: Any) -> Any:
        filepath = os.path.join(self.evolution_dir, f"{filename}.json")
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except:
                return default
        return default
    
    def _save_json(self, filename: str, data: Any):
        filepath = os.path.join(self.evolution_dir, f"{filename}.json")
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def track_execution(self, skill_name: str, inputs: Dict, outputs: Dict, 
                       metrics: Dict[str, float]) -> Dict:
        """Track skill execution."""
        # Calculate success score (simplified)
        success_score = sum(metrics.values()) / len(metrics) if metrics else 0.5
        
        record = {
            'timestamp': datetime.now().isoformat(),
            'agent_id': self.agent_id,
            'skill_name': skill_name,
            'inputs': inputs,
            'outputs': outputs,
            'metrics': metrics,
            'success_score': success_score,
            'execution_id': hashlib.md5(
                f"{skill_name}:{json.dumps(inputs, sort_keys=True)}".encode()
            ).hexdigest()[:12]
        }
        
        self.execution_history.append(record)
        self._save_json("execution_history", self.execution_history)
        
        # Extract pattern if successful
        if success_score >= self.pattern_threshold:
            self._extract_pattern(record)
        
        return record
    
    def _extract_pattern(self, record: Dict):
        """Extract pattern from execution."""
        pattern = {
            'pattern_id': f"{hashlib.md5(record['skill_name'].encode()).hexdigest()[:6]}_{hashlib.md5(json.dumps(record['inputs'], sort_keys=True).encode()).hexdigest()[:6]}",
            'agent_id': self.agent_id,
            'skill_name': record['skill_name'],
            'context': {
                'input_types': {k: type(v).__name__ for k, v in record['inputs'].items()},
                'input_count': len(record['inputs'])
            },
            'strategy': {
                'output_type': type(record['outputs']).__name__,
                'output_size': len(record['outputs']) if isinstance(record['outputs'], (dict, list)) else 1
            },
            'success_score': record['success_score'],
            'timestamp': record['timestamp'],
            'frequency': 1,
            'source_agents': [self.agent_id]
        }
        
        # Check for similar patterns
        similar = None
        for p in self.pattern_library:
            if p['skill_name'] == pattern['skill_name']:
                # Simple similarity check
                ctx1 = p['context']['input_types']
                ctx2 = pattern['context']['input_types']
                overlap = len(set(ctx1.values()) & set(ctx2.values()))
                total = len(set(ctx1.values()) | set(ctx2.values()))
                if overlap / max(total, 1) > 0.5:
                    similar = p
                    break
        
        if similar:
            similar['frequency'] += 1
            similar['success_score'] = max(similar['success_score'], pattern['success_score'])
            if self.agent_id not in similar['source_agents']:
                similar['source_agents'].append(self.agent_id)
        else:
            self.pattern_library.append(pattern)
        
        self._save_json("pattern_library", self.pattern_library)
    
    def get_successful_patterns(self, skill_name: Optional[str] = None, 
                               min_score: float = 0.5) -> List[Dict]:
        """Get successful patterns."""
        patterns = self.pattern_library
        
        if skill_name:
            patterns = [p for p in patterns if p['skill_name'] == skill_name]
        
        patterns = [p for p in patterns if p['success_score'] >= min_score]
        patterns.sort(key=lambda x: (x['success_score'], x.get('frequency', 1)), reverse=True)
        
        return patterns
    
    def evolve_skill(self, skill_name: str) -> Optional[str]:
        """Evolve a skill."""
        patterns = self.get_successful_patterns(skill_name, min_score=0.5)
        
        if not patterns:
            return None
        
        # Load skill
        skill_path = os.path.join(self.skill_dir, f"{skill_name}.md")
        if not os.path.exists(skill_path):
            skill_path = os.path.join(self.skill_dir, "SKILL.md")
        
        if not os.path.exists(skill_path):
            return None
        
        with open(skill_path, 'r') as f:
            current_content = f.read()
        
        # Create evolved version
        evolved = f"""# {skill_name} - Evolved Version
# Generated: {datetime.now().isoformat()}
# Based on {len(patterns)} successful patterns

## Evolution Insights
Average pattern score: {sum(p['success_score'] for p in patterns) / len(patterns):.2f}

### Top Patterns:
"""
        
        for p in patterns[:3]:
            evolved += f"- {p['pattern_id']} (Score: {p['success_score']:.2f}, Freq: {p.get('frequency', 1)})\n"
        
        evolved += f"\n---\n\n{current_content}\n\n---\n\n*Evolved using Skill Evolution Framework*"
        
        # Save evolved version
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        version_path = os.path.join(self.evolution_dir, "versions", f"{skill_name}_evolved_{timestamp}.md")
        
        os.makedirs(os.path.dirname(version_path), exist_ok=True)
        with open(version_path, 'w') as f:
            f.write(evolved)
        
        # Log evolution
        evolution_record = {
            'timestamp': datetime.now().isoformat(),
            'skill': skill_name,
            'new_version': version_path,
            'patterns_used': len(patterns),
            'avg_score': sum(p['success_score'] for p in patterns) / len(patterns)
        }
        
        self.skill_evolution_log.append(evolution_record)
        self._save_json("skill_evolution_log", self.skill_evolution_log)
        
        return version_path
    
    # FIXED: Complete share_patterns method
    def share_patterns(self, other_agent: 'SkillEvolutionAgent') -> int:
        """Share patterns with another agent."""
        patterns = self.get_successful_patterns(min_score=0.6)[:3]
        
        if not patterns:
            return 0
        
        # Share patterns
        shared = other_agent.receive_patterns(patterns)
        return shared
    
    # FIXED: Complete receive_patterns method
    def receive_patterns(self, patterns: List[Dict]) -> int:
        """Receive patterns from another agent."""
        added = 0
        
        for pattern in patterns:
            # Check if similar exists
            similar = None
            for p in self.pattern_library:
                if p['skill_name'] == pattern['skill_name']:
                    ctx1 = p['context']['input_types']
                    ctx2 = pattern['context']['input_types']
                    overlap = len(set(ctx1.values()) & set(ctx2.values()))
                    total = len(set(ctx1.values()) | set(ctx2.values()))
                    if overlap / max(total, 1) > 0.5:
                        similar = p
                        break
            
            if not similar:
                # Add new pattern
                self.pattern_library.append(pattern)
                added += 1
            else:
                # Update existing
                similar['frequency'] += 1
                similar['success_score'] = max(similar['success_score'], pattern['success_score'])
                if pattern['agent_id'] not in similar['source_agents']:
                    similar['source_agents'].append(pattern['agent_id'])
        
        if added > 0:
            self._save_json("pattern_library", self.pattern_library)
        
        return added
    
    # FIXED: Add missing get_evolution_report method
    def get_evolution_report(self) -> Dict:
        """Generate evolution progress report."""
        total_executions = len(self.execution_history)
        successful = len([r for r in self.execution_history if r['success_score'] >= 0.5])
        
        # Calculate skill performance
        skill_perf = {}
        for record in self.execution_history:
            skill = record['skill_name']
            if skill not in skill_perf:
                skill_perf[skill] = {'count': 0, 'total_score': 0}
            skill_perf[skill]['count'] += 1
            skill_perf[skill]['total_score'] += record['success_score']
        
        top_skills = []
        for skill, data in skill_perf.items():
            avg = data['total_score'] / data['count']
            top_skills.append({
                'skill': skill,
                'executions': data['count'],
                'avg_score': avg
            })
        
        top_skills.sort(key=lambda x: x['avg_score'], reverse=True)
        
        return {
            'agent_id': self.agent_id,
            'total_executions': total_executions,
            'successful_executions': successful,
            'success_rate': successful / max(total_executions, 1),
            'patterns_extracted': len(self.pattern_library),
            'skills_evolved': len(self.skill_evolution_log),
            'top_skills': top_skills[:3],
            'recent_evolutions': self.skill_evolution_log[-3:] if self.skill_evolution_log else []
        }

# Test the fixed implementation
def test_fixed_implementation():
    """Test the fixed implementation."""
    print("Testing Fixed Skill Evolution Agent...")
    
    # Create test directory
    import tempfile
    test_dir = tempfile.mkdtemp()
    
    # Create a sample skill
    skill_content = "# Test Skill\n\nTest content."
    skill_path = os.path.join(test_dir, "test_skill.md")
    with open(skill_path, 'w') as f:
        f.write(skill_content)
    
    # Create agent
    agent = SkillEvolutionAgent(agent_id="test-agent", skill_dir=test_dir)
    
    # Track executions
    for i in range(3):
        record = agent.track_execution(
            skill_name="test_skill",
            inputs={"param": f"value{i}"},
            outputs={"result": "success"},
            metrics={"accuracy": 70 + i*10, "speed": 5 - i}
        )
        print(f"  Execution {i+1}: Score = {record['success_score']:.2f}")
    
    # Get patterns
    patterns = agent.get_successful_patterns()
    print(f"  Patterns extracted: {len(patterns)}")
    
    # Evolve skill
    evolved_path = agent.evolve_skill("test_skill")
    if evolved_path and os.path.exists(evolved_path):
        print(f"  ✅ Skill evolved: {os.path.basename(evolved_path)}")
    else:
        print(f"  ❌ Skill evolution failed")
    
    # Get report
    report = agent.get_evolution_report()
    print(f"  Report generated: {len(report)} items")
    
    # Test sharing (create second agent)
    agent2 = SkillEvolutionAgent(agent_id="test-agent-2", skill_dir=test_dir)
    shared = agent.share_patterns(agent2)
    print(f"  Patterns shared: {shared}")
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)
    
    return evolved_path is not None and len(patterns) > 0

if __name__ == "__main__":
    success = test_fixed_implementation()
    if success:
        print("\n✅ Fixed implementation test PASSED")
    else:
        print("\n❌ Fixed implementation test FAILED")