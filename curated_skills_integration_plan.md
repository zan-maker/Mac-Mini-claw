#!/bin/bash
# Installation script for curated business skills from awesome-openclaw-skills

echo "🚀 Installing Curated Business Skills for Phase 2"
echo "=================================================="

# Create installation directory
INSTALL_DIR="/Users/cubiczan/mac-bot/skills/curated-business"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

echo "📁 Installation directory: $INSTALL_DIR"
echo ""

# Function to install skill with error handling
install_skill() {
    local skill_name=$1
    local skill_id=$2
    local priority=$3
    
    echo "📦 Installing $skill_name ($skill_id)..."
    echo "   Priority: $priority"
    
    # Create skill directory
    mkdir -p "$skill_id"
    cd "$skill_id"
    
    # Install via ClawHub
    echo "   Running: npx clawhub@latest install $skill_id"
    npx clawhub@latest install "$skill_id" 2>&1 | tee install.log
    
    if [ $? -eq 0 ]; then
        echo "   ✅ $skill_name installed successfully"
        
        # Create metadata
        cat > METADATA.json << EOF
{
  "id": "$skill_id",
  "name": "$skill_name",
  "source": "awesome-openclaw-skills",
  "installed_at": "$(date -Iseconds)",
  "priority": "$priority",
  "status": "installed",
  "integration_phase": 2
}
EOF
        
        # Check if SKILL.md exists, create stub if not
        if [ ! -f "SKILL.md" ]; then
            cat > SKILL.md << EOF
# $skill_name

Installed from awesome-openclaw-skills repository.

**Source:** https://github.com/VoltAgent/awesome-openclaw-skills

**Install Command:** \`npx clawhub@latest install $skill_id\`

**Status:** Installed $(date)

## Integration Notes
This skill is part of Phase 2: Content + Analytics + Business Intelligence expansion.

## Usage
Refer to the skill's original documentation for usage instructions.
EOF
        fi
        
    else
        echo "   ❌ Failed to install $skill_name"
        echo "   Check install.log for details"
    fi
    
    cd ..
    echo ""
}

# Phase 1: Foundation Skills (Week 1)
echo "🎯 PHASE 1: FOUNDATION SKILLS"
echo "=============================="

install_skill "Marketing Mode" "marketing-mode" "HIGHEST"
install_skill "Google Analytics 4" "ga4" "HIGHEST"
install_skill "Google Search Console" "gsc" "HIGH"
install_skill "Gamma Content Creator" "gamma" "HIGH"

# Phase 2: Distribution Skills (Week 2-3)
echo "🎯 PHASE 2: DISTRIBUTION SKILLS"
echo "================================"

install_skill "Kakiyo LinkedIn Automation" "kakiyo" "HIGH"
install_skill "Inference.sh AI Apps" "inference-sh" "HIGH"
install_skill "HubSpot CRM" "hubspot" "HIGH"

# Phase 3: Intelligence Skills (Week 4+)
echo "🎯 PHASE 3: INTELLIGENCE SKILLS"
echo "================================"

install_skill "Bluesky Social" "bluesky" "MEDIUM"
install_skill "X-Search Twitter Intelligence" "x-search" "MEDIUM"
install_skill "News Aggregator" "news-aggregator-skill" "MEDIUM"

echo "=================================================="
echo "📊 INSTALLATION SUMMARY"
echo "=================================================="

# Count installed skills
INSTALLED_COUNT=$(find . -name "METADATA.json" | wc -l | tr -d ' ')
echo "✅ Installed skills: $INSTALLED_COUNT/10"

# List installed skills
echo ""
echo "📋 Installed Skills:"
for skill_dir in */; do
    if [ -f "$skill_dir/METADATA.json" ]; then
        skill_name=$(grep -o '"name": "[^"]*"' "$skill_dir/METADATA.json" | head -1 | cut -d'"' -f4)
        skill_id=$(basename "$skill_dir")
        echo "  • $skill_name ($skill_id)"
    fi
done

echo ""
echo "🚀 Next Steps:"
echo "1. Review installed skills in: $INSTALL_DIR"
echo "2. Check SKILL.md files for usage instructions"
echo "3. Test integration with existing lead generation system"
echo "4. Begin Phase 1 implementation (marketing-mode + ga4 + gamma)"

echo ""
echo "📚 Documentation created:"
echo "  • /Users/cubiczan/.openclaw/workspace/curated_skills_integration_plan.md"
echo "  • /Users/cubiczan/.openclaw/workspace/curated_skills_workflow.md"

echo ""
echo "🎉 Phase 2 skills installation complete!"