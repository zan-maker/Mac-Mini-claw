# Standard Email Signature for All Outreach

## Signature Format

**For all email templates, use this exact signature:**

```
Best regards,

[Your Name]
Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.
```

## Implementation

### 1. Dorada Resort Outreach
**File:** `/Users/cubiczan/.openclaw/workspace/deals/dorada-outreach-campaign.md`
**Update:** All email templates to use the new signature

### 2. Miami Hotels Outreach  
**File:** `/Users/cubiczan/.openclaw/workspace/deals/miami-hotels-outreach-campaign.md`
**Update:** All email templates to use the new signature

### 3. AgentMail Integration Scripts
**Files:**
- `/workspace/scripts/agentmail-integration.py`
- `/workspace/scripts/expense-reduction-agentmail.py`
- `/workspace/scripts/send-remaining-leads.sh`

**Update:** Add signature to all email body generation functions

### 4. Lead Generator Skill
**File:** `/Users/cubiczan/mac-bot/skills/lead-generator/SKILL.md`
**Update:** Email templates section

## Example Updated Email Template

**Before:**
```
Would you be open to a brief call to discuss the opportunity? I'd be happy to share the full investor deck.

Best regards,

[Your Name]
```

**After:**
```
Would you be open to a brief call to discuss the opportunity? I'd be happy to share the full investor deck.

Best regards,

[Your Name]
Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.
```

## Cron Jobs Affected

All outreach cron jobs will automatically use the updated templates when they read the campaign files.

## Effective Date
2026-02-19 - All new emails will include the standardized signature.
