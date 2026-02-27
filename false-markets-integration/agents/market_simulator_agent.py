#!/usr/bin/env python3
"""
Market Simulator Agent
Controls and manages market simulations in FalseMarkets
"""

import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("MarketSimulatorAgent")

class MarketSimulatorAgent:
    """Agent for controlling market simulations"""
    
    def __init__(self, api_adapter=None, data_dir: str = None):
        self.api = api_adapter
        self.data_dir = Path(data_dir) if data_dir else Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        
        # Simulation configurations
        self.simulation_configs = self._load_configs()
        self.active_simulations = {}
        
        logger.info(f"Market Simulator Agent initialized. Data directory: {self.data_dir}")
    
    def _load_configs(self) -> Dict[str, Any]:
        """Load simulation configurations"""
        config_file = self.data_dir / "simulation_configs.json"
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        
        # Default configurations
        default_configs = {
            "daily_quick": {
                "name": "Daily Quick Simulation",
                "symbols": ["SPY", "QQQ", "IWM"],
                "duration_days": 1,
                "timeframe": "1h",
                "strategies": ["trend_following", "mean_reversion"],
                "parameters": {
                    "initial_capital": 10000,
                    "commission": 0.001,
                    "slippage": 0.0005
                }
            },
            "weekly_comprehensive": {
                "name": "Weekly Comprehensive Simulation",
                "symbols": ["SPY", "QQQ", "IWM", "DIA", "VTI"],
                "duration_days": 5,
                "timeframe": "15m",
                "strategies": ["trend_following", "mean_reversion", "breakout", "momentum"],
                "parameters": {
                    "initial_capital": 50000,
                    "commission": 0.001,
                    "slippage": 0.0005,
                    "risk_per_trade": 0.02
                }
            },
            "monthly_backtest": {
                "name": "Monthly Backtest",
                "symbols": ["SPY"],
                "duration_days": 21,
                "timeframe": "1d",
                "strategies": ["trend_following"],
                "parameters": {
                    "initial_capital": 100000,
                    "commission": 0.001,
                    "slippage": 0.001
                }
            }
        }
        
        # Save default configs
        with open(config_file, 'w') as f:
            json.dump(default_configs, f, indent=2)
        
        return default_configs
    
    def start_daily_simulation(self) -> Dict[str, Any]:
        """Start the daily simulation routine"""
        logger.info("Starting daily simulation routine")
        
        config = self.simulation_configs.get("daily_quick")
        if not config:
            return {"success": False, "error": "Daily simulation config not found"}
        
        # Add timestamp to config
        config = config.copy()
        config["start_time"] = datetime.now().isoformat()
        config["end_date"] = (datetime.now() + timedelta(days=config["duration_days"])).strftime("%Y-%m-%d")
        
        # Start simulation via API
        if self.api:
            result = self.api.start_simulation(config)
            
            if result.get("success"):
                sim_id = result["simulation_id"]
                self.active_simulations[sim_id] = {
                    "id": sim_id,
                    "config": config,
                    "started_at": datetime.now().isoformat(),
                    "status": "running"
                }
                
                # Save simulation record
                self._save_simulation_record(sim_id, config)
                
                logger.info(f"Daily simulation started: {sim_id}")
                return {
                    "success": True,
                    "simulation_id": sim_id,
                    "config": config,
                    "message": f"Daily simulation {sim_id} started successfully"
                }
            else:
                logger.error(f"Failed to start simulation: {result.get('error')}")
                return result
        
        # Mock response if no API
        sim_id = f"sim_daily_{int(time.time())}"
        self.active_simulations[sim_id] = {
            "id": sim_id,
            "config": config,
            "started_at": datetime.now().isoformat(),
            "status": "running"
        }
        
        self._save_simulation_record(sim_id, config)
        
        logger.info(f"Mock daily simulation started: {sim_id}")
        return {
            "success": True,
            "simulation_id": sim_id,
            "config": config,
            "message": f"Mock daily simulation {sim_id} started"
        }
    
    def monitor_simulations(self) -> Dict[str, Any]:
        """Monitor active simulations"""
        logger.info(f"Monitoring {len(self.active_simulations)} active simulations")
        
        results = {}
        completed = []
        
        for sim_id, sim_data in list(self.active_simulations.items()):
            if self.api:
                status = self.api.get_simulation_status(sim_id)
                
                if status.get("success"):
                    sim_status = status["simulation"]["status"]
                    sim_data["status"] = sim_status
                    sim_data["last_check"] = datetime.now().isoformat()
                    
                    if sim_status == "completed":
                        # Get results
                        results_data = self.api.get_simulation_results(sim_id)
                        if results_data.get("success"):
                            sim_data["results"] = results_data["results"]
                            sim_data["completed_at"] = datetime.now().isoformat()
                            completed.append(sim_id)
                            
                            # Save results
                            self._save_simulation_results(sim_id, results_data["results"])
                    
                    results[sim_id] = sim_data
                else:
                    logger.warning(f"Failed to get status for {sim_id}: {status.get('error')}")
            else:
                # Mock completion
                sim_data["status"] = "completed"
                sim_data["results"] = {
                    "total_return": round(random.uniform(-0.02, 0.05), 4),
                    "sharpe_ratio": round(random.uniform(0.5, 1.5), 2),
                    "max_drawdown": round(random.uniform(-0.15, -0.05), 4),
                    "win_rate": round(random.uniform(0.45, 0.65), 2)
                }
                sim_data["completed_at"] = datetime.now().isoformat()
                completed.append(sim_id)
                
                self._save_simulation_results(sim_id, sim_data["results"])
                results[sim_id] = sim_data
        
        # Remove completed simulations
        for sim_id in completed:
            if sim_id in self.active_simulations:
                del self.active_simulations[sim_id]
        
        return {
            "success": True,
            "active_count": len(self.active_simulations),
            "completed_count": len(completed),
            "simulations": results
        }
    
    def generate_daily_report(self) -> Dict[str, Any]:
        """Generate daily simulation report"""
        logger.info("Generating daily simulation report")
        
        # Load today's simulations
        today = datetime.now().strftime("%Y-%m-%d")
        report_file = self.data_dir / f"reports/daily_{today}.json"
        report_file.parent.mkdir(exist_ok=True)
        
        simulations_today = []
        if report_file.exists():
            with open(report_file, 'r') as f:
                try:
                    data = json.load(f)
                    # Check if it's a list (old format) or dict (new format)
                    if isinstance(data, list):
                        simulations_today = data
                    elif isinstance(data, dict) and "simulations" in data:
                        simulations_today = data["simulations"]
                    else:
                        simulations_today = []
                except json.JSONDecodeError:
                    simulations_today = []
        
        # Get performance summary
        summary = {
            "date": today,
            "total_simulations": len(simulations_today),
            "average_return": 0.0,
            "best_simulation": None,
            "worst_simulation": None
        }
        
        if simulations_today:
            returns = []
            for sim in simulations_today:
                if isinstance(sim, dict):
                    results = sim.get("results", {})
                    if isinstance(results, dict):
                        returns.append(results.get("total_return", 0))
            
            if returns:
                summary["average_return"] = sum(returns) / len(returns)
                
                # Find best and worst
                best_idx = returns.index(max(returns))
                worst_idx = returns.index(min(returns))
                summary["best_simulation"] = simulations_today[best_idx].get("id")
                summary["worst_simulation"] = simulations_today[worst_idx].get("id")
        
        # Save report
        report = {
            "summary": summary,
            "simulations": simulations_today,
            "generated_at": datetime.now().isoformat()
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Daily report generated: {report_file}")
        return {
            "success": True,
            "report": report,
            "report_path": str(report_file)
        }
    
    def _save_simulation_record(self, sim_id: str, config: Dict[str, Any]):
        """Save simulation record to file"""
        record_file = self.data_dir / f"simulations/{sim_id}.json"
        record_file.parent.mkdir(exist_ok=True)
        
        record = {
            "id": sim_id,
            "config": config,
            "started_at": datetime.now().isoformat(),
            "status": "running"
        }
        
        with open(record_file, 'w') as f:
            json.dump(record, f, indent=2)
    
    def _save_simulation_results(self, sim_id: str, results: Dict[str, Any]):
        """Save simulation results to file"""
        # Update simulation record
        record_file = self.data_dir / f"simulations/{sim_id}.json"
        if record_file.exists():
            with open(record_file, 'r') as f:
                record = json.load(f)
            
            record["status"] = "completed"
            record["completed_at"] = datetime.now().isoformat()
            record["results"] = results
            
            with open(record_file, 'w') as f:
                json.dump(record, f, indent=2)
        
        # Add to today's simulations list
        today = datetime.now().strftime("%Y-%m-%d")
        today_file = self.data_dir / f"reports/daily_{today}.json"
        today_file.parent.mkdir(exist_ok=True)
        
        simulations_today = []
        if today_file.exists():
            with open(today_file, 'r') as f:
                simulations_today = json.load(f)
        
        simulations_today.append({
            "id": sim_id,
            "completed_at": datetime.now().isoformat(),
            "results": results
        })
        
        with open(today_file, 'w') as f:
            json.dump(simulations_today, f, indent=2)
    
    def get_performance_stats(self, days: int = 7) -> Dict[str, Any]:
        """Get performance statistics for the last N days"""
        logger.info(f"Getting performance stats for last {days} days")
        
        stats = {
            "period_days": days,
            "total_simulations": 0,
            "average_return": 0.0,
            "positive_days": 0,
            "simulations_by_day": {}
        }
        
        all_returns = []
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            report_file = self.data_dir / f"reports/daily_{date}.json"
            
            if report_file.exists():
                with open(report_file, 'r') as f:
                    try:
                        data = json.load(f)
                        
                        # Handle both formats: list or dict with simulations key
                        if isinstance(data, list):
                            simulations = data
                        elif isinstance(data, dict) and "simulations" in data:
                            simulations = data["simulations"]
                        else:
                            simulations = []
                        
                        if isinstance(simulations, list):
                            day_returns = []
                            for sim in simulations:
                                if isinstance(sim, dict):
                                    results = sim.get("results", {})
                                    if isinstance(results, dict):
                                        day_returns.append(results.get("total_return", 0))
                            
                            if day_returns:
                                day_avg = sum(day_returns) / len(day_returns)
                                stats["simulations_by_day"][date] = {
                                    "count": len(simulations),
                                    "average_return": day_avg,
                                    "positive": day_avg > 0
                                }
                                
                                stats["total_simulations"] += len(simulations)
                                all_returns.extend(day_returns)
                                
                                if day_avg > 0:
                                    stats["positive_days"] += 1
                    except json.JSONDecodeError:
                        logger.warning(f"Could not parse report file: {report_file}")
                        continue
        
        if all_returns:
            stats["average_return"] = sum(all_returns) / len(all_returns)
            stats["success_rate"] = stats["positive_days"] / days if days > 0 else 0
        
        return {
            "success": True,
            "stats": stats,
            "generated_at": datetime.now().isoformat()
        }


# Example usage
if __name__ == "__main__":
    import random  # Import here to avoid circular import
    
    # Create mock API adapter
    from adapters.falsemarkets_api import FalseMarketsAPI
    
    api = FalseMarketsAPI()
    agent = MarketSimulatorAgent(api_adapter=api)
    
    # Test daily simulation
    print("Starting daily simulation...")
    result = agent.start_daily_simulation()
    print("Start Result:", json.dumps(result, indent=2))
    
    # Test monitoring
    print("\nMonitoring simulations...")
    monitor_result = agent.monitor_simulations()
    print("Monitor Result:", json.dumps(monitor_result, indent=2))
    
    # Test report generation
    print("\nGenerating daily report...")
    report_result = agent.generate_daily_report()
    print("Report Result:", json.dumps(report_result, indent=2))
    
    # Test performance stats
    print("\nGetting performance stats...")
    stats_result = agent.get_performance_stats(days=3)
    print("Stats Result:", json.dumps(stats_result, indent=2))