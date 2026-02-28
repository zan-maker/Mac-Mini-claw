#!/usr/bin/env python3
"""
Complete X (Twitter) Integration System
- Content discovery
- Competitor analysis  
- Trend monitoring
- Integration with social media system
"""

import os
import json
import time
from datetime import datetime, timedelta
from x_api_integration import XAPIIntegration

class XCompleteSystem:
    """Complete X integration for business content strategy"""
    
    def __init__(self):
        self.config_path = "/Users/cubiczan/.openclaw/workspace/config/social_media_config.json"
        self.results_dir = "/Users/cubiczan/.openclaw/workspace/results/x_analytics"
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Load configuration
        self.config = self.load_config()
        self.bearer_token = self.get_bearer_token()
        
        if not self.bearer_token:
            print("❌ No Bearer Token configured")
            return
        
        # Initialize API
        self.x_api = XAPIIntegration(self.bearer_token)
        
        # Business focus areas
        self.business_topics = [
            "lead generation", "business automation", "AI agents",
            "marketing strategy", "SMB growth", "entrepreneurship",
            "digital marketing", "content strategy", "social media marketing",
            "startup funding", "business intelligence", "ROI optimization"
        ]
        
        # Competitors to monitor
        self.competitors = [
            "garyvee", "neilpatel", "hubspot", "marketingwizdom",
            "socialmedia2day", "marketingexamples", "copyhackers"
        ]
    
    def load_config(self):
        """Load configuration"""
        if not os.path.exists(self.config_path):
            print(f"❌ Config file not found: {self.config_path}")
            return {}
        
        with open(self.config_path, "r") as f:
            return json.load(f)
    
    def get_bearer_token(self):
        """Get Bearer Token from config"""
        return self.config.get("platforms", {}).get("twitter_x", {}).get("credentials", {}).get("bearer_token", "")
    
    def daily_content_discovery(self):
        """Daily content discovery for social media posting"""
        print("🔍 Daily Content Discovery")
        print("="*50)
        
        results = {
            "date": datetime.now().isoformat(),
            "trending_topics": [],
            "content_ideas": [],
            "competitor_insights": [],
            "recommended_posts": []
        }
        
        # 1. Get trending topics
        print("\n1. Finding trending topics...")
        trends = self.x_api.get_trending_topics(count=5)
        results["trending_topics"] = trends
        
        # 2. Generate content ideas
        print("\n2. Generating content ideas...")
        for topic in self.business_topics[:3]:  # Top 3 topics
            ideas = self.x_api.generate_content_ideas([topic], max_ideas=2)
            results["content_ideas"].extend(ideas)
            time.sleep(1)  # Rate limiting
        
        # 3. Analyze top competitor
        print("\n3. Analyzing competitors...")
        if self.competitors:
            competitor = self.competitors[0]
            analysis = self.x_api.analyze_competitor(competitor, max_tweets=10)
            if analysis:
                results["competitor_insights"].append(analysis)
        
        # 4. Generate recommended posts
        print("\n4. Generating recommended posts...")
        recommended_posts = self.generate_recommended_posts(results)
        results["recommended_posts"] = recommended_posts
        
        # Save results
        filename = f"content_discovery_{datetime.now().strftime('%Y%m%d')}.json"
        filepath = os.path.join(self.results_dir, filename)
        
        with open(filepath, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✅ Daily content discovery complete!")
        print(f"📁 Results saved to: {filepath}")
        
        # Print summary
        self.print_summary(results)
        
        return results
    
    def generate_recommended_posts(self, discovery_data):
        """Generate recommended social media posts"""
        print("   Creating post recommendations...")
        
        recommended_posts = []
        
        # From trending topics
        for trend in discovery_data.get("trending_topics", [])[:2]:
            post = {
                "platform": "twitter",
                "type": "trending_topic",
                "content": f"Interesting discussion on {trend['topic']}:\n\n{trend['sample_tweet']}\n\nWhat are your thoughts? #Business #Trending",
                "hashtags": ["#" + trend["topic"].replace(" ", ""), "#Trending", "#Business"],
                "engagement_estimate": trend.get("engagement", 0),
                "source": "trending_topic"
            }
            recommended_posts.append(post)
        
        # From content ideas
        for idea in discovery_data.get("content_ideas", [])[:2]:
            post = {
                "platform": "twitter",
                "type": "content_idea",
                "content": f"{idea['content_angle']} on {idea['topic']}:\n\nInspired by @{idea['author']}'s post on this topic. What's your approach?",
                "hashtags": idea["suggested_hashtags"],
                "engagement_estimate": idea.get("estimated_engagement", 0),
                "source": "content_idea"
            }
            recommended_posts.append(post)
        
        # Generic business posts
        generic_posts = [
            {
                "platform": "twitter",
                "type": "question",
                "content": "What's your biggest challenge with lead generation right now?\n\n#LeadGeneration #Business #Marketing",
                "hashtags": ["#LeadGeneration", "#Business", "#Marketing", "#Question"],
                "engagement_estimate": 50,
                "source": "generic"
            },
            {
                "platform": "twitter",
                "type": "tip",
                "content": "Tip: Automating lead qualification can save 10+ hours/week.\n\nWhat's your favorite automation tool?\n\n#Automation #BusinessTips #Productivity",
                "hashtags": ["#Automation", "#BusinessTips", "#Productivity", "#SMB"],
                "engagement_estimate": 75,
                "source": "generic"
            }
        ]
        
        recommended_posts.extend(generic_posts)
        
        return recommended_posts
    
    def print_summary(self, results):
        """Print summary of discovery results"""
        print("\n" + "="*50)
        print("📊 DAILY CONTENT DISCOVERY SUMMARY")
        print("="*50)
        
        print(f"\n📈 Trending Topics: {len(results.get('trending_topics', []))}")
        for i, trend in enumerate(results.get('trending_topics', [])[:3], 1):
            print(f"   {i}. {trend['topic'].title()} ({trend.get('engagement', 0)} engagement)")
        
        print(f"\n💡 Content Ideas: {len(results.get('content_ideas', []))}")
        for i, idea in enumerate(results.get('content_ideas', [])[:3], 1):
            print(f"   {i}. {idea['topic'].title()} - {idea['content_angle']}")
        
        print(f"\n🎯 Competitor Insights: {len(results.get('competitor_insights', []))}")
        for insight in results.get('competitor_insights', []):
            print(f"   @{insight.get('username', 'N/A')}: {insight.get('metrics', {}).get('avg_engagement', 0):.1f} avg engagement")
        
        print(f"\n🚀 Recommended Posts: {len(results.get('recommended_posts', []))}")
        for i, post in enumerate(results.get('recommended_posts', [])[:3], 1):
            print(f"   {i}. {post['type'].title()}: {post['content'][:80]}...")
        
        print("\n" + "="*50)
        print("🎯 READY FOR SOCIAL MEDIA POSTING!")
        print("="*50)
    
    def integrate_with_social_system(self):
        """Integrate with the social media posting system"""
        print("🔗 Integrating with Social Media System...")
        
        # Load social media config
        social_config_path = "/Users/cubiczan/.openclaw/workspace/config/social_media_config.json"
        
        if not os.path.exists(social_config_path):
            print("❌ Social media config not found")
            return False
        
        with open(social_config_path, "r") as f:
            social_config = json.load(f)
        
        # Update Twitter/X configuration with Bearer Token
        twitter_config = social_config.get("platforms", {}).get("twitter_x", {})
        
        if not twitter_config.get("enabled", False):
            print("⚠️  Twitter/X not enabled in social media config")
            print("Enabling Twitter/X for content discovery...")
            twitter_config["enabled"] = True
        
        # Ensure Bearer Token is in credentials
        if "bearer_token" not in twitter_config.get("credentials", {}):
            twitter_config.setdefault("credentials", {})["bearer_token"] = self.bearer_token
        
        # Save updated config
        social_config["platforms"]["twitter_x"] = twitter_config
        
        with open(social_config_path, "w") as f:
            json.dump(social_config, f, indent=2)
        
        print("✅ Twitter/X integrated with social media system")
        print("   Bearer Token: Configured")
        print("   Content discovery: Enabled")
        print("   Competitor analysis: Ready")
        
        return True
    
    def create_daily_schedule(self):
        """Create daily posting schedule"""
        print("📅 Creating Daily Posting Schedule...")
        
        schedule = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timezone": "EST",
            "posts": [
                {
                    "time": "09:00",
                    "platform": "twitter",
                    "type": "trending_topic",
                    "auto_generate": True,
                    "source": "daily_discovery"
                },
                {
                    "time": "12:00",
                    "platform": "twitter",
                    "type": "content_idea",
                    "auto_generate": True,
                    "source": "daily_discovery"
                },
                {
                    "time": "15:00",
                    "platform": "twitter",
                    "type": "question",
                    "auto_generate": True,
                    "source": "generic"
                },
                {
                    "time": "18:00",
                    "platform": "twitter",
                    "type": "tip",
                    "auto_generate": True,
                    "source": "generic"
                }
            ],
            "analytics_check": "17:00",
            "competitor_check": "10:00",
            "trend_check": "08:00"
        }
        
        # Save schedule
        schedule_file = os.path.join(self.results_dir, f"posting_schedule_{datetime.now().strftime('%Y%m%d')}.json")
        
        with open(schedule_file, "w") as f:
            json.dump(schedule, f, indent=2)
        
        print(f"✅ Daily schedule created")
        print(f"📁 Schedule saved to: {schedule_file}")
        
        # Print schedule
        print("\n📋 TODAY'S POSTING SCHEDULE:")
        print("-"*40)
        for post in schedule["posts"]:
            print(f"  {post['time']} - {post['platform'].title()}: {post['type'].replace('_', ' ').title()}")
        
        print(f"\n  Analytics check: {schedule['analytics_check']}")
        print(f"  Competitor check: {schedule['competitor_check']}")
        print(f"  Trend check: {schedule['trend_check']}")
        
        return schedule
    
    def run_complete_system(self):
        """Run the complete X integration system"""
        print("🚀 X (Twitter) Complete Integration System")
        print("="*60)
        
        # Check Bearer Token
        if not self.bearer_token:
            print("❌ Please configure Bearer Token first")
            print("\nEdit: /Users/cubiczan/.openclaw/workspace/config/social_media_config.json")
            print('''Add to "twitter_x" section:
"credentials": {
  "bearer_token": "AAAAAAAAAAAAAAAAAAAAALPN7QEAAAAAE%2FzdYiwIFUznOIq0AMuGfm9XiTQ%3DqG2GS41y1x6BScR90xrbkzrK3eOmijtefTzuJtrkfQgt2kkQxT"
}''')
            return
        
        print(f"✅ Bearer Token: Configured")
        print(f"✅ Business topics: {len(self.business_topics)}")
        print(f"✅ Competitors to monitor: {len(self.competitors)}")
        print("="*60)
        
        # Menu
        print("\n📋 X INTEGRATION OPTIONS:")
        print("1. Run daily content discovery")
        print("2. Integrate with social media system")
        print("3. Create daily posting schedule")
        print("4. Run complete workflow (all of the above)")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ")
        
        if choice == "1":
            self.daily_content_discovery()
        
        elif choice == "2":
            self.integrate_with_social_system()
        
        elif choice == "3":
            self.create_daily_schedule()
        
        elif choice == "4":
            print("\n" + "="*60)
            print("🚀 RUNNING COMPLETE WORKFLOW")
            print("="*60)
            
            # Step 1: Integrate with social system
            print("\n1. Integrating with social media system...")
            self.integrate_with_social_system()
            
            # Step 2: Daily content discovery
            print("\n2. Running daily content discovery...")
            discovery = self.daily_content_discovery()
            
            # Step 3: Create posting schedule
            print("\n3. Creating daily posting schedule...")
            schedule = self.create_daily_schedule()
            
            # Step 4: Summary
            print("\n" + "="*60)
            print("🎯 COMPLETE WORKFLOW FINISHED!")
            print("="*60)
            
            print(f"\n✅ Integrated: Twitter/X with social media system")
            print(f"✅ Discovered: {len(discovery.get('content_ideas', []))} content ideas")
            print(f"✅ Scheduled: {len(schedule.get('posts', []))} posts for today")
            print(f"✅ Saved: All results to {self.results_dir}")
            
            print("\n🚀 Ready for automated social media posting!")
        
        elif choice == "5":
            print("👋 Goodbye!")
            return
        
        else:
            print("❌ Invalid choice")

def main():
    """Main function"""
    system = XCompleteSystem()
    system.run_complete_system()

if __name__ == "__main__":
    main()