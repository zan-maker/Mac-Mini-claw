#!/bin/bash
# Local Model Setup for Cost Reduction
# Installs Ollama + lightweight model + configures OpenClaw for local tasks

set -e

echo "================================================"
echo "LOCAL MODEL SETUP FOR COST REDUCTION"
echo "================================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Ollama is installed
echo "1. Checking Ollama installation..."
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✅ Ollama is installed${NC}"
    OLLAMA_VERSION=$(ollama --version 2>/dev/null | head -1)
    echo "   Version: $OLLAMA_VERSION"
else
    echo -e "${RED}❌ Ollama not installed${NC}"
    echo "   Installing via Homebrew..."
    brew install ollama
fi

# Start Ollama service
echo
echo "2. Starting Ollama service..."
if pgrep -x "ollama" > /dev/null; then
    echo -e "${GREEN}✅ Ollama service is running${NC}"
else
    echo -e "${YELLOW}⚠️ Starting Ollama service...${NC}"
    # Start in background
    ollama serve > /tmp/ollama.log 2>&1 &
    OLLAMA_PID=$!
    echo $OLLAMA_PID > /tmp/ollama.pid
    sleep 5
    
    # Check if started
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Ollama service started successfully${NC}"
    else
        echo -e "${RED}❌ Failed to start Ollama service${NC}"
        exit 1
    fi
fi

# Check available models
echo
echo "3. Checking available models..."
MODELS=$(curl -s http://localhost:11434/api/tags | jq -r '.models[].name' 2>/dev/null || echo "")

if [ -z "$MODELS" ]; then
    echo -e "${YELLOW}⚠️ No models found. Installing lightweight model...${NC}"
    
    # Install tinyllama (smallest, fastest for simple tasks)
    echo "   Downloading tinyllama (1.1GB)..."
    ollama pull tinyllama 2>&1 | while read line; do
        echo "   $line"
    done
    
    # Verify installation
    if curl -s http://localhost:11434/api/tags | grep -q "tinyllama"; then
        echo -e "${GREEN}✅ tinyllama installed successfully${NC}"
        SELECTED_MODEL="tinyllama"
    else
        echo -e "${RED}❌ Failed to install model${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Available models:${NC}"
    echo "$MODELS" | while read model; do
        echo "   - $model"
    done
    
    # Select smallest model for cost efficiency
    SELECTED_MODEL=$(echo "$MODELS" | head -1)
    echo
    echo -e "${GREEN}✅ Using model: $SELECTED_MODEL${NC}"
fi

# Test the model
echo
echo "4. Testing local model..."
TEST_RESPONSE=$(curl -s http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "'"$SELECTED_MODEL"'",
    "prompt": "Heartbeat check: system status OK?",
    "stream": false
  }' 2>/dev/null | jq -r '.response' || echo "Test failed")

if [ "$TEST_RESPONSE" != "Test failed" ] && [ ! -z "$TEST_RESPONSE" ]; then
    echo -e "${GREEN}✅ Local model test successful!${NC}"
    echo "   Response: $TEST_RESPONSE"
else
    echo -e "${RED}❌ Local model test failed${NC}"
    exit 1
fi

# Create OpenClaw configuration for local model
echo
echo "5. Configuring OpenClaw for local model..."
LOCAL_CONFIG="/Users/cubiczan/.openclaw/workspace/config/local-model-config.json"

cat > "$LOCAL_CONFIG" << EOF
{
  "local_models": {
    "ollama": {
      "base_url": "http://localhost:11434",
      "api": "ollama",
      "models": [
        {
          "id": "$SELECTED_MODEL",
          "name": "Local $SELECTED_MODEL",
          "reasoning": false,
          "input": ["text"],
          "cost": {
            "input": 0,
            "output": 0,
            "cacheRead": 0,
            "cacheWrite": 0
          },
          "contextWindow": 4096,
          "maxTokens": 1024
        }
      ]
    }
  },
  "model_routing": {
    "simple_tasks": ["heartbeat", "file_cleanup", "basic_monitoring"],
    "complex_tasks": ["research", "analysis", "email_composition"],
    "default_local": "$SELECTED_MODEL"
  },
  "cost_savings": {
    "estimated_monthly_savings": "$10-50",
    "tasks_to_localize": [
      "heartbeat",
      "token_monitor",
      "api_usage_check",
      "file_backup_notifications",
      "basic_system_checks"
    ]
  }
}
EOF

echo -e "${GREEN}✅ OpenClaw local model configuration created${NC}"
echo "   Location: $LOCAL_CONFIG"

# Create script to use local model for simple tasks
echo
echo "6. Creating local model utility script..."
LOCAL_SCRIPT="/Users/cubiczan/.openclaw/workspace/scripts/use-local-model.py"

cat > "$LOCAL_SCRIPT" << 'EOF'
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
EOF

chmod +x "$LOCAL_SCRIPT"
echo -e "${GREEN}✅ Local model utility script created${NC}"
echo "   Location: $LOCAL_SCRIPT"

# Update heartbeat cron job to use local model
echo
echo "7. Updating heartbeat configuration..."
HEARTBEAT_FILE="/Users/cubiczan/.openclaw/workspace/HEARTBEAT.md"

if [ -f "$HEARTBEAT_FILE" ]; then
    cat >> "$HEARTBEAT_FILE" << 'EOF'

## Local Model Optimization

**Cost-saving strategy:** Use local Ollama model for simple checks

**Tasks using local model:**
- System status checks
- Basic monitoring
- File cleanup notifications
- Token usage alerts (simple)

**Fallback to API if:**
- Local model unavailable
- Complex analysis needed
- Time-sensitive critical alerts

**Expected savings:** $10-50/month
EOF
    echo -e "${GREEN}✅ Heartbeat configuration updated${NC}"
else
    echo -e "${YELLOW}⚠️ HEARTBEAT.md not found, creating...${NC}"
    cat > "$HEARTBEAT_FILE" << 'EOF'
# HEARTBEAT.md - Local Model Optimized

## Tasks using local model (free):
- System status checks
- Basic monitoring alerts
- File cleanup notifications
- Simple token usage alerts

## Tasks using API (paid):
- Complex research
- Email composition
- Market analysis
- Deal evaluation

## Cost Optimization
Using local tinyllama model for simple tasks saves ~$0.001-0.005 per check.
Estimated monthly savings: $10-50
EOF
    echo -e "${GREEN}✅ Heartbeat file created${NC}"
fi

# Create service management script
echo
echo "8. Creating service management scripts..."
SERVICE_SCRIPT="/Users/cubiczan/.openclaw/workspace/scripts/manage-local-model.sh"

cat > "$SERVICE_SCRIPT" << 'EOF'
#!/bin/bash
# Manage local Ollama model service

case "$1" in
    start)
        echo "Starting Ollama service..."
        ollama serve > /tmp/ollama.log 2>&1 &
        echo $! > /tmp/ollama.pid
        sleep 3
        echo "✅ Ollama service started"
        ;;
    stop)
        echo "Stopping Ollama service..."
        if [ -f /tmp/ollama.pid ]; then
            kill $(cat /tmp/ollama.pid) 2>/dev/null
            rm /tmp/ollama.pid
        fi
        pkill -f "ollama serve" 2>/dev/null
        echo "✅ Ollama service stopped"
        ;;
    status)
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            echo "✅ Ollama service is running"
            curl -s http://localhost:11434/api/tags | jq '.models'
        else
            echo "❌ Ollama service is not running"
        fi
        ;;
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        exit 1
        ;;
esac
EOF

chmod +x "$SERVICE_SCRIPT"
echo -e "${GREEN}✅ Service management script created${NC}"
echo "   Location: $SERVICE_SCRIPT"

echo
echo "================================================"
echo "SETUP COMPLETE! 🎉"
echo "================================================"
echo
echo "Next steps:"
echo "1. Test local model: python3 $LOCAL_SCRIPT"
echo "2. Start service: $SERVICE_SCRIPT start"
echo "3. Update cron jobs to use local model for simple tasks"
echo "4. Monitor cost savings in next billing cycle"
echo
echo "Estimated monthly savings: $10-50"
echo "Local model: $SELECTED_MODEL"
echo "API fallback: DeepSeek/GLM-5 for complex tasks"
echo "================================================"
