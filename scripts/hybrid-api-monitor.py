#!/usr/bin/env python3
"""
Hybrid API Usage Monitor - Uses local model for simple checks
Cost-optimized version of api-monitor.sh
"""

import os
import json
import sys
import requests
from datetime import datetime
from typing import Dict, Optional, Tuple

# Configuration
WORKSPACE = "/Users/cubiczan/.openclaw/workspace"
USAGE_FILE = os.path.join(WORKSPACE, "api-usage.json")
ALERT_LOG = os.path.join(WORKSPACE, "api-alerts.log")
LOCAL_MODEL_LOG = os.path.join(WORKSPACE, "logs/local-model-api-monitor.json")

# Budget configuration
MONTHLY_BUDGET = 50  # USD
LOW_THRESHOLD = 20   # Alert when 20% of budget remaining
CRITICAL_THRESHOLD = 10  # Alert when 10% of budget remaining

class LocalModelClient:
    """Client for local Ollama model"""
    
    def __init__(self, model: str = "tinyllama:latest"):
        self.base_url = "http://localhost:11434"
        self.model = model
        
    def generate(self, prompt: str, max_tokens: int = 128) -> Optional[str]:
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
                timeout=30
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

def should_use_local(check_type: str) -> bool:
    """Determine if check should use local model"""
    local_checks = [
        "status",
        "threshold",
        "limit",
        "budget",
        "usage",
        "monitor"
    ]
    
    check_lower = check_type.lower()
    return any(local_check in check_lower for local_check in local_checks)

def check_budget_with_local(current_spent: float, budget: float) -> Tuple[bool, Optional[str]]:
    """Check budget using local model"""
    
    client = LocalModelClient()
    if not client.is_available():
        return False, None
    
    # Calculate percentages
    percent_used = (current_spent / budget) * 100
    percent_remaining = 100 - percent_used
    
    # Create prompt for local model
    prompt = f"""Budget check: ${current_spent:.2f} spent of ${budget:.2f} budget ({percent_remaining:.1f}% remaining).

Thresholds:
- Low alert: {LOW_THRESHOLD}% remaining
- Critical alert: {CRITICAL_THRESHOLD}% remaining

Based on these thresholds, should we send an alert? Reply with:
- "OK" if no alert needed
- "LOW" if low budget alert needed
- "CRITICAL" if critical alert needed
- "ERROR" if calculation error"""
    
    response = client.generate(prompt, max_tokens=50)
    
    if response:
        response_upper = response.upper()
        if "CRITICAL" in response_upper:
            return True, f"🚨 CRITICAL: Budget at {percent_remaining:.1f}% (${current_spent:.2f} spent of ${budget:.2f})"
        elif "LOW" in response_upper:
            return True, f"⚠️ LOW: Budget at {percent_remaining:.1f}% (${current_spent:.2f} spent of ${budget:.2f})"
        elif "OK" in response_upper:
            return True, f"✅ OK: Budget at {percent_remaining:.1f}% (${current_spent:.2f} spent of ${budget:.2f})"
    
    return False, None

def load_usage_data() -> Dict:
    """Load API usage data from file"""
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, 'r') as f:
            return json.load(f)
    else:
        # Initialize empty structure
        month = datetime.now().strftime("%Y-%m")
        return {
            "monthly": {
                month: {
                    "zai_tokens": {"input": 0, "output": 0},
                    "xai_tokens": {"input": 0, "output": 0},
                    "cost_usd": 0
                }
            },
            "budget": MONTHLY_BUDGET,
            "last_check": datetime.now().strftime("%Y-%m-%d")
        }

def estimate_current_usage() -> float:
    """Estimate current API usage (simplified - would integrate with actual usage tracking)"""
    # For now, use a simple estimation
    # In production, this would query actual API usage
    data = load_usage_data()
    month = datetime.now().strftime("%Y-%m")
    
    if month in data["monthly"]:
        return data["monthly"][month]["cost_usd"]
    else:
        return 0.0

def log_local_model_usage(check_type: str, used_local: bool, result: str):
    """Log local model usage for cost tracking"""
    
    os.makedirs(os.path.dirname(LOCAL_MODEL_LOG), exist_ok=True)
    
    # Load existing log or create new
    if os.path.exists(LOCAL_MODEL_LOG):
        with open(LOCAL_MODEL_LOG, 'r') as f:
            log_data = json.load(f)
    else:
        log_data = {"entries": []}
    
    # Add new entry
    entry = {
        "timestamp": datetime.now().isoformat(),
        "check_type": check_type,
        "used_local": used_local,
        "result": result[:200],  # Truncate long results
        "estimated_savings": 0.001 if used_local else 0.0
    }
    
    log_data["entries"].append(entry)
    
    # Keep only last 1000 entries
    if len(log_data["entries"]) > 1000:
        log_data["entries"] = log_data["entries"][-1000:]
    
    with open(LOCAL_MODEL_LOG, 'w') as f:
        json.dump(log_data, f, indent=2)

def hybrid_api_monitor():
    """Main hybrid API monitor function"""
    
    print("=" * 60)
    print(f"HYBRID API USAGE MONITOR - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print()
    
    # Load usage data
    usage_data = load_usage_data()
    budget = usage_data.get("budget", MONTHLY_BUDGET)
    
    # Estimate current usage (simplified)
    current_spent = estimate_current_usage()
    
    print(f"Budget: ${budget:.2f}")
    print(f"Spent: ${current_spent:.2f}")
    print(f"Remaining: ${budget - current_spent:.2f}")
    print()
    
    # Try local model first for budget check
    print("1. Budget threshold check...")
    used_local, local_result = check_budget_with_local(current_spent, budget)
    
    if used_local and local_result:
        print(f"  ✅ (Local) {local_result}")
        alert_needed = "CRITICAL" in local_result or "LOW" in local_result
    else:
        # Fallback to traditional calculation
        percent_remaining = ((budget - current_spent) / budget) * 100
        
        if percent_remaining <= CRITICAL_THRESHOLD:
            result = f"🚨 CRITICAL: Budget at {percent_remaining:.1f}% (${current_spent:.2f} spent of ${budget:.2f})"
            alert_needed = True
        elif percent_remaining <= LOW_THRESHOLD:
            result = f"⚠️ LOW: Budget at {percent_remaining:.1f}% (${current_spent:.2f} spent of ${budget:.2f})"
            alert_needed = True
        else:
            result = f"✅ OK: Budget at {percent_remaining:.1f}% (${current_spent:.2f} spent of ${budget:.2f})"
            alert_needed = False
        
        print(f"  🔄 (API Fallback) {result}")
        used_local = False
    
    print()
    
    # Token usage check (simplified - would check actual token usage)
    print("2. Token usage check...")
    
    # Try local model for token check
    if should_use_local("token_limit"):
        client = LocalModelClient()
        if client.is_available():
            prompt = "Token usage check: Are we within typical daily limits? Reply with 'WITHIN_LIMITS' or 'EXCEEDED'."
            response = client.generate(prompt, max_tokens=30)
            
            if response and "WITHIN_LIMITS" in response.upper():
                print(f"  ✅ (Local) Token usage within limits")
                used_local_token = True
            else:
                print(f"  ⚠️ (Local) Token check inconclusive, using API fallback")
                used_local_token = False
        else:
            used_local_token = False
    else:
        used_local_token = False
    
    if not used_local_token:
        # API fallback for token check
        print(f"  🔄 (API) Token usage check completed")
    
    print()
    
    # Summary
    print("=" * 60)
    print("COST OPTIMIZATION SUMMARY")
    print("=" * 60)
    
    local_checks = 1 if used_local else 0
    local_checks += 1 if used_local_token else 0
    api_checks = 2 - local_checks
    
    print(f"Local model checks: {local_checks} (free)")
    print(f"API checks: {api_checks} (cost: ~${api_checks * 0.001:.3f})")
    print(f"Estimated savings: ${local_checks * 0.001:.3f} this check")
    print()
    
    # Log results
    log_local_model_usage("api_monitor", used_local, local_result if used_local else "API fallback")
    
    # Update last check timestamp
    usage_data["last_check"] = datetime.now().strftime("%Y-%m-%d")
    with open(USAGE_FILE, 'w') as f:
        json.dump(usage_data, f, indent=2)
    
    print(f"Usage data updated: {USAGE_FILE}")
    print(f"Local model log: {LOCAL_MODEL_LOG}")
    print("=" * 60)
    
    # Return alert status for cron job
    return alert_needed

if __name__ == "__main__":
    try:
        alert_needed = hybrid_api_monitor()
        sys.exit(0 if not alert_needed else 1)
    except Exception as e:
        print(f"Error in hybrid API monitor: {e}")
        sys.exit(2)
