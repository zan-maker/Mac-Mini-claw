#!/bin/bash
# Universal Agent Integration
# Usage: ./integrate_agent.sh <name> <directory> [type]

AGENT_NAME="$1"
AGENT_DIR="$2"
AGENT_TYPE="${3:-custom}"

echo "🔧 Integrating: $AGENT_NAME"
echo "   Directory: $AGENT_DIR"
echo "   Type: $AGENT_TYPE"

# Copy files
cp /Users/cubiczan/.openclaw/workspace/optimized_browser_wrapper.py "$AGENT_DIR/"
cp /Users/cubiczan/.openclaw/workspace/skill-evolution/complete_agent.py "$AGENT_DIR/"

# Create directories
mkdir -p "$AGENT_DIR/evolution/patterns"
mkdir -p "$AGENT_DIR/evolution/versions"

echo "✅ Integration complete for $AGENT_NAME"
echo "   Capabilities: Browser + Token Optimization + Skill Evolution"
