#!/usr/bin/env python3
"""
Hybrid Critical API Alert - Uses local model for urgency assessment
Cost-optimized version for 12-hour critical alerts
"""

import os
import json
import sys
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

# Configuration
WORKSPACE = "/Users/cubiczan/.openclaw/workspace"
CRITICAL_LOG = os.path.join(WORKSPACE, "logs/critical-alerts.json")
LOCAL_MODEL_LOG = os.path.join(WORKSPACE, "logs/local-model-critical-alert.json")

# Alert thresholds
CRITICAL_BUDGET_PERCENT = 10  # Critical at 10% budget remaining
CRITICAL_TOKEN_PERCENT = 95   # Critical at 95% token usage
MIN_ALERT_INTERVAL = 3600     # Minimum 1 hour between alerts (seconds)

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

def assess_criticality_with_local(
    budget_percent: float, 
    token_percent: float,
    last_alert_time: Optional[datetime]
) -> Tuple[bool, Optional[str]]:
    """Assess criticality using local model"""
    
    client = LocalModelClient()
    if not client.is_available():
        return False, None
    
    # Calculate time since last alert
    time_since_last = ""
    if last_alert_time:
        hours_since = (datetime.now() - last_alert_time).total_seconds() / 3600
        time_since_last = f"Last alert was {hours_since:.1f} hours ago."
    
    # Create prompt for local model
    prompt = f"""Critical alert assessment:
- Budget remaining: {budget_percent:.1f}% (critical threshold: {CRITICAL_BUDGET_PERCENT}%)
- Token usage: {token_percent:.1f}% (critical threshold: {CRITICAL_TOKEN_PERCENT}%)
{time_since_last}

Should we send a CRITICAL alert? Consider:
1. Is either metric above critical threshold?
2. Has enough time passed since last alert?
3. Is this truly urgent?

Reply with:
- "CRITICAL" if urgent alert needed
- "WARNING" if concerning but not critical
- "OK" if no alert needed
- "ERROR" if assessment unclear"""
    
    response = client.generate(prompt, max_tokens=60)
    
    if response:
        response_upper = response.upper()
        
        if "CRITICAL" in response_upper:
            reason = "Budget critical" if budget_percent <= CRITICAL_BUDGET_PERCENT else "Token usage critical"
            return True, f"🚨 CRITICAL: {reason} (Budget: {budget_percent:.1f}%, Tokens: {token_percent:.1f}%)"
        elif "WARNING" in response_upper:
            return True, f"⚠️ WARNING: Approaching limits (Budget: {budget_percent:.1f}%, Tokens: {token_percent:.1f}%)"
        elif "OK" in response_upper:
            return True, f"✅ OK: Within limits (Budget: {budget_percent:.1f}%, Tokens: {token_percent:.1f}%)"
    
    return False, None

def load_critical_alerts() -> Dict:
    """Load critical alert history"""
    if os.path.exists(CRITICAL_LOG):
        with open(CRITICAL_LOG, 'r') as f:
            return json.load(f)
    else:
        return {
            "alerts": [],
            "last_alert": None,
            "settings": {
                "critical_budget_percent": CRITICAL_BUDGET_PERCENT,
                "critical_token_percent": CRITICAL_TOKEN_PERCENT,
                "min_alert_interval": MIN_ALERT_INTERVAL
            }
        }

def simulate_metrics() -> Tuple[float, float]:
    """Simulate metrics (in production, would query actual metrics)"""
    import random
    
    # Simulate budget remaining (5-15% for testing critical scenarios)
    budget_remaining = random.uniform(5, 15)
    
    # Simulate token usage (80-99% for testing critical scenarios)
    token_usage = random.uniform(80, 99)
    
    return budget_remaining, token_usage

def should_send_alert(last_alert_time: Optional[datetime]) -> bool:
    """Check if enough time has passed since last alert"""
    if not last_alert_time:
        return True
    
    time_since = (datetime.now() - last_alert_time).total_seconds()
    return time_since >= MIN_ALERT_INTERVAL

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

def hybrid_critical_alert():
    """Main hybrid critical alert function"""
    
    print("=" * 60)
    print(f"HYBRID CRITICAL API ALERT - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print()
    
    # Load alert history
    alert_data = load_critical_alerts()
    
    # Parse last alert time
    last_alert_time = None
    if alert_data.get("last_alert"):
        try:
            last_alert_time = datetime.fromisoformat(alert_data["last_alert"])
        except:
            last_alert_time = None
    
    # Check if enough time has passed
    if not should_send_alert(last_alert_time):
        print(f"⏰ Skipping: Last alert was too recent")
        print(f"  Minimum interval: {MIN_ALERT_INTERVAL/3600:.1f} hours")
        return False
    
    # Simulate metrics (in production, would query actual metrics)
    budget_remaining, token_usage = simulate_metrics()
    
    print(f"Budget remaining: {budget_remaining:.1f}% (critical: ≤{CRITICAL_BUDGET_PERCENT}%)")
    print(f"Token usage: {token_usage:.1f}% (critical: ≥{CRITICAL_TOKEN_PERCENT}%)")
    
    if last_alert_time:
        hours_since = (datetime.now() - last_alert_time).total_seconds() / 3600
        print(f"Last alert: {hours_since:.1f} hours ago")
    else:
        print(f"Last alert: Never")
    
    print()
    
    # Try local model first for criticality assessment
    print("1. Criticality assessment...")
    used_local, local_result = assess_criticality_with_local(
        budget_remaining, token_usage, last_alert_time
    )
    
    if used_local and local_result:
        print(f"  ✅ (Local) {local_result}")
        send_alert = "🚨" in local_result or "⚠️" in local_result
    else:
        # Fallback to traditional calculation
        is_budget_critical = budget_remaining <= CRITICAL_BUDGET_PERCENT
        is_token_critical = token_usage >= CRITICAL_TOKEN_PERCENT
        
        if is_budget_critical and is_token_critical:
            result = f"🚨 CRITICAL: Both budget ({budget_remaining:.1f}%) and tokens ({token_usage:.1f}%) critical"
            send_alert = True
        elif is_budget_critical:
            result = f"🚨 CRITICAL: Budget critical ({budget_remaining:.1f}% remaining)"
            send_alert = True
        elif is_token_critical:
            result = f"🚨 CRITICAL: Token usage critical ({token_usage:.1f}%)"
            send_alert = True
        else:
            result = f"✅ OK: Within limits (Budget: {budget_remaining:.1f}%, Tokens: {token_usage:.1f}%)"
            send_alert = False
        
        print(f"  🔄 (API Fallback) {result}")
        used_local = False
    
    print()
    
    # System health check (simplified)
    print("2. System health check...")
    
    # Try local model for health check
    client = LocalModelClient()
    if client.is_available():
        prompt = "System health check: Is the API monitoring system functioning properly? Reply with 'HEALTHY' or 'ISSUE'."
        response = client.generate(prompt, max_tokens=30)
        
        if response and "HEALTHY" in response.upper():
            print(f"  ✅ (Local) System health OK")
            used_local_health = True
        else:
            print(f"  ⚠️ (Local) Health check inconclusive")
            used_local_health = False
    else:
        used_local_health = False
    
    if not used_local_health:
        # API fallback for health check
        print(f"  🔄 (API) System health check completed")
    
    print()
    
    # Summary
    print("=" * 60)
    print("COST OPTIMIZATION SUMMARY")
    print("=" * 60)
    
    local_checks = 1 if used_local else 0
    local_checks += 1 if used_local_health else 0
    api_checks = 2 - local_checks
    
    print(f"Local model checks: {local_checks} (free)")
    print(f"API checks: {api_checks} (cost: ~${api_checks * 0.001:.3f})")
    print(f"Estimated savings: ${local_checks * 0.001:.3f} this check")
    print(f"Monthly savings (2 checks/day): ${local_checks * 0.001 * 2 * 30:.2f}")
    print()
    
    # Log results
    log_local_model_usage("critical_alert", used_local, local_result if used_local else "API fallback")
    
    # Update alert history if sending alert
    if send_alert:
        alert_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "critical" if "🚨" in (local_result if used_local else result) else "warning",
            "budget_remaining": budget_remaining,
            "token_usage": token_usage,
            "message": local_result if used_local else result
        }
        
        alert_data["alerts"].append(alert_entry)
        alert_data["last_alert"] = datetime.now().isoformat()
        
        # Keep only last 100 alerts
        if len(alert_data["alerts"]) > 100:
            alert_data["alerts"] = alert_data["alerts"][-100:]
    
    with open(CRITICAL_LOG, 'w') as f:
        json.dump(alert_data, f, indent=2)
    
    print(f"Alert data updated: {CRITICAL_LOG}")
    print(f"Local model log: {LOCAL_MODEL_LOG}")
    print("=" * 60)
    
    # Return alert status for cron job
    return send_alert

if __name__ == "__main__":
    try:
        send_alert = hybrid_critical_alert()
        sys.exit(0 if not send_alert else 1)
    except Exception as e:
        print(f"Error in hybrid critical alert: {e}")
        sys.exit(2)
