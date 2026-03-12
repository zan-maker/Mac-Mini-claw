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
