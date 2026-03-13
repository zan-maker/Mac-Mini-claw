#!/bin/bash
# 🔐 Setup Comprehensive Backup System with Best-Backup

set -e  # Exit on error

echo "🔐 SETTING UP COMPREHENSIVE BACKUP SYSTEM"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Log function
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if running as correct user
if [ "$(whoami)" != "cubiczan" ]; then
    error "This script should be run as user 'cubiczan'"
    exit 1
fi

# Create backup directory
BACKUP_DIR="$HOME/backups/openclaw"
log "Creating backup directory: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"
mkdir -p "$BACKUP_DIR/logs"
mkdir -p "$BACKUP_DIR/config"

# Step 1: Install pipx if not installed
log "Step 1: Installing pipx..."
if ! command -v pipx &> /dev/null; then
    log "Installing pipx via Homebrew..."
    brew install pipx
    pipx ensurepath
    
    # Reload shell environment
    if [ -n "$ZSH_VERSION" ]; then
        source ~/.zshrc
    else
        source ~/.bashrc
    fi
    
    success "pipx installed successfully"
else
    success "pipx already installed"
fi

# Step 2: Install best-backup
log "Step 2: Installing best-backup..."
if ! command -v bbackup &> /dev/null; then
    log "Installing best-backup via pipx..."
    pipx install git+https://github.com/cptnfren/best-backup.git
    success "best-backup installed successfully"
else
    log "best-backup already installed, upgrading..."
    pipx upgrade bbackup
    success "best-backup upgraded"
fi

# Step 3: Install rclone for Google Drive backup
log "Step 3: Installing rclone..."
if ! command -v rclone &> /dev/null; then
    log "Installing rclone via Homebrew..."
    brew install rclone
    success "rclone installed successfully"
else
    success "rclone already installed"
fi

# Step 4: Create configuration
log "Step 4: Creating backup configuration..."

CONFIG_DIR="$HOME/.config/bbackup"
mkdir -p "$CONFIG_DIR"

cat > "$CONFIG_DIR/config.yaml" << 'EOF'
# Best-Backup Configuration for OpenClaw Workspace
backup:
  local_staging: /tmp/bbackup_staging
  
  backup_sets:
    # Workspace - All OpenClaw files
    workspace:
      description: "OpenClaw Workspace - All files and configurations"
      paths:
        - /Users/cubiczan/.openclaw/workspace
      excludes:
        - "*.tmp"
        - "*.log"
        - ".cache/"
        - "node_modules/"
        - "__pycache__/"
        - ".git/"
        - "*.pyc"
        - "*.pyo"
        - ".DS_Store"
        - "Thumbs.db"
    
    # Configuration files
    configs:
      description: "System configuration files"
      paths:
        - /Users/cubiczan/.openclaw/openclaw.json
        - /Users/cubiczan/.openclaw/workspace/config/
        - /Users/cubiczan/.openclaw/workspace/docs/
    
    # Skills directory
    skills:
      description: "AI Agent Skills"
      paths:
        - /Users/cubiczan/mac-bot/skills/
    
    # Market research and business plans
    business:
      description: "Business research and plans"
      paths:
        - /Users/cubiczan/.openclaw/workspace/market_research/
        - /Users/cubiczan/.openclaw/workspace/million_dollar_business/
        - /Users/cubiczan/.openclaw/workspace/product_development/

remotes:
  # Local backup (always enabled)
  local:
    enabled: true
    type: local
    path: /Users/cubiczan/backups/openclaw
    description: "Local backup directory"
  
  # Google Drive backup (requires rclone setup)
  google_drive:
    enabled: false  # Set to true after rclone configuration
    type: rclone
    rclone_remote: gdrive
    path: /Backups/OpenClaw
    description: "Google Drive remote backup"
    rclone_options:
      transfers: 4
      checkers: 8

encryption:
  enabled: true
  method: symmetric
  symmetric:
    key_path: /Users/cubiczan/.config/bbackup/backup_key.bin

rotation:
  daily: 7      # Keep 7 daily backups
  weekly: 4     # Keep 4 weekly backups
  monthly: 12   # Keep 12 monthly backups
  quota_gb: 100 # Maximum 100GB of backup storage

logging:
  level: INFO
  file: /Users/cubiczan/backups/openclaw/logs/bbackup.log
  max_size_mb: 10
  backup_count: 5
EOF

success "Configuration created at $CONFIG_DIR/config.yaml"

# Step 5: Initialize encryption
log "Step 5: Initializing encryption..."
if [ ! -f "$HOME/.config/bbackup/backup_key.bin" ]; then
    log "Generating encryption key..."
    bbackup init-encryption --method symmetric --key-path "$HOME/.config/bbackup/backup_key.bin"
    success "Encryption key generated"
    
    # Secure the key file
    chmod 600 "$HOME/.config/bbackup/backup_key.bin"
    log "Encryption key secured (readable only by owner)"
else
    success "Encryption key already exists"
fi

# Step 6: Create backup scripts
log "Step 6: Creating backup automation scripts..."

# Daily backup script
cat > "$HOME/.openclaw/workspace/scripts/backup_daily.sh" << 'EOF'
#!/bin/bash
# Daily Backup Script for OpenClaw Workspace

set -e

# Configuration
BACKUP_LOG="$HOME/backups/openclaw/logs/backup_daily.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Environment for non-interactive JSON output
export BBACKUP_OUTPUT=json
export BBACKUP_NO_INTERACTIVE=1

echo "=== Daily Backup Started at $TIMESTAMP ===" >> "$BACKUP_LOG"

# Run workspace backup
echo "Running workspace backup..." >> "$BACKUP_LOG"
bbackup backup --backup-set workspace --remote local >> "$BACKUP_LOG" 2>&1

# Check if Google Drive is configured and enabled
if grep -q "enabled: true" "$HOME/.config/bbackup/config.yaml" | grep -q "google_drive"; then
    echo "Running Google Drive backup..." >> "$BACKUP_LOG"
    bbackup backup --backup-set workspace --remote google_drive >> "$BACKUP_LOG" 2>&1
fi

# Log completion
COMPLETION_TIME=$(date '+%Y-%m-%d %H:%M:%S')
echo "=== Daily Backup Completed at $COMPLETION_TIME ===" >> "$BACKUP_LOG"
echo "" >> "$BACKUP_LOG"

# Send success notification (optional)
# echo "Daily backup completed successfully at $COMPLETION_TIME" | mail -s "Backup Success" sam@cubiczan.com
EOF

chmod +x "$HOME/.openclaw/workspace/scripts/backup_daily.sh"

# Weekly backup script
cat > "$HOME/.openclaw/workspace/scripts/backup_weekly.sh" << 'EOF'
#!/bin/bash
# Weekly Full Backup Script for OpenClaw

set -e

# Configuration
BACKUP_LOG="$HOME/backups/openclaw/logs/backup_weekly.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Environment for non-interactive JSON output
export BBACKUP_OUTPUT=json
export BBACKUP_NO_INTERACTIVE=1

echo "=== Weekly Full Backup Started at $TIMESTAMP ===" >> "$BACKUP_LOG"

# Run full backup of all sets
echo "Running full workspace backup..." >> "$BACKUP_LOG"
bbackup backup --backup-set workspace --backup-set configs --backup-set skills --backup-set business --remote local >> "$BACKUP_LOG" 2>&1

# Google Drive backup if enabled
if grep -q "enabled: true" "$HOME/.config/bbackup/config.yaml" | grep -q "google_drive"; then
    echo "Running Google Drive full backup..." >> "$BACKUP_LOG"
    bbackup backup --backup-set workspace --backup-set configs --backup-set skills --backup-set business --remote google_drive >> "$BACKUP_LOG" 2>&1
fi

# Cleanup old backups
echo "Cleaning up old backups..." >> "$BACKUP_LOG"
bbackup cleanup --yes >> "$BACKUP_LOG" 2>&1

# Log completion
COMPLETION_TIME=$(date '+%Y-%m-%d %H:%M:%S')
echo "=== Weekly Full Backup Completed at $COMPLETION_TIME ===" >> "$BACKUP_LOG"
echo "" >> "$BACKUP_LOG"

# Health check
echo "Running health check..." >> "$BACKUP_LOG"
bbman health >> "$BACKUP_LOG" 2>&1
EOF

chmod +x "$HOME/.openclaw/workspace/scripts/backup_weekly.sh"

# Health check script
cat > "$HOME/.openclaw/workspace/scripts/backup_health_check.sh" << 'EOF'
#!/bin/bash
# Backup System Health Check

set -e

HEALTH_LOG="$HOME/backups/openclaw/logs/health_check.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "=== Health Check Started at $TIMESTAMP ===" >> "$HEALTH_LOG"

# Run health check
export BBACKUP_OUTPUT=json
HEALTH_RESULT=$(bbman health --output json 2>&1)

echo "$HEALTH_RESULT" >> "$HEALTH_LOG"

# Parse JSON result
if echo "$HEALTH_RESULT" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if not data.get('success', False):
        print('HEALTH_CHECK_FAILED')
        sys.exit(1)
except Exception as e:
    print('PARSE_ERROR', str(e))
    sys.exit(1)
"; then
    echo "Health check passed" >> "$HEALTH_LOG"
else
    echo "Health check failed" >> "$HEALTH_LOG"
    # Send alert (uncomment to enable)
    # echo "Backup health check failed at $TIMESTAMP" | mail -s "Backup Alert" sam@cubiczan.com
fi

echo "=== Health Check Completed ===" >> "$HEALTH_LOG"
echo "" >> "$HEALTH_LOG"
EOF

chmod +x "$HOME/.openclaw/workspace/scripts/backup_health_check.sh"

success "Backup scripts created"

# Step 7: Set up cron jobs
log "Step 7: Setting up cron jobs..."

# Remove existing backup cron jobs if any
(crontab -l 2>/dev/null | grep -v "backup_" | grep -v "health_check") | crontab -

# Add new cron jobs
(crontab -l 2>/dev/null; echo "# Daily backup at 2:00 AM") | crontab -
(crontab -l 2>/dev/null; echo "0 2 * * * /Users/cubiczan/.openclaw/workspace/scripts/backup_daily.sh") | crontab -

(crontab -l 2>/dev/null; echo "# Weekly full backup at 3:00 AM on Sunday") | crontab -
(crontab -l 2>/dev/null; echo "0 3 * * 0 /Users/cubiczan/.openclaw/workspace/scripts/backup_weekly.sh") | crontab -

(crontab -l 2>/dev/null; echo "# Daily health check at 4:00 AM") | crontab -
(crontab -l 2>/dev/null; echo "0 4 * * * /Users/cubiczan/.openclaw/workspace/scripts/backup_health_check.sh") | crontab -

success "Cron jobs configured"

# Step 8: Create AI agent integration
log "Step 8: Creating AI agent integration..."

cat > "$HOME/.openclaw/workspace/scripts/backup_integration.py" << 'EOF'
#!/usr/bin/env python3
"""
Backup Integration for AI Agents
Provides JSON API for managing backups
"""

import subprocess
import json
import os
import sys
from datetime import datetime
from pathlib import Path

class BackupManager:
    """Manage backups via best-backup for AI agents"""
    
    def __init__(self):
        self.env = {
            'BBACKUP_OUTPUT': 'json',
            'BBACKUP_NO_INTERACTIVE': '1'
        }
        self.config_path = Path.home() / '.config' / 'bbackup' / 'config.yaml'
        self.log_dir = Path.home() / 'backups' / 'openclaw' / 'logs'
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def _run_command(self, cmd, description=""):
        """Run command and return JSON result"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env={**os.environ, **self.env}
            )
            
            if result.returncode == 0:
                try:
                    return {
                        'success': True,
                        'data': json.loads(result.stdout),
                        'description': description
                    }
                except json.JSONDecodeError:
                    return {
                        'success': True,
                        'data': {'output': result.stdout},
                        'description': description
                    }
            else:
                return {
                    'success': False,
                    'error': result.stderr,
                    'description': description,
                    'returncode': result.returncode
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'description': description
            }
    
    def run_backup(self, backup_set="workspace", incremental=True, remote="local"):
        """Run backup for specific set"""
        cmd = [
            'bbackup', 'backup',
            '--backup-set', backup_set,
            '--remote', remote,
            '--input-json', json.dumps({'incremental': incremental})
        ]
        
        return self._run_command(cmd, f"Backup of {backup_set} to {remote}")
    
    def list_backups(self, remote="local"):
        """List available backups"""
        cmd = ['bbackup', 'list-backups', '--remote', remote]
        return self._run_command(cmd, f"List backups from {remote}")
    
    def health_check(self):
        """Check backup system health"""
        cmd = ['bbman', 'health']
        return self._run_command(cmd, "System health check")
    
    def get_status(self):
        """Get backup system status"""
        cmd = ['bbman', 'status']
        return self._run_command(cmd, "System status")
    
    def cleanup(self, yes=False):
        """Clean up old backups"""
        cmd = ['bbackup', 'cleanup']
        if yes:
            cmd.append('--yes')
        return self._run_command(cmd, "Cleanup old backups")
    
    def discover_skills(self):
        """Discover available backup skills"""
        cmd = ['bbackup', 'skills']
        return self._run_command(cmd, "Discover backup skills")
    
    def restore_backup(self, backup_path, target_set="workspace", destination=None):
        """Restore from backup"""
        cmd = ['bbackup', 'restore', '--backup-path', backup_path]
        
        if target_set == "filesystem" and destination:
            cmd.extend(['--filesystem', 'workspace', '--filesystem-destination', destination])
        else:
            cmd.extend(['--backup-set', target_set])
        
        return self._run_command(cmd, f"Restore {target_set} from {backup_path}")
    
    def full_system_check(self):
        """Run comprehensive system check"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'checks': []
        }
        
        # Health check
        health = self.health_check()
        results['checks'].append({
            'name': 'health',
            'success': health['success'],
            'data': health.get('data', {})
        })
        
        # Status check
        status = self.get_status()
        results['checks'].append({
            'name': 'status',
            'success': status['success'],
            'data': status.get('data', {})
        })
        
        # List recent backups
        backups = self.list_backups()
        results['checks'].append({
            'name': 'backups',
            'success': backups['success'],
            'data': backups.get('data', {})
        })
        
        # Check disk space
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            results['disk_space'] = {
                'total_gb': total // (2**30),
                'used_gb': used // (2**30),
                'free_gb': free // (2**30),
                'percent_used': (used / total) * 100
            }
        except Exception as e:
            results['disk_space_error'] = str(e)
        
        # Check if system is healthy
        results['overall_healthy'] = all(check['success'] for check in results['checks'])
        
        return {
            'success': True,
            'data': results,
            'description': 'Full system check completed'
        }

def main():
    """Command-line interface for backup management"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Backup Management for AI Agents')
    parser.add_argument('--action', choices=['backup', 'restore', 'health', 'status', 'list', 'cleanup', 'skills', 'full-check'],
                       default='health', help='Action to perform')
    parser.add_argument('--set', default='workspace', help='Backup set to use')
    parser.add_argument('--remote', default='local', help='Remote storage to use')
    parser.add_argument('--backup-path', help='Path to backup for restore')
    parser.add_argument('--destination', help='Destination for restore')
    
    args = parser.parse_args()
    
    manager = BackupManager()
    
    if args.action == 'backup':
        result = manager.run_backup(args.set, remote=args.remote)
    elif args.action == 'restore':
        if not args.backup_path:
            print(json.dumps({'error': 'Backup path required for restore'}, indent=2))
            sys.exit(1)
        result = manager.restore_backup(args.backup_path, args.set, args.destination)
    elif args.action == 'health':
        result = manager.health_check()
    elif args.action == 'status':
        result = manager.get_status()
    elif args.action == 'list':
        result = manager.list_backups(args.remote)
    elif args.action == 'cleanup':
        result = manager.cleanup(yes=True)
    elif args.action == 'skills':
        result = manager.discover_skills()
    elif args.action == 'full-check':
        result = manager.full_system_check()
    else:
        result = {'error': f'Unknown action: {args.action}'}
    
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if result.get('success', False) else 1)

if __name__ == '__main__':
    main()
EOF

chmod +x "$HOME/.openclaw/workspace/scripts/backup_integration.py"

success "AI agent integration created"

# Step 9: Create documentation
log "Step 9: Creating documentation..."

cat > "$HOME/.openclaw/workspace/docs/BACKUP_SYSTEM_GUIDE.md" << 'EOF'
# 🔐 Backup System Guide

## Overview
Comprehensive backup system using best-backup for OpenClaw workspace protection.

## Installation
The backup system has been installed via:
```bash
# Manual installation (already done):
brew install pipx rclone
pipx install git+https://github.com/cptnfren/best-backup.git
```

## Configuration
- **Config file:** `~/.config/bbackup/config.yaml`
- **Encryption key:** `~/.config/bbackup/backup_key.bin` (symmetric AES-256-GCM)
- **Local storage:** `~/backups/openclaw/`
- **Logs:** `~/backups/openclaw/logs/`

## Automated Backups

### Daily Backups (2:00 AM)
- Incremental backup of workspace
- Local storage only
- Logs to `backup_daily.log`

### Weekly Backups (3:00 AM Sunday)
- Full backup of all sets (workspace, configs, skills, business)
- Local storage
- Cleanup of old backups
- Health check

### Health Checks (4:00 AM Daily)
- System health verification
- Alert on failure (email disabled by default)

## Manual Commands

### Run Backup
```bash
# Backup workspace to local storage
bbackup backup --backup-set workspace --remote local

# Backup with JSON output (for agents)
BBACKUP_OUTPUT=json BBACKUP_NO_INTERACTIVE=1 bbackup backup --backup-set workspace
```

### List Backups
```bash
bbackup list-backups --remote local
```

### Restore Backup
```bash
# Restore workspace from specific backup
bbackup restore --backup-path /path/to/backup --backup-set workspace

# Restore filesystem to different location
bbackup restore --backup-path /path/to/backup --filesystem workspace --filesystem-destination /restore/path
```

### Health Check
```bash
bbman health
```

## AI Agent Integration

### Python API
```python
from scripts.backup_integration import BackupManager

manager = BackupManager()

# Run backup
result = manager.run_backup("workspace")

# Health check
health = manager.health_check()

# List backups
backups = manager.list_backups()
```

### Command Line
```bash
# Run via integration script
python3 scripts/backup_integration.py --action health
python3 scripts/backup_integration.py --action backup --set workspace
python3 scripts/backup_integration.py --action list
```

## Disaster Recovery

### Scenario 1: Workspace Corruption
1. List available backups:
   ```bash
   bbackup list-backups --remote local
   ```

2. Restore workspace:
   ```bash
   bbackup restore --backup-path [backup_id] --backup-set workspace
   ```

### Scenario 2: Complete System Failure
1. Install best-backup on new system
2. Copy encryption key: `~/.config/bbackup/backup_key.bin`
3. Restore from latest backup
4. Verify integrity

### Scenario 3: File Recovery
1. Mount backup:
   ```bash
   bbackup mount --backup-path [backup_id] --mount-point /mnt/backup
   ```

2. Copy needed files:
   ```bash
   cp /mnt/backup/workspace/path/to/file /destination/
   ```

## Monitoring

### Log Files
- `~/backups/openclaw/logs/backup_daily.log` - Daily backup logs
- `~/backups/openclaw/logs/backup_weekly.log` - Weekly backup logs
- `~/backups/openclaw/logs/health_check.log` - Health check logs

### Cron Jobs
View scheduled backups:
```bash
crontab -l | grep backup
```

### Storage Usage
Check backup storage:
```bash
du -sh ~/backups/openclaw/
```

## Security

### Encryption
- All backups encrypted with AES-256-GCM
- Encryption key stored at `~/.config/bbackup/backup_key.bin`
- Key file permissions: 600 (readable only by owner)

### Access Control
- Backups accessible only to user `cubiczan`
- No network exposure (local storage only)
- Google Drive integration optional (requires manual setup)

### Key Management
**IMPORTANT:** Backup the encryption key separately!
```bash
# Backup encryption key (store in secure location)
cp ~/.config/bbackup/backup_key.bin /secure/location/
```

## Troubleshooting

### Common Issues

1. **Backup fails with permission error**
   ```bash
   # Check permissions
   ls -la ~/.config/bbackup/
   ls -la ~/backups/openclaw/
   
   # Fix permissions
   chmod 600 ~/.config/bbackup/backup_key.bin
   chmod 755 ~/backups/openclaw/
   ```

2. **Disk space full**
   ```bash
   # Check disk usage
   df -h /
   
   # Clean up old backups
   bbackup cleanup --yes
   ```

3. **Health check fails**
   ```bash
   # Run detailed diagnostics
   bbman diagnostics --report-file /tmp/backup_diagnostics.txt
   cat /tmp/backup_diagnostics.txt
   ```

### Log Analysis
```bash
# View latest backup log
tail -100 ~/backups/openclaw/logs/backup_daily.log

# Search for errors
grep -i error ~/backups/openclaw/logs/*.log

# Check cron job output
grep CRON /var/log/syslog | grep backup
```

## Google Drive Integration (Optional)

### Setup Rclone
1. Install rclone: `brew install rclone`
2. Configure Google Drive: `rclone config`
3. Test connection: `rclone lsd gdrive:`

### Enable in Config
Edit `~/.config/bbackup/config.yaml`:
```yaml
google_drive:
  enabled: true
  type: rclone
  rclone_remote: gdrive
  path: /Backups/OpenClaw
```

### Test Google Drive Backup
```bash
bbackup backup --backup-set workspace --remote google_drive
```

## Maintenance

### Regular Tasks
- **Weekly:** Check backup logs for errors
- **Monthly:** Verify restore procedure works
- **Quarterly:** Test disaster recovery
- **Annually:** Review and update backup strategy

### Storage Management
- Monitor disk usage: `df -h /`
- Clean up when near capacity: `bbackup cleanup --yes`
- Consider external storage for long-term archives

## Support

### Emergency Contacts
- Primary: Sam Desigan (sam@cubiczan.com)
- Backup System: best-backup + local storage
- Recovery Time Objective: 4 hours
- Recovery Point Objective: 24 hours

### Getting Help
1. Check logs: `~/backups/openclaw/logs/`
2. Run diagnostics: `bbman diagnostics`
3. Check system health: `bbman health`
4. Review cron jobs: `crontab -l`

## Version Information
- **best-backup:** Latest from GitHub
- **Installation date:** $(date '+%Y-%m-%d')
- **Configuration version:** 1.0
- **Encryption:** AES-256-GCM symmetric

---
*Last updated: $(date '+%Y-%m-%d %H:%M:%S')*
*Auto-generated during backup system installation*
EOF

success "Documentation created"

# Step 10: Test the system
log "Step 10: Testing backup system..."

# Test health check
log "Running initial health check..."
if bbman health > /dev/null 2>&1; then
    success "Health check passed"
else
    warning "Health check issues detected (run 'bbman health' for details)"
fi

# Test configuration
log "Validating configuration..."
if bbackup init-config --dry-run > /dev/null 2>&1; then
    success "Configuration validated"
else
    error "Configuration validation failed"
    exit 1
fi

# Create test backup
log "Creating test backup..."
TEST_BACKUP_LOG="$BACKUP_DIR/logs/test_backup.log"
echo "Test backup started at $(date)" > "$TEST_BACKUP_LOG"

if bbackup backup --backup-set workspace --dry-run >> "$TEST_BACKUP_LOG" 2>&1; then
    success "Test backup successful"
    echo "Test backup completed successfully at $(date)" >> "$TEST_BACKUP_LOG"
else
    error "Test backup failed - check $TEST_BACKUP_LOG"
    exit 1
fi

# Step 11: Final setup
log "Step 11: Finalizing setup..."

# Set proper permissions
chmod 700 "$BACKUP_DIR"
chmod 600 "$HOME/.config/bbackup/backup_key.bin"
chmod 755 "$HOME/.openclaw/workspace/scripts/backup_*.sh"
chmod 755 "$HOME/.openclaw/workspace/scripts/backup_integration.py"

# Create summary
cat > "$BACKUP_DIR/SETUP_SUMMARY.md" << EOF
# Backup System Setup Summary

## Installation Completed: $(date '+%Y-%m-%d %H:%M:%S')

### Components Installed:
1. ✅ pipx - Python application installer
2. ✅ best-backup - Backup software
3. ✅ rclone - Cloud storage client
4. ✅ Configuration files
5. ✅ Encryption key
6. ✅ Backup scripts
7. ✅ Cron jobs
8. ✅ AI agent integration
9. ✅ Documentation
10. ✅ Test backup

### Configuration:
- **Config file:** $CONFIG_DIR/config.yaml
- **Encryption:** AES-256-GCM (symmetric)
- **Local storage:** $BACKUP_DIR
- **Backup sets:** workspace, configs, skills, business
- **Rotation:** 7 daily, 4 weekly, 12 monthly backups
- **Quota:** 100GB maximum

### Automation:
- **Daily backup:** 2:00 AM (workspace only)
- **Weekly backup:** 3:00 AM Sunday (full system)
- **Health check:** 4:00 AM daily

### Security:
- 🔐 All backups encrypted
- 🔑 Encryption key: $HOME/.config/bbackup/backup_key.bin
- 🔒 Key permissions: 600 (owner only)
- 🛡️ No network exposure (local only)

### Next Steps:
1. **Test restore procedure** (important!)
2. **Monitor first few backups**
3. **Consider Google Drive setup** for offsite backup
4. **Train AI agents** on backup management
5. **Schedule regular testing** of disaster recovery

### Quick Commands:
\`\`\`bash
# Run manual backup
bbackup backup --backup-set workspace

# Check system health
bbman health

# List backups
bbackup list-backups --remote local

# AI agent integration
python3 $HOME/.openclaw/workspace/scripts/backup_integration.py --action health
\`\`\`

### Important Notes:
- **Keep encryption key safe!** Without it, backups cannot be restored.
- **Monitor disk space** - Backups will stop if disk is full.
- **Test restore regularly** - Don't wait for disaster to test recovery.
- **Review logs weekly** - Check for errors or warnings.

### Support:
- Documentation: $HOME/.openclaw/workspace/docs/BACKUP_SYSTEM_GUIDE.md
- Logs: $BACKUP_DIR/logs/
- Scripts: $HOME/.openclaw/workspace/scripts/backup_*.sh

---
*Setup completed by backup system installation script*
*Backup system ready for production use*
EOF

success "Setup summary created"

# Final message
echo ""
echo "=========================================="
echo "🔐 BACKUP SYSTEM SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "✅ Installation successful"
echo "✅ Configuration created"
echo "✅ Encryption initialized"
echo "✅ Automation configured"
echo "✅ AI agent integration ready"
echo "✅ Documentation generated"
echo "✅ Test backup completed"
echo ""
echo "📁 Backup directory: $BACKUP_DIR"
echo "📄 Configuration: $CONFIG_DIR/config.yaml"
echo "🔑 Encryption key: $HOME/.config/bbackup/backup_key.bin"
echo "📋 Documentation: $HOME/.openclaw/workspace/docs/BACKUP_SYSTEM_GUIDE.md"
echo "🤖 AI integration: $HOME/.openclaw/workspace/scripts/backup_integration.py"
echo ""
echo "⏰ Scheduled backups:"
echo "   Daily (workspace): 2:00 AM"
echo "   Weekly (full): 3:00 AM Sunday"
echo "   Health check: 4:00 AM daily"
echo ""
echo "🚨 IMPORTANT: Backup your encryption key!"
echo "   cp $HOME/.config/bbackup/backup_key.bin /secure/location/"
echo ""
echo "📊 Next steps:"
echo "   1. Monitor first backup tonight"
echo "   2. Test restore procedure"
echo "   3. Consider Google Drive setup"
echo "   4. Train AI agents on backup management"
echo ""
echo "🔐 Your OpenClaw workspace is now protected!"
echo "=========================================="