#!/usr/bin/env python3
"""
FalseMarkets Integration Orchestrator
Main controller for the FalseMarkets integration system
"""

import json
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("FalseMarketsOrchestrator")

class FalseMarketsOrchestrator:
    """Main orchestrator for FalseMarkets integration"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.agents = {}
        self.workflows = {}
        self._initialize_system()
        
        logger.info("FalseMarkets Orchestrator initialized")
    
    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """Load configuration file"""
        if config_path is None:
            config_path = Path(__file__).parent / "config" / "integration_config.json"
        else:
            config_path = Path(config_path)
        
        if not config_path.exists():
            logger.error(f"Configuration file not found: {config_path}")
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        logger.info(f"Configuration loaded from {config_path}")
        return config
    
    def _initialize_system(self):
        """Initialize the integration system"""
        logger.info("Initializing FalseMarkets integration system...")
        
        # Create data directories
        data_dirs = self.config["openclaw_integration"]["data_storage"]
        for dir_name, dir_path in data_dirs.items():
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created/verified directory: {dir_path}")
        
        # Initialize API adapter
        try:
            from adapters.falsemarkets_api import FalseMarketsAPI
            
            api_config = self.config["falsemarkets"]["api"]
            self.api = FalseMarketsAPI(base_url=api_config["base_url"])
            
            # Test API connection
            health = self.api.health_check()
            if health.get("success"):
                logger.info(f"API connection established: {health['status']}")
            else:
                logger.warning("API connection test failed, using mock mode")
        except ImportError as e:
            logger.warning(f"Could not import API adapter: {e}. Using mock mode.")
            self.api = None
        
        # Initialize agents
        self._initialize_agents()
        
        logger.info("System initialization complete")
    
    def _initialize_agents(self):
        """Initialize all agents"""
        logger.info("Initializing agents...")
        
        agent_configs = self.config["openclaw_integration"]["agents"]
        
        # Market Simulator Agent
        if agent_configs["market_simulator"]["enabled"]:
            try:
                from agents.market_simulator_agent import MarketSimulatorAgent
                
                data_dir = self.config["openclaw_integration"]["data_storage"]["simulation_results"]
                self.agents["market_simulator"] = MarketSimulatorAgent(
                    api_adapter=self.api,
                    data_dir=data_dir
                )
                logger.info("Market Simulator Agent initialized")
            except ImportError as e:
                logger.error(f"Failed to initialize Market Simulator Agent: {e}")
        
        # Strategy Evolver Agent
        if agent_configs["strategy_evolver"]["enabled"]:
            try:
                from agents.strategy_evolver_simple import StrategyEvolver
                
                data_dir = self.config["openclaw_integration"]["data_storage"]["evolution_logs"]
                self.agents["strategy_evolver"] = StrategyEvolver(data_dir=data_dir)
                logger.info("Strategy Evolver Agent initialized")
            except ImportError as e:
                logger.error(f"Failed to initialize Strategy Evolver Agent: {e}")
        
        # TODO: Initialize other agents as they are implemented
        # - Performance Analyst Agent
        # - Dashboard Manager Agent
        
        logger.info(f"Total agents initialized: {len(self.agents)}")
    
    def run_daily_workflow(self) -> Dict[str, Any]:
        """Execute the daily workflow"""
        logger.info("Starting daily workflow...")
        
        workflow_start = datetime.now()
        results = {
            "workflow": "daily",
            "start_time": workflow_start.isoformat(),
            "steps": {},
            "success": True,
            "errors": []
        }
        
        # Step 1: Market Simulation
        if "market_simulator" in self.agents:
            logger.info("Step 1: Running market simulation...")
            try:
                sim_result = self.agents["market_simulator"].start_daily_simulation()
                results["steps"]["market_simulation"] = {
                    "success": sim_result.get("success", False),
                    "simulation_id": sim_result.get("simulation_id"),
                    "message": sim_result.get("message")
                }
                
                if not sim_result.get("success"):
                    results["success"] = False
                    results["errors"].append(f"Market simulation failed: {sim_result.get('error')}")
            except Exception as e:
                logger.error(f"Market simulation error: {e}")
                results["steps"]["market_simulation"] = {"success": False, "error": str(e)}
                results["success"] = False
                results["errors"].append(f"Market simulation exception: {e}")
        
        # Step 2: Monitor simulations
        if "market_simulator" in self.agents:
            logger.info("Step 2: Monitoring simulations...")
            try:
                monitor_result = self.agents["market_simulator"].monitor_simulations()
                results["steps"]["simulation_monitoring"] = {
                    "success": monitor_result.get("success", False),
                    "active_count": monitor_result.get("active_count", 0),
                    "completed_count": monitor_result.get("completed_count", 0)
                }
            except Exception as e:
                logger.error(f"Simulation monitoring error: {e}")
                results["steps"]["simulation_monitoring"] = {"success": False, "error": str(e)}
        
        # Step 3: Generate daily report
        if "market_simulator" in self.agents:
            logger.info("Step 3: Generating daily report...")
            try:
                report_result = self.agents["market_simulator"].generate_daily_report()
                results["steps"]["report_generation"] = {
                    "success": report_result.get("success", False),
                    "report_path": report_result.get("report_path")
                }
            except Exception as e:
                logger.error(f"Report generation error: {e}")
                results["steps"]["report_generation"] = {"success": False, "error": str(e)}
        
        # Step 4: Get performance stats
        if "market_simulator" in self.agents:
            logger.info("Step 4: Calculating performance stats...")
            try:
                stats_result = self.agents["market_simulator"].get_performance_stats(days=7)
                results["steps"]["performance_stats"] = {
                    "success": stats_result.get("success", False),
                    "average_return": stats_result.get("stats", {}).get("average_return", 0),
                    "success_rate": stats_result.get("stats", {}).get("success_rate", 0)
                }
            except Exception as e:
                logger.error(f"Performance stats error: {e}")
                results["steps"]["performance_stats"] = {"success": False, "error": str(e)}
        
        # Calculate workflow duration
        workflow_end = datetime.now()
        results["end_time"] = workflow_end.isoformat()
        results["duration_seconds"] = (workflow_end - workflow_start).total_seconds()
        
        # Save workflow results
        self._save_workflow_results("daily", results)
        
        logger.info(f"Daily workflow completed in {results['duration_seconds']:.2f} seconds")
        return results
    
    def run_weekly_workflow(self) -> Dict[str, Any]:
        """Execute the weekly workflow"""
        logger.info("Starting weekly workflow...")
        
        workflow_start = datetime.now()
        results = {
            "workflow": "weekly",
            "start_time": workflow_start.isoformat(),
            "steps": {},
            "success": True,
            "errors": []
        }
        
        # Step 1: Strategy Evolution
        if "strategy_evolver" in self.agents:
            logger.info("Step 1: Running strategy evolution...")
            try:
                evolution_result = self.agents["strategy_evolver"].run_weekly_workflow()
                results["steps"]["strategy_evolution"] = {
                    "success": evolution_result.get("status") == "completed",
                    "workflow_status": evolution_result.get("status"),
                    "best_fitness": evolution_result.get("steps", {}).get("evolution", {}).get("results", {}).get("best_fitness"),
                    "best_strategy_type": evolution_result.get("steps", {}).get("evolution", {}).get("results", {}).get("best_strategy_type")
                }
                
                if evolution_result.get("status") != "completed":
                    results["success"] = False
                    results["errors"].append(f"Strategy evolution failed: {evolution_result.get('error', 'Unknown error')}")
            except Exception as e:
                logger.error(f"Strategy evolution error: {e}")
                results["steps"]["strategy_evolution"] = {"success": False, "error": str(e)}
                results["success"] = False
                results["errors"].append(f"Strategy evolution exception: {e}")
        else:
            logger.warning("Strategy Evolver agent not available")
            results["steps"]["strategy_evolution"] = {"success": False, "error": "Agent not initialized"}
            results["success"] = False
            results["errors"].append("Strategy Evolver agent not available")
        
        # Step 2: Performance Review (placeholder)
        logger.info("Step 2: Performance review (placeholder)...")
        results["steps"]["performance_review"] = {
            "success": True,
            "message": "Performance review not yet implemented",
            "placeholder": True
        }
        
        # Step 3: Strategy Selection (placeholder)
        logger.info("Step 3: Strategy selection (placeholder)...")
        results["steps"]["strategy_selection"] = {
            "success": True,
            "message": "Strategy selection not yet implemented",
            "placeholder": True
        }
        
        # Calculate duration
        workflow_end = datetime.now()
        results["end_time"] = workflow_end.isoformat()
        results["duration_seconds"] = (workflow_end - workflow_start).total_seconds()
        
        # Save workflow results
        self._save_workflow_results("weekly", results)
        
        logger.info(f"Weekly workflow completed in {results['duration_seconds']:.2f} seconds")
        return results
    
    def run_monthly_workflow(self) -> Dict[str, Any]:
        """Execute the monthly workflow"""
        logger.info("Starting monthly workflow...")
        
        # TODO: Implement monthly workflow
        # - Comprehensive analysis
        # - Parameter optimization
        # - System health check
        # - Roadmap planning
        
        return {
            "workflow": "monthly",
            "start_time": datetime.now().isoformat(),
            "message": "Monthly workflow not yet implemented",
            "success": False
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Perform system health check"""
        logger.info("Performing system health check...")
        
        health = {
            "timestamp": datetime.now().isoformat(),
            "components": {},
            "overall_status": "healthy",
            "issues": []
        }
        
        # Check API
        if self.api:
            try:
                api_health = self.api.health_check()
                health["components"]["api"] = {
                    "status": api_health.get("status", "unknown"),
                    "version": api_health.get("version", "unknown")
                }
                
                if not api_health.get("success", False):
                    health["overall_status"] = "degraded"
                    health["issues"].append("API health check failed")
            except Exception as e:
                health["components"]["api"] = {"status": "error", "error": str(e)}
                health["overall_status"] = "unhealthy"
                health["issues"].append(f"API error: {e}")
        else:
            health["components"]["api"] = {"status": "mock_mode", "note": "Using mock API"}
        
        # Check agents
        health["components"]["agents"] = {
            "total": len(self.agents),
            "loaded": list(self.agents.keys()),
            "status": "healthy" if len(self.agents) > 0 else "warning"
        }
        
        if len(self.agents) == 0:
            health["overall_status"] = "degraded"
            health["issues"].append("No agents loaded")
        
        # Check data directories
        data_dirs = self.config["openclaw_integration"]["data_storage"]
        health["components"]["data_directories"] = {}
        
        for dir_name, dir_path in data_dirs.items():
            path = Path(dir_path)
            if path.exists():
                health["components"]["data_directories"][dir_name] = {
                    "status": "healthy",
                    "path": str(path)
                }
            else:
                health["components"]["data_directories"][dir_name] = {
                    "status": "error",
                    "path": str(path),
                    "error": "Directory does not exist"
                }
                health["overall_status"] = "degraded"
                health["issues"].append(f"Data directory missing: {dir_name}")
        
        # Save health check results
        health_file = Path(self.config["openclaw_integration"]["data_storage"]["performance_reports"]) / "health_checks" / f"health_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        health_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(health_file, 'w') as f:
            json.dump(health, f, indent=2)
        
        logger.info(f"Health check completed: {health['overall_status']}")
        return health
    
    def _save_workflow_results(self, workflow_name: str, results: Dict[str, Any]):
        """Save workflow results to file"""
        results_dir = Path(self.config["openclaw_integration"]["data_storage"]["performance_reports"]) / "workflows"
        results_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = results_dir / f"{workflow_name}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.debug(f"Workflow results saved to {filename}")
    
    def generate_summary_report(self) -> Dict[str, Any]:
        """Generate a summary report of system activity"""
        logger.info("Generating system summary report...")
        
        # Load recent workflow results
        results_dir = Path(self.config["openclaw_integration"]["data_storage"]["performance_reports"]) / "workflows"
        
        recent_workflows = []
        if results_dir.exists():
            for file in sorted(results_dir.glob("*.json"), reverse=True)[:10]:  # Last 10 workflows
                try:
                    with open(file, 'r') as f:
                        workflow = json.load(f)
                    recent_workflows.append(workflow)
                except Exception as e:
                    logger.warning(f"Could not load workflow file {file}: {e}")
        
        # Calculate statistics
        successful_workflows = [w for w in recent_workflows if w.get("success", False)]
        failed_workflows = [w for w in recent_workflows if not w.get("success", False)]
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "period": "recent",
            "total_workflows": len(recent_workflows),
            "successful_workflows": len(successful_workflows),
            "failed_workflows": len(failed_workflows),
            "success_rate": len(successful_workflows) / len(recent_workflows) if recent_workflows else 0,
            "recent_workflows": recent_workflows[:5],  # Include first 5 for detail
            "system_status": self.health_check()["overall_status"]
        }
        
        # Save summary report
        summary_file = Path(self.config["openclaw_integration"]["data_storage"]["performance_reports"]) / "summaries" / f"summary_{datetime.now().strftime('%Y%m%d')}.json"
        summary_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Summary report generated: {summary_file}")
        return summary


# Command line interface
def main():
    """Main command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="FalseMarkets Integration Orchestrator")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--workflow", choices=["daily", "weekly", "monthly", "health", "summary"], 
                       default="daily", help="Workflow to execute")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize orchestrator
        orchestrator = FalseMarketsOrchestrator(config_path=args.config)
        
        # Execute requested workflow
        if args.workflow == "daily":
            result = orchestrator.run_daily_workflow()
        elif args.workflow == "weekly":
            result = orchestrator.run_weekly_workflow()
        elif args.workflow == "monthly":
            result = orchestrator.run_monthly_workflow()
        elif args.workflow == "health":
            result = orchestrator.health_check()
        elif args.workflow == "summary":
            result = orchestrator.generate_summary_report()
        else:
            result = {"error": f"Unknown workflow: {args.workflow}"}
        
        # Print result
        print(json.dumps(result, indent=2))
        
        # Exit with appropriate code
        if result.get("success", False):
            sys.exit(0)
        else:
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Orchestrator error: {e}")
        print(json.dumps({"error": str(e), "success": False}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()