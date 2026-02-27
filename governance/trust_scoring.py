#!/usr/bin/env python3
"""
Dynamic Trust Calibration System
DeepMind Pillar 3: Trust must be dynamically formed and updated based on verifiable data.
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path

class TrustScoring:
    """Trust scoring and authority management system"""
    
    def __init__(self, scores_dir: str = None):
        self.scores_dir = scores_dir or "/Users/cubiczan/.openclaw/workspace/governance/scores"
        os.makedirs(self.scores_dir, exist_ok=True)
        
        # Load existing scores
        self.scores = self._load_scores()
        self.history = self._load_history()
        
        # Default scores for new agents
        self.default_score = 50  # Start at 50/100
    
    def update_score(self, agent_id: str, contract: Dict[str, Any], result: Dict[str, Any]) -> float:
        """Update trust score based on contract execution"""
        
        # Get current score or default
        current_score = self.scores.get(agent_id, {}).get("score", self.default_score)
        
        # Calculate performance metrics
        metrics = self._calculate_performance_metrics(contract, result)
        
        # Calculate adjustment
        adjustment = self._calculate_adjustment(metrics, contract)
        
        # Apply adjustment with bounds
        new_score = max(0, min(100, current_score + adjustment))
        
        # Update score
        self.scores[agent_id] = {
            "score": new_score,
            "updated_at": datetime.now().isoformat(),
            "last_adjustment": adjustment,
            "metrics": metrics
        }
        
        # Save to history
        self._save_to_history(agent_id, new_score, adjustment, metrics)
        
        # Apply authority scaling
        authority = self._apply_authority_scaling(agent_id, new_score)
        
        # Save scores
        self._save_scores()
        
        return new_score
    
    def _calculate_performance_metrics(self, contract: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, float]:
        """Calculate performance metrics from contract execution"""
        metrics = {
            "success": 1.0 if contract.get("status") == "completed" else 0.0,
            "timeliness": self._calculate_timeliness(contract),
            "efficiency": self._calculate_efficiency(contract, result),
            "quality": self._calculate_quality(contract, result),
            "compliance": self._calculate_compliance(contract, result)
        }
        
        return metrics
    
    def _calculate_timeliness(self, contract: Dict[str, Any]) -> float:
        """Calculate timeliness score (0-1)"""
        if contract.get("status") != "completed" or not contract.get("execution_time"):
            return 0.0
        
        max_time = contract["resource_ceilings"].get("max_execution_time", 3600)
        actual_time = contract.get("execution_time", max_time * 2)
        
        # Score: 1.0 if within limit, decreasing to 0.0 at 2x limit
        if actual_time <= max_time:
            return 1.0
        elif actual_time <= max_time * 2:
            return 1.0 - ((actual_time - max_time) / max_time)
        else:
            return 0.0
    
    def _calculate_efficiency(self, contract: Dict[str, Any], result: Dict[str, Any]) -> float:
        """Calculate resource efficiency score (0-1)"""
        max_tokens = contract["resource_ceilings"].get("max_tokens", 10000)
        used_tokens = result.get("tokens_used", max_tokens)
        
        max_api = contract["resource_ceilings"].get("max_api_calls", 100)
        used_api = result.get("api_calls_used", max_api)
        
        # Token efficiency
        token_score = 1.0 if used_tokens <= max_tokens else max_tokens / used_tokens
        
        # API efficiency
        api_score = 1.0 if used_api <= max_api else max_api / used_api
        
        # Combined efficiency score
        return (token_score * 0.7 + api_score * 0.3)
    
    def _calculate_quality(self, contract: Dict[str, Any], result: Dict[str, Any]) -> float:
        """Calculate output quality score (0-1)"""
        # Check if all success metrics were met
        success_metrics = contract.get("success_metrics", {})
        
        metrics_met = 0
        total_metrics = 0
        
        # Check each metric
        for key, expected in success_metrics.items():
            if key.startswith("min_") or key.startswith("max_") or key in ["required_sections", "output_format"]:
                total_metrics += 1
                actual = result.get(key.replace("min_", "").replace("max_", ""))
                
                if actual is not None:
                    if key.startswith("min_"):
                        if actual >= expected:
                            metrics_met += 1
                    elif key.startswith("max_"):
                        if actual <= expected:
                            metrics_met += 1
                    elif key == "required_sections":
                        if all(section in result.get("output", "") for section in expected):
                            metrics_met += 1
                    elif key == "output_format":
                        if result.get("output_format") == expected:
                            metrics_met += 1
        
        return metrics_met / total_metrics if total_metrics > 0 else 0.5
    
    def _calculate_compliance(self, contract: Dict[str, Any], result: Dict[str, Any]) -> float:
        """Calculate compliance score (0-1)"""
        # Check revocation triggers
        if contract.get("status") == "revoked":
            return 0.0
        
        # Check if any resource ceilings were exceeded
        ceilings = contract.get("resource_ceilings", {})
        for resource, limit in ceilings.items():
            used = result.get(f"{resource}_used", 0)
            if used > limit * 1.1:  # 10% buffer
                return 0.5  # Partial compliance
        
        return 1.0
    
    def _calculate_adjustment(self, metrics: Dict[str, float], contract: Dict[str, Any]) -> float:
        """Calculate trust score adjustment based on metrics"""
        
        # Weightings for different metrics
        weights = {
            "success": 0.4,      # Most important: did it complete?
            "timeliness": 0.2,   # Important: was it on time?
            "quality": 0.2,      # Important: was it good quality?
            "efficiency": 0.1,   # Somewhat important: was it efficient?
            "compliance": 0.1    # Somewhat important: did it follow rules?
        }
        
        # Calculate weighted score (0-1)
        weighted_score = sum(metrics[metric] * weight for metric, weight in weights.items())
        
        # Convert to adjustment (-10 to +10)
        # 0.5 = no change, 1.0 = +10, 0.0 = -10
        adjustment = (weighted_score - 0.5) * 20
        
        # Scale by contract importance
        importance = contract.get("importance", 1.0)
        adjustment *= importance
        
        # Cap adjustment
        adjustment = max(-10, min(10, adjustment))
        
        return adjustment
    
    def _apply_authority_scaling(self, agent_id: str, score: float) -> Dict[str, Any]:
        """Apply graduated authority based on trust score"""
        
        if score >= 90:  # Tier 3: Elite
            authority = {
                "tier": 3,
                "name": "Elite",
                "can_delegate": True,
                "max_delegation_depth": 2,
                "budget_multiplier": 2.0,
                "oversight_level": "outcome_only",
                "task_complexity": "high",
                "requires_approval": False
            }
        elif score >= 75:  # Tier 2: Trusted
            authority = {
                "tier": 2,
                "name": "Trusted",
                "can_delegate": True,
                "max_delegation_depth": 1,
                "budget_multiplier": 1.5,
                "oversight_level": "periodic",
                "task_complexity": "medium",
                "requires_approval": False
            }
        elif score >= 50:  # Tier 1: Provisional
            authority = {
                "tier": 1,
                "name": "Provisional",
                "can_delegate": False,
                "max_delegation_depth": 0,
                "budget_multiplier": 1.0,
                "oversight_level": "full",
                "task_complexity": "low",
                "requires_approval": True
            }
        else:  # Tier 0: Untrusted
            authority = {
                "tier": 0,
                "name": "Untrusted",
                "can_delegate": False,
                "max_delegation_depth": 0,
                "budget_multiplier": 0.5,
                "oversight_level": "full_with_spot_checks",
                "task_complexity": "micro",
                "requires_approval": True
            }
        
        # Save authority
        self._save_authority(agent_id, authority)
        
        return authority
    
    def get_score(self, agent_id: str) -> float:
        """Get current trust score for agent"""
        agent_data = self.scores.get(agent_id, {})
        return agent_data.get("score", self.default_score)
    
    def get_authority(self, agent_id: str) -> Dict[str, Any]:
        """Get authority level for agent"""
        authority_file = os.path.join(self.scores_dir, "authority", f"{agent_id}.json")
        
        if os.path.exists(authority_file):
            with open(authority_file, 'r') as f:
                return json.load(f)
        
        # Default authority for new agents
        return self._apply_authority_scaling(agent_id, self.default_score)
    
    def can_delegate(self, agent_id: str) -> bool:
        """Check if agent can delegate tasks"""
        authority = self.get_authority(agent_id)
        return authority.get("can_delegate", False)
    
    def get_max_delegation_depth(self, agent_id: str) -> int:
        """Get maximum delegation depth for agent"""
        authority = self.get_authority(agent_id)
        return authority.get("max_delegation_depth", 0)
    
    def get_budget_multiplier(self, agent_id: str) -> float:
        """Get budget multiplier for agent"""
        authority = self.get_authority(agent_id)
        return authority.get("budget_multiplier", 1.0)
    
    def get_trend(self, agent_id: str, days: int = 7) -> str:
        """Get trust score trend (up, down, stable)"""
        history = self.history.get(agent_id, [])
        
        if len(history) < 2:
            return "stable"
        
        # Get recent history
        recent = [h for h in history if h["timestamp"] > (datetime.now() - timedelta(days=days)).isoformat()]
        
        if len(recent) < 2:
            return "stable"
        
        # Calculate trend
        first = recent[0]["score"]
        last = recent[-1]["score"]
        
        if last > first + 5:
            return "up"
        elif last < first - 5:
            return "down"
        else:
            return "stable"
    
    def get_top_performers(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top performing agents"""
        agents = []
        
        for agent_id, data in self.scores.items():
            if isinstance(data, dict) and "score" in data:
                agents.append({
                    "agent_id": agent_id,
                    "score": data["score"],
                    "authority": self.get_authority(agent_id)["name"]
                })
        
        # Sort by score (highest first)
        agents.sort(key=lambda x: x["score"], reverse=True)
        
        return agents[:limit]
    
    def get_bottom_performers(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get bottom performing agents"""
        agents = []
        
        for agent_id, data in self.scores.items():
            if isinstance(data, dict) and "score" in data:
                agents.append({
                    "agent_id": agent_id,
                    "score": data["score"],
                    "authority": self.get_authority(agent_id)["name"]
                })
        
        # Sort by score (lowest first)
        agents.sort(key=lambda x: x["score"])
        
        return agents[:limit]
    
    def _load_scores(self) -> Dict[str, Any]:
        """Load scores from disk"""
        scores_file = os.path.join(self.scores_dir, "trust_scores.json")
        
        if os.path.exists(scores_file):
            with open(scores_file, 'r') as f:
                return json.load(f)
        
        return {}
    
    def _save_scores(self):
        """Save scores to disk"""
        scores_file = os.path.join(self.scores_dir, "trust_scores.json")
        
        with open(scores_file, 'w') as f:
            json.dump(self.scores, f, indent=2)
    
    def _load_history(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load score history from disk"""
        history_dir = os.path.join(self.scores_dir, "history")
        os.makedirs(history_dir, exist_ok=True)
        
        history = {}
        
        for file in Path(history_dir).glob("*.json"):
            agent_id = file.stem
            try:
                with open(file, 'r') as f:
                    history[agent_id] = json.load(f)
            except Exception as e:
                print(f"Error loading history for {agent_id}: {e}")
                history[agent_id] = []
        
        return history
    
    def _save_to_history(self, agent_id: str, score: float, adjustment: float, metrics: Dict[str, float]):
        """Save score update to history"""
        history_dir = os.path.join(self.scores_dir, "history")
        os.makedirs(history_dir, exist_ok=True)
        
        history_file = os.path.join(history_dir, f"{agent_id}.json")
        
        # Load existing history
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = []
        
        # Add new entry
        entry = {
            "timestamp": datetime.now().isoformat(),
            "score": score,
            "adjustment": adjustment,
            "metrics": metrics
        }
        
        history.append(entry)
        
        # Keep only last 100 entries
        if len(history) > 100:
            history = history[-100:]
        
        # Save history
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
        
        # Update in-memory cache
        self.history[agent_id] = history
    
    def _save_authority(self, agent_id: str, authority: Dict[str, Any]):
        """Save authority level to disk"""
        authority_dir = os.path.join(self.scores_dir, "authority")
        os.makedirs(authority_dir, exist_ok=True)
        
        authority_file = os.path.join(authority_dir, f"{agent_id}.json")
        
        with open(authority_file, 'w') as f:
            json.dump(authority, f, indent=2)


# Initialize default scores for existing agents
def initialize_agent_scores():
    """Initialize trust scores for existing agents"""
    scoring = TrustScoring()
    
    # Default agents
    agents = [
        "trade-recommender",
        "roi-analyst", 
        "lead-generator",
        "main-agent",
        "agent-browser"
    ]
    
    for agent_id in agents:
        if agent_id not in scoring.scores:
            # Start new agents at default score
            scoring.scores[agent_id] = {
                "score": scoring.default_score,
                "updated_at": datetime.now().isoformat(),
                "last_adjustment": 0
            }
            
            # Apply initial authority
            scoring._apply_authority_scaling(agent_id, scoring.default_score)
    
    scoring._save_scores()
    
    return scoring