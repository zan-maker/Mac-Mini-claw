#!/usr/bin/env python3
"""
Finance-Focused LinkedIn Content Generator
AI + Finance Education → Fractional CFO Leads
"""

import os
import json
from datetime import datetime, timedelta
from unified_ai_generator import UnifiedAIGenerator

class FinanceLinkedInGenerator:
    """Generate finance-focused LinkedIn content for fractional CFO leads"""
    
    def __init__(self):
        self.workspace = "/Users/cubiczan/.openclaw/workspace"
        self.ai_generator = UnifiedAIGenerator()
        
        # Finance/AI content pillars
        self.content_pillars = [
            "AI + Finance Integration",
            "Fractional CFO Value",
            "Financial Education",
            "Industry Insights"
        ]
        
        # Target audience
        self.target_audience = [
            "SMB Owners ($1M-$10M revenue)",
            "Startup Founders (Series A-B)",
            "Finance Professionals",
            "Business Leaders"
        ]
        
        # Hashtag bank
        self.hashtags = {
            "primary": ["#FractionalCFO", "#FinanceAI", "#FinancialAutomation", "#SMBFinance", "#CashFlowManagement"],
            "secondary": ["#AIinFinance", "#FinancialPlanning", "#BusinessGrowth", "#FinTech", "#AccountingAutomation"],
            "industry": ["#CFO", "#FinancialController", "#StartupFinance", "#FinancialStrategy", "#BusinessIntelligence"]
        }
        
        print("🏦 Finance-Focused LinkedIn Content Generator")
        print("="*60)
        print("🎯 Target: Fractional CFO Lead Generation")
        print("🤖 AI: Google Gemini (Primary) + xAI (Backup)")
        print("📊 Focus: AI + Finance Education")
        print("="*60)
    
    def generate_finance_post(self, pillar: str = None, topic: str = None) -> dict:
        """Generate finance-focused LinkedIn post"""
        print(f"📝 Generating finance LinkedIn post...")
        
        if not pillar:
            pillar = self.content_pillars[0]
        
        if not topic:
            # Generate topic based on pillar
            topic_prompt = f"Suggest a specific topic about {pillar} for LinkedIn"
            topic_result = self.ai_generator.generate_content(topic_prompt)
            topic = topic_result.get("content", "AI in Financial Automation").strip()[:100]
        
        # Create detailed prompt for finance content
        prompt = f"""
        Create a LinkedIn post for finance professionals about: {topic}
        
        Target Audience: {', '.join(self.target_audience[:2])}
        Content Pillar: {pillar}
        Goal: Attract fractional CFO clients through education
        
        Requirements:
        1. Professional, educational tone
        2. Demonstrate expertise in finance + AI
        3. Include practical, actionable advice
        4. Add 3-5 relevant hashtags from: {', '.join(self.hashtags['primary'])}
        5. Include a subtle call-to-action for fractional CFO services
        6. Length: 2-3 paragraphs (250-400 words)
        
        Format as:
        TITLE: [Catchy title]
        CONTENT: [The post content]
        HASHTAGS: [comma-separated hashtags]
        CTA: [Call-to-action]
        """
        
        print(f"   Pillar: {pillar}")
        print(f"   Topic: {topic}")
        
        result = self.ai_generator.generate_content(prompt, "linkedin_finance_post")
        
        if result["success"]:
            # Parse the response
            content = result["content"]
            parsed = self._parse_post_content(content)
            
            parsed.update({
                "pillar": pillar,
                "topic": topic,
                "target_audience": self.target_audience[:2],
                "service_used": result["service"],
                "tokens_used": result.get("total_tokens", 0)
            })
            
            result["parsed"] = parsed
            
            print(f"✅ Generated with {result['service'].upper()}")
            print(f"   Tokens: {result.get('total_tokens', 0)}")
        
        return result
    
    def generate_content_calendar(self, days: int = 7) -> dict:
        """Generate 7-day finance content calendar"""
        print(f"📅 Generating {days}-day finance content calendar...")
        
        prompt = f"""
        Create a {days}-day LinkedIn content calendar for a fractional CFO focusing on AI + finance.
        
        Daily Themes:
        - Monday: Educational (financial concepts)
        - Tuesday: AI Focus (tools/applications)
        - Wednesday: Interactive (questions/polls)
        - Thursday: Case Study (client success)
        - Friday: Industry News (trends/updates)
        - Saturday: Quick Tip (actionable advice)
        - Sunday: Planning (thought leadership)
        
        Requirements for each day:
        1. Specific topic related to finance + AI
        2. Target audience: SMB owners and finance professionals
        3. Goal: Lead generation for fractional CFO services
        4. Include 3-5 relevant hashtags
        5. Suggested posting time (EST)
        
        Format as structured content that can be parsed.
        """
        
        result = self.ai_generator.generate_content(prompt, "finance_content_calendar")
        
        if result["success"]:
            result["metadata"] = {
                "days": days,
                "themes": ["Educational", "AI Focus", "Interactive", "Case Study", "Industry News", "Quick Tip", "Planning"],
                "service_used": result["service"]
            }
        
        return result
    
    def generate_lead_magnet(self, type: str = "guide") -> dict:
        """Generate lead magnet ideas for fractional CFO services"""
        print(f"🎯 Generating {type} lead magnet idea...")
        
        lead_magnets = {
            "guide": "AI Finance Tools Checklist",
            "template": "Monthly Financial Dashboard Template",
            "calculator": "Cash Flow Projection Tool",
            "webinar": "AI for Fractional CFOs Masterclass"
        }
        
        magnet_name = lead_magnets.get(type, "AI Finance Tools Checklist")
        
        prompt = f"""
        Create a lead magnet offer for fractional CFO services: {magnet_name}
        
        Target: SMB owners interested in AI-powered finance
        Goal: Capture email leads for fractional CFO consultations
        
        Include:
        1. Compelling title and description
        2. 3-5 key benefits/features
        3. Target audience pain points it solves
        4. Call-to-action for download
        5. Suggested landing page copy
        
        Format as structured content.
        """
        
        result = self.ai_generator.generate_content(prompt, f"lead_magnet_{type}")
        
        if result["success"]:
            result["metadata"] = {
                "type": type,
                "name": magnet_name,
                "purpose": "Email capture for fractional CFO leads",
                "service_used": result["service"]
            }
        
        return result
    
    def generate_case_study(self) -> dict:
        """Generate anonymized client case study"""
        print("📊 Generating client case study...")
        
        prompt = """
        Create an anonymized client case study for fractional CFO services.
        
        Scenario: SMB struggling with cash flow management
        Solution: Implemented AI-powered financial systems
        Results: Improved cash flow, reduced costs, enabled growth
        
        Include:
        1. Client background (industry, size, challenges)
        2. Specific problems faced (cash flow, reporting, planning)
        3. Solutions implemented (AI tools, processes, systems)
        4. Measurable results (percentage improvements, cost savings)
        5. Client testimonial (anonymized)
        6. Key takeaways for other SMBs
        
        Format as LinkedIn post content (professional tone).
        """
        
        result = self.ai_generator.generate_content(prompt, "finance_case_study")
        
        if result["success"]:
            result["metadata"] = {
                "type": "case_study",
                "purpose": "Social proof for fractional CFO services",
                "anonymized": True,
                "service_used": result["service"]
            }
        
        return result
    
    def _parse_post_content(self, content: str) -> dict:
        """Parse AI-generated post content"""
        parsed = {
            "title": "",
            "content": "",
            "hashtags": [],
            "cta": ""
        }
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("TITLE:"):
                parsed["title"] = line.replace("TITLE:", "").strip()
            elif line.startswith("CONTENT:"):
                parsed["content"] = line.replace("CONTENT:", "").strip()
                current_section = "content"
            elif line.startswith("HASHTAGS:"):
                hashtags_str = line.replace("HASHTAGS:", "").strip()
                parsed["hashtags"] = [tag.strip() for tag in hashtags_str.split(',')]
            elif line.startswith("CTA:"):
                parsed["cta"] = line.replace("CTA:", "").strip()
            elif current_section == "content" and line:
                # Continue content section
                parsed["content"] += "\n" + line
        
        # If parsing failed, use the raw content
        if not parsed["content"]:
            parsed["content"] = content.strip()
        
        # Ensure we have hashtags
        if not parsed["hashtags"]:
            parsed["hashtags"] = self.hashtags["primary"][:3]
        
        return parsed
    
    def save_content(self, result: dict, content_type: str):
        """Save generated content to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"finance_{content_type}_{timestamp}.json"
        filepath = os.path.join(self.workspace, "results", "finance_content", filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, "w") as f:
            json.dump(result, f, indent=2)
        
        print(f"💾 Content saved: {filepath}")
        return filepath

def main():
    """Main function"""
    print("🏦 Finance-Focused LinkedIn Content Generator")
    print("="*60)
    
    # Initialize generator
    generator = FinanceLinkedInGenerator()
    
    print("\n🎯 CONTENT OPTIONS:")
    print("="*60)
    print("1. Generate finance LinkedIn post")
    print("2. Generate 7-day content calendar")
    print("3. Generate lead magnet idea")
    print("4. Generate client case study")
    print("5. Test all content types")
    print("6. Exit")
    
    choice = input("\nSelect option (1-6): ")
    
    if choice == "1":
        print("\n📊 Content Pillars:")
        for i, pillar in enumerate(generator.content_pillars, 1):
            print(f"   {i}. {pillar}")
        
        pillar_choice = input("\nSelect pillar (1-4, or Enter for AI+Finance): ")
        pillar = None
        
        if pillar_choice and pillar_choice.isdigit():
            idx = int(pillar_choice) - 1
            if 0 <= idx < len(generator.content_pillars):
                pillar = generator.content_pillars[idx]
        
        topic = input("Specific topic (or Enter for AI suggestion): ").strip()
        
        result = generator.generate_finance_post(pillar, topic or None)
        
        if result["success"] and "parsed" in result:
            parsed = result["parsed"]
            print(f"\n✅ Generated with {result['service'].upper()}")
            print(f"\n📝 Title: {parsed['title']}")
            print(f"\n📋 Content:")
            print(f"{parsed['content'][:500]}...")
            print(f"\n🏷️ Hashtags: {', '.join(parsed['hashtags'])}")
            print(f"\n🎯 CTA: {parsed['cta'][:100]}...")
            
            # Save content
            generator.save_content(result, "linkedin_post")
    
    elif choice == "2":
        result = generator.generate_content_calendar(7)
        
        if result["success"]:
            print(f"\n✅ Generated with {result['service'].upper()}")
            print(f"\n📅 {result['metadata']['days']}-Day Content Calendar")
            print(f"\n📋 Preview:")
            print(f"{result['content'][:800]}...")
            
            generator.save_content(result, "content_calendar")
    
    elif choice == "3":
        print("\n🎯 Lead Magnet Types:")
        print("   1. Guide (AI Finance Tools Checklist)")
        print("   2. Template (Financial Dashboard)")
        print("   3. Calculator (Cash Flow Projection)")
        print("   4. Webinar (AI for CFOs)")
        
        type_choice = input("\nSelect type (1-4): ")
        type_map = {"1": "guide", "2": "template", "3": "calculator", "4": "webinar"}
        
        magnet_type = type_map.get(type_choice, "guide")
        result = generator.generate_lead_magnet(magnet_type)
        
        if result["success"]:
            print(f"\n✅ Generated with {result['service'].upper()}")
            print(f"\n🎯 Lead Magnet: {result['metadata']['name']}")
            print(f"\n📋 Preview:")
            print(f"{result['content'][:600]}...")
            
            generator.save_content(result, f"lead_magnet_{magnet_type}")
    
    elif choice == "4":
        result = generator.generate_case_study()
        
        if result["success"]:
            print(f"\n✅ Generated with {result['service'].upper()}")
            print(f"\n📊 Client Case Study (Anonymized)")
            print(f"\n📋 Preview:")
            print(f"{result['content'][:800]}...")
            
            generator.save_content(result, "case_study")
    
    elif choice == "5":
        print("\n🧪 Testing all content types...")
        
        # Test post
        print("\n1. Testing LinkedIn post...")
        post_result = generator.generate_finance_post()
        if post_result["success"]:
            print(f"   ✅ Post: SUCCESS ({post_result['service']})")
        
        # Test calendar
        print("\n2. Testing content calendar...")
        calendar_result = generator.generate_content_calendar(3)  # 3 days for test
        if calendar_result["success"]:
            print(f"   ✅ Calendar: SUCCESS ({calendar_result['service']})")
        
        # Test lead magnet
        print("\n3. Testing lead magnet...")
        magnet_result = generator.generate_lead_magnet("guide")
        if magnet_result["success"]:
            print(f"   ✅ Lead magnet: SUCCESS ({magnet_result['service']})")
        
        print("\n🎉 All tests completed!")
    
    elif choice == "6":
        print("Exiting...")
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()