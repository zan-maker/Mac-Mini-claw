#!/usr/bin/env python3
"""
Download and organize Awesome Agent Skills for OpenClaw - Fixed version
"""

import os
import sys
import json
import subprocess
from pathlib import Path

class SkillDownloader:
    """Download and organize agent skills"""
    
    def __init__(self, base_dir: str = "/Users/cubiczan/.openclaw/workspace/skills"):
        self.base_dir = base_dir
        self.skills_dir = os.path.join(base_dir, "awesome-skills")
        os.makedirs(self.skills_dir, exist_ok=True)
        
        # Skills to download (based on user requirements)
        self.target_skills = {
            # Office Document Skills
            "pdf": {
                "repo": "anthropics/skills",
                "path": "skills/pdf",
                "url": "https://github.com/anthropics/skills/tree/main/skills/pdf",
                "description": "Extract text, create PDFs, and handle forms"
            },
            "xlsx": {
                "repo": "anthropics/skills", 
                "path": "skills/xlsx",
                "url": "https://github.com/anthropics/skills/tree/main/skills/xlsx",
                "description": "Create, edit, and analyze Excel spreadsheets"
            },
            "pptx": {
                "repo": "anthropics/skills",
                "path": "skills/pptx",
                "url": "https://github.com/anthropics/skills/tree/main/skills/pptx",
                "description": "Create, edit, and analyze PowerPoint presentations"
            },
            # Vercel Deployment
            "vercel-deploy": {
                "repo": "vercel-labs/agent-skills",
                "path": "skills/claude.ai/vercel-deploy-claimable",
                "url": "https://github.com/vercel-labs/agent-skills/tree/main/skills/claude.ai/vercel-deploy-claimable",
                "description": "Deploy projects to Vercel"
            },
            # Cloudflare Agents
            "cloudflare-agents": {
                "repo": "cloudflare/skills",
                "path": "skills/agents-sdk",
                "url": "https://github.com/cloudflare/skills/tree/main/skills/agents-sdk",
                "description": "Build stateful AI agents with scheduling, RPC, and MCP servers"
            },
            # Playwright Testing
            "playwright-testing": {
                "repo": "anthropics/skills",
                "path": "skills/webapp-testing",
                "url": "https://github.com/anthropics/skills/tree/main/skills/webapp-testing",
                "description": "Test local web applications using Playwright"
            },
            # Additional useful skills
            "docx": {
                "repo": "anthropics/skills",
                "path": "skills/docx",
                "url": "https://github.com/anthropics/skills/tree/main/skills/docx",
                "description": "Create, edit, and analyze Word documents"
            },
            "mcp-builder": {
                "repo": "anthropics/skills",
                "path": "skills/mcp-builder",
                "url": "https://github.com/anthropics/skills/tree/main/skills/mcp-builder",
                "description": "Create MCP servers to integrate external APIs and services"
            }
        }
    
    def download_skill(self, skill_id: str, skill_info: dict) -> bool:
        """Download a single skill"""
        print(f"📥 Downloading {skill_id}...")
        
        repo = skill_info["repo"]
        path = skill_info["path"]
        
        # Create skill directory
        skill_dir = os.path.join(self.skills_dir, skill_id)
        os.makedirs(skill_dir, exist_ok=True)
        
        # Check if we already have this repo cloned
        repo_name = repo.split("/")[1]
        repo_dir = os.path.join(self.skills_dir, "repos", repo_name)
        
        try:
            # Clone or update the repo
            if not os.path.exists(repo_dir):
                print(f"  Cloning {repo}...")
                repo_url = f"https://github.com/{repo}.git"
                result = subprocess.run(
                    ["git", "clone", "--depth", "1", repo_url, repo_dir],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    print(f"  ❌ Clone failed: {result.stderr}")
                    return False
            else:
                print(f"  Updating {repo}...")
                result = subprocess.run(
                    ["git", "-C", repo_dir, "pull"],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    print(f"  ⚠️  Update failed: {result.stderr}")
                    # Continue anyway, we might have old version
            
            # Copy the specific skill directory
            source_path = os.path.join(repo_dir, path)
            if os.path.exists(source_path):
                # Copy all files
                result = subprocess.run(
                    ["cp", "-r", f"{source_path}/.", skill_dir],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    print(f"  ⚠️  Copy failed: {result.stderr}")
                
                # Create a metadata file
                metadata = {
                    "id": skill_id,
                    "name": skill_id.replace("-", " ").title(),
                    "description": skill_info["description"],
                    "source_repo": repo,
                    "source_path": path,
                    "source_url": skill_info["url"],
                    "downloaded_at": subprocess.run(
                        ["date", "-Iseconds"],
                        capture_output=True,
                        text=True
                    ).stdout.strip()
                }
                
                with open(os.path.join(skill_dir, "METADATA.json"), "w") as f:
                    json.dump(metadata, f, indent=2)
                
                print(f"  ✅ {skill_id} downloaded successfully")
                return True
            else:
                print(f"  ❌ Skill path not found: {source_path}")
                return False
                
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            return False
    
    def download_all_skills(self) -> dict:
        """Download all target skills"""
        print("🚀 Downloading Awesome Agent Skills")
        print("="*60)
        
        results = {}
        
        for skill_id, skill_info in self.target_skills.items():
            success = self.download_skill(skill_id, skill_info)
            results[skill_id] = success
        
        return results
    
    def create_integration_guide(self):
        """Create integration guide for OpenClaw"""
        print("\n📋 Creating integration guide...")
        
        guide_path = os.path.join(self.skills_dir, "INTEGRATION_GUIDE.md")
        
        guide_content = """# Awesome Agent Skills Integration Guide

## 📦 Downloaded Skills

"""
        
        # List all downloaded skills
        for skill_id, skill_info in self.target_skills.items():
            skill_dir = os.path.join(self.skills_dir, skill_id)
            if os.path.exists(skill_dir):
                status = "✅ Downloaded"
            else:
                status = "❌ Failed"
            
            guide_content += f"### {skill_id.replace('-', ' ').title()}\n"
            guide_content += f"- **Status:** {status}\n"
            guide_content += f"- **Description:** {skill_info['description']}\n"
            guide_content += f"- **Source:** {skill_info['url']}\n"
            guide_content += f"- **Directory:** `skills/awesome-skills/{skill_id}`\n\n"
        
        # Add integration instructions
        guide_content += """## 🚀 Integration with OpenClaw

### Method 1: Direct Skill Reference
Add skill paths to your OpenClaw configuration:

```json
{
  "skills": {
    "paths": [
      "/Users/cubiczan/.openclaw/workspace/skills/awesome-skills/pdf",
      "/Users/cubiczan/.openclaw/workspace/skills/awesome-skills/xlsx",
      "/Users/cubiczan/.openclaw/workspace/skills/awesome-skills/pptx",
      "/Users/cubiczan/.openclaw/workspace/skills/awesome-skills/vercel-deploy",
      "/Users/cubiczan/.openclaw/workspace/skills/awesome-skills/cloudflare-agents",
      "/Users/cubiczan/.openclaw/workspace/skills/awesome-skills/playwright-testing"
    ]
  }
}
```

### Method 2: Symbolic Links
Create symbolic links in your main skills directory:

```bash
cd /Users/cubiczan/mac-bot/skills
ln -s /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/pdf pdf-awesome
ln -s /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/xlsx excel-awesome
ln -s /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/pptx powerpoint-awesome
ln -s /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/vercel-deploy vercel-deploy
ln -s /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/cloudflare-agents cloudflare-agents
ln -s /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/playwright-testing playwright-testing
```

## 🎯 Use Cases

### 1. Document Generation
- **PDF:** Generate reports, invoices, contracts
- **Excel:** Create financial models, data analysis sheets
- **PowerPoint:** Create presentations, pitch decks
- **Word:** Generate documents, letters, proposals

### 2. Deployment & Hosting
- **Vercel:** Deploy web applications instantly
- **Cloudflare:** Build full-stack AI agents with state

### 3. Testing & Quality Assurance
- **Playwright:** Test web applications automatically

### 4. Skill Development
- **MCP Builder:** Create custom Model Context Protocol servers

## 🔧 Testing Skills

Test each skill individually:

```bash
# Test PDF skill
cd /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/pdf
ls -la

# Test Excel skill  
cd /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/xlsx
ls -la

# Test Vercel deployment
cd /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/vercel-deploy
ls -la
```

## 📝 Notes

1. **Security:** Review all downloaded skills before use
2. **Dependencies:** Some skills may require additional packages
3. **Updates:** Skills can be updated by re-running the downloader
4. **Customization:** Modify skills to fit your specific needs

## 🔄 Updating Skills

To update all skills:

```bash
cd /Users/cubiczan/.openclaw/workspace
python3 download_awesome_skills_fixed.py
```

## 📞 Support

- **Original Repositories:** Check each skill's source repository
- **OpenClaw Documentation:** https://docs.openclaw.ai
- **Awesome Agent Skills:** https://github.com/VoltAgent/awesome-agent-skills
"""
        
        with open(guide_path, 'w') as f:
            f.write(guide_content)
        
        print(f"  ✅ Integration guide created: {guide_path}")
        return guide_path

def main():
    """Main function"""
    print("🔧 Awesome Agent Skills Downloader")
    print("="*60)
    
    downloader = SkillDownloader()
    
    # Download skills
    results = downloader.download_all_skills()
    
    # Create integration guide
    guide_path = downloader.create_integration_guide()
    
    # Summary
    print("\n" + "="*60)
    print("📊 DOWNLOAD SUMMARY")
    print("="*60)
    
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    
    print(f"✅ Successful: {successful}/{total}")
    print(f"❌ Failed: {total - successful}/{total}")
    
    print("\n🎯 Next Steps:")
    print(f"1. Review integration guide: {guide_path}")
    print("2. Create symbolic links to integrate with OpenClaw")
    print("3. Test each skill with sample tasks")
    print("4. Update OpenClaw configuration if needed")
    
    print("\n🚀 Quick integration command:")
    print("cd /Users/cubiczan/mac-bot/skills && \\")
    print("ln -s /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/pdf pdf-awesome && \\")
    print("ln -s /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/xlsx excel-awesome && \\")
    print("ln -s /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/pptx powerpoint-awesome")
    
    return successful > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)