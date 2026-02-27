# Miami Hotels Cron Job Fix

## Problem
Cron jobs are timing out because:
1. Agent doesn't have direct email sending capabilities
2. Instructions don't specify HOW to send emails
3. Timeouts are too short (180-600 seconds)

## Solution
Update cron job instructions to use AgentMail API with clear steps.

## Fixed Instructions for Wave 1

Replace the current `payload.message` with:

```
Execute buyer outreach for Miami Hotels deal using AgentMail API.

## Task
Send personalized outreach emails to Wave 1 buyers for Miami Hotels portfolio.

## Step-by-Step Instructions

1. **Read campaign files:**
   - Read `/Users/cubiczan/.openclaw/workspace/deals/miami-hotels-outreach-campaign.md` for email templates
   - Read `/Users/cubiczan/.openclaw/workspace/deals/miami-hotels-portfolio.md` for deal details

2. **Prepare emails for Wave 1 contacts:**
   - Jihad Hazzan (ALFAHIM): jihad.hazzan@alfahim.com - Use Template 1 (Tides South Beach)
   - David Stein (Long Wharf Capital): david.stein@longwharf.com - Use Template 2 (Thesis Hotel)
   - Tim Swanson (Marsh McLennan): tim.swanson@marshmma.com - Use Template 2 (Thesis Hotel)
   - Jon Flood (Roseview): jon.flood@madisonmarquette.com - Use Template 3 (Both assets)

3. **Send emails via AgentMail API:**
   Use this curl command for each contact (replace [EMAIL], [SUBJECT], [BODY]):
   ```bash
   curl -s -X POST "https://api.agentmail.to/v1/emails" \
     -H "Authorization: Bearer am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f" \
     -H "Content-Type: application/json" \
     -d '{
       "from": "Zane@agentmail.to",
       "to": ["[EMAIL]"],
       "cc": ["sam@impactquadrant.info"],
       "subject": "[SUBJECT]",
       "body": "[BODY]"
     }'
   ```

4. **Update tracking:**
   - Update `/Users/cubiczan/.openclaw/workspace/deals/miami-hotels-send-log.md` with send status
   - Log activity to `/Users/cubiczan/.openclaw/workspace/memory/YYYY-MM-DD.md`

5. **Signature:**
   All emails must include:
   ```
   Best regards,

   [Your Name]
   Agent Manager

   Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.
   ```

## Important Notes
- Send ONE email per day (rotate through the list)
- Use professional tone
- Include specific deal highlights
- Request OM or call
- **Always include Sam Desigan signature**

If all 4 contacts have been emailed, reply with MIAMI_WAVE_1_COMPLETE.
```

## Additional Fixes Needed

1. **Increase timeout:** Change `timeoutSeconds` from 600 to 1200 (20 minutes)
2. **Update Waves 2 & 3:** Apply same fix with their respective contact lists
3. **Verify AgentMail API:** Test with a single email first

## Testing

Before updating cron jobs, test with a single email:

```bash
# Test email to yourself
curl -s -X POST "https://api.agentmail.to/v1/emails" \
  -H "Authorization: Bearer am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "Zane@agentmail.to",
    "to": ["your-email@example.com"],
    "cc": ["sam@impactquadrant.info"],
    "subject": "Test - Miami Hotels Cron Job Fix",
    "body": "This is a test email to verify the Miami Hotels cron job fix is working.\n\nBest regards,\n\nZane\nAgent Manager\n\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."
  }'
```

## Files to Update

1. **Cron job configuration:** Update payload.message for all 3 waves
2. **Timeout settings:** Increase to 1200 seconds
3. **Campaign file:** Already updated with correct signature

## Alternative: Use Existing Scripts

If AgentMail API doesn't work, use the existing scripts:
- `scripts/send-miami-email-fixed.py` (updated to use AgentMail)
- `scripts/miami-hotels-wave1-timswanson.py`

Update instructions to:
```
3. **Send emails using script:**
   ```bash
   cat email-body.txt | python3 /Users/cubiczan/.openclaw/workspace/scripts/send-miami-email-fixed.py "jihad.hazzan@alfahim.com" "Trophy oceanfront asset - Miami Beach"
   ```
```
