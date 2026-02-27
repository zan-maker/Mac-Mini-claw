#!/usr/bin/env python3
"""
Deal Origination - Sellers Lead Generation
Scrapling-First Approach with API Fallbacks
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add scrapling integration to path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

# Configuration
TAVILY_API_KEY = "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"
BRAVE_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"

# Track data sources
data_source_report = {
    "scrapling_used": False,
    "scrapling_results": 0,
    "tavily_results": 0,
    "brave_results": 0,
    "start_time": datetime.now(),
    "errors": []
}

# Search terms for off-market sellers
SEARCH_TERMS = [
    "HVAC business for sale owner retiring off market",
    "plumbing company owner retirement selling",
    "electrical contractor business for sale direct owner",
    "commercial cleaning business owner exit selling",
    "healthcare services business acquisition opportunity",
    "dental practice owner retiring selling",
    "veterinary clinic for sale owner looking to exit",
    "insurance brokerage business for sale owner retiring",
    "logistics company acquisition opportunity direct sale",
    "roofing business owner retirement off market",
    "fire safety company for sale established business",
    "waste management business acquisition opportunity"
]


def score_seller_lead(lead: dict) -> int:
    """Score seller lead 0-100 based on deal origination criteria."""
    score = 0
    
    # EBITDA range (0-30 points)
    ebitda = lead.get("ebitda", 0)
    if isinstance(ebitda, str):
        ebitda = float(ebitda.replace("$", "").replace("M", "").replace("K", "000"))
    if ebitda >= 10:
        score += 30
    elif ebitda >= 5:
        score += 25
    elif ebitda >= 2:
        score += 20
    elif ebitda >= 1:
        score += 15
    elif ebitda >= 0.5:
        score += 10
    
    # Years in business (0-20 points)
    years = lead.get("years_in_business", 0)
    if years >= 25:
        score += 20
    elif years >= 20:
        score += 18
    elif years >= 15:
        score += 15
    elif years >= 10:
        score += 10
    elif years >= 5:
        score += 5
    
    # Owner retirement signals (0-25 points)
    retirement_signals = lead.get("retirement_signals", [])
    if "owner_retiring" in retirement_signals:
        score += 15
    if "second_generation" in retirement_signals:
        score += 10
    if "outdated_branding" in retirement_signals:
        score += 5
    if "high_reviews_low_marketing" in retirement_signals:
        score += 5
    if "no_broker" in retirement_signals:
        score += 10
    
    # Segment fit (0-25 points)
    industry = lead.get("industry", "").lower()
    blue_collar = ["hvac", "plumbing", "electrical", "roofing", "fire", "cleaning", "waste"]
    platform = ["healthcare", "dental", "veterinary", "insurance", "logistics"]
    
    if any(b in industry for b in blue_collar):
        score += 25
    elif any(p in industry for p in platform):
        score += 20
    else:
        score += 10
    
    return min(score, 100)


def estimate_finder_fee(ebitda: float) -> str:
    """Estimate finder fee based on EBITDA (typically 2-5% of deal value)."""
    # Deal value typically 4-6x EBITDA
    deal_value = ebitda * 5
    # Finder fee typically 2-5%
    min_fee = deal_value * 0.02
    max_fee = deal_value * 0.05
    return f"${min_fee/1000000:.1f}M - ${max_fee/1000000:.1f}M"


async def try_scrapling():
    """Try to use Scrapling for lead generation."""
    global data_source_report
    
    print("🔄 Attempting Scrapling integration...")
    
    try:
        from cron_integration import ScraplingCronIntegration
        
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if success:
            print("✅ Scrapling initialized successfully")
            data_source_report["scrapling_used"] = True
            
            # Try to find sellers using Scrapling
            sellers = await scrapling.find_off_market_sellers(SEARCH_TERMS[:5])
            
            if sellers:
                data_source_report["scrapling_results"] = len(sellers)
                print(f"✅ Scrapling found {len(sellers)} sellers")
                return sellers
            else:
                print("⚠️ Scrapling returned no results")
                data_source_report["errors"].append("Scrapling returned no results")
        else:
            print("⚠️ Scrapling initialization failed")
            data_source_report["errors"].append("Scrapling initialization failed")
            
    except ImportError as e:
        print(f"⚠️ Scrapling not available: {e}")
        data_source_report["errors"].append(f"ImportError: {e}")
    except AttributeError as e:
        print(f"⚠️ Scrapling method not found: {e}")
        data_source_report["errors"].append(f"AttributeError: {e}")
    except Exception as e:
        print(f"⚠️ Scrapling error: {e}")
        data_source_report["errors"].append(f"Exception: {e}")
    
    return []


async def try_tavily():
    """Fall back to Tavily API."""
    global data_source_report
    
    print("🔄 Falling back to Tavily API...")
    
    try:
        import aiohttp
        
        sellers = []
        
        async with aiohttp.ClientSession() as session:
            for query in SEARCH_TERMS[:8]:  # Limit to 8 queries
                try:
                    url = "https://api.tavily.com/search"
                    payload = {
                        "api_key": TAVILY_API_KEY,
                        "query": query,
                        "search_depth": "advanced",
                        "max_results": 5
                    }
                    
                    async with session.post(url, json=payload) as response:
                        if response.status == 200:
                            data = await response.json()
                            results = data.get("results", [])
                            
                            for result in results:
                                seller = parse_search_result(result, query)
                                if seller and not is_broker(seller):
                                    sellers.append(seller)
                                    
                except Exception as e:
                    print(f"  Tavily query error: {e}")
                    continue
        
        data_source_report["tavily_results"] = len(sellers)
        print(f"✅ Tavily found {len(sellers)} sellers")
        return sellers
        
    except Exception as e:
        print(f"❌ Tavily API error: {e}")
        data_source_report["errors"].append(f"Tavily error: {e}")
        return []


async def try_brave():
    """Fall back to Brave Search API."""
    global data_source_report
    
    print("🔄 Falling back to Brave Search API...")
    
    try:
        import aiohttp
        
        sellers = []
        
        async with aiohttp.ClientSession() as session:
            for query in SEARCH_TERMS[:8]:
                try:
                    url = "https://api.search.brave.com/res/v1/web/search"
                    headers = {
                        "Accept": "application/json",
                        "X-Subscription-Token": BRAVE_API_KEY
                    }
                    params = {
                        "q": query,
                        "count": 5
                    }
                    
                    async with session.get(url, headers=headers, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            results = data.get("web", {}).get("results", [])
                            
                            for result in results:
                                seller = parse_search_result(result, query)
                                if seller and not is_broker(seller):
                                    sellers.append(seller)
                                    
                except Exception as e:
                    print(f"  Brave query error: {e}")
                    continue
        
        data_source_report["brave_results"] = len(sellers)
        print(f"✅ Brave found {len(sellers)} sellers")
        return sellers
        
    except Exception as e:
        print(f"❌ Brave API error: {e}")
        data_source_report["errors"].append(f"Brave error: {e}")
        return []


def parse_search_result(result: dict, query: str) -> dict:
    """Parse search result into seller lead."""
    title = result.get("title", "")
    description = result.get("description", "") or result.get("snippet", "")
    url = result.get("url", "") or result.get("link", "")
    
    # Determine industry from query
    industry = "Other"
    if "hvac" in query.lower():
        industry = "HVAC"
    elif "plumbing" in query.lower():
        industry = "Plumbing"
    elif "electrical" in query.lower():
        industry = "Electrical"
    elif "roofing" in query.lower():
        industry = "Roofing"
    elif "cleaning" in query.lower():
        industry = "Commercial Cleaning"
    elif "healthcare" in query.lower():
        industry = "Healthcare"
    elif "dental" in query.lower():
        industry = "Dental"
    elif "veterinary" in query.lower():
        industry = "Veterinary"
    elif "insurance" in query.lower():
        industry = "Insurance Brokerage"
    elif "logistics" in query.lower():
        industry = "Logistics"
    elif "waste" in query.lower():
        industry = "Waste Management"
    elif "fire" in query.lower() or "safety" in query.lower():
        industry = "Fire/Safety"
    
    # Extract company name from title
    company_name = title.split("-")[0].split("|")[0].strip()
    
    # Estimate EBITDA based on industry
    ebitda_estimates = {
        "HVAC": 1.5,
        "Plumbing": 1.2,
        "Electrical": 1.8,
        "Roofing": 2.0,
        "Commercial Cleaning": 0.8,
        "Healthcare": 3.5,
        "Dental": 1.5,
        "Veterinary": 1.2,
        "Insurance Brokerage": 2.5,
        "Logistics": 4.0,
        "Waste Management": 3.0,
        "Fire/Safety": 1.8,
        "Other": 1.0
    }
    
    ebitda = ebitda_estimates.get(industry, 1.0)
    
    # Detect retirement signals
    retirement_signals = []
    text = (title + " " + description).lower()
    
    if "retiring" in text or "retirement" in text or "exit" in text:
        retirement_signals.append("owner_retiring")
    if "family" in text or "second generation" in text or "established" in text:
        retirement_signals.append("second_generation")
    if "founded" in text and ("1980" in text or "1990" in text or "1970" in text):
        retirement_signals.append("long_established")
    
    # Estimate years in business
    years_in_business = 20  # Default
    if "retiring" in text or "retirement" in text:
        years_in_business = 25
    elif "established" in text:
        years_in_business = 22
    
    seller = {
        "company_name": company_name,
        "industry": industry,
        "ebitda": ebitda,
        "years_in_business": years_in_business,
        "retirement_signals": retirement_signals,
        "source_url": url,
        "description": description[:200] if description else "",
        "is_broker": is_broker_text(title + " " + description),
        "segment": "Blue Collar" if industry in ["HVAC", "Plumbing", "Electrical", "Roofing", "Commercial Cleaning", "Waste Management", "Fire/Safety"] else "Platform"
    }
    
    # Calculate score
    seller["score"] = score_seller_lead(seller)
    seller["finder_fee"] = estimate_finder_fee(ebitda)
    
    return seller


def is_broker_text(text: str) -> bool:
    """Check if text indicates a broker listing."""
    broker_keywords = [
        "broker", "bizbuysell", "businessesforsale", "listed for sale",
        "listing", "asking price", "multiples", "brokerage firm",
        "mergers and acquisitions", "investment bank selling"
    ]
    text_lower = text.lower()
    return any(kw in text_lower for kw in broker_keywords)


def is_broker(seller: dict) -> bool:
    """Check if seller is a broker listing."""
    if seller.get("is_broker"):
        return True
    url = seller.get("source_url", "").lower()
    broker_domains = ["bizbuysell", "businessesforsale", "bizquest", "loopnet"]
    return any(domain in url for domain in broker_domains)


def save_results(sellers: list):
    """Save results to files."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Create directories
    Path("/Users/cubiczan/.openclaw/workspace/deals/sellers").mkdir(parents=True, exist_ok=True)
    
    # Save daily file
    daily_file = f"/Users/cubiczan/.openclaw/workspace/deals/sellers/daily-sellers-{today}.md"
    
    with open(daily_file, "w") as f:
        f.write(f"# Daily Sellers Report - {today}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Data source report
        f.write("## 🔍 Data Source Report\n\n")
        f.write(f"- **Scrapling Used:** {'✅ Yes' if data_source_report['scrapling_used'] else '❌ No'}\n")
        f.write(f"- **Scrapling Results:** {data_source_report['scrapling_results']} sellers\n")
        f.write(f"- **Tavily Results:** {data_source_report['tavily_results']} sellers\n")
        f.write(f"- **Brave Results:** {data_source_report['brave_results']} sellers\n")
        elapsed = (datetime.now() - data_source_report['start_time']).total_seconds()
        f.write(f"- **Total Processing Time:** {elapsed:.1f} seconds\n\n")
        
        if data_source_report['errors']:
            f.write("**Errors:**\n")
            for err in data_source_report['errors']:
                f.write(f"- {err}\n")
            f.write("\n")
        
        # Summary
        high_priority = [s for s in sellers if s["score"] >= 70]
        blue_collar = [s for s in sellers if s["segment"] == "Blue Collar"]
        platform = [s for s in sellers if s["segment"] == "Platform"]
        
        f.write("## Summary\n\n")
        f.write(f"- **Total Sellers:** {len(sellers)}\n")
        f.write(f"- **High Priority (70+):** {len(high_priority)}\n")
        f.write(f"- **Blue Collar:** {len(blue_collar)}\n")
        f.write(f"- **Platform:** {len(platform)}\n\n")
        
        # Seller details
        f.write("## Seller Leads\n\n")
        
        for i, seller in enumerate(sorted(sellers, key=lambda x: x["score"], reverse=True), 1):
            f.write(f"### {i}. {seller['company_name']}\n\n")
            f.write(f"| Attribute | Value |\n")
            f.write(f"|-----------|-------|\n")
            f.write(f"| Industry | {seller['industry']} |\n")
            f.write(f"| Segment | {seller['segment']} |\n")
            f.write(f"| EBITDA | ${seller['ebitda']}M |\n")
            f.write(f"| Years in Business | {seller['years_in_business']} |\n")
            f.write(f"| Score | {seller['score']}/100 |\n")
            f.write(f"| Priority | {'🔴 High' if seller['score'] >= 70 else '🟡 Medium' if seller['score'] >= 50 else '🟢 Low'} |\n")
            f.write(f"| Est. Finder Fee | {seller['finder_fee']} |\n")
            f.write(f"| Source | {seller['source_url']} |\n\n")
            
            if seller['retirement_signals']:
                f.write(f"**Retirement Signals:** {', '.join(seller['retirement_signals'])}\n\n")
            
            if seller['description']:
                f.write(f"**Description:** {seller['description']}\n\n")
            
            f.write("---\n\n")
    
    print(f"✅ Saved daily report: {daily_file}")
    
    # Update pipeline
    pipeline_file = "/Users/cubiczan/.openclaw/workspace/deals/pipeline.md"
    
    # Read existing pipeline or create new
    existing_content = ""
    if os.path.exists(pipeline_file):
        with open(pipeline_file, "r") as f:
            existing_content = f.read()
    
    # Add today's summary
    with open(pipeline_file, "w") as f:
        f.write("# Deal Pipeline\n\n")
        f.write(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Seller pipeline
        f.write("## Active Seller Pipeline\n\n")
        
        high_priority = [s for s in sellers if s["score"] >= 70]
        medium_priority = [s for s in sellers if 50 <= s["score"] < 70]
        
        f.write(f"**High Priority ({len(high_priority)}):**\n")
        for s in high_priority:
            f.write(f"- {s['company_name']} ({s['industry']}, ${s['ebitda']}M EBITDA, Fee: {s['finder_fee']})\n")
        
        f.write(f"\n**Medium Priority ({len(medium_priority)}):**\n")
        for s in medium_priority[:5]:
            f.write(f"- {s['company_name']} ({s['industry']}, ${s['ebitda']}M EBITDA)\n")
        
        f.write("\n---\n\n")
        f.write(existing_content)
    
    print(f"✅ Updated pipeline: {pipeline_file}")
    
    return daily_file


async def main():
    """Main execution."""
    print("=" * 60)
    print("🚀 Deal Origination - Sellers Lead Generation")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    sellers = []
    
    # Step 1: Try Scrapling
    sellers = await try_scrapling()
    
    # Step 2: Fall back to Tavily if needed
    if len(sellers) < 10:
        tavily_sellers = await try_tavily()
        sellers.extend(tavily_sellers)
    
    # Step 3: Fall back to Brave if still not enough
    if len(sellers) < 10:
        brave_sellers = await try_brave()
        sellers.extend(brave_sellers)
    
    # Deduplicate by company name
    seen = set()
    unique_sellers = []
    for s in sellers:
        name = s.get("company_name", "").lower()
        if name and name not in seen:
            seen.add(name)
            unique_sellers.append(s)
    
    sellers = unique_sellers[:15]  # Limit to 15
    
    print(f"\n📊 Total unique sellers found: {len(sellers)}")
    
    if sellers:
        # Save results
        save_results(sellers)
        
        # Print summary for Discord
        print("\n" + "=" * 60)
        print("📋 DISCORD SUMMARY")
        print("=" * 60)
        
        high_priority = len([s for s in sellers if s["score"] >= 70])
        blue_collar = len([s for s in sellers if s["segment"] == "Blue Collar"])
        platform = len([s for s in sellers if s["segment"] == "Platform"])
        
        # Calculate total finder fees
        total_min_fee = 0
        total_max_fee = 0
        for s in sellers:
            fee_range = s.get("finder_fee", "$0M - $0M")
            try:
                parts = fee_range.replace("$", "").replace("M", "").split(" - ")
                total_min_fee += float(parts[0])
                total_max_fee += float(parts[1])
            except:
                pass
        
        elapsed = (datetime.now() - data_source_report["start_time"]).total_seconds()
        
        print(f"**Daily Sellers Report - {datetime.now().strftime('%Y-%m-%d')}**")
        print()
        print(f"📊 **Summary:**")
        print(f"- **Total Sellers:** {len(sellers)}")
        print(f"- **High Priority:** {high_priority}")
        print(f"- **Blue Collar:** {blue_collar}")
        print(f"- **Platform:** {platform}")
        print(f"- **Est. Finder Fees:** ${total_min_fee:.1f}M - ${total_max_fee:.1f}M")
        print()
        print(f"🔍 **Data Source Report:**")
        print(f"- Scrapling Used: {'✅ Yes' if data_source_report['scrapling_used'] else '❌ No'}")
        print(f"- Scrapling Results: {data_source_report['scrapling_results']} sellers")
        print(f"- Tavily Results: {data_source_report['tavily_results']} sellers")
        print(f"- Brave Results: {data_source_report['brave_results']} sellers")
        print(f"- Processing Time: {elapsed:.1f}s")
        print()
        print("**Top 3 Sellers:**")
        for s in sorted(sellers, key=lambda x: x["score"], reverse=True)[:3]:
            print(f"1. **{s['company_name']}** - {s['industry']} (${s['ebitda']}M EBITDA, Score: {s['score']})")
        
        return {
            "success": True,
            "total_sellers": len(sellers),
            "high_priority": high_priority,
            "blue_collar": blue_collar,
            "platform": platform,
            "total_min_fee": total_min_fee,
            "total_max_fee": total_max_fee,
            "elapsed": elapsed,
            "data_source": data_source_report,
            "sellers": sellers
        }
    else:
        print("❌ No sellers found")
        return {
            "success": False,
            "total_sellers": 0,
            "data_source": data_source_report
        }


if __name__ == "__main__":
    result = asyncio.run(main())
    print(json.dumps(result, indent=2, default=str))
