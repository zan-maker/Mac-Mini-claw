#!/usr/bin/env python3
"""
Strategy Evolver Agent - Simple Version
Evolves trading strategies using genetic algorithms
"""

import json
import random
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("StrategyEvolver")

class StrategyEvolver:
    """Simple strategy evolver for FalseMarkets"""
    
    def __init__(self, data_dir: str = None):
        self.data_dir = Path(data_dir) if data_dir else Path(__file__).parent.parent / "data" / "evolution"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Evolution parameters
        self.population_size = 20  # Smaller for testing
        self.generations = 5       # Fewer for testing
        self.mutation_rate = 0.1
        self.elitism_count = 3
        
        logger.info(f"Strategy Evolver initialized. Data directory: {self.data_dir}")
    
    def create_random_strategy(self) -> Dict[str, Any]:
        """Create a random trading strategy"""
        strategy_types = ["trend_following", "mean_reversion", "breakout"]
        strategy_type = random.choice(strategy_types)
        
        # Strategy parameters based on type
        if strategy_type == "trend_following":
            params = {
                "lookback": random.randint(10, 50),
                "entry_threshold": round(random.uniform(0.01, 0.05), 3),
                "exit_threshold": round(random.uniform(-0.03, 0), 3),
                "position_size": round(random.uniform(0.05, 0.2), 2)
            }
        elif strategy_type == "mean_reversion":
            params = {
                "lookback": random.randint(5, 30),
                "std_dev_multiplier": round(random.uniform(1.5, 2.5), 1),
                "reversion_threshold": round(random.uniform(0.3, 0.8), 2),
                "position_size": round(random.uniform(0.05, 0.15), 2)
            }
        else:  # breakout
            params = {
                "consolidation_period": random.randint(10, 30),
                "breakout_threshold": round(random.uniform(0.015, 0.035), 3),
                "confirmation_bars": random.randint(1, 5),
                "position_size": round(random.uniform(0.05, 0.25), 2)
            }
        
        strategy_id = f"{strategy_type}_{datetime.now().strftime('%H%M%S')}_{random.randint(1000, 9999)}"
        
        return {
            "id": strategy_id,
            "name": f"{strategy_type.replace('_', ' ').title()} {strategy_id[-4:]}",
            "type": strategy_type,
            "parameters": params,
            "fitness": 0.0,
            "generation": 0,
            "created": datetime.now().isoformat()
        }
    
    def evaluate_fitness(self, strategy: Dict[str, Any]) -> float:
        """Evaluate strategy fitness (mock implementation)"""
        # In real system, this would run backtests
        # For now, use random fitness with some bias based on strategy type
        
        base_fitness = random.uniform(0.3, 0.8)
        
        # Adjust based on parameters (simple heuristics)
        params = strategy["parameters"]
        
        if strategy["type"] == "trend_following":
            # Prefer moderate lookback periods
            lookback_score = 1.0 - abs(params["lookback"] - 30) / 50
            fitness = base_fitness * 0.7 + lookback_score * 0.3
            
        elif strategy["type"] == "mean_reversion":
            # Prefer moderate std dev multipliers
            std_score = 1.0 - abs(params["std_dev_multiplier"] - 2.0) / 2.0
            fitness = base_fitness * 0.6 + std_score * 0.4
            
        else:  # breakout
            # Prefer moderate consolidation periods
            consolidation_score = 1.0 - abs(params["consolidation_period"] - 20) / 30
            fitness = base_fitness * 0.65 + consolidation_score * 0.35
        
        # Ensure fitness is between 0 and 1
        fitness = max(0.0, min(1.0, fitness))
        strategy["fitness"] = fitness
        
        return fitness
    
    def mutate_strategy(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create a mutated version of a strategy"""
        new_strategy = strategy.copy()
        new_strategy["id"] = f"{strategy['id']}_mutated_{datetime.now().strftime('%H%M%S')}"
        new_strategy["name"] = f"{strategy['name']} (Mutated)"
        new_strategy["generation"] = strategy["generation"] + 1
        new_strategy["created"] = datetime.now().isoformat()
        new_strategy["fitness"] = 0.0
        
        params = new_strategy["parameters"].copy()
        
        # Mutate each parameter with some probability
        for param_name in params:
            if random.random() < self.mutation_rate:
                current_value = params[param_name]
                
                if isinstance(current_value, int):
                    # Integer parameter
                    mutation = random.randint(-5, 5)
                    params[param_name] = max(1, current_value + mutation)
                else:
                    # Float parameter
                    mutation = random.uniform(-0.1, 0.1) * current_value
                    params[param_name] = max(0.01, current_value + mutation)
                    # Round to reasonable precision
                    if param_name in ["entry_threshold", "exit_threshold", "breakout_threshold"]:
                        params[param_name] = round(params[param_name], 3)
                    else:
                        params[param_name] = round(params[param_name], 2)
        
        new_strategy["parameters"] = params
        return new_strategy
    
    def run_evolution(self) -> Dict[str, Any]:
        """Run a complete evolution cycle"""
        logger.info("Starting strategy evolution")
        
        # Step 1: Create initial population
        logger.info("Creating initial population")
        population = []
        for i in range(self.population_size):
            strategy = self.create_random_strategy()
            self.evaluate_fitness(strategy)
            population.append(strategy)
        
        # Sort by fitness
        population.sort(key=lambda s: s["fitness"], reverse=True)
        
        evolution_history = []
        
        # Step 2: Run generations
        for gen in range(self.generations):
            logger.info(f"Generation {gen + 1}/{self.generations}")
            
            # Record generation stats
            gen_stats = {
                "generation": gen + 1,
                "best_fitness": population[0]["fitness"],
                "avg_fitness": sum(s["fitness"] for s in population) / len(population),
                "best_strategy": population[0]
            }
            evolution_history.append(gen_stats)
            
            # Create next generation
            next_generation = []
            
            # Elitism: keep best strategies
            for i in range(min(self.elitism_count, len(population))):
                elite = population[i].copy()
                elite["generation"] = gen + 1
                next_generation.append(elite)
            
            # Fill rest with mutations of best strategies
            while len(next_generation) < self.population_size:
                # Select a parent (biased toward better fitness)
                parent_idx = min(
                    int(random.triangular(0, len(population), 0)),
                    len(population) - 1
                )
                parent = population[parent_idx]
                
                # Create mutated child
                child = self.mutate_strategy(parent)
                self.evaluate_fitness(child)
                next_generation.append(child)
            
            population = next_generation
            population.sort(key=lambda s: s["fitness"], reverse=True)
            
            # Save generation data
            self._save_generation(gen + 1, population, gen_stats)
        
        # Step 3: Final results
        logger.info("Evolution completed")
        
        results = {
            "total_generations": self.generations,
            "best_strategy": population[0],
            "evolution_history": evolution_history,
            "population_stats": {
                "best_fitness": population[0]["fitness"],
                "avg_fitness": sum(s["fitness"] for s in population) / len(population),
                "strategy_types": {
                    "trend_following": len([s for s in population if s["type"] == "trend_following"]),
                    "mean_reversion": len([s for s in population if s["type"] == "mean_reversion"]),
                    "breakout": len([s for s in population if s["type"] == "breakout"])
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # Save final results
        self._save_results(results)
        
        return results
    
    def _save_generation(self, generation: int, population: List[Dict[str, Any]], stats: Dict[str, Any]):
        """Save generation data"""
        gen_dir = self.data_dir / f"gen_{generation:03d}"
        gen_dir.mkdir(exist_ok=True)
        
        # Save population
        with open(gen_dir / "population.json", 'w') as f:
            json.dump(population, f, indent=2)
        
        # Save stats
        with open(gen_dir / "stats.json", 'w') as f:
            json.dump(stats, f, indent=2)
    
    def _save_results(self, results: Dict[str, Any]):
        """Save final results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = self.data_dir / f"evolution_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Results saved to {results_file}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get evolver status"""
        return {
            "status": "ready",
            "population_size": self.population_size,
            "generations": self.generations,
            "mutation_rate": self.mutation_rate,
            "elitism_count": self.elitism_count,
            "data_directory": str(self.data_dir)
        }
    
    def run_weekly_workflow(self) -> Dict[str, Any]:
        """Run weekly evolution workflow"""
        logger.info("Running weekly evolution workflow")
        
        workflow = {
            "workflow": "weekly_strategy_evolution",
            "start_time": datetime.now().isoformat(),
            "steps": {}
        }
        
        try:
            # Step 1: Run evolution
            workflow["steps"]["evolution"] = {
                "status": "started",
                "timestamp": datetime.now().isoformat()
            }
            
            results = self.run_evolution()
            
            workflow["steps"]["evolution"]["status"] = "completed"
            workflow["steps"]["evolution"]["results"] = {
                "best_fitness": results["best_strategy"]["fitness"],
                "best_strategy_type": results["best_strategy"]["type"],
                "generations_completed": results["total_generations"]
            }
            
            # Step 2: Generate report
            workflow["steps"]["report"] = {
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "best_strategy": results["best_strategy"]["name"],
                    "fitness": results["best_strategy"]["fitness"],
                    "type": results["best_strategy"]["type"],
                    "key_parameters": results["best_strategy"]["parameters"]
                }
            }
            
            workflow["status"] = "completed"
            workflow["end_time"] = datetime.now().isoformat()
            
            # Save workflow results
            workflow_file = self.data_dir / f"weekly_workflow_{datetime.now().strftime('%Y%m%d')}.json"
            with open(workflow_file, 'w') as f:
                json.dump(workflow, f, indent=2)
            
            logger.info(f"Weekly workflow completed. Results saved to {workflow_file}")
            
        except Exception as e:
            logger.error(f"Weekly workflow failed: {e}")
            workflow["status"] = "failed"
            workflow["error"] = str(e)
            workflow["end_time"] = datetime.now().isoformat()
        
        return workflow