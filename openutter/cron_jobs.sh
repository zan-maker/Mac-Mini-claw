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
