#!/usr/bin/env python3
"""
Download and organize Awesome Agent Skills for OpenClaw
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any

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
            "cloudflare-building": {
                "repo": "cloudflare/skills",
                "path": "skills/building-ai-agent-on-cloudflare",
                "url": "https://github.com/cloudflare/skills/tree/main/skills/building-ai-agent-on-cloudflare",
                "description": "Build AI agents with state and WebSockets on Cloudflare"
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
            "canvas-design": {
                "repo": "anthropics/skills",
                "path": "skills/canvas-design",
                "url": "https://github.com/anthropics/skills/tree/main/skills/canvas-design",
                "description": "Design visual art in PNG and PDF formats"
            },
            "mcp-builder": {
                "repo": "anthropics/skills",
                "path": "skills/mcp-builder",
                "url": "https://github.com/anthropics/skills/tree/main/skills/mcp-builder",
                "description": "Create MCP servers to integrate external APIs and services"
            },
            "skill-creator": {
                "repo": "anthropics/skills",
                "path": "skills/skill-creator",
                "url": "https://github.com/anthropics/skills/tree/main/skills/skill-creator",
                "description": "Guide for creating skills that extend Claude's capabilities"
            }
        }
    
    def download_skill(self, skill_id: str, skill_info: Dict[str, str]) -> bool:
        """Download a single skill"""
        print(f"📥 Downloading {skill_id}...")
        
        repo = skill_info["repo"]
        path = skill_info["path"]
        url = skill_info["url"]
        
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
                subprocess.run(
                    ["git", "clone", "--depth", "1", repo_url, repo_dir],
                    check=True,
                    capture_output=True
                )
            else:
                print(f"  Updating {repo}...")
                subprocess.run(
                    ["git", "-C", repo_dir, "pull"],
                    check=True,
                    capture_output=True
                )
            
            # Copy the specific skill directory
            source_path = os.path.join(repo_dir, path)
            if os.path.exists(source_path):
                # Copy all files
                subprocess.run(
                    ["cp", "-r", f"{source_path}/.", skill_dir],
                    check=True
                )
                
                # Create a metadata file
                metadata = {
                    "id": skill_id,
                    "name": skill_id.replace("-", " ").title(),
                    "description": skill_info["description"],
                    "source_repo": repo,
                    "source_path": path,
                    "source_url": url,
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
                
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Error downloading {skill_id}: {e}")
            return False
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            return False
    
    def download_all_skills(self) -> Dict[str, bool]:
        """Download all target skills"""
        print("🚀 Downloading Awesome Agent Skills")
        print("="*60)
        
        results = {}
        
        for skill_id, skill_info in self.target_skills.items():
            success = self.download_skill(skill_id, skill_info)
            results[skill_id] = success
        
        return results
    
    def create_openclaw_skill_files(self):
        """Create OpenClaw-compatible skill files"""
        print("\n🔧 Creating OpenClaw skill files...")
        
        for skill_id in self.target_skills.keys():
            skill_dir = os.path.join(self.skills_dir, skill_id)
            if not os.path.exists(skill_dir):
                continue
            
            # Check for SKILL.md or README.md
            skill_md = os.path.join(skill_dir, "SKILL.md")
            readme_md = os.path.join(skill_dir, "README.md")
            
            if os.path.exists(skill_md):
                # Already has SKILL.md
                print(f"  ✅ {skill_id}: SKILL.md found")
            elif os.path.exists(readme_md):
                # Convert README.md to SKILL.md
                print(f"  📝 {skill_id}: Converting README.md to SKILL.md")
                with open(readme_md, 'r') as f:
                    content = f.read()
                
                # Create OpenClaw-compatible SKILL.md
                skill_content = self._create_skill_md_content(skill_id, content)
                with open(skill_md, 'w') as f:
                    f.write(skill_content)
            else:
                # Create basic SKILL.md
                print(f"  📝 {skill_id}: Creating basic SKILL.md")
                skill_content = self._create_basic_skill_md(skill_id)
                with open(skill_md, 'w') as f:
                    f.write(skill_content)
    
    def _create_skill_md_content(self, skill_id: str, original_content: str) -> str:
        """Create OpenClaw-compatible SKILL.md content"""
        skill_info = self.target_skills.get(skill_id, {})
        
        skill_md = f"""# {skill_id.replace("-", " ").title()} Skill

**Source:** {skill_info.get('description', 'Unknown')}

## Overview

This skill was downloaded from the Awesome Agent Skills collection.

**Original Repository:** {skill_info.get('repo', 'Unknown')}
**Source Path:** {skill_info.get('path', 'Unknown')}
**URL:** {skill_info.get('url', 'Unknown')}

## Usage

{original_content[:1000]}...

*Note: This is an auto-converted skill. Review the original documentation for complete details.*
"""
        return skill_md
    
    def _create_basic_skill_md(self, skill_id: str) -> str:
        """Create basic SKILL.md for skills without documentation"""
        skill_info = self.target_skills.get(skill_id, {})
        
        return f"""# {skill_id.replace("-", " ").title()} Skill

**Source:** {skill_info.get('description', 'Unknown')}

## Overview

This skill was downloaded from the Awesome Agent Skills collection but no documentation was found.

**Original Repository:** {skill_info.get('repo', 'Unknown')}
**Source Path:** {skill_info.get('path', 'Unknown')}
**URL:** {skill_info.get('url', 'Unknown')}

## Usage

Please refer to the original repository for documentation and usage instructions.

*Note: This is an auto-created placeholder. The actual skill files are present but documentation may be missing.*
"""
    
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

### Method 3: Copy Skills
Copy skills to your preferred location:

```bash
cp -r /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/* /Users/cubiczan/mac-bot/skills/
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
- **Skill Creator:** Learn to build your own skills

## 🔧 Testing Skills

Test each skill individually:

```bash
# Test PDF skill
cd /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/pdf
cat SKILL.md

# Test Excel skill  
cd /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/xlsx
cat SKILL.md

# Test Vercel deployment
cd /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/vercel-deploy
cat SKILL.md
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
python3 download_awesome_skills.py
```

## 📞 Support

- **Original Repositories:** Check each skill's source repository
- **OpenClaw Documentation:** https://docs.openclaw.ai
- **Awesome Agent Skills:** https://github.com/VoltAgent/awesome-agent-skills
"""
        
        with open(guide_path, 'w') as f:
            f.write(guide_content)
        
        print(f"  ✅ Integration guide created: {guide_path}")
    
    def create_setup_script(self):
        """Create setup script for easy integration"""
        print("\n⚡ Creating setup script...")
        
        script_path = os.path.join(self.skills_dir, "setup_openclaw_integration.sh")
        
        script_content = """#!/bin/bash
# Setup Awesome Agent Skills for OpenClaw

echo "🚀 Setting up Awesome Agent Skills for OpenClaw"
echo "="*60

# Create symbolic links in mac-bot/skills directory
echo "📁 Creating symbolic links..."
cd /Users/cubiczan/mac-bot/skills

# Remove existing links if they exist
for skill in pdf-awesome excel-awesome powerpoint-awesome vercel-deploy cloudflare-agents playwright-testing; do
    if [ -L "$skill" ]; then
        rm "$skill"
        echo "  Removed existing link: $skill"
    fi
done

# Create new symbolic links
ln -s /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/pdf pdf-awesome
ln -s /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/xlsx excel-awesome
ln -s /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/pptx powerpoint-awesome
ln -s /Users/cubiczan/.openclaw/workspace/skills/awesome-skills/vercel-deploy vercel-deploy
ln -s /Users/cubiczan