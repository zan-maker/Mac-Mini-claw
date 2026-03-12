#!/usr/bin/env python3
"""
Pinchtab Client for OpenClaw System
High-performance browser automation bridge for Kalshi trading, social media, and lead generation
"""

import requests
import json
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BrowserMode(Enum):
    HEADLESS = "headless"
    HEADED = "headed"

class PinchtabClient:
    """Client for Pinchtab HTTP API"""
    
    def __init__(self, host: str = "http://localhost:9867", api_token: Optional[str] = None):
        self.host = host
        self.api_token = api_token
        self.headers = {}
        if api_token:
            self.headers["Authorization"] = f"Bearer {api_token}"
        
        # Cache for instances and tabs
        self.instances: Dict[str, Dict] = {}
        self.tabs: Dict[str, Dict] = {}
        
        logger.info(f"Pinchtab client initialized: {host}")
    
    def health_check(self) -> bool:
        """Check if Pinchtab server is healthy"""
        try:
            response = requests.get(f"{self.host}/health", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def create_instance(self, name: str, mode: BrowserMode = BrowserMode.HEADLESS, 
                       profile_id: Optional[str] = None) -> Optional[str]:
        """Create a new browser instance"""
        try:
            payload = {"name": name, "mode": mode.value}
            if profile_id:
                payload["profileId"] = profile_id
            
            response = requests.post(
                f"{self.host}/instances/launch",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                instance_data = response.json()
                instance_id = instance_data.get("id")
                if instance_id:
                    self.instances[instance_id] = instance_data
                    logger.info(f"Created instance {name} with ID: {instance_id}")
                    return instance_id
            
            logger.error(f"Failed to create instance: {response.text}")
            return None
            
        except Exception as e:
            logger.error(f"Error creating instance: {e}")
            return None
    
    def open_tab(self, instance_id: str, url: str, name: Optional[str] = None) -> Optional[str]:
        """Open a new tab in an instance"""
        try:
            payload = {"url": url}
            if name:
                payload["name"] = name
            
            response = requests.post(
                f"{self.host}/instances/{instance_id}/tabs/open",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                tab_data = response.json()
                tab_id = tab_data.get("tabId")
                if tab_id:
                    self.tabs[tab_id] = tab_data
                    logger.info(f"Opened tab to {url} with ID: {tab_id}")
                    return tab_id
            
            logger.error(f"Failed to open tab: {response.text}")
            return None
            
        except Exception as e:
            logger.error(f"Error opening tab: {e}")
            return None
    
    def navigate(self, tab_id: str, url: str) -> bool:
        """Navigate a tab to a URL"""
        try:
            response = requests.post(
                f"{self.host}/tabs/{tab_id}/navigate",
                json={"url": url},
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"Navigated tab {tab_id} to {url}")
                return True
            
            logger.error(f"Failed to navigate: {response.text}")
            return False
            
        except Exception as e:
            logger.error(f"Error navigating: {e}")
            return False
    
    def snapshot(self, tab_id: str, interactive: bool = True, compact: bool = True) -> Optional[Dict]:
        """Get a snapshot of the current page"""
        try:
            params = {
                "filter": "interactive" if interactive else "all",
                "compact": "true" if compact else "false"
            }
            
            response = requests.get(
                f"{self.host}/tabs/{tab_id}/snapshot",
                params=params,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            
            logger.error(f"Failed to get snapshot: {response.text}")
            return None
            
        except Exception as e:
            logger.error(f"Error getting snapshot: {e}")
            return None
    
    def click(self, tab_id: str, element_ref: str) -> bool:
        """Click an element by reference"""
        try:
            response = requests.post(
                f"{self.host}/tabs/{tab_id}/action",
                json={"kind": "click", "ref": element_ref},
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"Clicked element {element_ref} in tab {tab_id}")
                return True
            
            logger.error(f"Failed to click: {response.text}")
            return False
            
        except Exception as e:
            logger.error(f"Error clicking: {e}")
            return False
    
    def type_text(self, tab_id: str, element_ref: str, text: str, submit: bool = False) -> bool:
        """Type text into an input element"""
        try:
            payload = {
                "kind": "type",
                "ref": element_ref,
                "text": text
            }
            if submit:
                payload["submit"] = True
            
            response = requests.post(
                f"{self.host}/tabs/{tab_id}/action",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"Typed text into {element_ref} in tab {tab_id}")
                return True
            
            logger.error(f"Failed to type text: {response.text}")
            return False
            
        except Exception as e:
            logger.error(f"Error typing text: {e}")
            return False
    
    def extract_text(self, tab_id: str) -> Optional[str]:
        """Extract text content from page (token-efficient)"""
        try:
            response = requests.get(
                f"{self.host}/tabs/{tab_id}/text",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                text_data = response.json()
                return text_data.get("text", "")
            
            logger.error(f"Failed to extract text: {response.text}")
            return None
            
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return None
    
    def close_tab(self, tab_id: str) -> bool:
        """Close a tab"""
        try:
            response = requests.delete(
                f"{self.host}/tabs/{tab_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                if tab_id in self.tabs:
                    del self.tabs[tab_id]
                logger.info(f"Closed tab {tab_id}")
                return True
            
            logger.error(f"Failed to close tab: {response.text}")
            return False
            
        except Exception as e:
            logger.error(f"Error closing tab: {e}")
            return False
    
    def close_instance(self, instance_id: str) -> bool:
        """Close an instance"""
        try:
            response = requests.delete(
                f"{self.host}/instances/{instance_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                if instance_id in self.instances:
                    del self.instances[instance_id]
                logger.info(f"Closed instance {instance_id}")
                return True
            
            logger.error(f"Failed to close instance: {response.text}")
            return False
            
        except Exception as e:
            logger.error(f"Error closing instance: {e}")
            return False
    
    def list_instances(self) -> List[Dict]:
        """List all running instances"""
        try:
            response = requests.get(
                f"{self.host}/instances",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get("instances", [])
            
            logger.error(f"Failed to list instances: {response.text}")
            return []
            
        except Exception as e:
            logger.error(f"Error listing instances: {e}")
            return []
    
    def cleanup(self):
        """Clean up all instances and tabs"""
        logger.info("Cleaning up all Pinchtab resources")
        
        # Close all tabs
        for tab_id in list(self.tabs.keys()):
            self.close_tab(tab_id)
        
        # Close all instances
        for instance_id in list(self.instances.keys()):
            self.close_instance(instance_id)
        
        logger.info("Cleanup complete")


class PinchtabManager:
    """High-level manager for Pinchtab automation tasks"""
    
    def __init__(self):
        self.client = PinchtabClient()
        self.kalshi_instance = None
        self.kalshi_tab = None
        self.linkedin_sam_instance = None
        self.linkedin_sam_tab = None
        self.linkedin_shyam_instance = None
        self.linkedin_shyam_tab = None
        
        logger.info("Pinchtab Manager initialized")
    
    def setup_kalshi_trading(self) -> bool:
        """Setup Kalshi trading automation"""
        try:
            logger.info("Setting up Kalshi trading automation")
            
            # Create instance for Kalshi
            self.kalshi_instance = self.client.create_instance(
                name="kalshi-trader",
                mode=BrowserMode.HEADLESS
            )
            
            if not self.kalshi_instance:
                logger.error("Failed to create Kalshi instance")
                return False
            
            # Open tab to Kalshi
            self.kalshi_tab = self.client.open_tab(
                instance_id=self.kalshi_instance,
                url="https://kalshi.com",
                name="kalshi-dashboard"
            )
            
            if not self.kalshi_tab:
                logger.error("Failed to open Kalshi tab")
                return False
            
            logger.info("Kalshi trading setup complete")
            return True
            
        except Exception as e:
            logger.error(f"Error setting up Kalshi trading: {e}")
            return False
    
    def setup_linkedin_profiles(self) -> bool:
        """Setup LinkedIn profiles for dual strategy"""
        try:
            logger.info("Setting up LinkedIn profiles")
            
            # Setup Sam Desigan profile
            self.linkedin_sam_instance = self.client.create_instance(
                name="linkedin-sam",
                mode=BrowserMode.HEADLESS,
                profile_id="sam-desigan"
            )
            
            if self.linkedin_sam_instance:
                self.linkedin_sam_tab = self.client.open_tab(
                    instance_id=self.linkedin_sam_instance,
                    url="https://linkedin.com",
                    name="sam-profile"
                )
            
            # Setup Shyam Desigan profile
            self.linkedin_shyam_instance = self.client.create_instance(
                name="linkedin-shyam",
                mode=BrowserMode.HEADLESS,
                profile_id="shyam-desigan"
            )
            
            if self.linkedin_shyam_instance:
                self.linkedin_shyam_tab = self.client.open_tab(
                    instance_id=self.linkedin_shyam_instance,
                    url="https://linkedin.com",
                    name="shyam-profile"
                )
            
            logger.info("LinkedIn profiles setup complete")
            return True
            
        except Exception as e:
            logger.error(f"Error setting up LinkedIn profiles: {e}")
            return False
    
    def monitor_gas_prices(self) -> Optional[float]:
        """Monitor AAA gas prices"""
        try:
            logger.info("Monitoring AAA gas prices")
            
            # Create temporary instance for AAA
            aaa_instance = self.client.create_instance(
                name="aaa-gas-monitor",
                mode=BrowserMode.HEADLESS
            )
            
            if not aaa_instance:
                return None
            
            # Open AAA gas prices page
            aaa_tab = self.client.open_tab(
                instance_id=aaa_instance,
                url="https://gasprices.aaa.com",
                name="aaa-gas-prices"
            )
            
            if not aaa_tab:
                self.client.close_instance(aaa_instance)
                return None
            
            # Wait for page to load
            time.sleep(3)
            
            # Get snapshot to find price element
            snapshot = self.client.snapshot(aaa_tab, interactive=True, compact=True)
            
            # Extract text (simplified - in real implementation would parse snapshot)
            page_text = self.client.extract_text(aaa_tab)
            
            # Clean up
            self.client.close_tab(aaa_tab)
            self.client.close_instance(aaa_instance)
            
            # Parse price from text (simplified)
            if page_text:
                # Look for price patterns
                import re
                price_pattern = r'\$(\d+\.\d{2})'
                matches = re.findall(price_pattern, page_text)
                if matches:
                    price = float(matches[0])
                    logger.info(f"Found gas price: ${price}")
                    return price
            
            logger.warning("Could not extract gas price")
            return None
            
        except Exception as e:
            logger.error(f"Error monitoring gas prices: {e}")
            return None
    
    def post_to_linkedin(self, profile: str, content: str) -> bool:
        """Post content to LinkedIn"""
        try:
            logger.info(f"Posting to LinkedIn profile: {profile}")
            
            # Select the right instance/tab
            if profile.lower() == "sam":
                instance = self.linkedin_sam_instance
                tab = self.linkedin_sam_tab
            elif profile.lower() == "shyam":
                instance = self.linkedin_shyam_instance
                tab = self.linkedin_shyam_tab
            else:
                logger.error(f"Unknown profile: {profile}")
                return False
            
            if not instance or not tab:
                logger.error(f"Profile {profile} not setup")
                return False
            
            # Navigate to LinkedIn post creation
            self.client.navigate(tab, "https://www.linkedin.com/feed/")
            time.sleep(2)
            
            # Get snapshot to find post button
            snapshot = self.client.snapshot(tab, interactive=True, compact=True)
            
            # In real implementation, would:
            # 1. Find and click "Start a post" button
            # 2. Type content
            # 3. Click post button
            
            # For now, just log the action
            logger.info(f"Would post to {profile}: {content[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Error posting to LinkedIn: {e}")
            return False
    
    def cleanup_all(self):
        """Clean up all resources"""
        logger.info("Cleaning up all Pinchtab resources")
        self.client.cleanup()
        
        # Reset references
        self.kalshi_instance = None
        self.kalshi_tab = None
        self.linkedin_sam_instance = None
        self.linkedin_sam_tab = None
        self.linkedin_shyam_instance = None
        self.linkedin_shyam_tab = None
        
        logger.info("Cleanup complete")


# Example usage
if __name__ == "__main__":
    print("🧪 Testing Pinchtab Integration")
    print("=" * 50)
    
    # Create manager
    manager = PinchtabManager()
    
    # Check health
    if manager.client.health_check():
        print("✅ Pinchtab server is healthy")
    else:
        print("❌ Pinchtab server is not responding")
        exit(1)
    
    # Test gas price monitoring
    print("\n📊 Testing gas price monitoring...")
    gas_price = manager.monitor_gas_prices()
    if gas_price:
        print(f"✅ Current gas price: ${gas_price}")
    else:
        print("⚠️  Could not get gas price")
    
    # List instances
    print("\n📋 Listing instances...")
    instances = manager.client.list_instances()
    print(f"Found {len(instances)} instances")
    
    # Cleanup
    print("\n🧹 Cleaning up...")
    manager.cleanup_all()
    
    print("\n🎉 Pinchtab integration test complete!")