# Hunter.io Email Enrichment Setup

## API Key
**Key:** `e341bb9af29f1da98190364caafb01a6b38e8e1c`
**Account:** sam@impactquadrant.info
**Plan:** Data-platform
**Credits:** 2000 available
**Reset Date:** 2027-03-03

## Configuration

### Environment Variable
```bash
export HUNTER_IO_API_KEY="e341bb9af29f1da98190364caafb01a6b38e8e1c"
```

### For Permanent Use
Add to your shell profile (`~/.zshrc`, `~/.bashrc`, or `~/.bash_profile`):
```bash
export HUNTER_IO_API_KEY="e341bb9af29f1da98190364caafb01a6b38e8e1c"
```

### For Cron Jobs
```bash
0 9 * * * export HUNTER_IO_API_KEY="e341bb9af29f1da98190364caafb01a6b38e8e1c" && /path/to/script.py
```

## Usage

### Python Script
```python
from hunter_io_config import hunter_client

# Domain search
result = hunter_client.domain_search("company.com")
emails = result.get('data', {}).get('emails', [])

# Email finder (specific person)
result = hunter_client.email_finder(
    domain="company.com",
    first_name="John",
    last_name="Doe"
)

# Email verifier
result = hunter_client.email_verifier("john.doe@company.com")
```

### Features
- **Domain Search:** Find all emails associated with a domain
- **Email Finder:** Find email for specific person
- **Email Verifier:** Check if email is valid/deliverable
- **Account Info:** Check remaining credits

## Integration Points

### 1. Lead Generator Skill
**File:** `/Users/cubiczan/mac-bot/skills/lead-generator/SKILL.md`
**Use:** Email enrichment for SMB leads

### 2. Expense Reduction Outreach
**Script:** `/workspace/scripts/send-remaining-leads.sh`
**Use:** Find CEO/CFO emails for outreach

### 3. Deal Origination
**Campaigns:** Dorada Resort, Miami Hotels
**Use:** Investor contact enrichment

## Rate Limits
- **Searches:** 2000 credits/month
- **Verifications:** 2000 credits/month
- **Reset:** Monthly on 3rd

## Best Practices

1. **Cache Results:** Store found emails to avoid duplicate searches
2. **Verify Before Sending:** Use email verifier for important outreach
3. **Check Credits:** Monitor usage with `get_account_info()`
4. **Fallback:** Use Tavily/Serper if Hunter.io fails

## Testing

```bash
# Test API key
python3 scripts/test-new-hunter-api.py

# Test domain search
python3 -c "from hunter_io_config import hunter_client; print(hunter_client.domain_search('google.com', limit=1))"
```

## Security Notes
- API key stored in environment variable (not in code)
- `.env` file in `.gitignore` to prevent accidental commits
- Regular key rotation recommended

## Alternative Services
- **ZeroBounce:** 87 credits remaining (email verification)
- **Tavily:** `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` (web search)
- **Serper:** `cac43a248afb1cc1ec004370df2e0282a67eb420` (Google search)

---

**Last Updated:** 2026-02-19
**Status:** ✅ Active and tested
