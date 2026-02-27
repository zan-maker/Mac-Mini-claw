#!/usr/bin/env python3
"""
Trust Protocol Compliance Monitor
Hourly monitoring to ensure adherence to established principles
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import re

class TrustMonitor:
    """Monitor trust protocol compliance"""
    
    def __init__(self):
        self.workspace = Path("/Users/cubiczan/.openclaw/workspace")
        self.protocol_path = self.workspace / "TRUST_PROTOCOL.md"
        self.log_dir = self.workspace / "logs" / "trust"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Compliance log paths
        self.compliance_log = self.log_dir / "compliance.json"
        self.decisions_log = self.log_dir / "decisions.json"
        self.violations_log = self.log_dir / "violations.json"
        
        # Initialize logs if they don't exist
        self.init_logs()
        
        # Timezone for quiet hours (EST)
        self.quiet_start = 22  # 10 PM
        self.quiet_end = 8     # 8 AM
        
    def init_logs(self):
        """Initialize log files if they don't exist"""
        logs = [
            (self.compliance_log, []),
            (self.decisions_log, []),
            (self.violations_log, [])
        ]
        
        for log_path, default in logs:
            if not log_path.exists():
                with open(log_path, 'w') as f:
                    json.dump(default, f, indent=2)
    
    def get_current_hour(self):
        """Get current hour in EST"""
        # Simple implementation - in production would use timezone conversion
        return datetime.now().hour
    
    def is_quiet_hours(self):
        """Check if current time is during quiet hours"""
        hour = self.get_current_hour()
        return hour >= self.quiet_start or hour < self.quiet_end
    
    def check_communication_cadence(self, recent_messages=None):
        """Check communication follows protocol"""
        violations = []
        
        # Check 1: No urgent messages during quiet hours (unless critical)
        if self.is_quiet_hours():
            # Check recent messages for urgency violations
            if recent_messages:
                for msg in recent_messages:
                    if msg.get('urgency') == 'high' and not msg.get('critical'):
                        violations.append({
                            'type': 'quiet_hours_violation',
                            'message': f"High urgency message during quiet hours: {msg.get('content', '')[:50]}...",
                            'timestamp': datetime.now().isoformat()
                        })
        
        # Check 2: Appropriate channel usage
        # This would check Discord message logs in production
        
        return {
            'passed': len(violations) == 0,
            'violations': violations,
            'quiet_hours': self.is_quiet_hours(),
            'current_hour': self.get_current_hour()
        }
    
    def check_decision_transparency(self, limit_hours=24):
        """Check recent decisions for transparency"""
        try:
            with open(self.decisions_log, 'r') as f:
                decisions = json.load(f)
            
            # Filter recent decisions
            cutoff = datetime.now() - timedelta(hours=limit_hours)
            recent_decisions = []
            
            for decision in decisions[-50:]:  # Check last 50 decisions
                try:
                    decision_time = datetime.fromisoformat(decision.get('timestamp', ''))
                    if decision_time >= cutoff:
                        recent_decisions.append(decision)
                except:
                    continue
            
            # Analyze transparency
            transparent_count = 0
            violations = []
            
            for decision in recent_decisions:
                has_reasoning = bool(decision.get('reasoning'))
                has_score = decision.get('score') is not None
                has_options = bool(decision.get('options'))
                
                if has_reasoning and has_score and has_options:
                    transparent_count += 1
                else:
                    violations.append({
                        'type': 'transparency_violation',
                        'decision_id': decision.get('id', 'unknown'),
                        'missing': [],
                        'timestamp': decision.get('timestamp')
                    })
                    if not has_reasoning:
                        violations[-1]['missing'].append('reasoning')
                    if not has_score:
                        violations[-1]['missing'].append('score')
                    if not has_options:
                        violations[-1]['missing'].append('options')
            
            total = len(recent_decisions)
            transparency_rate = transparent_count / total if total > 0 else 1.0
            
            return {
                'passed': transparency_rate >= 0.8,  # 80% threshold
                'transparency_rate': transparency_rate,
                'recent_decisions': total,
                'transparent_decisions': transparent_count,
                'violations': violations
            }
            
        except Exception as e:
            return {
                'passed': False,
                'error': str(e),
                'transparency_rate': 0,
                'recent_decisions': 0,
                'transparent_decisions': 0,
                'violations': [{'type': 'log_error', 'error': str(e)}]
            }
    
    def check_safety_compliance(self):
        """Check for unapproved high-risk actions"""
        # This would check system logs for actions requiring approval
        # For now, we'll check a simulated log
        
        safety_log_path = self.log_dir / "safety_actions.json"
        if not safety_log_path.exists():
            return {
                'passed': True,
                'unapproved_actions': 0,
                'total_actions': 0,
                'violations': []
            }
        
        try:
            with open(safety_log_path, 'r') as f:
                safety_log = json.load(f)
            
            # Check last 24 hours
            cutoff = datetime.now() - timedelta(hours=24)
            recent_actions = []
            unapproved = []
            
            for action in safety_log[-100:]:
                try:
                    action_time = datetime.fromisoformat(action.get('timestamp', ''))
                    if action_time >= cutoff:
                        recent_actions.append(action)
                        if action.get('requires_approval') and not action.get('approved'):
                            unapproved.append(action)
                except:
                    continue
            
            return {
                'passed': len(unapproved) == 0,
                'unapproved_actions': len(unapproved),
                'total_actions': len(recent_actions),
                'violations': unapproved
            }
            
        except Exception as e:
            return {
                'passed': False,
                'error': str(e),
                'unapproved_actions': 0,
                'total_actions': 0,
                'violations': [{'type': 'safety_log_error', 'error': str(e)}]
            }
    
    def calculate_compliance_score(self, checks):
        """Calculate overall compliance score"""
        weights = {
            'communication': 0.3,
            'transparency': 0.4,
            'safety': 0.3
        }
        
        score = 0
        for check_name, check_result in checks.items():
            if check_result.get('passed', False):
                score += weights.get(check_name, 0)
            else:
                # Partial credit for transparency rate
                if check_name == 'transparency':
                    transparency_rate = check_result.get('transparency_rate', 0)
                    score += weights['transparency'] * transparency_rate
        
        return round(score, 3)
    
    def log_decision(self, decision_type, options, chosen, reasoning, score=None):
        """Log a decision with transparency"""
        options_str = str(options)
        hash_val = abs(hash(options_str))
        decision_id = f"dec_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash_val % 100000000:08d}"
        
        decision = {
            'id': decision_id,
            'timestamp': datetime.now().isoformat(),
            'type': decision_type,
            'options': options,
            'chosen': chosen,
            'reasoning': reasoning,
            'score': score,
            'protocol_version': '1.0'
        }
        
        # Load existing decisions
        try:
            with open(self.decisions_log, 'r') as f:
                decisions = json.load(f)
        except:
            decisions = []
        
        # Add new decision
        decisions.append(decision)
        
        # Keep only last 1000 decisions
        if len(decisions) > 1000:
            decisions = decisions[-1000:]
        
        # Save
        with open(self.decisions_log, 'w') as f:
            json.dump(decisions, f, indent=2)
        
        # If score is low, flag for review
        if score is not None and score < 0.6:
            self.flag_for_review(decision)
        
        return decision_id
    
    def flag_for_review(self, decision):
        """Flag a decision for human review"""
        try:
            with open(self.violations_log, 'r') as f:
                violations = json.load(f)
        except:
            violations = []
        
        violation = {
            'type': 'low_confidence_decision',
            'decision': decision,
            'timestamp': datetime.now().isoformat(),
            'action': 'flag_for_review'
        }
        
        violations.append(violation)
        
        with open(self.violations_log, 'w') as f:
            json.dump(violations, f, indent=2)
        
        print(f"⚠️ Decision flagged for review: {decision['id']} (score: {decision.get('score', 'N/A')})")
    
    def run_compliance_check(self):
        """Run full compliance check"""
        print(f"[{datetime.now()}] Running Trust Protocol Compliance Check")
        
        # Run all checks
        checks = {
            'communication': self.check_communication_cadence(),
            'transparency': self.check_decision_transparency(),
            'safety': self.check_safety_compliance()
        }
        
        # Calculate overall score
        compliance_score = self.calculate_compliance_score(checks)
        
        # Generate report
        report = {
            'timestamp': datetime.now().isoformat(),
            'compliance_score': compliance_score,
            'checks': checks,
            'quiet_hours': self.is_quiet_hours(),
            'protocol_version': '1.0'
        }
        
        # Save compliance log
        try:
            with open(self.compliance_log, 'r') as f:
                compliance_history = json.load(f)
        except:
            compliance_history = []
        
        compliance_history.append(report)
        
        # Keep only last 720 entries (30 days of hourly checks)
        if len(compliance_history) > 720:
            compliance_history = compliance_history[-720:]
        
        with open(self.compliance_log, 'w') as f:
            json.dump(compliance_history, f, indent=2)
        
        # Print summary
        print(f"📊 Compliance Score: {compliance_score:.1%}")
        for check_name, check_result in checks.items():
            status = "✅ PASS" if check_result.get('passed', False) else "❌ FAIL"
            print(f"   {check_name}: {status}")
            
            if check_result.get('violations'):
                print(f"     Violations: {len(check_result['violations'])}")
        
        # Trigger alert if score is low
        if compliance_score < 0.8:
            self.trigger_alert(f"Low compliance score: {compliance_score:.1%}")
        
        return report
    
    def trigger_alert(self, message):
        """Trigger alert for low compliance"""
        alert = {
            'type': 'compliance_alert',
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'severity': 'medium'
        }
        
        alert_path = self.log_dir / "alerts.json"
        try:
            with open(alert_path, 'r') as f:
                alerts = json.load(f)
        except:
            alerts = []
        
        alerts.append(alert)
        
        with open(alert_path, 'w') as f:
            json.dump(alerts, f, indent=2)
        
        print(f"🚨 ALERT: {message}")
        
        # In production, this would send to Discord/email
        # For now, just log
        
    def generate_daily_report(self):
        """Generate daily compliance report"""
        try:
            with open(self.compliance_log, 'r') as f:
                compliance_history = json.load(f)
        except:
            compliance_history = []
        
        # Get last 24 hours
        cutoff = datetime.now() - timedelta(hours=24)
        recent_checks = []
        
        for check in compliance_history[-24:]:  # Last 24 entries (hourly)
            try:
                check_time = datetime.fromisoformat(check.get('timestamp', ''))
                if check_time >= cutoff:
                    recent_checks.append(check)
            except:
                continue
        
        if not recent_checks:
            return None
        
        # Calculate daily averages
        scores = [c.get('compliance_score', 0) for c in recent_checks]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Count violations
        total_violations = 0
        for check in recent_checks:
            for check_name, check_result in check.get('checks', {}).items():
                total_violations += len(check_result.get('violations', []))
        
        report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'period': '24h',
            'average_compliance_score': round(avg_score, 3),
            'checks_analyzed': len(recent_checks),
            'total_violations': total_violations,
            'quiet_hours_violations': sum(1 for c in recent_checks if c.get('quiet_hours', False)),
            'recommendations': self.generate_recommendations(recent_checks)
        }
        
        # Save daily report
        report_path = self.log_dir / f"daily_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def generate_recommendations(self, recent_checks):
        """Generate recommendations based on compliance data"""
        recommendations = []
        
        # Analyze patterns
        low_scores = [c for c in recent_checks if c.get('compliance_score', 0) < 0.8]
        
        if low_scores:
            recommendations.append({
                'priority': 'high',
                'action': 'Review trust protocol adherence',
                'reason': f'{len(low_scores)} checks below 80% compliance'
            })
        
        # Check for recurring violation types
        violation_types = {}
        for check in recent_checks:
            for check_name, check_result in check.get('checks', {}).items():
                for violation in check_result.get('violations', []):
                    v_type = violation.get('type', 'unknown')
                    violation_types[v_type] = violation_types.get(v_type, 0) + 1
        
        for v_type, count in violation_types.items():
            if count >= 3:  # Recurring issue
                recommendations.append({
                    'priority': 'medium',
                    'action': f'Address recurring {v_type} violations',
                    'reason': f'{count} occurrences in last 24h'
                })
        
        return recommendations
    
    def run(self, check_type='full'):
        """Main execution method"""
        if check_type == 'full':
            return self.run_compliance_check()
        elif check_type == 'daily_report':
            return self.generate_daily_report()
        else:
            print(f"Unknown check type: {check_type}")
            return None

def main():
    """Command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Trust Protocol Compliance Monitor")
    parser.add_argument('--check', choices=['full', 'daily'], default='full',
                       help='Type of check to run')
    parser.add_argument('--log-decision', action='store_true',
                       help='Log a decision (for testing)')
    
    args = parser.parse_args()
    
    monitor = TrustMonitor()
    
    if args.log_decision:
        # Example decision logging
        decision_id = monitor.log_decision(
            decision_type='prioritization',
            options=['Fix API issue', 'Add new feature', 'Run tests'],
            chosen='Fix API issue',
            reasoning='API issue affects multiple systems and has highest impact',
            score=0.85
        )
        print(f"Logged decision: {decision_id}")
    
    elif args.check == 'full':
        report = monitor.run_compliance_check()
        if report:
            print(f"\n📋 Compliance Report Generated")
            print(f"   Score: {report['compliance_score']:.1%}")
            print(f"   Log: {monitor.compliance_log}")
    
    elif args.check == 'daily':
        report = monitor.generate_daily_report()
        if report:
            print(f"\n📅 Daily Compliance Report")
            print(f"   Date: {report['date']}")
            print(f"   Avg Score: {report['average_compliance_score']:.1%}")
            print(f"   Violations: {report['total_violations']}")
            if report['recommendations']:
                print(f"\n   Recommendations:")
                for rec in report['recommendations']:
                    print(f"   • [{rec['priority'].upper()}] {rec['action']}")

if __name__ == "__main__":
    main()