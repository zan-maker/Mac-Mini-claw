#!/bin/bash

# Curated Business Skills Installation Script
# Based on awesome-openclaw-skills repository recommendations

echo "=================================================="
echo "🚀 Installing Curated Business Skills for Phase 2"
echo "=================================================="
echo ""

# Create installation directory
INSTALL_DIR="/Users/cubiczan/mac-bot/skills/curated-business"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

echo "📁 Installation directory: $INSTALL_DIR"
echo ""

# Install Phase 1: Foundation Skills
echo "🎯 PHASE 1: FOUNDATION SKILLS (Week 1)"
echo "======================================"

echo "📦 Installing marketing-mode (23 integrated marketing skills)..."
npx clawhub@latest install marketing-mode 2>&1 | tee marketing-mode-install.log
if [ $? -eq 0 ]; then echo "✅ marketing-mode installed"; else echo "❌ marketing-mode failed"; fi

echo ""
echo "📦 Installing ga4 (Google Analytics 4 integration)..."
npx clawhub@latest install ga4 2>&1 | tee ga4-install.log
if [ $? -eq 0 ]; then echo "✅ ga4 installed"; else echo "❌ ga4 failed"; fi

echo ""
echo "📦 Installing gsc (Google Search Console)..."
npx clawhub@latest install gsc 2>&1 | tee gsc-install.log
if [ $? -eq 0 ]; then echo "✅ gsc installed"; else echo "❌ gsc failed"; fi

echo ""
echo "📦 Installing gamma (AI-powered content creation)..."
npx clawhub@latest install gamma 2>&1 | tee gamma-install.log
if [ $? -eq 0 ]; then echo "✅ gamma installed"; else echo "❌ gamma failed"; fi

# Install Phase 2: Distribution Skills
echo ""
echo "🎯 PHASE 2: DISTRIBUTION SKILLS (Week 2-3)"
echo "=========================================="

echo "📦 Installing kakiyo (LinkedIn automation)..."
npx clawhub@latest install kakiyo 2>&1 | tee kakiyo-install.log
if [ $? -eq 0 ]; then echo "✅ kakiyo installed"; else echo "❌ kakiyo failed"; fi

echo ""
echo "📦 Installing inference-sh (150+ AI apps)..."
npx clawhub@latest install inference-sh 2>&1 | tee inference-sh-install.log
if [ $? -eq 0 ]; then echo "✅ inference-sh installed"; else echo "❌ inference-sh failed"; fi

echo ""
echo "📦 Installing hubspot (CRM integration)..."
npx clawhub@latest install hubspot 2>&1 | tee hubspot-install.log
if [ $? -eq 0 ]; then echo "✅ hubspot installed"; else echo "❌ hubspot failed"; fi

# Install Phase 3: Intelligence Skills
echo ""
echo "🎯 PHASE 3: INTELLIGENCE SKILLS (Week 4+)"
echo "=========================================="

echo "📦 Installing bluesky (emerging social platform)..."
npx clawhub@latest install bluesky 2>&1 | tee bluesky-install.log
if [ $? -eq 0 ]; then echo "✅ bluesky installed"; else echo "❌ bluesky failed"; fi

echo ""
echo "📦 Installing x-search (Twitter intelligence)..."
npx clawhub@latest install x-search 2>&1 | tee x-search-install.log
if [ $? -eq 0 ]; then echo "✅ x-search installed"; else echo "❌ x-search failed"; fi

echo ""
echo "📦 Installing news-aggregator-skill (content curation)..."
npx clawhub@latest install news-aggregator-skill 2>&1 | tee news-aggregator-install.log
if [ $? -eq 0 ]; then echo "✅ news-aggregator-skill installed"; else echo "❌ news-aggregator-skill failed"; fi

# Create summary
echo ""
echo "=================================================="
echo "📊 INSTALLATION SUMMARY"
echo "=================================================="

echo ""
echo "📋 Installed Skills:"
echo "-------------------"
for logfile in *-install.log; do
    skill_name=$(echo "$logfile" | sed 's/-install.log//')
    if grep -q "installed" "$logfile" 2>/dev/null || [ $? -eq 0 ]; then
        echo "✅ $skill_name"
    else
        echo "❌ $skill_name (check ${logfile})"
    fi
done

echo ""
echo "📁 Skill Directories:"
echo "-------------------"
ls -la "$INSTALL_DIR"

echo ""
echo "🚀 Next Steps:"
echo "1. Review installation logs in: $INSTALL_DIR"
echo "2. Check each skill's SKILL.md for usage instructions"
echo "3. Configure API keys and credentials"
echo "4. Test with: /marketing-mode help"
echo "5. Begin Phase 1 implementation"

echo ""
echo "📚 Documentation:"
echo "• Workflow: /Users/cubiczan/.openclaw/workspace/curated_skills_workflow.md"
echo "• Plan: /Users/cubiczan/.openclaw/workspace/curated_skills_integration_plan.md"

echo ""
echo "🎉 Installation complete! Ready for Phase 2 implementation."