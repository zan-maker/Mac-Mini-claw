#!/usr/bin/env python3
"""
Abstract API Rate Limiter Utility

For scripts using Abstract API company enrichment:
- Rate limit: 1 request per second
- Use this decorator or context manager to ensure compliance
"""

import time
import functools
from datetime import datetime, timedelta

class AbstractAPIRateLimiter:
    """Rate limiter for Abstract API (1 request per second)"""
    
    def __init__(self, requests_per_second=1):
        self.requests_per_second = requests_per_second
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0
        
    def wait_if_needed(self):
        """Wait if needed to maintain rate limit"""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        
        if elapsed < self.min_interval:
            sleep_time = self.min_interval - elapsed
            time.sleep(sleep_time)
            
        self.last_request_time = time.time()
        
    def __call__(self, func):
        """Decorator to rate limit function calls"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.wait_if_needed()
            return func(*args, **kwargs)
        return wrapper

# Global rate limiter instance
rate_limiter = AbstractAPIRateLimiter(requests_per_second=1)

def rate_limited(func):
    """Decorator for Abstract API functions"""
    return rate_limiter(func)

def make_abstract_api_request(url, params=None, headers=None):
    """
    Make a rate-limited request to Abstract API
    
    Usage:
        response = make_abstract_api_request(
            "https://companyenrichment.abstractapi.com/v1/",
            params={"api_key": "YOUR_KEY", "domain": "example.com"}
        )
    """
    import requests
    
    rate_limiter.wait_if_needed()
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Abstract API request failed: {e}")
        return None

def batch_process_with_rate_limit(items, process_func, batch_delay=1.0):
    """
    Process items with rate limiting
    
    Args:
        items: List of items to process
        process_func: Function to call for each item (will be rate-limited)
        batch_delay: Additional delay between items (default: 1 second)
    """
    results = []
    
    for i, item in enumerate(items):
        print(f"Processing item {i+1}/{len(items)}...")
        
        # Apply rate limiting
        rate_limiter.wait_if_needed()
        
        # Process the item
        result = process_func(item)
        results.append(result)
        
        # Optional additional delay
        if batch_delay > 0:
            time.sleep(batch_delay)
            
    return results

# Example usage
if __name__ == "__main__":
    print("Abstract API Rate Limiter Utility")
    print("=" * 50)
    
    # Example 1: Using decorator
    @rate_limited
    def get_company_info(domain):
        """Example function that calls Abstract API"""
        print(f"Getting info for {domain}")
        # Simulate API call
        time.sleep(0.1)
        return {"domain": domain, "data": "sample"}
    
    # Example 2: Using context manager style
    domains = ["example1.com", "example2.com", "example3.com"]
    
    print(f"\nProcessing {len(domains)} domains with rate limiting:")
    for domain in domains:
        rate_limiter.wait_if_needed()
        print(f"  Processing {domain}")
        # Call your Abstract API function here
    
    print("\n✅ Rate limiter ready for use in your scripts")
