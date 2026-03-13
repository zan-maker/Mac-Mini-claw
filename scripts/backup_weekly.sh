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
