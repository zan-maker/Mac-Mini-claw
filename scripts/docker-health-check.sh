#!/bin/bash
# docker-health-check.sh
# Monitor and maintain our Docker containerization system

set -e

echo "🐳 DOCKER SYSTEM HEALTH CHECK"
echo "=============================="
echo "Date: $(date)"
echo ""

# 1. Check Colima status
echo "1. Colima Status:"
colima status 2>/dev/null || echo "  ⚠️  Colima not running"

echo ""

# 2. Check Docker daemon
echo "2. Docker Daemon:"
if docker ps > /dev/null 2>&1; then
    echo "  ✅ Docker daemon responding"
    echo "  Version: $(docker --version | cut -d' ' -f3- | tr ',' ' ')"
else
    echo "  ❌ Docker daemon not responding"
fi

echo ""

# 3. Check running containers
echo "3. Running Containers:"
RUNNING_CONTAINERS=$(docker ps -q | wc -l)
if [ "$RUNNING_CONTAINERS" -gt 0 ]; then
    echo "  ✅ $RUNNING_CONTAINERS container(s) running"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | tail -n +2 | while read line; do
        echo "    - $line"
    done
else
    echo "  ℹ️  No containers running (normal for our use case)"
fi

echo ""

# 4. Check container images
echo "4. Container Images:"
IMAGE_COUNT=$(docker images -q | wc -l)
echo "  📦 $IMAGE_COUNT images available"
docker images --format "{{.Repository}}:{{.Tag}}" | head -5 | while read image; do
    echo "    - $image"
done
if [ "$IMAGE_COUNT" -gt 5 ]; then
    echo "    ... and $((IMAGE_COUNT - 5)) more"
fi

echo ""

# 5. Check disk usage
echo "5. Disk Usage:"
docker system df --format "table {{.Type}}\t{{.TotalCount}}\t{{.Size}}" | while read line; do
    echo "  $line"
done

echo ""

# 6. Test our container wrapper
echo "6. Container Wrapper Test:"
if [ -f "/Users/cubiczan/container-test/simple-container.sh" ]; then
    echo "  ✅ simple-container.sh exists"
    # Quick syntax check
    if bash -n "/Users/cubiczan/container-test/simple-container.sh" > /dev/null 2>&1; then
        echo "  ✅ Script syntax valid"
    else
        echo "  ⚠️  Script syntax issues"
    fi
else
    echo "  ⚠️  simple-container.sh not found"
fi

echo ""

# 7. Check project directories
echo "7. Project Directories:"
PROJECTS=(
    "/Users/cubiczan/container-test"
    "/Users/cubiczan/container-projects/kelly-calculator"
    "/Users/cubiczan/.openclaw/workspace/scripts"
)

for project in "${PROJECTS[@]}"; do
    if [ -d "$project" ]; then
        count=$(find "$project" -name "*.sh" -o -name "*.py" -o -name "Dockerfile" 2>/dev/null | wc -l)
        echo "  📁 $(basename "$project"): $count files"
    else
        echo "  ⚠️  $(basename "$project"): Not found"
    fi
done

echo ""

# 8. Recommendations
echo "8. Recommendations:"
echo ""

# Check if cleanup needed
TOTAL_SIZE=$(docker system df --format '{{.Size}}' | head -1 | sed 's/[^0-9]*//g')
if [ "$TOTAL_SIZE" -gt 5000 ]; then  # More than 5GB
    echo "  🔧 Consider cleanup: docker system prune -a --volumes"
else
    echo "  ✅ Disk usage reasonable"
fi

# Check for outdated images
if [ "$IMAGE_COUNT" -gt 20 ]; then
    echo "  🔧 Many images ($IMAGE_COUNT), consider: docker image prune"
fi

# Check container wrapper
if [ ! -f "/Users/cubiczan/container-test/simple-container.sh" ]; then
    echo "  🔧 Create container wrapper script"
fi

echo ""

# 9. Firecracker readiness check
echo "9. Firecracker Readiness:"
if [ -f "/Users/cubiczan/.openclaw/workspace/FIRECRACKER_READINESS.md" ]; then
    echo "  📚 Research document exists"
    echo "  Status: Maintain Docker, research Firecracker"
else
    echo "  ⚠️  Research document missing"
fi

echo ""
echo "=============================="
echo "HEALTH CHECK COMPLETE"
echo ""

# Summary
echo "SUMMARY:"
if docker ps > /dev/null 2>&1 && [ -f "/Users/cubiczan/container-test/simple-container.sh" ]; then
    echo "✅ Docker system healthy and ready"
    echo "✅ Container wrapper available"
    echo "✅ Firecracker research documented"
    echo ""
    echo "NEXT: Continue using Docker for current projects"
    echo "      Refer to FIRECRACKER_READINESS.md for future planning"
else
    echo "⚠️  Some issues detected"
    echo ""
    echo "NEXT: Fix identified issues above"
fi

echo ""
echo "To run a container:"
echo "  ~/container-test/simple-container.sh --cmd \"python3 script.py\""
echo ""
echo "To check Firecracker research:"
echo "  cat ~/.openclaw/workspace/FIRECRACKER_READINESS.md | head -20"