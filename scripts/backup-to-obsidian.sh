#!/bin/bash
# Backup OpenClaw Workspace to Obsidian
# Run daily to keep Obsidian in sync

WORKSPACE="$HOME/.openclaw/workspace"
OBSIDIAN_VAULT="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Cubiczan"
BACKUP_DIR="$OBSIDIAN_VAULT/OpenClaw Workspace Backup"
LOG_FILE="$WORKSPACE/logs/obsidian-backup.log"

# Create log directory
mkdir -p "$(dirname "$LOG_FILE")"

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Starting Obsidian backup..."

# Check if Obsidian vault exists
if [ ! -d "$OBSIDIAN_VAULT" ]; then
    log "ERROR: Obsidian vault not found at $OBSIDIAN_VAULT"
    exit 1
fi

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Count files before
BEFORE=$(find "$BACKUP_DIR" -name "*.md" -type f 2>/dev/null | wc -l)

# Sync MD files (using rsync for efficiency)
rsync -av --delete \
    --include="*/" \
    --include="*.md" \
    --exclude="*" \
    "$WORKSPACE/" "$BACKUP_DIR/" >> "$LOG_FILE" 2>&1

# Count files after
AFTER=$(find "$BACKUP_DIR" -name "*.md" -type f 2>/dev/null | wc -l)

# Get backup size
SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)

log "Backup complete: $AFTER MD files ($SIZE)"
log "Files: Before=$BEFORE, After=$AFTER"

# Create a summary note in Obsidian
cat > "$BACKUP_DIR/📋 Backup Info.md" << EOF
# OpenClaw Workspace Backup

**Last Updated:** $(date '+%Y-%m-%d %H:%M:%S')

## Statistics
- **Total Files:** $AFTER markdown files
- **Backup Size:** $SIZE
- **Source:** ~/.openclaw/workspace

## Key Files
- MEMORY.md - Agent memory and context
- IDENTITY.md - Agent identity
- morning-brief.md - Daily briefings
- meditations.md - Reflection topics
- pending-approvals.md - Pending actions

## Folders
- \`infrastructure/\` - System setup docs
- \`memory/\` - Memory files
- \`skills/\` - Skill documentation
- \`leads/\` - Lead generation
- \`deals/\` - Deal origination

## Auto-Backup
This folder is automatically synced daily.
EOF

log "Backup info updated"
echo ""
echo "✅ Backup complete: $AFTER files synced to Obsidian"
