# DOCKER ENGINE SETUP FOR CODE-CONTAINER

## What We're Installing

### Docker Engine (CLI Only)
- **docker** - Container runtime (CLI version)
- **docker-compose** - Multi-container orchestration
- **No GUI** - Runs entirely from command line

### Key Differences from Docker Desktop
1. **No GUI application** - All commands via terminal
2. **May need manual service start** - `sudo systemctl start docker` (Linux) or launchd service (macOS)
3. **Root access may be needed** - But we can configure rootless mode

## Post-Installation Setup

### 1. Start Docker Service
```bash
# On macOS with Homebrew
sudo brew services start docker

# Or manually
sudo /usr/local/opt/docker/bin/docker-daemon
```

### 2. Configure Rootless Mode (Optional but safer)
```bash
# Install rootless extras
brew install rootlesskit slirp4netns

# Setup rootless Docker
dockerd-rootless-setuptool.sh install

# Add to shell profile
echo "export DOCKER_HOST=unix:///run/user/$(id -u)/docker.sock" >> ~/.zshrc
source ~/.zshrc
```

### 3. Test Installation
```bash
# Check version
docker --version
docker-compose --version

# Run test container
docker run --rm hello-world
```

## Code-Container Adaptation for Docker Engine

The code-container script may need minor adjustments for Docker Engine:

### Original code-container uses:
```bash
docker run -it --rm \
  -v "$(pwd):/workspace" \
  -v "$SCRIPT_DIR/.opencode:/root/.config/opencode" \
  # ... other mounts
```

### May need for Docker Engine:
```bash
# Add user mapping for better permissions
docker run -it --rm \
  -v "$(pwd):/workspace" \
  -v "$SCRIPT_DIR/.opencode:/root/.config/opencode" \
  -u "$(id -u):$(id -g)" \  # Run as current user
  # ... other mounts
```

## Troubleshooting Common Issues

### 1. Permission Denied
```bash
# Add your user to docker group
sudo usermod -aG docker $USER
newgrp docker  # Or log out and back in
```

### 2. Cannot Connect to Docker Daemon
```bash
# Check if docker service is running
sudo systemctl status docker  # Linux
sudo brew services list | grep docker  # macOS

# Start if not running
sudo systemctl start docker  # Linux
sudo brew services start docker  # macOS
```

### 3. Rootless Mode Issues
```bash
# Check rootless setup
docker context ls

# Use rootless context
docker context use rootless

# Or set environment variable
export DOCKER_HOST=unix:///run/user/$(id -u)/docker.sock
```

## Verification Steps

After installation, run these checks:

```bash
# 1. Basic version check
docker --version
docker-compose --version

# 2. Service status
sudo brew services list | grep docker

# 3. Run test container
docker run --rm hello-world

# 4. Check user permissions
docker ps  # Should work without sudo

# 5. Test volume mounting
mkdir -p /tmp/docker-test
echo "test" > /tmp/docker-test/file.txt
docker run --rm -v /tmp/docker-test:/test alpine cat /test/file.txt
```

## Code-Container Specific Setup

Once Docker Engine is working:

```bash
# Clone code-container
cd ~/container-test
git clone https://github.com/kevinMEH/code-container.git
cd code-container

# Make script executable
chmod +x container.sh

# Test with our safe project
cd ~/container-test/safe-project
~/container-test/code-container/container.sh
```

## Expected Output

If everything works, you should see:
1. Container starts without errors
2. You get a shell inside the container
3. Can run `./test-container-safety.sh`
4. Can run `python3 generate_docs.py`
5. Files created persist in container
6. Host system remains untouched

## Fallback Options

If Docker Engine has issues:

### Option 1: Podman (Rootless by default)
```bash
brew install podman
podman machine init
podman machine start
# Use podman instead of docker (mostly compatible)
```

### Option 2: Lima (Docker Desktop alternative)
```bash
brew install lima
limactl start docker
# Provides Docker API without Desktop
```

### Option 3: Colima (Container runtimes on macOS)
```bash
brew install colima
colima start
# Provides Docker and containerd
```

## Next Steps After Successful Installation

1. **Test basic container functionality**
2. **Verify isolation with safe project**
3. **Adapt code-container script if needed**
4. **Test with Kelly Calculator**
5. **Plan migration of real projects**

---
*Setup Guide for Docker Engine + Code-Container*
*Safe, CLI-only approach for OpenClaw environment*