#!/bin/bash
# Simple Backup Script for OpenClaw Workspace
# Uses rsync for incremental backups with hard links

set -e

# Configuration
BACKUP_ROOT="/Users/cubiczan/backups/openclaw"
SOURCE_DIR="/Users/cubiczan/.openclaw/workspace"
BACKUP_NAME="workspace_backup_$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="$BACKUP_ROOT/$BACKUP_NAME"
LATEST_LINK="$BACKUP_ROOT/latest"
LOG_FILE="$BACKUP_ROOT/logs/backup_$(date +%Y%m%d).log"

# Create directories
mkdir -p "$BACKUP_ROOT/logs"
mkdir -p "$BACKUP_DIR"

# Exclude patterns
EXCLUDE_FILE="$BACKUP_ROOT/exclude_patterns.txt"
cat > "$EXCLUDE_FILE" << 'EOF'
*.tmp
*.log
.cache/
node_modules/
__pycache__/
.git/
*.pyc
*.pyo
.DS_Store
Thumbs.db
*.swp
*.swo
*~
EOF

# Start backup
echo "==========================================" >> "$LOG_FILE"
echo "Backup started: $(date)" >> "$LOG_FILE"
echo "Source: $SOURCE_DIR" >> "$LOG_FILE"
echo "Destination: $BACKUP_DIR" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

# Use rsync with hard links for incremental backup
if [ -L "$LATEST_LINK" ]; then
    echo "Creating incremental backup (hard linked to previous backup)" >> "$LOG_FILE"
    rsync -avh \
        --delete \
        --exclude-from="$EXCLUDE_FILE" \
        --link-dest="$LATEST_LINK" \
        "$SOURCE_DIR/" \
        "$BACKUP_DIR/" \
        >> "$LOG_FILE" 2>&1
else
    echo "Creating first full backup" >> "$LOG_FILE"
    rsync -avh \
        --delete \
        --exclude-from="$EXCLUDE_FILE" \
        "$SOURCE_DIR/" \
        "$BACKUP_DIR/" \
        >> "$LOG_FILE" 2>&1
fi

# Update latest symlink
rm -f "$LATEST_LINK"
ln -s "$BACKUP_DIR" "$LATEST_LINK"

# Calculate backup size
BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
TOTAL_SIZE=$(du -sh "$BACKUP_ROOT" | cut -f1)

echo "Backup completed: $(date)" >> "$LOG_FILE"
echo "Backup size: $BACKUP_SIZE" >> "$LOG_FILE"
echo "Total backup storage: $TOTAL_SIZE" >> "$LOG_FILE"
echo "Backup location: $BACKUP_DIR" >> "$LOG_FILE"
echo "Latest symlink: $LATEST_LINK" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

# Cleanup old backups (keep last 7 days)
echo "Cleaning up old backups..." >> "$LOG_FILE"
find "$BACKUP_ROOT" -maxdepth 1 -type d -name "workspace_backup_*" -mtime +7 -exec rm -rf {} \; 2>/dev/null || true

# List remaining backups
REMAINING_BACKUPS=$(find "$BACKUP_ROOT" -maxdepth 1 -type d -name "workspace_backup_*" | wc -l)
echo "Remaining backups: $REMAINING_BACKUPS" >> "$LOG_FILE"

echo "Backup completed successfully!"
echo "Log file: $LOG_FILE"
echo "Backup location: $BACKUP_DIR"
echo "Latest symlink: $LATEST_LINK"

# Create restore script
cat > "$BACKUP_DIR/RESTORE_INSTRUCTIONS.md" << EOF
# Restore Instructions

To restore from this backup:

## Option 1: Copy files back
\`\`\`bash
# Copy entire workspace back
rsync -avh "$BACKUP_DIR/" "/Users/cubiczan/.openclaw/workspace/"

# Or copy specific files
cp -r "$BACKUP_DIR/path/to/file" "/Users/cubiczan/.openclaw/workspace/path/to/"
\`\`\`

## Option 2: Use the latest symlink
\`\`\`bash
# The 'latest' symlink always points to the most recent backup
LATEST_BACKUP="/Users/cubiczan/backups/openclaw/latest"
rsync -avh "\$LATEST_BACKUP/" "/Users/cubiczan/.openclaw/workspace/"
\`\`\`

## Backup Information
- **Backup date:** $(date)
- **Backup size:** $BACKUP_SIZE
- **Source:** $SOURCE_DIR
- **Backup location:** $BACKUP_DIR

## Files included:
$(find "$BACKUP_DIR" -type f | wc -l) files
$(find "$BACKUP_DIR" -type d | wc -l) directories

## Excluded patterns:
$(cat "$EXCLUDE_FILE")
EOF

echo "Restore instructions created: $BACKUP_DIR/RESTORE_INSTRUCTIONS.md"