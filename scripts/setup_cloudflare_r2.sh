#!/bin/bash

# 🚀 Cloudflare R2 Implementation Script
# Free: 10GB storage, unlimited requests

set -e

echo "========================================="
echo "🚀 CLOUDFLARE R2 IMPLEMENTATION"
echo "========================================="
echo "Free: 10GB storage, unlimited requests"
echo "Use: File storage for Instagram, general storage"
echo "Savings: \$50/month vs S3/cloud storage"
echo "========================================="

# Configuration
CONFIG_DIR="/Users/cubiczan/.openclaw/workspace/config"
R2_CONFIG="$CONFIG_DIR/cloudflare_r2_config.json"
ENV_FILE="$CONFIG_DIR/.env"

echo ""
echo "📋 PREREQUISITES:"
echo "1. Cloudflare account (free)"
echo "2. R2 bucket created"
echo "3. API token with R2 permissions"
echo ""
echo "🔗 Sign up: https://dash.cloudflare.com/sign-up"

# Check for credentials
if [ $# -lt 3 ]; then
    echo "❓ Do you have Cloudflare R2 credentials ready?"
    echo ""
    echo "📋 Needed credentials:"
    echo "   • Account ID (from Cloudflare dashboard)"
    echo "   • R2 Bucket Name (you create this)"
    echo "   • Access Key ID (from API Tokens)"
    echo "   • Secret Access Key (from API Tokens)"
    echo ""
    echo "🔧 Get credentials:"
    echo "   1. Go to Cloudflare Dashboard"
    echo "   2. R2 → Create bucket"
    echo "   3. R2 → Manage R2 API Tokens"
    echo "   4. Create token with:"
    echo "      - Account: Account Read & Write"
    echo "      - R2: Object Read & Write"
    echo ""
    read -p "❓ Ready to proceed? (y to continue, n to get credentials first): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "⚠️  Get credentials first, then run:"
        echo "   ./scripts/setup_cloudflare_r2.sh <account_id> <bucket_name> <access_key_id> <secret_access_key>"
        exit 0
    fi
    
    echo "❌ Please provide credentials:"
    echo "Usage: $0 <account_id> <bucket_name> <access_key_id> <secret_access_key>"
    exit 1
fi

ACCOUNT_ID="$1"
BUCKET_NAME="$2"
ACCESS_KEY_ID="$3"
SECRET_ACCESS_KEY="$4"

echo ""
echo "🔧 Configuring Cloudflare R2..."
echo "   Account ID: $ACCOUNT_ID"
echo "   Bucket Name: $BUCKET_NAME"
echo "   Access Key ID: ${ACCESS_KEY_ID:0:10}..."
echo "   Secret Access Key: ${SECRET_ACCESS_KEY:0:10}..."

# Create configuration
cat > "$R2_CONFIG" << CONFIG_EOF
{
    "provider": "cloudflare_r2",
    "account_id": "$ACCOUNT_ID",
    "bucket_name": "$BUCKET_NAME",
    "access_key_id": "$ACCESS_KEY_ID",
    "secret_access_key": "$SECRET_ACCESS_KEY",
    "free_tier": {
        "storage": "10GB",
        "requests": "unlimited",
        "class_a_operations": "1M/month",
        "class_b_operations": "10M/month"
    },
    "endpoint": "https://\$ACCOUNT_ID.r2.cloudflarestorage.com",
    "public_url": "https://pub-\$ACCOUNT_ID.r2.dev",
    "configured_at": "$(date -Iseconds)",
    "version": "1.0"
}
CONFIG_EOF

echo "✅ Configuration saved to: $R2_CONFIG"

# Update environment file
echo ""
echo "🔧 Updating environment variables..."
if [ -f "$ENV_FILE" ]; then
    # Update existing
    grep -v "CLOUDFLARE_R2_" "$ENV_FILE" > "$ENV_FILE.tmp" || true
    mv "$ENV_FILE.tmp" "$ENV_FILE"
fi

cat >> "$ENV_FILE" << ENV_EOF
CLOUDFLARE_R2_ACCOUNT_ID=$ACCOUNT_ID
CLOUDFLARE_R2_BUCKET_NAME=$BUCKET_NAME
CLOUDFLARE_R2_ACCESS_KEY_ID=$ACCESS_KEY_ID
CLOUDFLARE_R2_SECRET_ACCESS_KEY=$SECRET_ACCESS_KEY
ENV_EOF

echo "✅ Environment variables added"

# Test the configuration
echo ""
echo "🧪 Testing configuration..."
python3 -c "
import json
import os

config_path = '$R2_CONFIG'
with open(config_path, 'r') as f:
    config = json.load(f)

print('✅ Configuration loaded successfully')
print(f'   Provider: {config[\"provider\"]}')
print(f'   Account ID: {config[\"account_id\"]}')
print(f'   Bucket Name: {config[\"bucket_name\"]}')
print(f'   Free tier: {config[\"free_tier\"][\"storage\"]} storage')

# Check environment variables
account_id = os.getenv('CLOUDFLARE_R2_ACCOUNT_ID')
bucket_name = os.getenv('CLOUDFLARE_R2_BUCKET_NAME')
access_key = os.getenv('CLOUDFLARE_R2_ACCESS_KEY_ID')
secret_key = os.getenv('CLOUDFLARE_R2_SECRET_ACCESS_KEY')

if all([account_id, bucket_name, access_key, secret_key]):
    print('✅ All environment variables set')
    print(f'   Account ID: {account_id}')
    print(f'   Bucket Name: {bucket_name}')
else:
    print('❌ Missing environment variables')
"

# Create Python client
echo ""
echo "🔧 Creating Python client..."
cat > scripts/cloudflare_r2_client.py << 'PYTHON_EOF'
#!/usr/bin/env python3
"""
Cloudflare R2 Python Client
Free tier: 10GB storage, unlimited requests
"""

import os
import json
import boto3
from botocore.client import Config
from typing import Dict, Any, Optional, BinaryIO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CloudflareR2Client:
    """Client for Cloudflare R2 (S3-compatible)"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize Cloudflare R2 client
        
        Args:
            config_path: Path to config file (optional)
        """
        self.config = self._load_config(config_path)
        self.s3_client = self._create_s3_client()
        logger.info(f"✅ CloudflareR2Client initialized")
        logger.info(f"   Bucket: {self.config['bucket_name']}")
        logger.info(f"   Free tier: {self.config['free_tier']['storage']} storage")
        
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file or environment"""
        
        # Try environment variables first
        account_id = os.getenv("CLOUDFLARE_R2_ACCOUNT_ID")
        bucket_name = os.getenv("CLOUDFLARE_R2_BUCKET_NAME")
        access_key_id = os.getenv("CLOUDFLARE_R2_ACCESS_KEY_ID")
        secret_access_key = os.getenv("CLOUDFLARE_R2_SECRET_ACCESS_KEY")
        
        # Try config file
        if not all([account_id, bucket_name, access_key_id, secret_access_key]):
            if config_path and os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        config_data = json.load(f)
                        account_id = config_data.get("account_id", account_id)
                        bucket_name = config_data.get("bucket_name", bucket_name)
                        access_key_id = config_data.get("access_key_id", access_key_id)
                        secret_access_key = config_data.get("secret_access_key", secret_access_key)
                        logger.info(f"✅ Loaded config from {config_path}")
                except Exception as e:
                    logger.warning(f"⚠️  Failed to load config file: {e}")
        
        # Default config path
        if not all([account_id, bucket_name, access_key_id, secret_access_key]):
            default_config = "/Users/cubiczan/.openclaw/workspace/config/cloudflare_r2_config.json"
            if os.path.exists(default_config):
                try:
                    with open(default_config, 'r') as f:
                        config_data = json.load(f)
                        account_id = config_data.get("account_id", account_id)
                        bucket_name = config_data.get("bucket_name", bucket_name)
                        access_key_id = config_data.get("access_key_id", access_key_id)
                        secret_access_key = config_data.get("secret_access_key", secret_access_key)
                        logger.info(f"✅ Loaded config from {default_config}")
                except Exception as e:
                    logger.warning(f"⚠️  Failed to load default config: {e}")
        
        if not all([account_id, bucket_name, access_key_id, secret_access_key]):
            raise ValueError("Missing Cloudflare R2 credentials. Set environment variables or config file.")
        
        return {
            "account_id": account_id,
            "bucket_name": bucket_name,
            "access_key_id": access_key_id,
            "secret_access_key": secret_access_key,
            "free_tier": {
                "storage": "10GB",
                "requests": "unlimited",
                "class_a_operations": "1M/month",
                "class_b_operations": "10M/month"
            },
            "endpoint_url": f"https://{account_id}.r2.cloudflarestorage.com"
        }
    
    def _create_s3_client(self):
        """Create S3-compatible client for R2"""
        return boto3.client(
            's3',
            endpoint_url=self.config["endpoint_url"],
            aws_access_key_id=self.config["access_key_id"],
            aws_secret_access_key=self.config["secret_access_key"],
            config=Config(signature_version='s3v4')
        )
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return {
            "provider": "cloudflare_r2",
            "account_id": self.config["