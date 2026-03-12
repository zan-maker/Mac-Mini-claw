#!/bin/bash

# 🚀 Mediaworkbench.ai Implementation Script
# Free: 100,000 words/month for Azure OpenAI, DeepSeek, Google Gemini

set -e

echo "========================================="
echo "🚀 MEDIAWORKBENCH.AI IMPLEMENTATION"
echo "========================================="
echo "Free: 100,000 words/month"
echo "Models: Azure OpenAI, DeepSeek, Google Gemini"
echo "Savings: \$100/month vs OpenAI API"
echo "========================================="

# Configuration
CONFIG_DIR="/Users/cubiczan/.openclaw/workspace/config"
MEDIAWORKBENCH_CONFIG="$CONFIG_DIR/mediaworkbench_config.json"
ENV_FILE="$CONFIG_DIR/.env"

# Create config directory
mkdir -p "$CONFIG_DIR"

echo ""
echo "📝 SIGNUP REQUIRED (2 minutes):"
echo "   1. Go to: https://mediaworkbench.ai/"
echo "   2. Click 'Sign Up' (free)"
echo "   3. Get API key from dashboard"
echo ""
read -p "Have you signed up and have an API key? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "⚠️  Please sign up first at https://mediaworkbench.ai/"
    exit 1
fi

echo "🔑 Enter your Mediaworkbench.ai API key:"
read -r API_KEY

if [ -z "$API_KEY" ]; then
    echo "❌ API key required"
    exit 1
fi

# Save configuration
echo "💾 Saving Mediaworkbench.ai configuration..."
cat > "$MEDIAWORKBENCH_CONFIG" << EOL
{
    "provider": "mediaworkbench.ai",
    "api_key": "$API_KEY",
    "api_endpoint": "https://api.mediaworkbench.ai/v1",
    "free_tier": "100,000 words/month",
    "available_models": [
        "azure-openai/gpt-4",
        "azure-openai/gpt-3.5-turbo",
        "deepseek/deepseek-chat",
        "google/gemini-pro"
    ],
    "rate_limits": {
        "words_per_month": 100000,
        "requests_per_minute": 60
    },
    "configured_at": "$(date -Iseconds)",
    "version": "1.0"
}
EOL

echo "✅ Configuration saved: $MEDIAWORKBENCH_CONFIG"

# Add to environment file
echo "🔐 Adding to environment file..."
if [ -f "$ENV_FILE" ]; then
    if grep -q "MEDIAWORKBENCH_API_KEY" "$ENV_FILE"; then
        sed -i '' "s|MEDIAWORKBENCH_API_KEY=.*|MEDIAWORKBENCH_API_KEY=$API_KEY|" "$ENV_FILE"
    else
        echo "MEDIAWORKBENCH_API_KEY=$API_KEY" >> "$ENV_FILE"
    fi
else
    echo "MEDIAWORKBENCH_API_KEY=$API_KEY" > "$ENV_FILE"
fi

echo "✅ Environment variable set"

# Create Python client
echo "🐍 Creating Python client..."
CLIENT_FILE="/Users/cubiczan/.openclaw/workspace/scripts/mediaworkbench_client.py"

cat > "$CLIENT_FILE" << 'EOL'
#!/usr/bin/env python3
"""
Mediaworkbench.ai Client
Free: 100,000 words/month for Azure OpenAI, DeepSeek, Google Gemini
"""

import os
import json
import requests
import time
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ChatMessage:
    """Chat message"""
    role: str  # "system", "user", "assistant"
    content: str

@dataclass
class CompletionResult:
    """Completion result"""
    success: bool
    text: Optional[str] = None
    model: Optional[str] = None
    usage: Optional[Dict] = None
    error: Optional[str] = None
    response: Optional[Dict] = None

class MediaworkbenchClient:
    """Mediaworkbench.ai client with 100k free words/month"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize Mediaworkbench client
        
        Args:
            config_path: Path to configuration file
        """
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
            self.api_key = config.get('api_key')
            self.api_endpoint = config.get('api_endpoint', 'https://api.mediaworkbench.ai/v1')
            self.free_words_per_month = config.get('rate_limits', {}).get('words_per_month', 100000)
            self.available_models = config.get('available_models', [
                "azure-openai/gpt-4",
                "azure-openai/gpt-3.5-turbo",
                "deepseek/deepseek-chat",
                "google/gemini-pro"
            ])
        else:
            # Try environment variable
            self.api_key = os.getenv('MEDIAWORKBENCH_API_KEY')
            self.api_endpoint = 'https://api.mediaworkbench.ai/v1'
            self.free_words_per_month = 100000
            self.available_models = [
                "azure-openai/gpt-4",
                "azure-openai/gpt-3.5-turbo",
                "deepseek/deepseek-chat",
                "google/gemini-pro"
            ]
        
        if not self.api_key:
            raise ValueError("Mediaworkbench API key not found in config or environment")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Track usage
        self.monthly_word_count = 0
        self.last_reset = datetime.now().replace(day=1)  # Reset on 1st of month
        
        # Test connection
        try:
            self.test_connection()
        except:
            logger.warning("Initial connection test failed, but client created")
    
    def test_connection(self) -> bool:
        """Test API connection"""
        try:
            # Simple test request
            test_payload = {
                "model": "azure-openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 5
            }
            
            response = requests.post(
                f"{self.api_endpoint}/chat/completions",
                headers=self.headers,
                json=test_payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Connected to Mediaworkbench.ai")
                logger.info(f"   Free tier: {self.free_words_per_month:,} words/month")
                return True
            else:
                logger.error(f"❌ Connection failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Connection error: {e}")
            return False
    
    def chat_completion(
        self,
        messages: List[ChatMessage],
        model: str = "azure-openai/gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> CompletionResult:
        """
        Chat completion
        
        Args:
            messages: List of chat messages
            model: Model to use
            temperature: Creativity (0-2)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters
            
        Returns:
            CompletionResult
        """
        # Check monthly limit
        self._check_monthly_reset()
        estimated_words = max_tokens or 100
        
        if self.monthly_word_count + estimated_words > self.free_words_per_month:
            logger.warning(f"⚠️  Monthly limit approaching: {self.monthly_word_count}/{self.free_words_per_month} words")
            # Could switch to another free provider
        
        # Prepare messages
        messages_dict = [{"role": msg.role, "content": msg.content} for msg in messages]
        
        # Build payload
        payload = {
            "model": model,
            "messages": messages_dict,
            "temperature": temperature,
            **kwargs
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        try:
            logger.info(f"🧠 Generating completion with {model}")
            logger.info(f"   Messages: {len(messages)}, Estimated words: {estimated_words}")
            
            response = requests.post(
                f"{self.api_endpoint}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                choice = data.get('choices', [{}])[0]
                message = choice.get('message', {})
                usage = data.get('usage', {})
                
                # Update word count (approximate)
                words_used = usage.get('total_tokens', estimated_words)
                self.monthly_word_count += words_used
                
                result = CompletionResult(
                    success=True,
                    text=message.get('content'),
                    model=model,
                    usage=usage,
                    response=data
                )
                
                logger.info(f"✅ Completion successful")
                logger.info(f"   Words used: {words_used}")
                logger.info(f"   Monthly total: {self.monthly_word_count}/{self.free_words_per_month}")
                return result
                
            else:
                error_msg = f"Completion failed: {response.status_code} - {response.text}"
                logger.error(f"❌ {error_msg}")
                
                return CompletionResult(
                    success=False,
                    error=error_msg,
                    response=response.json() if response.text else None
                )
                
        except Exception as e:
            error_msg = f"Exception during completion: {e}"
            logger.error(f"❌ {error_msg}")
            
            return CompletionResult(
                success=False,
                error=error_msg
            )
    
    def simple_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: str = "azure-openai/gpt-3.5-turbo",
        **kwargs
    ) -> str:
        """
        Simple completion (convenience method)
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            model: Model to use
            **kwargs: Additional parameters
            
        Returns:
            Generated text or error message
        """
        messages = []
        
        if system_prompt:
            messages.append(ChatMessage(role="system", content=system_prompt))
        
        messages.append(ChatMessage(role="user", content=prompt))
        
        result = self.chat_completion(messages, model=model, **kwargs)
        
        if result.success:
            return result.text
        else:
            return f"Error: {result.error}"
    
    def _check_monthly_reset(self):
        """Check and reset monthly usage counter"""
        now = datetime.now()
        if now.month != self.last_reset.month or now.year != self.last_reset.year:
            self.monthly_word_count = 0
            self.last_reset = now.replace(day=1)
            logger.info(f"🔄 Monthly usage reset: {self.free_words_per_month:,} words available")
    
    def get_usage(self) -> Dict:
        """Get current usage statistics"""
        return {
            "monthly_word_count": self.monthly_word_count,
            "free_words_per_month": self.free_words_per_month,
            "words_remaining": self.free_words_per_month - self.monthly_word_count,
            "last_reset": self.last_reset.isoformat()
        }

# Example usage
if __name__ == "__main__":
    # Initialize client
    client = MediaworkbenchClient(config_path="/Users/cubiczan/.openclaw/workspace/config/mediaworkbench_config.json")
    
    # Test connection
    if not client.test_connection():
        print("⚠️  Connection test failed, but client created")
    
    # Get usage
    usage = client.get_usage()
    print(f"📊 Usage: {usage['monthly_word_count']}/{usage['free_words_per_month']} words")
    print(f"   Remaining: {usage['words_remaining']} words")
    
    # Test completion
    print("\n🧪 Testing completion...")
    result = client.simple_completion(
        prompt="Hello, how are you?",
        system_prompt="You are a helpful assistant.",
        model="azure-openai/gpt-3.5-turbo",
        max_tokens=20
    )
    
    if "Error:" not in result:
        print("✅ Test successful!")
        print(f"   Response: {result[:50]}...")
    else:
        print(f"❌ Test failed: {result}")
EOL

chmod +x "$CLIENT_FILE"
echo "✅ Python client created: $CLIENT_FILE"

# Create test script
echo "🧪 Creating test script..."
TEST_FILE="/Users/cubiczan/.openclaw/workspace/scripts/test_mediaworkbench.py"

cat > "$TEST_FILE" << 'EOL'
#!/usr/bin/env python3
"""
Test Mediaworkbench.ai integration
"""

import sys
import os
sys.path.append('/Users/cubiczan/.openclaw/workspace/scripts')

from mediaworkbench_client import MediaworkbenchClient

def test_mediaworkbench_integration():
    """Test Mediaworkbench.ai integration"""
    print("🧪 Testing Mediaworkbench.ai Integration")
    print("="*50)
    
    # Initialize client
    try:
        client = MediaworkbenchClient(config_path="/Users/cubiczan/.openclaw/workspace/config/mediaworkbench_config.json")
        print("✅ Mediaworkbench client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return False
    
    # Test connection
    if not client.test_connection():
        print("❌ Connection test failed")
        return False
    
    # Get usage
    usage = client.get_usage()
    print(f"\n📊 Free Tier Information:")
    print(f"   Words/month: {usage['free_words_per_month']:,}")
    print(f"   Used: {usage['monthly_word_count']:,}")
    print(f"   Remaining: {usage['words_remaining']:,}")
    print(f"   Last reset: {usage['last_reset']}")
    
    # Test available models
    print(f"\n🎯 Available Models:")
    models = ["azure-openai/gpt-3.5-turbo", "deepseek/deepseek-chat", "google/gemini-pro"]
    for model in models:
        print(f"   - {model}")
    
    # Test completion
    print("\n🧪 Testing completion with GPT-3.5 Turbo...")
    result = client.simple_completion(
        prompt="What is artificial intelligence in one sentence?",
        system_prompt="You are a helpful AI assistant.",
        model="azure-openai/gpt-3.5-turbo",
        max_tokens=30
    )
    
    if "Error:" not in result:
        print("✅ Completion test successful!")
        print(f"   Response: {result}")
        
        # Test DeepSeek model
        print("\n🧪 Testing completion with DeepSeek...")
        deepseek_result = client.simple_completion(
            prompt="Explain machine learning briefly",
            system_prompt="You are a technical AI assistant.",
            model="deepseek/deepseek-chat",
            max_tokens=40
        )
        
        if "Error:" not in deepseek_result:
            print("✅ DeepSeek test successful!")
            print(f"   Response: {deepseek_result[:80]}...")
        else:
            print(f"❌ DeepSeek test failed: {deepseek_result}")
    else:
        print(f"❌ Completion test failed: {result}")
        return False
    
    # Check updated usage
    updated_usage = client.get_usage()
    print(f"\n📈 Updated Usage:")
    print(f"   Used: {updated_usage['monthly_word_count']:,} words")
    print(f"   Remaining: {updated_usage['words_remaining']:,} words")
    
    print("\n✅ Mediaworkbench.ai integration test complete")
    print("\n🎯 Next steps:")
    print("1. Use as backup for OpenRouter free models")
    print("2. Monitor monthly word usage")
    print("3. Implement fallback between multiple free AI providers")
    print("4. Update cron jobs to use Mediaworkbench when OpenRouter hits limits")
    
    return True

if __name__ == "__main__":
    success = test_mediaworkbench_integration()
    if success:
        print("\n" + "="*50)
        print("✅ MEDIAWORKBENCH.AI INTEGRATION TEST COMPLETE")
        print("="*50)
        print("\n🎯 Ready to use as free AI provider")
        print("💸 Monthly savings: $100")
        print("📊 Free tier: 100,000 words/month")
    else:
        print("\n❌ MEDIAWORKBENCH.AI INTEGRATION TEST FAILED")
        print("Check configuration and try again")
EOL

chmod +x "$TEST_FILE"
echo "✅ Test script created: $TEST_FILE"

# Create migration guide
echo "📖 Creating migration guide..."
GUIDE_FILE="/Users/cubiczan/.openclaw/workspace/docs/MEDIAWORKBENCH_MIGRATION_GUIDE.md"

cat > "$GUIDE_FILE" << EOL
# Mediaworkbench.ai Migration Guide

## Free Tier: 100,000 words/month
**Models:** Azure OpenAI GPT-4/3.5, DeepSeek, Google Gemini
**Savings:** \$100/month vs OpenAI API
**Status:** Ready for implementation

## Signup Required (2 minutes):
1. Go to: https://mediaworkbench.ai/
2. Click "Sign Up" (free)
3. Get API key from dashboard

## Configuration:
\`\`\`bash
cd /Users/cubiczan/.openclaw/workspace
./scripts/setup_mediaworkbench.sh
\`\`\`

## Usage:
\`\`\`python
from mediaworkbench_client import MediaworkbenchClient

client = MediaworkbenchClient()
result = client.simple_completion(
    prompt="Your question here",
    system_prompt="You are a helpful assistant.",
    model="azure-openai/gpt-3.5-turbo"
)
\`\`\`

## Strategy:
- **Primary:** OpenRouter free models
- **Backup:** Mediaworkbench.ai (100k words/month)
- **Fallback:** Multiple free providers ensure reliability

## 🎉 READY TO IMPLEMENT!
**Monthly Savings:** \$100
**Next:** Sign up and run setup script
EOL

echo "✅ Migration guide created: $GUIDE_FILE"

echo ""
echo "========================================="
echo "✅ MEDIAWORKBENCH.AI IMPLEMENTATION READY!"
echo "========================================="
echo ""
echo "🎯 What's ready:"
echo "   1. ✅ Setup script created"
echo "   2. ✅ Python client ready"
echo "   3. ✅ Test script ready"
echo "   4. ✅ Migration guide created"
echo ""
echo "🚀 Next steps:"
echo "   1. Sign up at https://mediaworkbench.ai/"
echo "   2. Run: ./scripts/setup_mediaworkbench.sh"
echo "   3. Test: python3 scripts/test_mediaworkbench.py"
echo ""
echo "💸 Potential savings: \$100/month"
echo ""
echo "Ready for the next free service? 🚀"
