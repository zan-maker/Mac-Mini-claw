# Qwen3-TTS Setup Status

**API Key:** `sk-115a12c59a00439f96b1313270ac88ee`
**Status:** ⚠️ Invalid API Key

---

## Error Received

```json
{"code":"InvalidApiKey","message":"Invalid API-key provided."}
```

---

## Possible Causes

1. **Key Not Activated:** Need to activate in Alibaba Cloud Console
2. **Wrong Service:** Key might be for different Alibaba Cloud service
3. **Region Issue:** May need to use correct regional endpoint
4. **Subscription Required:** DashScope TTS requires paid subscription

---

## How to Fix

### Step 1: Activate DashScope

1. Go to: https://dashscope.console.aliyun.com/
2. Login with Alibaba Cloud account
3. Enable DashScope service
4. Subscribe to TTS (cosyvoice-v1)

### Step 2: Get Valid API Key

1. In DashScope Console
2. Go to API-KEY Management
3. Create new key
4. Copy the valid key

### Step 3: Test

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/audio/tts" \
  -H "Authorization: Bearer YOUR_VALID_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "cosyvoice-v1",
    "input": {"text": "Hello"},
    "parameters": {"voice": "longshuo_eng"}
  }'
```

---

## Alternative: Use Edge-TTS (Free)

Until Qwen key is activated, use Edge-TTS:

```bash
~/.openclaw/venvs/chatterbox/bin/edge-tts \
  --text "Your message here" \
  --voice en-US-JennyNeural \
  --write-media output.mp3
```

---

## Voice Quality Comparison

| Feature | Edge-TTS | Qwen3-TTS |
|---------|----------|-----------|
| Cost | FREE | Paid |
| Quality | 8/10 | 9/10 |
| Speed | Fast | Medium |
| Languages | 100+ | Chinese/English |
| Emotional | Limited | Advanced |
| Status | ✅ Working | ⚠️ Key invalid |

---

*Qwen3-TTS setup status - 2026-02-16*
