# KELLY CALCULATOR CONTAINER MIGRATION PLAN

## Current Status
- **Script:** `/Users/cubiczan/.openclaw/workspace/scripts/kelly-calculator.py`
- **Dependencies:** Python 3.11, standard library only
- **Risk Level:** Low (mathematical calculations only)
- **Container Ready:** ✅ Yes (already tested successfully)

## Migration Steps

### Step 1: Create Containerized Version
```bash
# Create dedicated container script
cat > ~/container-projects/kelly-calculator/run.sh << 'EOF'
#!/bin/bash
# Containerized Kelly Calculator

cd /Users/cubiczan/.openclaw/workspace
~/container-test/simple-container.sh --cmd "python3 scripts/kelly-calculator.py"
EOF

chmod +x ~/container-projects/kelly-calculator/run.sh
```

### Step 2: Test Thoroughly
```bash
# Test basic functionality
~/container-projects/kelly-calculator/run.sh

# Test with different parameters
cd /Users/cubiczan/.openclaw/workspace
~/container-test/simple-container.sh --cmd "python3 -c \"
import sys
sys.path.append('scripts')
import kelly-calculator
print('Kelly Calculator module loaded successfully')
\""
```

### Step 3: Update Cron Jobs (if any)
```bash
# Update existing cron jobs to use container version
~/container-test/container-cron-manager.sh create kelly-production "0 9 * * *" "scripts/kelly-calculator.py"
```

### Step 4: Create Documentation
```bash
cat > ~/container-projects/kelly-calculator/README.md << 'EOF'
# Containerized Kelly Calculator

## Purpose
Run Kelly Criterion calculations in isolated container for safety.

## Files
- `run.sh` - Main execution script
- `test.sh` - Test script
- `README.md` - This documentation

## Usage
```bash
# Run calculator
./run.sh

# Or directly
cd /Users/cubiczan/.openclaw/workspace
~/container-test/simple-container.sh --cmd "python3 scripts/kelly-calculator.py"
```

## Safety Features
- ✅ Isolated from host filesystem
- ✅ No network access required
- ✅ No external dependencies
- ✅ Read-only access to script files

## Cron Integration
Runs daily at 9:00 AM via container-cron-manager.
EOF
```

### Step 5: Verify Migration
```bash
# Compare outputs
echo "=== HOST VERSION ==="
python3 /Users/cubiczan/.openclaw/workspace/scripts/kelly-calculator.py | head -20

echo "=== CONTAINER VERSION ==="
~/container-projects/kelly-calculator/run.sh | head -20

# Verify they match
```

## Files Created
1. `~/container-projects/kelly-calculator/run.sh`
2. `~/container-projects/kelly-calculator/test.sh`
3. `~/container-projects/kelly-calculator/README.md`

## Next Projects for Migration

### High Priority:
1. **War Monitor** - After fixing dependency issues
2. **Gas Monitor** - Similar to war monitor
3. **Kalshi Scanner** - Trading automation

### Medium Priority:
1. **Lead Generation Scripts** - Web scraping
2. **Email Outreach** - API integrations
3. **Data Processing** - Large data files

### Low Priority:
1. **Documentation Generators** - Already safe
2. **Log Analyzers** - Read-only operations
3. **Configuration Validators** - Simple checks

## Success Criteria
- [ ] Kelly Calculator runs in container
- [ ] Output matches host version
- [ ] No permission issues
- [ ] Logging works correctly
- [ ] Can be scheduled via cron

## Rollback Plan
If issues occur:
1. Revert to direct Python execution
2. Remove container cron jobs
3. Restore original scripts

---
*Migration Plan Created: 2026-03-09*
*First containerized project: Kelly Calculator*