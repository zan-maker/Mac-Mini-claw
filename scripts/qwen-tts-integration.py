#!/usr/bin/env python3
"""
Qwen3-TTS Integration for Voice Assistant
API Key: sk-115a12c59a00439f96b1313270ac88ee
Base URL: https://dashscope.aliyuncs.com/api/v1
"""

import urllib.request
import urllib.error
import json
import os
from datetime import datetime

# Qwen API Configuration
QWEN_API_KEY = "sk-115a12c59a00439f96b1313270ac88ee"
QWEN_BASE_URL = "https://dashscope.aliyuncs.com/api/v1"

# Available voices for Qwen TTS
AVAILABLE_VOICES = {
    "zhitian_emo": "Female, emotional (Chinese)",
    "zhiyan_emo": "Female, emotional (Chinese)",
    "zhida_emo": "Male, emotional (Chinese)",
    "zhibei_emo": "Male, emotional (Chinese)",
    "longxiaochun": "Female, natural (Chinese)",
    "longwan": "Female, gentle (Chinese)",
    "longyue": "Female, sweet (Chinese)",
    "longfei": "Male, magnetic (Chinese)",
    "longjielidou": "Male, lively (Chinese)",
    "longshuo": "Male, steady (Chinese)",
    "longshuo_eng": "Male, English",
    "longxiaochun_eng": "Female, English",
}

def generate_speech(text, output_path, voice="longshuo_eng", model="cosyvoice-v1"):
    """
    Generate speech using Qwen3-TTS
    
    Args:
        text: Text to convert to speech
        output_path: Path to save the audio file
        voice: Voice ID (default: longshuo_eng for English male)
        model: TTS model (cosyvoice-v1 or speech-synthesizer)
    
    Returns:
        dict with success status and file path or error
    """
    url = f"{QWEN_BASE_URL}/services/audio/tts"
    
    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable"  # For async processing
    }
    
    payload = {
        "model": model,
        "input": {
            "text": text
        },
        "parameters": {
            "voice": voice,
            "format": "wav",
            "sample_rate": 16000
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            
            if result.get("output", {}).get("audio"):
                # Audio is returned directly
                audio_url = result["output"]["audio"]
                return download_audio(audio_url, output_path)
            elif result.get("output", {}).get("task_id"):
                # Async task - need to poll
                task_id = result["output"]["task_id"]
                return poll_async_task(task_id, output_path)
            else:
                return {"success": False, "error": f"Unexpected response: {result}"}
                
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        return {"success": False, "error": f"HTTP {e.code}: {error_body}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def download_audio(url, output_path):
    """Download audio file from URL"""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            audio_data = response.read()
            
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(audio_data)
            
        return {"success": True, "output": output_path, "size": len(audio_data)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def poll_async_task(task_id, output_path, max_wait=60):
    """Poll async task until complete"""
    import time
    
    url = f"{QWEN_BASE_URL}/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {QWEN_API_KEY}"}
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        req = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                status = result.get("output", {}).get("task_status")
                
                if status == "SUCCEEDED":
                    audio_url = result["output"].get("results", {}).get("audio_url")
                    if audio_url:
                        return download_audio(audio_url, output_path)
                    return {"success": False, "error": "No audio URL in result"}
                    
                elif status == "FAILED":
                    return {"success": False, "error": result.get("message", "Task failed")}
                    
                elif status in ["PENDING", "RUNNING"]:
                    time.sleep(2)
                    continue
                    
                else:
                    return {"success": False, "error": f"Unknown status: {status}"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    return {"success": False, "error": "Timeout waiting for task"}


def generate_lead_script(company_name, contact_name, savings_amount, output_path):
    """Generate a lead generation voice script"""
    text = f"""
    Hi {contact_name}, this is a quick follow-up from the expense reduction team.
    Based on our analysis, {company_name} could potentially save {savings_amount} annually
    through our technology-led expense optimization.
    
    Companies your size typically see 15 to 30 percent reduction in operating expenses.
    Would you be open to a brief 15-minute call to see the numbers?
    
    Thanks, and have a great day!
    """
    
    return generate_speech(text.strip(), output_path, voice="longshuo_eng")


def list_voices():
    """List available voices"""
    print("\n🎤 Available Qwen TTS Voices:\n")
    print("English Voices:")
    print("  - longshuo_eng: Male, English")
    print("  - longxiaochun_eng: Female, English")
    print("\nChinese Voices (Emotional):")
    for voice_id, description in list(AVAILABLE_VOICES.items())[:4]:
        print(f"  - {voice_id}: {description}")
    print("\nChinese Voices (Natural):")
    for voice_id, description in list(AVAILABLE_VOICES.items())[4:8]:
        print(f"  - {voice_id}: {description}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Qwen3-TTS Voice Assistant Integration")
    print("="*60 + "\n")
    
    # List available voices
    list_voices()
    
    # Test basic generation
    print("\n📝 Testing TTS generation...")
    
    test_text = "Hello, this is a test of the Qwen3 TTS system for lead generation."
    output_file = "/tmp/qwen-tts-test.wav"
    
    result = generate_speech(test_text, output_file)
    
    if result["success"]:
        print(f"✅ Audio generated: {result['output']}")
        print(f"   Size: {result.get('size', 'unknown')} bytes")
    else:
        print(f"❌ Error: {result['error']}")
        print("\n⚠️ Note: Qwen TTS requires a valid DashScope API subscription.")
        print("   If you see authentication errors, check your API key and subscription.")
    
    print("\n" + "="*60 + "\n")
