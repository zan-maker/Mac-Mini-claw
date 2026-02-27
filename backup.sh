#!/bin/bash
# Daily backup script for OpenClaw workspace
# Repository: https://github.com/zan-maker/Mac-Mini-claw

cd /Users/cubiczan/.openclaw/workspace

# Check if there are changes to commit
if git diff --quiet && git diff --staged --quiet; then
    echo "No changes to backup"
    exit 0
fi

# Add all changes
git add -A

# Create commit with timestamp
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
git commit -m "Automated backup: $TIMESTAMP" --allow-empty

# Push to GitHub
git push origin main

echo "Backup completed at $TIMESTAMP"
