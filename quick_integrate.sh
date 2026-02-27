#!/bin/bash
# Quick Integration Script for Skill Evolution Framework
# Apply to ANY new agent with one command

set -e

echo "🚀 QUICK INTEGRATION: Skill Evolution Framework"
echo "=============================================="

if [ $# -lt 2 ]; then
    echo "Usage: $0 <agent_name> <skill_directory> [agent_type]"
    echo ""
    echo "Examples:"
    echo "  $0 data-analyzer ~/skills/data-analyzer analytics"
    echo "  $0 content-writer ~/skills/content-writer outreach"
    echo "  $0 custom-agent ~/skills/custom-agent"
    echo ""
    echo "Agent types: trading, analytics, outreach, custom (default)"
    exit 1
fi

AGENT_ID="$1"
SKILL_DIR=$(realpath "$2")
AGENT_TYPE="${3:-custom}"

echo "🔧 Integrating: $AGENT_ID"
echo "   Directory: $SKILL_DIR"
echo "   Type: $AGENT_TYPE"
echo ""

# Check if skill directory exists
if [ ! -d "$SKILL_DIR" ]; then
    echo "⚠️  Creating skill directory: $SKILL_DIR"
    mkdir -p "$SKILL_DIR"
fi

# Check for SKILL.md
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "⚠️  Creating SKILL.md template..."
    cat > "$SKILL_DIR/SKILL.md" << EOF
# ${AGENT_ID//-/ } Agent

## Description
This agent uses the Skill Evolution Framework for autonomous improvement.

## Skills
- skill_1: Primary skill description
- skill_2: Secondary skill description
- skill_3: Support skill description

## Integration Status
✅ Skill Evolution Framework integrated on $(date +%Y-%m-%d)

## How to Track Executions
\`\`\`python
from complete_agent import SkillEvolutionAgent

agent = SkillEvolutionAgent(
    agent_id='$AGENT_ID',
    skill_dir='$SKILL_DIR'
)

# After each execution:
agent.track_execution(
    skill_name='skill_name',
    inputs={...},
    outputs={...},
    metrics={...}
)
\`\`\`
EOF
    echo "✅ Created SKILL.md"
fi

# Run the auto-integration
cd /Users/cubiczan/.openclaw/workspace
python3 skill-evolution/auto_integrate_new_agent.py "$AGENT_ID" "$SKILL_DIR" "$AGENT_TYPE"

echo ""
echo "🎉 INTEGRATION COMPLETE!"
echo ""
echo "📋 Next Steps:"
echo "   1. Review $SKILL_DIR/EVOLUTION_ACTIVE.md"
echo "   2. Add execution tracking to your agent code"
echo "   3. Test with: python3 skill-evolution/evolve_${AGENT_ID//-/_}.py"
echo "   4. Schedule evolution (add to crontab):"
echo ""
echo "      # Daily at 1 AM"
echo "      0 1 * * * cd /Users/cubiczan/.openclaw/workspace && python3 skill-evolution/evolve_${AGENT_ID//-/_}.py >> ~/.openclaw/logs/evolution_${AGENT_ID}.log 2>&1"
echo ""
echo "   5. Monitor: tail -f ~/.openclaw/logs/evolution_${AGENT_ID}.log"
echo ""
echo "✅ Your agent now has autonomous skill evolution capabilities!"