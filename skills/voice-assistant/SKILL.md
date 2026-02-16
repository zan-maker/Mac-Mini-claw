---
name: voice-assistant
description: "Unified voice assistant using Qwen3-TTS or Edge-TTS. Generates voice messages for lead generation, follow-ups, and announcements. Use for: (1) lead script voice generation, (2) phone call audio, (3) voice messages, (4) announcement narration."
---

# Voice Assistant - Qwen3-TTS + Edge-TTS

Unified voice generation for lead generation and outreach.

---

## APIs

### Qwen3-TTS (Primary - Premium Quality)
- **API Key:** `sk-115a12c59a00439f96b1313270ac88ee`
- **Base URL:** `https://dashscope.aliyuncs.com/api/v1`
- **Model:** `cosyvoice-v1`
- **Status:** ⚠️ Key needs activation in Alibaba Cloud Console

### Edge-TTS (Fallback - Free)
- **Location:** `~/.openclaw/venvs/chatterbox/bin/edge-tts`
- **Status:** ✅ Working
- **Cost:** Free

---

## Usage

### Option 1: Edge-TTS (Recommended - Free)

```bash
~/.openclaw/venvs/chatterbox/bin/edge-tts \
  --text "Hello from the lead generation team." \
  --voice en-US-JennyNeural \
  --write-media /tmp/output.mp3
```

### Available Edge-TTS Voices

**English:**
- `en-US-JennyNeural` - Female, friendly
- `en-US-GuyNeural` - Male, professional
- `en-GB-SoniaNeural` - British female
- `en-AU-NatashaNeural` - Australian female

**For lead generation, recommended:**
- Female: `en-US-JennyNeural`
- Male: `en-US-GuyNeural`

---

### Option 2: Qwen3-TTS (Premium)

**Setup:**
1. Go to: https://dashscope.console.aliyun.com/
2. Activate DashScope service
3. Verify API key is valid
4. Subscribe to TTS service

**Usage:**
```python
from qwen_tts_integration import generate_speech

result = generate_speech(
    text="Hello, this is a follow-up call.",
    output_path="/tmp/output.wav",
    voice="longshuo_eng"
)
```

**Qwen Voices:**
- `longshuo_eng` - Male, English
- `longxiaochun_eng` - Female, English

---

## Integration with Lead Generation

### Generate Lead Script

```python
# Using Edge-TTS (free)
import subprocess

def generate_lead_voice(company_name, contact_name, savings, output_path):
    text = f"""
    Hi {contact_name}, this is a follow-up from the expense reduction team.
    {company_name} could save {savings} annually.
    Would you be open to a 15-minute call?
    """
    
    cmd = [
        "~/.openclaw/venvs/chatterbox/bin/edge-tts",
        "--text", text,
        "--voice", "en-US-JennyNeural",
        "--write-media", output_path
    ]
    
    subprocess.run(cmd, shell=True)
    return output_path
```

### For Vapi Phone Calls

Generate audio for Vapi to play:

```python
# Generate greeting audio
edge_tts --text "Hi, thanks for your interest in expense reduction." \
  --voice en-US-JennyNeural \
  --write-media greeting.mp3

# Upload to public URL
# Use in Vapi assistant configuration
```

---

## Scripts Available

| Script | Purpose |
|--------|---------|
| `/scripts/qwen-tts-integration.py` | Qwen3-TTS API |
| `/scripts/edge-tts-integration.py` | Edge-TTS wrapper |

---

## Recommended Flow

1. **Use Edge-TTS** for all voice generation (free, reliable)
2. **Use Qwen3-TTS** for premium quality if needed (requires activation)
3. **For Vapi calls:** Generate audio files and use as prompts

---

## Quick Commands

```bash
# Generate lead script
~/.openclaw/venvs/chatterbox/bin/edge-tts \
  --text "Hi, I'm calling about your interest in expense reduction." \
  --voice en-US-JennyNeural \
  --write-media lead-greeting.mp3

# List all voices
~/.openclaw/venvs/chatterbox/bin/edge-tts --list-voices

# Test Python integration
python3 ~/.openclaw/workspace/scripts/edge-tts-integration.py
```

---

*Voice assistant integration - Qwen3-TTS + Edge-TTS*
