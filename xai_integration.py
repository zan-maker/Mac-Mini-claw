#!/usr/bin/env python3
"""
xAI (Grok) API Integration for Social Media Content Creation
"""

import os
import json
import requests
from datetime import datetime

class XAIIntegration:
    """xAI API integration for advanced content creation"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.x.ai/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # Available models
        self.models = {
            "grok-4": "grok-4-latest",
            "grok-2": "grok-2-latest",
            "grok-1": "grok-1-latest"
        }
    
    def test_connection(self):
        """Test API connection"""
        print("🔌 Testing xAI API connection...")
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": "Say 'API connection successful' if you can read this."
                }
            ],
            "model": self.models["grok-4"],
            "stream": False,
            "temperature": 0
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                message = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                print(f"✅ xAI API connection SUCCESSFUL!")
                print(f"   Model: {data.get('model', 'N/A')}")
                print(f"   Response: {message}")
                print(f"   Tokens used: {data.get('usage', {}).get('total_tokens', 0)}")
                
                return True
            else:
                print(f"❌ API connection failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ API request failed: {e}")
            return False
    
    def generate_social_media_post(self, topic, platform="twitter", tone="professional"):
        """Generate social media post for specific platform"""
        print(f"📝 Generating {platform} post about: {topic}")
        
        platform_prompts = {
            "twitter": "Create a Twitter/X post (280 characters max) that is engaging and includes relevant hashtags.",
            "instagram": "Create an Instagram caption (2-3 sentences) with emojis and relevant hashtags for a business audience.",
            "facebook": "Create a Facebook post (1-2 paragraphs) for a business page, professional but engaging.",
            "linkedin": "Create a LinkedIn post (professional tone) that provides value to business professionals."
        }
        
        tone_prompts = {
            "professional": "Use a professional, business-appropriate tone.",
            "casual": "Use a casual, conversational tone.",
            "enthusiastic": "Use an enthusiastic, energetic tone.",
            "educational": "Use an educational, informative tone."
        }
        
        prompt = f"""
        {platform_prompts.get(platform, "Create a social media post")}
        {tone_prompts.get(tone, "Use a professional tone.")}
        
        Topic: {topic}
        
        Requirements:
        1. Include 3-5 relevant hashtags
        2. Add appropriate emojis if suitable for the platform
        3. Include a call-to-action if appropriate
        4. Keep it engaging and shareable
        
        Format your response as:
        POST: [the post content]
        HASHTAGS: [comma-separated hashtags]
        PLATFORM: {platform}
        TONE: {tone}
        """
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert social media content creator specializing in business and marketing content."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": self.models["grok-4"],
            "stream": False,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                # Parse the response
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
                
                print(f"✅ Post generated successfully!")
                print(f"   Platform: {platform}")
                print(f"   Tone: {tone}")
                print(f"   Hashtags: {', '.join(hashtags[:3])}")
                
                return {
                    "platform": platform,
                    "topic": topic,
                    "content": post_content,
                    "hashtags": hashtags,
                    "tone": tone,
                    "model": data.get("model", "grok-4"),
                    "tokens_used": data.get("usage", {}).get("total_tokens", 0),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                print(f"❌ Post generation failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ API request failed: {e}")
            return None
    
    def generate_content_calendar(self, topics, days=7):
        """Generate a 7-day content calendar"""
        print(f"📅 Generating {days}-day content calendar...")
        
        prompt = f"""
        Create a {days}-day social media content calendar for a business focused on: {', '.join(topics)}
        
        For each day, provide:
        1. Main theme/topic
        2. Platform-specific posts (Twitter, Instagram, LinkedIn)
        3. Hashtag strategy
        4. Key messaging points
        
        Format as a structured JSON that I can parse programmatically.
        """
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a social media strategist and content planner. Always respond with valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": self.models["grok-4"],
            "stream": False,
            "temperature": 0.5,
            "response_format": {"type": "json_object"}
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=45
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                try:
                    calendar_data = json.loads(content)
                    print(f"✅ Content calendar generated!")
                    print(f"   Days: {days}")
                    print(f"   Topics: {len(topics)}")
                    
                    return {
                        "calendar": calendar_data,
                        "topics": topics,
                        "days": days,
                        "model": data.get("model", "grok-4"),
                        "tokens_used": data.get("usage", {}).get("total_tokens", 0),
                        "timestamp": datetime.now().isoformat()
                    }
                except json.JSONDecodeError:
                    print("❌ Failed to parse JSON response")
                    return None
            else:
                print(f"❌ Calendar generation failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ API request failed: {e}")
            return None
    
    def analyze_competitor_content(self, competitor_info, platform="twitter"):
        """Analyze competitor content strategy"""
        print(f"🎯 Analyzing competitor content for {platform}...")
        
        prompt = f"""
        Analyze the social media content strategy for a competitor in the business/marketing space.
        
        Competitor info: {competitor_info}
        Platform: {platform}
        
        Provide analysis covering:
        1. Content themes and topics
        2. Posting frequency and timing
        3. Engagement strategies
        4. Hashtag usage
        5. Content formats (text, images, videos, etc.)
        6. Recommendations for improvement
        
        Format as structured JSON analysis.
        """
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a competitive intelligence analyst specializing in social media strategy. Always respond with valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": self.models["grok-4"],
            "stream": False,
            "temperature": 0.3,
            "response_format": {"type": "json_object"}
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=45
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                try:
                    analysis = json.loads(content)
                    print(f"✅ Competitor analysis complete!")
                    
                    return {
                        "analysis": analysis,
                        "competitor": competitor_info,
                        "platform": platform,
                        "model": data.get("model", "grok-4"),
                        "tokens_used": data.get("usage", {}).get("total_tokens", 0),
                        "timestamp": datetime.now().isoformat()
                    }
                except json.JSONDecodeError:
                    print("❌ Failed to parse JSON response")
                    return None
            else:
                print(f"❌ Analysis failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ API request failed: {e}")
            return None
    
    def generate_hashtag_strategy(self, topic, platform="twitter"):
        """Generate hashtag strategy for a topic"""
        print(f"🏷️ Generating hashtag strategy for: {topic}")
        
        prompt = f"""
        Create a comprehensive hashtag strategy for social media posts about: {topic}
        
        Platform: {platform}
        
        Include:
        1. Primary hashtags (3-5 most relevant)
        2. Secondary hashtags (5-7 related topics)
        3. Trending hashtags (3-5 currently popular)
        4. Niche hashtags (3-5 specific to sub-topics)
        5. Branded hashtag suggestions (2-3)
        
        Format as structured JSON.
        """
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a social media marketing expert specializing in hashtag strategy. Always respond with valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": self.models["grok-2"],
            "stream": False,
            "temperature": 0.5,
            "response_format": {"type": "json_object"}
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                try:
                    strategy = json.loads(content)
                    print(f"✅ Hashtag strategy generated!")
                    
                    return {
                        "strategy": strategy,
                        "topic": topic,
                        "platform": platform,
                        "model": data.get("model", "grok-2"),
                        "tokens_used": data.get("usage", {}).get("total_tokens", 0),
                        "timestamp": datetime.now().isoformat()
                    }
                except json.JSONDecodeError:
                    print("❌ Failed to parse JSON response")
                    return None
            else:
                print(f"❌ Strategy generation failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ API request failed: {e}")
            return None
    
    def save_results(self, data, filename_prefix):
        """Save results to file"""
        results_dir = "/Users/cubiczan/.openclaw/workspace/results/xai"
        os.makedirs(results_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.json"
        filepath = os.path.join(results_dir, filename)
        
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        
        print(f"📁 Results saved to: {filepath}")
        return filepath

def main():
    """Main function"""
    print("🚀 xAI (Grok) Integration for Social Media Content")
    print("="*60)
    
    # API Key from user
    api_key = "xai-vzGa7b1VR6o5vLXxKqL69u8iIMWvACT2P8gmt5mrh4wMWqJvnPlZp4B6RK8hum5HHHnfM2g9wKvFkr1t"
    
    # Initialize
    xai = XAIIntegration(api_key)
    
    # Test connection
    if not xai.test_connection():
        print("❌ Cannot proceed without API connection")
        return
    
    print("\n" + "="*60)
    print("📋 CONTENT CREATION OPTIONS")
    print("="*60)
    
    print("\n1. Generate social media post")
    print("2. Generate content calendar (7 days)")
    print("3. Analyze competitor content")
    print("4. Generate hashtag strategy")
    print("5. Run complete workflow")
    print("6. Exit")
    
    choice = input("\nSelect option (1-6): ")
    
    business_topics = [
        "lead generation automation",
        "AI-powered marketing",
        "business growth strategies",
        "social media for SMBs",
        "content marketing ROI"
    ]
    
    if choice == "1":
        topic = input("Enter topic: ") or business_topics[0]
        platform = input("Platform (twitter/instagram/facebook/linkedin): ") or "twitter"
        tone = input("Tone (professional/casual/enthusiastic/educational): ") or "professional"
        
        post = xai.generate_social_media_post(topic, platform, tone)
        if post:
            xai.save_results(post, "social_media_post")
    
    elif choice == "2":
        print(f"Using topics: {', '.join(business_topics[:3])}")
        calendar = xai.generate_content_calendar(business_topics[:3], days=7)
        if calendar:
            xai.save_results(calendar, "content_calendar")
    
    elif choice == "3":
        competitor = input("Enter competitor name/description: ") or "Neil Patel (digital marketing influencer)"
        platform = input("Platform: ") or "twitter"
        
        analysis = xai.analyze_competitor_content(competitor, platform)
        if analysis:
            xai.save_results(analysis, "competitor_analysis")
    
    elif choice == "4":
        topic = input("Enter topic: ") or business_topics[0]
        platform = input("Platform: ") or "twitter"
        
        strategy = xai.generate_hashtag_strategy(topic, platform)
        if strategy:
            xai.save_results(strategy, "hashtag_strategy")
    
    elif choice == "5":
        print("\n" + "="*60)
        print("🚀 RUNNING COMPLETE CONTENT WORKFLOW")
        print("="*60)
        
        # 1. Generate content calendar
        print("\n1. 📅 Generating 7-day content calendar...")
        calendar = xai.generate_content_calendar(business_topics[:3], days=7)
        if calendar:
            xai.save_results(calendar, "complete_workflow_calendar")
        
        # 2. Generate posts for each day
        print("\n2. 📝 Generating sample posts...")
        sample_posts = []
        
        for i, topic in enumerate(business_topics[:2], 1):
            print(f"   Generating post {i}/2: {topic}")
            post = xai.generate_social_media_post(topic, "twitter", "professional")
            if post:
                sample_posts.append(post)
            # Don't overwhelm the API
            import time
            if i < 2:
                time.sleep(1)
        
        if sample_posts:
            xai.save_results({"posts": sample_posts}, "complete_workflow_posts")
        
        # 3. Generate hashtag strategy
        print("\n3. 🏷️ Generating hashtag strategy...")
        strategy = xai.generate_hashtag_strategy(business_topics[0], "twitter")
        if strategy:
            xai.save_results(strategy, "complete_workflow_hashtags")
        
        print("\n" + "="*60)
        print("🎯 COMPLETE WORKFLOW FINISHED!")
        print("="*60)
        print(f"\n✅ Generated: 7-day content calendar")
        print(f"✅ Generated: {len(sample_posts)} sample posts")
        print(f"✅ Generated: Has