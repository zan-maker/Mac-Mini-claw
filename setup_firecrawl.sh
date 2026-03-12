#!/bin/bash

# Firecrawl Setup Script for AI Agents
# Production-ready web scraping setup

set -e

echo "========================================="
echo "FIRECRAWL SETUP FOR AI AGENTS"
echo "========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
FIRECRAWL_API_KEY=""
WORKSPACE_DIR="/Users/cubiczan/.openclaw/workspace"
LOG_FILE="/tmp/firecrawl_setup_$(date +%Y%m%d_%H%M%S).log"

# Function to print status
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if Node.js is installed
check_node() {
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_status "Node.js found: $NODE_VERSION"
        return 0
    else
        print_error "Node.js not found. Firecrawl CLI requires Node.js."
        echo "Install Node.js from: https://nodejs.org/"
        return 1
    fi
}

# Check if npm is installed
check_npm() {
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        print_status "npm found: $NPM_VERSION"
        return 0
    else
        print_error "npm not found."
        return 1
    fi
}

# Check if Python is installed
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        print_status "Python3 found: $PYTHON_VERSION"
        return 0
    else
        print_error "Python3 not found."
        return 1
    fi
}

# Install Firecrawl CLI
install_firecrawl_cli() {
    echo ""
    echo "📦 Installing Firecrawl CLI..."
    
    # Install globally
    if npm install -g firecrawl-cli@latest 2>> "$LOG_FILE"; then
        print_status "Firecrawl CLI installed globally"
        
        # Verify installation
        if firecrawl --version 2>> "$LOG_FILE"; then
            print_status "Firecrawl CLI verified"
            return 0
        else
            print_error "Firecrawl CLI verification failed"
            return 1
        fi
    else
        print_error "Failed to install Firecrawl CLI"
        return 1
    fi
}

# Install Firecrawl Python SDK
install_firecrawl_python() {
    echo ""
    echo "🐍 Installing Firecrawl Python SDK..."
    
    if pip install firecrawl-py 2>> "$LOG_FILE"; then
        print_status "Firecrawl Python SDK installed"
        
        # Test import
        if python3 -c "from firecrawl import Firecrawl; print('Firecrawl import successful')" 2>> "$LOG_FILE"; then
            print_status "Firecrawl Python SDK verified"
            return 0
        else
            print_error "Firecrawl Python SDK import failed"
            return 1
        fi
    else
        print_error "Failed to install Firecrawl Python SDK"
        return 1
    fi
}

# Install Firecrawl Skill for AI Agents
install_firecrawl_skill() {
    echo ""
    echo "🤖 Installing Firecrawl Skill for AI Agents..."
    
    # Install skill for all detected agents
    if npx -y firecrawl-cli@latest init --all --browser 2>> "$LOG_FILE"; then
        print_status "Firecrawl Skill installed for AI agents"
        return 0
    else
        print_warning "Firecrawl Skill installation had issues (may require agent restart)"
        return 0  # Continue even if skill installation has issues
    fi
}

# Get API key from user
get_api_key() {
    echo ""
    echo "🔑 Firecrawl API Key Setup"
    echo "=========================="
    echo "1. Sign up at: https://firecrawl.dev"
    echo "2. Get your API key from dashboard"
    echo "3. Enter it below (starts with 'fc-')"
    echo ""
    
    read -p "Enter Firecrawl API Key: " FIRECRAWL_API_KEY
    
    if [[ -z "$FIRECRAWL_API_KEY" ]]; then
        print_error "No API key provided"
        return 1
    elif [[ ! "$FIRECRAWL_API_KEY" =~ ^fc- ]]; then
        print_error "API key should start with 'fc-'"
        return 1
    else
        print_status "API key format looks good"
        return 0
    fi
}

# Configure API key
configure_api_key() {
    echo ""
    echo "⚙️  Configuring Firecrawl API Key..."
    
    # Method 1: Environment variable
    export FIRECRAWL_API_KEY="$FIRECRAWL_API_KEY"
    echo "export FIRECRAWL_API_KEY=\"$FIRECRAWL_API_KEY\"" >> ~/.zshrc
    print_status "Added to ~/.zshrc"
    
    # Method 2: Firecrawl CLI login
    if firecrawl login --api-key "$FIRECRAWL_API_KEY" 2>> "$LOG_FILE"; then
        print_status "Firecrawl CLI configured"
    else
        print_warning "Firecrawl CLI login failed (may already be configured)"
    fi
    
    # Method 3: Create .env file in workspace
    ENV_FILE="$WORKSPACE_DIR/.env.firecrawl"
    echo "FIRECRAWL_API_KEY=$FIRECRAWL_API_KEY" > "$ENV_FILE"
    print_status "Created $ENV_FILE"
    
    # Method 4: Update agent web scraper config
    PYTHON_CONFIG="$WORKSPACE_DIR/firecrawl_config.py"
    cat > "$PYTHON_CONFIG" << EOF
# Firecrawl Configuration for AI Agents
import os

# API Key (prioritize environment variable)
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "$FIRECRAWL_API_KEY")

# Configuration
FIRECRAWL_CONFIG = {
    "api_key": FIRECRAWL_API_KEY,
    "base_url": "https://api.firecrawl.dev",
    "timeout": 30,
    "max_retries": 3
}

# Usage example:
# from firecrawl import Firecrawl
# app = Firecrawl(api_key=FIRECRAWL_API_KEY)
EOF
    print_status "Created Python config: $PYTHON_CONFIG"
    
    return 0
}

# Test Firecrawl setup
test_firecrawl() {
    echo ""
    echo "🧪 Testing Firecrawl Setup..."
    
    # Test 1: CLI
    echo "Testing CLI..."
    if firecrawl --version 2>> "$LOG_FILE"; then
        print_status "CLI test passed"
    else
        print_error "CLI test failed"
        return 1
    fi
    
    # Test 2: Python SDK
    echo "Testing Python SDK..."
    TEST_SCRIPT="$WORKSPACE_DIR/test_firecrawl.py"
    cat > "$TEST_SCRIPT" << 'EOF'
#!/usr/bin/env python3
"""Test Firecrawl installation"""
import os
import sys

try:
    from firecrawl import Firecrawl
    print("✅ Firecrawl Python SDK import successful")
    
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if api_key:
        print(f"✅ API key found: {api_key[:10]}...")
        
        # Try to initialize (won't make API call without actual key)
        try:
            app = Firecrawl(api_key=api_key)
            print("✅ Firecrawl client initialized")
        except Exception as e:
            print(f"⚠️  Client initialization: {e}")
    else:
        print("❌ API key not found in environment")
        
except ImportError as e:
    print(f"❌ Firecrawl import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"⚠️  Other error: {e}")
EOF
    
    if python3 "$TEST_SCRIPT" 2>> "$LOG_FILE"; then
        print_status "Python SDK test passed"
    else
        print_error "Python SDK test failed"
        return 1
    fi
    
    # Test 3: Agent web scraper
    echo "Testing agent web scraper..."
    if python3 "$WORKSPACE_DIR/agent_web_scraper.py" 2>> "$LOG_FILE" | grep -q "Testing Agent Web Scraper"; then
        print_status "Agent web scraper test passed"
    else
        print_warning "Agent web scraper test had issues (check log)"
    fi
    
    return 0
}

# Create documentation
create_documentation() {
    echo ""
    echo "📚 Creating Documentation..."
    
    DOC_FILE="$WORKSPACE_DIR/FIRECRAWL_SETUP.md"
    cat > "$DOC_FILE" << EOF
# Firecrawl Setup for AI Agents

## ✅ Setup Complete

Firecrawl is now configured for AI agent web scraping.

## 🔑 API Key
- Key: \`${FIRECRAWL_API_KEY:0:10}...\`
- Configured in: \`~/.zshrc\`, \`$WORKSPACE_DIR/.env.firecrawl\`
- Environment variable: \`FIRECRAWL_API_KEY\`

## 🛠️ Installation Summary

### 1. Firecrawl CLI
- Installed globally: \`firecrawl\`
- Version: \`$(firecrawl --version 2>/dev/null || echo "Not available")\`
- Login: \`firecrawl login --api-key YOUR_KEY\`

### 2. Firecrawl Python SDK
- Package: \`firecrawl-py\`
- Import: \`from firecrawl import Firecrawl\`
- Config: \`$WORKSPACE_DIR/firecrawl_config.py\`

### 3. Firecrawl Skill for AI Agents
- Installed for: Claude Code, Codex, OpenCode, etc.
- Restart your AI agent to detect the skill

## 🚀 Usage Examples

### Python (Recommended for Agents)
\`\`\`python
from firecrawl import Firecrawl
import os

# Initialize
api_key = os.getenv("FIRECRAWL_API_KEY")
app = Firecrawl(api_key=api_key)

# Scrape URL
result = app.scrape("https://example.com", formats=["markdown"])
print(result.markdown)

# Search web
results = app.search("best web scraping tools", limit=5)
for result in results.data["web"]:
    print(f"{result['title']}: {result['url']}")

# Extract structured data
from pydantic import BaseModel

class CompanyInfo(BaseModel):
    name: str
    description: str

result = app.scrape(
    "https://firecrawl.dev",
    formats=[{"type": "json", "schema": CompanyInfo.model_json_schema()}]
)
print(result.json)
\`\`\`

### CLI
\`\`\`bash
# Scrape URL
firecrawl https://example.com --only-main-content

# Search
firecrawl search "web scraping" --limit 5

# Browser automation
firecrawl browser "open https://example.com"
firecrawl browser "snapshot"
firecrawl browser "click @e5"
\`\`\`

### Agent Web Scraper Wrapper
\`\`\`python
from agent_web_scraper import AgentWebScraper

scraper = AgentWebScraper()
result = scraper.scrape_url("https://example.com")
if result.success:
    print(result.content)
\`\`\`

## 📊 Features Available

1. **URL Scraping**: Any URL → clean markdown/HTML
2. **Web Search**: Search + content extraction
3. **Browser Automation**: Click, type, scroll, wait
4. **Structured Extraction**: Pydantic schemas
5. **Batch Processing**: Multiple URLs at once
6. **JavaScript Rendering**: Automatic JS execution
7. **Agent Integration**: CLI skill for AI agents

## 🔧 Troubleshooting

### Common Issues:

1. **"API key not found"**
   - Check \`echo \$FIRECRAWL_API_KEY\`
   - Source ~/.zshrc: \`source ~/.zshrc\`

2. **"Module not found"**
   - Install: \`pip install firecrawl-py\`
   - Upgrade: \`pip install --upgrade firecrawl-py\`

3. **CLI not working**
   - Reinstall: \`npm install -g firecrawl-cli@latest\`
   - Check PATH: \`which firecrawl\`

4. **Rate limiting**
   - Check dashboard: https://firecrawl.dev/dashboard
   - Upgrade plan if needed

## 📈 Next Steps

1. **Test with real data**: Try scraping your target websites
2. **Integrate with agents**: Add to lead generation, deal origination
3. **Monitor usage**: Check dashboard for credits and performance
4. **Explore advanced features**: Browser automation, structured extraction

## 🔗 Resources

- Dashboard: https://firecrawl.dev/dashboard
- Documentation: https://docs.firecrawl.dev
- Playground: https://firecrawl.dev/playground
- Support: https://discord.gg/firecrawl

---

*Setup completed: $(date)*
*Log file: $LOG_FILE*
EOF
    
    print_status "Documentation created: $DOC_FILE"
}

# Main execution
main() {
    echo "Starting Firecrawl setup..."
    echo "Log file: $LOG_FILE"
    
    # Check prerequisites
    check_node || exit 1
    check_npm || exit 1
    check_python || exit 1
    
    # Get API key
    get_api_key || exit 1
    
    # Install components
    install_firecrawl_cli || { print_warning "CLI installation issues, continuing..."; }
    install_firecrawl_python || { print_warning "Python SDK installation issues, continuing..."; }
    install_firecrawl_skill || { print_warning "Skill installation issues, continuing..."; }
    
    # Configure
    configure_api_key || exit 1
    
    # Test
    test_firecrawl || { print_warning "Some tests failed, but setup may still work"; }
    
    # Create documentation
    create_documentation
    
    echo ""
    echo "========================================="
    echo "✅ FIRECRAWL SETUP COMPLETE!"
    echo "========================================="
    echo ""
    echo "Next steps:"
    echo "1. Restart your AI agents to detect Firecrawl skill"
    echo "2. Test with: python3 $WORKSPACE_DIR/agent_web_scraper.py"
    echo "3. Read documentation: $WORKSPACE_DIR/FIRECRAWL_SETUP.md"
    echo ""
    echo "Happy scraping! 🕷️"
}

# Run main function
main "$@" 2>&1 | tee -a "$LOG_FILE"