#!/bin/bash
# Position Monitor - Automated tracking for Kalshi positions
# Created: 2026-03-09 (Autonomous Session)
# Purpose: Monitor trading positions, alert on price movements

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================="
echo "📊 POSITION MONITOR - $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================="
echo ""

# Position Data (from morning-brief.md as of 2026-03-09)
# Settlement: March 13 (4 days)

echo "🎯 SETTLEMENT COUNTDOWN: 4 DAYS (March 13)"
echo ""

# Copper Position 1
echo "1️⃣  COPPER POSITION 1: \$25 YES on \$5.69-5.74"
echo "   Target: \$5.69-5.74/lb"
echo "   Current: \$5.84/lb"
echo "   Status: ${GREEN}✅ PROFITABLE (+2.72%)${NC}"
echo "   Max Return: \$335 (13.4x)"
echo "   Action: ${GREEN}HOLD${NC}"
echo ""

# Copper Position 2
echo "2️⃣  COPPER POSITION 2: \$25 YES on \$5.63-5.68"
echo "   Target: \$5.63-5.68/lb"
echo "   Current: \$5.84/lb"
echo "   Status: ${GREEN}✅ PROFITABLE (+3.81%)${NC}"
echo "   Max Return: \$213.75 (8.55x)"
echo "   Action: ${GREEN}HOLD${NC}"
echo ""

# Silver Position 1
echo "3️⃣  SILVER POSITION 1: \$25 YES on >\$84.49"
echo "   Target: >\$84.49"
echo "   Current: \$84.46"
echo "   Status: ${YELLOW}⚠️  AT RISK (-\$0.03, -0.04%)${NC}"
echo "   Gap: \$0.03 (0.04%)"
echo "   Max Return: \$44 (1.76x)"
echo "   Action: ${YELLOW}MONITOR CLOSELY${NC}"
echo ""

# Silver Position 2
echo "4️⃣  SILVER POSITION 2: \$25 YES on >\$85.49"
echo "   Target: >\$85.49"
echo "   Current: \$84.46"
echo "   Status: ${RED}⚠️  AT RISK (-\$1.03, -1.22%)${NC}"
echo "   Gap: \$1.03 (1.22%)"
echo "   Max Return: \$47.50 (1.9x)"
echo "   Action: ${RED}MONITOR CLOSELY${NC}"
echo ""

# Gold Position
echo "5️⃣  GOLD POSITION: \$50 YES on >\$5,159"
echo "   Target: >\$5,159"
echo "   Current: \$5,172"
echo "   Status: ${GREEN}✅ PROFITABLE (+\$13, +0.25%)${NC}"
echo "   Max Return: TBD"
echo "   Action: ${GREEN}HOLD${NC}"
echo ""

# Portfolio Summary
echo "========================================="
echo "📈 PORTFOLIO SUMMARY"
echo "========================================="
echo "Total Invested: \$150"
echo "Profitable: \$100 (3 positions)"
echo "At Risk: \$50 (2 positions)"
echo "Max Potential Return: \$640.25+"
echo ""

# Risk Assessment
echo "========================================="
echo "⚠️  RISK ASSESSMENT"
echo "========================================="
echo "Copper: ${GREEN}LOW RISK${NC} - Already above targets"
echo "Gold: ${GREEN}LOW RISK${NC} - Already above target"
echo "Silver #1: ${YELLOW}MEDIUM RISK${NC} - \$0.03 gap (0.04%)"
echo "Silver #2: ${RED}HIGH RISK${NC} - \$1.03 gap (1.22%)"
echo ""

# Action Items
echo "========================================="
echo "🎯 ACTION ITEMS"
echo "========================================="
echo "1. Monitor silver prices daily (volatile)"
echo "2. Check Kalshi platform for live prices"
echo "3. Consider exit strategy if silver drops further"
echo "4. Settlement date: March 13 (4 days)"
echo ""

# API Integration Note
echo "========================================="
echo "📡 DATA SOURCE"
echo "========================================="
echo "Primary: metals.dev API"
echo "Copper: \$12,885.46/MT = \$5.84/lb"
echo "Silver: \$84.46 (current)"
echo "Gold: \$5,172 (current)"
echo ""
echo "Update: Run 'python3 scripts/check_metals_prices.py' for live data"
echo ""

echo "========================================="
echo "✅ Monitor complete at $(date '+%H:%M:%S')"
echo "========================================="
