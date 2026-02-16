# Chatterbox TTS - Google Colab Template

## How to Use

1. Open Google Colab: https://colab.research.google.com/
2. Create new notebook
3. Set runtime to GPU: Runtime → Change runtime type → T4 GPU
4. Copy and paste the code below

---

## Setup Code

```python
# Cell 1: Install Chatterbox
!pip install chatterbox-tts torchaudio

# Cell 2: Import and load model
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

print("Loading Chatterbox model...")
model = ChatterboxTTS.from_pretrained(device="cuda")
print("✅ Model loaded!")

# Cell 3: Generate speech with default voice
text = "Hello, this is an automated message from the expense reduction team. Companies like yours typically save over $100,000 annually."
wav = model.generate(text)
ta.save("output.wav", wav, model.sr)
print("✅ Audio saved to output.wav")

# Cell 4: Generate with custom voice (upload 10s reference clip)
from google.colab import files
uploaded = files.upload()  # Upload your reference audio

ref_clip = list(uploaded.keys())[0]
text = "Hi there! I'm calling about your interest in expense reduction."
wav = model.generate(text, audio_prompt_path=ref_clip)
ta.save("custom_voice.wav", wav, model.sr)
print("✅ Custom voice audio saved")

# Cell 5: Download generated audio
files.download("output.wav")
files.download("custom_voice.wav")
```

---

## For Lead Generation

Generate multiple scripts:

```python
# Lead scripts generator
scripts = [
    "Hi {name}, this is a follow-up from the expense reduction team...",
    "Hello, I'm calling about the savings analysis for {company}...",
    "Thanks for your interest in reducing operational expenses..."
]

for i, script in enumerate(scripts):
    wav = model.generate(script)
    ta.save(f"script_{i}.wav", wav, model.sr)
    files.download(f"script_{i}.wav")
```

---

## Colab Link

Create notebook: https://colab.research.google.com/

---

*Use Chatterbox via Colab for free GPU-powered TTS*
