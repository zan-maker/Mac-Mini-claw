#!/usr/bin/env python3
"""
Complete Decision Trees Implementation
Trust Protocol Decision Framework
"""

import json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional
from monitor_trust_compliance import TrustMonitor

class Priority(Enum):
    """Task priority levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

class DecisionTree:
    """Base class for decision trees"""
    
    def __init__(self, monitor: TrustMonitor = None):
        self.monitor = monitor or TrustMonitor()
        self.decision_log = []
    
    def log_decision(self, tree_name: str, decision: Dict, score: float = None):
        """Log decision with transparency"""
        decision_id = self.monitor.log_decision(
            decision_type=f"tree_{tree_name}",
            options=decision.get('options', []),
            chosen=decision.get('chosen'),
            reasoning=decision.get('reasoning', ''),
            score=score
        )
        
        self.decision_log.append({
            'id': decision_id,
            'tree': tree_name,
            'decision': decision,
            'timestamp': datetime.now().isoformat()
        })
        
        return decision_id

class SystemMaintenanceVsFeatureTree(DecisionTree):
    """
    Tree 1: System Maintenance vs New Feature
    """
    
    def decide(self, maintenance_issue: Dict, new_feature: Dict, context: Dict) -> Dict:
        """Make decision between maintenance and feature"""
        
        options = [
            {'name': 'Fix maintenance issue', 'type': 'maintenance'},
            {'name': 'Build new feature', 'type': 'feature'},
            {'name': 'Do both (parallel)', 'type': 'both'},
            {'name': 'Defer decision', 'type': 'defer'}
        ]
        
        reasoning = []
        
        # Decision logic
        if maintenance_issue.get('stability_risk', False):
            chosen = options[0]
            reasoning.append("System stability at risk")
        elif new_feature.get('has_deadline', False):
            chosen = options[1]
            reasoning.append("Explicit deadline for feature")
        else:
            # Calculate ROI
            m_roi = self.calculate_roi(maintenance_issue)
            f_roi = self.calculate_roi(new_feature)
            
            if m_roi > f_roi:
                chosen = options[0]
                reasoning.append(f"Higher ROI ({m_roi:.1f} vs {f_roi:.1f})")
            else:
                chosen = options[1]
                reasoning.append(f"Higher ROI ({f_roi:.1f} vs {m_roi:.1f})")
        
        decision = {
            'options': [opt['name'] for opt in options],
            'chosen': chosen['name'],
            'reasoning': ' | '.join(reasoning),
            'confidence': self.calculate_confidence(maintenance_issue, new_feature)
        }
        
        self.log_decision('maintenance_vs_feature', decision, decision['confidence'])
        return decision
    
    def calculate_roi(self, item: Dict) -> float:
        impact = item.get('impact', 5)
        effort = item.get('effort', 5)
        urgency = item.get('urgency', 5)
        return (impact * urgency) / max(effort, 1)
    
    def calculate_confidence(self, maintenance: Dict, feature: Dict) -> float:
        factors = []
        if maintenance.get('has_data'): factors.append(0.7)
        if feature.get('has_data'): factors.append(0.7)
        return sum(factors) / len(factors) if factors else 0.5

class CommunicationDecisionTree(DecisionTree):
    """
    Tree 2: Proactive Communication Decision
    """
    
    def decide(self, information: Dict, context: Dict) -> Dict:
        options = [
            {'name': 'Notify immediately', 'action': 'immediate'},
            {'name': 'Wait for next heartbeat', 'action': 'defer'},
            {'name': 'Batch with next update', 'action': 'batch'},
            {'name': 'Do not notify', 'action': 'silent'}
        ]
        
        reasoning = []
        
        # Check time sensitivity
        if information.get('time_sensitive') and information.get('time_horizon_hours', 48) < 24:
            chosen = options[0]
            reasoning.append(f"Time-sensitive ({information.get('time_horizon_hours')}h)")
        
        # Check focus time
        elif context.get('in_focus_time'):
            chosen = options[1]
            reasoning.append("Human in focus time")
        
        # Value vs cost analysis
        else:
            value = information.get('value_score', 5)
            cost = self.estimate_communication_cost(context)
            
            if value > cost:
                chosen = options[0]
                reasoning.append(f"Value ({value}) > cost ({cost:.1f})")
            else:
                chosen = options[2]
                reasoning.append(f"Cost ({cost:.1f}) > value ({value})")
        
        # Quiet hours check
        monitor = TrustMonitor()
        if monitor.is_quiet_hours() and chosen['action'] == 'immediate':
            if not information.get('critical'):
                chosen = options[1]
                reasoning.append("Quiet hours - deferred")
        
        decision = {
            'options': [opt['name'] for opt in options],
            'chosen': chosen['name'],
            'action': chosen['action'],
            'reasoning': ' | '.join(reasoning),
            'confidence': self.calculate_confidence(information, context)
        }
        
        self.log_decision('communication', decision, decision['confidence'])
        return decision
    
    def estimate_communication_cost(self, context: Dict) -> float:
        cost = 5.0
        hour = datetime.now().hour
        
        if 22 <= hour or hour < 8:
            cost += 3.0
        elif 9 <= hour <= 17:
            cost -= 1.0
        
        if context.get('recent_messages_count', 0) > 10:
            cost += 1.0
        
        if context.get('human_busy'):
            cost += 2.0
        
        return max(1.0, min(10.0, cost))
    
    def calculate_confidence(self, information: Dict, context: Dict) -> float:
        confidence = 0.7
        if context.get('has_recent_interaction'):
            confidence += 0.1
        if information.get('has_clear_urgency'):
            confidence += 0.1
        return max(0.3, min(1.0, confidence))

class ErrorHandlingTree(DecisionTree):
    """
    Tree 3: Error Handling Protocol
    """
    
    def decide(self, error: Dict, context: Dict) -> Dict:
        options = [
            {'name': 'Immediate alert + stop', 'action': 'stop'},
            {'name': 'Notify + alternatives', 'action': 'notify'},
            {'name': 'Auto-fix + document', 'action': 'auto_fix'},
            {'name': 'Log for review', 'action': 'log'},
            {'name': 'Ignore', 'action': 'ignore'}
        ]
        
        reasoning = []
        
        if error.get('safety_critical'):
            chosen = options[0]
            reasoning.append("Safety-critical error")
        elif error.get('can_auto_fix') and error.get('auto_fix_confidence', 0) > 0.8:
            chosen = options[2]
            reasoning.append(f"Auto-fixable ({error.get('auto_fix_confidence', 0):.0%} confidence)")
        elif error.get('affects_outputs'):
            chosen = options[1]
            reasoning.append("Affects current outputs")
        elif error.get('is_known_issue'):
            chosen = options[3]
            reasoning.append("Known issue")
        else:
            chosen = options[3]
            reasoning.append("Default: log for review")
        
        decision = {
            'options': [opt['name'] for opt in options],
            'chosen': chosen['name'],
            'action': chosen['action'],
            'reasoning': ' | '.join(reasoning),
            'confidence': self.calculate_confidence(error, context)
        }
        
        self.log_decision('error_handling', decision, decision['confidence'])
        return decision
    
    def calculate_confidence(self, error: Dict, context: Dict) -> float:
        confidence = 0.8
        if error.get('has_known_solution'):
            confidence += 0.1
        if context.get('similar_errors_handled', 0) > 0:
            confidence += 0.1
        if context.get('system_unstable'):
            confidence -= 0.2
        return max(0.4, min(1.0, confidence))

class ResourceAllocationTree(DecisionTree):
    """
    Tree 4: Resource Allocation
    """
    
    def decide(self, tasks: List[Dict], resources: Dict) -> Dict:
        # Check resource exhaustion
        exhausted = any(
            r.get('usage_percent', 0) > 80 
            for r in resources.values() 
            if isinstance(r, dict)
        )
        
        if exhausted:
            strategy = 'conservative'
            allocation = self.conservative_allocation(tasks, resources)
            reasoning = "Resources near exhaustion"
        elif len(tasks) > 1:
            strategy = 'scored'
            allocation = self.scored_allocation(tasks, resources)
            reasoning = "Multiple tasks - using scoring"
        else:
            strategy = 'direct'
            allocation = self.direct_allocation(tasks, resources)
            reasoning = "Single task allocation"
        
        options = [
            'Conservative allocation',
            'Scored allocation', 
            'Direct allocation',
            'Deferred allocation'
        ]
        
        decision = {
            'options': options,
            'chosen': f'{strategy.title()} allocation',
            'strategy': strategy,
            'allocation': allocation,
            'reasoning': reasoning,
            'confidence': self.calculate_confidence(tasks, resources)
        }
        
        self.log_decision('resource_allocation', decision, decision['confidence'])
        return decision
    
    def conservative_allocation(self, tasks: List[Dict], resources: Dict) -> Dict:
        """Allocate minimal resources to essential tasks only"""
        allocation = {}
        essential_tasks = [t for t in tasks if t.get('essential', False)]
        
        if essential_tasks:
            # Split remaining resources among essential tasks
            remaining = resources.get('remaining_percent', 20)
            per_task = remaining / len(essential_tasks)
            
            for task in essential_tasks:
                allocation[task['id']] = per_task
        
        return allocation
    
    def scored_allocation(self, tasks: List[Dict], resources: Dict) -> Dict:
        """Allocate based on task scores"""
        allocation = {}
        total_score = sum(t.get('priority_score', 5) for t in tasks)
        
        if total_score > 0:
            for task in tasks:
                share = task.get('priority_score', 5) / total_score
                allocation[task['id']] = share * 100  # Percentage
        
        return allocation
    
    def direct_allocation(self, tasks: List[Dict], resources: Dict) -> Dict:
        """Direct allocation for single task"""
        allocation = {}
        if tasks:
            allocation[tasks[0]['id']] = 100  # All resources
        return allocation
    
    def calculate_confidence(self, tasks: List[Dict], resources: Dict) -> float:
        confidence = 0.7
        if len(tasks) <= 3:
            confidence += 0.1
        if all('priority_score' in t for t in tasks):
            confidence += 0.1
        return max(0.5, min(1.0, confidence))

class DecisionOrchestrator:
    """Orchestrates decision trees based on context"""
    
    def __init__(self):
        self.monitor = TrustMonitor()
        self.trees = {
            'maintenance_vs_feature': SystemMaintenanceVsFeatureTree(self.monitor),
            'communication': CommunicationDecisionTree(self.monitor),
            'error_handling': ErrorHandlingTree(self.monitor),
            'resource_allocation': ResourceAllocationTree(self.monitor)
        }
    
    def make_decision(self, scenario_type: str, **kwargs) -> Dict:
        """Make decision using appropriate tree"""
        tree = self.trees.get(scenario_type)
        if not tree:
            return {'error': f'Unknown scenario type: {scenario_type}'}
        
        return tree.decide(**kwargs)
    
    def run_compliance_check(self):
        """Run trust compliance check"""
        return self.monitor.run_compliance_check()
    
    def generate_daily_report(self):
        """Generate daily compliance report"""
        return self.monitor.generate_daily_report()

# Example usage and testing
def test_decision_trees():
    """Test all decision trees"""
    orchestrator = DecisionOrchestrator()
    
    print("🧪 Testing Decision Trees")
    print("="*50)
    
    # Test 1: Maintenance vs Feature
    print("\n1. Maintenance vs Feature Decision:")
    maintenance = {
        'description': 'API rate limiting issue',
        'stability_risk': True,
        'impact': 8,
        'effort': 3,
        'urgency': 9,
        'has_data': True
    }
    
    feature = {
        'description': 'New reporting dashboard',
        'has_deadline': False,
        'impact': 7,
        'effort': 5,
        'urgency': 6,
        'has_data': True
    }
    
    context = {'has_precedent': True, 'known_preference': False}
    
    result = orchestrator.make_decision(
        'maintenance_vs_feature',
        maintenance_issue=maintenance,
        new_feature=feature,
        context=context
    )
    
    print(f"   Decision: {result.get('chosen')}")
    print(f"   Reasoning: {result.get('reasoning')}")
    print(f"   Confidence: {result.get('confidence', 0):.0%}")
    
    # Test 2: Communication Decision
    print("\n2. Communication Decision:")
    information = {
        'type': 'market_opportunity',
        'time_sensitive': True,
        'time_horizon_hours': 12,
        'value_score': 8,
        'critical': False
    }
    
    human_context = {
        'in_focus_time': False,
        'recent_messages_count': 5,
        'human_busy': False,
        'has_recent_interaction': True
    }
    
    result = orchestrator.make_decision(
        'communication',
        information=information,
        context=human_context
    )
    
    print(f"   Decision: {result.get('chosen')}")
    print(f"   Action: {result.get('action')}")
    print(f"   Confidence: {result.get('confidence', 0):.0%}")
    
    # Test 3: Error Handling
    print("\n3. Error Handling Decision:")
    error = {
        'type': 'api_connection',
        'safety_critical': False,
        'can_auto_fix': True,
        'auto_fix_confidence': 0.9,
        'affects_outputs': True,
        'is_known_issue': False,
        'has_known_solution': True
    }
    
    system_context = {
        'similar_errors_handled': 3,
        'system_unstable': False
    }
    
    result = orchestrator.make_decision(
        'error_handling',
        error=error,
        context=system_context
    )
    
    print(f"   Decision: {result.get('chosen')}")
    print(f"   Action: {result.get('action')}")
    print(f"   Confidence: {result.get('confidence', 0):.0%}")
    
    # Test 4: Resource Allocation
    print("\n4. Resource Allocation Decision:")
    tasks = [
        {'id': 'task1', 'essential': True, 'priority_score': 8},
        {'id': 'task2', 'essential': False, 'priority_score': 6},
        {'id': 'task3', 'essential': True, 'priority_score': 7}
    ]
    
    resources = {
        'api_calls': {'usage_percent': 65},
        'time_minutes': {'usage_percent': 40},
        'memory_mb': {'usage_percent': 75},
        'remaining_percent': 35
    }
    
    result = orchestrator.make_decision(
        'resource_allocation',
        tasks=tasks,
        resources=resources
    )
    
    print(f"   Strategy: {result.get('strategy')}")
    print(f"   Allocation: {result.get('allocation')}")
    print(f"   Confidence: {result.get('confidence', 0):.0%}")
    
    # Run compliance check
    print("\n5. Trust Compliance Check:")
    report = orchestrator.run_compliance_check()
    print(f"   Compliance Score: {report.get('compliance_score', 0):.1%}")
    
    print("\n" + "="*50)
    print("✅ Decision Trees Test Complete")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Trust Protocol Decision Trees")
    parser.add_argument('--test', action='store_true', help='Run tests')
    parser.add_argument('--compliance', action='store_true', help='Run compliance check')
    parser.add_argument('--daily', action='store_true', help='Generate daily report')
    
    args = parser.parse_args()
    
    if args.test:
        test_decision_trees()
    elif args.compliance:
        orchestrator = DecisionOrchestrator()
        report = orchestrator.run_compliance_check()
        print(f"Compliance Score: {report.get('compliance_score', 0):.1%}")
    elif args.daily:
        orchestrator = DecisionOrchestrator()
        report = orchestrator.generate_daily_report()
        if report:
            print(f"Daily Report: {report.get('date', 'unknown')}")
            print(f"  Avg Score: {report.get('average_compliance_score', 0):.1%}")