---
name: lead-capture-forms
description: "Formbricks and Typebot integration for lead capture. Open-source form builder and conversational chatbots. Use for: (1) lead capture forms, (2) quiz funnels, (3) NPS surveys, (4) conversational lead magnets."
---

# Lead Capture Forms - Formbricks & Typebot

Open-source form builders for lead generation.

---

## Formbricks

**URL:** https://formbricks.com
**Status:** Open source (AGPL-3.0)

### Features
- Drag-and-drop form builder
- Multi-step forms
- Logic branching
- Webhook integrations
- NPS/CSAT surveys

### Cloud Setup (Free Tier)
1. Go to: https://app.formbricks.com
2. Create account
3. Create environment
4. Build form

### Lead Capture Form Template
```json
{
  "name": "Expense Reduction Lead Capture",
  "questions": [
    {"type": "text", "label": "Company Name", "required": true},
    {"type": "text", "label": "Your Name", "required": true},
    {"type": "email", "label": "Work Email", "required": true},
    {"type": "number", "label": "Employee Count", "required": true},
    {"type": "dropdown", "label": "Industry", "options": ["Technology", "Healthcare", "Manufacturing", "Professional Services", "Other"]},
    {"type": "textarea", "label": "Biggest Expense Challenge"}
  ]
}
```

### Webhook to n8n
```
POST https://your-n8n.com/webhook/formbricks-lead
{
  "responseId": "xxx",
  "data": {"company": "Acme", "email": "cfo@acme.com", ...}
}
```

---

## Typebot

**URL:** https://typebot.io
**Status:** Open source (AGPL-3.0)

### Features
- Visual flow builder
- Conversational UX
- Conditional logic
- Integrations (Zapier, Make, webhooks)
- Embed anywhere

### Cloud Setup (Free Tier)
1. Go to: https://app.typebot.io
2. Create account
3. Create workspace
4. Build bot

### Lead Qualification Bot Template
```
Welcome Block:
"Hi! I'm here to help you discover potential savings for your business."
→ Continue

Question 1 - Company:
"What's your company name?"
→ Save to variable: company_name

Question 2 - Size:
"How many employees do you have?"
→ Buttons: 1-50 | 51-200 | 201-500 | 500+

Question 3 - Challenge:
"What's your biggest expense challenge right now?"
→ Buttons: Software costs | Vendor contracts | Telecom | Not sure

Calculation Block:
"If employees > 50 AND challenge != Not sure"
→ Qualified Lead Path
Else:
→ Nurture Path

Qualified Lead Path:
"Based on your answers, companies like yours typically save $50,000-$200,000 annually."
→ "Want to see your personalized estimate?"
→ Capture: email, phone

End Block:
"Thanks! You'll receive your estimate within 24 hours."
→ Webhook to n8n
```

---

## Supabase Integration

### Database Schema for Leads
```sql
CREATE TABLE leads (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Contact info
  company_name TEXT,
  contact_name TEXT,
  email TEXT,
  phone TEXT,
  
  -- Qualification
  employee_count INTEGER,
  industry TEXT,
  challenge TEXT,
  
  -- Source tracking
  source TEXT, -- 'formbricks', 'typebot', 'email'
  campaign TEXT,
  
  -- Scoring
  qualification_score INTEGER,
  status TEXT DEFAULT 'new', -- new, contacted, qualified, converted
  
  -- Calculated fields
  estimated_savings INTEGER,
  potential_deal_value INTEGER
);

-- Enable realtime
ALTER TABLE leads REPLICA IDENTITY FULL;
ALTER PUBLICATION supabase_realtime ADD TABLE leads;
```

### API Access
```bash
# Insert lead
curl -X POST "https://YOUR_PROJECT.supabase.co/rest/v1/leads" \
  -H "apikey: YOUR_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"company_name":"Acme","email":"cfo@acme.com"}'
```

---

## Integration with n8n

### Workflow: Form → Supabase → AgentMail
```
[Formbricks Webhook] 
       ↓
[Process Lead Data]
       ↓
[Calculate Savings]
       ↓
[Save to Supabase]
       ↓
[Send via AgentMail]
       ↓
[Log to Discord]
```

---

## Embed Codes

### Formbricks
```html
<script src="https://cdn.formbricks.com/formbricks.umd.js"></script>
<script>
  window.formbricks.init({
    environmentId: "YOUR_ENV_ID",
    apiHost: "https://app.formbricks.com"
  });
</script>
```

### Typebot
```html
<script type="module">
  import Typebot from 'https://cdn.jsdelivr.net/npm/@typebot.io/js@0.3/dist/web.js'
  
  Typebot.initBubble({
    typebot: "expense-reduction-quiz",
    apiHost: "https://app.typebot.io",
  })
</script>
```

---

## Setup Checklist

- [ ] Create Formbricks account
- [ ] Create Typebot account
- [ ] Create Supabase project
- [ ] Create database schema
- [ ] Build lead capture form
- [ ] Build qualification bot
- [ ] Set up n8n webhooks
- [ ] Test full flow

---

*Open-source lead capture infrastructure*
