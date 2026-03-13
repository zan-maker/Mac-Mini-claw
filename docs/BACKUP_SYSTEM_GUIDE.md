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
