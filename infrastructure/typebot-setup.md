# Typebot Integration Setup

**Dashboard:** https://app.typebot.io
**Status:** 📋 Ready to configure

---

## Create Account

1. Go to: https://app.typebot.io
2. Sign up (free tier: 200 chats/month)
3. Create workspace

---

## Lead Qualification Bot

### Bot Flow

```
[Start]
   ↓
"Hi! I can help you discover potential savings for your business."
   ↓
"What's your company name?" → Save: company_name
   ↓
"How many employees do you have?"
   ├── 1-50 → low_score
   ├── 51-200 → medium_score
   └── 200+ → high_score
   ↓
"What's your biggest expense challenge?"
   ├── Software/SaaS → qualified
   ├── Vendor contracts → qualified
   ├── Telecom → qualified
   └── Not sure → nurture
   ↓
[Condition: high_score OR medium_score + qualified]
   ├── Yes → "Based on your answers, companies like yours save $50K-$200K annually"
   │           ↓
   │         "Want your personalized estimate?"
   │           ↓
   │         Capture: name, email, phone
   │           ↓
   │         "Thanks! You'll hear from us within 24 hours."
   │           ↓
   │         [Webhook to n8n/Supabase]
   │
   └── No → "Thanks! We'll send you some helpful resources."
             ↓
           Capture: email
             ↓
           [Add to nurture sequence]
```

---

## Embed Code

### Website Bubble
```html
<script type="module">
  import Typebot from 'https://cdn.jsdelivr.net/npm/@typebot.io/js@0.3/dist/web.js'
  
  Typebot.initBubble({
    typebot: "expense-reduction-quiz",
    apiHost: "https://app.typebot.io",
    previewMessage: {
      message: "See how much you could save!",
      autoShowDelay: 5000
    },
    theme: {
      button: { backgroundColor: "#0042DA" },
      previewMessage: { backgroundColor: "#0042DA" }
    }
  })
</script>
```

### Inline Embed
```html
<typebot-standard
  style="width: 100%; height: 600px;"
  typebot="expense-reduction-quiz"
  api-host="https://app.typebot.io"
></typebot-standard>
<script>
  import '@typebot.io/js/web'
</script>
```

---

## Webhook Integration

### Configure Webhook Block
```
URL: https://your-n8n.com/webhook/typebot-lead
Method: POST
Body:
{
  "company": "{{company_name}}",
  "employees": "{{employee_count}}",
  "challenge": "{{challenge}}",
  "name": "{{contact_name}}",
  "email": "{{email}}",
  "phone": "{{phone}}",
  "score": "{{qualification_score}}",
  "source": "typebot"
}
```

---

## Connect to Supabase

### After webhook hits n8n:
1. Process lead data
2. Calculate savings estimate
3. Insert to Supabase
4. Trigger AgentMail
5. Notify Discord

---

## Typebot Settings

| Setting | Value |
|---------|-------|
| Bot ID | Create in dashboard |
| Workspace | Your workspace |
| Plan | Free (200 chats/month) |

---

*Typebot conversational lead capture setup*
