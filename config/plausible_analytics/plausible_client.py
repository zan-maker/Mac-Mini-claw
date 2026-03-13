#!/usr/bin/env python3
"""
Plausible Analytics Client
Free alternative to Mixpanel
"""

import requests
import json
from typing import Dict, List, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class PlausibleClient:
    """Client for Plausible Analytics API"""
    
    def __init__(self, site_id: str, api_key: Optional[str] = None):
        """
        Initialize Plausible client
        
        Args:
            site_id: Your Plausible site ID
            api_key: Optional API key for stats API (not required for tracking)
        """
        self.site_id = site_id
        self.api_key = api_key
        self.base_url = "https://plausible.io"
        
        logger.info(f"Plausible client initialized for site: {site_id}")
    
    def track_pageview(self, url: str, referrer: Optional[str] = None,
                      screen_width: Optional[int] = None,
                      user_agent: Optional[str] = None) -> bool:
        """
        Track a pageview event
        
        Note: Normally you'd use the JavaScript snippet for pageviews.
        This is for server-side tracking when needed.
        
        Args:
            url: Page URL
            referrer: Referrer URL
            screen_width: Screen width in pixels
            user_agent: User agent string
            
        Returns:
            True if successful
        """
        payload = {
            'domain': self.site_id,
            'name': 'pageview',
            'url': url,
            'referrer': referrer,
            'screen_width': screen_width
        }
        
        headers = {
            'User-Agent': user_agent or 'Plausible-Python-Client/1.0',
            'Content-Type': 'application/json'
        }
        
        try:
            # Plausible events endpoint
            response = requests.post(
                f'{self.base_url}/api/event',
                json=payload,
                headers=headers
            )
            
            if response.status_code == 202:
                logger.info(f"Tracked pageview: {url}")
                return True
            else:
                logger.warning(f"Failed to track pageview: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error tracking pageview: {e}")
            return False
    
    def track_custom_event(self, event_name: str, props: Optional[Dict] = None,
                          url: Optional[str] = None) -> bool:
        """
        Track a custom event
        
        Args:
            event_name: Name of the event
            props: Optional event properties
            url: Page URL where event occurred
            
        Returns:
            True if successful
        """
        payload = {
            'domain': self.site_id,
            'name': event_name,
            'url': url or 'https://app.impactquadrant.info',
            'props': props or {}
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/api/event',
                json=payload
            )
            
            if response.status_code == 202:
                logger.info(f"Tracked custom event: {event_name}")
                return True
            else:
                logger.warning(f"Failed to track event: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error tracking event: {e}")
            return False
    
    def get_stats(self, period: str = '30d', metrics: List[str] = None) -> Dict:
        """
        Get site statistics (requires API key)
        
        Args:
            period: Time period (30d, 7d, day, month, etc.)
            metrics: List of metrics to retrieve
            
        Returns:
            Dictionary with stats
        """
        if not self.api_key:
            logger.error("API key required for stats")
            return {'error': 'API key required'}
        
        metrics = metrics or ['visitors', 'pageviews', 'bounce_rate', 'visit_duration']
        
        params = {
            'site_id': self.site_id,
            'period': period,
            'metrics': ','.join(metrics)
        }
        
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        
        try:
            response = requests.get(
                f'{self.base_url}/api/v1/stats/aggregate',
                params=params,
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get stats: {response.status_code}")
                return {'error': f'API error: {response.status_code}'}
                
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {'error': str(e)}
    
    def generate_tracking_snippet(self) -> str:
        """
        Generate HTML tracking snippet for website
        
        Returns:
            HTML script tag for Plausible
        """
        snippet = f"""<!-- Plausible Analytics - Privacy-friendly alternative to Mixpanel -->
<script defer data-domain="{self.site_id}" src="https://plausible.io/js/script.js"></script>
<!-- Optional: Track custom events -->
<script>
  window.plausible = window.plausible || function() {{ (window.plausible.q = window.plausible.q || []).push(arguments) }}
</script>"""
        
        return snippet
    
    def compare_with_mixpanel(self) -> Dict:
        """
        Compare Plausible with Mixpanel
        
        Returns:
            Comparison dictionary
        """
        return {
            'cost': {
                'plausible': 'Free (10k pageviews/month)',
                'mixpanel': '$75/month (starter plan)'
            },
            'privacy': {
                'plausible': 'GDPR compliant, no cookies',
                'mixpanel': 'Requires cookie consent'
            },
            'size': {
                'plausible': '1.4KB',
                'mixpanel': '50KB+'
            },
            'features': {
                'plausible_has': ['Pageviews', 'Referrers', 'Countries', 'Devices', 'Custom events'],
                'mixpanel_has_extra': ['Funnel analysis', 'Cohort analysis', 'A/B testing', 'Advanced segmentation']
            },
            'recommendation': 'Use Plausible for basic analytics, keep Mixpanel only if advanced features are critical'
        }

# Example usage
def example_plausible_usage():
    """Example usage of Plausible Analytics"""
    print("📊 Plausible Analytics Example")
    print("="*50)
    
    # Initialize client
    client = PlausibleClient(
        site_id='impactquadrant.info',  # Your site ID
        api_key=os.getenv('PLAUSIBLE_API_KEY')  # Optional for stats
    )
    
    print(f"✅ Plausible client initialized")
    print(f"   Site: {client.site_id}")
    
    # Generate tracking snippet
    snippet = client.generate_tracking_snippet()
    print(f"\n📝 Tracking snippet (add to website HTML):")
    print(snippet[:200] + "...")
    
    # Compare with Mixpanel
    print("\n🔄 Comparison with Mixpanel:")
    comparison = client.compare_with_mixpanel()
    print(f"   Cost: {comparison['cost']['plausible']} vs {comparison['cost']['mixpanel']}")
    print(f"   Size: {comparison['size']['plausible']} vs {comparison['size']['mixpanel']}")
    print(f"   Privacy: {comparison['privacy']['plausible']}")
    
    # Example tracking
    print("\n🎯 Example tracking calls:")
    print("   • client.track_pageview('https://impactquadrant.info/dashboard')")
    print("   • client.track_custom_event('lead_generated', {'source': 'instagram'})")
    print("   • client.get_stats('30d', ['visitors', 'pageviews'])")
    
    print("\n💰 Monthly savings: $75")
    print("📈 Free tier: 10,000 pageviews/month")

if __name__ == "__main__":
    import os
    example_plausible_usage()
