#!/usr/bin/env python3
"""
FalseMarkets API Adapter
Mock implementation that will be replaced with real API calls
"""

import json
import time
import random
from datetime import datetime
from typing import Dict, List, Any, Optional

class FalseMarketsAPI:
    """Mock API client for FalseMarkets platform"""
    
    def __init__(self, base_url: str = "http://localhost:3000/api"):
        self.base_url = base_url
        self.simulations = {}
        self.strategies = {}
        self._init_mock_data()
    
    def _init_mock_data(self):
        """Initialize mock data for testing"""
        # Mock strategies
        self.strategies = {
            "trend_following": {
                "id": "strategy_001",
                "name": "Trend Following",
                "type": "technical",
                "parameters": {
                    "lookback_period": 20,
                    "entry_threshold": 0.02,
                    "exit_threshold": -0.01
                },
                "performance": {
                    "sharpe_ratio": 1.2,
                    "max_drawdown": -0.15,
                    "win_rate": 0.58
                }
            },
            "mean_reversion": {
                "id": "strategy_002",
                "name": "Mean Reversion",
                "type": "statistical",
                "parameters": {
                    "lookback_period": 50,
                    "std_dev_threshold": 2.0,
                    "reversion_period": 5
                },
                "performance": {
                    "sharpe_ratio": 0.9,
                    "max_drawdown": -0.22,
                    "win_rate": 0.52
                }
            }
        }
        
        # Mock simulations
        self.simulations = {
            "sim_001": {
                "id": "sim_001",
                "name": "SPY Daily Simulation",
                "status": "completed",
                "start_date": "2026-02-15",
                "end_date": "2026-02-20",
                "symbols": ["SPY", "QQQ", "IWM"],
                "results": {
                    "total_return": 0.034,
                    "sharpe_ratio": 1.1,
                    "max_drawdown": -0.08,
                    "win_rate": 0.55
                }
            }
        }
    
    def start_simulation(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Start a new market simulation"""
        sim_id = f"sim_{len(self.simulations) + 1:03d}"
        
        simulation = {
            "id": sim_id,
            "name": config.get("name", f"Simulation {sim_id}"),
            "status": "running",
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": config.get("end_date"),
            "symbols": config.get("symbols", ["SPY"]),
            "strategies": config.get("strategies", []),
            "parameters": config.get("parameters", {}),
            "created_at": datetime.now().isoformat()
        }
        
        self.simulations[sim_id] = simulation
        
        # Simulate processing time
        time.sleep(0.5)
        
        return {
            "success": True,
            "simulation_id": sim_id,
            "message": f"Simulation {sim_id} started successfully"
        }
    
    def get_simulation_status(self, simulation_id: str) -> Dict[str, Any]:
        """Get status of a simulation"""
        if simulation_id not in self.simulations:
            return {
                "success": False,
                "error": f"Simulation {simulation_id} not found"
            }
        
        sim = self.simulations[simulation_id]
        
        # Simulate progress
        if sim["status"] == "running":
            # Randomly complete some simulations
            if random.random() > 0.7:
                sim["status"] = "completed"
                sim["results"] = {
                    "total_return": random.uniform(-0.05, 0.1),
                    "sharpe_ratio": random.uniform(0.5, 1.5),
                    "max_drawdown": random.uniform(-0.25, -0.05),
                    "win_rate": random.uniform(0.45, 0.65)
                }
        
        return {
            "success": True,
            "simulation": sim
        }
    
    def get_simulation_results(self, simulation_id: str) -> Dict[str, Any]:
        """Get results of a completed simulation"""
        if simulation_id not in self.simulations:
            return {
                "success": False,
                "error": f"Simulation {simulation_id} not found"
            }
        
        sim = self.simulations[simulation_id]
        
        if sim["status"] != "completed":
            return {
                "success": False,
                "error": f"Simulation {simulation_id} is not completed"
            }
        
        return {
            "success": True,
            "results": sim.get("results", {}),
            "metadata": {
                "id": sim["id"],
                "name": sim["name"],
                "duration": f"{random.randint(1, 24)} hours",
                "symbols": sim["symbols"]
            }
        }
    
    def evolve_strategy(self, strategy_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Evolve a strategy using evolutionary algorithms"""
        if strategy_id not in self.strategies:
            return {
                "success": False,
                "error": f"Strategy {strategy_id} not found"
            }
        
        original = self.strategies[strategy_id]
        
        # Create evolved version
        evolved_id = f"{strategy_id}_evolved_{int(time.time())}"
        
        # Mutate parameters slightly
        evolved_params = original["parameters"].copy()
        for key in evolved_params:
            if isinstance(evolved_params[key], (int, float)):
                # Apply small random mutation
                mutation = random.uniform(0.9, 1.1)
                evolved_params[key] = round(evolved_params[key] * mutation, 2)
        
        evolved_strategy = {
            "id": evolved_id,
            "name": f"Evolved {original['name']}",
            "type": original["type"],
            "parameters": evolved_params,
            "parent_id": strategy_id,
            "performance": {
                "sharpe_ratio": original["performance"]["sharpe_ratio"] * random.uniform(0.95, 1.05),
                "max_drawdown": original["performance"]["max_drawdown"] * random.uniform(0.95, 1.05),
                "win_rate": original["performance"]["win_rate"] * random.uniform(0.95, 1.05)
            }
        }
        
        self.strategies[evolved_id] = evolved_strategy
        
        return {
            "success": True,
            "evolved_strategy_id": evolved_id,
            "parameters": evolved_params,
            "improvement": random.uniform(-0.05, 0.15)  # Random improvement score
        }
    
    def get_available_strategies(self) -> Dict[str, Any]:
        """Get list of available strategies"""
        return {
            "success": True,
            "strategies": list(self.strategies.values()),
            "count": len(self.strategies)
        }
    
    def get_performance_metrics(self, timeframe: str = "daily") -> Dict[str, Any]:
        """Get performance metrics for analysis"""
        metrics = {
            "daily": {
                "simulations_run": random.randint(5, 20),
                "average_return": random.uniform(-0.01, 0.03),
                "best_strategy": random.choice(list(self.strategies.keys())),
                "evolution_cycles": random.randint(1, 5)
            },
            "weekly": {
                "simulations_run": random.randint(20, 100),
                "average_return": random.uniform(-0.02, 0.05),
                "strategy_improvement": random.uniform(0.01, 0.1),
                "success_rate": random.uniform(0.6, 0.9)
            }
        }
        
        return {
            "success": True,
            "timeframe": timeframe,
            "metrics": metrics.get(timeframe, {}),
            "timestamp": datetime.now().isoformat()
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        return {
            "success": True,
            "status": "healthy",
            "version": "1.0.0-mock",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "simulation_engine": "operational",
                "evolution_engine": "operational",
                "data_pipeline": "operational"
            }
        }


# Example usage
if __name__ == "__main__":
    api = FalseMarketsAPI()
    
    # Test health check
    print("Health Check:", json.dumps(api.health_check(), indent=2))
    
    # Test starting simulation
    config = {
        "name": "Test Simulation",
        "symbols": ["SPY", "QQQ"],
        "strategies": ["trend_following"],
        "parameters": {"duration_days": 30}
    }
    
    result = api.start_simulation(config)
    print("\nStart Simulation:", json.dumps(result, indent=2))
    
    # Test getting strategies
    strategies = api.get_available_strategies()
    print("\nAvailable Strategies:", json.dumps(strategies, indent=2))