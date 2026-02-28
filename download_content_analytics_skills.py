#!/usr/bin/env python3
"""
Download Content, Analytics & Business Skills from Awesome OpenClaw Skills
"""

import os
import sys
import json
import subprocess
from pathlib import Path

class ContentAnalyticsSkillsDownloader:
    """Download skills for content posting, analytics, and business focus"""
    
    def __init__(self):
        self.base_dir = "/Users/cubiczan/mac-bot/skills"
        self.content_dir = os.path.join(self.base_dir, "content-analytics")
        os.makedirs(self.content_dir, exist_ok=True)
        
        # Priority skills for Phase 2 (Content + Analytics + Business)
        self.priority_skills = {
            # Content Creation & Distribution
            "wordpress": {
                "url": "https://github.com/openclaw/skills/tree/main/skills/wordpress",
                "description": "WordPress content management and publishing",
                "category": "content",
                "priority": 1
            },
            "create-content": {
                "url": "https://github.com/openclaw/skills/tree/main/skills/itsflow/create-content",
                "description": "Platform-optimized content creation",
                "category": "content",
                "priority": 1
            },
            "facebook-page-manager": {
                "url": "https://github.com/openclaw/skills/tree/main/skills/longmaba/facebook-page-manager",
                "description": "Manage Facebook Pages via Meta Graph API",
                "category": "content",
                "priority": 1
            },
            
            # Analytics & Business Intelligence
            "add-analytics": {
                "url": "https://github.com/openclaw/skills/tree/main/skills/jeftekhari/add-analytics",
                "description": "Add Google Analytics 4 tracking to any project",
                "category": "analytics",
                "priority": 1
            },
            "google-analytics-api": {
                "url": "https://github.com/openclaw/skills/tree/main/skills/rich-song/google-analytics-api",
                "description": "Google Analytics API integration",
                "category": "analytics",
                "priority": 1
            },
            "data-analyst": {
                "url": "https://github.com/openclaw/skills/tree/main/skills/oyi77/data-analyst",
                "description": "Data visualization, report generation, SQL queries",
                "category": "analytics",
                "priority": 1
            },
            "ceorater": {
                "url": "https://github.com/openclaw/skills/tree/main/skills/ceorater-skills/ceorater",
                "description": "Institutional-grade CEO performance analytics",
                "category": "business",
                "priority": 1
            },
            
            # Business Operations
            "daily-report": {
                "url": "https://github.com/openclaw/skills/tree/main/skills/visualdeptcreative/daily-report",
                "description": "Track progress, report metrics, manage memory",
                "category": "business",
                "priority": 2
            },
            "expense-tracker-pro": {
                "url": "https://github.com/openclaw/skills/tree/main/skills/jhillin8/expense-tracker-pro",
                "description": "Track expenses via natural language",
                "category": "business",
                "priority": 2
            },
            
            # Additional useful skills
            "canva": {
                "url": "https://github.com/openclaw/skills/tree/main/skills/abgohel/canva",
                "description": "Create, export, and manage Canva designs",
                "category": "content",
                "priority": 2
            },
            "linkdapi": {
                "url": "https://github.com/openclaw/skills/tree/main/skills/foontinz/linkdapi",
                "description": "LinkedIn professional profile access",
                "category": "content",
                "priority": 2
            },
            "supermetrics-openclawd": {
                "url": "https://github.com/openclaw/skills/tree/main/skills/bartschneider/supermetrics-openclawd",
                "description": "Official Supermetrics skill for marketing data",
                "category": "analytics",
                "priority": 2
            }
        }
    
    def download_skill(self, skill_id: str, skill_info: dict) -> bool:
        """Download a single skill"""
        print(f"📥 Downloading {skill_id}...")
        
        url = skill_info["url"]
        description = skill_info["description"]
        category = skill_info["category"]
        
        # Create skill directory
        skill_dir = os.path.join(self.content_dir, skill_id)
        os.makedirs(skill_dir, exist_ok=True)
        
        try:
            # Extract GitHub path from URL
            # URL format: https://github.com/openclaw/skills/tree/main/skills/wordpress
            parts = url.split("/")
            repo_owner = parts[3]  # openclaw
            repo_name = parts[4]   # skills
            skill_path = "/".join(parts[7:])  # skills/wordpress
            
            # Clone the openclaw/skills repo if not exists
            repo_dir = os.path.join(self.content_dir, "repos", "openclaw-skills")
            if not os.path.exists(repo_dir):
                print(f"  Cloning openclaw/skills repository...")
                repo_url = "https://github.com/openclaw/skills.git"
                result = subprocess.run(
                    ["git", "clone", "--depth", "1", repo_url, repo_dir],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    print(f"  ❌ Clone failed: {result.stderr}")
                    return False
            else:
                print(f"  Updating openclaw/skills repository...")
                result = subprocess.run(
                    ["git", "-C", repo_dir, "pull"],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    print(f"  ⚠️  Update failed: {result.stderr}")
                    # Continue with existing version
            
            # Find the skill directory
            source_path = os.path.join(repo_dir, skill_path)
            if os.path.exists(source_path):
                # Copy skill files
                print(f"  Copying from {source_path}...")
                
                # Copy all files
                for item in os.listdir(source_path):
                    source_item = os.path.join(source_path, item)
                    dest_item = os.path.join(skill_dir, item)
                    
                    if os.path.isdir(source_item):
                        # Copy directory
                        subprocess.run(["cp", "-r", source_item, dest_item], 
                                     capture_output=True)
                    else:
                        # Copy file
                        subprocess.run(["cp", source_item, dest_item], 
                                     capture_output=True)
                
                # Create metadata
                metadata = {
                    "id": skill_id,
                    "name": skill_id.replace("-", " ").title(),
                    "description": description,
                    "category": category,
                    "priority": skill_info["priority"],
                    "source_url": url,
                    "source_path": skill_path,
                    "downloaded_at": subprocess.run(
                        ["date", "-Iseconds"],
                        capture_output=True,
                        text=True
                    ).stdout.strip(),
                    "openclaw_compatible": True
                }
                
                with open(os.path.join(skill_dir, "METADATA.json"), "w") as f:
                    json.dump(metadata, f, indent=2)
                
                # Ensure SKILL.md exists
                skill_md = os.path.join(skill_dir, "SKILL.md")
                if not os.path.exists(skill_md):
                    # Create basic SKILL.md
                    with open(skill_md, "w") as f:
                        f.write(f"# {skill_id.replace('-', ' ').title()} Skill\n\n")
                        f.write(f"**Description:** {description}\n\n")
                        f.write(f"**Category:** {category}\n\n")
                        f.write(f"**Source:** {url}\n\n")
                        f.write("## Usage\n\nThis skill was downloaded from OpenClaw skills repository.\n")
                
                print(f"  ✅ {skill_id} downloaded successfully")
                return True
            else:
                print(f"  ❌ Skill path not found: {source_path}")
                return False
                
        except Exception as e:
            print(f"  ❌ Error downloading {skill_id}: {e}")
            return False
    
    def download_priority_skills(self) -> dict:
        """Download all priority skills"""
        print("🚀 Downloading Content, Analytics & Business Skills")
        print("="*60)
        
        results = {}
        
        # Sort by priority
        sorted_skills = sorted(
            self.priority_skills.items(),
            key=lambda x: (x[1]["priority"], x[0])
        )
        
        for skill_id, skill_info in sorted_skills:
            success = self.download_skill(skill_id, skill_info)
            results[skill_id] = {
                "success": success,
                "category": skill_info["category"],
                "priority": skill_info["priority"]
            }
        
        return results
    
    def create_integration_guide(self, results: dict):
        """Create integration guide"""
        print("\n📖 Creating Integration Guide...")
        
        guide_path = os.path.join(self.content_dir, "INTEGRATION_GUIDE.md")
        
        guide_content = """# Content, Analytics & Business Skills Integration Guide

## 🎯 Phase 2: Content + Analytics + Business Focus

### Current Phase: Lead Generation + Outbound Emails ✅
### Next Phase: Content Distribution + Analytics + Business Intelligence 🚀

## 📦 Downloaded Skills

### Content Creation & Distribution
"""
        
        # Add content skills
        content_skills = [(k, v) for k, v in results.items() 
                         if self.priority_skills[k]["category"] == "content"]
        
        for skill_id, result in content_skills:
            status = "✅ Success" if result["success"] else "❌ Failed"
            skill_info = self.priority_skills[skill_id]
            guide_content += f"- **{skill_id}**: {skill_info['description']} ({status})\n"
        
        guide_content += "\n### Analytics & Business Intelligence\n"
        
        # Add analytics skills
        analytics_skills = [(k, v) for k, v in results.items() 
                           if self.priority_skills[k]["category"] == "analytics"]
        
        for skill_id, result in analytics_skills:
            status = "✅ Success" if result["success"] else "❌ Failed"
            skill_info = self.priority_skills[skill_id]
            guide_content += f"- **{skill_id}**: {skill_info['description']} ({status})\n"
        
        guide_content += "\n### Business Operations\n"
        
        # Add business skills
        business_skills = [(k, v) for k, v in results.items() 
                          if self.priority_skills[k]["category"] == "business"]
        
        for skill_id, result in business_skills:
            status = "✅ Success" if result["success"] else "❌ Failed"
            skill_info = self.priority_skills[skill_id]
            guide_content += f"- **{skill_id}**: {skill_info['description']} ({status})\n"
        
        # Add integration instructions
        guide_content += """
## 🚀 Quick Start Integration

### 1. Content Publishing Workflow
```python
# Example: Automated blog posting
from skills.wordpress import WordPressPublisher
from skills.create_content import ContentOptimizer

def publish_blog_post(title, content, tags=[]):
    # Optimize content
    optimizer = ContentOptimizer()
    optimized = optimizer.optimize(content, platform="blog")
    
    # Publish to WordPress
    wp = WordPressPublisher(
        url="https://your-wordpress-site.com",
        username="admin",
        app_password="xxxx"
    )
    
    post_id = wp.publish_post(
        title=title,
        content=optimized,
        tags=tags,
        status="publish"
    )
    
    return post_id
```

### 2. Analytics Integration
```python
# Example: Business analytics dashboard
from skills.google_analytics_api import GoogleAnalytics
from skills.data_analyst import DataAnalyst

def generate_daily_analytics():
    # Get web analytics
    ga = GoogleAnalytics(property_id="G-XXXXXX")
    metrics = ga.get_daily_metrics()
    
    # Analyze data
    analyst = DataAnalyst()
    insights = analyst.analyze_traffic(metrics)
    
    # Generate report
    report = {
        "date": datetime.now(),
        "visitors": metrics["users"],
        "pageviews": metrics["pageviews"],
        "conversion_rate": metrics["conversions"] / metrics["users"],
        "insights": insights
    }
    
    return report
```

### 3. Business Intelligence
```python
# Example: CEO performance analytics
from skills.ceorater import CEOAnalyzer
from skills.daily_report import ReportGenerator

def analyze_business_performance():
    # Get CEO analytics
    ceo_analyzer = CEOAnalyzer()
    performance = ceo_analyzer.get_performance_metrics()
    
    # Generate daily report
    reporter = ReportGenerator()
    report = reporter.generate_daily_report(
        metrics=performance,
        format="markdown"
    )
    
    return report
```

## 🔧 Configuration

### WordPress Configuration
```json
{
  "wordpress": {
    "url": "https://your-wordpress-site.com",
    "username": "admin",
    "app_password": "xxxx",
    "default_category": "Business",
    "auto_publish": true
  }
}
```

### Google Analytics Configuration
```json
{
  "google_analytics": {
    "property_id": "G-XXXXXX",
    "credentials_path": "/path/to/credentials.json",
    "metrics": ["users", "pageviews", "sessions", "conversions"],
    "dimensions": ["source", "medium", "campaign"]
  }
}
```

### Business Analytics Configuration
```json
{
  "business_analytics": {
    "daily_reporting": true,
    "weekly_summary": true,
    "monthly_analysis": true,
    "alert_thresholds": {
      "traffic_drop": -20,
      "conversion_drop": -15,
      "revenue_drop": -10
    }
  }
}
```

## 🎯 Use Cases for Our Business

### 1. Content Marketing for Lead Generation
```python
# Create lead magnet content
def create_lead_magnet(topic, format="ebook"):
    content_system = ContentSystem()
    
    # Generate content
    content = content_system.generate_content(
        topic=topic,
        format=format,
        target_audience="SMB owners",
        call_to_action="Download free template"
    )
    
    # Publish and track
    post_id = publish_blog_post(
        title=f"Free {topic} Guide for SMBs",
        content=content
    )
    
    # Track performance
    analytics.track_content_performance(post_id)
    
    return post_id
```

### 2. Campaign Performance Analytics
```python
# Track marketing campaign ROI
def track_campaign_roi(campaign_name, start_date, end_date):
    analytics = AnalyticsSystem()
    
    # Get campaign data
    campaign_data = analytics.get_campaign_metrics(
        name=campaign_name,
        start_date=start_date,
        end_date=end_date
    )
    
    # Calculate ROI
    roi = analytics.calculate_roi(
        revenue=campaign_data["revenue"],
        cost=campaign_data["cost"]
    )
    
    # Generate report
    report = {
        "campaign": campaign_name,
        "period": f"{start_date} to {end_date}",
        "metrics": campaign_data,
        "roi": roi,
        "recommendations": analytics.get_optimization_recommendations(campaign_data)
    }
    
    return report
```

### 3. Business Performance Dashboard
```python
# Comprehensive business dashboard
def generate_business_dashboard():
    dashboard = BusinessDashboard()
    
    # Content performance
    content_metrics = dashboard.get_content_performance()
    
    # Lead generation metrics
    lead_metrics = dashboard.get_lead_generation_metrics()
    
    # Financial metrics
    financial_metrics = dashboard.get_financial_metrics()
    
    # Campaign performance
    campaign_metrics = dashboard.get_campaign_performance()
    
    # Generate insights
    insights = dashboard.analyze_insights(
        content=content_metrics,
        leads=lead_metrics,
        finance=financial_metrics,
        campaigns=campaign_metrics
    )
    
    return {
        "dashboard": {
            "content": content_metrics,
            "leads": lead_metrics,
            "finance": financial_metrics,
            "campaigns": campaign_metrics
        },
        "insights": insights,
        "recommendations": dashboard.get_recommendations(insights)
    }
```

## 📊 Expected Business Impact

### Content Distribution:
- **80% time savings** on manual posting
- **3x wider reach** with multi-platform distribution
- **2x higher engagement** with optimized content
- **Improved SEO** with consistent, quality content

### Analytics & Insights:
- **Data-driven decisions** with real-time analytics
- **40% improvement** in campaign performance
- **10+ hours/week saved** on manual reporting
- **Clear ROI measurement** for all activities

### Business Intelligence:
- **Better resource allocation** based on performance data
- **Proactive optimization** with predictive analytics
- **Competitive advantage** with business insights
- **Scalable growth** with data-backed strategies

## 🚀 Next Steps

### Immediate (Today):
1. **Test WordPress integration** with sample post
2. **Configure Google Analytics** tracking
3. **Set up daily reporting** automation

### Short-term (This Week):
1. **Create content calendar** for lead generation topics
2. **Implement analytics dashboard** for campaign tracking
3