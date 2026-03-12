#!/bin/bash

# OpenUtter Setup Script for Investor Event Monitoring
# Attends online investor events, Zoom/Google Meet calls, and reports back

set -e

echo "========================================="
echo "OPENUTTER SETUP FOR INVESTOR EVENTS"
echo "========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
WORKSPACE_DIR="/Users/cubiczan/.openclaw/workspace"
OPENUTTER_WORKSPACE="$WORKSPACE_DIR/openutter"
LOG_FILE="/tmp/openutter_setup_$(date +%Y%m%d_%H%M%S).log"

# Function to print status
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    echo "🔍 Checking prerequisites..."
    
    # Check Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_status "Node.js: $NODE_VERSION"
    else
        print_error "Node.js not found. Install from: https://nodejs.org/"
        return 1
    fi
    
    # Check npm
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        print_status "npm: $NPM_VERSION"
    else
        print_error "npm not found"
        return 1
    fi
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        print_status "Python: $PYTHON_VERSION"
    else
        print_error "Python3 not found"
        return 1
    fi
    
    return 0
}

# Install OpenUtter
install_openutter() {
    echo ""
    echo "📦 Installing OpenUtter..."
    
    # Install to workspace (not global)
    print_status "Installing OpenUtter to workspace..."
    
    if npx openutter --target-dir "$WORKSPACE_DIR/skills/openutter" 2>> "$LOG_FILE"; then
        print_status "OpenUtter installed successfully"
        return 0
    else
        print_error "OpenUtter installation failed"
        print_warning "Trying alternative installation method..."
        
        # Try alternative
        if npm install -g firecrawl-cli 2>> "$LOG_FILE"; then
            print_status "Installed via alternative method"
            return 0
        else
            print_error "All installation methods failed"
            return 1
        fi
    fi
}

# Install Playwright Chromium
install_playwright() {
    echo ""
    echo "🌐 Installing Playwright Chromium..."
    
    if npx playwright-core install chromium 2>> "$LOG_FILE"; then
        print_status "Playwright Chromium installed"
        return 0
    else
        print_error "Playwright installation failed"
        print_warning "Meeting joins may not work without Chromium"
        return 1
    fi
}

# Create workspace structure
create_workspace() {
    echo ""
    echo "📁 Creating workspace structure..."
    
    # Create directories
    mkdir -p "$OPENUTTER_WORKSPACE"
    mkdir -p "$OPENUTTER_WORKSPACE/transcripts"
    mkdir -p "$OPENUTTER_WORKSPACE/screenshots"
    mkdir -p "$OPENUTTER_WORKSPACE/reports"
    
    print_status "Workspace created: $OPENUTTER_WORKSPACE"
    
    # Create initial events database
    EVENTS_DB="$OPENUTTER_WORKSPACE/investor_events.json"
    if [ ! -f "$EVENTS_DB" ]; then
        cat > "$EVENTS_DB" << 'EOF'
{
  "events": [],
  "updated": "2026-03-11T00:00:00",
  "version": "1.0"
}
EOF
        print_status "Created events database: $EVENTS_DB"
    fi
    
    return 0
}

# Test OpenUtter installation
test_openutter() {
    echo ""
    echo "🧪 Testing OpenUtter installation..."
    
    # Test basic command
    if npx openutter --help 2>> "$LOG_FILE" | grep -q "OpenUtter"; then
        print_status "OpenUtter CLI is working"
        return 0
    else
        print_error "OpenUtter CLI test failed"
        return 1
    fi
}

# Create authentication guide
create_auth_guide() {
    echo ""
    echo "🔑 Authentication Guide"
    echo "======================"
    echo ""
    echo "For reliable meeting joins (not stuck in lobby), authenticate:"
    echo ""
    echo "1. Run: npx openutter auth"
    echo "2. A browser will open"
    echo "3. Sign in to your Google account"
    echo "4. Return to terminal and press Enter"
    echo ""
    echo "This saves your session to: ~/.openutter/auth.json"
    echo ""
    echo "Then join meetings with: npx openutter join <url> --auth"
    echo ""
    
    AUTH_GUIDE="$OPENUTTER_WORKSPACE/AUTHENTICATION.md"
    cat > "$AUTH_GUIDE" << 'EOF'
# OpenUtter Authentication Guide

## Why Authenticate?

Without authentication, OpenUtter joins as a guest and waits in the lobby for host approval. This often fails if:
- Host doesn't notice the guest
- Meeting has guest restrictions
- Host rejects unknown guests

With authentication, OpenUtter joins as your Google account, which is much more reliable.

## Setup Authentication

1. **Run authentication command:**
   ```bash
   npx openutter auth
   ```

2. **Browser opens:** Sign in to your Google account

3. **Return to terminal:** Press Enter when done

## Files Created

- `~/.openutter/auth.json` - Encrypted session
- `~/.openutter/auth-meta.json` - Session metadata
- `~/.openutter/chrome-profile/` - Persistent browser profile

## Joining Meetings

**With authentication (recommended):**
```bash
npx openutter join https://meet.google.com/abc-defg-hij --auth
```

**As guest (less reliable):**
```bash
npx openutter join https://meet.google.com/abc-defg-hij --anon --bot-name "Investor Bot"
```

## Troubleshooting Authentication

### Session Expired
Run `npx openutter auth` again to refresh.

### Authentication Failed
1. Check you're signed into Google in the browser
2. Ensure you have permission to join the meeting
3. Try incognito/private browsing mode

### Browser Doesn't Open
Run with `--headed` flag:
```bash
npx openutter auth --headed
```

## Security Notes

- Session is encrypted and stored locally
- Only used for meeting joins
- Can be deleted anytime: `rm -rf ~/.openutter/`
EOF
    
    print_status "Authentication guide created: $AUTH_GUIDE"
}

# Create usage examples
create_usage_examples() {
    echo ""
    echo "🚀 Usage Examples"
    echo "================"
    
    USAGE_FILE="$OPENUTTER_WORKSPACE/USAGE_EXAMPLES.md"
    cat > "$USAGE_FILE" << 'EOF'
# OpenUtter Usage Examples

## Basic Meeting Join

```bash
# Join as authenticated user (most reliable)
npx openutter join https://meet.google.com/abc-defg-hij --auth

# Join as guest
npx openutter join https://meet.google.com/abc-defg-hij --anon --bot-name "Investor Intelligence"

# Join with browser visible (debugging)
npx openutter join https://meet.google.com/abc-defg-hij --auth --headed
```

## Meeting Management

```bash
# Auto-leave after 30 minutes
npx openutter join https://meet.google.com/abc-defg-hij --auth --duration 30m

# Send updates to OpenClaw channel
npx openutter join https://meet.google.com/abc-defg-hij --auth --channel discord

# Verbose output (see captions in real-time)
npx openutter join https://meet.google.com/abc-defg-hij --auth --verbose
```

## Transcripts & Screenshots

```bash
# Read latest transcript
npx openutter transcript

# Read last 20 lines
npx openutter transcript --last 20

# Take screenshot
npx openutter screenshot

# Transcripts are saved to:
# ~/.openclaw/workspace/openutter/transcripts/<meeting-id>.txt

# Screenshots are saved to:
# ~/.openclaw/workspace/openutter/on-demand-screenshot.png
```

## Investor Event Monitor

Use the Python monitor for automated event attendance:

```bash
# Run the investor event monitor
python3 /Users/cubiczan/.openclaw/workspace/investor_event_monitor.py

# Or run directly
cd /Users/cubiczan/.openclaw/workspace
./investor_event_monitor.py
```

## Common Investor Event Types

### 1. Earnings Calls
```bash
npx openutter join <earnings-call-url> --auth --duration 90m --verbose
# Keywords: revenue, EPS, guidance, growth, outlook
```

### 2. VC Pitch Events
```bash
npx openutter join <pitch-event-url> --auth --duration 120m --verbose
# Keywords: funding, valuation, round, term sheet, due diligence
```

### 3. Industry Webinars
```bash
npx openutter join <webinar-url> --auth --duration 180m --verbose
# Keywords: market, trends, analysis, forecast, opportunity
```

## Integration with OpenClaw

### Send Updates to Discord
```bash
npx openutter join <url> --auth --channel discord --target "#investor-events"
```

### Cron Job for Regular Events
```bash
# Add to crontab for daily earnings calls
0 14 * * 1-5 cd /Users/cubiczan/.openclaw/workspace && python3 investor_event_monitor.py >> ~/openutter.log 2>&1
```

## Troubleshooting

### Meeting Join Fails
1. Check URL is correct
2. Ensure meeting hasn't ended
3. Try `--headed` to see what's happening
4. Check authentication with `npx openutter auth`

### No Captions
1. Host must enable captions
2. Try `--verbose` to see if captions are detected
3. Some meetings don't support captions

### Bot Gets Kicked
1. Use `--auth` instead of `--anon`
2. Join with a recognizable name
3. Some meetings have strict admission

## Advanced: Custom Integration

```python
# Example Python integration
import subprocess
import json

def join_investor_event(url, event_name):
    """Join an investor event and capture transcript"""
    cmd = [
        "npx", "openutter", "join", url,
        "--auth",
        "--duration", "60m",
        "--verbose"
    ]
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Process output in real-time
    for line in process.stdout:
        if ":" in line:  # Caption line
            print(f"[{event_name}] {line.strip()}")
    
    return process
```
EOF
    
    print_status "Usage examples created: $USAGE_FILE"
}

# Create cron job template
create_cron_template() {
    echo ""
    echo "⏰ Cron Job Template"
    echo "==================="
    
    CRON_FILE="$OPENUTTER_WORKSPACE/cron_jobs.sh"
    cat > "$CRON_FILE" << 'EOF'
#!/bin/bash

# OpenUtter Cron Jobs for Investor Events
# Add to crontab: crontab -e

# Daily earnings call monitor (2:00 PM EST)
0 14 * * 1-5 cd /Users/cubiczan/.openclaw/workspace && python3 investor_event_monitor.py >> ~/openutter_daily.log 2>&1

# Weekly VC pitch event scanner (Monday 10:00 AM)
0 10 * * 1 cd /Users/cubiczan/.openclaw/workspace && python3 vc_event_scanner.py >> ~/openutter_vc.log 2>&1

# Monthly mining investor day (1st of month 9:00 AM)
0 9 1 * * cd /Users/cubiczan/.openclaw/workspace && python3 mining_investor_day.py >> ~/openutter_mining.log 2>&1

# Transcript cleanup (weekly, Sunday midnight)
0 0 * * 0 find /Users/cubiczan/.openclaw/workspace/openutter/transcripts -name "*.txt" -mtime +30 -delete

# Report generation (daily, 6:00 PM)
0 18 * * * cd /Users/cubiczan/.openclaw/workspace && python3 generate_daily_report.py >> ~/openutter_reports.log 2>&1
EOF
    
    chmod +x "$CRON_FILE"
    print_status "Cron job template created: $CRON_FILE"
}

# Create quick start guide
create_quick_start() {
    echo ""
    echo "⚡ Quick Start Guide"
    echo "==================="
    
    QUICK_START="$OPENUTTER_WORKSPACE/QUICK_START.md"
    cat > "$QUICK_START" << 'EOF'
# OpenUtter Quick Start

## 1. Test Installation
```bash
npx openutter --help
```

## 2. Authenticate (Recommended)
```bash
npx openutter auth
# Follow browser prompts, then press Enter in terminal
```

## 3. Test with a Meeting
```bash
# Join a test meeting (replace with actual URL)
npx openutter join https://meet.google.com/abc-defg-hij --auth --duration 5m --verbose
```

## 4. Run Investor Event Monitor
```bash
cd /Users/cubiczan/.openclaw/workspace
python3 investor_event_monitor.py
```

## 5. Add Your First Event
Edit the events database:
```bash
nano /Users/cubiczan/.openclaw/workspace/openutter/investor_events.json
```

Add an event (example):
```json
{
  "id": "my_first_event",
  "name": "Tech Startup Demo Day",
  "event_type": "vc_pitch",
  "meet_url": "https://meet.google.com/your-meeting-id",
  "scheduled_time": "2026-03-12T14:00:00",
  "duration_minutes": 120,
  "keywords": ["funding", "startup", "pitch"],
  "priority": 8,
  "auto_join": true,
  "report_channel": "discord"
}
```

## 6. Monitor Automatically
```bash
# Run in background
nohup python3 investor_event_monitor.py > monitor.log 2>&1 &

# Or add to crontab
crontab -e
# Add: 0 * * * * cd /Users/cubiczan/.openclaw/workspace && python3 investor_event_monitor.py >> ~/openutter.log 2>&1
```

## Need Help?

- Check logs: `tail -f ~/openutter.log`
- View transcripts: `ls -la ~/.openclaw/workspace/openutter/transcripts/`
- Debug with browser: Add `--headed` to any command
- Re-authenticate: `npx openutter auth`
EOF
    
    print_status "Quick start guide created: $QUICK_START"
}

# Main execution
main() {
    echo "Starting OpenUtter setup for investor events..."
    echo "Log file: $LOG_FILE"
    
    # Check prerequisites
    check_prerequisites || exit 1
    
    # Install OpenUtter
    install_openutter || { print_warning "OpenUtter installation had issues"; }
    
    # Install Playwright
    install_playwright || { print_warning "Playwright installation had issues"; }
    
    # Create workspace
    create_workspace
    
    # Test installation
    test_openutter || { print_warning "OpenUtter test failed but setup may still work"; }
    
    # Create documentation
    create_auth_guide
    create_usage_examples
    create_cron_template
    create_quick_start
    
    # Final summary
    echo ""
    echo "========================================="
    echo "✅ OPENUTTER SETUP COMPLETE!"
    echo "========================================="
    echo ""
    echo "🎯 What was installed:"
    echo "   1. OpenUtter Google Meet bot"
    echo "   2. Playwright Chromium browser"
    echo "   3. Investor event monitor system"
    echo "   4. Complete documentation"
    echo ""
    echo "📁 Workspace: $OPENUTTER_WORKSPACE"
    echo ""
    echo "🚀 Next steps:"
    echo "   1. Read: $OPENUTTER_WORKSPACE/QUICK_START.md"
    echo "   2. Authenticate: npx openutter auth"
    echo "   3. Test: python3 $WORKSPACE_DIR/investor_event_monitor.py"
    echo "   4. Add your investor events to the database"
    echo ""
    echo "📊 Now you can attend investor events you can't make!"
    echo "   OpenUtter will join, capture transcripts, and report back."
    echo ""
    echo "Happy investing! 🎯"
}

# Run main function
main "$@" 2>&1 | tee -a "$LOG_FILE"