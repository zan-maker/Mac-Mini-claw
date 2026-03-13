#!/bin/bash

# Backup Hoppscotch collections
cd "$(dirname "$0")"
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "💾 Backing up Hoppscotch data..."
docker cp hoppscotch:/app/data "$BACKUP_DIR/"

echo "✅ Backup created: $BACKUP_DIR"
echo "   Size: $(du -sh "$BACKUP_DIR" | cut -f1)"
