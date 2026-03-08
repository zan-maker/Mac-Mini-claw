#!/usr/bin/env python3
"""
Utility to use local Ollama model for simple tasks
Fallback to API if local model fails
"""

import os
import json
import requests
import time
from typing import Dict, Optional

class LocalModelClient:
    """Client for local Ollama model"""
    
    def __init__(self, model: str = "tinyllama"):
        self.base_url = "http://localhost:11434"
        self.model = model
        self.timeout = 30  # seconds
        
    def generate(self, prompt: str, max_tokens: int = 256) -> Optional[str]:
        """Generate response using local model"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0.1  # Low temp for consistent responses
                    }
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            return data.get('response', '').strip()
        except Exception as e:
            print(f"Local model error: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if local model is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_model_info(self) -> Dict:
        """Get information about available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.json()
        except:
            return {"models": []}

def should_use_local(task_type: str) -> bool:
    """Determine if task should use local model"""
    local_tasks = [
        "heartbeat",
        "monitor",
        "check",
        "notification",
        "cleanup",
        "backup",
        "status"
    ]
    
    task_lower = task_type.lower()
    return any(local_task in task_lower for local_task in local_tasks)

def main():
    """Example usage"""
    client = LocalModelClient()
    
    if client.is_available():
        print("✅ Local model available")
        
        # Test with heartbeat check
        response = client.generate("Heartbeat check: system status OK? Reply with 'OK' or 'ISSUE'.")
        print(f"Test response: {response}")
    else:
        print("❌ Local model not available")

if __name__ == "__main__":
    main()
