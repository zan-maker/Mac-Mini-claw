#!/usr/bin/env python3
"""
Social Media Outreach Setup Script
Configures Pinchtab profiles and sets up automation
"""

import os
import sys
import json
from datetime import datetime

def create_setup_guide():
    """Create setup guide for social media outreach system"""
    
    guide = """# 🚀 SOCIAL MEDIA OUTREACH SETUP GUIDE

## 📋 PREREQUISITES

### 1. Pinchtab Installation
```bash
# Install Pinchtab
curl -fsSL https://pinchtab.com/install.sh | sh

# Start Pinchtab server
pinchtab start

# Verify installation
pinchtab --version
curl http://localhost:9867/health
```

### 2. LinkedIn Profile Setup in Pinchtab

#### Step 1: Create Browser Profiles
```bash
# Create profile for Sam Desigan
pinchtab profile create sam-desigan --name "Sam Desigan LinkedIn"

# Create profile for Shyam Desigan  
pinchtab profile create shyam-desigan --name "Shyam Desigan LinkedIn"
```

#### Step 2: Login to LinkedIn (One-time)
```bash
# For each profile, you'll need to manually login once:
# 1. Start Pinchtab with profile
pinchtab start --profile sam-desigan

# 2. Open browser and navigate to LinkedIn
# 3. Login with credentials
# 4. Close browser when done

# Repeat for shyam-desigan profile
```

### 3. Environment Configuration

#### Create Environment File
```bash
cat > /Users/cubiczan/.openclaw/workspace/.env.social_media << 'EOF'
# Social Media Automation Configuration
PINCHTAB_HOST=http://localhost:9867
PINCHTAB_PROFILE_SAM=sam-desigan
PINCHTAB_PROFILE_SHYAM=shyam-desigan

# LinkedIn URLs
LINKEDIN_SAM=https://linkedin.com/in/sam-desigan-198a742a7
LINKEDIN_SHYAM=https://linkedin.com/in/shyam-desigan-3b616

# Posting Schedule
POSTING_TIMES_SAM=09:00,12:00,17:00,20:00
POSTING_TIMES_SHYAM=08:00,11:00,16:00,19:00

# Content Settings
CONTENT_STRATEGY_FILE=/Users/cubiczan/.openclaw/workspace/social_media_outreach/weekly_strategy.json
CONTENT_CALENDAR_FILE=/Users/cubiczan/.openclaw/workspace/social_media_outreach/content_calendar.json
EOF
```

## 🚀 QUICK START

### Option 1: Full Automation Setup
```bash
# 1. Run setup script
python3 /Users/cubiczan/.openclaw/workspace/scripts/setup_social_media.py

# 2. Test automation
python3 /Users/cubiczan/.openclaw/workspace/scripts/pinchtab_social_media.py --test

# 3. Schedule daily automation
crontab -e
# Add: 0 7,11,15,19 * * * python3 /Users/cubiczan/.openclaw/workspace/scripts/pinchtab_social_media.py
```

### Option 2: Manual Execution
```bash
# 1. Generate weekly strategy
python3 /Users/cubiczan/.openclaw/workspace/scripts/social_media_orchestrator.py

# 2. Review generated content
cat /Users/cubiczan/.openclaw/workspace/social_media_outreach/content_calendar_*.json | jq '.[] | {profile, day, time, topic}'

# 3. Execute automation
python3 /Users/cubiczan/.openclaw/workspace/scripts/pinchtab_social_media.py
```

## 📊 MONITORING SETUP

### 1. Performance Dashboard
```bash
# Create monitoring script
cat > /Users/cubiczan/.openclaw/workspace/scripts/monitor_social_media.py << 'EOF'
#!/usr/bin/env python3
# Social Media Performance Monitor
import json
from datetime import datetime

def monitor_performance():
    posts_file = "/Users/cubiczan/.openclaw/workspace/linkedin_posts.json"
    
    if os.path.exists(posts_file):
        with open(posts_file, 'r') as f:
            posts = json.load(f)
        
        print(f"📊 PERFORMANCE DASHBOARD")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📝 Total Posts: {len(posts)}")
        
        # Calculate by profile
        sam_posts = [p for p in posts if p.get('profile') == 'sam_desigan']
        shyam_posts = [p for p in posts if p.get('profile') == 'shyam_desigan']
        
        print(f"👤 Sam Desigan: {len(sam_posts)} posts")
        print(f"👤 Shyam Desigan: {len(shyam_posts)} posts")
        
        # Recent activity
        today = datetime.now().date()
        today_posts = [p for p in posts 
                      if datetime.fromisoformat(p.get('timestamp', '')).date() == today]
        
        print(f"📈 Today's Activity: {len(today_posts)} posts")
EOF

# Make executable
chmod +x /Users/cubiczan/.openclaw/workspace/scripts/monitor_social_media.py
```

### 2. Daily Reporting
```bash
# Add to crontab for daily report at 6 PM
crontab -e
# Add: 0 18 * * * python3 /Users/cubiczan/.openclaw/workspace/scripts/monitor_social_media.py >> /tmp/social_media_report.log
```

## 🔧 TROUBLESHOOTING

### Common Issues & Solutions

#### Issue 1: Pinchtab Profiles Not Found
```bash
# List existing profiles
pinchtab profile list

# Create missing profiles
pinchtab profile create sam-desigan
pinchtab profile create shyam-desigan

# Verify profiles
pinchtab profile info sam-desigan
```

#### Issue 2: LinkedIn Login Required
```bash
# Manual login process:
# 1. Start Pinchtab with profile
pinchtab start --profile sam-desigan

# 2. In another terminal, check browser URL
curl http://localhost:9867/instances

# 3. Open the URL in your regular browser
# 4. Login to LinkedIn
# 5. Close when done
```

#### Issue 3: Automation Not Posting
```bash
# Check if posts are scheduled for current time
python3 /Users/cubiczan/.openclaw/workspace/scripts/pinchtab_social_media.py --debug

# Check content calendar
cat /Users/cubiczan/.openclaw/workspace/social_media_outreach/content_calendar_*.json | \
  jq '.[] | select(.date == "'$(date +%Y-%m-%d)'") | {time, profile, topic}'
```

#### Issue 4: Performance Monitoring
```bash
# Check automation logs
tail -f /tmp/pinchtab_automation.log

# Check posted content
cat /Users/cubiczan/.openclaw/workspace/linkedin_posts.json | jq '.[-5:]'

# Check Pinchtab health
curl -s http://localhost:9867/health | jq '.'
```

## 🎯 OPTIMIZATION TIPS

### 1. Content Strategy
- **Review weekly performance** every Friday
- **Adjust posting times** based on engagement data
- **Test different content formats** (text, images, videos)
- **Monitor competitor activity** for inspiration

### 2. Automation Efficiency
- **Batch process** posts for efficiency
- **Use headless mode** for background operations
- **Implement retry logic** for failed posts
- **Monitor resource usage** of browser instances

### 3. Engagement Strategy
- **Respond to comments** within 2 hours
- **Engage with relevant content** from others
- **Use analytics** to identify best-performing topics
- **Adjust strategy** based on audience feedback

## 📁 FILE STRUCTURE

```
/Users/cubiczan/.openclaw/workspace/
├── scripts/
│   ├── social_media_orchestrator.py    # Strategy generation
│   ├── pinchtab_social_media.py        # Automation execution
│   ├── monitor_social_media.py         # Performance tracking
│   └── setup_social_media.py           # System setup
├── social_media_outreach/
│   ├── weekly_strategy_*.json          # Weekly strategies
│   ├── content_calendar_*.json         # Scheduled posts
│   └── agent_configurations.json       # Agency-agents settings
├── linkedin_posts.json                 # Posted content log
└── automation_report.json              # Automation performance
```

## 🚀 DEPLOYMENT CHECKLIST

### Phase 1: Setup (Day 1)
- [ ] Install and configure Pinchtab
- [ ] Create browser profiles for both LinkedIn accounts
- [ ] Manually login to LinkedIn for each profile
- [ ] Configure environment variables
- [ ] Test basic automation

### Phase 2: Content Strategy (Day 2)
- [ ] Generate initial weekly strategy
- [ ] Review and approve content calendar
- [ ] Set up monitoring and reporting
- [ ] Test full automation cycle

### Phase 3: Execution (Day 3+)
- [ ] Schedule daily automation via cron
- [ ] Monitor daily performance
- [ ] Adjust strategy based on results
- [ ] Expand to additional platforms (Twitter)

### Phase 4: Optimization (Week 2+)
- [ ] Analyze weekly performance reports
- [ ] Optimize posting times and content
- [ ] Implement advanced engagement strategies
- [ ] Scale system as needed

## 📞 SUPPORT

### Quick Reference Commands
```bash
# Start the system
./start_social_media.sh

# Check status
./check_status.sh

# View logs
tail -f /tmp/social_media_automation.log

# Generate report
python3 scripts/monitor_social_media.py --report
```

### Getting Help
1. **Check logs**: `/tmp/pinchtab_automation.log`
2. **Verify profiles**: `pinchtab profile list`
3. **Test connectivity**: `curl http://localhost:9867/health`
4. **Review content**: Check generated JSON files

## 🎉 READY TO LAUNCH!

Your social media outreach system is configured and ready. The integration of **Agency-Agents framework** with **Pinchtab automation** creates a powerful, cost-effective solution for building professional presence on LinkedIn.

**Next Action**: Run the setup script and begin automation!
"""

    # Save guide
    guide_file = "/Users/cubiczan/.openclaw/workspace/SOCIAL_MEDIA_SETUP_GUIDE.md"
    with open(guide_file, 'w') as f:
        f.write(guide)
    
    print(f"✅ Setup guide saved to: {guide_file}")
    
    # Create quick start script
    quick_start = """#!/bin/bash
# Quick Start Script for Social Media Outreach

echo "🚀 SOCIAL MEDIA OUTREACH QUICK START"
echo "========================================"

# Check prerequisites
echo "1. Checking prerequisites..."
if ! command -v pinchtab &> /dev/null; then
    echo "❌ Pinchtab not installed"
    echo "   Install with: curl -fsSL https://pinchtab.com/install.sh | sh"
    exit 1
fi

if ! curl -s http://localhost:9867/health &> /dev/null; then
    echo "⚠️  Pinchtab server not running"
    echo "   Start with: pinchtab start"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Generate strategy
echo "2. Generating weekly strategy..."
python3 /Users/cubiczan/.openclaw/workspace/scripts/social_media_orchestrator.py

# Check content calendar
echo "3. Checking content calendar..."
if [ -f "/Users/cubiczan/.openclaw/workspace/social_media_outreach/content_calendar_*.json" ]; then
    echo "✅ Content calendar generated"
else
    echo "❌ Content calendar not found"
    exit 1
fi

# Test automation
echo "4. Testing automation..."
python3 /Users/cubiczan/.openclaw/workspace/scripts/pinchtab_social_media.py

echo ""
echo "🎉 QUICK START COMPLETE!"
echo "========================================"
echo "Next steps:"
echo "1. Review generated content calendar"
echo "2. Configure Pinchtab profiles if needed"
echo "3. Schedule automation with cron"
echo "4. Monitor performance daily"
echo ""
echo "For detailed setup, see: SOCIAL_MEDIA_SETUP_GUIDE.md"
"""

    quick_start_file = "/Users/cubiczan/.openclaw/workspace/start_social_media.sh"
    with open(quick_start_file, 'w') as f:
        f.write(quick_start)
    
    # Make executable
    os.chmod(quick_start_file, 0o755)
    
    print(f"✅ Quick start script saved to: {quick_start_file}")
    print(f"✅ Make executable: chmod +x {quick_start_file}")
    
    return guide_file, quick_start_file

if __name__ == "__main__":
    guide_file, quick_start_file = create_setup_guide()
    
    print("\n🎯 SETUP COMPLETE!")
    print("=" * 60)
    print("📁 Generated files:")
    print(f"   • Setup Guide: {guide_file}")
    print(f"   • Quick Start: {quick_start_file}")
    print("")
    print("🚀 To get started:")
    print(f"   1. Review: {guide_file}")
    print(f"   2. Run: ./{os.path.basename(quick_start_file)}")
    print("   3. Configure Pinchtab profiles")
    print("   4. Schedule automation")
    print("")
    print("🤖 System leverages:")
    print("   • Agency-Agents framework for expert strategies")
    print("   • Pinchtab for cost-effective browser automation")
    print("   • Dual LinkedIn strategy for maximum impact")
    print("")
    print("✅ Ready for deployment!")