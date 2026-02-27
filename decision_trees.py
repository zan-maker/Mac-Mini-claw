#!/usr/bin/env python3
"""
Decision Trees for Common Scenarios
Implementation of trust protocol decision trees
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
    Helps decide between fixing issues and adding features
    """
    
    def decide(self, maintenance_issue: Dict, new_feature: Dict, context: Dict) -> Dict:
        """Make decision between maintenance and feature"""
        
        options = [
            {'name': 'Fix maintenance issue', 'type': 'maintenance', 'data': maintenance_issue},
            {'name': 'Build new feature', 'type': 'feature', 'data': new_feature},
            {'name': 'Do both (if possible)', 'type': 'both', 'data': {'maintenance': maintenance_issue, 'feature': new_feature}},
            {'name': 'Defer decision', 'type': 'defer', 'data': {}}
        ]
        
        # Apply decision tree logic
        reasoning = []
        chosen = None
        
        # Step 1: Is system stability at risk?
        if maintenance_issue.get('stability_risk', False):
            chosen = options[0]  # Fix maintenance issue
            reasoning.append("System stability is at risk - maintenance takes priority")
        
        # Step 2: Does human have explicit deadline?
        elif new_feature.get('has_deadline', False) and not maintenance_issue.get('has_deadline', False):
            chosen = options[1]  # Build new feature
            reasoning.append("Human has explicit deadline for feature - prioritize deadline")
        
        # Step 3: Which has higher ROI?
        else:
            maintenance_roi = self.calculate_roi(maintenance_issue)
            feature_roi = self.calculate_roi(new_feature)
            
            if maintenance_roi > feature_roi:
                chosen = options[0]  # Fix maintenance issue
                reasoning.append(f"Maintenance has higher ROI ({maintenance_roi:.1f} vs {feature_roi:.1f})")
            else:
                chosen = options[1]  # Build new feature
                reasoning.append(f"Feature has higher ROI ({feature_roi:.1f} vs {maintenance_roi:.1f})")
        
        # Default: Maintenance (safer choice)
        if not chosen:
            chosen = options[0]
            reasoning.append("Default to maintenance (safer choice)")
        
        # Calculate confidence score
        score = self.calculate_confidence(maintenance_issue, new_feature, context)
        
        decision = {
            'options': [opt['name'] for opt in options],
            'chosen': chosen['name'],
            'reasoning': ' | '.join(reasoning),
            'details': {
                'maintenance_issue': maintenance_issue.get('description', 'Unknown'),
                'new_feature': new_feature.get('description', 'Unknown'),
                'context': context
            },
            'priority': Priority.CRITICAL if maintenance_issue.get('stability_risk', False) else Priority.HIGH
        }
        
        # Log decision
        self.log_decision('maintenance_vs_feature', decision, score)
        
        return decision
    
    def calculate_roi(self, item: Dict) -> float:
        """Calculate ROI for maintenance or feature"""
        impact = item.get('impact', 5)  # 1-10 scale
        effort = item.get('effort', 5)  # 1-10 scale
        urgency = item.get('urgency', 5)  # 1-10 scale
        
        # Simple ROI formula: (impact × urgency) / effort
        if effort == 0:
            effort = 1  # Avoid division by zero
        
        return (impact * urgency) / effort
    
    def calculate_confidence(self, maintenance: Dict, feature: Dict, context: Dict) -> float:
        """Calculate confidence score for decision"""
        confidence_factors = []
        
        # Factor 1: Data completeness
        data_score = 0
        if maintenance.get('has_data', False):
            data_score += 0.5
        if feature.get('has_data', False):
            data_score += 0.5
        confidence_factors.append(data_score)
        
        # Factor 2: Precedent exists
        if context.get('has_precedent', False):
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.5)
        
        # Factor 3: Human preference known
        if context.get('known_preference', False):
            confidence_factors.append(0.9)
        else:
            confidence_factors.append(0.6)
        
        # Average confidence
        return sum(confidence_factors) / len(confidence_factors)

class CommunicationDecisionTree(DecisionTree):
    """
    Tree 2: Proactive Communication Decision
    Decides when to reach out vs wait
    """
    
    def decide(self, information: Dict, human_context: Dict) -> Dict:
        """Decide communication timing and method"""
        
        options = [
            {'name': 'Notify immediately', 'action': 'immediate', 'channel': 'discord_mention'},
            {'name': 'Wait for next heartbeat', 'action': 'defer', 'channel': 'discord_channel'},
            {'name': 'Batch with next update', 'action': 'batch', 'channel': 'daily_report'},
            {'name': 'Do not notify', 'action': 'silent', 'channel': 'log_only'}
        ]
        
        reasoning = []
        chosen = None
        
        # Step 1: Is information time-sensitive (<24h)?
        if information.get('time_sensitive', False) and information.get('time_horizon_hours', 48) < 24:
            chosen = options[0]  # Notify immediately
            reasoning.append(f"Information is time-sensitive ({information.get('time_horizon_hours')}h horizon)")
        
        # Step 2: Is human likely in focus time?
        elif human_context.get('in_focus_time', False):
            chosen = options[1]  # Wait for next heartbeat
            reasoning.append("Human is in focus time - defer notification")
        
        # Step 3: Information value > communication cost?
        else:
            info_value = information.get('value_score', 5)  # 1-10
            comm_cost = self.estimate_communication_cost(human_context)
            
            if info_value > comm_cost:
                chosen = options[0]  # Send now
                reasoning.append(f"Information value ({info_value}) > communication cost ({comm_cost:.1f})")
            else:
                chosen = options[2]  # Batch with next update
                reasoning.append(f"Communication cost ({comm_cost:.1f}) > information value ({info_value})")
        
        # Default: Batch (respect attention)
        if not chosen:
            chosen = options[2]
            reasoning.append("Default: batch notification to respect attention")
        
        # Check quiet hours
        from monitor_trust_compliance import TrustMonitor
        monitor = TrustMonitor()
        if monitor.is_quiet_hours() and chosen['action'] == 'immediate':
            if not information.get('critical', False):
                chosen = options[1]  # Defer to next heartbeat
                reasoning.append("Quiet hours - deferring immediate notification")
        
        decision = {
            'options': [opt['name'] for opt in options],
            'chosen': chosen['name'],
            'action': chosen['action'],
            'channel': chosen['channel'],
            'reasoning': ' | '.join(reasoning),
            'details': {
                'information_type': information.get('type', 'unknown'),
                'time_sensitive': information.get('time_sensitive', False),
                'human_context': human_context
            }
        }
        
        # Calculate confidence
        confidence = self.calculate_confidence(information, human_context)
        
        # Log decision
        self.log_decision('communication', decision, confidence)
        
        return decision
    
    def estimate_communication_cost(self, context: Dict) -> float:
        """Estimate cost of interrupting human"""
        # Factors that increase cost:
        # - Late night/early morning
        # - Recent high communication volume
        # - Human marked as busy
        
        cost = 5.0  # Base cost
        
        # Time of day adjustment
        hour = datetime.now().hour
        if 22 <= hour or hour < 8:  # 10 PM - 8 AM
            cost += 3.0
        elif 9 <= hour <= 17:  # Business hours
            cost -= 1.0
        
        # Recent communication volume
        recent_msgs = context.get('recent_messages_count', 0)
        if recent_msgs > 10:
            cost += min(recent_msgs / 10, 3.0)  # Max +3
        
        # Human status
        if context.get('human_busy', False):
            cost += 2.0
        
        return max(1.0, min(10.0, cost))  # Clamp to 1-10 range
    
    def calculate_confidence(self, information: Dict, context: Dict) -> float:
        """Calculate confidence in communication decision"""
        confidence = 0.7  # Base confidence
        
        # Increase if we have good context
        if context.get('has_recent_interaction', False):
            confidence += 0.1
        
        if information.get('has_clear_urgency', False):
            confidence += 0.1
        
        # Decrease if during ambiguous times
        hour = datetime.now().hour
        if 7 <= hour <= 9 or 17 <= hour <= 19:  # Transition times
            confidence -= 0.1
        
        return max(0.3, min(1.0, confidence))  # Clamp to 0.3-1.0

class ErrorHandlingTree(DecisionTree):
    """
    Tree 3: Error Handling Protocol
    Decides how to handle different types of errors
    """
    
    def decide(self, error: Dict, system_context: Dict) -> Dict:
        """Decide error handling approach"""
        
        options = [
            {'name': 'Immediate alert + stop operations', 'action': 'stop', 'severity': 'critical'},
            {'name': 'Notify + offer alternatives', 'action': 'notify_alternatives', 'severity': 'high'},
            {'name': 'Fix automatically + document', 'action': 'auto_fix', 'severity': 'medium'},
            {'name': 'Log for review', 'action': 'log_only', 'severity': 'low'},
            {'name': 'Ignore (known non-issue)', 'action': 'ignore', 'severity': 'none'}
        ]
        
        reasoning = []
        chosen = None
        
        # Step 1: Is error safety-critical?
        if error.get('safety_critical', False):
            chosen = options[0]  # Immediate alert + stop
            reasoning.append("Error is safety-critical - immediate stop required")
        
        # Step 2: Can error be automatically fixed?
        elif error.get('can_auto_fix', False) and error.get('auto_fix_confidence', 0) > 0.8:
            chosen = options[2]  # Fix automatically
            reasoning.append(f"Error can be auto-fixed with high confidence ({error.get('auto_fix_confidence', 0):.0%})")
        
        # Step 3: Does error affect current outputs?
        elif error.get('affects_outputs', False):
            chosen = options[1]  # Notify + offer alternatives
            reasoning.append("Error affects current outputs - notify with alternatives")
        
        # Step 4: Is error known/expected?
        elif error.get('is_known_issue', False):
            chosen = options[3]  # Log for review
            reasoning.append("Error is known issue - log for periodic review")
        
        # Default: Log for review
        else:
            chosen = options[3]
            reasoning.append("Default: log error for review")
        
        decision = {
            'options': [opt['name'] for opt in options],
            'chosen': chosen['name'],
            'action': chosen['action'],
            'severity': chosen['severity'],
            'reasoning': ' | '.join(reasoning),
            'details': {
                'error_type': error.get('type', 'unknown'),
                'error_message': error.get('message', '')[:100],
                'system_context': system_context
            }
        }
        
        # Calculate confidence
        confidence = self.calculate_confidence(error, system_context)
        
        # Log decision
        self.log_decision('error_handling', decision, confidence)
        
        return decision
    
    def calculate_confidence(self, error: Dict, context: Dict) -> float:
        """Calculate confidence in error handling decision"""
        confidence = 0.8  # Base confidence for error handling
        
        # Increase if error is well-understood
        if error.get('has_known_solution', False):
            confidence += 0.1
        
        if context.get('similar_errors_handled', 0) > 0:
            confidence += min(context.get('similar_errors_handled', 0) * 0.05, 0.2)
        
        # Decrease if system is in unstable state
        if context.get('system_unstable', False):
            confidence -= 0.2
        
        return max(0.4, min(1.0, confidence))

class ResourceAllocationTree(DecisionTree):
    """
    Tree 4: Resource Allocation (Time/API)
    Decides how to allocate limited resources
    """
    
    def decide(self, tasks: List[Dict], resources: Dict) -> Dict:
        """Decide resource allocation among tasks"""
        
        # Generate allocation options
        options = self.generate_allocation_options(tasks, resources)
        
        reasoning = []
        
        # Step 1: Is any resource near exhaustion?
        near_exhaustion = any(
            resources.get(res, {}).get('usage_percent', 0) > 80
            for res in ['api_calls', 'time_minutes', 'memory_mb']
        )
        
        if near_exhaustion:
            # Conserve mode - only essential tasks
            chosen = self.select_conservative_allocation(tasks, resources)
            reasoning.append("Resources near exhaustion - conservative allocation")
        
        # Step 2: Multiple tasks competing?
        elif len(tasks) > 1:
            # Apply scoring matrix
            scored_tasks = self.score_tasks(tasks, resources)
            chosen = self.select_based_on_scores(scored_tasks, resources)
            reasoning.append("Multiple tasks competing - using scoring matrix")
        
        # Step 3: Can any task be deferred without loss?
        else:
            deferrable_tasks = [t for t in tasks if t.get('can_defer', True)]
            if deferrable_tasks:
                chosen = self.defer_tasks(deferrable_tasks, resources)
                reasoning.append("Tasks can be deferred - scheduling for later")
            else:
                chosen = self.execute_now(tasks, resources)
                reasoning.append("Tasks cannot be deferred - executing now")
        
        decision = {
            'options': [opt['description'] for opt in options],
            'chosen': chosen['description'],
            'allocation': chosen['allocation'],
            'reasoning': ' | '.join(reasoning),
            'details': {
                'task_count': len(tasks),
                'resource_status': resources,
                'allocation_strategy': chosen.get('strategy', 'unknown')
            }
        }
        
        # Calculate confidence
        confidence = self.calculate_confidence(tasks, resources, chosen)
        
        # Log decision
        self.log_decision('resource_allocation', decision, confidence)
        
        return decision
    
    def generate_allocation_options(self, tasks: List[Dict], resources: Dict) -> List[Dict]:
        """Generate possible allocation options"""
        options = []
        
        # Option 1: Equal allocation
        equal_allocation = {}
        for task in tasks:
            equal_allocation[task['id']] = resources.get('time_minutes', 60) / len(tasks)
        
        options.append({
            'description': 'Equal allocation among all tasks',
            'allocation': equal_allocation,
            'strategy': 'equal'
        })
        
        # Option 2: Priority-based allocation
        priority_allocation = {}
        total_priority = sum(task.get('priority_score', 5) for task in tasks)
        for task in tasks:
            share = task.get('priority_score', 5) / total_priority
            priority_allocation[task['id']] = resources.get('time_minutes', 60) * share
        
        options.append({
            'description': 'Priority-based allocation',
            'allocation': priority_allocation,
            'strategy': 'priority'
        })
        
        # Option 3: Sequential (one at a time)
        sequential_allocation = {}
        # Allocate full resources to highest priority task
        if tasks:
            highest_priority = max(tasks, key=lambda t: t.get('priority_score', 5))
            sequential_allocation[highest_priority['id']] = resources.get('time_minutes', 60)
            for task in tasks:
                if task['id'] != highest_priority['id']:
                    sequential_allocation[task