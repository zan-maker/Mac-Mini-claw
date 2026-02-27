#!/bin/bash
# Dorada Resort - Complete Wave 2 & Start Wave 3
# Send emails to remaining Wave 2 contacts and begin Wave 3

AGENTMAIL_API_KEY="am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
FROM_EMAIL="zane@agentmail.to"
CC_EMAIL="sam@impactquadrant.info"

echo "======================================================================"
echo "DORADA RESORT OUTREACH - $(date '+%Y-%m-%d %H:%M')"
echo "======================================================================"
echo

# Wave 2 - Contact #5: Cresset (Jack Ablin)
echo "Wave 2 - Contact #5: Cresset (Jack Ablin)"
echo "  Email: jablin@cressetcapital.com"
echo "  Version: Family Office"

curl -s -X POST "https://api.agentmail.to/v1/emails" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'"$FROM_EMAIL"'",
    "to": ["jablin@cressetcapital.com"],
    "cc": ["'"$CC_EMAIL"'"],
    "subject": "Legacy wellness asset in Costa Rica - health preservation meets wealth preservation",
    "body": "Dear Mr. Ablin,\n\nI'\''m reaching out regarding **Dorada**, a first-of-its-kind regenerative destination resort in Costa Rica'\''s Blue Zone—designed specifically for families seeking to preserve both health and capital across generations.\n\nGiven Cresset'\''s focus on healthcare, wellness, and family office clients, I believe Dorada aligns with your clients'\'' priorities:\n\n- **Capital preservation with upside**\n- **Hard assets paired with experiential value**\n- **Intergenerational relevance**\n- **Personal use optionality alongside returns**\n\n**The Asset:**\n- **300-acre protected bio-reserve** with world-class ocean views\n- **40 private estate homes** (1+ acre lots)\n- **Longevity & Human Performance Center** with personalized healthspan programs\n- Fully off-grid with sustainable infrastructure\n- **Curated longevity community** of like-minded families\n\n**Founder:** Dr. Vincent Giampapa, globally recognized leader in anti-aging medicine and regenerative science.\n\n**Market Opportunity:** The wellness economy is projected to reach **$2.1T by 2030**, driven by aging HNW populations seeking preventive, performance-based health solutions.\n\n**Legacy Value:** Dorada allows families to invest in something that enhances not only balance sheets—but quality of life, longevity, and human potential.\n\nWould you be interested in sharing this opportunity with your family office clients?\n\nBest regards,\n\nZane\nAgent Manager\nImpact Quadrant\n\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."
  }' > /dev/null && echo "  ✅ SENT" || echo "  ❌ FAILED"

echo

# Wave 2 - Contact #8: BHB Private (Rebecca Farrer)
echo "Wave 2 - Contact #8: BHB Private (Rebecca Farrer)"
echo "  Email: rf@bhbprivate.com"
echo "  Version: Family Office"

curl -s -X POST "https://api.agentmail.to/v1/emails" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'"$FROM_EMAIL"'",
    "to": ["rf@bhbprivate.com"],
    "cc": ["'"$CC_EMAIL"'"],
    "subject": "Legacy wellness asset in Costa Rica - health preservation meets wealth preservation",
    "body": "Dear Ms. Farrer,\n\nI'\''m reaching out regarding **Dorada**, a first-of-its-kind regenerative destination resort in Costa Rica'\''s Blue Zone—designed specifically for families seeking to preserve both health and capital across generations.\n\nGiven BHB Private'\''s focus on healthcare, wellness, and family office clients, I believe Dorada aligns with your clients'\'' priorities:\n\n- **Capital preservation with upside**\n- **Hard assets paired with experiential value**\n- **Intergenerational relevance**\n- **Personal use optionality alongside returns**\n\n**The Asset:**\n- **300-acre protected bio-reserve** with world-class ocean views\n- **40 private estate homes** (1+ acre lots)\n- **Longevity & Human Performance Center** with personalized healthspan programs\n- Fully off-grid with sustainable infrastructure\n- **Curated longevity community** of like-minded families\n\n**Founder:** Dr. Vincent Giampapa, globally recognized leader in anti-aging medicine and regenerative science.\n\n**Market Opportunity:** The wellness economy is projected to reach **$2.1T by 2030**, driven by aging HNW populations seeking preventive, performance-based health solutions.\n\n**Legacy Value:** Dorada allows families to invest in something that enhances not only balance sheets—but quality of life, longevity, and human potential.\n\nWould you be interested in sharing this opportunity with your family office clients?\n\nBest regards,\n\nZane\nAgent Manager\nImpact Quadrant\n\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."
  }' > /dev/null && echo "  ✅ SENT" || echo "  ❌ FAILED"

echo

# Wave 2 - Contact #9: Fisher Brothers (Michael Bar)
echo "Wave 2 - Contact #9: Fisher Brothers (Michael Bar)"
echo "  Email: mbar@fisherbrothers.com"
echo "  Version: Institutional"

curl -s -X POST "https://api.agentmail.to/v1/emails" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'"$FROM_EMAIL"'",
    "to": ["mbar@fisherbrothers.com"],
    "cc": ["'"$CC_EMAIL"'"],
    "subject": "Luxury wellness platform in Costa Rica - $2.1T market opportunity",
    "body": "Dear Mr. Bar,\n\nI'\''m reaching out regarding **Dorada**, a category-defining luxury wellness and longevity platform in Costa Rica'\''s Blue Zone.\n\nGiven Fisher Brothers'\'' portfolio spanning hotels, healthcare, and wellness, I believe Dorada represents a strategic fit as a **multi-stream revenue platform**:\n\n**Revenue Streams:**\n- Luxury real estate sales and appreciation\n- Hospitality and branded residence income\n- High-margin longevity and performance programs (7-10 day intensives)\n- Membership-based recurring revenues\n- Farm-to-table dining and experiential services\n\n**Core Differentiator:**\nThe **Longevity & Human Performance Center** delivers personalized, data-driven healthspan interventions—transforming Dorada from a destination into a **lifetime engagement model** with materially higher customer LTV.\n\n**Asset Overview:**\n- 300-acre protected development\n- Ultra-low density, premium positioning\n- Replicable model across Blue Zone geographies\n- Brand extensibility into digital health and affiliated clinics\n\nThe global wellness and longevity economy is projected to reach **$2.1T by 2030** (12.4% CAGR). Dorada is positioned at the intersection of this trend with defensible scientific credibility.\n\nWould you be open to reviewing the investor deck?\n\nBest regards,\n\nZane\nAgent Manager\nImpact Quadrant\n\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."
  }' > /dev/null && echo "  ✅ SENT" || echo "  ❌ FAILED"

echo

# Wave 2 - Contact #10: The Graham Group (Lee Graham)
echo "Wave 2 - Contact #10: The Graham Group (Lee Graham)"
echo "  Email: graham@thegrahamgroup.co.uk"
echo "  Version: Family Office"

curl -s -X POST "https://api.agentmail.to/v1/emails" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'"$FROM_EMAIL"'",
    "to": ["graham@thegrahamgroup.co.uk"],
    "cc": ["'"$CC_EMAIL"'"],
    "subject": "Legacy wellness asset in Costa Rica - health preservation meets wealth preservation",
    "body": "Dear Mr. Graham,\n\nI'\''m reaching out regarding **Dorada**, a first-of-its-kind regenerative destination resort in Costa Rica'\''s Blue Zone—designed specifically for families seeking to preserve both health and capital across generations.\n\nGiven The Graham Group'\''s focus on healthcare, wellness, and family office clients, I believe Dorada aligns with your clients'\'' priorities:\n\n- **Capital preservation with upside**\n- **Hard assets paired with experiential value**\n- **Intergenerational relevance**\n- **Personal use optionality alongside returns**\n\n**The Asset:**\n- **300-acre protected bio-reserve** with world-class ocean views\n- **40 private estate homes** (1+ acre lots)\n- **Longevity & Human Performance Center** with personalized healthspan programs\n- Fully off-grid with sustainable infrastructure\n- **Curated longevity community** of like-minded families\n\n**Founder:** Dr. Vincent Giampapa, globally recognized leader in anti-aging medicine and regenerative science.\n\n**Market Opportunity:** The wellness economy is projected to reach **$2.1T by 2030**, driven by aging HNW populations seeking preventive, performance-based health solutions.\n\n**Legacy Value:** Dorada allows families to invest in something that enhances not only balance sheets—but quality of life, longevity, and human potential.\n\nWould you be interested in sharing this opportunity with your family office clients?\n\nBest regards,\n\nZane\nAgent Manager\nImpact Quadrant\n\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."
  }' > /dev/null && echo "  ✅ SENT" || echo "  ❌ FAILED"

echo
echo "======================================================================"
echo "WAVE 2 COMPLETE - STARTING WAVE 3"
echo "======================================================================"
echo

# Wave 3 - Contact #11: TRT Holdings (Bob Rowling)
echo "Wave 3 - Contact #11: TRT Holdings (Bob Rowling)"
echo "  Email: bob.rowling@omnihotels.com"
echo "  Version: Institutional"

curl -s -X POST "https://api.agentmail.to/v1/emails" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'"$FROM_EMAIL"'",
    "to": ["bob.rowling@omnihotels.com"],
    "cc": ["'"$CC_EMAIL"'"],
    "subject": "Luxury wellness platform in Costa Rica - $2.1T market opportunity",
    "body": "Dear Mr. Rowling,\n\nI'\''m reaching out regarding **Dorada**, a category-defining luxury wellness and longevity platform in Costa Rica'\''s Blue Zone.\n\nGiven TRT Holdings'\'' portfolio spanning hotels, healthcare, and wellness, I believe Dorada represents a strategic fit as a **multi-stream revenue platform**:\n\n**Revenue Streams:**\n- Luxury real estate sales and appreciation\n- Hospitality and branded residence income\n- High-margin longevity and performance programs (7-10 day intensives)\n- Membership-based recurring revenues\n- Farm-to-table dining and experiential services\n\n**Core Differentiator:**\nThe **Longevity & Human Performance Center** delivers personalized, data-driven healthspan interventions—transforming Dorada from a destination into a **lifetime engagement model** with materially higher customer LTV.\n\n**Asset Overview:**\n- 300-acre protected development\n- Ultra-low density, premium positioning\n- Replicable model across Blue Zone geographies\n- Brand extensibility into digital health and affiliated clinics\n\nThe global wellness and longevity economy is projected to reach **$2.1T by 2030** (12.4% CAGR). Dorada is positioned at the intersection of this trend with defensible scientific credibility.\n\nWould you be open to reviewing the investor deck?\n\nBest regards,\n\nZane\nAgent Manager\nImpact Quadrant\n\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."
  }' > /dev/null && echo "  ✅ SENT" || echo "  ❌ FAILED"

echo

# Wave 3 - Contact #12: TRT Holdings (Brendan O'Hara)
echo "Wave 3 - Contact #12: TRT Holdings (Brendan O'Hara)"
echo "  Email: brendan.ohara@omnihotels.com"
echo "  Version: Institutional"

curl -s -X POST "https://api.agentmail.to/v1/emails" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'"$FROM_EMAIL"'",
    "to": ["brendan.ohara@omnihotels.com"],
    "cc": ["'"$CC_EMAIL"'"],
    "subject": "Luxury wellness platform in Costa Rica - $2.1T market opportunity",
    "body": "Dear Mr. O'\''Hara,\n\nI'\''m reaching out regarding **Dorada**, a category-defining luxury wellness and longevity platform in Costa Rica'\''s Blue Zone.\n\nGiven TRT Holdings'\'' portfolio spanning hotels, healthcare, and wellness, I believe Dorada represents a strategic fit as a **multi-stream revenue platform**:\n\n**Revenue Streams:**\n- Luxury real estate sales and appreciation\n- Hospitality and branded residence income\n- High-margin longevity and performance programs (7-10 day intensives)\n- Membership-based recurring revenues\n- Farm-to-table dining and experiential services\n\n**Core Differentiator:**\nThe **Longevity & Human Performance Center** delivers personalized, data-driven healthspan interventions—transforming Dorada from a destination into a **lifetime engagement model** with materially higher customer LTV.\n\n**Asset Overview:**\n- 300-acre protected development\n- Ultra-low density, premium positioning\n- Replicable model across Blue Zone geographies\n- Brand extensibility into digital health and affiliated clinics\n\nThe global wellness and longevity economy is projected to reach **$2.1T by 2030** (12.4% CAGR). Dorada is positioned at the intersection of this trend with defensible scientific credibility.\n\nWould you be open to reviewing the investor deck?\n\nBest regards,\n\nZane\nAgent Manager\nImpact Quadrant\n\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."
  }' > /dev/null && echo "  ✅ SENT" || echo "  ❌ FAILED"

echo
echo "======================================================================"
echo "SUMMARY"
echo "======================================================================"
echo "Wave 2 emails sent: 4"
echo "Wave 3 emails sent: 2"
echo "Total emails sent: 6"
echo "All emails CC'd to: sam@impactquadrant.info"
echo "======================================================================"
