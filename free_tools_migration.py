#!/usr/bin/env python3
"""
Free Tools Migration Script
Migrate from paid services to free alternatives from free-for-dev
"""

import os
import json
import sys
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import subprocess
import requests

class ServiceCategory(Enum):
    """Categories of free services"""
    GENERATIVE_AI = "generative_ai"
    EMAIL = "email"
    CLOUD = "cloud"
    STORAGE = "storage"
    MONITORING = "monitoring"
    DATABASE = "database"
    CDN = "cdn"
    IMAGE_GEN = "image_generation"

@dataclass
class FreeService:
    """Free service from free-for-dev"""
    name: str
    category: ServiceCategory
    url: str
    free_tier: str
    use_case: str
    migration_priority: int  # 1-10, higher = more urgent
    estimated_savings: float  # Monthly savings in USD
    
    def to_dict(self) -> Dict:
        return asdict(self)

class FreeToolsMigrator:
    """Migrate from paid services to free alternatives"""
    
    def __init__(self):
        self.services = self.load_free_services()
        self.current_config = self.load_current_config()
        
    def load_free_services(self) -> List[FreeService]:
        """Load curated free services for AI agents"""
        return [
            # Generative AI
            FreeService(
                name="OpenRouter Free Models",
                category=ServiceCategory.GENERATIVE_AI,
                url="https://openrouter.ai/models?q=free",
                free_tier="DeepSeek R1, V3, Llama, Moonshot AI (rate limited)",
                use_case="Replace paid LLM APIs for routine tasks",
                migration_priority=9,
                estimated_savings=200.0
            ),
            FreeService(
                name="Mediaworkbench.ai",
                category=ServiceCategory.GENERATIVE_AI,
                url="https://mediaworkbench.ai",
                free_tier="100,000 free words for Azure OpenAI, DeepSeek, Google Gemini",
                use_case="Code generation, deep research, image creation",
                migration_priority=8,
                estimated_savings=150.0
            ),
            FreeService(
                name="Pollinations.AI",
                category=ServiceCategory.IMAGE_GEN,
                url="https://pollinations.ai/",
                free_tier="Free image generation API, no signup/keys required",
                use_case="Replace OpenAI DALL-E for AI finance visuals",
                migration_priority=9,
                estimated_savings=100.0
            ),
            FreeService(
                name="Langfuse",
                category=ServiceCategory.MONITORING,
                url="https://langfuse.com/",
                free_tier="50k observations/month, all platform features",
                use_case="LLM observability, debugging, prompt optimization",
                migration_priority=7,
                estimated_savings=50.0
            ),
            
            # Email Services
            FreeService(
                name="Brevo",
                category=ServiceCategory.EMAIL,
                url="https://www.brevo.com/",
                free_tier="9,000 emails/month, 300 emails/day",
                use_case="Replace AgentMail for outreach campaigns",
                migration_priority=10,
                estimated_savings=75.0
            ),
            FreeService(
                name="EmailOctopus",
                category=ServiceCategory.EMAIL,
                url="https://emailoctopus.com",
                free_tier="2,500 subscribers, 10,000 emails/month",
                use_case="Newsletter and campaign management",
                migration_priority=8,
                estimated_savings=50.0
            ),
            FreeService(
                name="ImprovMX",
                category=ServiceCategory.EMAIL,
                url="https://improvmx.com",
                free_tier="Free email forwarding for custom domains",
                use_case="Domain email aliases for testing",
                migration_priority=6,
                estimated_savings=20.0
            ),
            
            # Cloud Infrastructure
            FreeService(
                name="Google Cloud Firestore",
                category=ServiceCategory.DATABASE,
                url="https://cloud.google.com/firestore",
                free_tier="1GB storage, 50k reads/day, 20k writes/day",
                use_case="Replace Supabase for lead storage",
                migration_priority=8,
                estimated_savings=50.0
            ),
            FreeService(
                name="AWS Lambda",
                category=ServiceCategory.CLOUD,
                url="https://aws.amazon.com/lambda/",
                free_tier="1 million requests/month",
                use_case="Serverless functions for agent workflows",
                migration_priority=7,
                estimated_savings=30.0
            ),
            FreeService(
                name="Cloudflare R2",
                category=ServiceCategory.STORAGE,
                url="https://developers.cloudflare.com/r2/",
                free_tier="10GB/month, 1M operations/month",
                use_case="Image and file storage for AI agents",
                migration_priority=8,
                estimated_savings=25.0
            ),
            FreeService(
                name="Cloudflare Workers",
                category=ServiceCategory.CLOUD,
                url="https://developers.cloudflare.com/workers/",
                free_tier="100k requests/day",
                use_case="Edge computing for agent APIs",
                migration_priority=6,
                estimated_savings=20.0
            ),
        ]
    
    def load_current_config(self) -> Dict:
        """Load current paid service configuration"""
        config_path = "/Users/cubiczan/.openclaw/workspace/config/paid_services.json"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        
        # Default current config
        return {
            "email": {
                "provider": "AgentMail + Gmail SMTP",
                "monthly_cost": 100.0,
                "monthly_volume": 10000
            },
            "llm": {
                "provider": "DeepSeek API",
                "monthly_cost": 200.0,
                "monthly_tokens": 1000000
            },
            "image_generation": {
                "provider": "OpenAI DALL-E",
                "monthly_cost": 100.0,
                "monthly_images": 100
            },
            "database": {
                "provider": "Supabase",
                "monthly_cost": 50.0,
                "storage_gb": 1.0
            },
            "storage": {
                "provider": "Various",
                "monthly_cost": 30.0,
                "storage_gb": 5.0
            }
        }
    
    def analyze_savings(self) -> Dict:
        """Analyze potential savings from migration"""
        total_current_cost = sum(
            service["monthly_cost"] 
            for service in self.current_config.values()
        )
        
        potential_savings = sum(
            service.estimated_savings 
            for service in self.services
            if service.migration_priority >= 7
        )
        
        return {
            "current_monthly_cost": total_current_cost,
            "potential_monthly_savings": potential_savings,
            "new_monthly_cost": total_current_cost - potential_savings,
            "annual_savings": potential_savings * 12,
            "services_to_migrate": [
                service.name 
                for service in self.services 
                if service.migration_priority >= 7
            ]
        }
    
    def generate_migration_plan(self) -> Dict:
        """Generate step-by-step migration plan"""
        plan = {
            "phase_1": {
                "name": "Immediate Replacements (Week 1)",
                "services": [],
                "estimated_savings": 0.0,
                "steps": []
            },
            "phase_2": {
                "name": "Infrastructure Optimization (Week 2-3)",
                "services": [],
                "estimated_savings": 0.0,
                "steps": []
            },
            "phase_3": {
                "name": "Enhanced Capabilities (Month 2)",
                "services": [],
                "estimated_savings": 0.0,
                "steps": []
            }
        }
        
        # Categorize services by priority
        for service in self.services:
            if service.migration_priority >= 9:
                plan["phase_1"]["services"].append(service.name)
                plan["phase_1"]["estimated_savings"] += service.estimated_savings
            elif service.migration_priority >= 7:
                plan["phase_2"]["services"].append(service.name)
                plan["phase_2"]["estimated_savings"] += service.estimated_savings
            else:
                plan["phase_3"]["services"].append(service.name)
                plan["phase_3"]["estimated_savings"] += service.estimated_savings
        
        # Generate steps
        plan["phase_1"]["steps"] = [
            "1. Sign up for Brevo (email sending)",
            "2. Test OpenRouter free models",
            "3. Integrate Pollinations.AI for image generation",
            "4. Update email sending in cron jobs",
            "5. Test new LLM models for routine tasks"
        ]
        
        plan["phase_2"]["steps"] = [
            "1. Set up Google Cloud Firestore",
            "2. Migrate lead data from Supabase",
            "3. Configure Cloudflare R2 for storage",
            "4. Set up Langfuse for LLM observability",
            "5. Test AWS Lambda for serverless functions"
        ]
        
        plan["phase_3"]["steps"] = [
            "1. Implement EmailOctopus for newsletters",
            "2. Set up ImprovMX for email forwarding",
            "3. Configure Cloudflare Workers",
            "4. Add Mediaworkbench.ai for advanced tasks",
            "5. Optimize all integrations"
        ]
        
        return plan
    
    def create_implementation_scripts(self):
        """Create implementation scripts for each service"""
        scripts_dir = "/Users/cubiczan/.openclaw/workspace/scripts/free_tools"
        os.makedirs(scripts_dir, exist_ok=True)
        
        # 1. Brevo Email Integration
        brevo_script = f"""#!/bin/bash
# Brevo Email Integration Script
# Replaces AgentMail for outreach campaigns

echo "🚀 Setting up Brevo (formerly Sendinblue)"

# Sign up at: https://www.brevo.com/
# Get API key from SMTP & API section

# Configure environment
export BREVO_API_KEY="your_brevo_api_key_here"
export BREVO_SENDER_EMAIL="sam@impactquadrant.info"
export BREVO_SENDER_NAME="Agent Manager"

echo "✅ Brevo configuration ready"
echo "📧 Free tier: 9,000 emails/month, 300 emails/day"
echo "💸 Savings: ~$75/month vs AgentMail"

# Test email sending
python3 {scripts_dir}/test_brevo.py
"""
        
        with open(f"{scripts_dir}/setup_brevo.sh", "w") as f:
            f.write(brevo_script)
        os.chmod(f"{scripts_dir}/setup_brevo.sh", 0o755)
        
        # 2. OpenRouter Free Models
        openrouter_script = f"""#!/bin/bash
# OpenRouter Free Models Integration
# Replaces paid DeepSeek API

echo "🚀 Setting up OpenRouter Free Models"

# Available free models:
# - DeepSeek R1
# - DeepSeek V3
# - Llama models
# - Moonshot AI

# Sign up at: https://openrouter.ai/
# Get API key from account settings

export OPENROUTER_API_KEY="your_openrouter_key_here"
export OPENROUTER_FREE_MODEL="deepseek/deepseek-r1"

echo "✅ OpenRouter configuration ready"
echo "🧠 Free models available with rate limits"
echo "💸 Savings: ~$200/month vs paid APIs"

# Test with a simple query
python3 {scripts_dir}/test_openrouter.py
"""
        
        with open(f"{scripts_dir}/setup_openrouter.sh", "w") as f:
            f.write(openrouter_script)
        os.chmod(f"{scripts_dir}/setup_openrouter.sh", 0o755)
        
        # 3. Pollinations.AI Image Generation
        pollinations_script = f"""#!/bin/bash
# Pollinations.AI Image Generation
# Replaces OpenAI DALL-E

echo "🚀 Setting up Pollinations.AI"

# No signup or API keys required!
# Direct API access available

export POLLINATIONS_API="https://image.pollinations.ai/prompt/"
export POLLINATIONS_DEFAULT_SIZE="1024x1024"

echo "✅ Pollinations.AI configuration ready"
echo "🎨 Free image generation, no limits"
echo "💸 Savings: ~$100/month vs DALL-E"

# Test image generation
python3 {scripts_dir}/test_pollinations.py
"""
        
        with open(f"{scripts_dir}/setup_pollinations.sh", "w") as f:
            f.write(pollinations_script)
        os.chmod(f"{scripts_dir}/setup_pollinations.sh", 0o755)
        
        print(f"✅ Created implementation scripts in: {scripts_dir}")
    
    def generate_report(self):
        """Generate comprehensive migration report"""
        savings = self.analyze_savings()
        plan = self.generate_migration_plan()
        
        report = f"""
# 🚀 FREE TOOLS MIGRATION REPORT
# Generated: {subprocess.check_output(['date']).decode().strip()}

## 📊 CURRENT COST ANALYSIS

**Monthly Cost Breakdown:**
"""
        
        for service_name, config in self.current_config.items():
            report += f"- **{service_name.title()}**: ${config['monthly_cost']} ({config['provider']})\n"
        
        report += f"""
**Total Monthly Cost: ${savings['current_monthly_cost']:.2f}**
**Annual Cost: ${savings['current_monthly_cost'] * 12:.2f}**

## 💰 POTENTIAL SAVINGS

**Immediate Savings (Priority ≥ 7):**
- **Monthly**: ${savings['potential_monthly_savings']:.2f}
- **Annual**: ${savings['annual_savings']:.2f}

**New Monthly Cost**: ${savings['new_monthly_cost']:.2f}
**Reduction**: {((savings['potential_monthly_savings'] / savings['current_monthly_cost']) * 100):.1f}%

## 🎯 MIGRATION PLAN

### Phase 1: Immediate Replacements (Week 1)
**Services:** {', '.join(plan['phase_1']['services'])}
**Savings:** ${plan['phase_1']['estimated_savings']:.2f}/month

**Steps:**
"""
        
        for step in plan['phase_1']['steps']:
            report += f"{step}\n"
        
        report += f"""
### Phase 2: Infrastructure Optimization (Week 2-3)
**Services:** {', '.join(plan['phase_2']['services'])}
**Savings:** ${plan['phase_2']['estimated_savings']:.2f}/month

**Steps:**
"""
        
        for step in plan['phase_2']['steps']:
            report += f"{step}\n"
        
        report += f"""
### Phase 3: Enhanced Capabilities (Month 2)
**Services:** {', '.join(plan['phase_3']['services'])}
**Savings:** ${plan['phase_3']['estimated_savings']:.2f}/month

**Steps:**
"""
        
        for step in plan['phase_3']['steps']:
            report += f"{step}\n"
        
        report += """
## 🔧 IMPLEMENTATION SCRIPTS

Scripts created in: `/Users/cubiczan/.openclaw/workspace/scripts/free_tools/`

1. `setup_brevo.sh` - Email sending (replaces AgentMail)
2. `setup_openrouter.sh` - Free LLM models (replaces DeepSeek API)
3. `setup_pollinations.sh` - Image generation (replaces DALL-E)

## 🚀 RECOMMENDED ACTION PLAN

### Day 1-2:
1. Sign up for Brevo (email)
2. Test with small batch of outreach emails
3. Compare deliverability vs current system

### Day 3-4:
1. Sign up for OpenRouter
2. Test free models with routine agent tasks
3. Compare quality vs paid models

### Day 5-7:
1. Integrate Pollinations.AI for image generation
2. Update Instagram automation scripts
3. Test image quality and generation speed

## ⚠️ RISKS & MITIGATION

### 1. Rate Limits
- **Risk**: Free tiers have usage limits
- **Mitigation**: Monitor usage, implement fallbacks
- **Solution**: Use multiple free services as backup

### 2. Service Reliability
- **Risk**: Free services may have downtime
- **Mitigation**: Keep paid services as backup for 30 days
- **Solution**: Implement circuit breaker pattern

### 3. Feature Limitations
- **Risk**: Free tiers may lack advanced features
- **Mitigation**: Test thoroughly before full migration
- **Solution**: Phase migration, not all-at-once

## 📈 EXPECTED OUTCOMES

### Short-term (30 days):
- Reduce monthly costs by 60-80%
- Maintain same functionality
- Build redundancy with multiple providers

### Medium-term (90 days):
- Fully migrate from all paid services
- Implement monitoring for free tiers
- Optimize usage patterns

### Long-term (180 days):
- Annual savings: $3,000-$9,000
- Enhanced reliability with multiple providers
- Scalable foundation for growth

## 🔗 RESOURCES

1. **Free-for-dev GitHub**: https://github.com/ripienaar/free-for-dev
2. **Brevo Documentation**: https://developers.brevo.com/
3. **OpenRouter API Docs**: https://openrouter.ai/docs
4. **Pollinations.AI API**: https://pollinations.ai/

## 📞 SUPPORT

For implementation assistance:
1. Review scripts in `/scripts/free_tools/`
2. Test each service with small batches
3. Monitor performance for 7 days before full migration
4. Keep backup of current configuration

---
*Migration can save ${savings['annual_savings']:.2f}/year while maintaining capabilities*
*Start with Phase 1 this week for immediate savings*
"""
        
        report_path = "/Users/cubiczan/.openclaw/workspace/FREE_TOOLS_MIGRATION_REPORT.md"
        with open(report_path, "w") as f:
            f.write(report)
        
        print(f"✅ Report generated: {report_path}")
        return report_path

def main():
    """Main function"""
    print("="*60)
    print("FREE TOOLS MIGRATION ANALYZER")
    print("="*60)
    
    migrator = FreeToolsMigrator()
    
    # Analyze savings
    print("\n📊 Analyzing current costs vs free alternatives...")
    savings = migrator.analyze_savings()
    
    print(f"\n💸 Current Monthly Cost: ${savings['current_monthly_cost']:.2f}")
    print(f"💰 Potential Monthly Savings: ${savings['potential_monthly_savings']:.2f}")
    print(f"🎯 New Monthly Cost: ${savings['new_monthly_cost']:.2f}")
    print(f"📈 Annual Savings: ${savings['annual_savings']:.2f}")
    
    # Generate migration plan
    print("\n🎯 Generating migration plan...")
    migrator.generate_migration_plan()
    
    # Create implementation scripts
    print("\n🔧 Creating implementation scripts...")
    migrator.create_implementation_scripts()
    
    # Generate comprehensive report
    print("\n📄 Generating comprehensive report...")
    report_path = migrator.generate_report()
    
    print("\n" + "="*60)
    print("✅ MIGRATION ANALYSIS COMPLETE")
    print("="*60)
    print(f"\n📋 Report: {report_path}")
    print("🔧 Scripts: /Users/cubiczan/.openclaw/workspace/scripts/free_tools/")
    print("\n🚀 Next Steps:")
    print("1. Review the migration report")
    print("2. Run setup scripts for Phase 1 services")
    print("3. Test with small batches before full migration")
    print("4. Monitor performance for 7 days")
    print("\n💸 Expected savings: ${}/month".format(savings['potential_monthly_savings']))
    print("="*60)

if __name__ == "__main__":
    main()