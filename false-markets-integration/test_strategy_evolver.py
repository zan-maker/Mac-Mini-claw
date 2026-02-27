#!/usr/bin/env python3
"""
Test script for Strategy Evolver Agent
"""

import sys
from pathlib import Path

# Add the agents directory to the path
sys.path.insert(0, str(Path(__file__).parent / "agents"))

from strategy_evolver_simple import StrategyEvolver

def test_strategy_evolver():
    """Test the Strategy Evolver agent"""
    print("🧬 Testing Strategy Evolver Agent...")
    
    # Initialize evolver
    evolver = StrategyEvolver()
    
    # Test 1: Get status
    print("\n1. Getting evolver status...")
    status = evolver.get_status()
    print(f"   Status: {status['status']}")
    print(f"   Population size: {status['population_size']}")
    print(f"   Generations: {status['generations']}")
    
    # Test 2: Create random strategy
    print("\n2. Creating random strategy...")
    strategy = evolver.create_random_strategy()
    print(f"   Strategy ID: {strategy['id']}")
    print(f"   Type: {strategy['type']}")
    print(f"   Parameters: {strategy['parameters']}")
    
    # Test 3: Evaluate fitness
    print("\n3. Evaluating strategy fitness...")
    fitness = evolver.evaluate_fitness(strategy)
    print(f"   Fitness: {fitness:.4f}")
    
    # Test 4: Mutate strategy
    print("\n4. Mutating strategy...")
    mutated = evolver.mutate_strategy(strategy)
    print(f"   Mutated ID: {mutated['id']}")
    print(f"   Generation: {mutated['generation']}")
    print(f"   Parameters: {mutated['parameters']}")
    
    # Test 5: Run evolution
    print("\n5. Running evolution...")
    results = evolver.run_evolution()
    
    print(f"   Generations completed: {results['total_generations']}")
    print(f"   Best fitness: {results['best_strategy']['fitness']:.4f}")
    print(f"   Best strategy type: {results['best_strategy']['type']}")
    print(f"   Best strategy parameters: {results['best_strategy']['parameters']}")
    
    # Test 6: Run weekly workflow
    print("\n6. Running weekly workflow...")
    workflow = evolver.run_weekly_workflow()
    
    print(f"   Workflow status: {workflow['status']}")
    if workflow['status'] == 'completed':
        print(f"   Best fitness: {workflow['steps']['evolution']['results']['best_fitness']:.4f}")
        print(f"   Best type: {workflow['steps']['evolution']['results']['best_strategy_type']}")
    
    print("\n✅ Strategy Evolver tests completed successfully!")
    return True

if __name__ == "__main__":
    try:
        test_strategy_evolver()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)