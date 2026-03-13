#!/usr/bin/env python3
"""
Secure Configuration Loader
Based on Correction #1: API Key Security - Server-Side Storage Only

PRINCIPLE: Never hardcode API keys in source files.
           Store keys server-side in environment variables.
"""

import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class SecureConfig:
    """Secure configuration management using environment variables"""
    
    @staticmethod
    def get_env_var(name: str, default: Optional[str] = None) -> str:
        """
        Get environment variable with validation
        
        Args:
            name: Environment variable name
            default: Default value if not found
            
        Returns:
            Environment variable value
            
        Raises:
            ValueError: If variable not found and no default provided
        """
        value = os.getenv(name, default)
        if value is None:
            raise ValueError(f"Missing required environment variable: {name}")
        return value
    
    @staticmethod
    def mask_key(key: str) -> str:
        """Mask API key for safe logging"""
        if len(key) > 8:
            return f"{key[:4]}...{key[-4:]}"
        return "***"
    
    @classmethod
    def load_all(cls) -> Dict[str, Any]:
        """Load all configurations from environment variables"""
        
        config = {}
        
        # API Keys (never hardcoded)
        try:
            config['openai'] = {
                'api_key': cls.get_env_var('OPENAI_API_KEY'),
                'organization': cls.get_env_var('OPENAI_ORG_ID', '')
            }
            logger.info(f"OpenAI config loaded (key: {cls.mask_key(config['openai']['api_key'])})")
        except ValueError:
            logger.warning("OpenAI API key not set")
        
        try:
            config['anthropic'] = {
                'api_key': cls.get_env_var('ANTHROPIC_API_KEY')
            }
            logger.info(f"Anthropic config loaded (key: {cls.mask_key(config['anthropic']['api_key'])})")
        except ValueError:
            logger.warning("Anthropic API key not set")
        
        try:
            config['mistral'] = {
                'api_key': cls.getenv('MISTRAL_API_KEY')
            }
            logger.info(f"Mistral config loaded (key: {cls.mask_key(config['mistral']['api_key'])})")
        except ValueError:
            logger.warning("Mistral API key not set")
        
        # Database credentials
        try:
            config['database'] = {
                'url': cls.get_env_var('DATABASE_URL'),
                'username': cls.get_env_var('DB_USERNAME'),
                'password': cls.get_env_var('DB_PASSWORD')
            }
            logger.info("Database config loaded")
        except ValueError:
            logger.warning("Database credentials not set")
        
        # External services
        try:
            config['stripe'] = {
                'public_key': cls.get_env_var('STRIPE_PUBLIC_KEY'),
                'secret_key': cls.get_env_var('STRIPE_SECRET_KEY')
            }
            logger.info(f"Stripe config loaded (key: {cls.mask_key(config['stripe']['secret_key'])})")
        except ValueError:
            logger.warning("Stripe keys not set")
        
        # Application settings
        config['app'] = {
            'environment': cls.get_env_var('NODE_ENV', 'development'),
            'debug': cls.get_env_var('DEBUG', 'false').lower() == 'true',
            'port': int(cls.get_env_var('PORT', '3000'))
        }
        
        logger.info(f"Application environment: {config['app']['environment']}")
        
        return config
    
    @classmethod
    def validate_config(cls, config: Dict[str, Any]) -> bool:
        """Validate configuration for security issues"""
        
        issues = []
        
        # Check for hardcoded keys (should not be in config dict)
        hardcoded_patterns = [
            r'sk-[a-zA-Z0-9]{48}',
            r'pk_[a-z]{4}_[a-zA-Z0-9]{24}',
            r'xkeysib-[a-f0-9]{64}',
            r'AIzaSy[A-Za-z0-9_-]{33}'
        ]
        
        config_str = json.dumps(config)
        
        for pattern in hardcoded_patterns:
            import re
            if re.search(pattern, config_str):
                issues.append(f"Hardcoded API key pattern found: {pattern}")
        
        # Check for missing required configs
        required_services = ['app']
        for service in required_services:
            if service not in config:
                issues.append(f"Missing required service config: {service}")
        
        if issues:
            logger.error(f"Configuration validation failed: {issues}")
            return False
        
        logger.info("Configuration validation passed")
        return True
    
    @classmethod
    def create_env_template(cls) -> str:
        """Create .env.example template"""
        
        template = """# 🔒 SECURE CONFIGURATION - ENVIRONMENT VARIABLES
# Copy to .env and fill in your values
# NEVER commit .env to version control

# Application
NODE_ENV=development
DEBUG=false
PORT=3000

# API Keys (get from service providers)
OPENAI_API_KEY=sk-your-openai-api-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
MISTRAL_API_KEY=your-mistral-api-key-here

# Database
DATABASE_URL=postgresql://user:password@localhost/dbname
DB_USERNAME=your_db_user
DB_PASSWORD=your_db_password

# External Services
STRIPE_PUBLIC_KEY=pk_test_your_stripe_public_key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key

# Optional Services
SENTRY_DSN=your_sentry_dsn_here
LOG_LEVEL=INFO
"""
        
        return template

# Example usage demonstrating the CORRECT pattern
def example_correct_usage():
    """Example showing correct API key handling"""
    
    print("✅ CORRECT: Server-side API key handling")
    print("="*50)
    
    # Load configuration from environment variables
    config = SecureConfig.load_all()
    
    # Use in application
    openai_key = config['openai']['api_key']
    
    # Initialize client with environment variable
    # const mistralClient = new MistralClient(process.env.MISTRAL_API_KEY);
    print(f"OpenAI API key loaded from environment: {SecureConfig.mask_key(openai_key)}")
    
    # Validate configuration
    if SecureConfig.validate_config(config):
        print("✅ Configuration validation passed")
    else:
        print("❌ Configuration validation failed")
    
    # Show what NOT to do
    print("\n❌ WRONG: Client-side API key exposure")
    print("const mistralClient = new MistralClient('sk-exposed-key-12345');")
    
    print("\n" + "="*50)
    print("🎯 PRINCIPLE: Store API keys server-side in environment variables")
    print("   Never expose keys in client-side code")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Run example
    example_correct_usage()
    
    # Create .env template
    print("\n📝 .env.example template:")
    print(SecureConfig.create_env_template())