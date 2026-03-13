#!/usr/bin/env python3
"""
Secure Environment Variable Configuration Loader
Loads configuration from environment variables, never hardcodes secrets
"""

import os
import json
from typing import Dict, Any

class SecureConfig:
    """Secure configuration loader using environment variables"""
    
    @staticmethod
    def load_firestore_config() -> Dict[str, Any]:
        """Load Firestore configuration from environment"""
        return {
            "api_key": os.getenv("FIRESTORE_API_KEY"),
            "project_id": os.getenv("FIRESTORE_PROJECT_ID", "project-651348c0-d39f-4cd5-b8a"),
            "auth_domain": os.getenv("FIRESTORE_AUTH_DOMAIN", "project-651348c0-d39f-4cd5-b8a.firebaseapp.com")
        }
    
    @staticmethod
    def load_cloudinary_config() -> Dict[str, Any]:
        """Load Cloudinary configuration from environment"""
        return {
            "cloud_name": os.getenv("CLOUDINARY_CLOUD_NAME"),
            "api_key": os.getenv("CLOUDINARY_API_KEY"),
            "api_secret": os.getenv("CLOUDINARY_API_SECRET"),
            "url": os.getenv("CLOUDINARY_URL")
        }
    
    @staticmethod
    def load_brevo_config() -> Dict[str, Any]:
        """Load Brevo configuration from environment"""
        return {
            "api_key": os.getenv("BREVO_API_KEY"),
            "sender_email": os.getenv("BREVO_SENDER_EMAIL", "sam@impactquadrant.info"),
            "sender_name": os.getenv("BREVO_SENDER_NAME", "Agent Manager")
        }
    
    @staticmethod
    def load_openrouter_config() -> Dict[str, Any]:
        """Load OpenRouter configuration from environment"""
        return {
            "api_key": os.getenv("OPENROUTER_API_KEY"),
            "base_url": os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        }
    
    @staticmethod
    def get_all_config() -> Dict[str, Any]:
        """Get all configuration from environment variables"""
        return {
            "firestore": SecureConfig.load_firestore_config(),
            "cloudinary": SecureConfig.load_cloudinary_config(),
            "brevo": SecureConfig.load_brevo_config(),
            "openrouter": SecureConfig.load_openrouter_config(),
            "environment": os.getenv("NODE_ENV", "development"),
            "port": int(os.getenv("PORT", "3000"))
        }
    
    @staticmethod
    def validate_config() -> bool:
        """Validate that required environment variables are set"""
        required_vars = [
            "BREVO_API_KEY",
            "OPENROUTER_API_KEY",
            "CLOUDINARY_CLOUD_NAME",
            "CLOUDINARY_API_KEY",
            "CLOUDINARY_API_SECRET"
        ]
        
        missing = []
        for var in required_vars:
            if not os.getenv(var):
                missing.append(var)
        
        if missing:
            print(f"❌ Missing required environment variables: {missing}")
            print("   Set them in config/.env or system environment")
            return False
        
        print("✅ All required environment variables are set")
        return True

# Example usage
if __name__ == "__main__":
    print("🔒 SECURE CONFIGURATION LOADER")
    print("="*50)
    
    # Load from .env file if exists
    env_file = "/Users/cubiczan/.openclaw/workspace/config/.env"
    if os.path.exists(env_file):
        print(f"📁 Loading environment from: {env_file}")
        from dotenv import load_dotenv
        load_dotenv(env_file)
    
    # Validate configuration
    if SecureConfig.validate_config():
        config = SecureConfig.get_all_config()
        print("\n✅ Configuration loaded securely from environment variables")
        print(f"   Environment: {config['environment']}")
        print(f"   Services configured: {len(config) - 2}")  # minus environment and port
        
        # Show config (without secrets)
        safe_config = json.dumps(config, indent=2)
        # Mask secrets in output
        import re
        safe_config = re.sub(r'"api_key": "([^"]+)"', '"api_key": "***MASKED***"', safe_config)
        safe_config = re.sub(r'"api_secret": "([^"]+)"', '"api_secret": "***MASKED***"', safe_config)
        print(f"\n📋 Safe configuration view:\n{safe_config}")
    else:
        print("\n❌ Configuration validation failed")
