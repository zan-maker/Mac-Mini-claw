#!/usr/bin/env python3
"""
Simplified Enhanced Lead Gen v2 - Quick & Reliable
"""

import json
import requests
from datetime import datetime
import os

# API Keys
TAVILY_API_KEY = "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"
SERPER_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"

def search_tavily(query):
    """Search using Tavily API."""
    print(f"🔍 Searching: {query}")
    
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "max_results": 10
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data.get("results", [])
    except Exception as e:
        print(f"⚠️ Tavily error: {e}")
    
    return []

def search_serper(query):
    """Search using Serper API."""
    print(f"🔍 Searching Serper: {query}")
    
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"q": query}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            results = []
            for item in data.get("organic", []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "content": item.get("snippet", "")
                })
            return results
    except Exception as e:
        print(f"⚠️ Serper error: {e}")
    
    return []

def score_lead(title, content):
    """Simple scoring: 0-100"""
    score = 0
    text = (title + " " + content).lower()
    
    # Industry keywords (25 pts)
    if any(kw in text for kw in ["manufacturing", "technology", "healthcare", "services"]):
        score += 25
    
    # Company indicators (25 pts)
    if any(kw in text for kw in ["company", "corporation", "inc", "llc", "ltd"]):
        score += 25
    
    # Size indicators (25 pts)
    if any(kw in text for kw in ["employees", "staff", "team", "growing"]):
        score += 25
    
    # Contact potential (25 pts)
    if any(kw in text for kw in ["contact", "ceo", "president", "director", "leadership"]):
        score += 25
    
    return min(score, 100)

def main():
    print("🚀 Enhanced Lead Gen v2 - Quick Mode\n")
    start_time = datetime.now()
    
    # Check Scrapling
    scrapling_available = False
    try:
        import sys
        sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')
        from cron_integration import ScraplingCronIntegration
        print("✅ Scrapling module found")
        scrapling_available = True
    except:
        print("⚠️ Scrapling not available, using APIs")
    
    # Search queries
    queries = [
        "manufacturing companies 50-200 employees Texas",
        "technology companies California 20-100 employees",
        "healthcare companies Florida 30-150 employees",
        "professional services firms New York 25-75 employees"
    ]
    
    all_results = []
    api_source = "Tavily"
    
    # Try Tavily first
    for query in queries:
        results = search_tavily(query)
        if results:
            all_results.extend(results)
            print(f"  ✅ Found {len(results)} results")
        else:
            # Fall back to Serper
            api_source = "Serper"
            results = search_serper(query)
            if results:
                all_results.extend(results)
                print(f"  ✅ Found {len(results)} results from Serper")
    
    print(f"\n📊 Total results: {len(all_results)}")
    
    # Process and score leads
    leads = []
    for result in all_results:
        title = result.get("title", "")
        url = result.get("url", "")
        content = result.get("content", "")
        
        if not title or not url:
            continue
        
        score = score_lead(title, content)
        
        leads.append({
            "company_name": title,
            "url": url,
            "description": content,
            "score": score,
            "source": api_source
        })
    
    # Sort by score
    leads.sort(key=lambda x: x["score"], reverse=True)
    
    # Take top 30
    leads = leads[:30]
    
    print(f"📊 Processed {len(leads)} leads")
    
    # Save to file
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = f"/Users/cubiczan/.openclaw/workspace/leads/daily-leads-{today}.md"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w") as f:
        f.write(f"# Daily Leads - {today}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Leads:** {len(leads)}\n")
        high_priority = sum(1 for l in leads if l["score"] >= 70)
        f.write(f"**High Priority (70+):** {high_priority}\n\n")
        f.write("---\n\n")
        
        for i, lead in enumerate(leads, 1):
            emoji = "🔥" if lead["score"] >= 70 else "⭐" if lead["score"] >= 50 else "📌"
            f.write(f"## {emoji} Lead #{i}: {lead['company_name']}\n\n")
            f.write(f"**Score:** {lead['score']}/100\n")
            f.write(f"**Source:** {lead['source']}\n")
            f.write(f"**URL:** {lead['url']}\n\n")
            f.write(f"**Description:**\n{lead['description']}\n\n")
            f.write("---\n\n")
    
    print(f"✅ Saved to {output_file}")
    
    # Generate report
    elapsed = (datetime.now() - start_time).total_seconds()
    
    report = f"""# 🎯 Enhanced Lead Gen Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 🔍 Data Source Report:
- **Scrapling Used:** {'✅ Yes' if scrapling_available else '❌ No (not functional)'}
- **Scrapling Results:** 0 leads
- **Traditional API Results:** {len(leads)} leads (via {api_source})
- **Total Processing Time:** {elapsed:.1f} seconds

## 📊 Summary:
- **Total Found:** {len(leads)}
- **High Priority (70+):** {high_priority}

## 🔥 Top 3 Companies:
"""
    
    for i, lead in enumerate(leads[:3], 1):
        report += f"\n**{i}. {lead['company_name']}** (Score: {lead['score']})\n"
        desc = lead['description'][:100] if lead['description'] else "No description"
        report += f"   • {desc}...\n"
        report += f"   • Source: {lead['source']}\n"
    
    report += f"\n---\n✅ Leads saved to: `/workspace/leads/daily-leads-{today}.md`"
    
    print("\n" + report)
    return report

if __name__ == "__main__":
    main()
