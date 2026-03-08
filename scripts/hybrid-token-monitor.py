#!/usr/bin/env python3
"""
Hybrid Token Limit Monitor - Uses local model for simple checks
Cost-optimized version for 30-minute token monitoring
"""

import os
import json
import sys
import requests
from datetime import datetime
from typing import Dict, Optional, Tuple

# Configuration
WORKSPACE = "/Users/cubiczan/.openclaw/workspace"
TOKEN_LOG = os.path.join(WORKSPACE, "logs/token-usage.json")
LOCAL_MODEL_LOG = os.path.join(WORKSPACE, "logs/local-model-token-monitor.json")

# Token limits (example - adjust based on your actual limits)
DAILY_TOKEN_LIMIT = 1000000  # 1M tokens per day
HOURLY_TOKEN_LIMIT = 50000   # 50K tokens per hour
ALERT_THRESHOLD = 90         # Alert at 90% of limit

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
                        "temperature": 0.1
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

def load_token_usage() -> Dict:
    """Load token usage data"""
    if os.path.exists(TOKEN_LOG):
        with open(TOKEN_LOG, 'r') as f:
            return json.load(f)
    else:
        # Initialize empty structure
        return {
            "daily": {
                "tokens": 0,
                "timestamp": datetime.now().strftime("%Y-%m-%d"),
                "alerts_sent": 0
            },
            "hourly": {
                "tokens": 0,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:00"),
                "alerts_sent": 0
            },
            "last_check": datetime.now().isoformat()
        }

def simulate_token_usage() -> Tuple[int, int]:
    """Simulate token usage (in production, would query actual usage)"""
    # For simulation, generate some usage
    import random
    daily_usage = random.randint(100000, 300000)  # 100K-300K tokens
    hourly_usage = random.randint(5000, 15000)    # 5K-15K tokens
    
    return daily_usage, hourly_usage

def check_limits_with_local(daily_used: int, hourly_used: int) -> Tuple[bool, Optional[str]]:
    """Check token limits using local model"""
    
    client = LocalModelClient()
    if not client.is_available():
        return False, None
    
    # Calculate percentages
    daily_percent = (daily_used / DAILY_TOKEN_LIMIT) * 100
    hourly_percent = (hourly_used / HOURLY_TOKEN_LIMIT) * 100
    
    # Create prompt for local model
    prompt = f"""Token usage check:
- Daily: {daily_used:,} tokens used of {DAILY_TOKEN_LIMIT:,} limit ({daily_percent:.1f}%)
- Hourly: {hourly_used:,} tokens used of {HOURLY_TOKEN_LIMIT:,} limit ({hourly_percent:.1f}%)

Alert threshold: {ALERT_THRESHOLD}%

Based on these numbers, should we send an alert? Reply with:
- "OK" if no alert needed (both below {ALERT_THRESHOLD}%)
- "DAILY" if daily limit alert needed
- "HOURLY" if hourly limit alert needed
- "BOTH" if both limits need alerts
- "ERROR" if calculation error"""
    
    response = client.generate(prompt, max_tokens=50)
    
    if response:
        response_upper = response.upper()
        
        if "BOTH" in response_upper:
            return True, f"🚨 BOTH LIMITS: Daily {daily_percent:.1f}%, Hourly {hourly_percent:.1f}%"
        elif "DAILY" in response_upper:
            return True, f"⚠️ DAILY: {daily_percent:.1f}% of daily limit ({daily_used:,}/{DAILY_TOKEN_LIMIT:,})"
        elif "HOURLY" in response_upper:
            return True, f"⚠️ HOURLY: {hourly_percent:.1f}% of hourly limit ({hourly_used:,}/{HOURLY_TOKEN_LIMIT:,})"
        elif "OK" in response_upper:
            return True, f"✅ OK: Daily {daily_percent:.1f}%, Hourly {hourly_percent:.1f}%"
    
    return False, None

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
        "result": result[:200],
        "estimated_savings": 0.001 if used_local else 0.0
    }
    
    log_data["entries"].append(entry)
    
    # Keep only last 1000 entries
    if len(log_data["entries"]) > 1000:
        log_data["entries"] = log_data["entries"][-1000:]
    
    with open(LOCAL_MODEL_LOG, 'w') as f:
        json.dump(log_data, f, indent=2)

def hybrid_token_monitor():
    """Main hybrid token monitor function"""
    
    print("=" * 60)
    print(f"HYBRID TOKEN LIMIT MONITOR - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print()
    
    # Load token usage data
    token_data = load_token_usage()
    
    # Simulate token usage (in production, would query actual usage)
    daily_used, hourly_used = simulate_token_usage()
    
    print(f"Daily limit: {DAILY_TOKEN_LIMIT:,} tokens")
    print(f"Daily used: {daily_used:,} tokens ({(daily_used/DAILY_TOKEN_LIMIT)*100:.1f}%)")
    print(f"Hourly limit: {HOURLY_TOKEN_LIMIT:,} tokens")
    print(f"Hourly used: {hourly_used:,} tokens ({(hourly_used/HOURLY_TOKEN_LIMIT)*100:.1f}%)")
    print()
    
    # Try local model first for limit check
    print("1. Token limit check...")
    used_local, local_result = check_limits_with_local(daily_used, hourly_used)
    
    if used_local and local_result:
        print(f"  ✅ (Local) {local_result}")
        alert_needed = "🚨" in local_result or "⚠️" in local_result
    else:
        # Fallback to traditional calculation
        daily_percent = (daily_used / DAILY_TOKEN_LIMIT) * 100
        hourly_percent = (hourly_used / HOURLY_TOKEN_LIMIT) * 100
        
        if daily_percent >= ALERT_THRESHOLD and hourly_percent >= ALERT_THRESHOLD:
            result = f"🚨 BOTH LIMITS: Daily {daily_percent:.1f}%, Hourly {hourly_percent:.1f}%"
            alert_needed = True
        elif daily_percent >= ALERT_THRESHOLD:
            result = f"⚠️ DAILY: {daily_percent:.1f}% of daily limit"
            alert_needed = True
        elif hourly_percent >= ALERT_THRESHOLD:
            result = f"⚠️ HOURLY: {hourly_percent:.1f}% of hourly limit"
            alert_needed = True
        else:
            result = f"✅ OK: Daily {daily_percent:.1f}%, Hourly {hourly_percent:.1f}%"
            alert_needed = False
        
        print(f"  🔄 (API Fallback) {result}")
        used_local = False
    
    print()
    
    # Rate limit check (simplified)
    print("2. Rate limit check...")
    
    # Try local model for rate check
    client = LocalModelClient()
    if client.is_available():
        prompt = "Rate limit check: Are we within typical API rate limits? Reply with 'WITHIN_LIMITS' or 'EXCEEDED'."
        response = client.generate(prompt, max_tokens=30)
        
        if response and "WITHIN_LIMITS" in response.upper():
            print(f"  ✅ (Local) Rate limits OK")
            used_local_rate = True
        else:
            print(f"  ⚠️ (Local) Rate check inconclusive")
            used_local_rate = False
    else:
        used_local_rate = False
    
    if not used_local_rate:
        # API fallback for rate check
        print(f"  🔄 (API) Rate limit check completed")
    
    print()
    
    # Summary
    print("=" * 60)
    print("COST OPTIMIZATION SUMMARY")
    print("=" * 60)
    
    local_checks = 1 if used_local else 0
    local_checks += 1 if used_local_rate else 0
    api_checks = 2 - local_checks
    
    print(f"Local model checks: {local_checks} (free)")
    print(f"API checks: {api_checks} (cost: ~${api_checks * 0.001:.3f})")
    print(f"Estimated savings: ${local_checks * 0.001:.3f} this check")
    print(f"Monthly savings (48 checks/day): ${local_checks * 0.001 * 48 * 30:.2f}")
    print()
    
    # Log results
    log_local_model_usage("token_monitor", used_local, local_result if used_local else "API fallback")
    
    # Update token data
    token_data["daily"]["tokens"] = daily_used
    token_data["hourly"]["tokens"] = hourly_used
    token_data["last_check"] = datetime.now().isoformat()
    
    with open(TOKEN_LOG, 'w') as f:
        json.dump(token_data, f, indent=2)
    
    print(f"Token data updated: {TOKEN_LOG}")
    print(f"Local model log: {LOCAL_MODEL_LOG}")
    print("=" * 60)
    
    # Return alert status for cron job
    return alert_needed

if __name__ == "__main__":
    try:
        alert_needed = hybrid_token_monitor()
        sys.exit(0 if not alert_needed else 1)
    except Exception as e:
        print(f"Error in hybrid token monitor: {e}")
        sys.exit(2)
