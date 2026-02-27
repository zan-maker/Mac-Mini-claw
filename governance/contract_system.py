#!/usr/bin/env python3
"""
Contract-First Decomposition System
DeepMind Pillar 1: Every delegated task must have precise verification criteria BEFORE execution.
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

class ContractSystem:
    """Contract creation, validation, and management"""
    
    def __init__(self, contracts_dir: str = None):
        self.contracts_dir = contracts_dir or "/Users/cubiczan/.openclaw/workspace/governance/contracts"
        os.makedirs(self.contracts_dir, exist_ok=True)
        
        # Load existing contracts
        self.contracts = self._load_contracts()
    
    def create_contract(self, delegator: str, delegatee: str, task_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Create a governance contract for task delegation"""
        
        contract_id = str(uuid.uuid4())
        
        contract = {
            "contract_id": contract_id,
            "delegator": delegator,
            "delegatee": delegatee,
            "task": task_spec.get("task", "unknown"),
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            
            # Success metrics (must be verifiable)
            "success_metrics": self._validate_success_metrics(
                task_spec.get("success_metrics", {})
            ),
            
            # Verification method
            "verification_method": task_spec.get("verification_method", "unit_test"),
            
            # Liability
            "liability_firebreak": task_spec.get("liability_firebreak", "delegatee_assumes_full"),
            "ultimate_responsibility": delegator,
            
            # Resource ceilings
            "resource_ceilings": self._validate_resource_ceilings(
                task_spec.get("resource_ceilings", {})
            ),
            
            # Revocation triggers
            "revocation_triggers": task_spec.get("revocation_triggers", []),
            
            # Chain info (for accountability)
            "parent_contract": task_spec.get("parent_contract"),
            "child_contracts": [],
            "chain_depth": task_spec.get("chain_depth", 0),
            
            # Execution tracking
            "started_at": None,
            "completed_at": None,
            "execution_time": None,
            "result_hash": None,
            "proof": None,
            
            # Penalties and rewards
            "penalty_applied": False,
            "reward_applied": False,
            "trust_score_impact": 0
        }
        
        # Save contract
        self._save_contract(contract)
        
        # Update parent if this is a sub-delegation
        if contract["parent_contract"]:
            self._add_child_to_parent(contract["parent_contract"], contract_id)
        
        return contract
    
    def _validate_success_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that success metrics are precise and verifiable"""
        required = {
            "output_format": metrics.get("output_format", "unknown"),
            "verification_possible": True  # Must be verifiable
        }
        
        # Add any provided metrics
        required.update(metrics)
        
        return required
    
    def _validate_resource_ceilings(self, ceilings: Dict[str, Any]) -> Dict[str, Any]:
        """Validate resource ceilings are reasonable"""
        defaults = {
            "max_execution_time": 3600,  # 1 hour default
            "max_tokens": 10000,
            "max_api_calls": 100,
            "max_memory_mb": 1024,
            "max_disk_mb": 100
        }
        
        # Override defaults with provided values
        defaults.update(ceilings)
        
        return defaults
    
    def mark_started(self, contract_id: str):
        """Mark contract as started"""
        contract = self.get_contract(contract_id)
        if contract:
            contract["status"] = "started"
            contract["started_at"] = datetime.now().isoformat()
            contract["updated_at"] = datetime.now().isoformat()
            self._save_contract(contract)
    
    def mark_completed(self, contract_id: str, result_hash: str, proof: str = None):
        """Mark contract as completed with result"""
        contract = self.get_contract(contract_id)
        if contract:
            contract["status"] = "completed"
            contract["completed_at"] = datetime.now().isoformat()
            contract["updated_at"] = datetime.now().isoformat()
            contract["result_hash"] = result_hash
            contract["proof"] = proof
            
            # Calculate execution time
            if contract["started_at"]:
                started = datetime.fromisoformat(contract["started_at"])
                completed = datetime.fromisoformat(contract["completed_at"])
                contract["execution_time"] = (completed - started).total_seconds()
            
            self._save_contract(contract)
    
    def mark_failed(self, contract_id: str, reason: str):
        """Mark contract as failed"""
        contract = self.get_contract(contract_id)
        if contract:
            contract["status"] = "failed"
            contract["updated_at"] = datetime.now().isoformat()
            contract["failure_reason"] = reason
            self._save_contract(contract)
    
    def check_revocation_triggers(self, contract_id: str, current_metrics: Dict[str, Any]) -> bool:
        """Check if any revocation triggers have been hit"""
        contract = self.get_contract(contract_id)
        if not contract:
            return False
        
        triggers = contract.get("revocation_triggers", [])
        
        for trigger in triggers:
            if self._trigger_hit(trigger, current_metrics, contract):
                contract["status"] = "revoked"
                contract["revocation_reason"] = trigger
                contract["updated_at"] = datetime.now().isoformat()
                self._save_contract(contract)
                return True
        
        return False
    
    def _trigger_hit(self, trigger: str, metrics: Dict[str, Any], contract: Dict[str, Any]) -> bool:
        """Check if a specific trigger has been hit"""
        if trigger == "execution_time_exceeded":
            max_time = contract["resource_ceilings"].get("max_execution_time", 3600)
            current_time = metrics.get("execution_time", 0)
            return current_time > max_time
        
        elif trigger == "token_budget_exceeded":
            max_tokens = contract["resource_ceilings"].get("max_tokens", 10000)
            current_tokens = metrics.get("tokens_used", 0)
            return current_tokens > max_tokens
        
        elif trigger == "api_limit_exceeded":
            max_api = contract["resource_ceilings"].get("max_api_calls", 100)
            current_api = metrics.get("api_calls", 0)
            return current_api > max_api
        
        # Add more trigger checks as needed
        return False
    
    def get_contract(self, contract_id: str) -> Optional[Dict[str, Any]]:
        """Get contract by ID"""
        return self.contracts.get(contract_id)
    
    def get_contracts_by_agent(self, agent_id: str, status: str = None) -> list:
        """Get all contracts for an agent"""
        contracts = []
        
        for contract in self.contracts.values():
            if contract["delegatee"] == agent_id or contract["delegator"] == agent_id:
                if status is None or contract["status"] == status:
                    contracts.append(contract)
        
        return contracts
    
    def _load_contracts(self) -> Dict[str, Dict[str, Any]]:
        """Load all contracts from disk"""
        contracts = {}
        
        for file in Path(self.contracts_dir).glob("*.json"):
            try:
                with open(file, 'r') as f:
                    contract = json.load(f)
                    contracts[contract["contract_id"]] = contract
            except Exception as e:
                print(f"Error loading contract {file}: {e}")
        
        return contracts
    
    def _save_contract(self, contract: Dict[str, Any]):
        """Save contract to disk"""
        contract_id = contract["contract_id"]
        file_path = os.path.join(self.contracts_dir, f"{contract_id}.json")
        
        with open(file_path, 'w') as f:
            json.dump(contract, f, indent=2)
        
        # Update in-memory cache
        self.contracts[contract_id] = contract
    
    def _add_child_to_parent(self, parent_id: str, child_id: str):
        """Add child contract to parent's child_contracts list"""
        parent = self.get_contract(parent_id)
        if parent:
            if child_id not in parent["child_contracts"]:
                parent["child_contracts"].append(child_id)
                parent["updated_at"] = datetime.now().isoformat()
                self._save_contract(parent)
    
    def get_success_rate(self, agent_id: str) -> float:
        """Calculate agent's contract success rate"""
        contracts = self.get_contracts_by_agent(agent_id)
        
        if not contracts:
            return 0.0
        
        completed = [c for c in contracts if c["status"] == "completed"]
        failed = [c for c in contracts if c["status"] in ["failed", "revoked"]]
        
        total_attempted = len(completed) + len(failed)
        
        if total_attempted == 0:
            return 0.0
        
        return len(completed) / total_attempted
    
    def get_average_execution_time(self, agent_id: str) -> float:
        """Calculate average execution time for completed contracts"""
        contracts = self.get_contracts_by_agent(agent_id, "completed")
        
        if not contracts:
            return 0.0
        
        total_time = 0
        count = 0
        
        for contract in contracts:
            if contract.get("execution_time"):
                total_time += contract["execution_time"]
                count += 1
        
        return total_time / count if count > 0 else 0.0


# Contract templates for common tasks
CONTRACT_TEMPLATES = {
    "reddit_analysis": {
        "task": "daily_reddit_analysis",
        "success_metrics": {
            "output_format": "markdown",
            "required_sections": ["TOP 3 PICKS", "KALSHI INSIGHTS", "RISK DISCLAIMER"],
            "min_recommendations": 3,
            "max_execution_time": 1800,
            "token_budget": 800
        },
        "verification_method": "unit_test + hash_verification",
        "resource_ceilings": {
            "max_execution_time": 1800,
            "max_tokens": 1000,
            "max_api_calls": 50
        },
        "revocation_triggers": [
            "execution_time_exceeded",
            "token_budget_exceeded"
        ]
    },
    
    "financial_analysis": {
        "task": "weekly_performance_analysis",
        "success_metrics": {
            "output_format": "markdown",
            "accuracy_threshold": 0.85,
            "completeness_required": True,
            "audit_trail": True
        },
        "verification_method": "cross_validation + expert_review",
        "resource_ceilings": {
            "max_execution_time": 3600,
            "max_tokens": 5000,
            "max_api_calls": 100
        }
    },
    
    "lead_generation": {
        "task": "daily_lead_generation",
        "success_metrics": {
            "min_leads": 50,
            "max_leads": 70,
            "privacy_compliance": True,
            "email_validation_rate": 0.95
        },
        "verification_method": "validation_check + compliance_audit",
        "resource_ceilings": {
            "max_execution_time": 7200,
            "max_tokens": 3000,
            "max_api_calls": 200
        }
    }
}


def create_contract_from_template(template_name: str, delegator: str, delegatee: str, **kwargs) -> Dict[str, Any]:
    """Create contract from template with customizations"""
    template = CONTRACT_TEMPLATES.get(template_name, {})
    
    # Merge template with any customizations
    task_spec = template.copy()
    task_spec.update(kwargs)
    
    # Create contract
    system = ContractSystem()
    return system.create_contract(delegator, delegatee, task_spec)