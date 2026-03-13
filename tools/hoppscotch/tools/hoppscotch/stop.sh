#!/bin/bash

# Stop Hoppscotch
cd "$(dirname "$0")"
echo "🛑 Stopping Hoppscotch..."
docker-compose down

echo "✅ Hoppscotch stopped"
