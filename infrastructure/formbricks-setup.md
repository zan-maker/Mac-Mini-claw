# Formbricks Integration

**Environment ID:** `cmlolpn609uahre01dm4yoqxe`
**SDK URL:** `https://app.formbricks.com`
**Dashboard:** https://app.formbricks.com

---

## Embed Code

### Website Integration
```html
<script src="https://cdn.formbricks.com/formbricks.umd.js"></script>
<script>
  window.formbricks.init({
    environmentId: "cmlolpn609uahre01dm4yoqxe",
    apiHost: "https://app.formbricks.com"
  });
</script>
```

### React/Next.js
```bash
npm install @formbricks/js
```

```javascript
import formbricks from '@formbricks/js';

formbricks.init({
  environmentId: "cmlolpn609uahre01dm4yoqxe",
  apiHost: "https://app.formbricks.com"
});

// Track events
formbricks.track("lead_captured");

// Set user attributes
formbricks.setUserId("user-123");
formbricks.setAttribute("company", "Acme Corp");
```

---

## Webhook Integration

### n8n Webhook URL
```
POST https://your-n8n.com/webhook/formbricks-lead
```

### Webhook Payload
```json
{
  "event": "responseCreated",
  "data": {
    "responseId": "resp_xxx",
    "surveyId": "survey_xxx",
    "createdAt": "2026-02-16T00:00:00Z",
    "data": {
      "company_name": "Acme Corp",
      "email": "cfo@acme.com",
      "employee_count": 150
    }
  }
}
```

---

## Lead Capture Form Setup

### Recommended Questions

1. **Company Name** (text, required)
2. **Your Name** (text, required)
3. **Work Email** (email, required)
4. **Phone** (phone, optional)
5. **Employee Count** (number, required)
6. **Industry** (dropdown)
7. **Biggest Challenge** (textarea)

### Form Endings

- **Qualified Lead:** "Thanks! You could save $50K-$200K annually. Schedule your analysis."
- **Nurture:** "Thanks! We'll send you helpful resources."

---

## API Integration

```javascript
// Fetch responses via API
const response = await fetch(
  'https://app.formbricks.com/api/v1/responses?environmentId=cmlolpn609uahre01dm4yoqxe',
  {
    headers: {
      'Authorization': 'Bearer YOUR_API_KEY'
    }
  }
);
```

---

## Workflow

```
[Formbricks Form]
       ↓
[Webhook to n8n]
       ↓
[Calculate Savings]
       ↓
[Save to Supabase]
       ↓
[Send AgentMail]
       ↓
[Discord Notification]
```

---

*Formbricks lead capture integration*
