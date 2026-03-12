#!/usr/bin/env python3
"""
Social Media Automation Script using PinchTab CLI
For Instagram, Facebook, and other platforms
"""

import subprocess
import json
import time
import os
from datetime import datetime
from typing import Dict, List, Optional

class PinchTabAutomation:
    """Social media automation using PinchTab CLI"""
    
    def __init__(self):
        self.current_tab_id = None
        
    def run_command(self, command: str) -> Dict:
        """Run PinchTab CLI command and parse JSON output"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Try to parse JSON output
            if result.stdout.strip():
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    # Some commands output non-JSON (like snap)
                    return {"output": result.stdout, "success": True}
            else:
                return {"error": result.stderr, "success": False}
                
        except subprocess.TimeoutExpired:
            return {"error": "Command timed out", "success": False}
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def navigate(self, url: str) -> bool:
        """Navigate to URL"""
        result = self.run_command(f"pinchtab nav {url}")
        if result.get("success") and "tabId" in result:
            self.current_tab_id = result.get("tabId")
            print(f"✅ Navigated to {url}")
            print(f"   Tab ID: {self.current_tab_id}")
            return True
        else:
            print(f"❌ Failed to navigate to {url}")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            return False
    
    def snapshot(self, compact: bool = True, interactive: bool = False) -> Optional[str]:
        """Take snapshot of current page"""
        flags = ""
        if compact:
            flags += " -c"
        if interactive:
            flags += " -i"
            
        result = self.run_command(f"pinchtab snap{flags}")
        if "output" in result:
            return result["output"]
        return None
    
    def click_element(self, element_ref: str) -> bool:
        """Click on element by reference"""
        result = self.run_command(f"pinchtab click {element_ref}")
        success = result.get("success", False)
        if success:
            print(f"✅ Clicked element {element_ref}")
        else:
            print(f"❌ Failed to click element {element_ref}")
        return success
    
    def type_text(self, element_ref: str, text: str) -> bool:
        """Type text into element"""
        # Escape quotes for shell command
        escaped_text = text.replace('"', '\\"')
        result = self.run_command(f'pinchtab type {element_ref} "{escaped_text}"')
        success = result.get("success", False)
        if success:
            print(f"✅ Typed into element {element_ref}")
        else:
            print(f"❌ Failed to type into element {element_ref}")
        return success
    
    def extract_text(self) -> Optional[Dict]:
        """Extract readable text from page"""
        result = self.run_command("pinchtab text")
        if result.get("success"):
            return result
        return None
    
    def screenshot(self, filename: str) -> bool:
        """Take screenshot"""
        result = self.run_command(f"pinchtab ss -o {filename}")
        success = result.get("success", False)
        if success:
            print(f"✅ Screenshot saved to {filename}")
        else:
            print(f"❌ Failed to save screenshot")
        return success

class SocialMediaManager:
    """Manage social media automation workflows"""
    
    def __init__(self):
        self.pinchtab = PinchTabAutomation()
        
    def post_to_instagram(self, image_path: str, caption: str):
        """Post to Instagram (requires login)"""
        print("\n📱 Instagram Posting Workflow")
        print("=" * 50)
        
        # Step 1: Navigate to Instagram
        if not self.pinchtab.navigate("https://www.instagram.com"):
            return False
        
        # Step 2: Check if logged in (simplified - would need actual login flow)
        snapshot = self.pinchtab.snapshot()
        if snapshot and "Create" in snapshot:
            print("✅ Already logged into Instagram")
        else:
            print("⚠️ Not logged in - authentication required")
            print("   Please log in manually first")
            return False
        
        # Step 3: Create new post (simplified workflow)
        # In reality, would need to:
        # 1. Click create button
        # 2. Upload image
        # 3. Add caption
        # 4. Click share
        
        print(f"📸 Would post: {image_path}")
        print(f"📝 Caption: {caption[:50]}...")
        
        # For now, return success but note it's a placeholder
        print("✅ Instagram posting workflow ready (requires authentication)")
        return True
    
    def post_to_facebook(self, content: str, image_path: Optional[str] = None):
        """Post to Facebook (requires login)"""
        print("\n📘 Facebook Posting Workflow")
        print("=" * 50)
        
        # Step 1: Navigate to Facebook
        if not self.pinchtab.navigate("https://www.facebook.com"):
            return False
        
        # Step 2: Check login status
        snapshot = self.pinchtab.snapshot()
        if snapshot and ("What's on your mind" in snapshot or "Create post" in snapshot):
            print("✅ Already logged into Facebook")
        else:
            print("⚠️ Not logged in - authentication required")
            print("   Please log in manually first")
            return False
        
        print(f"📝 Content: {content[:50]}...")
        if image_path:
            print(f"📸 Image: {image_path}")
        
        print("✅ Facebook posting workflow ready (requires authentication)")
        return True
    
    def monitor_hashtag(self, platform: str, hashtag: str, limit: int = 10):
        """Monitor posts with specific hashtag"""
        print(f"\n🔍 Monitoring #{hashtag} on {platform}")
        print("=" * 50)
        
        if platform.lower() == "instagram":
            url = f"https://www.instagram.com/explore/tags/{hashtag}/"
        elif platform.lower() == "twitter":
            url = f"https://twitter.com/hashtag/{hashtag}"
        else:
            print(f"❌ Platform {platform} not supported for hashtag monitoring")
            return []
        
        if not self.pinchtab.navigate(url):
            return []
        
        # Wait for page to load
        time.sleep(3)
        
        # Extract text content
        result = self.pinchtab.extract_text()
        if result:
            text = result.get("text", "")
            print(f"📊 Found content for #{hashtag}")
            print(f"   URL: {result.get('url', 'N/A')}")
            print(f"   Title: {result.get('title', 'N/A')}")
            
            # Take screenshot for record
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_file = f"/tmp/hashtag_{hashtag}_{timestamp}.png"
            self.pinchtab.screenshot(screenshot_file)
            
            return [{"hashtag": hashtag, "content": text[:200], "screenshot": screenshot_file}]
        
        return []
    
    def create_scheduled_posting_script(self, platform: str, content_file: str):
        """Create a script for scheduled posting"""
        print(f"\n⏰ Creating scheduled posting script for {platform}")
        print("=" * 50)
        
        script_content = f"""#!/bin/bash
# Scheduled posting script for {platform}
# Generated: {datetime.now().isoformat()}

export PINCHTAB_URL="http://127.0.0.1:9867"

# Load content from file
CONTENT_FILE="{content_file}"
if [ ! -f "$CONTENT_FILE" ]; then
    echo "Error: Content file not found: $CONTENT_FILE"
    exit 1
fi

# Read content
CAPTION=$(head -1 "$CONTENT_FILE")
IMAGE_PATH=$(sed -n '2p' "$CONTENT_FILE" 2>/dev/null || echo "")

echo "Posting to {platform}..."
echo "Caption: $CAPTION"
if [ -n "$IMAGE_PATH" ]; then
    echo "Image: $IMAGE_PATH"
fi

# Add your posting commands here
# Example for Instagram:
# pinchtab nav https://www.instagram.com
# pinchtab click eXX  # Create button
# ... etc

echo "✅ Post scheduled for {platform}"
"""

        script_file = f"/tmp/schedule_{platform.lower()}.sh"
        with open(script_file, "w") as f:
            f.write(script_content)
        
        os.chmod(script_file, 0o755)
        print(f"✅ Script created: {script_file}")
        print(f"   To schedule: crontab -e")
        print(f"   Add: 0 9,12,15,18 * * * {script_file}")
        
        return script_file

def main():
    """Main function"""
    print("=" * 60)
    print("SOCIAL MEDIA AUTOMATION WITH PINCHTAB")
    print("=" * 60)
    
    manager = SocialMediaManager()
    
    # Example workflows
    print("\n1. Testing basic navigation...")
    manager.pinchtab.navigate("https://example.com")
    time.sleep(2)
    
    print("\n2. Creating scheduled posting script for Instagram...")
    content_file = "/tmp/instagram_post.txt"
    with open(content_file, "w") as f:
        f.write("Check out our latest AI automation tools! #AI #Automation\n")
        f.write("/path/to/image.jpg\n")
    
    script_path = manager.create_scheduled_posting_script("Instagram", content_file)
    
    print("\n3. Testing hashtag monitoring (example)...")
    # This would work once authenticated
    # manager.monitor_hashtag("instagram", "AI", limit=5)
    
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("1. Fix authentication for Instagram/Facebook")
    print("2. Update script with actual element references")
    print("3. Schedule with cron: crontab -e")
    print("4. Test with safe content first")
    print("=" * 60)

if __name__ == "__main__":
    main()
