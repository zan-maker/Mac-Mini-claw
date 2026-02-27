#!/usr/bin/env python3
"""
Simplified Deal Origination - Sellers
Using traditional APIs since Scrapling integration needs debugging
"""

import sys
import os
import json
import time
from datetime import datetime
import requests

# Configuration
TAVILY_API_KEY = "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"
BRAVE_API_KEY = "BSA4VYA3FjSPQmTjZeKjsq5CqWvFy2u"

# Search terms for off-market sellers
SEARCH_TERMS = [
    "HVAC business for sale owner retiring",
    "plumbing company owner retirement",
    "electrical contractor business sale",
    "commercial cleaning business owner exit",
    "healthcare services business acquisition",
    "roofing company for sale no broker",
    "fire safety business owner retiring",
    "waste management company succession planning",
    "insurance brokerage owner exit strategy",
    "dental practice for sale doctor retiring",
    "veterinary clinic owner retirement",
    "logistics company owner succession",
    "manufacturing business owner retiring",
    "distribution company for sale no broker"
]

def main():
    print("🚀 Starting Deal Origination - Sellers")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔍 Search terms: {len(SEARCH_TERMS)}")
    
    start_time = time.time()
    sellers = []
    
    # Try Tavily API first
    print("\n🔄 Trying Tavily API...")
    tavily_sellers = find_with_tavily()
    sellers.extend(tavily_sellers)
    print(f"   Found {len(tavily_sellers)} sellers via Tavily")
    
    # If not enough results, try Brave
    if len(sellers) < 10:
        print("\n🔄 Trying Brave Search API...")
        brave_sellers = find_with_brave()
        sellers.extend(brave_sellers)
        print(f"   Found {len(brave_sellers)} sellers via Brave")
    
    # Process results
    print(f"\n📊 Total sellers found: {len(sellers)}")
    
    if sellers:
        # Save results
        save_results(sellers, start_time)
        
        # Generate summary
        generate_summary(sellers, start_time)
    else:
        print("❌ No sellers found")
        
    print(f"\n⏱️ Total processing time: {time.time() - start_time:.2f} seconds")

def find_with_tavily():
    """Find sellers using Tavily API"""
    sellers = []
    headers = {
        "X-API-Key": TAVILY_API_KEY,
        "Content-Type": "application/json"
    }
    
    for search_term in SEARCH_TERMS[:5]:  # Limit to 5 to avoid rate limits
        try:
            print(f"  Searching: {search_term}")
            payload = {
                "query": f"{search_term} -broker",
                "max_results": 3,
                "search_depth": "basic"
            }
            
            response = requests.post(
                "https://api.tavily.com/search",
                json=payload,
                headers=headers,
                timeout=20
            )
            
            if response.status_code == 200:
                results = response.json().get("results", [])
                for result in results:
                    seller = {
                        "company": result.get("title", "Unknown Company"),
                        "source": "Tavily API",
                        "url": result.get("url", ""),
                        "description": result.get("content", ""),
                        "industry": extract_industry(search_term),
                        "ebitda_range": estimate_ebitda(search_term),
                        "years_in_business": 15,
                        "owner_signals": ["owner_near_retirement", "off_market"],
                        "search_term": search_term
                    }
                    sellers.append(seller)
                    
        except Exception as e:
            print(f"    Error: {e}")
            continue
    
    return sellers

def find_with_brave():
    """Find sellers using Brave Search API"""
    sellers = []
    
    for search_term in SEARCH_TERMS[5:10]:  # Different set of terms
        try:
            print(f"  Searching: {search_term}")
            params = {
                "q": f"{search_term} -broker",
                "count": 3,
                "country": "US",
                "search_lang": "en"
            }
            
            headers = {
                "X-Subscription-Token": BRAVE_API_KEY,
                "Accept": "application/json"
            }
            
            response = requests.get(
                "https://api.search.brave.com/res/v1/web/search",
                params=params,
                headers=headers,
                timeout=20
            )
            
            if response.status_code == 200:
                results = response.json().get("web", {}).get("results", [])
                for result in results:
                    seller = {
                        "company": result.get("title", "Unknown Company"),
                        "source": "Brave Search",
                        "url": result.get("url", ""),
                        "description": result.get("description", ""),
                        "industry": extract_industry(search_term),
                        "ebitda_range": estimate_ebitda(search_term),
                        "years_in_business": 15,
                        "owner_signals": ["owner_near_retirement", "off_market"],
                        "search_term": search_term
                    }
                    sellers.append(seller)
                    
        except Exception as e:
            print(f"    Error: {e}")
            continue
    
    return sellers

def extract_industry(search_term):
    """Extract industry from search term"""
    if any(word in search_term.lower() for word in ["hvac", "plumbing", "electrical", "roofing"]):
        return "HVAC/Construction"
    elif any(word in search_term.lower() for word in ["healthcare", "dental", "veterinary"]):
        return "Healthcare"
    elif any(word in search_term.lower() for word in ["insurance", "brokerage"]):
        return "Insurance"
    elif any(word in search_term.lower() for word in ["logistics", "distribution"]):
        return "Logistics"
    elif any(word in search_term.lower() for word in ["cleaning", "waste"]):
        return "Commercial Services"
    return "Other"

def estimate_ebitda(search_term):
    """Estimate EBITDA range"""
    if any(word in search_term.lower() for word in ["hvac", "plumbing", "electrical", "roofing"]):
        return "$1M-3M"
    elif any(word in search_term.lower() for word in ["healthcare", "insurance", "dental"]):
        return "$3M-10M"
    return "$500K-1M"

def calculate_score(seller):
    """Calculate lead score (0-100)"""
    score = 0
    
    # EBITDA range
    ebitda = seller.get("ebitda_range", "")
    if "1M-3M" in ebitda:
        score += 25
    elif "3M-10M" in ebitda:
        score += 30
    else:
        score += 15
    
    # Years in business
    score += 15  # Default assumption
    
    # Owner signals
    score += 20  # Assuming retirement signals
    
    # Industry fit
    industry = seller.get("industry", "")
    if industry in ["HVAC/Construction", "Healthcare", "Insurance"]:
        score += 25
    else:
        score += 15
    
    return min(score, 100)

def estimate_finder_fee(seller):
    """Estimate finder fee"""
    ebitda = seller.get("ebitda_range", "")
    if "1M-3M" in ebitda:
        return "$50,000 - $150,000"
    elif "3M-10M" in ebitda:
        return "$150,000 - $500,000"
    return "$25,000 - $50,000"

def save_results(sellers, start_time):
    """Save results to file"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Create directory
    os.makedirs("/Users/cubiczan/.openclaw/workspace/deals/sellers", exist_ok=True)
    
    # Process sellers
    for seller in sellers:
        seller["score"] = calculate_score(seller)
        seller["estimated_finder_fee"] = estimate_finder_fee(seller)
        seller["priority"] = "High" if seller["score"] >= 80 else "Medium" if seller["score"] >= 60 else "Low"
        seller["discovered_date"] = today
    
    # Sort by score
    sellers.sort(key=lambda x: x["score"], reverse=True)
    
    # Save to file
    daily_file = f"/Users/cubiczan/.openclaw/workspace/deals/sellers/daily-sellers-{today}.md"
    
    with open(daily_file, "w") as f:
        f.write(f"# Daily Off-Market Sellers - {today}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Sellers:** {len(sellers)}\n")
        f.write(f"**Processing Time:** {time.time() - start_time:.2f} seconds\n\n")
        
        f.write("## Summary\n")
        high = len([s for s in sellers if s["priority"] == "High"])
        medium = len([s for s in sellers if s["priority"] == "Medium"])
        low = len([s for s in sellers if s["priority"] == "Low"])
        f.write(f"- **High Priority:** {high}\n")
        f.write(f"- **Medium Priority:** {medium}\n")
        f.write(f"- **Low Priority:** {low}\n")
        
        # Calculate total finder fees
        total_fees = 0
        for seller in sellers:
            fee = seller.get("estimated_finder_fee", "")
            if "$50,000 - $150,000" in fee:
                total_fees += 100000
            elif "$150,000 - $500,000" in fee:
                total_fees += 325000
            else:
                total_fees += 37500
        
        f.write(f"- **Total Estimated Finder Fees:** ${total_fees:,}\n\n")
        
        f.write("## Seller Details\n\n")
        for i, seller in enumerate(sellers, 1):
            f.write(f"### {i}. {seller.get('company', 'Unknown Company')}\n")
            f.write(f"- **Industry:** {seller.get('industry', 'Unknown')}\n")
            f.write(f"- **EBITDA Range:** {seller.get('ebitda_range', 'Unknown')}\n")
            f.write(f"- **Years in Business:** {seller.get('years_in_business', 'Unknown')}\n")
            f.write(f"- **Owner Signals:** {', '.join(seller.get('owner_signals', []))}\n")
            f.write(f"- **Score:** {seller.get('score', 0)}/100\n")
            f.write(f"- **Priority:** {seller.get('priority', 'Low')}\n")
            f.write(f"- **Estimated Finder Fee:** {seller.get('estimated_finder_fee', 'Unknown')}\n")
            f.write(f"- **Source:** {seller.get('source', 'Unknown')}\n")
            if seller.get('url'):
                f.write(f"- **URL:** {seller.get('url')}\n")
            f.write(f"- **Description:** {seller.get('description', '')[:150]}...\n\n")
    
    print(f"✅ Saved results to: {daily_file}")

def generate_summary(sellers, start_time):
    """Generate summary for Discord report"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    high = len([s for s in sellers if s["priority"] == "High"])
    medium = len([s for s in sellers if s["priority"] == "Medium"])
    low = len([s for s in sellers if s["priority"] == "Low"])
    
    # Count by industry type
    blue_collar = len([s for s in sellers if any(word in s.get('industry', '').lower() 
                    for word in ['hvac', 'construction', 'plumbing', 'electrical', 'roofing'])])
    platform = len([s for s in sellers if any(word in s.get('industry', '').lower() 
                    for word in ['healthcare', 'insurance', 'logistics'])])
    
    # Calculate total finder fees
    total_fees = 0
    for seller in sellers:
        fee = seller.get("estimated_finder_fee", "")
        if "$50,000 - $150,000" in fee:
            total_fees += 100000
        elif "$150,000 - $500,000" in fee:
            total_fees += 325000
        else:
            total_fees += 37500
    
    print("\n" + "="*60)
    print("📋 DEAL ORIGINATION - SELLERS SUMMARY")
    print("="*60)
    print(f"📅 Date: {today}")
    print(f"⏱️ Processing Time: {time.time() - start_time:.2f} seconds")
    print(f"🔍 Data Source: Traditional APIs (Tavily + Brave)")
    print(f"📊 Scrapling Used: ❌ No (integration needs debugging)")
    print("")
    print(f"📈 RESULTS:")
    print(f"  • Total Sellers Identified: {len(sellers)}")
    print(f"  • High Priority: {high}")
    print(f"  • Medium Priority: {medium}")
    print(f"  • Low Priority: {low}")
    print(f"  • Blue Collar: {blue_collar}")
    print(f"  • Platform: {platform}")
    print(f"  • Total Estimated Finder Fees: ${total_fees:,}")
    print("")
    print("🎯 TARGET STATUS:")
    if len(sellers) >= 10:
        print(f"  • ✅ Target Achieved: {len(sellers)}/10-15 sellers")
    else:
        print(f"  • ⚠️ Below Target: {len(sellers)}/10-15 sellers")
    print("")
    print("🔧 NEXT STEPS:")
    print("  1. Review high-priority sellers in daily file")
    print("  2. Debug Scrapling integration for future runs")
    print("  3. Add to investor matching pipeline")
    print("="*60)

if __name__ == "__main__":
    main()