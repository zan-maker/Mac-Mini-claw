# Complete Lead Generation Stack - Setup Guide

## ✅ Tools Installed & Configured

| Tool | Status | Details |
|------|--------|---------|
| n8n | ✅ v2.7.5 | Workflow automation |
| Ollama | ✅ v0.15.6 | Local LLM |
| Vapi | ✅ Connected | 2 phone lines |
| Edge-TTS | ✅ Working | Free TTS |
| fpdf2 | ✅ Working | PDF generation |
| Supabase CLI | ✅ v2.75.0 | Database |
| Formbricks | ✅ Ready | Forms |

---

## 📋 Remaining Setup Tasks

### 1. Create Supabase Leads Table

Go to: https://supabase.com/dashboard → SQL Editor

Run:
```sql
CREATE TABLE leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  company_name TEXT,
  contact_name TEXT,
  email TEXT,
  phone TEXT,
  employee_count INTEGER,
  industry TEXT,
  challenge TEXT,
  source TEXT DEFAULT 'unknown',
  qualification_score INTEGER DEFAULT 0,
  status TEXT DEFAULT 'new',
  estimated_savings INTEGER
);

ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON leads FOR ALL USING (true);
```

### 2. Create Formbricks Form

1. Go to: https://app.formbricks.com
2. Create survey/form
3. Add questions:
   - Company Name (text)
   - Email (email)
   - Employee Count (number)
   - Challenge (textarea)
4. Add webhook: `http://localhost:5678/webhook/formbricks-lead`

### 3. Create Typebot Bot

1. Go to: https://app.typebot.io
2. Create bot: "Expense Reduction Quiz"
3. Build flow (see typebot-setup.md)
4. Add webhook block to n8n

### 4. Start n8n

```bash
n8n start --port=5678
```

Access at: http://localhost:5678

Import workflow: `/workspace/n8n-workflows/lead-capture-workflow.json`

---

## 🚀 Full Integration Architecture

```
┌─────────────┐
│ Formbricks  │──────┐
│  (Forms)    │      │
└─────────────┘      │
                     ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Typebot   │──►│    n8n     │──►│  Supabase  │
│  (Chatbot)  │  │ (Workflow)  │  │ (Database) │
└─────────────┘  └─────────────┘  └─────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ AgentMail   │ │   Discord   │ │    Vapi    │
│  (Email)    │ │ (Notify)    │ │  (Voice)   │
└─────────────┘ └─────────────┘ └─────────────┘
```

---

## 📞 Vapi Integration

### Phone Numbers
- +1 (572) 300 6475
- +1 (575) 232 9474

### Make Outbound Call
```bash
curl -X POST "https://api.vapi.ai/call" \
  -H "Authorization: Bearer 24455236-8179-4d7b-802a-876aa44d4677" \
  -H "Content-Type: application/json" \
  -d '{
    "assistantId": "3f5b4b81-9975-4f29-958b-cadd7694deca",
    "phoneNumberId": "07867d73-85a2-475c-b7c1-02f2879a4916",
    "customer": {"number": "+1XXXXXXXXXX"}
  }'
```

---

## 🎵 Edge-TTS

```bash
~/.openclaw/venvs/chatterbox/bin/edge-tts \
  --text "Hello from the team" \
  --voice en-US-JennyNeural \
  --write-media output.mp3
```

---

## 📊 Lead Scoring

| Score | Status | Action |
|-------|--------|--------|
| 70-100 | Hot Lead | Call within 1 hour |
| 50-69 | Warm Lead | Email within 24 hours |
| 30-49 | Nurture | Add to sequence |
| 0-29 | Cold | Monthly newsletter |

---

## 🔄 Daily Automation

Cron jobs running:
- 9 AM: Lead generation
- 2 PM: Email outreach
- 1 AM: Nightly meditation

---

*Complete lead generation infrastructure*
