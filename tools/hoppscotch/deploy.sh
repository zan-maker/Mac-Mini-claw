#!/bin/bash

# 🚀 Hoppscotch Deployment Script
# Self-hosted API development platform

set -e

echo "========================================="
echo "🚀 DEPLOYING HOPPSCOTCH (SELF-HOSTED)"
echo "========================================="
echo "Open-source alternative to Postman/Insomnia"
echo "Cost savings: $110/month"
echo "========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "Install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Create directories
mkdir -p tools/hoppscotch/{collections,environments,scripts,docs}

echo ""
echo "📁 Creating directory structure..."
echo "✅ Directories created in tools/hoppscotch/"

echo ""
echo "🐳 Creating Docker Compose configuration..."

cat > tools/hoppscotch/docker-compose.yml << 'DOCKER_EOF'
version: '3.8'
services:
  hoppscotch:
    image: hoppscotch/hoppscotch:latest
    container_name: hoppscotch
    ports:
      - "3000:3000"
    volumes:
      - hoppscotch_data:/app/data
      - ./collections:/app/collections:ro
    environment:
      - NODE_ENV=production
      - VITE_BASE_URL=http://localhost:3000
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  hoppscotch_data:
DOCKER_EOF

echo "✅ Docker Compose configuration created"

echo ""
echo "🔧 Creating startup script..."

cat > tools/hoppscotch/start.sh << 'START_EOF'
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
echo "echo "   1. Open http://localhost:3000"
echo "   2. Create your first collection"
echo "   3. Set up environment variables"
echo "   4. Start testing APIs!"
START_EOF

chmod +x tools/hoppscotch/start.sh

cat > tools/hoppscotch/stop.sh << 'STOP_EOF'
#!/bin/bash

# Stop Hoppscotch
cd "$(dirname "$0")"
echo "🛑 Stopping Hoppscotch..."
docker-compose down

echo "✅ Hoppscotch stopped"
STOP_EOF

chmod +x tools/hoppscotch/stop.sh

cat > tools/hoppscotch/logs.sh << 'LOGS_EOF'
#!/bin/bash

# View Hoppscotch logs
cd "$(dirname "$0")"
echo "📋 Viewing Hoppscotch logs..."
docker-compose logs -f
LOGS_EOF

chmod +x tools/hoppscotch/logs.sh

cat > tools/hoppscotch/backup.sh << 'BACKUP_EOF'
#!/bin/bash

# Backup Hoppscotch collections
cd "$(dirname "$0")"
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "💾 Backing up Hoppscotch data..."
docker cp hoppscotch:/app/data "$BACKUP_DIR/"

echo "✅ Backup created: $BACKUP_DIR"
echo "   Size: $(du -sh "$BACKUP_DIR" | cut -f1)"
BACKUP_EOF

chmod +x tools/hoppscotch/backup.sh

echo "✅ Management scripts created"

echo ""
echo "📝 Creating initial API collections..."

# Lead Generation API Collection
cat > tools/hoppscotch/collections/lead-generation.json << 'COLLECTION_EOF'
{
  "name": "Lead Generation APIs",
  "folders": [
    {
      "name": "Brevo Email",
      "requests": [
        {
          "name": "Send Transactional Email",
          "method": "POST",
          "url": "https://api.brevo.com/v3/smtp/email",
          "headers": {
            "api-key": "{{BREVO_API_KEY}}",
            "Content-Type": "application/json"
          },
          "body": {
            "sender": {
              "name": "Agent Manager",
              "email": "sam@impactquadrant.info"
            },
            "to": [
              {
                "email": "{{TEST_EMAIL}}",
                "name": "Test Recipient"
              }
            ],
            "subject": "Test Email from Hoppscotch",
            "htmlContent": "<p>This is a test email from our AI agent system.</p>"
          },
          "tests": [
            "pm.test('Status code is 200', function() { pm.response.to.have.status(200); });",
            "pm.test('Response has message ID', function() { pm.response.to.have.jsonBody('messageId'); });"
          ]
        }
      ]
    },
    {
      "name": "Serper Search",
      "requests": [
        {
          "name": "Search for Companies",
          "method": "POST",
          "url": "https://google.serper.dev/search",
          "headers": {
            "X-API-KEY": "{{SERPER_API_KEY}}",
            "Content-Type": "application/json"
          },
          "body": {
            "q": "construction companies 50-200 employees",
            "gl": "us",
            "hl": "en",
            "num": 10
          }
        }
      ]
    }
  ]
}
COLLECTION_EOF

# LLM API Collection
cat > tools/hoppscotch/collections/llm-apis.json << 'LLM_EOF'
{
  "name": "LLM APIs",
  "folders": [
    {
      "name": "OpenRouter",
      "requests": [
        {
          "name": "Chat Completion",
          "method": "POST",
          "url": "https://openrouter.ai/api/v1/chat/completions",
          "headers": {
            "Authorization": "Bearer {{OPENROUTER_API_KEY}}",
            "Content-Type": "application/json"
          },
          "body": {
            "model": "deepseek/deepseek-r1",
            "messages": [
              {
                "role": "user",
                "content": "Hello, how are you?"
              }
            ],
            "max_tokens": 100
          }
        }
      ]
    }
  ]
}
COLLECTION_EOF

echo "✅ Initial API collections created"

echo ""
echo "🌍 Creating environment templates..."

# Development environment
cat > tools/hoppscotch/environments/development.json << 'ENV_EOF'
{
  "name": "Development",
  "values": [
    {
      "key": "API_BASE_URL",
      "value": "http://localhost:3000",
      "enabled": true
    },
    {
      "key": "BREVO_API_KEY",
      "value": "{{BREVO_DEV_KEY}}",
      "enabled": true
    },
    {
      "key": "OPENROUTER_API_KEY",
      "value": "{{OPENROUTER_DEV_KEY}}",
      "enabled": true
    },
    {
      "key": "TEST_EMAIL",
      "value": "test@impactquadrant.info",
      "enabled": true
    }
  ]
}
ENV_EOF

# Production environment
cat > tools/hoppscotch/environments/production.json << 'PROD_EOF'
{
  "name": "Production",
  "values": [
    {
      "key": "API_BASE_URL",
      "value": "https://api.impactquadrant.info",
      "enabled": true
    },
    {
      "key": "BREVO_API_KEY",
      "value": "{{BREVO_PROD_KEY}}",
      "enabled": true
    },
    {
      "key": "OPENROUTER_API_KEY",
      "value": "{{OPENROUTER_PROD_KEY}}",
      "enabled": true
    },
    {
      "key": "TEST_EMAIL",
      "value": "sam@impactquadrant.info",
      "enabled": true
    }
  ]
}
PROD_EOF

echo "✅ Environment templates created"

echo ""
echo "📚 Creating documentation..."

cat > tools/hoppscotch/docs/QUICK_START.md << 'DOCS_EOF'
# 🚀 Hoppscotch Quick Start Guide

## Overview
Hoppscotch is our self-hosted API development platform, replacing paid tools like Postman and Insomnia.

## Getting Started

### 1. Start Hoppscotch
```bash
cd tools/hoppscotch
./start.sh
```

### 2. Access the Interface
Open your browser to: http://localhost:3000

### 3. Import Collections
1. Click "Collections" in sidebar
2. Click "Import"
3. Select files from `tools/hoppscotch/collections/`

### 4. Set Up Environments
1. Click "Environments" in sidebar
2. Click "Import"
3. Select files from `tools/hoppscotch/environments/`
4. Fill in your actual API keys

## Key Features

### Collections
Organized API requests by service:
- `lead-generation.json` - Lead gen APIs (Brevo, Serper, etc.)
- `llm-apis.json` - LLM service APIs (OpenRouter, etc.)
- More to come...

### Environments
Switch between configurations:
- **Development** - Local testing
- **Production** - Live APIs
- **Staging** - Pre-production testing

### Testing
Write JavaScript tests for API responses:
```javascript
pm.test("Status is 200", () => pm.response.to.have.status(200));
pm.test("Response time < 2s", () => pm.expect(pm.response.responseTime).to.be.below(2000));
```

## Automation

### CLI Installation
```bash
npm install -g @hoppscotch/cli
```

### Export Collections
```bash
hoppscotch export --all --format json --output collections/
```

### Run Tests
```bash
hoppscotch test --collection lead-generation --env production
```

## Management

### Start/Stop
```bash
./start.sh    # Start Hoppscotch
./stop.sh     # Stop Hoppscotch
./logs.sh     # View logs
./backup.sh   # Backup data
```

### Backup & Restore
- Backups stored in `tools/hoppscotch/backups/`
- Automatic backups recommended weekly

## Integration with Our System

### Testing Cron Jobs
```bash
# Before deploying cron jobs
cd tools/hoppscotch
hoppscotch test --collection lead-generation --env production
```

### CI/CD Pipeline
Add to `.github/workflows/api-tests.yml`:
```yaml
- name: Run API tests
  run: hoppscotch test --all --env staging
```

## Troubleshooting

### Common Issues

1. **Port 3000 already in use**
   ```bash
   # Edit docker-compose.yml to use different port
   ports:
     - "3001:3000"
   ```

2. **Cannot access localhost:3000**
   ```bash
   # Check if container is running
   docker ps | grep hoppscotch
   
   # View logs for errors
   ./logs.sh
   ```

3. **Import errors**
   - Ensure JSON files are valid
   - Check file permissions
   - Restart Hoppscotch after imports

## Support
- [Hoppscotch Documentation](https://docs.hoppscotch.io)
- [GitHub Issues](https://github.com/hoppscotch/hoppscotch/issues)
- Internal Slack/Teams channel for API discussions

## Cost Savings
- **Previous:** $110/month (Postman Pro + other tools)
- **Current:** $0/month (self-hosted)
- **Annual Savings:** $1,320
DOCS_EOF

echo "✅ Documentation created"

echo ""
echo "🎯 HOPPSCOTCH DEPLOYMENT READY!"
echo "========================================="
echo ""
echo "📁 Files created in tools/hoppscotch/:"
echo "   • docker-compose.yml          - Deployment config"
echo "   • start.sh / stop.sh          - Management scripts"
echo "   • collections/                - API collections"
echo "   • environments/               - Environment configs"
echo "   • docs/QUICK_START.md         - User guide"
echo ""
echo "🚀 To deploy Hoppscotch:"
echo "   1. cd tools/hoppscotch"
echo "   2. ./start.sh"
echo "   3. Open http://localhost:3000"
echo ""
echo "💰 Cost savings: $110/month"
echo "📈 Annual savings: $1,320"
echo ""
echo "Ready to deploy Hoppscotch?"
