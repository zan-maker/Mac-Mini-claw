# 🚀 Simplified Hoppscotch Integration

## Overview
Instead of running the full self-hosted Hoppscotch platform, we're using:
- **Hoppscotch CLI** for API testing automation
- **JSON collections** stored in version control
- **Simple scripts** for integration with AI agents

## Benefits
- ✅ No database setup required
- ✅ No Docker containers to manage
- ✅ Faster setup and deployment
- ✅ Same API testing capabilities
- ✅ Still saves $110/month vs Postman

## Setup

### 1. Install Hoppscotch CLI
```bash
npm install -g @hoppscotch/cli
```

### 2. Verify installation
```bash
hoppscotch --version
```

### 3. Create API collections
Collections are stored as JSON files in `collections/` directory.

## Usage

### Test APIs for Cron Jobs
```bash
# Test lead generation APIs
hoppscotch test --collection collections/lead-generation.json

# Test all collections
hoppscotch test --all
```

### Export/Import Collections
```bash
# Export collections
hoppscotch export --all --format json --output collections/

# Import collections
hoppscotch import collections/lead-generation.json
```

## Integration with AI Agents

### Pre-flight API Checks
```bash
#!/bin/bash
# cron-preflight.sh
echo "🧪 Running API checks before cron jobs..."

# Test lead generation APIs
hoppscotch test --collection collections/lead-generation.json

# Test email APIs
hoppscotch test --collection collections/email-services.json

# If any test fails, exit with error
if [ $? -ne 0 ]; then
    echo "❌ API checks failed - aborting cron jobs"
    exit 1
fi

echo "✅ All API checks passed - proceeding with cron jobs"
```

### Automated Testing
```bash
#!/bin/bash
# run-api-tests.sh
echo "🚀 Running automated API tests..."

# Run all tests
hoppscotch test --all --report html --output test-report.html

# Check results
if [ $? -eq 0 ]; then
    echo "✅ All API tests passed"
else
    echo "❌ Some API tests failed"
    # Send alert, log error, etc.
fi
```

## Collections Structure

```
collections/
├── lead-generation.json      # Lead gen APIs (Brevo, Serper, etc.)
├── llm-apis.json            # LLM service APIs (OpenRouter, etc.)
├── email-services.json      # Email sending APIs
├── database-apis.json       # Database APIs (Supabase, etc.)
└── internal-agents.json     # Internal AI agent APIs
```

## Environment Variables

Create `.env` file:
```bash
# API Keys
BREVO_API_KEY=your_brevo_key
OPENROUTER_API_KEY=your_openrouter_key
SERPER_API_KEY=your_serper_key

# Environment
ENVIRONMENT=production
API_BASE_URL=https://api.impactquadrant.info
```

## CI/CD Integration

Add to `.github/workflows/api-tests.yml`:
```yaml
name: API Tests
on: [push, pull_request]

jobs:
  test-apis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install Hoppscotch CLI
        run: npm install -g @hoppscotch/cli
      - name: Run API tests
        run: hoppscotch test --all
      - name: Upload test results
        uses: actions/upload-artifact@v3
        with:
          name: api-test-results
          path: test-report.html
```

## Cost Savings

- **Previous:** $110/month (Postman Pro + other tools)
- **Current:** $0/month (Hoppscotch CLI + JSON collections)
- **Annual Savings:** $1,320

## Next Steps

1. Install Hoppscotch CLI
2. Create API collections
3. Set up pre-flight checks for cron jobs
4. Integrate with CI/CD pipeline
5. Monitor API health

## Troubleshooting

### Common Issues

1. **CLI not found**
   ```bash
   npm install -g @hoppscotch/cli
   ```

2. **Collection import errors**
   - Ensure JSON files are valid
   - Check file permissions
   - Verify collection structure

3. **API test failures**
   - Check API endpoints are accessible
   - Verify API keys are valid
   - Check network connectivity

## Support
- [Hoppscotch CLI Documentation](https://docs.hoppscotch.io/cli)
- [GitHub Issues](https://github.com/hoppscotch/hoppscotch/issues)
- [Discord Community](https://discord.gg/hoppscotch)
