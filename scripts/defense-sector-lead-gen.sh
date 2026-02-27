#!/bin/bash
# Defense Sector Lead Gen - Using Tavily/Brave APIs
# Date: 2026-02-24

set -e

TAVILY_KEY="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"
BRAVE_KEY="cac43a248afb1cc1ec004370df2e0282a67eb420"
OUTPUT_DIR="/Users/cubiczan/.openclaw/workspace/defense-leads"
TODAY=$(date +"%Y-%m-%d")
START_TIME=$(date +%s)

mkdir -p "$OUTPUT_DIR"

echo "============================================================"
echo "🛡️  Defense Sector Lead Gen - API-Based"
echo "============================================================"
echo "Started: $(date)"
echo ""

# Temp files
COMPANIES_TEMP=$(mktemp)
INVESTORS_TEMP=$(mktemp)

# Part 1: Defense Companies (US/UK/EU)
echo "📍 Part 1: Defense Companies (US/UK/EU)"
echo "------------------------------------------------------------"

# Defense company queries
DEFENSE_QUERIES=(
    "defense technology companies Series A B C funding US UK EU"
    "cybersecurity military defense companies early stage"
    "counter-drone C-UAS anti-drone systems companies"
    "space defense satellite technology startups"
    "military AI machine learning defense companies"
)

tavily_count=0
brave_count=0

for query in "${DEFENSE_QUERIES[@]}"; do
    echo "🔍 Searching: $query"
    
    # Try Tavily first
    response=$(curl -s -X POST "https://api.tavily.com/search" \
        -H "Content-Type: application/json" \
        -d "{
            \"api_key\": \"$TAVILY_KEY\",
            \"query\": \"$query\",
            \"search_depth\": \"advanced\",
            \"max_results\": 10
        }" 2>/dev/null || echo "")
    
    if [ -n "$response" ] && [ "$response" != "" ]; then
        # Parse results
        echo "$response" | jq -r '.results[] | "\(.title)|\(.url)|\(.content)|Tavily"' >> "$COMPANIES_TEMP" 2>/dev/null || true
        tavily_count=$((tavily_count + 1))
        echo "  ✅ Tavily: Found results"
    else
        # Fall back to Brave
        echo "  ⚠️ Tavily failed, trying Brave..."
        
        response=$(curl -s "https://api.search.brave.com/res/v1/web/search" \
            -H "X-Subscription-Token: $BRAVE_KEY" \
            -G \
            --data-urlencode "q=$query" \
            -d "count=10" 2>/dev/null || echo "")
        
        if [ -n "$response" ]; then
            echo "$response" | jq -r '.web.results[] | "\(.title)|\(.url)|\(.description)|Brave"' >> "$COMPANIES_TEMP" 2>/dev/null || true
            brave_count=$((brave_count + 1))
            echo "  ✅ Brave: Found results"
        fi
    fi
    
    sleep 1
done

echo ""
echo "📍 Part 2: PE/VC Funds (Asia/India)"
echo "------------------------------------------------------------"

# PE/VC queries (EXCLUDING CHINA)
INVESTOR_QUERIES=(
    "private equity defense drone aerospace investment Asia India Singapore"
    "venture capital military technology autonomous systems Japan Korea"
    "PE fund dual-use technology surveillance India Middle East"
    "defense tech investor UAV drone funding Taiwan Southeast Asia"
)

for query in "${INVESTOR_QUERIES[@]}"; do
    echo "🔍 Searching: $query"
    
    # Try Tavily first
    response=$(curl -s -X POST "https://api.tavily.com/search" \
        -H "Content-Type: application/json" \
        -d "{
            \"api_key\": \"$TAVILY_KEY\",
            \"query\": \"$query\",
            \"search_depth\": \"advanced\",
            \"max_results\": 10
        }" 2>/dev/null || echo "")
    
    if [ -n "$response" ] && [ "$response" != "" ]; then
        # Parse and filter out China
        echo "$response" | jq -r '.results[] | select(.url | test("china") | not) | select(.content | test("china"; "i") | not) | "\(.title)|\(.url)|\(.content)|Tavily"' >> "$INVESTORS_TEMP" 2>/dev/null || true
        echo "  ✅ Tavily: Found results"
    else
        # Fall back to Brave
        echo "  ⚠️ Tavily failed, trying Brave..."
        
        response=$(curl -s "https://api.search.brave.com/res/v1/web/search" \
            -H "X-Subscription-Token: $BRAVE_KEY" \
            -G \
            --data-urlencode "q=$query" \
            -d "count=10" 2>/dev/null || echo "")
        
        if [ -n "$response" ]; then
            echo "$response" | jq -r '.web.results[] | select(.url | test("china") | not) | select(.description | test("china"; "i") | not) | "\(.title)|\(.url)|\(.description)|Brave"' >> "$INVESTORS_TEMP" 2>/dev/null || true
            echo "  ✅ Brave: Found results"
        fi
    fi
    
    sleep 1
done

echo ""
echo "============================================================"
echo "📊 Processing Results..."
echo "============================================================"

# Process companies with Python for scoring
python3 << 'PYTHON_SCRIPT' "$COMPANIES_TEMP" "$INVESTORS_TEMP" "$OUTPUT_DIR" "$TODAY"
import sys
import re
from datetime import datetime
from collections import defaultdict

companies_file = sys.argv[1]
investors_file = sys.argv[2]
output_dir = sys.argv[3]
today = sys.argv[4]

def score_defense_company(desc):
    """Score defense company (0-100)."""
    score = 0
    desc_lower = desc.lower()
    
    # Sector fit (30 points)
    sector_keywords = {
        "cybersecurity": 30, "counter-drone": 30, "c-uas": 30, "anti-drone": 30,
        "defense": 25, "military": 25, "drone": 20, "space": 20, "satellite": 20,
        "surveillance": 20, "ai": 15, "autonomous": 15, "security": 15
    }
    for keyword, points in sector_keywords.items():
        if keyword in desc_lower:
            score = max(score, min(points, 30))
            break
    
    # Stage fit (20 points)
    if any(kw in desc_lower for kw in ["series a", "series b", "series c", "early stage", "funding", "raised"]):
        score += 20
    
    # Technical depth (20 points)
    tech_keywords = ["ai", "ml", "autonomous", "sensor", "satellite", "encryption", "quantum"]
    tech_count = sum(1 for kw in tech_keywords if kw in desc_lower)
    score += min(tech_count * 5, 20)
    
    # Integration potential (20 points)
    if any(kw in desc_lower for kw in ["platform", "api", "integration", "modular"]):
        score += 20
    
    # Region match (10 points)
    if any(kw in desc_lower for kw in ["us", "united states", "uk", "europe", "eu", "germany", "france"]):
        score += 10
    
    return min(score, 100)

def score_pe_fund(desc):
    """Score PE/VC fund (0-100)."""
    score = 0
    desc_lower = desc.lower()
    
    # Defense/drone focus (40 points)
    defense_keywords = ["defense", "military", "drone", "uav", "aerospace", "autonomous", "surveillance"]
    defense_count = sum(1 for kw in defense_keywords if kw in desc_lower)
    score += min(defense_count * 8, 40)
    
    # Region match (20 points)
    if any(kw in desc_lower for kw in ["india", "singapore", "japan", "korea", "taiwan", "southeast", "middle east"]):
        score += 20
    
    # Portfolio fit (20 points)
    if any(kw in desc_lower for kw in ["portfolio", "investment", "backed", "funded"]):
        score += 20
    
    # Fund size/stage (20 points)
    if any(kw in desc_lower for kw in ["early stage", "growth", "venture", "series"]):
        score += 20
    
    return min(score, 100)

# Parse companies
companies = []
seen_companies = set()

with open(companies_file, 'r') as f:
    for line in f:
        parts = line.strip().split('|')
        if len(parts) >= 4:
            name = parts[0].split(' - ')[0].split(' | ')[0].strip()
            url = parts[1]
            desc = parts[2]
            source = parts[3]
            
            # Deduplicate
            name_lower = name.lower()
            if name_lower not in seen_companies and len(name) > 2:
                seen_companies.add(name_lower)
                score = score_defense_company(desc)
                companies.append({
                    'name': name,
                    'url': url,
                    'desc': desc,
                    'source': source,
                    'score': score
                })

# Sort and take top 10
companies.sort(key=lambda x: x['score'], reverse=True)
top_companies = companies[:10]

# Parse investors
investors = []
seen_investors = set()

with open(investors_file, 'r') as f:
    for line in f:
        parts = line.strip().split('|')
        if len(parts) >= 4:
            name = parts[0].split(' - ')[0].split(' | ')[0].strip()
            url = parts[1]
            desc = parts[2]
            source = parts[3]
            
            # Deduplicate
            name_lower = name.lower()
            if name_lower not in seen_investors and len(name) > 2:
                seen_investors.add(name_lower)
                score = score_pe_fund(desc)
                investors.append({
                    'name': name,
                    'url': url,
                    'desc': desc,
                    'source': source,
                    'score': score
                })

# Sort and take top 5
investors.sort(key=lambda x: x['score'], reverse=True)
top_investors = investors[:5]

# Write companies file
with open(f"{output_dir}/daily-companies-{today}.md", 'w') as f:
    f.write(f"# Defense Companies - {today}\n\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"**Total Leads:** {len(top_companies)}\n\n")
    
    for i, company in enumerate(top_companies, 1):
        priority = "🟢 HIGH" if company['score'] >= 70 else "🟡 MEDIUM" if company['score'] >= 50 else "🔴 LOW"
        f.write(f"## {i}. {company['name']}\n")
        f.write(f"**Score:** {company['score']}/100 {priority}\n")
        f.write(f"**URL:** {company['url']}\n")
        f.write(f"**Description:** {company['desc'][:200]}...\n")
        f.write(f"**Source:** {company['source']}\n\n")

# Write investors file
with open(f"{output_dir}/daily-investors-{today}.md", 'w') as f:
    f.write(f"# PE/VC Investors (Asia/India) - {today}\n\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"**Total Funds:** {len(top_investors)}\n\n")
    
    for i, investor in enumerate(top_investors, 1):
        priority = "🟢 HIGH" if investor['score'] >= 70 else "🟡 MEDIUM" if investor['score'] >= 50 else "🔴 LOW"
        f.write(f"## {i}. {investor['name']}\n")
        f.write(f"**Score:** {investor['score']}/100 {priority}\n")
        f.write(f"**URL:** {investor['url']}\n")
        f.write(f"**Description:** {investor['desc'][:200]}...\n")
        f.write(f"**Source:** {investor['source']}\n\n")

# Print summary
print(f"✅ Defense Companies: {len(top_companies)}")
print(f"   - High Priority (70+): {sum(1 for c in top_companies if c['score'] >= 70)}")
print(f"   - Medium Priority (50-69): {sum(1 for c in top_companies if 50 <= c['score'] < 70)}")
print(f"")
print(f"✅ PE/VC Funds: {len(top_investors)}")
print(f"   - High Priority (70+): {sum(1 for i in top_investors if i['score'] >= 70)}")
print(f"")
print("Top 3 Companies:")
for c in top_companies[:3]:
    print(f"  - {c['name']} (Score: {c['score']})")
print("")
print("Top 3 Investors:")
for i in top_investors[:3]:
    print(f"  - {i['name']} (Score: {i['score']})")

# Write Discord report
high_priority_companies = sum(1 for c in top_companies if c['score'] >= 70)
high_priority_investors = sum(1 for i in top_investors if i['score'] >= 60)

top_3_companies_str = ", ".join([f"{c['name']} ({c['score']})" for c in top_companies[:3]]) if top_companies else "None found"
top_3_investors_str = ", ".join([f"{i['name']} ({i['score']})" for i in top_investors[:3]]) if top_investors else "None found"

discord_report = f"""🛡️ **Defense Sector Report (API-Based)**

## Companies (US/UK/EU)
- Identified: {len(top_companies)}
- High priority (70+): {high_priority_companies}
- Top 3: {top_3_companies_str}

## Investors (Asia/India)
- PE/VC funds: {len(top_investors)}
- Defense-focused: {high_priority_investors}
- Top 3: {top_3_investors_str}

🔍 **Data Source:**
- Scrapling Used: ❌ No (Syntax error in integration)
- Scrapling Results: 0
- Traditional API Results: {len(companies) + len(investors)}
- Processing Time: Will be calculated by bash script"""

with open(f"{output_dir}/discord-report-{today}.txt", 'w') as f:
    f.write(discord_report)

print("")
print("=" * 60)
print("💬 Discord Report:")
print("=" * 60)
print(discord_report)
PYTHON_SCRIPT

# Clean up
rm -f "$COMPANIES_TEMP" "$INVESTORS_TEMP"

END_TIME=$(date +%s)
PROCESSING_TIME=$((END_TIME - START_TIME))

echo ""
echo "✅ Results saved to:"
echo "   - $OUTPUT_DIR/daily-companies-$TODAY.md"
echo "   - $OUTPUT_DIR/daily-investors-$TODAY.md"
echo "   - $OUTPUT_DIR/discord-report-$TODAY.txt"
echo ""
echo "⏱️  Total Processing Time: $PROCESSING_TIME seconds"
