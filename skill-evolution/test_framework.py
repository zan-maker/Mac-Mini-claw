#!/usr/bin/env python3
"""
Test the Skill Evolution Framework with all agents
"""

import os
import sys
import json
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skill_evolution_agent import SkillEvolutionAgent, PerformanceTracker

def test_performance_tracker():
    """Test performance score calculation"""
    print("Testing Performance Tracker...")
    
    # Test Trade Recommender metrics
    trade_metrics = {
        'win_rate': 75.0,
        'avg_return': 2.5,
        'sharpe_ratio': 1.8,
        'max_drawdown': 15.0,
        'execution_speed': 2.5
    }
    
    trade_score = PerformanceTracker.calculate_score('trade-recommender', trade_metrics)
    print(f"  Trade Recommender Score: {trade_score:.2f}")
    
    # Test ROI Analyst metrics
    roi_metrics = {
        'accuracy': 88.0,
        'completeness': 92.0,
        'actionability': 85.0,
        'time_to_insight': 45.0
    }
    
    roi_score = PerformanceTracker.calculate_score('roi-analyst', roi_metrics)
    print(f"  ROI Analyst Score: {roi_score:.2f}")
    
    # Test Lead Generator metrics
    lead_metrics = {
        'response_rate': 25.0,
        'conversion_rate': 12.0,
        'lead_quality': 85.0,
        'enrichment_accuracy': 92.0
    }
    
    lead_score = PerformanceTracker.calculate_score('lead-generator', lead_metrics)
    print(f"  Lead Generator Score: {lead_score:.2f}")
    
    return trade_score > 0.5 and roi_score > 0.5 and lead_score > 0.5

def test_trade_recommender_evolution():
    """Test skill evolution for Trade Recommender"""
    print("\nTesting Trade Recommender Evolution...")
    
    # Create test directory
    test_dir = "/tmp/test_trade_evolution"
    os.makedirs(test_dir, exist_ok=True)
    
    # Create a sample skill file
    skill_content = """# Market Analysis Skill

## Purpose
Analyze stock market data and generate trading recommendations.

## Inputs
- symbol: Stock symbol
- timeframe: Analysis timeframe
- indicators: Technical indicators to use

## Outputs
- recommendation: BUY/SELL/HOLD
- confidence: Confidence score (0-1)
- target_price: Target price

## Strategy
Use technical analysis with RSI and MACD indicators.
"""
    
    skill_file = os.path.join(test_dir, "market_analysis.md")
    with open(skill_file, 'w') as f:
        f.write(skill_content)
    
    # Create evolution agent
    agent = SkillEvolutionAgent(agent_id='trade-recommender', skill_dir=test_dir)
    
    # Track some executions
    executions = [
        {
            'skill_name': 'market_analysis',
            'inputs': {'symbol': 'AAPL', 'timeframe': '1d', 'indicators': ['RSI', 'MACD']},
            'outputs': {'recommendation': 'BUY', 'confidence': 0.85, 'target_price': 185.50},
            'metrics': {'win_rate': 75.0, 'avg_return': 2.5, 'sharpe_ratio': 1.8, 'max_drawdown': 15.0, 'execution_speed': 2.5}
        },
        {
            'skill_name': 'market_analysis',
            'inputs': {'symbol': 'GOOGL', 'timeframe': '1w', 'indicators': ['RSI', 'Bollinger']},
            'outputs': {'recommendation': 'HOLD', 'confidence': 0.65, 'target_price': 152.30},
            'metrics': {'win_rate': 60.0, 'avg_return': 1.2, 'sharpe_ratio': 1.2, 'max_drawdown': 25.0, 'execution_speed': 3.0}
        }
    ]
    
    for exec_data in executions:
        record = agent.track_execution(**exec_data)
        print(f"  Tracked: {record.skill_name} for {exec_data['inputs']['symbol']} (Score: {record.success_score:.2f})")
    
    # Check patterns extracted
    patterns = agent.get_successful_patterns('market_analysis')
    print(f"  Patterns extracted: {len(patterns)}")
    
    # Evolve the skill
    evolved_path = agent.evolve_skill('market_analysis')
    
    if evolved_path and os.path.exists(evolved_path):
        print(f"  ✅ Skill evolved successfully: {evolved_path}")
        
        # Check evolution log
        evolution_log = agent.skill_evolution_log
        print(f"  Evolution log entries: {len(evolution_log)}")
        
        return True
    else:
        print(f"  ❌ Skill evolution failed")
        return False

def test_cross_agent_pattern_sharing():
    """Test pattern sharing between agents"""
    print("\nTesting Cross-Agent Pattern Sharing...")
    
    # Create test directories
    trade_dir = "/tmp/test_trade"
    roi_dir = "/tmp/test_roi"
    
    os.makedirs(trade_dir, exist_ok=True)
    os.makedirs(roi_dir, exist_ok=True)
    
    # Create agents
    trade_agent = SkillEvolutionAgent(agent_id='trade-recommender', skill_dir=trade_dir)
    roi_agent = SkillEvolutionAgent(agent_id='roi-analyst', skill_dir=roi_dir)
    
    # Add some patterns to trade agent
    trade_pattern = {
        'pattern_id': 'test_trade_pattern',
        'agent_id': 'trade-recommender',
        'skill_name': 'financial_analysis',
        'context': {'input_types': {'symbol': 'str', 'timeframe': 'str'}},
        'strategy': {'approach': 'technical', 'complexity': 'medium'},
        'success_score': 0.85,
        'timestamp': datetime.now().isoformat(),
        'frequency': 3,
        'source_agents': ['trade-recommender']
    }
    
    trade_agent.pattern_library.append(trade_pattern)
    trade_agent._save_json("pattern_library", trade_agent.pattern_library)
    
    # Share patterns
    shared_count = trade_agent.share_patterns(roi_agent)
    
    print(f"  Patterns shared: {shared_count}")
    print(f"  ROI Agent patterns after sharing: {len(roi_agent.pattern_library)}")
    
    return shared_count > 0

def test_evolution_report():
    """Test evolution report generation"""
    print("\nTesting Evolution Report...")
    
    test_dir = "/tmp/test_report"
    os.makedirs(test_dir, exist_ok=True)
    
    agent = SkillEvolutionAgent(agent_id='lead-generator', skill_dir=test_dir)
    
    # Add some execution history
    for i in range(5):
        exec_data = {
            'skill_name': f'skill_{i % 2}',
            'inputs': {'test': f'data_{i}'},
            'outputs': {'result': 'success'},
            'metrics': {'response_rate': 20.0 + i*5, 'conversion_rate': 10.0 + i*3}
        }
        agent.track_execution(**exec_data)
    
    # Generate report
    report = agent.get_evolution_report()
    
    print(f"  Agent ID: {report['agent_id']}")
    print(f"  Total executions: {report['total_executions']}")
    print(f"  Successful executions: {report['successful_executions']}")
    print(f"  Patterns extracted: {report['patterns_extracted']}")
    print(f"  Average success score: {report['avg_success_score']:.2f}")
    
    return len(report) > 0

def main():
    """Run all tests"""
    print("=" * 60)
    print("SKILL EVOLUTION FRAMEWORK TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Performance Tracker", test_performance_tracker),
        ("Trade Recommender Evolution", test_trade_recommender_evolution),
        ("Cross-Agent Pattern Sharing", test_cross_agent_pattern_sharing),
        ("Evolution Report", test_evolution_report)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            success = test_func()
            results.append((test_name, success))
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"  {status}")
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Skill Evolution Framework is ready.")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Review and fix issues.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
