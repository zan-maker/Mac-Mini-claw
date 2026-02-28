#!/usr/bin/env python3
"""
Unified AI Content Generator
Prioritizes Google Gemini (with $300 credits) for all content
Falls back to xAI (Grok-4) if needed
Uses DeepSeek for system tasks
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, Any, Optional

class UnifiedAIGenerator:
    """Unified AI generator prioritizing Google Gemini with $300 credits"""
    
    def __init__(self):
        self.workspace = "/Users/cubiczan/.openclaw/workspace"
        self.config_path = os.path.join(self.workspace, "config/social_media_config.json")
        self.results_dir = os.path.join(self.workspace, "results/ai_generation")
        
        # Ensure directories exist
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Load configuration
        self.config = self.load_config()
        
        # Initialize services
        self.services = self.initialize_services()
        
        print("🤖 Unified AI Generator Initialized")
        print(f"💰 Primary: Google Gemini 2.5 Flash ($300 credits)")
        print(f"🔧 Backup: xAI (Grok-4)")
        print(f"⚙️ System: DeepSeek")
        print("="*60)
    
    def load_config(self):
        """Load AI services configuration"""
        if not os.path.exists(self.config_path):
            print(f"❌ Config file not found: {self.config_path}")
            return {}
        
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return {}
    
    def initialize_services(self):
        """Initialize all AI services"""
        services = {}
        ai_config = self.config.get("ai_services", {})
        
        # Google Gemini (Primary)
        gemini_config = ai_config.get("gemini", {})
        if gemini_config.get("enabled", False):
            services["gemini"] = {
                "api_key": gemini_config.get("api_key", ""),
                "model": gemini_config.get("model", "gemini-2.5-flash"),
                "priority": gemini_config.get("priority", "primary"),
                "credits": gemini_config.get("credits", "$300 Google Cloud"),
                "base_url": "https://generativelanguage.googleapis.com/v1beta"
            }
        
        # xAI (Grok-4) - Backup
        xai_config = ai_config.get("xai", {})
        if xai_config.get("enabled", False):
            services["xai"] = {
                "api_key": xai_config.get("api_key", ""),
                "model": xai_config.get("model", "grok-4-latest"),
                "priority": xai_config.get("priority", "backup"),
                "base_url": "https://api.x.ai/v1"
            }
        
        # DeepSeek - System
        deepseek_config = ai_config.get("deepseek", {})
        if deepseek_config.get("enabled", False):
            services["deepseek"] = {
                "model": deepseek_config.get("model", "custom-api-deepseek-com/deepseek-chat"),
                "priority": deepseek_config.get("priority", "system")
            }
        
        return services
    
    def generate_with_gemini(self, prompt: str, model: str = "gemini-2.5-flash") -> Optional[Dict]:
        """Generate content using Google Gemini (Primary)"""
        print(f"🔮 Generating with Google Gemini ({model})...")
        
        gemini_config = self.services.get("gemini", {})
        api_key = gemini_config.get("api_key", "")
        
        if not api_key:
            print("❌ Gemini API key not configured")
            return None
        
        url = f"{gemini_config['base_url']}/models/{model}:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            response = requests.post(url, json=payload, timeout=45)
            
            if response.status_code == 200:
                data = response.json()
                text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                
                # Get usage metadata
                usage = data.get("usageMetadata", {})
                
                result = {
                    "success": True,
                    "service": "gemini",
                    "model": model,
                    "content": text,
                    "prompt_tokens": usage.get("promptTokenCount", 0),
                    "candidates_token_count": usage.get("candidatesTokenCount", 0),
                    "total_tokens": usage.get("totalTokenCount", 0),
                    "timestamp": datetime.now().isoformat()
                }
                
                print(f"✅ Gemini generation successful ({result['total_tokens']} tokens)")
                return result
                
            else:
                print(f"❌ Gemini generation failed: {response.status_code}")
                print(f"   Error: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"❌ Gemini API request failed: {e}")
            return None
    
    def generate_with_xai(self, prompt: str, model: str = "grok-4-latest") -> Optional[Dict]:
        """Generate content using xAI (Grok-4) - Backup"""
        print(f"🧠 Generating with xAI ({model})...")
        
        xai_config = self.services.get("xai", {})
        api_key = xai_config.get("api_key", "")
        
        if not api_key:
            print("❌ xAI API key not configured")
            return None
        
        url = f"{xai_config['base_url']}/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant for business content creation."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": model,
            "stream": False,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=45)
            
            if response.status_code == 200:
                data = response.json()
                text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                # Get usage
                usage = data.get("usage", {})
                
                result = {
                    "success": True,
                    "service": "xai",
                    "model": model,
                    "content": text,
                    "prompt_tokens": usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                    "total_tokens": usage.get("total_tokens", 0),
                    "timestamp": datetime.now().isoformat()
                }
                
                print(f"✅ xAI generation successful ({result['total_tokens']} tokens)")
                return result
                
            else:
                print(f"❌ xAI generation failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ xAI API request failed: {e}")
            return None
    
    def generate_content(self, prompt: str, content_type: str = "text") -> Dict:
        """
        Generate content with priority:
        1. Google Gemini (Primary - uses $300 credits)
        2. xAI (Grok-4) - Backup
        3. DeepSeek - System fallback
        """
        print(f"🎯 Generating {content_type} content...")
        print(f"📝 Prompt: {prompt[:100]}...")
        
        # Try Google Gemini first (Primary)
        gemini_result = self.generate_with_gemini(prompt)
        if gemini_result:
            gemini_result["priority_used"] = "primary"
            self.save_result(gemini_result, content_type)
            return gemini_result
        
        # Fall back to xAI (Backup)
        print("⚠️ Gemini failed, trying xAI (Grok-4)...")
        xai_result = self.generate_with_xai(prompt)
        if xai_result:
            xai_result["priority_used"] = "backup"
            self.save_result(xai_result, content_type)
            return xai_result
        
        # Ultimate fallback (would be DeepSeek, but we don't have API key)
        print("❌ Both Gemini and xAI failed")
        
        # Return error result
        error_result = {
            "success": False,
            "service": "none",
            "model": "none",
            "content": f"Failed to generate content. Prompt: {prompt[:200]}...",
            "error": "All AI services failed",
            "timestamp": datetime.now().isoformat(),
            "priority_used": "failed"
        }
        
        self.save_result(error_result, content_type)
        return error_result
    
    def generate_social_media_post(self, topic: str, platform: str = "twitter", tone: str = "professional") -> Dict:
        """Generate social media post with optimal AI service"""
        print(f"📱 Generating {platform} post about: {topic}")
        
        prompt = f"""
        Create a {platform} post about: {topic}
        
        Tone: {tone}
        Platform: {platform}
        
        Requirements:
        1. Engaging and shareable
        2. Include 3-5 relevant hashtags
        3. Add appropriate emojis
        4. Include a call-to-action
        5. Platform-appropriate length
        
        Format as:
        POST: [the post content]
        HASHTAGS: [comma-separated hashtags]
        """
        
        result = self.generate_content(prompt, "social_media_post")
        
        if result["success"]:
            # Parse the response
            content = result["content"]
            post_content = ""
            hashtags = []
            
            for line in content.split('\n'):
                if line.startswith("POST:"):
                    post_content = line.replace("POST:", "").strip()
                elif line.startswith("HASHTAGS:"):
                    hashtags_str = line.replace("HASHTAGS:", "").strip()
                    hashtags = [tag.strip() for tag in hashtags_str.split(',')]
            
            if not post_content:
                post_content = content.strip()
            
            result["parsed"] = {
                "platform": platform,
                "topic": topic,
                "tone": tone,
                "content": post_content,
                "hashtags": hashtags,
                "service_used": result["service"]
            }
        
        return result
    
    def generate_content_calendar(self, topics: list, days: int = 7) -> Dict:
        """Generate content calendar with optimal AI service"""
        print(f"📅 Generating {days}-day content calendar...")
        
        topics_str = ", ".join(topics)
        
        prompt = f"""
        Create a {days}-day social media content calendar focused on: {topics_str}
        
        For each day, provide:
        1. Main theme/topic
        2. Platform-specific content ideas (Twitter, Instagram, LinkedIn)
        3. Hashtag strategy
        4. Visual concept suggestions
        5. Key messaging points
        
        Format as structured content that can be parsed.
        """
        
        result = self.generate_content(prompt, "content_calendar")
        
        if result["success"]:
            result["metadata"] = {
                "topics": topics,
                "days": days,
                "service_used": result["service"]
            }
        
        return result
    
    def analyze_image_content(self, image_description: str, purpose: str = "social_media") -> Dict:
        """Analyze image content with Gemini Vision"""
        print(f"🖼️ Analyzing image content for: {purpose}")
        
        prompt = f"""
        Analyze this image description for {purpose} use:
        
        Image: {image_description}
        
        Provide:
        1. Visual strengths and weaknesses
        2. Social media optimization suggestions
        3. Recommended platforms
        4. Caption ideas
        5. Hashtag suggestions
        
        Be specific and actionable.
        """
        
        # Use Gemini for image analysis (its specialty)
        result = self.generate_with_gemini(prompt)
        
        if result:
            result["content_type"] = "image_analysis"
            result["purpose"] = purpose
            self.save_result(result, "image_analysis")
            return result
        
        # Fallback to regular text generation
        return self.generate_content(prompt, "image_analysis")
    
    def save_result(self, result: Dict, content_type: str):
        """Save generation results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{content_type}_{timestamp}.json"
        filepath = os.path.join(self.results_dir, filename)
        
        with open(filepath, "w") as f:
            json.dump(result, f, indent=2)
        
        print(f"📁 Results saved: {filepath}")
        return filepath
    
    def get_service_stats(self):
        """Get statistics about AI service usage"""
        stats = {
            "total_generations": 0,
            "by_service": {},
            "by_content_type": {},
            "total_tokens": 0
        }
        
        # Count files in results directory
        if os.path.exists(self.results_dir):
            for filename in os.listdir(self.results_dir):
                if filename.endswith(".json"):
                    filepath = os.path.join(self.results_dir, filename)
                    try:
                        with open(filepath, "r") as f:
                            data = json.load(f)
                        
                        stats["total_generations"] += 1
                        
                        # Count by service
                        service = data.get("service", "unknown")
                        stats["by_service"][service] = stats["by_service"].get(service, 0) + 1
                        
                        # Count by content type (from filename)
                        content_type = filename.split("_")[0]
                        stats["by_content_type"][content_type] = stats["by_content_type"].get(content_type, 0) + 1
                        
                        # Count tokens
                        total_tokens = data.get("total_tokens", 0)
                        if isinstance(total_tokens, (int, float)):
                            stats["total_tokens"] += total_tokens
                        
                    except:
                        continue
        
        return stats

def main():
    """Main function"""
    print("🤖 Unified AI Content Generator")
    print("="*60)
    
    # Initialize generator
    generator = UnifiedAIGenerator()
    
    # Check services
    print("\n🔍 Available AI Services:")
    for service_name, config in generator.services.items():
        print(f"   • {service_name.upper()}: {config.get('priority', 'unknown').upper()}")
        if service_name == "gemini":
            print(f"     Credits: {config.get('credits', 'unknown')}")
    
    print("\n" + "="*60)
    print("🎯 CONTENT GENERATION OPTIONS")
    print("="*60)
    
    print("\n1. Generate social media post")
    print("2. Generate content calendar (7 days)")
    print("3. Analyze image content")
    print("4. Test all services")
    print("5. View statistics")
    print("6. Exit")
    
    choice = input("\nSelect option (1-6): ")
    
    business_topics = [
        "lead generation automation",
        "AI-powered marketing",
        "business growth strategies",
        "social media for SMBs"
    ]
    
    if choice == "1":
        topic = input("Topic: ") or business_topics[0]
        platform = input("Platform (twitter/instagram/facebook/linkedin): ") or "twitter"
        tone = input("Tone (professional/casual/enthusiastic): ") or "professional"
        
        result = generator.generate_social_media_post(topic, platform, tone)
        
        if result["success"]:
            print(f"\n✅ Generated with {result['service'].upper()} ({result['priority_used']})")
            if "parsed" in result:
                parsed = result["parsed"]
                print(f"\n📝 Post content:")
                print(f"   {parsed['content']}")
                print(f"\n🏷️ Hashtags: {', '.join(parsed['hashtags'][:3])}")
            else:
                print(f"\n📝 Content:\n{result['content'][:500]}...")
        else:
            print(f"\n❌ Generation failed")
    
    elif choice == "2":
        print(f"Using topics: {', '.join(business_topics[:3])}")
        result = generator.generate_content_calendar(business_topics[:3], days=7)
        
        if result["success"]:
            print(f"\n✅ Generated with {result['service'].upper()}")
            print(f"\n📅 Content calendar created ({result['metadata']['days']} days)")
            print(f"\n📋 Preview:\n{result['content'][:500]}...")
    
    elif choice == "3":
        image_desc = input("Describe the image: ") or "A modern office with people collaborating around computers"
        purpose = input("Purpose (social_media/blog/advertisement): ") or "social_media"
        
        result = generator.analyze_image_content(image_desc, purpose)
        
        if result["success"]:
            print(f"\n✅ Analyzed with {result.get('service', 'gemini').upper()}")
            print(f"\n📊 Analysis:\n{result['content'][:800]}...")
    
    elif choice == "4":
        print("\n🧪 Testing all AI services...")
        
        # Test Gemini
        print("\n1. Testing Google Gemini...")
        gemini_test = generator.generate_with_gemini("Say 'Gemini is working'")
        if gemini_test:
            print(f"   ✅ Gemini: WORKING ({gemini_test['total_tokens']} tokens)")
        else:
            print("   ❌ Gemini: FAILED")
