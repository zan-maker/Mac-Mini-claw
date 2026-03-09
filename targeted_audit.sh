#!/bin/bash
# Targeted Security Audit
# Checks specific files for actual secrets

echo "🔒 TARGETED SECURITY AUDIT"
echo "=========================="
echo ""

cd /Users/cubiczan/.openclaw/workspace

# Check specific known problematic files
FILES_TO_AUDIT=(
  "agentmail-test-results.json"
  "test_agentmail_api.py"
  "test_agentmail_pipeline.py"
  "scripts/hybrid-api-monitor.py"
  "social_media/linkedin_auto_poster.py"
  "BROWSER_AUTOMATION_GUIDE.md"
  "AUTOMATION_OPTIONS.md"
)

echo "🔍 Auditing specific files..."
echo ""

for file in "${FILES_TO_AUDIT[@]}"; do
  if [ -f "$file" ]; then
    echo "📄 $file:"
    
    # Check for GitHub tokens
    if grep -q "ghp_" "$file"; then
      echo "   ⚠️  Contains GitHub token pattern"
      grep -n "ghp_" "$file" | head -2
    fi
    
    # Check for OpenAI keys
    if grep -q "sk-" "$file"; then
      echo "   ⚠️  Contains OpenAI key pattern"
      grep -n "sk-" "$file" | head -2
    fi
    
    # Check for generic API keys
    if grep -q "api_key.*=" "$file"; then
      echo "   ⚠️  Contains API key assignment"
      grep -n "api_key.*=" "$file" | head -2
    fi
    
    # Check for bearer tokens
    if grep -q "Bearer " "$file"; then
      echo "   ⚠️  Contains Bearer token"
      grep -n "Bearer " "$file" | head -2
    fi
    
    echo ""
  fi
done

echo "✅ Initial audit complete"
echo ""
echo "🔧 RECOMMENDED IMMEDIATE ACTIONS:"
echo "1. Create .env file template"
echo "2. Update .gitignore"
echo "3. Create secure script templates"
echo ""