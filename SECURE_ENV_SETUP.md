# SECURE ENVIRONMENT SETUP

## 1. Create .env file (ADD TO .gitignore!)
```bash
# Create .env file - NEVER COMMIT THIS!
cat > .env << 'EOF'
# GITHUB
GITHUB_TOKEN=your_personal_access_token_here

# OPENAI / AI SERVICES
OPENAI_API_KEY=sk-your_key_here
DEEPSEEK_API_KEY=your_deepseek_key_here
TAVILY_API_KEY=your_tavily_key_here

# EMAIL & OUTREACH
AGENTMAIL_API_KEY=your_agentmail_key_here
ZEROBOUNCE_API_KEY=your_zerobounce_key_here
HUNTER_IO_API_KEY=your_hunter_key_here

# SEARCH & DATA
SERPER_API_KEY=your_serper_key_here
ZEMBRA_API_KEY=your_zembra_key_here

# VOICE & AUTOMATION
VAPI_API_KEY=your_vapi_key_here

# FINANCIAL
ALPACA_API_KEY=your_alpaca_key_here
ALPACA_SECRET_KEY=your_alpaca_secret_here
WEBULL_ACCESS_TOKEN=your_webull_token_here

# DATABASE
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here

# SOCIAL MEDIA
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_secret

# OTHER
STRIPE_API_KEY=your_stripe_key_here
XAI_API_KEY=your_xai_key_here
EOF

# Make it read-only
chmod 600 .env
```

## 2. Update .gitignore
```bash
# Add to .gitignore
cat >> .gitignore << 'EOF'

# SECURITY - NEVER COMMIT
.env
.env.*
*.secret
*.key
*.token
*.password
credentials*
config/private/
secrets/

# SESSION DATA
*.session
*.cookie
*.cache

# LOCAL DATA
logs/
data/local/
temp/
tmp/
EOF
```

## 3. Create Secure Script Template
```python
#!/usr/bin/env python3
"""
Secure Script Template - Uses environment variables
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_env_var(name, required=True):
    """Safely get environment variable"""
    value = os.environ.get(name)
    if required and not value:
        print(f"❌ ERROR: {name} environment variable not set")
        print(f"   Add it to your .env file or export it")
        sys.exit(1)
    return value

# Example usage
if __name__ == "__main__":
    # Get API keys securely
    github_token = get_env_var("GITHUB_TOKEN")
    openai_key = get_env_var("OPENAI_API_KEY")
    
    print(f"✅ GitHub token: {github_token[:10]}...")
    print(f"✅ OpenAI key: {openai_key[:10]}...")
```

## 4. Install Required Package
```bash
pip install python-dotenv
```

## 5. Update Existing Scripts
For each script with hardcoded secrets:
1. Remove hardcoded values
2. Add `from dotenv import load_dotenv`
3. Add `load_dotenv()` at start
4. Replace `"hardcoded_value"` with `os.environ.get("ENV_VAR_NAME")`

## 6. Security Verification Script
```python
#!/usr/bin/env python3
"""
Security verification - checks for hardcoded secrets
"""

import re
import os

def check_file_for_secrets(filepath):
    """Check a file for common secret patterns"""
    patterns = [
        (r'ghp_[A-Za-z0-9]{36}', "GitHub Token"),
        (r'sk-[A-Za-z0-9]{48}', "OpenAI Key"),
        (r'Bearer\s+[A-Za-z0-9._-]{20,}', "Bearer Token"),
        (r'api_key\s*=\s*["\'][A-Za-z0-9._-]{20,}["\']', "API Key"),
        (r'secret\s*=\s*["\'][A-Za-z0-9._-]{20,}["\']', "Secret"),
    ]
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    issues = []
    for pattern, name in patterns:
        matches = re.findall(pattern, content)
        if matches:
            issues.append(f"{name}: {len(matches)} found")
    
    return issues

# Run check
if __name__ == "__main__":
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(('.py', '.json', '.md', '.sh')):
                filepath = os.path.join(root, file)
                issues = check_file_for_secrets(filepath)
                if issues:
                    print(f"⚠️  {filepath}:")
                    for issue in issues:
                        print(f"   - {issue}")
```

## 7. Pre-commit Hook
```bash
# .git/hooks/pre-commit
#!/bin/bash
echo "🔒 Running security check..."
python3 security_check.py
if [ $? -ne 0 ]; then
    echo "❌ Security check failed - commit blocked"
    exit 1
fi
echo "✅ Security check passed"
exit 0
```

## 8. Immediate Actions
1. **Create .env file** with all your actual keys
2. **Update .gitignore** to exclude sensitive files
3. **Run security check** on all scripts
4. **Update 2 critical files** found in audit
5. **Test** that everything works with env vars

## 9. Long-term Security
- Regular security audits
- Use GitHub Secrets for CI/CD
- Rotate keys periodically
- Monitor for unauthorized access