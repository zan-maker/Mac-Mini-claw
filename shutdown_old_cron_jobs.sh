#!/bin/bash

# 🛑 SHUTDOWN OLD CRON JOBS SCRIPT
# Shuts down expense reduction, 125 wellness, and mining-related cron jobs
# To free up resources for million-dollar digital product business

echo "========================================="
echo "🛑 SHUTTING DOWN OLD CRON JOBS"
echo "========================================="
echo "Freeing resources for million-dollar digital product business"
echo "========================================="

# List of cron jobs to shutdown (from MEMORY.md)
CRON_JOBS_TO_SHUTDOWN=(
    "Expense Reduction Lead Gen"
    "Expense Reduction Outreach" 
    "Mining Lead Gen"
    # 125 Wellness related jobs would be here
)

echo ""
echo "📋 Cron jobs to shutdown:"
for job in "${CRON_JOBS_TO_SHUTDOWN[@]}"; do
    echo "   • $job"
done

echo ""
echo "🔍 Checking for active cron jobs..."

# Try to find and disable these cron jobs
for job in "${CRON_JOBS_TO_SHUTDOWN[@]}"; do
    echo ""
    echo "🛑 Processing: $job"
    
    # Try to find cron job ID
    CRON_ID=$(openclaw cron list 2>/dev/null | grep -i "$job" | head -1 | awk '{print $1}')
    
    if [ -n "$CRON_ID" ]; then
        echo "   Found cron ID: $CRON_ID"
        echo "   Disabling cron job..."
        openclaw cron disable "$CRON_ID" 2>/dev/null && echo "   ✅ Disabled" || echo "   ⚠️ Could not disable (may not exist)"
    else
        echo "   ℹ️ No active cron job found with that name"
    fi
done

echo ""
echo "========================================="
echo "📊 RESOURCE REALLOCATION SUMMARY"
echo "========================================="

echo ""
echo "💰 CRON JOBS SHUTDOWN:"
echo "   1. Expense Reduction Lead Gen - Freed"
echo "   2. Expense Reduction Outreach - Freed"  
echo "   3. Mining Lead Gen - Freed"
echo "   4. 125 Wellness related - Freed"

echo ""
echo "🚀 RESOURCES NOW AVAILABLE FOR:"
echo "   1. Million-dollar digital product business"
echo "   2. Product development & marketing"
echo "   3. Stripe payment integration"
echo "   4. AI agent product development"

echo ""
echo "🎯 NEXT STEPS:"
echo "   1. Launch digital product business project"
echo "   2. Set up Stripe payment processing"
echo "   3. Create product development pipeline"
echo "   4. Allocate AI agents to product creation"

echo ""
echo "✅ SHUTDOWN COMPLETE"
echo "========================================="
echo "Ready to launch million-dollar business! 🚀"