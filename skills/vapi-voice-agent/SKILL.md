---
name: vapi-voice-agent
description: "Voice AI agent using Vapi for inbound/outbound calls. Free US phone number for lead qualification, appointment scheduling, and customer service. Use for: (1) voice lead capture, (2) automated follow-up calls, (3) appointment reminders, (4) lead qualification via phone."
---

# Vapi Voice Agent Integration

AI-powered voice agent for lead generation and customer engagement.

## Phone Numbers

**Phone 1:** +1 (572) 300 6475
**Phone 2:** +1 (575) 232 9474
**Private API Key:** `24455236-8179-4d7b-802a-876aa44d4677`
**Public API Key:** `be077154-0347-4c8e-a668-36bee62039ca`
**Dashboard:** https://dashboard.vapi.ai/
**Status:** ✅ Connected

## Assistants

| Name | ID | Purpose |
|------|----|----|
| Lead Qualification Agent | `3f5b4b81-9975-4f29-958b-cadd7694deca` | Expense reduction leads |
| Riley | `91153052-2d5e-4c6a-aa29-8b78ffb5b882` | Appointment scheduling |

---

## Vapi API Integration

### Base URL
```
https://api.vapi.ai
```

### Authentication
```
Authorization: Bearer 07867d73-85a2-475c-b7c1-02f2879a4916
```

---

## Use Cases

### 1. Inbound Lead Capture
- Customer calls +1 (572) 300 6475
- AI qualifies lead with questions
- Captures name, email, company, needs
- Sends summary to AgentMail

### 2. Outbound Follow-up
- Trigger from n8n workflow
- AI calls prospect
- Delivers personalized message
- Captures response/interest level

### 3. Appointment Scheduling
- AI handles scheduling calls
- Confirms appointments
- Sends reminders
- Reduces no-shows

---

## Integration with Lead Systems

### Workflow:
```
Lead captured → Email sent → SMS → Phone call (Vapi)
                                    ↓
                          Qualified → CRM
```

### Webhook Integration:
- Vapi sends call transcripts to n8n
- Lead data extracted and stored
- Follow-up sequences triggered

---

## API Endpoints

### Create Call
```bash
curl -X POST https://api.vapi.ai/call \
  -H "Authorization: Bearer 07867d73-85a2-475c-b7c1-02f2879a4916" \
  -H "Content-Type: application/json" \
  -d '{
    "phoneNumberId": "PHONE_ID",
    "customer": {
      "number": "+1234567890"
    },
    "assistant": {
      "name": "Lead Qualification Agent",
      "model": {
        "provider": "deepseek",
        "model": "deepseek-chat"
      },
      "firstMessage": "Hi, this is an automated call from..."
    }
  }'
```

### Get Call Logs
```bash
curl -X GET https://api.vapi.ai/call \
  -H "Authorization: Bearer 07867d73-85a2-475c-b7c1-02f2879a4916"
```

---

## Lead Qualification Script

```
Assistant: "Hi, this is [Company] following up on your interest 
in expense reduction services. Is now a good time to talk?"

If yes:
  "Great! Quick questions:
   1. How many employees does your company have?
   2. What's your biggest expense challenge right now?
   3. Would you be open to a free analysis?"

Capture responses → Qualify → Schedule meeting
```

---

## Metrics to Track

- Total calls made/received
- Average call duration
- Lead qualification rate
- Appointment conversion rate
- Cost per qualified lead

---

## Safety

- Comply with TCPA regulations
- Honor do-not-call requests
- Business hours only for outbound
- Clear opt-out option
