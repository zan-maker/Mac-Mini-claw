#!/usr/bin/env python3
"""
Secure Configuration Loader
Loads API keys from environment variables only
"""

import os
import json
from typing import Dict, Any, Optional

class SecureConfig:
    """Secure configuration management"""
    
    @staticmethod
    def get_env_var(name: str, default: Optional[str] = None) -> str:
        """Get environment variable with validation"""
        value = os.getenv(name, default)
        if value is None:
            raise ValueError(f"Missing required environment variable: {name}")
        return value
    
    @staticmethod
    def load_firestore() -> Dict[str, Any]:
        """Load Firestore configuration"""
        return {
            "api_key": SecureConfig.get_env_var("FIRESTORE_API_KEY"),
            "project_id": SecureConfig.get_env_var("FIRESTORE_PROJECT_ID"),
            "auth_domain": SecureConfig.get_env_var("FIRESTORE_AUTH_DOMAIN")
        }
    
    @staticmethod
    def load_cloudinary() -> Dict[str, Any]:
        """Load Cloudinary configuration"""
        return {
            "cloud_name": SecureConfig.get_env_var("CLOUDINARY_CLOUD_NAME"),
            "api_key": SecureConfig.get_env_var("CLOUDINARY_API_KEY"),
            "api_secret": SecureConfig.get_env_var("CLOUDINARY_API_SECRET")
        }
    
    @staticmethod
    def load_brevo() -> Dict[str, Any]:
        """Load Brevo configuration"""
        return {
            "api_key": SecureConfig.get_env_var("BREVO_API_KEY"),
            "sender_email": SecureConfig.get_env_var("BREVO_SENDER_EMAIL", "sam@impactquadrant.info"),
            "sender_name": SecureConfig.get_env_var("BREVO_SENDER_NAME", "Agent Manager")
        }
    
    @staticmethod
    def load_openrouter() -> Dict[str, Any]:
        """Load OpenRouter configuration"""
        return {
            "api_key": SecureConfig.get_env_var("OPENROUTER_API_KEY"),
            "base_url": SecureConfig.get_env_var("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        }
    
    @staticmethod
    def load_all() -> Dict[str, Any]:
        """Load all configurations"""
        return {
            "firestore": SecureConfig.load_firestore(),
            "cloudinary": SecureConfig.load_cloudinary(),
            "brevo": SecureConfig.load_brevo(),
            "openrouter": SecureConfig.load_openrouter(),
            "environment": os.getenv("NODE_ENV", "development")
        }

if __name__ == "__main__":
    print("🔒 Secure Configuration Loader")
    print("="*50)
    
    # Load from .env file
    env_file = "/Users/cubiczan/.openclaw/workspace/config/.env"
    if os.path.exists(env_file):
        from dotenv import load_dotenv
        load_dotenv(env_file)
        print(f"✅ Loaded environment from: {env_file}")
    
    try:
        config = SecureConfig.load_all()
        print("✅ Configuration loaded securely")
        print(f"   Services: {len(config)}")
        print(f"   Environment: {config['environment']}")
        
        # Show safe view (masked)
        safe_config = json.dumps(config, indent=2)
        safe_config = safe_config.replace(config['brevo']['api_key'], "***MASKED***")
        safe_config = safe_config.replace(config['openrouter']['api_key'], "***MASKED***")
        safe_config = safe_config.replace(config['cloudinary']['api_key'], "***MASKED***")
        safe_config = safe_config.replace(config['cloudinary']['api_secret'], "***MASKED***")
        
        print(f"\n📋 Safe configuration view:\n{safe_config}")
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("   Set missing environment variables in config/.env")
