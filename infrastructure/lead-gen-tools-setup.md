# Lead Generation Infrastructure Setup

## Tools to Set Up

| Tool | Type | Purpose |
|------|------|---------|
| Formbricks | Form Builder | Lead capture forms |
| Typebot | Chatbot | Conversational lead magnets |
| Supabase | Database | Lead data storage |

---

## 1. Formbricks

**URL:** https://formbricks.com
**GitHub:** https://github.com/formbricks/formbricks
**License:** AGPL-3.0 (open source)

### Docker Installation (when Docker available)
```bash
docker run -d \
  --name formbricks \
  -p 3000:3000 \
  -e NEXTAUTH_URL=http://localhost:3000 \
  -e DATABASE_URL=postgresql://... \
  formbricks/formbricks
```

### Cloud Alternative
- Free tier: https://app.formbricks.com
- Unlimited forms, 1000 responses/month free

### Use Cases
- Lead capture forms
- NPS surveys
- Customer feedback
- Qualification quizzes

---

## 2. Typebot

**URL:** https://typebot.io
**GitHub:** https://github.com/baptisteArno/typebot.io
**License:** AGPL-3.0 (open source)

### Docker Installation (when Docker available)
```bash
git clone https://github.com/baptisteArno/typebot.io.git
cd typebot.io
docker-compose up -d
```

### Cloud Alternative
- Free tier: https://app.typebot.io
- Unlimited bots, 200 chats/month free

### Use Cases
- Conversational lead magnets
- Quiz funnels
- WhatsApp bots
- Website chat widgets

---

## 3. Supabase

**URL:** https://supabase.com
**GitHub:** https://github.com/supabase/supabase
**License:** Apache-2.0 (open source)

### Cloud Setup (Recommended)
1. Go to: https://supabase.com
2. Sign up for free
3. Create new project
4. Get API credentials:
   - Project URL
   - Anon/Public Key
   - Service Role Key

### Free Tier
- 500MB database
- 1GB file storage
- 50,000 monthly active users
- Real-time subscriptions

### Use Cases
- Store lead data
- Track interactions
- Real-time updates
- Authentication

---

## Integration Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Formbricks │────►│   n8n      │────►│  Supabase  │
│  (Forms)    │     │ (Workflow) │     │  (Storage) │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Typebot   │────►│  AgentMail │────►│   CRM      │
│  (Chatbot)  │     │  (Outreach)│     │  (Deals)   │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## Quick Setup (Cloud)

### Step 1: Supabase
1. Create account: https://supabase.com
2. Create project: "lead-generation"
3. Save credentials:
   - PROJECT_URL
   - ANON_KEY

### Step 2: Formbricks
1. Create account: https://app.formbricks.com
2. Create form: "Lead Capture"
3. Add webhook to n8n

### Step 3: Typebot
1. Create account: https://app.typebot.io
2. Create bot: "Expense Reduction Quiz"
3. Connect to Supabase

---

## Next Steps

1. [ ] Create Supabase account and project
2. [ ] Create Formbricks account and form
3. [ ] Create Typebot account and bot
4. [ ] Connect all via n8n webhooks

---

*Infrastructure for lead capture and storage*
