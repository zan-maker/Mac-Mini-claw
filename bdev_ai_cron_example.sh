#!/bin/bash
# bdev_ai_cron_integration.sh
# Example cron job script for Bdev.ai integration

cd /Users/cubiczan/.openclaw/workspace

# Set OpenAI API key (store securely in production)
export OPENAI_API_KEY="your-api-key-here"

# Run Bdev.ai integration
echo "$(date): Starting Bdev.ai integration" >> logs/bdev_ai.log
python3 bdev_ai_integration_main.py --batch-size 50

# Export results to outreach system
if [ -f bdev_ai_outreach_*.csv ]; then
    echo "$(date): Exporting to outreach system" >> logs/bdev_ai.log
    # Add your integration command here
    # Example: python3 send_to_agentmail.py bdev_ai_outreach_*.csv
fi

echo "$(date): Bdev.ai integration completed" >> logs/bdev_ai.log
