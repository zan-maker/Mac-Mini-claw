#!/usr/bin/env python3
"""
Strategy Evolver Agent
Evolves and optimizes trading strategies using genetic algorithms
"""

import json
import random
import logging
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("StrategyEvolverAgent")

class StrategyEvolverAgent:
    """Agent for evolving and optimizing trading strategies"""
    
    def __init__(self, api_adapter=None, data_dir: str = None):
        self.api = api_adapter
        self.data_dir = Path(data_dir) if data_dir else Path(__file__).parent.parent / "data" / "evolution"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Evolution parameters from config
        self.population_size = 50
        self.generations = 10
        self.mutation_rate = 0.1
        self.crossover_rate = 0.7
        self.elitism_count = 5
        
        # Strategy templates
        self.strategy_templates = self._load_strategy_templates()
        self.current_population = []
        self.generation_history = []
        
        logger.info(f"Strategy Evolver Agent initialized. Data directory: {self.data_dir}")
    
    def _load_strategy_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load strategy templates"""
        return {
            "trend_following": {
                "name": "Trend Following",
                "parameters": {
                    "lookback_period": {"min": 5, "max": 100, "step": 1},
                    "entry_threshold": {"min": 0.005, "max": 0.1, "step": 0.001},
                    "exit_threshold": {"min": -0.05, "max": 0, "step": 0.001},
                    "position_size": {"min": 0.01, "max": 0.5, "step": 0.01},
                    "stop_loss": {"min": 0.01, "max": 0.2, "step": 0.01},
                    "take_profit": {"min": 0.02, "max": 0.3, "step": 0.01}
                }
            },
            "mean_reversion": {
                "name": "Mean Reversion",
                "parameters": {
                    "lookback_period": {"min": 5, "max": 50, "step": 1},
                    "std_dev_multiplier": {"min": 1.0, "max": 3.0, "step": 0.1},
                    "reversion_threshold": {"min": 0.1, "max": 1.0, "step": 0.05},
                    "position_size": {"min": 0.01, "max": 0.5, "step": 0.01},
                    "stop_loss": {"min": 0.01, "max": 0.1, "step": 0.01},
                    "take_profit": {"min": 0.01, "max": 0.15, "step": 0.01}
                }
            },
            "breakout": {
                "name": "Breakout",
                "parameters": {
                    "consolidation_period": {"min": 5, "max": 50, "step": 1},
                    "breakout_threshold": {"min": 0.005, "max": 0.05, "step": 0.001},
                    "confirmation_period": {"min": 1, "max": 10, "step": 1},
                    "position_size": {"min": 0.01, "max": 0.5, "step": 0.01},
                    "stop_loss": {"min": 0.01, "max": 0.15, "step": 0.01},
                    "take_profit": {"min": 0.02, "max": 0.25, "step": 0.01}
                }
            }
        }
    
    def create_random_strategy(self, strategy_type: str = None) -> Dict[str, Any]:
        """Create a random strategy"""
        if strategy_type is None:
            strategy_type = random.choice(list(self.strategy_templates.keys()))
        
        template = self.strategy_templates[strategy_type]
        parameters = {}
        
        for param_name, param_config in template["parameters"].items():
            min_val = param_config["min"]
            max_val = param_config["max"]
            step = param_config.get("step", 0.01)
            
            # Generate random value within bounds
            value = random.uniform(min_val, max_val)
            if step > 0:
                value = round(value / step) * step
            
            parameters[param_name] = value
        
        strategy_id = hashlib.md5(
            f"{strategy_type}_{datetime.now().timestamp()}_{random.random()}".encode()
        ).hexdigest()[:8]
        
        return {
            "id": strategy_id,
            "name": f"{template['name']} {strategy_id}",
            "type": strategy_type,
            "parameters": parameters,
            "fitness": 0.0,
            "generation": 0,
            "created_at": datetime.now().isoformat(),
            "performance": {}
        }
    
    def create_initial_population(self) -> List[Dict[str, Any]]:
        """Create initial population of strategies"""
        logger.info(f"Creating initial population of size {self.population_size}")
        
        population = []
        for i in range(self.population_size):
            strategy = self.create_random_strategy()
            population.append(strategy)
        
        self.current_population = population
        return population
    
    def evaluate_strategy_fitness(self, strategy: Dict[str, Any], performance_data: Dict[str, float]) -> float:
        """Evaluate fitness of a strategy"""
        # Fitness calculation weights
        weights = {
            "total_return": 0.3,
            "sharpe_ratio": 0.25,
            "win_rate": 0.2,
            "profit_factor": 0.15,
            "max_drawdown": -0.1
        }
        
        fitness = 0.0
        
        for metric, weight in weights.items():
            if metric in performance_data:
                value = performance_data[metric]
                
                # Normalize values
                if metric == "max_drawdown":
                    normalized_value = 1.0 / (1.0 + abs(value))
                elif metric == "sharpe_ratio":
                    normalized_value = (value + 2.0) / 4.0
                elif metric == "total_return":
                    normalized_value = min(1.0, max(0.0, value / 1.0))
                elif metric == "win_rate":
                    normalized_value = value / 100.0
                elif metric == "profit_factor":
                    normalized_value = min(1.0, value / 5.0)
                else:
                    normalized_value = value
                
                fitness += weight * normalized_value
        
        # Ensure fitness is between 0 and 1
        fitness = max(0.0, min(1.0, fitness))
        
        strategy["fitness"] = fitness
        strategy["performance"] = performance_data
        strategy["last_tested"] = datetime.now().isoformat()
        
        return fitness
    
    def mutate_strategy(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Mutate a strategy"""
        strategy_type = strategy["type"]
        template = self.strategy_templates[strategy_type]
        
        mutated_params = strategy["parameters"].copy()
        
        for param_name, param_config in template["parameters"].items():
            if random.random() < self.mutation_rate:
                min_val = param_config["min"]
                max_val = param_config["max"]
                step = param_config.get("step", 0.01)
                
                # Add random mutation
                mutation_range = (max_val - min_val) * 0.1
                new_value = mutated_params[param_name] + random.uniform(-mutation_range, mutation_range)
                new_value = max(min_val, min(max_val, new_value))
                
                if step > 0:
                    new_value = round(new_value / step) * step
                
                mutated_params[param_name] = new_value
        
        new_id = hashlib.md5(
            f"{strategy['id']}_{datetime.now().timestamp()}".encode()
        ).hexdigest()[:8]
        
        return {
            "id": new_id,
            "name": f"{strategy['name']} (Mutated)",
            "type": strategy_type,
            "parameters": mutated_params,
            "fitness": 0.0,
            "generation": strategy.get("generation", 0) + 1,
            "created_at": datetime.now().isoformat(),
            "performance": {}
        }
    
    def crossover_strategies(self, parent1: Dict[str, Any], parent2: Dict[str, Any]) -> Dict[str, Any]:
        """Crossover two strategies"""
        if parent1["type"] != parent2["type"]:
            # If types differ, just mutate one parent
            return self.mutate_strategy(parent1)
        
        strategy_type = parent1["type"]
        template = self.strategy_templates[strategy_type]
        
        child_params = {}
        
        for param_name in template["parameters"]:
            if param_name in parent1["parameters"] and param_name in parent2["parameters"]:
                # Average crossover
                child_value = (parent1["parameters"][param_name] + parent2["parameters"][param_name]) / 2
                child_params[param_name] = child_value
        
        new_id = hashlib.md5(
            f"{parent1['id']}_{parent2['id']}_{datetime.now().timestamp()}".encode()
        ).hexdigest()[:8]
        
        return {
            "id": new_id,
            "name": f"Child of {parent1['name']} & {parent2['name']}",
            "type": strategy_type,
            "parameters": child_params,
            "fitness": 0.0,
            "generation": max(parent1.get("generation", 0), parent2.get("generation", 0)) + 1,
            "created_at": datetime.now().isoformat(),
            "performance": {}
        }
    
    def tournament_selection(self, tournament_size: int = 3) -> Dict[str, Any]:
        """Select a strategy using tournament selection"""
        if len(self.current_population) < tournament_size:
            tournament_size = len(self.current_population)
        
        tournament = random.sample(self.current_population, tournament_size)
        return max(tournament, key=lambda s: s["fitness"])
    
    def run_evolution_step(self, generation: int) -> Dict[str, Any]:
        """Run one evolution step/generation"""
        logger.info(f"Running evolution generation {generation}")
        
        # Evaluate fitness for any unevaluated strategies
        for strategy in self.current_population:
            if strategy["fitness"] == 0.0:
                # Generate random performance for demonstration
                performance_data = {
                    "total_return": random.uniform(-0.1, 0.3),
                    "sharpe_ratio": random.uniform(-1.0, 2.0),
                    "win_rate": random.uniform(40.0, 70.0),
                    "profit_factor": random.uniform(0.5, 3.0),
                    "max_drawdown": random.uniform(-0.15, -0.05)
                }
                self.evaluate_strategy_fitness(strategy, performance_data)
        
        # Sort by fitness
        self.current_population.sort(key=lambda s: s["fitness"], reverse=True)
        
        # Record generation stats
        gen_stats = {
            "generation": generation,
            "best_fitness": self.current_population[0]["fitness"],
            "avg_fitness": np.mean([s["fitness"] for s in self.current_population]),
            "worst_fitness": self.current_population[-1]["fitness"],
            "best_strategy": self.current_population[0]
        }
        
        self.generation_history.append(gen_stats)
        
        # Create next generation
        next_generation = []
        
        # Elitism: keep best strategies
        for i in range(min(self.elitism_count, len(self.current_population))):
            elite = self.current_population[i].copy()
            elite["generation"] = generation
            next_generation.append(elite)
        
        # Fill rest with crossover and mutation
        while len(next_generation) < self.population_size:
            if random.random() < self.crossover_rate and len(self.current_population) >= 2:
                # Crossover
                parent1 = self.tournament_selection()
                parent2 = self.tournament_selection()
                child = self.crossover_strategies(parent1, parent2)
                next_generation.append(child)
            else:
                # Mutation
                parent = self.tournament_selection()
                child = self.mutate_strategy(parent)
                next_generation.append(child)
        
        self.current_population = next_generation[:self.population_size]
        
        # Save generation data
        self._save_generation_data(generation)
        
        return gen_stats
    
    def run_evolution(self, generations: int = None) -> Dict[str, Any]:
        """Run complete evolution process"""
        if generations is None:
            generations = self.generations
        
        logger.info(f"Starting evolution with {generations} generations")
        
        if not self.current_population:
            self.create_initial_population()
        
        for gen in range(1, generations + 1):
            self.run_evolution_step(gen)
        
        # Final evaluation
        for strategy in self.current_population:
            if strategy["fitness"] == 0.0:
                performance_data = {
                    "total_return": random.uniform(-0.1, 0.3),
                    "sharpe_ratio": random.uniform(-1.0, 2.0),
                    "win_rate": random.uniform(40.0, 70.0),
                    "profit_factor": random.uniform(0.5, 3.0),
                    "max_drawdown": random.uniform(-0.15, -0.05)
                }
                self.evaluate_strategy_fitness(strategy, performance_data)
        
        self.current_population.sort(key=lambda s: s["fitness"], reverse=True)
        
        # Save final results
        results = {
            "total_generations": generations,
            "best_strategy": self.current_population[0],
            "evolution_history": self.generation_history,
            "final_population_stats": {
                "best_fitness": self.current_population[0]["fitness"],
                "avg_fitness": np.mean([s["fitness"] for s in self.current_population]),
                "worst_fitness": self.current_population[-1]["fitness"],
                "strategy_types": {
                    stype: len([s for s in self.current_population if s["type"] == stype])
                    for stype in self.strategy_templates.keys()
                }
            }
        }
        
        self._save_evolution_results(results)
        
        logger.info(f"Evolution completed. Best fitness: {results['final_population_stats']['best_fitness']:.4f}")
        return results
    
    def _save_generation_data(self, generation: int):
        """Save generation data to file"""
        gen_dir = self.data_dir / f"generation_{generation:03d}"
        gen_dir.mkdir(exist_ok=True)
        
        # Save population
        with open(gen_dir / "population.json", 'w') as f:
            json.dump(self.current_population, f, indent=2)
        
        # Save summary
        summary = {
            "generation": generation,
            "population_size": len(self.current_population),
            "best_fitness": self.current_population[0]["fitness"] if self.current_population else 0.0,
            "avg_fitness": np.mean([s["fitness"] for s in self.current_population]) if self.current_population else 0.0,
            "best_strategy_id": self.current_population[0]["id"] if self.current_population else "",
            "timestamp": datetime.now().isoformat()
        }
        
        with open(gen_dir / "summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
    
    def _save_evolution_results(self, results: Dict[str, Any]):
        """Save evolution results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = self.data_dir / f"evolution_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Evolution results saved to {results_file}")
    
    def get_best_strategies(self, count: int = 5) -> List[Dict[str, Any]]:
        """Get top N strategies from current population"""
        if not self.current_population:
            return []
        
        sorted_population = sorted(self.current_population, key=lambda s: s["fitness"], reverse=True)
        return sorted_population[:count]
    
    def run_weekly_evolution_workflow(self) -> Dict[str, Any]:
        """Run the complete weekly evolution workflow"""
        logger.info("Starting weekly evolution workflow")
        
        workflow_results = {
            "workflow": "weekly_strategy_evolution",
            "start_time": datetime.now().isoformat(),
            "steps": {}
        }
        
        try:
            # Step 1: Load previous best strategies
            logger.info("Step 1: Loading previous best strategies")
            previous_strategies = self._load_previous_best_strategies()
            workflow_results["steps"]["load_previous"] = {
                "count": len(previous_strategies),
                "status": "completed"
            }
            
            # Step 2: Create initial population
            logger