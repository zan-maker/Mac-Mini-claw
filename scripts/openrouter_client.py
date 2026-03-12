#!/usr/bin/env python3
"""
OpenRouter LLM Client
Free: Multiple models (DeepSeek R1, Llama, Gemma, Phi-3.5)
Replaces: DeepSeek API, OpenAI API
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

@dataclass
class ModelInfo:
    """Model information"""
    id: str
    name: str
    context_length: int
    pricing: Dict
    is_free: bool

class OpenRouterClient:
    """OpenRouter LLM client with free models"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize OpenRouter client
        
        Args:
            config_path: Path to configuration file
        """
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
            self.api_key = config.get('api_key')
            self.api_endpoint = config.get('api_endpoint', 'https://openrouter.ai/api/v1')
            self.free_models = config.get('free_models', [
                "deepseek/deepseek-r1",
                "deepseek/deepseek-v3", 
                "meta-llama/llama-3.2-3b-instruct",
                "moonshot/moonshot-v1-8k",
                "google/gemma-2-2b-it",
                "microsoft/phi-3.5-mini-instruct"
            ])
            self.rate_limits = config.get('rate_limits', {
                "requests_per_minute": 60,
                "tokens_per_minute": 60000
            })
        else:
            # Try environment variable
            self.api_key = os.getenv('OPENROUTER_API_KEY')
            self.api_endpoint = 'https://openrouter.ai/api/v1'
            self.free_models = [
                "deepseek/deepseek-r1",
                "deepseek/deepseek-v3",
                "meta-llama/llama-3.2-3b-instruct",
                "moonshot/moonshot-v1-8k",
                "google/gemma-2-2b-it",
                "microsoft/phi-3.5-mini-instruct"
            ]
            self.rate_limits = {
                "requests_per_minute": 60,
                "tokens_per_minute": 60000
            }
        
        if not self.api_key:
            raise ValueError("OpenRouter API key not found in config or environment")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://impactquadrant.info",
            "X-Title": "AI Agent System"
        }
        
        # Rate limiting
        self.request_times = []
        self.token_counts = []
        
        # Test connection
        try:
            self.test_connection()
        except:
            logger.warning("Initial connection test failed, but client created")
    
    def _check_rate_limit(self, estimated_tokens: int = 100) -> bool:
        """Check if we're within rate limits"""
        now = time.time()
        
        # Clean old entries (last minute)
        self.request_times = [t for t in self.request_times if now - t < 60]
        self.token_counts = [t for t in self.token_counts if now - t[0] < 60]
        
        # Check request limit
        if len(self.request_times) >= self.rate_limits["requests_per_minute"]:
            logger.warning(f"⚠️  Request rate limit approaching: {len(self.request_times)}/min")
            return False
        
        # Check token limit
        recent_tokens = sum(t[1] for t in self.token_counts)
        if recent_tokens + estimated_tokens > self.rate_limits["tokens_per_minute"]:
            logger.warning(f"⚠️  Token rate limit approaching: {recent_tokens}/min")
            return False
        
        return True
    
    def _record_request(self, tokens_used: int):
        """Record request for rate limiting"""
        now = time.time()
        self.request_times.append(now)
        self.token_counts.append((now, tokens_used))
    
    def test_connection(self) -> bool:
        """Test API connection"""
        try:
            response = requests.get(
                f"{self.api_endpoint}/auth/key",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json().get('data', {})
                logger.info(f"✅ Connected to OpenRouter")
                logger.info(f"   Usage: {data.get('usage', {})}")
                logger.info(f"   Limits: {data.get('limits', {})}")
                return True
            else:
                logger.error(f"❌ Connection failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Connection error: {e}")
            return False
    
    def get_available_models(self) -> List[ModelInfo]:
        """Get list of available models"""
        try:
            response = requests.get(
                f"{self.api_endpoint}/models",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                models_data = response.json().get('data', [])
                models = []
                
                for model_data in models_data:
                    model_id = model_data.get('id')
                    is_free = model_id in self.free_models
                    
                    models.append(ModelInfo(
                        id=model_id,
                        name=model_data.get('name', model_id),
                        context_length=model_data.get('context_length', 4096),
                        pricing=model_data.get('pricing', {}),
                        is_free=is_free
                    ))
                
                return models
            else:
                logger.error(f"❌ Failed to get models: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Error getting models: {e}")
            return []
    
    def chat_completion(
        self,
        messages: List[ChatMessage],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> CompletionResult:
        """
        Chat completion
        
        Args:
            messages: List of chat messages
            model: Model to use (default: first free model)
            temperature: Creativity (0-2)
            max_tokens: Maximum tokens to generate
            stream: Stream response
            **kwargs: Additional parameters
            
        Returns:
            CompletionResult
        """
        # Select model
        if model is None:
            model = self.free_models[0]  # Default to first free model
        
        # Check if model is free
        if model not in self.free_models:
            logger.warning(f"⚠️  Model {model} may not be free. Using {self.free_models[0]} instead.")
            model = self.free_models[0]
        
        # Check rate limits
        estimated_tokens = max_tokens or 100
        if not self._check_rate_limit(estimated_tokens):
            # Try a different free model
            for alt_model in self.free_models:
                if alt_model != model:
                    model = alt_model
                    logger.info(f"🔄 Switching to alternative free model: {model}")
                    break
        
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
        
        if stream:
            payload["stream"] = True
        
        try:
            logger.info(f"🧠 Generating completion with {model}")
            logger.info(f"   Messages: {len(messages)}, Estimated tokens: {estimated_tokens}")
            
            response = requests.post(
                f"{self.api_endpoint}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30,
                stream=stream
            )
            
            if response.status_code == 200:
                if stream:
                    # Handle streaming response
                    full_response = ""
                    for line in response.iter_lines():
                        if line:
                            line_str = line.decode('utf-8')
                            if line_str.startswith('data: '):
                                data_str = line_str[6:]
                                if data_str == '[DONE]':
                                    break
                                try:
                                    data = json.loads(data_str)
                                    choice = data.get('choices', [{}])[0]
                                    delta = choice.get('delta', {})
                                    if 'content' in delta:
                                        content = delta['content']
                                        full_response += content
                                except:
                                    pass
                    
                    result = CompletionResult(
                        success=True,
                        text=full_response,
                        model=model,
                        response={"streamed": True}
                    )
                else:
                    data = response.json()
                    choice = data.get('choices', [{}])[0]
                    message = choice.get('message', {})
                    usage = data.get('usage', {})
                    
                    # Record tokens used
                    tokens_used = usage.get('total_tokens', estimated_tokens)
                    self._record_request(tokens_used)
                    
                    result = CompletionResult(
                        success=True,
                        text=message.get('content'),
                        model=model,
                        usage=usage,
                        response=data
                    )
                
                logger.info(f"✅ Completion successful")
                logger.info(f"   Tokens: {result.usage.get('total_tokens', 'N/A') if result.usage else 'N/A'}")
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
        model: Optional[str] = None,
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
    
    def get_free_models(self) -> List[str]:
        """Get list of free models"""
        return self.free_models.copy()
    
    def rotate_free_model(self) -> str:
        """Rotate to next free model (for rate limiting)"""
        if not hasattr(self, '_current_model_index'):
            self._current_model_index = 0
        
        model = self.free_models[self._current_model_index]
        self._current_model_index = (self._current_model_index + 1) % len(self.free_models)
        
        return model

# Example usage
if __name__ == "__main__":
    # Initialize client
    client = OpenRouterClient(config_path="/Users/cubiczan/.openclaw/workspace/config/openrouter_config.json")
    
    # Test connection
    if not client.test_connection():
        print("⚠️  Connection test failed, but client created")
    
    # Get available models
    models = client.get_available_models()
    free_models = [m for m in models if m.is_free]
    
    print(f"✅ Available free models: {len(free_models)}")
    for model in free_models[:3]:  # Show first 3
        print(f"   - {model.id} ({model.context_length} context)")
    
    # Test completion with free model
    print("\n🧪 Testing free model completion...")
    result = client.simple_completion(
        prompt="Hello, how are you?",
        system_prompt="You are a helpful AI assistant.",
        model="google/gemma-2-2b-it",
        max_tokens=20
    )
    
    if "Error:" not in result:
        print("✅ Free model test successful!")
        print(f"   Response: {result[:50]}...")
    else:
        print(f"❌ Free model test failed: {result}")
