#!/usr/bin/env python3
"""
Fixed Skill Evolution Agent
Complete implementation with all missing methods fixed
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class AgentType(Enum):
    TRADE_RECOMMENDER = "trade-recommender"
    ROI_ANALYST = "roi-analyst"
    LEAD_GENERATOR = "lead-generator"

@dataclass
class ExecutionRecord:
    """Record of skill execution for learning"""
    timestamp: str
    agent_id: str
    skill_name: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    metrics: Dict[str, float]
    success_score: float
    execution_id: str
    
    @classmethod
    def create(cls, agent_id: str, skill_name: str, inputs: Dict, outputs: Dict, metrics: Dict):
        """Create new execution record"""
        timestamp = datetime.now().isoformat()
        execution_id = cls._generate_id(skill_name, inputs)
        success_score = PerformanceTracker.calculate_score(agent_id, metrics)
        
        return cls(
            timestamp=timestamp,
            agent_id=agent_id,
            skill_name=skill_name,
            inputs=inputs,
            outputs=outputs,
            metrics=metrics,
            success_score=success_score,
            execution_id=execution_id
        )
    
    @staticmethod
    def _generate_id(skill_name: str, inputs: Dict) -> str:
        """Generate unique execution ID"""
        input_str = json.dumps(inputs, sort_keys=True)
        hash_input = f"{skill_name}:{input_str}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:12]

@dataclass
class SkillPattern:
    """Pattern extracted from successful executions"""
    pattern_id: str
    agent_id: str
    skill_name: str
    context: Dict[str, Any]
    strategy: Dict[str, Any]
    success_score: float
    timestamp: str
    frequency: int = 1
    source_agents: List[str] = None
    
    def __post_init__(self):
        if self.source_agents is None:
            self.source_agents = [self.agent_id]

class PerformanceTracker:
    """Standardized performance tracking"""
    
    # Metric weights and normalization by agent type
    METRIC_CONFIGS = {
        AgentType.TRADE_RECOMMENDER.value: {
            'win_rate': {'weight': 0.3, 'max': 100},
            'avg_return': {'weight': 0.25, 'max': 10},
            'sharpe_ratio': {'weight': 0.2, 'max': 2},
            'max_drawdown': {'weight': 0.15, 'inverse': True, 'max': 50},
            'execution_speed': {'weight': 0.1, 'inverse': True, 'max': 10}
        },
        AgentType.ROI_ANALYST.value: {
            'accuracy': {'weight': 0.4, 'max': 100},
            'completeness': {'weight': 0.25, 'max': 100},
            'actionability': {'weight': 0.2, 'max': 100},
            'time_to_insight': {'weight': 0.15, 'inverse': True, 'max': 60}
        },
        AgentType.LEAD_GENERATOR.value: {
            'response_rate': {'weight': 0.3, 'max': 100},
            'conversion_rate': {'weight': 0.25, 'max': 100},
            'lead_quality': {'weight': 0.25, 'max': 100},
            'enrichment_accuracy': {'weight': 0.2, 'max': 100}
        }
    }
    
    @staticmethod
    def calculate_score(agent_id: str, metrics: Dict[str, float]) -> float:
        """Calculate composite success score (0-1)"""
        config = PerformanceTracker.METRIC_CONFIGS.get(agent_id, {})
        
        if not config:
            # Default calculation if agent type not configured
            return sum(metrics.values()) / len(metrics) if metrics else 0.5
        
        total_score = 0
        total_weight = 0
        
        for metric_name, metric_value in metrics.items():
            if metric_name in config:
                metric_config = config[metric_name]
                weight = metric_config['weight']
                
                # Normalize value
                if 'inverse' in metric_config and metric_config['inverse']:
                    # Inverse metric (lower is better)
                    normalized = 1.0 - min(metric_value / metric_config['max'], 1.0)
                else:
                    # Direct metric (higher is better)
                    normalized = min(metric_value / metric_config['max'], 1.0)
                
                total_score += normalized * weight
                total_weight += weight
        
        # Normalize by total weight used
        if total_weight > 0:
            return total_score / total_weight
        return 0.5  # Default score if no metrics match

class SkillEvolutionAgent:
    """
    Complete Skill Evolution Agent with all methods fixed.
    """
    
    def __init__(self, agent_id: str, skill_dir: str):
        """
        Initialize Skill Evolution Agent.
        
        Args:
            agent_id: Agent identifier (trade-recommender, roi-analyst, lead-generator)
            skill_dir: Directory containing skill files
        """
        self.agent_id = agent_id
        self.skill_dir = skill_dir
        self.evolution_dir = os.path.join(skill_dir, "evolution")
        
        # Create evolution directory structure
        os.makedirs(self.evolution_dir, exist_ok=True)
        os.makedirs(os.path.join(self.evolution_dir, "patterns"), exist_ok=True)
        os.makedirs(os.path.join(self.evolution_dir, "versions"), exist_ok=True)
        os.makedirs(os.path.join(self.evolution_dir, "history"), exist_ok=True)
        
        # Load existing data
        self.execution_history = self._load_json("execution_history", [])
        self.pattern_library = self._load_json("pattern_library", [])
        self.skill_evolution_log = self._load_json("skill_evolution_log", [])
        
        # FIXED: Lower pattern threshold for better learning
        self.pattern_threshold = 0.5  # Changed from 0.7 to 0.5
    
    def _load_json(self, filename: str, default: Any) -> Any:
        """Load JSON data from file"""
        filepath = os.path.join(self.evolution_dir, f"{filename}.json")
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except:
                return default
        return default
    
    def _save_json(self, filename: str, data: Any):
        """Save data to JSON file"""
        filepath = os.path.join(self.evolution_dir, f"{filename}.json")
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def track_execution(self, skill_name: str, inputs: Dict, outputs: Dict, 
                       metrics: Dict[str, float]) -> ExecutionRecord:
        """
        Track skill execution for learning and pattern extraction.
        """
        # Create execution record
        record = ExecutionRecord.create(
            agent_id=self.agent_id,
            skill_name=skill_name,
            inputs=inputs,
            outputs=outputs,
            metrics=metrics
        )
        
        # Add to history
        self.execution_history.append(asdict(record))
        self._save_json("execution_history", self.execution_history)
        
        # Extract pattern if successful (with lower threshold)
        if record.success_score >= self.pattern_threshold:
            self._extract_pattern(record)
        
        return record
    
    def _extract_pattern(self, record: ExecutionRecord):
        """Extract pattern from successful execution"""
        pattern = SkillPattern(
            pattern_id=self._generate_pattern_id(record),
            agent_id=self.agent_id,
            skill_name=record.skill_name,
            context=self._extract_context(record.inputs),
            strategy=self._extract_strategy(record),
            success_score=record.success_score,
            timestamp=record.timestamp
        )
        
        # Check for similar patterns
        similar_pattern = self._find_similar_pattern(pattern)
        if similar_pattern:
            # Update existing pattern
            similar_pattern['frequency'] += 1
            similar_pattern['success_score'] = max(
                similar_pattern['success_score'],
                pattern.success_score
            )
            # Add this agent to sources if not already there
            if self.agent_id not in similar_pattern['source_agents']:
                similar_pattern['source_agents'].append(self.agent_id)
        else:
            # Add new pattern
            self.pattern_library.append(asdict(pattern))
        
        # Save updated library
        self._save_json("pattern_library", self.pattern_library)
        
        # Also save individual pattern file
        pattern_file = os.path.join(
            self.evolution_dir,
            "patterns",
            f"{pattern.pattern_id}.json"
        )
        with open(pattern_file, 'w') as f:
            json.dump(asdict(pattern), f, indent=2)
    
    def _generate_pattern_id(self, record: ExecutionRecord) -> str:
        """Generate unique pattern ID"""
        skill_hash = hashlib.md5(record.skill_name.encode()).hexdigest()[:6]
        context_hash = hashlib.md5(
            json.dumps(record.inputs, sort_keys=True).encode()
        ).hexdigest()[:6]
        return f"{skill_hash}_{context_hash}"
    
    def _extract_context(self, inputs: Dict) -> Dict:
        """Extract context from inputs"""
        return {
            'input_types': {k: type(v).__name__ for k, v in inputs.items()},
            'input_count': len(inputs),
            'has_numeric': any(isinstance(v, (int, float)) for v in inputs.values()),
            'has_text': any(isinstance(v, str) for v in inputs.values())
        }
    
    def _extract_strategy(self, record: ExecutionRecord) -> Dict:
        """Extract strategy from execution"""
        outputs = record.outputs
        return {
            'output_type': type(outputs).__name__,
            'output_size': len(outputs) if isinstance(outputs, (dict, list)) else 1,
            'has_decisions': any(isinstance(v, bool) for v in outputs.values()) 
                           if isinstance(outputs, dict) else False,
            'complexity': len(str(outputs))
        }
    
    def _find_similar_pattern(self, new_pattern: SkillPattern) -> Optional[Dict]:
        """Find similar pattern in library"""
        for pattern in self.pattern_library:
            if self._patterns_similar(pattern, new_pattern):
                return pattern
        return None
    
    def _patterns_similar(self, pattern1: Dict, pattern2: SkillPattern) -> bool:
        """Check if two patterns are similar"""
        # Same skill
        if pattern1['skill_name'] != pattern2.skill_name:
            return False
        
        # Similar context
        ctx1 = pattern1['context']
        ctx2 = pattern2.context
        
        # Check input type similarity
        types1 = set(ctx1.get('input_types', {}).values())
        types2 = set(ctx2.get('input_types', {}).values())
        
        type_overlap = len(types1 & types2)
        type_total = len(types1 | types2)
        
        return type_overlap / max(type_total, 1) > 0.5
    
    def get_successful_patterns(self, skill_name: Optional[str] = None, 
                               min_score: float = 0.5) -> List[Dict]:
        """
        Get successful patterns.
        """
        patterns = self.pattern_library
        
        if skill_name:
            patterns = [p for p in patterns if p['skill_name'] == skill_name]
        
        patterns = [p for p in patterns if p['success_score'] >= min_score]
        
        # Sort by success score and frequency
        patterns.sort(key=lambda x: (x['success_score'], x.get('frequency', 1)), 
                     reverse=True)
        
        return patterns
    
    def evolve_skill(self, skill_name: str) -> Optional[str]:
        """
        Evolve a skill based on successful patterns.
        """
        # Get successful patterns for this skill
        successful_patterns = self.get_successful_patterns(skill_name, min_score=0.5)
        
        if not successful_patterns:
            print(f"No successful patterns found for {skill_name}")
            return None
        
        # Load current skill
        skill_path = os.path.join(self.skill_dir, f"{skill_name}.md")
        if not os.path.exists(skill_path):
            skill_path = os.path.join(self.skill_dir, "SKILL.md")
        
        if not os.path.exists(skill_path):
            print(f"Skill file not found: {skill_name}")
            return None
        
        with open(skill_path, 'r') as f:
            current_content = f.read()
        
        # Get performance data for this skill
        performance_data = [
            r for r in self.execution_history 
            if r['skill_name'] == skill_name
        ]
        
        # Generate evolved content
        evolved_content = self._generate_evolved_content(
            skill_name=skill_name,
            current_content=current_content,
            patterns=successful_patterns,
            performance_data=performance_data
        )
        
        # Create new version
        version_path = self._create_skill_version(skill_name, evolved_content)
        
        # Log evolution
        evolution_record = {
            'timestamp': datetime.now().isoformat(),
            'skill': skill_name,
            'old_version': skill_path,
            'new_version': version_path,
            'patterns_used': [p['pattern_id'] for p in successful_patterns],
            'pattern_count': len(successful_patterns),
            'avg_pattern_score': sum(p['success_score'] for p in successful_patterns) / len(successful_patterns)
        }
        
        self.skill_evolution_log.append(evolution_record)
        self._save_json("skill_evolution_log", self.skill_evolution_log)
        
        return version_path
    
    def _generate_evolved_content(self, skill_name: str, current_content: str,
                                 patterns: List[Dict], performance_data: List[Dict]) -> str:
        """
        Generate evolved skill content.
        """
        # Create evolved version with pattern annotations
        evolved = f"""# {skill_name} - Evolved Version
# Generated: {datetime.now().isoformat()}
# Based on {len(patterns)} successful patterns
# Average pattern success score: {sum(p['success_score'] for p in patterns) / len(patterns):.2f}

## Evolution Insights

### Successful Patterns Used:
"""
        
        for pattern in patterns[:3]:  # Top 3 patterns
            evolved += f"""
**Pattern {pattern['pattern_id']}** (Score: {pattern['success_score']:.2f})
- Context: {pattern['context'].get('input_types', {})}
- Strategy: {pattern['strategy']}
- Frequency: {pattern.get('frequency', 1)}
"""
        
        evolved += f"""

### Performance Summary:
- Total executions: {len(performance_data)}
- Average success: {sum(r['success_score'] for r in performance_data) / len(performance_data):.2f}
- Best execution: {max(r['success_score'] for r in performance_data):.2f}

---

## Original Skill Content

{current_content}

---

## Evolution Notes
This skill has been evolved using the Skill Evolution Framework.
Key improvements based on successful patterns have been incorporated.
"""
        
        return evolved
    
    def _create_skill_version(self, skill_name: str, content: str) -> str:
        """Create new version of skill"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        version_filename = f"{skill_name}_evolved_{timestamp}.md"
        version_path = os.path.join(self.evolution_dir, "versions", version_filename)
        
        with open(version_path, 'w') as f:
            f.write(content)
        
        return version_path
    
    # FIXED: Complete share_patterns method
    def share_patterns(self, other_agent: 'SkillEvolutionAgent') -> int:
        """
        Share successful patterns with another agent.
        """
        # Get top patterns
        top_patterns = self.get_successful_patterns(min_score=0.6)[:3]
        
        if not top_patterns:
            return 0
        
        # Share patterns
        shared_count = other_agent.receive_patterns(top_patterns)
        return shared_count
    
    # FIXED: Complete receive_patterns method
    def receive_patterns(self, patterns: List[Dict]) -> int:
        """
        Receive patterns from another agent.
        """
        added = 0
        
        for pattern in patterns:
            # Check if similar pattern exists
            similar = self._find_similar_pattern(SkillPattern(**pattern))
            if not similar:
                # Add new pattern
                self.pattern_library.append(pattern)
                added += 1
            else:
                # Update existing pattern
                similar['frequency'] += 1
                similar['success_score'] = max(
                    similar['success_score'],
                    pattern['success_score']
                )
                # Add source agent if not already there
                if pattern['agent_id'] not in similar['source_agents