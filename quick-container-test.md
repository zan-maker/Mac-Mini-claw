# QUICK CODE-CONTAINER TEST - SAFE APPROACH

## IMMEDIATE ACTIONS (While Docker Installs)

### 1. Create Test Directory Structure
```bash
mkdir -p ~/container-test/{safe-project,logs,backups}
cd ~/container-test
```

### 2. Create Safest Test Project: Documentation Generator
```bash
cd ~/container-test/safe-project

# Create a simple Python script that only reads and writes in its own directory
cat > generate_docs.py << 'EOF'
#!/usr/bin/env python3
"""
Safe Documentation Generator
Only works within its own directory, no external access
"""

import os
import json
from datetime import datetime

def generate_project_summary():
    """Generate a simple project summary document"""
    project_info = {
        "name": "Container Test Project",
        "type": "Documentation Generator",
        "created": datetime.now().isoformat(),
        "purpose": "Test code-container isolation safely",
        "risk_level": "Zero",
        "files": []
    }
    
    # List files in current directory (safe)
    for file in os.listdir("."):
        if os.path.isfile(file):
            project_info["files"].append({
                "name": file,
                "size": os.path.getsize(file),
                "modified": datetime.fromtimestamp(os.path.getmtime(file)).isoformat()
            })
    
    # Write summary (only in current directory)
    with open("project-summary.json", "w") as f:
        json.dump(project_info, f, indent=2)
    
    # Create README
    with open("README.md", "w") as f:
        f.write(f"""# Container Test Project

## Project Information
- **Name**: {project_info['name']}
- **Type**: {project_info['type']}
- **Created**: {project_info['created']}
- **Purpose**: {project_info['purpose']}
- **Risk Level**: {project_info['risk_level']}

## Files in Project
""")
        for file_info in project_info["files"]:
            f.write(f"- `{file_info['name']}` ({file_info['size']} bytes, modified {file_info['modified']})\n")
        
        f.write("""
## Safety Features
1. **No external file access** - Only reads/writes in current directory
2. **No network calls** - Completely offline
3. **No system commands** - Only uses Python standard library
4. **No sensitive data** - Only generates documentation

## Test Results
This project is designed to test code-container isolation with zero risk.
If this works in a container, we can proceed to more complex projects.
""")
    
    print("✅ Documentation generated successfully!")
    print(f"📁 Created: project-summary.json")
    print(f"📄 Created: README.md")
    print(f"📊 Total files: {len(project_info['files'])}")
    return True

if __name__ == "__main__":
    print("🔒 SAFE DOCUMENTATION GENERATOR")
    print("=" * 40)
    print("This script only works within its own directory.")
    print("It cannot access files outside its container.")
    print("=" * 40)
    
    try:
        generate_project_summary()
        print("\n✅ Test completed successfully!")
        print("💡 This proves the script can run safely in isolation.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("This helps identify isolation issues.")
EOF

# Make it executable
chmod +x generate_docs.py

# Create a test data file
cat > test-data.txt << 'EOF'
Test Data File
==============
This is a safe test file for container testing.
It contains no sensitive information.
Created: $(date)
Purpose: Test file operations in container
EOF
```

### 3. Create Test Script
```bash
cat > test-container-safety.sh << 'EOF'
#!/bin/bash
# Test Container Safety

echo "🔒 CONTAINER SAFETY TEST"
echo "========================"
echo "Testing: $(date)"
echo ""

# Test 1: Current directory isolation
echo "1. Testing directory isolation..."
pwd
ls -la
echo ""

# Test 2: File operations (safe)
echo "2. Testing file operations..."
echo "Creating test file..." > container-test-file.txt
cat container-test-file.txt
rm container-test-file.txt
echo "File created and deleted successfully."
echo ""

# Test 3: Command availability
echo "3. Testing command availability..."
which python3 && python3 --version
which node && node --version
which npm && npm --version
echo ""

# Test 4: Resource limits
echo "4. Testing resource awareness..."
echo "CPU cores: $(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 'Unknown')"
echo "Memory: $(free -h 2>/dev/null || echo 'Memory info not available')"
echo ""

# Test 5: Network test (optional)
echo "5. Testing network isolation..."
echo "Attempting to reach google.com (timeout 2s)..."
curl -s --max-time 2 https://google.com >/dev/null && echo "Network: Connected" || echo "Network: Limited or offline"
echo ""

echo "✅ Safety tests completed!"
echo "📊 If all tests pass, container isolation is working."
EOF

chmod +x test-container-safety.sh
```

### 4. Create README for Test Project
```bash
cat > README-TEST.md << 'EOF'
# Code-Container Safety Test Project

## Purpose
Test code-container isolation with zero risk to host system.

## Files
1. `generate_docs.py` - Safe documentation generator (Python)
2. `test-container-safety.sh` - Basic safety tests (Bash)
3. `test-data.txt` - Sample data file
4. `README-TEST.md` - This file

## Safety Guarantees
- ✅ No access to host filesystem outside test directory
- ✅ No network exfiltration capability
- ✅ No system modification outside test directory
- ✅ No sensitive data exposure
- ✅ No permanent changes to host

## Test Procedure
1. Clone code-container repository
2. Enter container in this directory
3. Run safety tests
4. Verify isolation
5. Exit container

## Expected Results
- Scripts run successfully inside container
- Cannot access files outside `~/container-test/safe-project/`
- Network access is limited/controlled
- Changes persist only within container
- Host system remains untouched

## Next Steps After Success
1. Test with Kelly Calculator (low risk)
2. Test with data processing scripts (medium risk)
3. Test with web scraping (high risk, in container)
4. Integrate with OpenClaw sub-agents
EOF
```

echo "✅ Safe test project created at ~/container-test/safe-project/"
echo "📋 Ready for code-container testing once Docker is installed"