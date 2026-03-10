#!/bin/bash
# code-container-install.sh
# Install and configure code-container for OpenClaw

set -e  # Exit on error

echo "🎯 CODE-CONTAINER INSTALLATION FOR OPENCLAW"
echo "=========================================="

# Check if running on macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo "❌ This script is designed for macOS"
    exit 1
fi

# Configuration
OPENCLAW_HOME="/Users/cubiczan/.openclaw"
WORKSPACE="$OPENCLAW_HOME/workspace"
CONTAINERS_DIR="$OPENCLAW_HOME/containers"
CODE_CONTAINER_DIR="$CONTAINERS_DIR/code-container"

echo "📁 Setting up directories..."
mkdir -p "$CONTAINERS_DIR"/{projects,scripts,config,logs}

# Step 1: Check Docker
echo "🔧 Step 1: Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not installed"
    echo "📦 Installing Docker via Homebrew..."
    
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew not installed. Installing Homebrew first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    brew install --cask docker
    echo "✅ Docker installed via Homebrew"
    echo "⚠️  Please open Docker Desktop to complete installation"
    echo "⚠️  Then run this script again"
    exit 0
else
    echo "✅ Docker is already installed"
    docker --version
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running"
    echo "⚠️  Please start Docker Desktop and run this script again"
    exit 1
fi
echo "✅ Docker is running"

# Step 2: Clone code-container
echo ""
echo "🔧 Step 2: Cloning code-container repository..."
if [ -d "$CODE_CONTAINER_DIR" ]; then
    echo "✅ code-container already exists at $CODE_CONTAINER_DIR"
    cd "$CODE_CONTAINER_DIR"
    git pull
else
    cd "$CONTAINERS_DIR"
    git clone https://github.com/kevinMEH/code-container.git
    echo "✅ code-container cloned to $CODE_CONTAINER_DIR"
fi

# Step 3: Make container script executable
echo ""
echo "🔧 Step 3: Setting up container script..."
cd "$CODE_CONTAINER_DIR"
chmod +x container.sh

# Create symlink if it doesn't exist
if [ ! -f /usr/local/bin/container ]; then
    echo "🔗 Creating symlink to /usr/local/bin/container..."
    sudo ln -sf "$CODE_CONTAINER_DIR/container.sh" /usr/local/bin/container
    echo "✅ Symlink created"
else
    echo "✅ Symlink already exists"
fi

# Step 4: Copy AI harness configurations
echo ""
echo "🔧 Step 4: Copying AI harness configurations..."
mkdir -p "$CODE_CONTAINER_DIR"/{.opencode,.codex,.claude}

# Copy OpenCode config
if [ -d "$HOME/.config/opencode" ]; then
    cp -R "$HOME/.config/opencode/" "$CODE_CONTAINER_DIR/.opencode/"
    echo "✅ Copied OpenCode configuration"
else
    echo "⚠️  OpenCode configuration not found (expected at ~/.config/opencode/)"
fi

# Copy Codex config
if [ -d "$HOME/.codex" ]; then
    cp -R "$HOME/.codex/" "$CODE_CONTAINER_DIR/.codex/"
    echo "✅ Copied Codex configuration"
else
    echo "⚠️  Codex configuration not found (expected at ~/.codex/)"
fi

# Copy Claude config
if [ -d "$HOME/.claude" ]; then
    cp -R "$HOME/.claude/" "$CODE_CONTAINER_DIR/.claude/"
    echo "✅ Copied Claude directory"
else
    echo "⚠️  Claude directory not found (expected at ~/.claude/)"
fi

if [ -f "$HOME/.claude.json" ]; then
    cp "$HOME/.claude.json" "$CODE_CONTAINER_DIR/container.claude.json"
    echo "✅ Copied Claude JSON configuration"
else
    echo "⚠️  Claude JSON configuration not found (expected at ~/.claude.json)"
fi

# Step 5: Build the container
echo ""
echo "🔧 Step 5: Building Docker container..."
echo "⚠️  This may take several minutes on first run..."
cd "$CODE_CONTAINER_DIR"
if container --build; then
    echo "✅ Container built successfully"
else
    echo "❌ Container build failed"
    echo "Trying with sudo..."
    sudo container --build
fi

# Step 6: Create test project
echo ""
echo "🔧 Step 6: Creating test project..."
TEST_PROJECT="$CONTAINERS_DIR/projects/test-container"
mkdir -p "$TEST_PROJECT"
cd "$TEST_PROJECT"

echo "#!/bin/bash" > test.sh
echo "echo 'Hello from inside the container!'" >> test.sh
echo "python3 --version" >> test.sh
echo "node --version" >> test.sh
chmod +x test.sh

echo "✅ Test project created at $TEST_PROJECT"

# Step 7: Create management scripts
echo ""
echo "🔧 Step 7: Creating management scripts..."

# create-container-project.sh
cat > "$CONTAINERS_DIR/scripts/create-container-project.sh" << 'EOF'
#!/bin/bash
# create-container-project.sh
# Create a new containerized project

set -e

if [ $# -lt 1 ]; then
    echo "Usage: $0 <project-name> [project-type]"
    echo "Project types: trading, lead-gen, web-dev, research, custom"
    exit 1
fi

PROJECT_NAME="$1"
PROJECT_TYPE="${2:-custom}"
OPENCLAW_HOME="/Users/cubiczan/.openclaw"
CONTAINERS_DIR="$OPENCLAW_HOME/containers"
PROJECT_DIR="$CONTAINERS_DIR/projects/$PROJECT_TYPE/$PROJECT_NAME"

echo "🎯 Creating containerized project: $PROJECT_NAME"
echo "📁 Type: $PROJECT_TYPE"
echo "📍 Location: $PROJECT_DIR"

# Create directory
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Create basic structure
mkdir -p {src,scripts,config,logs,data}

# Create README
cat > README.md << README
# $PROJECT_NAME

**Type:** $PROJECT_TYPE
**Container:** Yes
**Created:** $(date)

## Description
This project runs inside a code-container for isolation and safety.

## Usage
\`\`\`bash
# Enter the container
cd $PROJECT_DIR
container

# Inside container, you have full permissions
# Your work persists between sessions
\`\`\`

## Project Structure
- \`src/\` - Source code
- \`scripts/\` - Utility scripts
- \`config/\` - Configuration files
- \`logs/\` - Log files
- \`data/\` - Data files

## Safety Notes
- Changes are isolated to this container
- Host system is protected
- State persists between sessions
README

# Create .gitignore
cat > .gitignore << GITIGNORE
# Logs
logs/
*.log

# Data
data/*.csv
data/*.json
data/*.db

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
GITIGNORE

# Create entry script
cat > scripts/entry.sh << 'ENTRY'
#!/bin/bash
# entry.sh - Container entry point for $PROJECT_NAME

echo "🚀 Starting $PROJECT_NAME in container..."
echo "📅 $(date)"
echo "📁 Working directory: $(pwd)"

# Load environment if .env exists
if [ -f .env ]; then
    echo "🔧 Loading environment variables..."
    set -a
    source .env
    set +a
fi

# Project-specific initialization
case "$PROJECT_TYPE" in
    trading)
        echo "📈 Trading project detected"
        # Install trading dependencies
        pip install pandas numpy scipy matplotlib 2>/dev/null || true
        ;;
    lead-gen)
        echo "📧 Lead generation project detected"
        # Install web scraping dependencies
        pip install beautifulsoup4 requests selenium 2>/dev/null || true
        ;;
    web-dev)
        echo "🌐 Web development project detected"
        # Install web dev dependencies
        npm init -y 2>/dev/null || true
        ;;
    research)
        echo "🔬 Research project detected"
        # Install research dependencies
        pip install jupyter notebook scikit-learn 2>/dev/null || true
        ;;
esac

echo "✅ $PROJECT_NAME container ready!"
echo "💡 Use 'exit' to leave the container"
ENTRY

chmod +x scripts/entry.sh

echo "✅ Project created successfully!"
echo ""
echo "📋 Next steps:"
echo "1. cd $PROJECT_DIR"
echo "2. container"
echo "3. ./scripts/entry.sh"
echo ""
echo "🔒 Your work is now safely isolated in a container!"
EOF

chmod +x "$CONTAINERS_DIR/scripts/create-container-project.sh"

echo "✅ Management scripts created"
echo ""
echo "🎉 INSTALLATION COMPLETE!"
echo "========================"
echo ""
echo "📋 NEXT STEPS:"
echo "1. Test the container:"
echo "   cd $TEST_PROJECT"
echo "   container"
echo "   ./test.sh"
echo "   exit"
echo ""
echo "2. Create your first project:"
echo "   $CONTAINERS_DIR/scripts/create-container-project.sh my-project trading"
echo ""
echo "3. Manage containers:"
echo "   $CONTAINERS_DIR/scripts/manage-containers.sh list"
echo ""
echo "🔒 Your OpenClaw environment is now container-ready!"
echo "💡 Risky projects can run safely in isolated containers"