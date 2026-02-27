#!/bin/bash
# Start n8n workflow engine
# Requires: Node.js 18+

# Install n8n globally if not installed
if ! command -v n8n &> /dev/null; then
    echo "Installing n8n..."
    npm install -g n8n
fi

# Start n8n
echo "Starting n8n on port 5678..."
N8N_PORT=5678 n8n start
