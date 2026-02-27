# Gmail Rotation System for Cron Jobs

## Overview
Dual Gmail account rotation system to avoid rate limits and ensure "no pending emails daily".

## Accounts

### Primary Account
- **Email:** `zan@impactquadrant.info`
- **App Password:** `apbj bvsl tngo vqhu`
- **Daily Limit:** 50 emails
- **Name:** Zane

### Secondary Account  
- **Email:** `sam@impactquadrant.info`
- **App Password:** `ajup xyhf abbx iugj`
- **Daily Limit:** 50 emails
- **Name:** Sam

### Standard CC
- `sam@impactquadrant.info`

## Rotation Logic

### Simple Rotation
```python
# Basic rotation between 2 accounts
accounts = [account1, account2]
current_idx = 0

for email in emails_to_send:
    account = accounts[current_idx]
    send_email(account, email)
    current_idx = (current_idx + 1) % 2
    time.sleep(5)  # 5-second delay
```

### Smart Rotation (Recommended)
1. Track daily sent counts per account
2. Rotate when account reaches 40 emails (80% of limit)
3. Automatic failover if account fails
4. Daily reset at midnight

## Campaign Status

### ✅ COMPLETE TODAY (2026-02-26)

**Dorada Resort:**
- Wave 3: 3/3 sent ✅
- Wave 5: 1/11 sent (Manu Gupta) ✅

**Miami Hotels:**
- Wave 2: 4/4 sent ✅
- Wave 3: 4/4 sent ✅

### ⏳ PENDING (For Cron Jobs)

**Dorada Resort:**
- Wave 4: 7 contacts (16-22)
- Wave 5: 10 contacts (24-33, minus Manu Gupta)
- Wave 6: 8 contacts (35-42, minus John Catsimatidis)

**Total pending:** 25 emails

## Cron Job Updates Needed

### 1. Dorada Campaign Jobs
Update all 6 wave jobs to:
- Use Gmail rotation system
- Include 5-second delays between emails
- Track sent counts
- Update campaign tracking file

### 2. Miami Campaign Jobs  
Update all 3 wave jobs to:
- Use Gmail rotation
- Mark as complete (all waves sent)
- Or pause until new campaign

### 3. Daily Outreach Jobs
- Lead Outreach (2 PM)
- Expense Reduction (2 PM)
- Defense Sector (2 PM)

All should use Gmail rotation.

## Implementation Files

### Core Rotation Module
`/Users/cubiczan/.openclaw/workspace/scripts/gmail_rotation.py`

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import json
import os
from datetime import datetime

class GmailRotator:
    def __init__(self):
        self.accounts = [
            {"email": "zan@impactquadrant.info", "password": "apbj bvsl tngo vqhu", "name": "Zane"},
            {"email": "sam@impactquadrant.info", "password": "ajup xyhf abbx iugj", "name": "Sam"}
        ]
        self.state_file = "/Users/cubiczan/.openclaw/workspace/gmail-rotation-state.json"
        self.cc_email = "sam@impactquadrant.info"
    
    def send_with_rotation(self, to_email, to_name, subject, body):
        # Implementation with rotation logic
        pass
```

### Campaign Script Updates
Each campaign script should:
1. Import `GmailRotator`
2. Use `send_with_rotation()` instead of direct SMTP
3. Update campaign tracking file after sending
4. Include proper error handling

## Daily Workflow

### Morning (9-11 AM)
1. Lead generation cron jobs run
2. New leads added to database

### Afternoon (2 PM)
1. Outreach cron jobs run with Gmail rotation
2. Emails sent with 5-second delays
3. Campaign tracking updated
4. Results logged

### Evening
1. Daily summary generated
2. Rotation state saved
3. Campaign progress checked

## Monitoring

### Success Metrics
- **Delivery Rate:** >95%
- **Open Rate:** Track via tracking pixels
- **Reply Rate:** Monitor responses
- **Daily Completion:** 100% of scheduled emails sent

### Rate Limit Prevention
- Max 40 emails per account per day (80% of limit)
- 5-second minimum delay between emails
- Automatic failover to backup account
- Daily reset of counters

## Next Steps

1. **Immediate:** Update Dorada cron jobs with rotation
2. **Today:** Send pending Dorada emails via rotation
3. **Ongoing:** Monitor delivery and adjust delays
4. **Future:** Add email tracking and analytics

## Files to Create/Update

1. `gmail_rotation.py` - Core rotation module
2. `update_all_cron_scripts.py` - Update campaign scripts
3. `send_todays_pending.py` - Send today's pending emails
4. `campaign_tracker.py` - Update campaign tracking files

## Goal: Zero Pending Daily
With proper rotation and scheduling, all scheduled emails should be sent daily with no backlog.
