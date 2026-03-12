#!/usr/bin/env python3
"""
Pollinations.AI Image Generation Client
Free: Unlimited image generation, no API keys
Replaces: OpenAI DALL-E
"""

import os
import json
import requests
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
from urllib.parse import quote
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ImageGenerationParams:
    """Image generation parameters"""
    prompt: str
    width: int = 1024
    height: int = 1024
    model: str = "flux"
    seed: Optional[int] = None
    nologo: bool = True
    enhance: bool = True
    private: bool = False
    
    def to_query_params(self) -> Dict:
        """Convert to query parameters"""
        params = {
            "width": self.width,
            "height": self.height,
            "model": self.model,
            "nologo": str(self.nologo).lower(),
            "enhance": str(self.enhance).lower(),
            "private": str(self.private).lower()
        }
        
        if self.seed is not None:
            params["seed"] = self.seed
        
        return params

@dataclass
class ImageGenerationResult:
    """Image generation result"""
    success: bool
    image_url: Optional[str] = None
    image_data: Optional[bytes] = None
    image_path: Optional[str] = None
    prompt: Optional[str] = None
    params: Optional[Dict] = None
    error: Optional[str] = None
    response_time: Optional[float] = None

class PollinationsClient:
    """Pollinations.AI image generation client"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize Pollinations client
        
        Args:
            config_path: Path to configuration file
        """
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
            self.api_endpoint = config.get('api_endpoint', 'https://image.pollinations.ai/prompt/')
            self.default_width = config.get('default_width', 1024)
            self.default_height = config.get('default_height', 1024)
            self.default_model = config.get('default_model', 'flux')
            self.available_models = config.get('available_models', ['flux', 'dall-e', 'stable-diffusion', 'midjourney'])
        else:
            self.api_endpoint = 'https://image.pollinations.ai/prompt/'
            self.default_width = 1024
            self.default_height = 1024
            self.default_model = 'flux'
            self.available_models = ['flux', 'dall-e', 'stable-diffusion', 'midjourney']
        
        # Test connection
        self.test_connection()
    
    def test_connection(self) -> bool:
        """Test API connection"""
        try:
            test_url = f"{self.api_endpoint}test%20image?width=256&height=256"
            response = requests.get(test_url, timeout=10)
            
            if response.status_code == 200:
                logger.info("✅ Connected to Pollinations.AI")
                logger.info(f"   Free tier: Unlimited images, no API keys")
                return True
            else:
                logger.error(f"❌ Connection failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Connection error: {e}")
            return False
    
    def generate_image(
        self,
        prompt: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        model: Optional[str] = None,
        seed: Optional[int] = None,
        save_path: Optional[str] = None,
        **kwargs
    ) -> ImageGenerationResult:
        """
        Generate image from text prompt
        
        Args:
            prompt: Text description of image
            width: Image width (default: 1024)
            height: Image height (default: 1024)
            model: Model to use (flux, dall-e, stable-diffusion, midjourney)
            seed: Random seed for reproducibility
            save_path: Path to save image (optional)
            **kwargs: Additional parameters
            
        Returns:
            ImageGenerationResult with image data
        """
        start_time = time.time()
        
        # Set defaults
        if width is None:
            width = self.default_width
        if height is None:
            height = self.default_height
        if model is None:
            model = self.default_model
        
        # Validate model
        if model not in self.available_models:
            logger.warning(f"Model {model} not in available models. Using {self.default_model}")
            model = self.default_model
        
        # Create parameters
        params = ImageGenerationParams(
            prompt=prompt,
            width=width,
            height=height,
            model=model,
            seed=seed,
            **kwargs
        )
        
        try:
            # Encode prompt for URL
            encoded_prompt = quote(prompt)
            
            # Build URL with parameters
            url = f"{self.api_endpoint}{encoded_prompt}"
            query_params = params.to_query_params()
            
            logger.info(f"🖼️  Generating image: {prompt[:50]}...")
            logger.info(f"   Model: {model}, Size: {width}x{height}")
            
            # Make request
            response = requests.get(url, params=query_params, timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                # Check if response is an image
                content_type = response.headers.get('content-type', '')
                
                if 'image' in content_type:
                    image_data = response.content
                    
                    # Save image if path provided
                    image_path = None
                    if save_path:
                        os.makedirs(os.path.dirname(save_path), exist_ok=True)
                        with open(save_path, 'wb') as f:
                            f.write(image_data)
                        image_path = save_path
                        logger.info(f"💾 Image saved: {save_path}")
                    
                    logger.info(f"✅ Image generated successfully")
                    logger.info(f"   Size: {len(image_data)} bytes, Time: {response_time:.2f}s")
                    
                    return ImageGenerationResult(
                        success=True,
                        image_url=response.url,
                        image_data=image_data,
                        image_path=image_path,
                        prompt=prompt,
                        params=asdict(params),
                        response_time=response_time
                    )
                else:
                    error_msg = f"Response is not an image: {content_type}"
                    logger.error(f"❌ {error_msg}")
                    
                    return ImageGenerationResult(
                        success=False,
                        prompt=prompt,
                        params=asdict(params),
                        error=error_msg,
                        response_time=response_time
                    )
            else:
                error_msg = f"Generation failed: {response.status_code} - {response.text[:100]}"
                logger.error(f"❌ {error_msg}")
                
                return ImageGenerationResult(
                    success=False,
                    prompt=prompt,
                    params=asdict(params),
                    error=error_msg,
                    response_time=response_time
                )
                
        except Exception as e:
            error_msg = f"Exception during generation: {e}"
            logger.error(f"❌ {error_msg}")
            
            return ImageGenerationResult(
                success=False,
                prompt=prompt,
                params=asdict(params),
                error=error_msg
            )
    
    def generate_ai_finance_visual(
        self,
        theme: str = "market trends",
        style: str = "professional infographic",
        save_path: Optional[str] = None
    ) -> ImageGenerationResult:
        """
        Generate AI finance visual for Instagram
        
        Args:
            theme: Finance theme (market trends, crypto, stocks, etc.)
            style: Visual style
            save_path: Path to save image
            
        Returns:
            ImageGenerationResult
        """
        # Create prompt for AI finance visual
        prompt = f"AI finance visual, {theme}, {style}, clean professional design, data visualization, charts and graphs, modern aesthetic, suitable for Instagram, high quality, detailed"
        
        return self.generate_image(
            prompt=prompt,
            width=1080,  # Instagram optimal width
            height=1080, # Instagram square format
            model="flux",  # Best for detailed images
            enhance=True,
            nologo=True,
            save_path=save_path
        )

# Example usage
if __name__ == "__main__":
    # Initialize client
    client = PollinationsClient(config_path="/Users/cubiczan/.openclaw/workspace/config/pollinations_config.json")
    
    # Test connection
    if not client.test_connection():
        print("❌ Connection test failed")
        exit(1)
    
    # Test image generation
    print("\n🧪 Testing image generation...")
    result = client.generate_image(
        prompt="A beautiful sunset over mountains, digital art",
        width=512,
        height=512,
        model="flux",
        save_path="/tmp/test_pollinations.png"
    )
    
    if result.success:
        print("✅ Image generated successfully!")
        print(f"   Size: {len(result.image_data)} bytes")
        print(f"   Time: {result.response_time:.2f}s")
        print(f"   Saved to: {result.image_path}")
    else:
        print(f"❌ Image generation failed: {result.error}")
