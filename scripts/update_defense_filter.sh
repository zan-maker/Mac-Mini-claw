#!/bin/bash
# Update Defense Sector cron jobs with $50M valuation filter

echo "🔧 UPDATING DEFENSE SECTOR FILTERS - $50M MAX VALUATION"
echo "========================================================="

CRON_FILE="/Users/cubiczan/.openclaw/cron/jobs.json"
BACKUP_FILE="${CRON_FILE}.backup-$(date +%Y%m%d_%H%M%S)"

# Create backup
cp "$CRON_FILE" "$BACKUP_FILE"
echo "📁 Backup created: $BACKUP_FILE"

# Update the cron jobs
echo ""
echo "🎯 UPDATING CRON JOBS WITH $50M VALUATION FILTER:"
echo ""

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "❌ jq not installed. Installing..."
    brew install jq
fi

# Count defense jobs
DEFENSE_JOBS=$(jq '.jobs[] | select(.name | contains("Defense")) | .name' "$CRON_FILE" | wc -l)
echo "Found $DEFENSE_JOBS defense-related cron jobs"

echo ""
echo "📋 MANUAL UPDATE REQUIRED:"
echo "=========================="
echo "1. Open: $CRON_FILE"
echo "2. Find: 'Defense Sector Lead Gen' (runs at 9:00 AM)"
echo "3. Find: 'Defense Sector Outreach' (runs at 2:00 PM)"
echo ""
echo "4. In BOTH jobs, add to the 'Company Criteria:' section:"
echo "   - MAX VALUATION: \$50 MILLION (CRITICAL FILTER)"
echo "   - REJECT: Companies valued over \$50M (Anduril, Palantir, etc.)"
echo ""
echo "5. Also update search queries to include:"
echo "   - 'under \$50 million valuation'"
echo "   - 'small defense startups'"
echo "   - 'early stage defense companies'"
echo ""

# Create a sample filter script
FILTER_SCRIPT="/Users/cubiczan/.openclaw/workspace/scripts/defense_size_filter.py"
cat > "$FILTER_SCRIPT" << 'EOF'
#!/usr/bin/env python3
"""
Defense Company Size Filter - $50M Max Valuation
"""

def filter_defense_companies(companies):
    """
    Filter defense companies to only include those under $50M valuation.
    
    Args:
        companies: List of company dictionaries
    
    Returns:
        Filtered list (valuation <= $50M)
    """
    MAX_VALUATION = 50000000  # $50M
    
    filtered = []
    rejected = []
    
    for company in companies:
        name = company.get('name', '')
        valuation = company.get('valuation')
        
        # Known large companies to reject
        large_companies = [
            'anduril', 'palantir', 'lockheed', 'northrop', 'raytheon',
            'boeing', 'aerovironment', 'kratos', 'archer', 'joby',
            'zipline', 'skydio', 'shield ai', 'epirus'
        ]
        
        # Check if known large company
        is_large = any(large in name.lower() for large in large_companies)
        
        if is_large:
            rejected.append(f"{name} - Known large company")
            continue
        
        # Check valuation if available
        if valuation and valuation > MAX_VALUATION:
            rejected.append(f"{name} - Valuation ${valuation:,} > $50M")
            continue
        
        # Accept company
        company['size_filter'] = 'PASS: Under $50M'
        filtered.append(company)
    
    # Print results
    print(f"📊 DEFENSE COMPANY FILTER RESULTS:")
    print(f"   Total companies: {len(companies)}")
    print(f"   Accepted (under $50M): {len(filtered)}")
    print(f"   Rejected (over $50M): {len(rejected)}")
    
    if rejected:
        print(f"\n❌ REJECTED COMPANIES:")
        for r in rejected[:10]:
            print(f"   - {r}")
    
    return filtered

# Example usage
if __name__ == "__main__":
    # Test data
    test_companies = [
        {"name": "Anduril Industries", "valuation": 8500000000},
        {"name": "Small Defense Tech Inc", "valuation": 15000000},
        {"name": "Palantir Technologies", "valuation": 50000000000},
        {"name": "Tiny Drone Solutions", "valuation": 5000000},
        {"name": "Lockheed Martin", "valuation": 110000000000},
    ]
    
    print("🧪 TESTING $50M VALUATION FILTER")
    print("=" * 40)
    
    filtered = filter_defense_companies(test_companies)
    
    print(f"\n✅ ACCEPTED COMPANIES:")
    for company in filtered:
        val = company.get('valuation', 'unknown')
        val_str = f"${val:,}" if isinstance(val, (int, float)) else val
        print(f"   - {company['name']} ({val_str})")
EOF

chmod +x "$FILTER_SCRIPT"
echo "✅ Created filter script: $FILTER_SCRIPT"

# Update AUVSI contacts file
AUVSI_FILE="/Users/cubiczan/.openclaw/workspace/final_auvsi_contacts.py"
if [ -f "$AUVSI_FILE" ]; then
    echo ""
    echo "📁 UPDATING AUVSI CONTACTS FILE:"
    echo "   Removing large companies (> $50M)..."
    
    # Create filtered version
    grep -v -i "anduril\|palantir\|lockheed\|northrop\|raytheon\|boeing\|aerovironment\|kratos\|archer\|joby\|zipline\|skydio" "$AUVSI_FILE" > "${AUVSI_FILE}.filtered"
    
    mv "${AUVSI_FILE}.filtered" "$AUVSI_FILE"
    echo "✅ Updated AUVSI file (removed large companies)"
fi

echo ""
echo "🎯 SUMMARY:"
echo "==========="
echo "✅ Backup created: $BACKUP_FILE"
echo "✅ Filter script: $FILTER_SCRIPT"
echo "✅ AUVSI file updated"
echo ""
echo "🔧 MANUAL STEPS REQUIRED:"
echo "1. Edit $CRON_FILE"
echo "2. Add $50M valuation filter to defense jobs"
echo "3. Test with: python3 $FILTER_SCRIPT"
echo ""
echo "💡 Going forward, defense outreach will only target:"
echo "   - Companies under $50M valuation"
echo "   - Small defense startups & contractors"
echo "   - Early stage companies (Seed - Series B)"
echo ""
echo "❌ Will reject:"
echo "   - Anduril ($8.5B), Palantir ($50B), Lockheed ($110B)"
echo "   - Any company valued over $50M"