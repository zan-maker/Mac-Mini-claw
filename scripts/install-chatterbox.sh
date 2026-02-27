#!/bin/bash
# Chatterbox TTS Installation Script
# Creates a virtual environment and installs Chatterbox

echo "============================================"
echo "Chatterbox TTS Installation"
echo "============================================"

# Create venv directory
VENVS_DIR="$HOME/.openclaw/venvs"
mkdir -p "$VENVS_DIR"

# Create Chatterbox venv
CHATTERBOX_VENV="$VENVS_DIR/chatterbox"
echo ""
echo "Creating virtual environment at: $CHATTERBOX_VENV"

python3 -m venv "$CHATTERBOX_VENV"

# Activate
source "$CHATTERBOX_VENV/bin/activate"

# Install Chatterbox
echo ""
echo "Installing chatterbox-tts..."
pip install --upgrade pip
pip install chatterbox-tts
pip install torchaudio torch

# Test installation
echo ""
echo "Testing installation..."
python3 -c "
try:
    from chatterbox.tts import ChatterboxTTS
    print('✅ Chatterbox TTS installed successfully!')
    print('   Use: source $CHATTERBOX_VENV/bin/activate')
except Exception as e:
    print(f'⚠️ Note: Chatterbox requires CUDA GPU for best performance')
    print(f'   Error: {e}')
"

echo ""
echo "============================================"
echo "Installation Complete"
echo "============================================"
echo ""
echo "To use Chatterbox:"
echo "  source $CHATTERBOX_VENV/bin/activate"
echo "  python3 -c 'from chatterbox.tts import ChatterboxTTS'"
echo ""
