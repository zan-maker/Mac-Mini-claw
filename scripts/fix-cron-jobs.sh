#!/bin/bash
# Cron Job Fixes - Run once to apply all approved fixes
# Generated: 2026-02-19

echo "Applying cron job fixes..."

# Note: These updates need to be applied via OpenClaw's cron tool
# This script documents the changes needed

# 1. TIMEOUT FIXES (300s → 600s)
# Jobs affected:
# - 21f22635-5622-41f1-88d4-af1b43965e61 (Expense Reduction Lead Gen)
# - 21cf8088-939d-40cb-9105-248c9361b682 (Miami Hotels Wave 1)
# - e8806fc0-ea33-416b-84f5-9d7bf880bd78 (Miami Hotels Wave 3)

# Fix: Add "timeoutSeconds": 600 to each job's payload

# 2. RATE LIMIT STAGGERING (9 AM batch)
# Jobs currently at 9 AM EST:
# - 81c9f55e-2c86-47ea-81e3-0e4635bc212b (API Balance Dashboard) - 9:00 AM
# - 21f22635-5622-41f1-88d4-af1b43965e61 (Expense Reduction) - 9:00 AM
# - ad9ea923-d3bb-465b-a2eb-233203b7c90e (Deal Origination - Sellers) - 9:00 AM
# - 8bc2acb7-6a30-48d7-911f-8e4a7edd44a0 (Referral Engine - Prospects) - 9:00 AM
# - f546195e-6efd-4622-b131-33e79097252a (Referral Engine - Providers) - 9:00 AM
# - 583a120a-dfb9-4529-b228-67bfa60734bd (Enhanced Lead Gen) - 9:00 AM
# - 9c2fe9b1-12e5-4561-ac8a-4d5a8da1c7dd (Deal Origination - Buyers) - 9:00 AM
# - 5eb89608-b94d-4908-8bef-5f5264cb17ce (Defense Sector) - 9:00 AM

# Staggered schedule (5 min intervals):
# 9:00 AM - API Balance Dashboard, Deal Origination - Buyers
# 9:05 AM - Expense Reduction Lead Gen
# 9:10 AM - Deal Origination - Sellers
# 9:15 AM - Referral Engine - Prospects
# 9:20 AM - Referral Engine - Providers
# 9:25 AM - Enhanced Lead Gen
# 9:30 AM - Defense Sector Lead Gen

# 3. DISCORD DELIVERY FIXES
# Jobs with "cron announce delivery failed":
# - f546195e-6efd-4622-b131-33e79097252a (Referral Engine - Providers)
# - 36ee369b-fbbd-40c9-9d5f-3c9164b32e34 (Dorada Wave 1)
# - 9b2e4bca-e413-4ed8-abf8-dc658a80e06e (Miami Hotels Wave 2)
# - a6c94247-c668-4d17-ba7e-ddbbea2b1b26 (Daily API Usage Check)
# - f7e6d0b8-5b5e-431e-922c-6b08767bbbda (Critical API Alert Check)
# - 93d34680-a42f-475a-9477-eedf1784b4cd (Expense Reduction Outreach)

# Issue: These jobs target different channels:
# - Some target 1473087264568381440 (#cron-output-channel)
# - Some target 1473331628507004939 (another channel)
# - Some target 1471933082297831545 (#mac-mini1)

# Fix: Verify Discord bot has permissions for all target channels
# Test: Send test message to each channel

echo "Fixes documented. Apply manually via cron tool or next session."
echo ""
echo "Summary:"
echo "- 3 jobs need timeout extended to 600s"
echo "- 8 jobs need staggered 9 AM start times"
echo "- 6 jobs need Discord delivery investigation"
