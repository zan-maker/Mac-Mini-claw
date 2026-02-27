#!/bin/bash
# Lead Gen Runner - Activates venv and runs lead gen scripts
# Usage: ./run-lead-gen.sh [script-name]

VENV_PATH="/Users/cubiczan/.openclaw/workspace/kalshi-venv"
SCRIPTS_DIR="/Users/cubiczan/.openclaw/workspace/scripts"
LOG_DIR="/Users/cubiczan/.openclaw/workspace/logs"

# Create log dir if needed
mkdir -p "$LOG_DIR"

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Get current timestamp
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Run the specified script
SCRIPT="$1"

if [ -z "$SCRIPT" ]; then
    echo "[$TIMESTAMP] Running ALL lead gen scripts..."
    
    echo "[$TIMESTAMP] Running expense-reduction-lead-gen.py..."
    python3 "$SCRIPTS_DIR/expense-reduction-lead-gen.py" >> "$LOG_DIR/lead-gen.log" 2>&1
    
    echo "[$TIMESTAMP] Running buyer-lead-gen.py..."
    python3 "$SCRIPTS_DIR/buyer-lead-gen.py" >> "$LOG_DIR/lead-gen.log" 2>&1
    
    echo "[$TIMESTAMP] Running seller-lead-gen.py..."
    python3 "$SCRIPTS_DIR/seller-lead-gen.py" >> "$LOG_DIR/lead-gen.log" 2>&1
    
    echo "[$TIMESTAMP] Running referral-engine-prospects.py..."
    python3 "$SCRIPTS_DIR/referral-engine-prospects.py" >> "$LOG_DIR/lead-gen.log" 2>&1
    
    echo "[$TIMESTAMP] Running referral-engine-providers.py..."
    python3 "$SCRIPTS_DIR/referral-engine-providers.py" >> "$LOG_DIR/lead-gen.log" 2>&1
    
    echo "[$TIMESTAMP] All lead gen scripts completed."
else
    echo "[$TIMESTAMP] Running $SCRIPT..."
    python3 "$SCRIPTS_DIR/$SCRIPT" >> "$LOG_DIR/lead-gen.log" 2>&1
    echo "[$TIMESTAMP] $SCRIPT completed."
fi
