# Chatterbox Installation Status

## ❌ Local Installation Issue

**Problem:** Chatterbox requires `torch==2.6.0` which doesn't exist in stable releases.

**Available torch versions:** 2.0.0 - 2.2.2 (CPU)
**Required by Chatterbox:** torch==2.6.0

---

## Why This Happens

Chatterbox is a **GPU-focused** TTS model:
- Designed for CUDA GPUs (NVIDIA)
- macOS doesn't support CUDA
- CPU torch versions are behind GPU versions

---

## Solutions

### Option 1: Use Cloud API
Use Chatterbox via Hugging Face Spaces or Resemble AI API:
- **Demo:** https://huggingface.co/spaces/ResembleAI/chatterbox-turbo-demo
- **API:** https://resemble.ai (paid but cheaper than ElevenLabs)

### Option 2: Google Colab (Free GPU)
```python
# In Colab with GPU runtime:
!pip install chatterbox-tts

from chatterbox.tts import ChatterboxTTS
model = ChatterboxTTS.from_pretrained(device="cuda")
wav = model.generate("Hello, this is a test.")
```

### Option 3: Wait for Update
Chatterbox may release a CPU-compatible version in the future.

---

## Alternative: Use What We Have

We already have:
- ✅ **n8n** - Workflow automation
- ✅ **Ollama** - Local LLM
- ✅ **fpdf2** - PDF generation
- ✅ **Multiple TTS APIs** available via web

For voice output, can use:
- **ElevenLabs API** (paid)
- **OpenAI TTS API** (paid)
- **Edge TTS** (free, Microsoft Edge's TTS)
- **gTTS** (Google Translate TTS, free)

---

## Recommendation

For lead generation voice needs:
1. **Use Vapi** for phone calls (once API key is resolved)
2. **Use n8n + webhooks** for voice workflows
3. **Use cloud TTS APIs** for audio content generation

Chatterbox is best suited for:
- Linux servers with NVIDIA GPUs
- Google Colab projects
- Cloud deployment

---

*Updated: 2026-02-16*
