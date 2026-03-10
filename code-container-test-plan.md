# CODE-CONTAINER TEST PLAN
# Safe Implementation for OpenClaw Environment

## PHASE 1: DOCKER INSTALLATION & VERIFICATION

### Step 1.1: Install Docker via Homebrew
```bash
brew install --cask docker
```

### Step 1.2: Start Docker Desktop
- Open Docker Desktop from Applications
- Complete initial setup
- Verify Docker is running: `docker info`

### Step 1.3: Test Basic Docker Commands
```bash
docker --version
docker run hello-world
docker ps -a
```

## PHASE 2: CODE-CONTAINER SETUP

### Step 2.1: Create Isolated Test Directory
```bash
mkdir -p ~/code-container-test
cd ~/code-container-test
```

### Step 2.2: Clone Repository
```bash
git clone https://github.com/kevinMEH/code-container.git
cd code-container
```

### Step 2.3: Make Script Executable
```bash
chmod +x container.sh
```

### Step 2.4: Create Symlink (Optional)
```bash
sudo ln -sf "$(pwd)/container.sh" /usr/local/bin/container
```

## PHASE 3: BASIC FUNCTIONALITY TEST

### Step 3.1: Create Test Project
```bash
mkdir test-simple
cd test-simple
```

### Step 3.2: Create Test Files
```bash
cat > hello.py << 'EOF'
print("Hello from inside the container!")
print(f"Python version: {__import__('sys').version}")
EOF

cat > test.sh << 'EOF'
#!/bin/bash
echo "Bash test from container"
echo "Current directory: $(pwd)"
echo "Files in directory:"
ls -la
EOF
chmod +x test.sh
```

### Step 3.3: Enter Container
```bash
container
```

### Step 3.4: Inside Container Tests
```bash
# Test Python
python3 hello.py

# Test Bash
./test.sh

# Test basic commands
pwd
ls -la
python3 --version
node --version
npm --version
pip --version

# Exit container
exit
```

## PHASE 4: ISOLATION VERIFICATION

### Step 4.1: Test Host File Protection
```bash
# Create a file outside container
cd ~/code-container-test
echo "SECRET_HOST_FILE" > host-secret.txt

# Enter container and try to access
container
cat /host-secret.txt  # Should fail
ls /Users/cubiczan/  # Limited visibility
exit
```

### Step 4.2: Test Container Persistence
```bash
# Enter container
container

# Create file inside container
echo "Container persistence test" > container-file.txt
ls -la

# Exit and re-enter
exit
container

# Check if file still exists
ls -la  # Should see container-file.txt
cat container-file.txt
exit
```

### Step 4.3: Test Package Installation Isolation
```bash
# Enter container
container

# Install a Python package
pip install cowsay

# Test it works
python3 -c "import cowsay; cowsay.cow('Hello from container!')"

# Exit and check host
exit
python3 -c "import cowsay"  # Should fail on host
```

## PHASE 5: OPENCLAW INTEGRATION TEST

### Step 5.1: Test with Simple OpenClaw Script
```bash
# Create test OpenClaw project
mkdir ~/code-container-test/openclaw-test
cd ~/code-container-test/openclaw-test

# Copy a simple script from workspace
cp /Users/cubiczan/.openclaw/workspace/scripts/kelly-calculator.py .

# Enter container and test
container
python3 kelly-calculator.py
exit
```

### Step 5.2: Test File Operations Safety
```bash
# Enter container
container

# Try to access sensitive directories (should fail or be limited)
ls /Users/cubiczan/.openclaw/workspace/.env 2>/dev/null || echo "Protected - good!"
ls /Users/cubiczan/.ssh/ 2>/dev/null || echo "SSH protected - good!"

# Create and delete files in container (safe)
echo "test" > test-delete.txt
rm test-delete.txt
exit
```

## PHASE 6: PERFORMANCE & RESOURCE TEST

### Step 6.1: Test Resource Limits
```bash
# Monitor container resource usage
docker stats --no-stream

# Test memory usage
container
python3 -c "
import numpy as np
# Create large array (should work within limits)
arr = np.random.rand(1000, 1000)
print(f'Array size: {arr.nbytes / 1024 / 1024:.2f} MB')
"
exit
```

### Step 6.2: Test Network Access (Controlled)
```bash
# Enter container
container

# Test basic network (should work)
curl -s https://httpbin.org/ip | jq -r .origin 2>/dev/null || echo "jq not installed"

# Test API access (with our keys - careful!)
# We'll test without exposing keys first
echo "Network test complete"
exit
```

## PHASE 7: SECURITY VALIDATION

### Step 7.1: Verify Container Isolation
```bash
# List all containers
docker ps -a

# Check container processes
container
ps aux
exit

# Check from host
docker top $(docker ps -lq)
```

### Step 7.2: Test Read-Only Mounts (If configured)
```bash
# This depends on code-container configuration
# We'll verify what mounts are available
container
mount | grep -E "(ro|rw)"
exit
```

## PHASE 8: CLEANUP TEST

### Step 8.1: Test Container Cleanup
```bash
# Stop container
container --stop

# Remove container
container --remove

# Verify cleanup
docker ps -a | grep code-container || echo "Container cleaned up"
```

## TEST SUCCESS CRITERIA

### Must Pass:
1. ✅ Docker installs and runs
2. ✅ Container starts without errors
3. ✅ Host filesystem protected
4. ✅ Container persistence works
5. ✅ Package installation isolated
6. ✅ Network access controlled
7. ✅ Cleanup works properly

### Nice to Have:
1. ⚡ Performance within acceptable limits
2. 🔧 Easy integration with OpenClaw
3. 📁 File sharing works as expected
4. 🔒 Security isolation verified

## RISK MITIGATION

### Before Production Use:
1. **Backup critical data** before testing
2. **Test in isolated environment** first
3. **Monitor resource usage** during tests
4. **Have rollback plan** ready
5. **Document all findings**

### Safety Checks:
- Never test with production API keys first
- Start with read-only access to sensitive directories
- Monitor disk usage during package installations
- Test cleanup thoroughly before relying on it

## NEXT STEPS AFTER TESTING

1. **Document results** in memory file
2. **Identify first real project** to containerize
3. **Create migration checklist** for that project
4. **Schedule gradual rollout**
5. **Monitor performance** for 1 week
6. **Expand to other projects** based on success

---
*Test Plan Created: 2026-03-09*
*For OpenClaw Code-Container Implementation*