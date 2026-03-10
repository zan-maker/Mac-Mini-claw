#!/bin/bash
# setup-code-container.sh
# Setup code-container with Colima on macOS

set -e  # Exit on error

echo "🎯 SETTING UP CODE-CONTAINER WITH COLIMA"
echo "========================================"

# Configuration
TEST_DIR="$HOME/container-test"
CODE_CONTAINER_DIR="$TEST_DIR/code-container"
SAFE_PROJECT_DIR="$TEST_DIR/safe-project"

echo "📁 Checking directories..."
mkdir -p "$TEST_DIR"

# Step 1: Check Colima status
echo ""
echo "🔧 Step 1: Checking Colima status..."
if colima status 2>/dev/null | grep -q "RUNNING"; then
    echo "✅ Colima is running"
else
    echo "❌ Colima is not running"
    echo "Starting Colima..."
    colima start
fi

# Step 2: Check Docker connectivity
echo ""
echo "🔧 Step 2: Testing Docker..."
if docker ps 2>/dev/null; then
    echo "✅ Docker is working"
else
    echo "❌ Docker not responding"
    echo "Troubleshooting..."
    
    # Check Colima again
    colima status
    
    # Check Docker context
    docker context ls
    
    # Try to use colima context
    docker context use colima 2>/dev/null || true
    
    # Test again
    if docker ps 2>/dev/null; then
        echo "✅ Docker now working"
    else
        echo "❌ Docker still not working"
        echo "Please check:"
        echo "1. Run: colima status"
        echo "2. Run: docker context ls"
        echo "3. Run: docker context use colima"
        exit 1
    fi
fi

# Step 3: Clone code-container
echo ""
echo "🔧 Step 3: Cloning code-container..."
if [ -d "$CODE_CONTAINER_DIR" ]; then
    echo "✅ code-container already exists"
    cd "$CODE_CONTAINER_DIR"
    git pull
else
    cd "$TEST_DIR"
    git clone https://github.com/kevinMEH/code-container.git
    echo "✅ code-container cloned"
fi

# Step 4: Make script executable
echo ""
echo "🔧 Step 4: Setting up container script..."
cd "$CODE_CONTAINER_DIR"
chmod +x container.sh

# Create symlink for easy access
if [ ! -f /usr/local/bin/container ]; then
    echo "🔗 Creating symlink..."
    sudo ln -sf "$CODE_CONTAINER_DIR/container.sh" /usr/local/bin/container 2>/dev/null || {
        echo "⚠️  Could not create symlink (sudo may be needed)"
        echo "   You can run: sudo ln -sf \"$CODE_CONTAINER_DIR/container.sh\" /usr/local/bin/container"
    }
else
    echo "✅ Symlink already exists"
fi

# Step 5: Test basic Docker functionality
echo ""
echo "🔧 Step 5: Testing basic Docker..."
docker run --rm hello-world >/dev/null 2>&1 && echo "✅ Docker test passed" || {
    echo "❌ Docker test failed"
    echo "Running debug test..."
    docker run --rm hello-world
}

# Step 6: Check safe project
echo ""
echo "🔧 Step 6: Checking safe project..."
if [ -d "$SAFE_PROJECT_DIR" ]; then
    echo "✅ Safe project exists at $SAFE_PROJECT_DIR"
    echo "   Files:"
    ls -la "$SAFE_PROJECT_DIR/"
else
    echo "⚠️  Safe project not found"
    echo "   Expected at: $SAFE_PROJECT_DIR"
fi

# Step 7: Create test script for code-container
echo ""
echo "🔧 Step 7: Creating test script..."
cat > "$TEST_DIR/test-code-container.sh" << 'EOF'
#!/bin/bash
# test-code-container.sh
# Test code-container functionality

set -e

echo "🧪 CODE-CONTAINER TEST"
echo "======================"

TEST_DIR="$HOME/container-test"
SAFE_PROJECT="$TEST_DIR/safe-project"
CODE_CONTAINER="$TEST_DIR/code-container"

# Check prerequisites
echo "1. Checking prerequisites..."
which docker && docker --version
which container || echo "container command not found (symlink may be missing)"

# Test 1: Basic container functionality
echo ""
echo "2. Testing basic container..."
cd "$SAFE_PROJECT"
echo "Current directory: $(pwd)"
echo "Files:"
ls -la

# Test 2: Try to enter container
echo ""
echo "3. Attempting to enter container..."
echo "If this works, you'll be inside the container."
echo "Run these commands inside container:"
echo "  ./test-container-safety.sh"
echo "  python3 generate_docs.py"
echo "  exit (to leave container)"
echo ""
echo "Starting container (if 'container' command exists)..."
if command -v container >/dev/null 2>&1; then
    container
else
    echo "⚠️ 'container' command not found"
    echo "Using direct path: $CODE_CONTAINER/container.sh"
    "$CODE_CONTAINER/container.sh"
fi

# Test 3: Verify from outside
echo ""
echo "4. Verifying host system..."
echo "Back in host system at: $(pwd)"
echo "Host files should be unchanged."
ls -la

echo ""
echo "✅ Test script complete"
echo "📋 If you entered and exited the container successfully, code-container is working!"
EOF

chmod +x "$TEST_DIR/test-code-container.sh"

# Step 8: Create quick start guide
echo ""
echo "🔧 Step 8: Creating quick start guide..."
cat > "$TEST_DIR/QUICK_START.md" << 'EOF'
# CODE-CONTAINER QUICK START

## Prerequisites
- ✅ Colima running (`colima status` should show RUNNING)
- ✅ Docker working (`docker ps` should not error)
- ✅ code-container cloned (`~/container-test/code-container/`)

## Quick Test
```bash
cd ~/container-test
./test-code-container.sh
```

## Manual Test
1. Go to safe project:
   ```bash
   cd ~/container-test/safe-project
   ```

2. Enter container:
   ```bash
   # If symlink exists:
   container
   
   # Or directly:
   ~/container-test/code-container/container.sh
   ```

3. Inside container, run tests:
   ```bash
   ./test-container-safety.sh
   python3 generate_docs.py
   ls -la
   ```

4. Exit container:
   ```bash
   exit
   ```

## Expected Results
- ✅ Can enter container without errors
- ✅ Can run scripts inside container
- ✅ Files created inside container persist
- ✅ Host system files unchanged
- ✅ Can exit container cleanly

## Troubleshooting

### Docker not working:
```bash
colima status  # Should show RUNNING
colima start   # Start if not running
docker context use colima  # Use colima context
```

### 'container' command not found:
```bash
# Use full path
~/container-test/code-container/container.sh

# Or create symlink
sudo ln -sf ~/container-test/code-container/container.sh /usr/local/bin/container
```

### Permission errors:
```bash
# Check Colima VM resources
colima status

# Restart Colima with more resources
colima stop
colima start --cpu 4 --memory 8
```

## Next Steps After Success
1. Test with Kelly Calculator (`scripts/kelly-calculator.py`)
2. Create containerized project structure
3. Migrate real projects to containers
4. Implement automated container management

## Safety Notes
- The safe project cannot access host files
- All changes are isolated to container
- Network access is limited
- Resource usage is controlled
EOF

echo ""
echo "🎉 SETUP COMPLETE!"
echo "================="
echo ""
echo "📋 NEXT STEPS:"
echo "1. Check Colima is running:"
echo "   colima status"
echo ""
echo "2. Run the test:"
echo "   cd ~/container-test"
echo "   ./test-code-container.sh"
echo ""
echo "3. If successful, you'll be inside the container."
echo "   Run the safety tests, then type 'exit' to leave."
echo ""
echo "📚 Documentation:"
echo "   ~/container-test/QUICK_START.md"
echo "   ~/.openclaw/workspace/docker-engine-setup.md"
echo ""
echo "🔒 Your safe test project is ready at:"
echo "   ~/container-test/safe-project/"
echo ""
echo "🚀 Let's test code-container isolation!"