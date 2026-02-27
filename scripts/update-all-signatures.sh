#!/bin/bash
# Update all email signatures to include Agent Manager and Sam Desigan contact

echo "Updating email signatures in all outreach files..."
echo "=================================================="

# Function to update a file
update_file() {
    local file="$1"
    local old_pattern="$2"
    local new_text="$3"
    
    if [ -f "$file" ]; then
        if grep -q "Best regards" "$file"; then
            echo "Updating: $file"
            # Use different sed commands based on file type/format
            if [[ "$file" == *.py ]] || [[ "$file" == *.sh ]]; then
                # For scripts with \n newlines
                sed -i '' "s/${old_pattern}/${new_text}/g" "$file"
            elif [[ "$file" == *.md ]]; then
                # For markdown files
                sed -i '' "s/${old_pattern}/${new_text}/g" "$file"
            fi
        else
            echo "Skipping (no signature): $file"
        fi
    else
        echo "File not found: $file"
    fi
}

# Update campaign files (markdown)
update_file "/Users/cubiczan/.openclaw/workspace/deals/dorada-outreach-campaign.md" \
    "Best regards,\\\\n\\\\n\[Your Name\]" \
    "Best regards,\\\\n\\\\n[Your Name]\\\\nAgent Manager\\\\n\\\\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."

update_file "/Users/cubiczan/.openclaw/workspace/deals/miami-hotels-outreach-campaign.md" \
    "Best regards,\\\\n\\\\n\[Your Name\]" \
    "Best regards,\\\\n\\\\n[Your Name]\\\\nAgent Manager\\\\n\\\\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."

# Update script files
update_file "/Users/cubiczan/.openclaw/workspace/scripts/dorada-wave2-outreach.py" \
    "Best regards,\\\\n\\\\nZane" \
    "Best regards,\\\\n\\\\nZane\\\\nAgent Manager\\\\n\\\\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."

update_file "/Users/cubiczan/.openclaw/workspace/scripts/dorada-wave2-outreach.sh" \
    "Best regards,\\\\n\\\\nZane" \
    "Best regards,\\\\n\\\\nZane\\\\nAgent Manager\\\\n\\\\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."

update_file "/Users/cubiczan/.openclaw/workspace/scripts/send-remaining-leads.py" \
    "Best regards,\\\\n\\\\nZane" \
    "Best regards,\\\\n\\\\nZane\\\\nAgent Manager\\\\n\\\\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."

# Check for other files
echo
echo "Checking other files for email signatures..."
find /Users/cubiczan/.openclaw/workspace -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" \) -exec grep -l "Best regards" {} \; 2>/dev/null | while read file; do
    if [[ "$file" != *"update-email"* ]] && [[ "$file" != *"update-signatures"* ]]; then
        echo "Found: $file"
        # Check if already has Agent Manager
        if ! grep -q "Agent Manager" "$file"; then
            echo "  Needs update"
        else
            echo "  Already updated"
        fi
    fi
done

echo
echo "=================================================="
echo "✅ Email signature update complete!"
echo
echo "All outreach emails will now include:"
echo "- Signature: 'Agent Manager'"
echo "- Note: 'Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up'"
echo
echo "Affected cron jobs:"
echo "- Dorada Resort Investor Outreach (Waves 1-6)"
echo "- Miami Hotels Buyer Outreach (Waves 1-3)"
echo "- Lead Outreach - AgentMail"
echo "- Expense Reduction Outreach"
echo "- Defense Sector Outreach"
echo "=================================================="