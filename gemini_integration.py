#!/usr/bin/env python3
"""
Google Gemini API Integration
For video and image analysis with $300 Google Cloud credits
"""

import os
import json
import base64
import requests
from datetime import datetime
from pathlib import Path

class GeminiIntegration:
    """Google Gemini API integration for video and image analysis"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
        # Available models (Gemini 2.5)
        self.models = {
            "gemini-2.5-flash": "gemini-2.5-flash",
            "gemini-2.5-pro": "gemini-2.5-pro", 
            "gemini-2.0-flash": "gemini-2.0-flash",
            "gemini-2.0-flash-lite": "gemini-2.0-flash-lite"
        }
        
        # Results directory
        self.results_dir = "/Users/cubiczan/.openclaw/workspace/results/gemini"
        os.makedirs(self.results_dir, exist_ok=True)
        
        print("🔮 Google Gemini Integration Initialized")
        print(f"💰 Credits: $300 Google Cloud")
        print(f"🔑 API Key: {api_key[:15]}...")
    
    def test_connection(self):
        """Test Gemini API connection"""
        print("🔌 Testing Gemini API connection...")
        
        url = f"{self.base_url}/models?key={self.api_key}"
        
        try:
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                models = response.json().get("models", [])
                available_models = [m["name"] for m in models]
                
                print(f"✅ Gemini API connection SUCCESSFUL!")
                print(f"   Available models: {len(models)}")
                print(f"   Includes: {', '.join([m for m in available_models if 'gemini' in m][:3])}")
                
                # Test a simple prompt
                test_result = self.generate_text("Say 'Gemini API is working' if you can read this.")
                if test_result:
                    print(f"   Text generation: ✅ WORKING")
                
                return True
            else:
                print(f"❌ API connection failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ API request failed: {e}")
            return False
    
    def generate_text(self, prompt, model="gemini-2.5-flash"):
        """Generate text from prompt"""
        url = f"{self.base_url}/models/{model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                return text
            else:
                print(f"❌ Text generation failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ API request failed: {e}")
            return None
    
    def analyze_image(self, image_path, prompt="Describe this image in detail"):
        """Analyze an image with Gemini Vision"""
        print(f"🖼️ Analyzing image: {os.path.basename(image_path)}...")
        
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return None
        
        # Read and encode image
        try:
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode("utf-8")
        except Exception as e:
            print(f"❌ Failed to read image: {e}")
            return None
        
        # Determine MIME type
        ext = os.path.splitext(image_path)[1].lower()
        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }
        mime_type = mime_types.get(ext, "image/jpeg")
        
        url = f"{self.base_url}/models/gemini-2.5-flash:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": image_data
                        }
                    }
                ]
            }]
        }
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                analysis = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                
                print(f"✅ Image analysis complete!")
                
                # Save results
                result = {
                    "timestamp": datetime.now().isoformat(),
                    "image": os.path.basename(image_path),
                    "prompt": prompt,
                    "analysis": analysis,
                    "model": "gemini-2.5-flash",
                    "file_size": os.path.getsize(image_path)
                }
                
                self.save_results(result, "image_analysis")
                return analysis
            else:
                print(f"❌ Image analysis failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ API request failed: {e}")
            return None
    
    def analyze_video(self, video_path, prompt="Describe this video in detail"):
        """Analyze a video with Gemini (extracts frames)"""
        print(f"🎥 Analyzing video: {os.path.basename(video_path)}...")
        
        if not os.path.exists(video_path):
            print(f"❌ Video not found: {video_path}")
            return None
        
        # Note: Gemini 1.5 can handle videos directly, but for simplicity we'll extract frames
        # For full video analysis, we need to use video API or extract key frames
        
        print("⚠️  Video analysis requires frame extraction or using Gemini 1.5 Pro with video support")
        print("   For now, let's extract a frame and analyze it")
        
        # Extract first frame using ffmpeg if available
        frame_path = os.path.join(self.results_dir, "video_frame.jpg")
        
        try:
            import subprocess
            # Extract first frame
            cmd = [
                "ffmpeg", "-i", video_path,
                "-vframes", "1",
                "-q:v", "2",
                frame_path,
                "-y"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if os.path.exists(frame_path):
                print(f"✅ Extracted frame: {frame_path}")
                # Analyze the frame
                analysis = self.analyze_image(frame_path, f"{prompt} - This is a frame from a video")
                
                # Save video metadata
                result_data = {
                    "timestamp": datetime.now().isoformat(),
                    "video": os.path.basename(video_path),
                    "prompt": prompt,
                    "frame_analysis": analysis,
                    "frame_path": frame_path,
                    "video_size": os.path.getsize(video_path),
                    "note": "Analysis based on extracted frame"
                }
                
                self.save_results(result_data, "video_analysis")
                return analysis
            else:
                print("❌ Failed to extract frame")
                return None
                
        except Exception as e:
            print(f"❌ Video processing failed: {e}")
            print("   Install ffmpeg: brew install ffmpeg")
            return None
    
    def generate_social_media_content(self, topic, platform="instagram"):
        """Generate social media content with image suggestions"""
        print(f"📱 Generating {platform} content for: {topic}")
        
        prompt = f"""
        Create engaging social media content for {platform} about: {topic}
        
        Include:
        1. A compelling caption (platform-appropriate length)
        2. 5-7 relevant hashtags
        3. Image description for a designer to create
        4. Call-to-action
        5. Suggested posting time
        
        Format as JSON with keys: caption, hashtags, image_description, cta, best_time
        """
        
        url = f"{self.base_url}/models/gemini-2.5-pro:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "response_mime_type": "application/json"
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=45)
            
            if response.status_code == 200:
                data = response.json()
                content_json = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                
                try:
                    content = json.loads(content_json)
                    print(f"✅ {platform} content generated!")
                    
                    result = {
                        "timestamp": datetime.now().isoformat(),
                        "platform": platform,
                        "topic": topic,
                        "content": content,
                        "model": "gemini-2.5-pro"
                    }
                    
                    self.save_results(result, "social_content")
                    return content
                except json.JSONDecodeError:
                    print("❌ Failed to parse JSON response")
                    return content_json
            else:
                print(f"❌ Content generation failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ API request failed: {e}")
            return None
    
    def analyze_competitor_social(self, competitor_url, platform="instagram"):
        """Analyze competitor social media (from screenshots)"""
        print(f"🎯 Analyzing competitor: {competitor_url}")
        
        # This would typically involve:
        # 1. Taking screenshots of competitor social media
        # 2. Analyzing with Gemini Vision
        # 3. Extracting insights
        
        prompt = f"""
        Based on social media analysis of {competitor_url} on {platform}, provide:
        
        1. Content themes and topics
        2. Visual style analysis
        3. Engagement strategies
        4. Hashtag usage
        5. Posting frequency patterns
        6. Recommendations for improvement
        
        Format as structured analysis.
        """
        
        analysis = self.generate_text(prompt)
        
        if analysis:
            result = {
                "timestamp": datetime.now().isoformat(),
                "competitor": competitor_url,
                "platform": platform,
                "analysis": analysis,
                "model": "gemini-2.5-pro"
            }
            
            self.save_results(result, "competitor_analysis")
            print("✅ Competitor analysis complete!")
        
        return analysis
    
    def create_content_calendar(self, topics, days=7):
        """Create content calendar with visual themes"""
        print(f"📅 Creating {days}-day content calendar...")
        
        topics_str = ", ".join(topics)
        
        prompt = f"""
        Create a {days}-day social media content calendar focused on: {topics_str}
        
        For each day, provide:
        1. Main theme/topic
        2. Platform-specific content (Instagram, Twitter, Facebook)
        3. Visual concept description
        4. Hashtag strategy
        5. Key messaging points
        
        Format as structured JSON.
        """
        
        url = f"{self.base_url}/models/gemini-2.5-pro:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "response_mime_type": "application/json"
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                calendar_json = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                
                try:
                    calendar = json.loads(calendar_json)
                    print(f"✅ {days}-day content calendar created!")
                    
                    result = {
                        "timestamp": datetime.now().isoformat(),
                        "topics": topics,
                        "days": days,
                        "calendar": calendar,
                        "model": "gemini-2.5-pro"
                    }
                    
                    self.save_results(result, "content_calendar")
                    return calendar
                except json.JSONDecodeError:
                    print("❌ Failed to parse JSON response")
                    return calendar_json
            else:
                print(f"❌ Calendar creation failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ API request failed: {e}")
            return None
    
    def save_results(self, data, prefix):
        """Save results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.json"
        filepath = os.path.join(self.results_dir, filename)
        
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        
        print(f"📁 Results saved to: {filepath}")
        return filepath

def main():
    """Main function"""
    print("🔮 Google Gemini Integration for Social Media")
    print("="*60)
    
    # API Key from user
    api_key = "AIzaSyBbQfFg7d-XOnRuB67WtKoWRx2hq9G8QhM"
    
    # Initialize
    gemini = GeminiIntegration(api_key)
    
    # Test connection
    if not gemini.test_connection():
        print("❌ Cannot proceed without API connection")
        return
    
    print("\n" + "="*60)
    print("🎯 GEMINI CAPABILITIES")
    print("="*60)
    
    print("\n1. Image analysis (Vision)")
    print("2. Video analysis (frame extraction)")
    print("3. Social media content generation")
    print("4. Competitor analysis")
    print("5. Content calendar creation")
    print("6. Run complete workflow")
    print("7. Exit")
    
    choice = input("\nSelect option (1-7): ")
    
    business_topics = [
        "lead generation automation",
        "AI-powered marketing",
        "business growth strategies",
        "social media for SMBs"
    ]
    
    if choice == "1":
        # Image analysis
        image_path = input("Image path (or press Enter for sample): ").strip()
        if not image_path:
            # Check for sample images
            sample_images = [
                "/Users/cubiczan/.openclaw/workspace/sample.jpg",
                "/Users/cubiczan/Desktop/*.jpg",
                "/Users/cubiczan/Desktop/*.png"
            ]
            
            for pattern in sample_images:
                import glob
                images = glob.glob(pattern)
                if images:
                    image_path = images[0]
                    break
        
        if image_path and os.path.exists(image_path):
            prompt = input("Analysis prompt (or press Enter for default): ").strip()
            if not prompt:
                prompt = "Describe this image in detail and suggest how it could be used for social media marketing"
            
            gemini.analyze_image(image_path, prompt)
        else:
            print("❌ No image found. Please provide a valid image path.")
    
    elif choice == "2":
        # Video analysis
        video_path = input("Video path: ").strip()
        if video_path and os.path.exists(video_path):
            prompt = input("Analysis prompt (or press Enter for default): ").strip()
            if not prompt:
                prompt = "Describe this video content and suggest social media use"
            
            gemini.analyze_video(video_path, prompt)
        else:
            print("❌ Video not found")
    
    elif choice == "3":
        # Social media content
        topic = input("Topic: ") or business_topics[0]
        platform = input("Platform (instagram/twitter/facebook): ") or "instagram"
        
        content = gemini.generate_social_media_content(topic, platform)
        if content:
            print(f"\n📝 Generated content:")
            if isinstance(content, dict):
                for key, value in content.items():
                    print(f"\n{key.upper()}:")
                    print(f"  {value}")
            else:
                print(content)
    
    elif choice == "4":
        # Competitor analysis
        competitor = input("Competitor URL/name: ") or "https://instagram.com/neilpatel"
        platform = input("Platform: ") or "instagram"
        
        analysis = gemini.analyze_competitor_social(competitor, platform)
        if analysis:
            print(f"\n📊 Analysis:\n{analysis}")
    
    elif choice == "5":
        # Content calendar
        print(f"Using topics: {', '.join(business_topics[:3])}")
        calendar = gemini.create_content_calendar(business_topics[:3], days=7)
        if calendar:
            print(f"\n📅 7-day calendar created!")
            if isinstance(calendar, dict):
                print(f"Structure: {list(calendar.keys())}")
    
    elif choice == "6":
        # Complete workflow
        print("\n" + "="*60)
        print("🚀 RUNNING COMPLETE GEMINI WORKFLOW")
        print("="*60)
        
        # 1. Generate content calendar
        print("\n1. 📅 Generating 7-day content calendar...")
        calendar = gemini.create_content_calendar(business_topics[:2], days=7)
        
        # 2. Generate sample content
        print("\n2. 📝