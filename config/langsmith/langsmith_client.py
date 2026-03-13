#!/usr/bin/env python3
"""
LangSmith Client
Free alternative to Langfuse for LLM observability
"""

import os
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

# Try to import LangSmith (optional)
try:
    from langsmith import Client
    from langsmith.schemas import Run, Example
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("⚠️  LangSmith not installed. Run: pip install langsmith")

logger = logging.getLogger(__name__)

class LangSmithClient:
    """Client for LangSmith observability"""
    
    def __init__(self, api_key: Optional[str] = None, project_name: str = "default"):
        """
        Initialize LangSmith client
        
        Args:
            api_key: LangSmith API key (optional, can use environment variable)
            project_name: Project name for grouping traces
        """
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("LangSmith not installed. Run: pip install langsmith")
        
        self.api_key = api_key or os.getenv("LANGSMITH_API_KEY")
        self.project_name = project_name
        
        if not self.api_key:
            logger.warning("No LangSmith API key provided. Tracing will be disabled.")
            self.client = None
        else:
            os.environ["LANGSMITH_API_KEY"] = self.api_key
            self.client = Client()
            logger.info(f"LangSmith client initialized for project: {project_name}")
    
    def trace_llm_call(self, run_id: str, inputs: Dict, outputs: Dict,
                      run_type: str = "llm", metadata: Optional[Dict] = None,
                      tags: Optional[List[str]] = None) -> Optional[str]:
        """
        Trace an LLM call
        
        Args:
            run_id: Unique ID for this run
            inputs: Input parameters to the LLM
            outputs: Output from the LLM
            run_type: Type of run (llm, chain, tool, etc.)
            metadata: Additional metadata
            tags: Tags for categorization
            
        Returns:
            Run ID if successful, None otherwise
        """
        if not self.client:
            logger.warning("LangSmith client not initialized. Skipping trace.")
            return None
        
        try:
            run = Run(
                id=run_id,
                name=f"{run_type}_call",
                run_type=run_type,
                inputs=inputs,
                outputs=outputs,
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow(),
                extra=metadata or {},
                tags=tags or []
            )
            
            self.client.create_run(
                run_name=run.name,
                run_type=run.run_type,
                inputs=run.inputs,
                outputs=run.outputs,
                id=run.id,
                project_name=self.project_name,
                extra=run.extra,
                tags=run.tags
            )
            
            logger.info(f"Traced LLM call: {run_id}")
            return run_id
            
        except Exception as e:
            logger.error(f"Failed to trace LLM call: {e}")
            return None
    
    def trace_chain(self, chain_id: str, steps: List[Dict], 
                   metadata: Optional[Dict] = None) -> Optional[str]:
        """
        Trace a chain of LLM calls
        
        Args:
            chain_id: Unique ID for this chain
            steps: List of steps in the chain
            metadata: Additional metadata
            
        Returns:
            Chain ID if successful
        """
        if not self.client:
            logger.warning("LangSmith client not initialized. Skipping trace.")
            return None
        
        try:
            # Create parent run for the chain
            parent_run = Run(
                id=chain_id,
                name="llm_chain",
                run_type="chain",
                inputs={"step_count": len(steps)},
                outputs={"completed": True},
                start_time=datetime.utcnow(),
                extra=metadata or {},
                tags=["chain"]
            )
            
            self.client.create_run(
                run_name=parent_run.name,
                run_type=parent_run.run_type,
                inputs=parent_run.inputs,
                outputs=parent_run.outputs,
                id=parent_run.id,
                project_name=self.project_name,
                extra=parent_run.extra,
                tags=parent_run.tags
            )
            
            # Create child runs for each step
            for i, step in enumerate(steps):
                child_run = Run(
                    id=f"{chain_id}_step_{i}",
                    name=step.get("name", f"step_{i}"),
                    run_type=step.get("type", "llm"),
                    inputs=step.get("inputs", {}),
                    outputs=step.get("outputs", {}),
                    parent_run_id=chain_id,
                    start_time=datetime.utcnow(),
                    extra=step.get("metadata", {})
                )
                
                self.client.create_run(
                    run_name=child_run.name,
                    run_type=child_run.run_type,
                    inputs=child_run.inputs,
                    outputs=child_run.outputs,
                    id=child_run.id,
                    project_name=self.project_name,
                    parent_run_id=child_run.parent_run_id,
                    extra=child_run.extra
                )
            
            logger.info(f"Traced chain with {len(steps)} steps: {chain_id}")
            return chain_id
            
        except Exception as e:
            logger.error(f"Failed to trace chain: {e}")
            return None
    
    def create_dataset(self, name: str, description: str = "") -> Optional[str]:
        """
        Create a dataset for evaluation
        
        Args:
            name: Dataset name
            description: Dataset description
            
        Returns:
            Dataset ID if successful
        """
        if not self.client:
            logger.warning("LangSmith client not initialized.")
            return None
        
        try:
            dataset = self.client.create_dataset(
                dataset_name=name,
                description=description
            )
            
            logger.info(f"Created dataset: {name} ({dataset.id})")
            return dataset.id
            
        except Exception as e:
            logger.error(f"Failed to create dataset: {e}")
            return None
    
    def add_example_to_dataset(self, dataset_id: str, inputs: Dict, 
                              outputs: Dict, metadata: Optional[Dict] = None) -> Optional[str]:
        """
        Add example to dataset
        
        Args:
            dataset_id: Dataset ID
            inputs: Example inputs
            outputs: Expected outputs
            metadata: Additional metadata
            
        Returns:
            Example ID if successful
        """
        if not self.client:
            logger.warning("LangSmith client not initialized.")
            return None
        
        try:
            example = self.client.create_example(
                inputs=inputs,
                outputs=outputs,
                dataset_id=dataset_id,
                metadata=metadata or {}
            )
            
            logger.info(f"Added example to dataset {dataset_id}")
            return example.id
            
        except Exception as e:
            logger.error(f"Failed to add example: {e}")
            return None
    
    def compare_with_langfuse(self) -> Dict:
        """
        Compare LangSmith with Langfuse
        
        Returns:
            Comparison dictionary
        """
        return {
            'cost': {
                'langsmith': 'Free (1k traces/day)',
                'langfuse': '$50/month (starter plan)'
            },
            'retention': {
                'langsmith': '7 days (free tier)',
                'langfuse': '30 days'
            },
            'integration': {
                'langsmith': 'Best with LangChain',
                'langfuse': 'Framework agnostic'
            },
            'features': {
                'langsmith_better': ['Prompt management', 'Dataset versioning', 'Evaluation workflows'],
                'langfuse_better': ['Advanced analytics', 'Longer retention', 'Team features']
            },
            'recommendation': 'Use LangSmith if using LangChain, otherwise evaluate if Langfuse features are critical'
        }
    
    def get_usage_stats(self) -> Dict:
        """
        Get usage statistics
        
        Returns:
            Usage statistics
        """
        if not self.client:
            return {'error': 'Client not initialized'}
        
        try:
            # Note: LangSmith API for usage stats may be limited in free tier
            # This is a simplified version
            runs = self.client.list_runs(project_name=self.project_name, limit=100)
            
            return {
                'total_runs': len(list(runs)),
                'project': self.project_name,
                'free_tier_limit': 1000,
                'status': 'active'
            }
            
        except Exception as e:
            logger.error(f"Failed to get usage stats: {e}")
            return {'error': str(e)}

# Example usage
def example_langsmith_usage():
    """Example usage of LangSmith"""
    print("🔍 LangSmith Observability Example")
    print("="*50)
    
    # Check if LangSmith is available
    if not LANGCHAIN_AVAILABLE:
        print("⚠️  LangSmith not installed.")
        print("   Install with: pip install langsmith")
        return
    
    # Initialize client
    api_key = os.getenv("LANGSMITH_API_KEY")
    client = LangSmithClient(api_key=api_key, project_name="ai-agents")
    
    if client.client:
        print(f"✅ LangSmith client initialized")
        print(f"   Project: {client.project_name}")
        
        # Compare with Langfuse
        print("\n🔄 Comparison with Langfuse:")
        comparison = client.compare_with_langfuse()
        print(f"   Cost: {comparison['cost']['langsmith']} vs {comparison['cost']['langfuse']}")
        print(f"   Retention: {comparison['retention']['langsmith']} vs {comparison['retention']['langfuse']}")
        
        # Example tracing
        print("\n🎯 Example tracing calls:")
        print("   • client.trace_llm_call('run_123', {'prompt': '...'}, {'response': '...'})")
        print("   • client.trace_chain('chain_123', [step1, step2, step3])")
        print("   • client.create_dataset('evaluation_dataset', 'For testing prompts')")
        
        print("\n💰 Monthly savings: $50")
        print("📈 Free tier: 1,000 traces/day")
        
    else:
        print("❌ LangSmith client not initialized")
        print("   Set LANGSMITH_API_KEY environment variable")
        print("   Get API key from: https://smith.langchain.com")

if __name__ == "__main__":
    import os
    example_langsmith_usage()
