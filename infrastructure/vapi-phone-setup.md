# Vapi.ai - Free Phone Number Setup

**Source:** https://vapi.ai/blog/free-telephony-with-vapi

## What You Get

- **Free US phone number** (up to 10 per account)
- **Make and receive calls** at no cost
- **Voice AI integration** for automated agents
- US area codes only

---

## Setup Steps

1. **Sign up at:** https://dashboard.vapi.ai/
2. **Go to:** Phone Numbers tab
3. **Click:** "Create a Phone Number"
4. **Select:** "Free Vapi Number" tab
5. **Enter:** US area code you want
6. **Get:** Random phone number assigned

---

## Use Cases for Lead Generation

### 1. Inbound Lead Line
- Add phone number to email signatures
- Capture voice leads 24/7
- Auto-transcribe calls to text
- Route to CRM

### 2. Voice AI Agent
- Qualify leads via phone
- Answer FAQs
- Schedule appointments
- Transfer to human when needed

### 3. Follow-up Calls
- Automated follow-up sequences
- Voice message drops
- Appointment reminders

---

## Integration with Lead Systems

### Workflow:
```
Lead captured → Email sent → SMS follow-up → Phone call (Vapi)
```

### n8n Integration:
- Vapi webhook triggers on new call
- Lead data extracted
- Added to Supabase
- Follow-up sequence triggered

---

## Vapi Features

| Feature | Description |
|---------|-------------|
| TTS | Text-to-speech |
| STT | Speech-to-text |
| LLM | AI conversation |
| Tools | Custom integrations |
| Squads | Multiple agents |

---

## API Integration

```bash
# Create assistant via API
curl -X POST https://api.vapi.ai/assistant \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Lead Qualification Agent",
    "model": {
      "provider": "deepseek",
      "model": "deepseek-chat"
    }
  }'
```

---

## Cost

- **Free tier:** 10 US numbers, free calls
- **Paid:** Non-US numbers, additional features
- **Pay-as-you-go:** Beyond free limits

---

*Add to lead generation system for voice channel*
