#!/bin/bash
# Send mining investor outreach email to all investors in CSV
# Using sam@cubiczan.com as sender

AGENTMAIL_API_KEY="am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f"
FROM_EMAIL="sam@cubiczan.com"
CSV_FILE="/Users/cubiczan/.openclaw/media/inbound/d5fc3aca-3c73-46b3-a9e4-aa86ffd8c49b.csv"
LOG_FILE="/Users/cubiczan/.openclaw/workspace/mining-investor-outreach-$(date +%Y%m%d-%H%M%S).log"

echo "============================================================"
echo "MINING INVESTOR OUTREACH - $(date '+%Y-%m-%d %H:%M')"
echo "============================================================"
echo "CSV File: $CSV_FILE"
echo "Sender: $FROM_EMAIL"
echo "Total contacts: $(wc -l < "$CSV_FILE")"
echo "============================================================"
echo

# Count total contacts
total_contacts=$(wc -l < "$CSV_FILE")
sent_count=0
failed_count=0

# Read CSV and send emails
while IFS=, read -r id name email; do
    # Clean up fields (remove quotes, extra spaces)
    name=$(echo "$name" | sed 's/^"//;s/"$//;s/^ *//;s/ *$//')
    email=$(echo "$email" | sed 's/^"//;s/"$//;s/^ *//;s/ *$//')
    
    # Skip empty lines or invalid emails
    if [[ -z "$email" ]] || [[ ! "$email" =~ @ ]]; then
        echo "⚠️ Skipping invalid email: $name ($email)"
        continue
    fi
    
    # Extract first name for personalization
    first_name=$(echo "$name" | awk '{print $1}')
    
    echo "Sending to: $name ($email)"
    
    # Send email via AgentMail API
    response=$(curl -s -w "%{http_code}" -X POST "https://api.agentmail.to/v1/emails" \
      -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "from": "'"$FROM_EMAIL"'",
        "to": ["'"$email"'"],
        "subject": "Mining deal flow partnership – What are you looking for?",
        "body": "Hi '"$first_name"',\n\nI hope this message finds you well.\n\nWe are partnered with a leading mining deal-flow and asset intelligence platform that gives us structured access to a curated pipeline of pre-vetted junior exploration and development-stage opportunities globally.\n\nThe platform aggregates live listings, operator-submitted project data, and independently verified resource disclosures — giving us early visibility on assets before they reach mainstream investor attention.\n\n**To better align our sourcing with your investment mandate, could you please let us know:**\n\n1. **Primary metals/commodities** you are focused on (e.g., copper, gold, lithium, nickel, etc.)\n2. **Preferred jurisdictions** (e.g., Tier 1 like Canada/US/Australia, or emerging markets like Latin America/West Africa)\n3. **Project stage** preference (exploration, development, production)\n4. **Deal size range** you typically participate in\n5. Any specific **geological models or deposit types** of interest\n\n**Sample of recent opportunities we have sourced (2025):**\n- Large-scale copper development in Chile (Tier 1 jurisdiction)\n- High-grade gold exploration in Peru\n- Copper-gold porphyry system in Colombia\n- Gold heap-leach production asset in Mexico\n- Nevada gold portfolio (USA)\n- Lithium brine exploration in Argentina\n- Copper-molybdenum porphyry in Ecuador\n- Near-surface placer coltan in West Africa\n\nOnce we understand your specific criteria, we can immediately start filtering the live pipeline and sending you anonymised project summaries that match your mandate.\n\nPlease reply directly to this email with your investment criteria, or feel free to schedule a brief call if you prefer to discuss.\n\nBest regards,\n\nSam Desigan\nSam@cubiczan.com"
      }' 2>/dev/null)
    
    http_code=${response: -3}
    response_body=${response:0:${#response}-3}
    
    if [[ "$http_code" == "200" ]] || [[ "$http_code" == "201" ]]; then
        echo "  ✅ SENT"
        echo "$(date '+%Y-%m-%d %H:%M:%S'),SENT,$name,$email" >> "$LOG_FILE"
        ((sent_count++))
    else
        echo "  ❌ FAILED (HTTP $http_code)"
        echo "$(date '+%Y-%m-%d %H:%M:%S'),FAILED,$name,$email,$http_code" >> "$LOG_FILE"
        ((failed_count++))
    fi
    
    # Small delay to avoid rate limiting
    sleep 1
    
done < <(tail -n +1 "$CSV_FILE")  # Skip header if exists

echo
echo "============================================================"
echo "SUMMARY"
echo "============================================================"
echo "Total contacts processed: $total_contacts"
echo "Emails sent successfully: $sent_count"
echo "Emails failed: $failed_count"
echo "Log file: $LOG_FILE"
echo "============================================================"

# Also create a summary report
SUMMARY_FILE="/Users/cubiczan/.openclaw/workspace/mining-investor-outreach-summary-$(date +%Y%m%d).md"
cat > "$SUMMARY_FILE" << EOF
# Mining Investor Outreach - $(date '+%Y-%m-%d')

## Campaign Details
- **Date:** $(date '+%Y-%m-%d %H:%M')
- **Sender:** $FROM_EMAIL
- **Total Contacts:** $total_contacts
- **Emails Sent:** $sent_count
- **Failed:** $failed_count

## Email Template
**Subject:** Mining deal flow partnership – What are you looking for?

**Body:**
> Hi [First Name],
> 
> I hope this message finds you well.
> 
> We are partnered with a leading mining deal-flow and asset intelligence platform that gives us structured access to a curated pipeline of pre-vetted junior exploration and development-stage opportunities globally.
> 
> The platform aggregates live listings, operator-submitted project data, and independently verified resource disclosures — giving us early visibility on assets before they reach mainstream investor attention.
> 
> **To better align our sourcing with your investment mandate, could you please let us know:**
> 
> 1. **Primary metals/commodities** you are focused on (e.g., copper, gold, lithium, nickel, etc.)
> 2. **Preferred jurisdictions** (e.g., Tier 1 like Canada/US/Australia, or emerging markets like Latin America/West Africa)
> 3. **Project stage** preference (exploration, development, production)
> 4. **Deal size range** you typically participate in
> 5. Any specific **geological models or deposit types** of interest
> 
> **Sample of recent opportunities we have sourced (2025):**
> - Large-scale copper development in Chile (Tier 1 jurisdiction)
> - High-grade gold exploration in Peru
> - Copper-gold porphyry system in Colombia
> - Gold heap-leach production asset in Mexico
> - Nevada gold portfolio (USA)
> - Lithium brine exploration in Argentina
> - Copper-molybdenum porphyry in Ecuador
> - Near-surface placer coltan in West Africa
> 
> Once we understand your specific criteria, we can immediately start filtering the live pipeline and sending you anonymised project summaries that match your mandate.
> 
> Please reply directly to this email with your investment criteria, or feel free to schedule a brief call if you prefer to discuss.
> 
> Best regards,
> 
> Sam Desigan
> Sam@cubiczan.com

## Contacts List
Total: $total_contacts investors

## Next Steps
- Monitor reply rate (target: 15-20%)
- Follow up in 3-5 days if no response
- Segment responses by commodity/jurisdiction preference
- Begin sending matched deal flow to interested investors

## Files
- **Log:** $LOG_FILE
- **CSV Source:** $CSV_FILE
- **Sample Projects:** 67ad652e-b1ae-42a8-9143-56801695f8b7.md

EOF

echo "Summary report: $SUMMARY_FILE"
