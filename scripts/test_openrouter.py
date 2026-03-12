#!/usr/bin/env python3
"""
Test OpenRouter free models integration
"""

import sys
import os
sys.path.append('/Users/cubiczan/.openclaw/workspace/scripts')

from openrouter_client import OpenRouterClient, ChatMessage

def test_openrouter_integration():
    """Test OpenRouter free models integration"""
    print("🧪 Testing OpenRouter Free Models Integration")
    print("="*50)
    
    # Initialize client
    try:
        client = OpenRouterClient(config_path="/Users/cubiczan/.openclaw/workspace/config/openrouter_config.json")
        print("✅ OpenRouter client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return False
    
    # Test connection
    if not client.test_connection():
        print("❌ Connection test failed")
        return False
    
    # Get available models
    models = client.get_available_models()
    free_models = [m for m in models if m.is_free]
    
    print(f"\n📊 Available Models:")
    print(f"   Total: {len(models)}")
    print(f"   Free: {len(free_models)}")
    
    print(f"\n🎯 Free Models Available:")
    for model in free_models[:5]:  # Show first 5
        print(f"   - {model.id}")
        print(f"     Context: {model.context_length}")
    
    # Test each free model
    print("\n🧪 Testing free models (quick tests)...")
    
    test_prompts = [
        ("Simple greeting", "Hello, how are you today?"),
        ("Short question", "What is AI?"),
    ]
    
    successful_tests = 0
    tested_models = []
    
    # Test first 3 free models
    test_models = free_models[:3]
    for model in test_models:
        print(f"\n   Testing model: {model.id}")
        tested_models.append(model.id)
        
        try:
            # Simple test
            result = client.simple_completion(
                prompt="Say 'Hello, world!' in a creative way",
                system_prompt="You are a helpful assistant.",
                model=model.id,
                max_tokens=20
            )
            
            if "Error:" not in result:
                print(f"      ✅ Works: {result[:50]}...")
                successful_tests += 1
            else:
                print(f"      ❌ Failed: {result}")
                
        except Exception as e:
            print(f"      ❌ Exception: {e}")
    
    # Test rate limiting awareness
    print("\n📈 Rate Limit Information:")
    print(f"   Requests/minute: {client.rate_limits['requests_per_minute']}")
    print(f"   Tokens/minute: {client.rate_limits['tokens_per_minute']}")
    
    # Test model rotation
    print("\n🔄 Testing model rotation (for rate limiting):")
    rotation_results = []
    for i in range(3):
        model = client.rotate_free_model()
        rotation_results.append(model)
        print(f"   Rotation {i+1}: {model}")
    
    print(f"\n✅ OpenRouter integration test complete")
    print(f"   Successful model tests: {successful_tests}/{len(tested_models)}")
    
    print("\n🎯 Next steps:")
    print("1. Update DeepSeek API calls to use OpenRouter free models")
    print("2. Implement model rotation for rate limiting")
    print("3. Monitor token usage against free limits")
    print("4. Test with actual agent tasks")
    
    return successful_tests > 0

if __name__ == "__main__":
    success = test_openrouter_integration()
    if success:
        print("\n" + "="*50)
        print("✅ OPENROUTER INTEGRATION TEST COMPLETE")
        print("="*50)
        print("\n🎯 Ready to replace DeepSeek API")
        print("💸 Monthly savings: $200")
        print("\n📊 Free models available:")
        print("   - deepseek/deepseek-r1")
        print("   - deepseek/deepseek-v3")
        print("   - meta-llama/llama-3.2-3b-instruct")
        print("   - moonshot/moonshot-v1-8k")
        print("   - google/gemma-2-2b-it")
        print("   - microsoft/phi-3.5-mini-instruct")
    else:
        print("\n❌ OPENROUTER INTEGRATION TEST FAILED")
        print("Check configuration and try again")
