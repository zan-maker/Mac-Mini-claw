#!/usr/bin/env python3
"""
Cloudinary Python Client
Free tier: 25GB storage, 25GB bandwidth/month
"""

import os
import json
import cloudinary
import cloudinary.uploader
import cloudinary.api
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CloudinaryClient:
    """Client for Cloudinary API"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize Cloudinary client
        
        Args:
            config_path: Path to config file (optional)
        """
        self.config = self._load_config(config_path)
        self._configure_cloudinary()
        logger.info(f"✅ CloudinaryClient initialized")
        logger.info(f"   Cloud Name: {self.config['cloud_name']}")
        logger.info(f"   Free tier: {self.config['free_tier']['storage']} storage")
        
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file or environment"""
        
        # Try environment variables first
        cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
        api_key = os.getenv("CLOUDINARY_API_KEY")
        api_secret = os.getenv("CLOUDINARY_API_SECRET")
        
        # Try config file
        if not all([cloud_name, api_key, api_secret]):
            if config_path and os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        config_data = json.load(f)
                        cloud_name = config_data.get("cloud_name", cloud_name)
                        api_key = config_data.get("api_key", api_key)
                        api_secret = config_data.get("api_secret", api_secret)
                        logger.info(f"✅ Loaded config from {config_path}")
                except Exception as e:
                    logger.warning(f"⚠️  Failed to load config file: {e}")
        
        # Default config path
        if not all([cloud_name, api_key, api_secret]):
            default_config = "/Users/cubiczan/.openclaw/workspace/config/cloudinary_config.json"
            if os.path.exists(default_config):
                try:
                    with open(default_config, 'r') as f:
                        config_data = json.load(f)
                        cloud_name = config_data.get("cloud_name", cloud_name)
                        api_key = config_data.get("api_key", api_key)
                        api_secret = config_data.get("api_secret", api_secret)
                        logger.info(f"✅ Loaded config from {default_config}")
                except Exception as e:
                    logger.warning(f"⚠️  Failed to load default config: {e}")
        
        if not all([cloud_name, api_key, api_secret]):
            raise ValueError("Missing Cloudinary credentials. Set environment variables or config file.")
        
        return {
            "cloud_name": cloud_name,
            "api_key": api_key,
            "api_secret": api_secret,
            "free_tier": {
                "storage": "25GB",
                "bandwidth": "25GB/month",
                "transformations": "25,000/month"
            }
        }
    
    def _configure_cloudinary(self):
        """Configure Cloudinary SDK"""
        cloudinary.config(
            cloud_name=self.config["cloud_name"],
            api_key=self.config["api_key"],
            api_secret=self.config["api_secret"],
            secure=True
        )
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return {
            "provider": "cloudinary",
            "cloud_name": self.config["cloud_name"],
            "free_tier": self.config["free_tier"],
            "configured": True
        }
    
    def upload_image(self, image_path: str, public_id: Optional[str] = None, 
                    folder: str = "instagram") -> Dict[str, Any]:
        """
        Upload image to Cloudinary
        
        Args:
            image_path: Path to image file
            public_id: Public ID for the image (optional)
            folder: Folder to upload to
            
        Returns:
            Upload result
        """
        try:
            logger.info(f"📤 Uploading image: {image_path}")
            
            upload_options = {
                "folder": folder,
                "resource_type": "image"
            }
            
            if public_id:
                upload_options["public_id"] = public_id
            
            result = cloudinary.uploader.upload(image_path, **upload_options)
            
            logger.info(f"✅ Image uploaded successfully")
            logger.info(f"   URL: {result.get('secure_url', 'N/A')}")
            logger.info(f"   Public ID: {result.get('public_id', 'N/A')}")
            
            return {
                "success": True,
                "secure_url": result.get("secure_url"),
                "public_id": result.get("public_id"),
                "format": result.get("format"),
                "bytes": result.get("bytes"),
                "width": result.get("width"),
                "height": result.get("height")
            }
            
        except Exception as e:
            logger.error(f"❌ Image upload failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_instagram_url(self, public_id: str) -> str:
        """
        Get Instagram-optimized URL for an image
        
        Args:
            public_id: Public ID of the image
            
        Returns:
            Optimized URL for Instagram
        """
        # Instagram square format (1080x1080)
        transformation = {
            "width": 1080,
            "height": 1080,
            "crop": "fill",
            "quality": "auto",
            "format": "jpg"
        }
        
        url = cloudinary.utils.cloudinary_url(
            public_id,
            **transformation
        )[0]
        
        return url
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test Cloudinary connection
        
        Returns:
            Test result
        """
        logger.info("🧪 Testing Cloudinary connection...")
        
        try:
            # Try to get account usage info
            result = cloudinary.api.usage()
            
            return {
                "success": True,
                "message": "✅ Cloudinary connection successful",
                "usage": {
                    "plan": result.get("plan"),
                    "storage": result.get("storage", {}),
                    "bandwidth": result.get("bandwidth", {}),
                    "transformations": result.get("transformations", {})
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Connection test failed: {e}",
                "suggestion": "Check API credentials and network connection"
            }

# Example usage
if __name__ == "__main__":
    print("🧪 Cloudinary Client Test")
    print("="*50)
    
    try:
        # Initialize client
        client = CloudinaryClient()
        
        # Show config
        config = client.get_config()
        print(f"✅ Configuration loaded")
        print(f"   Provider: {config['provider']}")
        print(f"   Cloud Name: {config['cloud_name']}")
        print(f"   Free tier: {config['free_tier']['storage']} storage")
        
        # Test connection
        test_result = client.test_connection()
        if test_result["success"]:
            print(f"✅ {test_result['message']}")
            usage = test_result.get("usage", {})
            print(f"   Plan: {usage.get('plan', 'Free')}")
        else:
            print(f"⚠️  {test_result['error']}")
            print(f"   {test_result.get('suggestion', '')}")
        
        print("\n" + "="*50)
        print("🚀 Cloudinary Client Ready!")
        print("💰 Monthly savings: $50 vs paid image hosting")
        print("📊 Free tier: 25GB storage, 25GB bandwidth/month")
        
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        print("   Check credentials and configuration")
