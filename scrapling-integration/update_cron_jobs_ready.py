#!/usr/bin/env python3
# Script to update cron jobs with Scrapling-first approach
# Run this in OpenClaw session

import subprocess
import json

# Update Expense Reduction Lead Gen
expense_reduction_msg = '''# Expense Reduction Lead Gen - Scrapling-First Enhanced

## 🚀 NEW: Scrapling Integration Activated

**Scrapling gives us an unfair advantage:**
- **774x faster** than traditional web scraping
- **Cloudflare bypass** - automatically handles anti-bot systems
- **Maximum stealth** - no bot detection
- **Adaptive scraping** - no selector maintenance needed
- **AI-powered extraction** - natural language queries

## 📋 Your Task (Scrapling-First Approach)

### Step 1: Try Scrapling First (Primary Source)
```python
# Use Scrapling integration for fast, reliable data extraction
from scrapling_integration.cron_integration import ScraplingCronIntegration

async def run_with_scrapling():
    # Initialize Scrapling with stealth mode
    scrapling = ScraplingCronIntegration(stealth_mode=True)
    success = await scrapling.initialize()
    
    if success:
        print("✅ Scrapling initialized successfully")
        # Use Scrapling for data extraction
        # [Add job-specific Scrapling code here]...'''

# Update Defense Sector Lead Gen  
defense_sector_msg = '''# Defense Sector Lead Gen - Scrapling-First Enhanced

## 🚀 NEW: Scrapling Integration Activated

**Scrapling gives us an unfair advantage:**
- **774x faster** than traditional web scraping
- **Cloudflare bypass** - automatically handles anti-bot systems
- **Maximum stealth** - no bot detection
- **Adaptive scraping** - no selector maintenance needed
- **AI-powered extraction** - natural language queries

## 📋 Your Task (Scrapling-First Approach)

### Step 1: Try Scrapling First (Primary Source)
```python
# Use Scrapling integration for fast, reliable data extraction
from scrapling_integration.cron_integration import ScraplingCronIntegration

async def run_with_scrapling():
    # Initialize Scrapling with stealth mode
    scrapling = ScraplingCronIntegration(stealth_mode=True)
    success = await scrapling.initialize()
    
    if success:
        print("✅ Scrapling initialized successfully")
        # Use Scrapling for data extraction
        # [Add job-specific Scrapling code here]
  ...'''

print("Ready to update cron jobs with Scrapling-first approach!")
print("Copy the messages above and update each cron job via:")
print("1. cron update --jobId <id> --patch '{"payload": {"message": "<message>"}}'")
print("2. Or use the OpenClaw web interface")
