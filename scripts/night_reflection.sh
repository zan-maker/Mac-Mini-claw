#!/bin/bash
# Night Reflection Script for MetaClaw
# Runs at 2:00 AM daily for automatic learning

echo "🧠 META-CLAW NIGHT REFLECTION - $(date)"
echo "=========================================="

# Ensure MetaClaw is running
if ! curl -s http://localhost:30000/health > /dev/null; then
    echo "Starting MetaClaw..."
    metaclaw start &
    sleep 10
fi

# Create night reflection task
cat > /tmp/night_reflection.jsonl << 'TASKS'
{"task_id": "night_reflection_$(date +%Y%m%d)", "instruction": "Analyze today's conversations and extract learning insights. Focus on: 1. Successful patterns to reinforce, 2. Failure lessons to learn from, 3. New skills to create, 4. Improvements for tomorrow."}
TASKS

echo "✅ Night reflection task created"
echo "📊 MetaClaw will analyze today's conversations and evolve skills"

# The actual analysis happens through normal OpenClaw usage
# MetaClaw auto-evolves skills after each conversation
