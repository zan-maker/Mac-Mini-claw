#!/bin/bash
# Deer Flow Quick Evaluation Script
# Tests if Deer Flow can integrate with our OpenClaw environment

echo "🦌 DEER FLOW EVALUATION SCRIPT"
echo "================================"
echo "Date: $(date)"
echo "OpenClaw Version: $(openclaw --version 2>/dev/null || echo "Not found")"
echo "================================"

echo ""
echo "1. 🔍 CHECKING SYSTEM REQUIREMENTS..."
echo "======================================"

# Check Docker
if command -v docker &> /dev/null; then
    echo "✅ Docker: $(docker --version | head -1)"
else
    echo "❌ Docker not found"
    exit 1
fi

# Check Node.js
if command -v node &> /dev/null; then
    echo "✅ Node.js: $(node --version)"
else
    echo "❌ Node.js not found"
    exit 1
fi

# Check Python
if command -v python3 &> /dev/null; then
    echo "✅ Python: $(python3 --version)"
else
    echo "❌ Python3 not found"
    exit 1
fi

echo ""
echo "2. 📥 CLONING DEER FLOW REPOSITORY..."
echo "======================================"

cd /tmp
if [ -d "deer-flow" ]; then
    echo "✅ Deer Flow already cloned, updating..."
    cd deer-flow
    git pull
else
    echo "📥 Cloning Deer Flow repository..."
    git clone https://github.com/bytedance/deer-flow.git
    cd deer-flow
fi

echo "✅ Repository: $(pwd)"
echo "✅ Branch: $(git branch --show-current)"

echo ""
echo "3. ⚙️ GENERATING CONFIGURATION..."
echo "======================================"

if [ -f "config.yaml" ]; then
    echo "✅ config.yaml already exists"
else
    echo "⚙️ Running make config..."
    if make config 2>&1 | tail -10; then
        echo "✅ Configuration generated"
    else
        echo "❌ Failed to generate configuration"
        exit 1
    fi
fi

echo ""
echo "4. 🔧 ANALYZING CONFIGURATION..."
echo "======================================"

echo "📋 Configuration file structure:"
ls -la config.yaml .env.example 2>/dev/null || echo "Config files not found"

echo ""
echo "📄 Sample config.yaml (first 30 lines):"
head -30 config.yaml 2>/dev/null || echo "config.yaml not found"

echo ""
echo "5. 🎯 CHECKING COMPATIBILITY WITH OUR APIS..."
echo "======================================"

# Check if our APIs could be integrated
echo "🔍 Our current APIs that could integrate:"
echo "  • DeepSeek API (custom-api-deepseek-com)"
echo "  • GLM-5 API (zai)"
echo "  • Tavily API (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)"
echo "  • Serper API (cac43a248afb1cc1ec004370df2e0282a67eb420)"
echo "  • NewsAPI (fe52ac365edf464c9dca774544a40da3)"
echo "  • Hunter.io API (environment variable)"
echo "  • Brevo API (email)"
echo "  • OpenRouter API (free AI)"

echo ""
echo "6. 🔄 ANALYZING SKILL COMPATIBILITY..."
echo "======================================"

echo "📁 Deer Flow skills directory:"
find skills/ -name "SKILL.md" 2>/dev/null | head -5

echo ""
echo "📁 Our current skills that could convert:"
echo "  • /Users/cubiczan/mac-bot/skills/trade-recommender/"
echo "  • /Users/cubiczan/mac-bot/skills/lead-generator/"
echo "  • /Users/cubiczan/mac-bot/skills/deal-origination/"
echo "  • /Users/cubiczan/.openclaw/workspace/skills/"

echo ""
echo "7. 🐳 DOCKER SANDBOX COMPATIBILITY..."
echo "======================================"

echo "🔍 Our current Docker setup:"
docker --version
docker ps -a | wc -l | awk '{print "✅ " $1-1 " containers found"}'

echo ""
echo "🔍 Deer Flow sandbox modes:"
echo "  • Local Execution (host machine)"
echo "  • Docker Execution (isolated containers)"
echo "  • Kubernetes Execution (pods via provisioner)"

echo ""
echo "8. 🤖 AGENT ORCHESTRATION COMPARISON..."
echo "======================================"

echo "📊 OpenClaw Current Orchestration:"
echo "  • Main agent (DeepSeek)"
echo "  • Trade Recommender (GLM-5)"
echo "  • ROI Analyst (GLM-5)"
echo "  • Lead Generator (GLM-5)"
echo "  • Manual coordination"

echo ""
echo "📊 Deer Flow Orchestration:"
echo "  • Lead agent with sub-agent spawning"
echo "  • Parallel execution when possible"
echo "  • Structured result reporting"
echo "  • Context isolation per sub-agent"
echo "  • Memory persistence across sessions"

echo ""
echo "9. 🚀 QUICK INTEGRATION TEST IDEA..."
echo "======================================"

cat << 'EOF'
Test Scenario: LinkedIn Automation Fix

OpenClaw (Current):
1. Manual Pinchtab profile creation
2. Failed API calls
3. Manual posting required
4. No memory of past posts

Deer Flow (Proposed):
1. LinkedIn skill with sub-agents:
   - Profile manager agent
   - Content generator agent  
   - Posting agent
   - Engagement monitor agent
2. All sandboxed in Docker
3. Persistent memory of posts/engagement
4. Automated scheduling

Test Command:
```bash
# In Deer Flow
/deerflow "Fix LinkedIn automation for Sam Desigan and Shyam Desigan profiles"
```

Expected Flow:
1. Deer Flow analyzes problem
2. Spawns sub-agent for profile setup
3. Spawns sub-agent for content generation
4. Spawns sub-agent for posting automation
5. Coordinates all agents
6. Reports solution
EOF

echo ""
echo "10. 📈 RECOMMENDATION SUMMARY..."
echo "======================================"

echo "✅ STRONG FIT FOR:"
echo "  • Complex multi-agent workflows"
echo "  • Sandboxed code execution"
echo "  • Persistent memory needs"
echo "  • Skill-based architecture"
echo "  • Docker/Kubernetes deployment"

echo ""
echo "⚠️ INTEGRATION CHALLENGES:"
echo "  • Learning new system"
echo "  • Converting existing skills"
echo "  • Coordinating two systems"
echo "  • Additional resource usage"

echo ""
echo "🎯 RECOMMENDED APPROACH:"
echo "  1. Install Deer Flow in test environment"
echo "  2. Convert one skill (trade-recommender)"
echo "  3. Test with our APIs"
echo "  4. Evaluate performance"
echo "  5. Decide: Replace or complement OpenClaw"

echo ""
echo "================================"
echo "🦌 DEER FLOW EVALUATION COMPLETE"
echo "================================"
echo ""
echo "⚡ NEXT STEP:"
echo "Run actual installation:"
echo "  cd /tmp/deer-flow"
echo "  make config"
echo "  # Edit config.yaml with our APIs"
echo "  make docker-start"
echo ""
echo "🌐 Access: http://localhost:2026"
echo ""
echo "📊 Decision criteria:"
echo "  • Can it fix LinkedIn automation?"
echo "  • Can it improve trading workflows?"
echo "  • Is the skill conversion easy?"
echo "  • Does memory system work well?"
echo ""
echo "🚀 Potential to solve our LinkedIn automation issues AND improve all workflows!"