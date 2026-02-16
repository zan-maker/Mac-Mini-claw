---
name: chatterbox-tts
description: "Open-source Text-to-Speech using Chatterbox by Resemble AI. Free alternative to ElevenLabs with zero-shot voice cloning. 23+ languages supported. Use for: (1) voice AI agents, (2) audio content creation, (3) phone call scripts, (4) video narration."
---

# Chatterbox TTS - Open Source Voice AI

State-of-the-art open-source text-to-speech by Resemble AI. Free alternative to ElevenLabs.

## Why Chatterbox?

- **100% Free & Open Source** (MIT License)
- **Zero-shot voice cloning** from 10-second clips
- **23+ languages** supported
- **Paralinguistic tags**: [laugh], [cough], [chuckle]
- **Outperforms ElevenLabs** in blind tests
- **Local processing** - no API calls needed

---

## Model Options

| Model | Size | Best For |
|-------|------|----------|
| **Chatterbox-Turbo** | 350M | Voice agents, production (fastest) |
| **Chatterbox-Multilingual** | 500M | 23+ languages |
| **Chatterbox** | 500M | Creative control |

---

## Installation

```bash
pip install chatterbox-tts
```

Or from source:
```bash
git clone https://github.com/resemble-ai/chatterbox.git
cd chatterbox
pip install -e .
```

**Requirements:**
- Python 3.11
- CUDA-capable GPU (recommended)
- 4GB+ VRAM for Turbo, 8GB+ for full models

---

## Usage

### Basic TTS
```python
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

# Load model
model = ChatterboxTTS.from_pretrained(device="cuda")

# Generate speech
text = "Hello, this is an automated message about your expense reduction analysis."
wav = model.generate(text)

# Save
ta.save("output.wav", wav, model.sr)
```

### Voice Cloning (Zero-shot)
```python
# Clone voice from 10-second reference clip
wav = model.generate(
    text="Hi, I'm calling from your account management team.",
    audio_prompt_path="reference_voice.wav"
)
ta.save("cloned.wav", wav, model.sr)
```

### Turbo with Emotions
```python
from chatterbox.tts_turbo import ChatterboxTurboTTS

model = ChatterboxTurboTTS.from_pretrained(device="cuda")

text = "Hi there! [laugh] I have great news about your savings analysis!"
wav = model.generate(text, audio_prompt_path="reference.wav")
```

---

## Integration with Lead Generation

### Use Cases

1. **Phone Call Scripts**
   - Generate voice for Vapi calls
   - Custom greetings per prospect
   - Follow-up message variations

2. **Video Narration**
   - Lead magnet videos
   - Product explainers
   - Case study narration

3. **Podcast Content**
   - Industry updates
   - Educational content
   - Interview simulations

4. **Voice Agents**
   - Inbound call handling
   - Qualification scripts
   - Appointment confirmations

---

## Supported Languages

Arabic, Chinese, Danish, Dutch, English, Finnish, French, German, Greek, Hebrew, Hindi, Italian, Japanese, Korean, Malay, Norwegian, Polish, Portuguese, Russian, Spanish, Swahili, Swedish, Turkish

---

## Performance

| Metric | Chatterbox Turbo | ElevenLabs |
|--------|------------------|------------|
| Quality | 4.6/5 | 4.5/5 |
| Speed | ~200ms | ~300ms |
| Cost | **FREE** | $5-99/mo |
| Languages | 23+ | 29 |

---

## Paralinguistic Tags

Add natural elements to speech:
- `[laugh]` - Natural laughter
- `[cough]` - Coughing sound
- `[chuckle]` - Light laughter
- `[sigh]` - Breathing sounds

---

## Watermarking

All audio includes Resemble AI's PerTh watermarking for responsible AI usage. Extract with:
```python
import perth
watermarker = perth.PerthImplicitWatermarker()
watermark = watermarker.get_watermark(audio, sample_rate=sr)
```

---

## For Lead Gen Scripts

```python
# Generate outreach voice message
text = """
Hi [Name], this is a quick follow-up on your interest in expense reduction.
[laugh] I know you're busy, so I'll be brief.
Companies your size typically save over $100,000 annually.
Would you be open to a 15-minute call this week?
"""

wav = model.generate(text, audio_prompt_path="professional_voice.wav")
```

---

## ✅ Working Alternative: Edge-TTS

**Free TTS using Microsoft Edge voices** (100+ voices, works on macOS)

### Installation
Already installed in `~/.openclaw/venvs/chatterbox/`

### Usage
```bash
# Generate audio
~/.openclaw/venvs/chatterbox/bin/edge-tts \
  --text "Hello, this is a test." \
  --voice en-US-JennyNeural \
  --write-media output.mp3
```

### Script Integration
```python
# Use edge-tts-integration.py
from edge_tts_integration import generate_audio, generate_lead_script

# Generate lead script
result = generate_lead_script("Acme Corp", "John", "/tmp/lead.mp3")
```

### Available Voices
- `en-US-JennyNeural` - Female, friendly
- `en-US-GuyNeural` - Male, professional
- `en-GB-SoniaNeural` - British female
- 100+ other voices

---

## Resources

- **GitHub:** https://github.com/resemble-ai/chatterbox
- **Demo:** https://huggingface.co/spaces/ResembleAI/chatterbox-turbo-demo
- **Discord:** https://discord.gg/rJq9cRJBJ6
- **Docs:** https://resemble.ai/chatterbox/
