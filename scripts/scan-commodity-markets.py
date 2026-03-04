#!/usr/bin/env python3
"""
Scan Kalshi data for commodity trades
"""

import re

def find_commodity_markets(file_path):
    """Find all commodity-related markets in Kalshi data"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Split by market sections (lines with $ and vol)
    lines = content.split('\n')
    
    commodity_markets = []
    current_market = None
    in_commodity_section = False
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Look for commodity keywords
        commodity_keywords = [
            'gas', 'oil', 'gold', 'silver', 'copper', 'aluminum', 
            'wheat', 'corn', 'soy', 'agriculture', 'commodity',
            'crude', 'energy', 'metal', 'natural gas', 'petroleum',
            'gasoline', 'diesel', 'heating oil', 'ethanol',
            'rice', 'cotton', 'sugar', 'coffee', 'cocoa',
            'livestock', 'cattle', 'hog', 'pork', 'poultry'
        ]
        
        # Check if line contains commodity keyword (case insensitive)
        if any(keyword in line.lower() for keyword in commodity_keywords):
            # This might be a commodity market
            # Look backward for question
            question = ""
            for j in range(i-1, max(i-5, -1), -1):
                if lines[j].strip() and '?' in lines[j]:
                    question = lines[j].strip()
                    break
            
            # Look forward for volume
            volume = 0
            for j in range(i, min(i+5, len(lines))):
                if '$' in lines[j] and 'vol' in lines[j]:
                    # Extract volume
                    vol_match = re.search(r'\$([\d,]+)', lines[j])
                    if vol_match:
                        volume = int(vol_match.group(1).replace(',', ''))
                    break
            
            if question and volume > 0:
                # Look for options (next few lines)
                options = []
                for j in range(i, min(i+10, len(lines))):
                    option_line = lines[j].strip()
                    if 'x' in option_line and ('%' in option_line or any(c.isdigit() for c in option_line)):
                        # This looks like an option
                        options.append(option_line)
                
                commodity_markets.append({
                    'question': question,
                    'volume': volume,
                    'options': options[:2] if options else [],
                    'line_number': i
                })
    
    return commodity_markets

def main():
    file_path = '/Users/cubiczan/.openclaw/media/inbound/21cb8e01-a5c3-417d-a27c-144a726518a7.txt'
    
    print("🔍 Scanning Kalshi data for commodity trades...")
    print("=" * 80)
    
    markets = find_commodity_markets(file_path)
    
    if not markets:
        print("No commodity markets found.")
        return
    
    print(f"Found {len(markets)} commodity-related markets:")
    print()
    
    # Group by commodity type
    commodity_groups = {}
    for market in markets:
        question_lower = market['question'].lower()
        
        # Categorize
        category = "Other"
        if 'gas' in question_lower:
            category = "Gasoline"
        elif 'oil' in question_lower:
            category = "Oil"
        elif 'gold' in question_lower:
            category = "Gold"
        elif 'silver' in question_lower:
            category = "Silver"
        elif 'copper' in question_lower:
            category = "Copper"
        elif any(ag in question_lower for ag in ['wheat', 'corn', 'soy', 'agriculture']):
            category = "Agriculture"
        elif 'energy' in question_lower:
            category = "Energy"
        elif 'metal' in question_lower:
            category = "Metals"
        
        if category not in commodity_groups:
            commodity_groups[category] = []
        commodity_groups[category].append(market)
    
    # Print by category
    for category, cat_markets in commodity_groups.items():
        print(f"📊 {category.upper()} MARKETS:")
        print("-" * 80)
        
        for market in cat_markets:
            print(f"❓ {market['question']}")
            print(f"   💰 Volume: ${market['volume']:,}")
            
            if market['options']:
                print(f"   📈 Options:")
                for option in market['options'][:2]:  # Show first 2 options
                    print(f"      • {option}")
            
            # Check if this is the gas trade you already placed
            if 'gas' in market['question'].lower() and '3.50' in market['question']:
                print(f"   ✅ YOUR TRADE: $25 YES on this market")
            
            print()
        
        print()

if __name__ == "__main__":
    main()
