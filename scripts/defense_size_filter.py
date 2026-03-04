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
