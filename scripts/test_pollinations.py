#!/usr/bin/env python3
"""
Test Pollinations.AI image generation integration
"""

import sys
import os
sys.path.append('/Users/cubiczan/.openclaw/workspace/scripts')

from pollinations_client import PollinationsClient

def test_pollinations_integration():
    """Test Pollinations.AI image generation"""
    print("🧪 Testing Pollinations.AI Image Generation")
    print("="*50)
    
    # Initialize client
    try:
        client = PollinationsClient(config_path="/Users/cubiczan/.openclaw/workspace/config/pollinations_config.json")
        print("✅ Pollinations client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return False
    
    # Test connection
    if not client.test_connection():
        print("❌ Connection test failed")
        return False
    
    print(f"\n📊 Configuration:")
    print(f"   API Endpoint: {client.api_endpoint}")
    print(f"   Default Model: {client.default_model}")
    print(f"   Available Models: {', '.join(client.available_models)}")
    print(f"   Free tier: Unlimited images, no API keys")
    
    # Test simple image generation
    print("\n🧪 Testing simple image generation...")
    test_prompt = "A beautiful digital art of a mountain landscape at sunset"
    
    result = client.generate_image(
        prompt=test_prompt,
        width=512,
        height=512,
        model="flux",
        save_path="/tmp/test_pollinations_simple.png"
    )
    
    if result.success:
        print("✅ Simple image generated successfully!")
        print(f"   Prompt: {result.prompt[:50]}...")
        print(f"   Size: {len(result.image_data)} bytes")
        print(f"   Time: {result.response_time:.2f}s")
        print(f"   Saved to: {result.image_path}")
    else:
        print(f"❌ Simple image failed: {result.error}")
        return False
    
    # Test AI finance visual (for Instagram)
    print("\n🧪 Testing AI finance visual (Instagram format)...")
    finance_result = client.generate_ai_finance_visual(
        theme="stock market trends and cryptocurrency",
        style="professional infographic with clean charts",
        save_path="/tmp/ai_finance_instagram_test.png"
    )
    
    if finance_result.success:
        print("✅ AI finance visual generated successfully!")
        print(f"   Prompt: {finance_result.prompt[:60]}...")
        print(f"   Size: {len(finance_result.image_data)} bytes")
        print(f"   Time: {finance_result.response_time:.2f}s")
        print(f"   Saved to: {finance_result.image_path}")
        print(f"   Format: {finance_result.params.get('width')}x{finance_result.params.get('height')}")
    else:
        print(f"❌ AI finance visual failed: {finance_result.error}")
        return False
    
    print("\n✅ Pollinations.AI integration test complete")
    print("\n🎯 Next steps:")
    print("1. Update Instagram automation to use Pollinations.AI")
    print("2. Replace OpenAI DALL-E calls in all scripts")
    print("3. Test with actual Instagram posting workflow")
    print("4. Monitor image quality and generation speed")
    
    return True

if __name__ == "__main__":
    success = test_pollinations_integration()
    if success:
        print("\n" + "="*50)
        print("✅ POLLINATIONS.AI INTEGRATION TEST COMPLETE")
        print("="*50)
        print("\n🎯 Ready to replace OpenAI DALL-E")
        print("💸 Monthly savings: $100")
        print("🎨 Free tier: Unlimited images, no API keys")
    else:
        print("\n❌ POLLINATIONS.AI INTEGRATION TEST FAILED")
        print("Check configuration and try again")
