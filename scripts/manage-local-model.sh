#!/bin/bash
# Manage local Ollama model service

case "$1" in
    start)
        echo "Starting Ollama service..."
        ollama serve > /tmp/ollama.log 2>&1 &
        echo $! > /tmp/ollama.pid
        sleep 3
        echo "✅ Ollama service started"
        ;;
    stop)
        echo "Stopping Ollama service..."
        if [ -f /tmp/ollama.pid ]; then
            kill $(cat /tmp/ollama.pid) 2>/dev/null
            rm /tmp/ollama.pid
        fi
        pkill -f "ollama serve" 2>/dev/null
        echo "✅ Ollama service stopped"
        ;;
    status)
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            echo "✅ Ollama service is running"
            curl -s http://localhost:11434/api/tags | jq '.models'
        else
            echo "❌ Ollama service is not running"
        fi
        ;;
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        exit 1
        ;;
esac
