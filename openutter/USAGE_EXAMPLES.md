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
