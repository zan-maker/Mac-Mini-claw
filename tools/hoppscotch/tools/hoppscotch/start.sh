#!/bin/bash

# Start Hoppscotch
cd "$(dirname "$0")"
echo "🚀 Starting Hoppscotch..."
docker-compose up -d

echo ""
echo "✅ Hoppscotch should now be running at:"
echo "   🌐 http://localhost:3000"
echo ""
echo "📋 Management commands:"
echo "   ./start.sh          - Start Hoppscotch"
echo "   ./stop.sh           - Stop Hoppscotch"
echo "   ./logs.sh           - View logs"
echo "   ./backup.sh         - Backup collections"
echo ""
echo "🎯 Next steps:"
echo "   1. Open http://localhost:3000"
echo "   2. Create your first collection"
echo "   3. Set up environment variables"
echo "   4. Start testing APIs!"
