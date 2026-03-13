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
