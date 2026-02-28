#!/bin/bash
# Send mining investor outreach using Gmail SMTP
# To all 114 investors in CSV file

GMAIL_EMAIL="sam@cubiczan.com"
GMAIL_PASSWORD="mwzh abbf ssih mjsf"
CSV_FILE="/Users/cubiczan/.openclaw/media/inbound/d5fc3aca-3c73-46b3-a9e4-aa86ffd8c49b.csv"
LOG_FILE="/Users/cubiczan/.openclaw/workspace/mining-investor-outreach-gmail-$(date +%Y%m%d-%H%M%S).log"
SUMMARY_FILE="/Users/cubiczan/.openclaw/workspace/mining-investor-outreach-summary-$(date +%Y%m%d).md"

echo "============================================================"
echo "MINING INVESTOR OUTREACH - GMAIL SMTP"
echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
echo "Sender: $GMAIL_EMAIL"
echo "CSV File: $CSV_FILE"
echo "Total contacts: $(wc -l < "$CSV_FILE")"
echo "============================================================"
echo

total_contacts=$(wc -l < "$CSV_FILE")
sent_count=0
failed_count=0

# Create summary file
cat > "$SUMMARY_FILE" << EOF
# Mining Investor Outreach - $(date '+%Y-%m-%d')

## Campaign Details
- **Date:** $(date '+%Y-%m-%d %H:%M:%S')
- **Sender:** $GMAIL_EMAIL
- **Total Contacts:** $total_contacts
- **Method:** Gmail SMTP

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

## Contacts Processed
EOF

# Process CSV file
line_num=0
while IFS=, read -r id name email; do
    line_num=$((line_num + 1))
    
    # Clean up fields
    name=$(echo "$name" | sed 's/^"//;s/"$//;s/^ *//;s/ *$//' | tr -d '\r')
    email=$(echo "$email" | sed 's/^"//;s/"$//;s/^ *//;s/ *$//' | tr -d '\r')
    
    # Skip empty lines or invalid emails
    if [[ -z "$email" ]] || [[ ! "$email" =~ @ ]]; then
        echo "[$line_num/$total_contacts] ⚠️ Skipping invalid: $name ($email)"
        echo "$(date '+%H:%M:%S'),SKIP,$name,$email,Invalid email" >> "$LOG_FILE"
        continue
    fi
    
    # Extract first name
    first_name=$(echo "$name" | awk '{print $1}')
    
    echo "[$line_num/$total_contacts] 📧 Sending to: $name ($email)"
    
    # Create email body
    cat > /tmp/mining_email.txt << EOF
From: Sam Desigan <$GMAIL_EMAIL>
To: $email
Subject: Mining deal flow partnership – What are you looking for?
Content-Type: text/plain; charset=utf-8

Hi $first_name,

I hope this message finds you well.

We are partnered with a leading mining deal-flow and asset intelligence platform that gives us structured access to a curated pipeline of pre-vetted junior exploration and development-stage opportunities globally.

The platform aggregates live listings, operator-submitted project data, and independently verified resource disclosures — giving us early visibility on assets before they reach mainstream investor attention.

**To better align our sourcing with your investment mandate, could you please let us know:**

1. **Primary metals/commodities** you are focused on (e.g., copper, gold, lithium, nickel, etc.)
2. **Preferred jurisdictions** (e.g., Tier 1 like Canada/US/Australia, or emerging markets like Latin America/West Africa)
3. **Project stage** preference (exploration, development, production)
4. **Deal size range** you typically participate in
5. Any specific **geological models or deposit types** of interest

**Sample of recent opportunities we have sourced (2025):**
- Large-scale copper development in Chile (Tier 1 jurisdiction)
- High-grade gold exploration in Peru
- Copper-gold porphyry system in Colombia
- Gold heap-leach production asset in Mexico
- Nevada gold portfolio (USA)
- Lithium brine exploration in Argentina
- Copper-molybdenum porphyry in Ecuador
- Near-surface placer coltan in West Africa

Once we understand your specific criteria, we can immediately start filtering the live pipeline and sending you anonymised project summaries that match your mandate.

Please reply directly to this email with your investment criteria, or feel free to schedule a brief call if you prefer to discuss.

Best regards,

Sam Desigan
Sam@cubiczan.com
EOF
    
    # Send email via Gmail SMTP
    send_result=$(curl -s --url 'smtp://smtp.gmail.com:587' \
      --ssl-reqd \
      --mail-from "$GMAIL_EMAIL" \
      --mail-rcpt "$email" \
      --user "$GMAIL_EMAIL:$GMAIL_PASSWORD" \
      --upload-file /tmp/mining_email.txt 2>&1)
    
    if [ $? -eq 0 ]; then
        echo "   ✅ SENT"
        echo "$(date '+%H:%M:%S'),SENT,$name,$email" >> "$LOG_FILE"
        echo "- $name ($email) - ✅ SENT" >> "$SUMMARY_FILE"
        ((sent_count++))
    else
        echo "   ❌ FAILED: $send_result"
        echo "$(date '+%H:%M:%S'),FAILED,$name,$email,$send_result" >> "$LOG_FILE"
        echo "- $name ($email) - ❌ FAILED" >> "$SUMMARY_FILE"
        ((failed_count++))
    fi
    
    # Add to summary
    if [ $((line_num % 10)) -eq 0 ]; then
        echo "   [Progress: $line_num/$total_contacts, Sent: $sent_count, Failed: $failed_count]"
    fi
    
    # Delay to avoid rate limiting (2 seconds between emails)
    sleep 2
    
done < "$CSV_FILE"

# Complete summary
echo "============================================================"
echo "SUMMARY"
echo "============================================================"
echo "Total contacts: $total_contacts"
echo "Emails sent: $sent_count"
echo "Emails failed: $failed_count"
echo "Log file: $LOG_FILE"
echo "Summary: $SUMMARY_FILE"
echo "============================================================"

# Update summary file
cat >> "$SUMMARY_FILE" << EOF

## Results Summary
- **Total Contacts:** $total_contacts
- **Emails Sent:** $sent_count
- **Failed:** $failed_count
- **Success Rate:** $((sent_count * 100 / total_contacts))%

## Next Steps
1. Monitor reply rate (target: 15-20%)
2. Follow up in 3-5 days if no response
3. Segment responses by commodity/jurisdiction preference
4. Begin sending matched deal flow to interested investors

## Files
- **Log:** $LOG_FILE
- **CSV Source:** $CSV_FILE
- **Sample Projects:** 67ad652e-b1ae-42a8-9143-56801695f8b7.md

---
*Campaign completed: $(date '+%Y-%m-%d %H:%M:%S')*
EOF

echo
echo "✅ Campaign completed! Check $SUMMARY_FILE for details."
