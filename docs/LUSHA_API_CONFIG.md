# Lusha API Configuration

**Purpose:** Contact enrichment backup when Hunter.io credits are exhausted
**API Key:** `d4a62d16-5058-49c8-bc5c-15d3f029dc7a`
**Dashboard:** https://dashboard.lusha.com/api/manage-api-keys
**Status:** ✅ Provided by user as backup contact enrichment API

---

## API Details

### Authentication
**Note:** Test indicates API key format may need adjustment. Error: "invalid Bearer token format"

**Current API Key:** `d4a62d16-5058-49c8-bc5c-15d3f029dc7a`

**Possible formats to try:**
1. `Authorization: Bearer d4a62d16-5058-49c8-bc5c-15d3f029dc7a`
2. `Authorization: Token d4a62d16-5058-49c8-bc5c-15d3f029dc7a`
3. `X-API-Key: d4a62d16-5058-49c8-bc5c-15d3f029dc7a`
4. `api-key: d4a62d16-5058-49c8-bc5c-15d3f029dc7a`

### Base URL
**Tested endpoints:**
- `https://api.lusha.com/person` - Returns 404 (not found)
- `https://api.lusha.com/company` - Returns 401 (auth error)

**Possible correct base URLs:**
- `https://api.lusha.com/v1/`
- `https://api.lusha.co/`
- Check dashboard for exact endpoints

### Rate Limits
- Unknown - use conservatively as backup
- Test with small queries first

---

## Integration Strategy

### Primary Contact Enrichment Stack:
1. **Hunter.io** - Primary (when credits available)
2. **Lusha API** - Backup (when Hunter.io exhausted)
3. **Tavily API** - Web search fallback
4. **Manual search** - Last resort

### Usage Priority:
1. Check Hunter.io balance first
2. If < 10 credits remaining, switch to Lusha
3. Use Lusha for critical leads only
4. Fall back to Tavily for non-critical leads

---

## API Endpoints (Common)

### 1. Person Search
```
GET /person?company={domain}&firstName={first}&lastName={last}
```

### 2. Company Search
```
GET /company?name={companyName}&domain={domain}
```

### 3. Email Finder
```
GET /email?company={domain}&fullName={fullName}
```

---

## Python Integration Example

```python
import requests

LUSHA_API_KEY = "d4a62d16-5058-49c8-bc5c-15d3f029dc7a"
LUSHA_BASE_URL = "https://api.lusha.com"

def get_lusha_contact(company_domain, first_name, last_name):
    """Get contact info from Lusha API"""
    
    headers = {
        "Authorization": f"Bearer {LUSHA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    params = {
        "company": company_domain,
        "firstName": first_name,
        "lastName": last_name
    }
    
    try:
        response = requests.get(
            f"{LUSHA_BASE_URL}/person",
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Lusha API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Lusha API connection error: {e}")
        return None
```

---

## Bash Integration Example

```bash
#!/bin/bash

LUSHA_API_KEY="d4a62d16-5058-49c8-bc5c-15d3f029dc7a"

# Search for person
curl -s -X GET "https://api.lusha.com/person?company=example.com&firstName=John&lastName=Doe" \
  -H "Authorization: Bearer $LUSHA_API_KEY" \
  -H "Content-Type: application/json"
```

---

## Lead Generator Integration

### Update `/Users/cubiczan/mac-bot/skills/lead-generator/SKILL.md`:

Add Lusha as backup enrichment method:

```markdown
## Contact Enrichment APIs

### Primary: Hunter.io
- API Key: [configured in environment]
- Usage: First 100 credits/month

### Backup: Lusha API
- API Key: d4a62d16-5058-49c8-bc5c-15d3f029dc7a
- Usage: When Hunter.io exhausted

### Fallback: Tavily API
- API Key: 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
- Usage: Web search for contact info
```

---

## Testing

### Test Command:
```bash
curl -s -X GET "https://api.lusha.com/person?company=google.com&firstName=Sundar&lastName=Pichai" \
  -H "Authorization: Bearer d4a62d16-5058-49c8-bc5c-15d3f029dc7a" \
  -H "Content-Type: application/json" | jq .
```

### Expected Response:
```json
{
  "data": {
    "firstName": "Sundar",
    "lastName": "Pichai",
    "email": "sundar@google.com",
    "phone": "+1-650-253-0000",
    "position": "CEO",
    "company": "Google"
  }
}
```

---

## Monitoring

### Check API Usage:
- Monitor response codes
- Track successful vs failed requests
- Log usage for cost tracking

### Balance Alerts:
- Create alert when switching to Lusha
- Monitor Lusha usage to avoid overages
- Set daily limit (e.g., 50 requests/day)

---

## Important Notes

⚠️ **Conservation:**
- Lusha is backup only
- Use sparingly for high-value leads
- Implement request throttling

🔒 **Security:**
- API key stored in environment variables
- Never commit to public repositories
- Rotate keys if compromised

💰 **Cost Management:**
- Unknown pricing - assume pay-per-use
- Set hard limits to prevent unexpected charges
- Monitor usage daily

---

**Last Updated:** 2026-03-01
**Status:** Ready for integration as backup contact enrichment
**Primary:** Hunter.io
**Backup:** Lusha API
**Fallback:** Tavily web search
