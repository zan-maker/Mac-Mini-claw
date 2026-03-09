#!/bin/bash
# Security Cleanup Script
# Removes any API keys, tokens, or secrets from tracked files

echo "🔒 SECURITY CLEANUP SCRIPT"
echo "=========================="
echo ""

WORKSPACE="/Users/cubiczan/.openclaw/workspace"
cd "$WORKSPACE"

echo "📋 Checking for sensitive information in recent commits..."
echo ""

# List of patterns to check for
SENSITIVE_PATTERNS=(
  "ghp_[A-Za-z0-9]"
  "sk-[A-Za-z0-9]"
  "Bearer "
  "token:"
  "secret:"
  "password:"
  "api[_-]key"
  "client[_-]secret"
  "access[_-]token"
)

echo "🔍 Scanning files in recent commits..."
FILES_TO_CHECK=$(git log --name-only --oneline -10 | grep -E "\.(json|md|py|sh|txt|cfg|conf|config|yml|yaml)$" | sort -u)

SAFE_FILES=()
NEEDS_REVIEW=()

for file in $FILES_TO_CHECK; do
  if [ -f "$file" ]; then
    # Check if file contains sensitive patterns
    FOUND=false
    for pattern in "${SENSITIVE_PATTERNS[@]}"; do
      if grep -qi "$pattern" "$file" 2>/dev/null; then
        FOUND=true
        break
      fi
    done
    
    if $FOUND; then
      NEEDS_REVIEW+=("$file")
      echo "⚠️  $file - MAY contain sensitive info"
    else
      SAFE_FILES+=("$file")
    fi
  fi
done

echo ""
echo "📊 RESULTS:"
echo "✅ Safe files: ${#SAFE_FILES[@]}"
echo "⚠️  Files needing review: ${#NEEDS_REVIEW[@]}"
echo ""

if [ ${#NEEDS_REVIEW[@]} -gt 0 ]; then
  echo "🔧 RECOMMENDED ACTIONS:"
  echo "1. Review these files for actual secrets:"
  for file in "${NEEDS_REVIEW[@]}"; do
    echo "   - $file"
  done
  echo ""
  echo "2. If secrets are found, use:"
  echo "   git filter-branch or BFG Repo-Cleaner"
  echo ""
  echo "3. For future security:"
  echo "   - Use .gitignore for sensitive files"
  echo "   - Use environment variables"
  echo "   - Use .env files (add to .gitignore)"
  echo "   - Use GitHub Secrets for CI/CD"
fi

echo ""
echo "🔐 SECURITY BEST PRACTICES:"
echo "1. NEVER commit API keys, tokens, or secrets"
echo "2. Use .env files with .gitignore"
echo "3. Use environment variables in production"
echo "4. Use GitHub Secrets for workflows"
echo "5. Regular security audits"
echo ""
echo "✅ Cleanup check complete"