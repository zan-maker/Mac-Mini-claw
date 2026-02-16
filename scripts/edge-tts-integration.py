#!/usr/bin/env python3
"""
Edge-TTS Integration - Free Text-to-Speech
Uses Microsoft Edge's TTS engine (100+ voices, free)
"""

import subprocess
import os

# Edge-TTS is installed in the chatterbox venv
VENV_PYTHON = os.path.expanduser("~/.openclaw/venvs/chatterbox/bin/python3")
EDGE_TTS = os.path.expanduser("~/.openclaw/venvs/chatterbox/bin/edge-tts")

def list_voices():
    """List available voices"""
    result = subprocess.run(
        [EDGE_TTS, "--list-voices"],
        capture_output=True,
        text=True
    )
    return result.stdout

def generate_audio(text, output_path, voice="en-US-JennyNeural"):
    """Generate audio from text"""
    cmd = [
        EDGE_TTS,
        "--text", text,
        "--voice", voice,
        "--write-media", output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        return {"success": True, "output": output_path}
    else:
        return {"success": False, "error": result.stderr}

def generate_lead_script(company_name, contact_name, output_path):
    """Generate a lead generation voice script"""
    text = f"""
    Hi {contact_name}, this is a quick follow-up from the expense reduction team.
    I noticed {company_name} could potentially save over $100,000 annually 
    through our technology-led expense optimization.
    
    Companies your size typically see 15 to 30 percent reduction in OPEX.
    Would you be open to a brief 15-minute call to see the numbers?
    
    Thanks, and have a great day!
    """
    
    return generate_audio(text.strip(), output_path, voice="en-US-JennyNeural")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Edge-TTS - Free Text-to-Speech")
    print("="*60 + "\n")
    
    # Test basic generation
    result = generate_audio(
        "Hello, this is a test of the Edge TTS system.",
        "/tmp/edge-tts-test.mp3"
    )
    
    if result["success"]:
        print(f"✅ Audio generated: {result['output']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Test lead script
    result2 = generate_lead_script(
        "Test Company",
        "John",
        "/tmp/lead-script.mp3"
    )
    
    if result2["success"]:
        print(f"✅ Lead script generated: {result2['output']}")
    
    print("\n" + "="*60 + "\n")
