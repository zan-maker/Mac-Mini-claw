#!/bin/bash

# View Hoppscotch logs
cd "$(dirname "$0")"
echo "📋 Viewing Hoppscotch logs..."
docker-compose logs -f
