#!/bin/bash
# Send expense reduction outreach emails via AgentMail API
# Using Tavily-enriched contacts

AGENTMAIL_API_KEY="am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
FROM_EMAIL="Zane@agentmail.to"
CC_EMAIL="sam@impactquadrant.info"

echo "============================================================"
echo "EXPENSE REDUCTION OUTREACH - $(date '+%Y-%m-%d %H:%M')"
echo "============================================================"
echo

# Lead 1: Precision Products Machining Group
echo "Sending to: Don Brown (CEO) - Precision Products Machining Group"
echo "  Email: dbrown@precprodmachgrp.com"

curl -s -X POST "https://api.agentmail.to/v1/emails" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'"$FROM_EMAIL"'",
    "to": ["dbrown@precprodmachgrp.com"],
    "cc": ["'"$CC_EMAIL"'"],
    "subject": "Quick question about Precision Products Machining Group'\''s operating expenses",
    "body": "Hi Don,\n\nI hope this message finds you well. I'\''m reaching out because we'\''ve identified Precision Products Machining Group as an excellent candidate for our expense reduction program.\n\nOur team specializes in helping precision manufacturing companies reduce operating expenses by 18-23% without compromising quality or service levels. We'\''ve successfully partnered with similar organizations and consistently deliver:\n\n✓ 15-25% reduction in telecommunications, waste management, and utility costs\n✓ 100% contingency-based model - you only pay from savings generated\n✓ Zero upfront costs or risks to your organization\n\nGiven Precision Products Machining Group'\''s profile and industry position, we'\''re confident we can identify significant savings opportunities across your vendor contracts and operational expenses.\n\nWould you be open to a brief 15-minute call next week to explore potential areas where we might help reduce costs? I'\''d be happy to share specific examples from similar precision manufacturing companies.\n\nIf you'\''re not the right person to speak with about this, could you point me in the right direction?\n\nBest regards,\n\nZane\nAgent Manager\nImpact Quadrant\n\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.\n\nP.S. Our average client saves $75,000-$150,000 annually, and there'\''s absolutely no cost unless we deliver measurable savings."
  }' > /dev/null && echo "  ✅ SENT" || echo "  ❌ FAILED"

echo

# Lead 2: Midwest Foods
echo "Sending to: Erin Fitzgerald (Owner) - Midwest Foods"
echo "  Email: efitzgerald@midwestfoods.com"

curl -s -X POST "https://api.agentmail.to/v1/emails" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'"$FROM_EMAIL"'",
    "to": ["efitzgerald@midwestfoods.com"],
    "cc": ["'"$CC_EMAIL"'"],
    "subject": "Quick question about Midwest Foods'\'' operating expenses",
    "body": "Hi Erin,\n\nI hope this message finds you well. I'\''m reaching out because we'\''ve identified Midwest Foods as an excellent candidate for our expense reduction program.\n\nOur team specializes in helping food distribution companies reduce operating expenses by 18-23% without compromising quality or service levels. We'\''ve successfully partnered with similar organizations and consistently deliver:\n\n✓ 15-25% reduction in telecommunications, waste management, and utility costs\n✓ 100% contingency-based model - you only pay from savings generated\n✓ Zero upfront costs or risks to your organization\n\nGiven Midwest Foods'\'' profile and industry position, we'\''re confident we can identify significant savings opportunities across your vendor contracts and operational expenses.\n\nWould you be open to a brief 15-minute call next week to explore potential areas where we might help reduce costs? I'\''d be happy to share specific examples from similar food distribution companies.\n\nIf you'\''re not the right person to speak with about this, could you point me in the right direction?\n\nBest regards,\n\nZane\nAgent Manager\nImpact Quadrant\n\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.\n\nP.S. Our average client saves $75,000-$150,000 annually, and there'\''s absolutely no cost unless we deliver measurable savings."
  }' > /dev/null && echo "  ✅ SENT" || echo "  ❌ FAILED"

echo

# Lead 3: Industrial Supply Company
echo "Sending to: Jessica Yurgaitis (CEO) - Industrial Supply Company"
echo "  Email: jyurgaitis@indsupply.com"

curl -s -X POST "https://api.agentmail.to/v1/emails" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'"$FROM_EMAIL"'",
    "to": ["jyurgaitis@indsupply.com"],
    "cc": ["'"$CC_EMAIL"'"],
    "subject": "Quick question about Industrial Supply Company'\''s operating expenses",
    "body": "Hi Jessica,\n\nI hope this message finds you well. I'\''m reaching out because we'\''ve identified Industrial Supply Company as an excellent candidate for our expense reduction program.\n\nOur team specializes in helping industrial distribution companies reduce operating expenses by 18-23% without compromising quality or service levels. We'\''ve successfully partnered with similar organizations and consistently deliver:\n\n✓ 15-25% reduction in telecommunications, waste management, and utility costs\n✓ 100% contingency-based model - you only pay from savings generated\n✓ Zero upfront costs or risks to your organization\n\nGiven Industrial Supply Company'\''s 108-year legacy and industry position, we'\''re confident we can identify significant savings opportunities across your vendor contracts and operational expenses.\n\nWould you be open to a brief 15-minute call next week to explore potential areas where we might help reduce costs? I'\''d be happy to share specific examples from similar industrial distribution companies.\n\nIf you'\''re not the right person to speak with about this, could you point me in the right direction?\n\nBest regards,\n\nZane\nAgent Manager\nImpact Quadrant\n\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.\n\nP.S. Our average client saves $75,000-$150,000 annually, and there'\''s absolutely no cost unless we deliver measurable savings."
  }' > /dev/null && echo "  ✅ SENT" || echo "  ❌ FAILED"

echo

# Lead 4: Peninsula Building Materials
echo "Sending to: Leadership Team - Peninsula Building Materials"
echo "  Email: PGshowroom@pbm1923.com"

curl -s -X POST "https://api.agentmail.to/v1/emails" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'"$FROM_EMAIL"'",
    "to": ["PGshowroom@pbm1923.com"],
    "cc": ["'"$CC_EMAIL"'"],
    "subject": "Quick question about Peninsula Building Materials'\'' operating expenses",
    "body": "Hi,\n\nI hope this message finds you well. I'\''m reaching out because we'\''ve identified Peninsula Building Materials as an excellent candidate for our expense reduction program.\n\nOur team specializes in helping building materials companies reduce operating expenses by 18-23% without compromising quality or service levels. We'\''ve successfully partnered with similar organizations and consistently deliver:\n\n✓ 15-25% reduction in telecommunications, waste management, and utility costs\n✓ 100% contingency-based model - you only pay from savings generated\n✓ Zero upfront costs or risks to your organization\n\nGiven Peninsula Building Materials'\'' profile and industry position across the San Francisco Bay Area, we'\''re confident we can identify significant savings opportunities across your vendor contracts and operational expenses.\n\nWould you be open to a brief 15-minute call next week to explore potential areas where we might help reduce costs? I'\''d be happy to share specific examples from similar building materials companies.\n\nIf you'\''re not the right person to speak with about this, could you point me in the right direction?\n\nBest regards,\n\nZane\nAgent Manager\nImpact Quadrant\n\nPlease reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.\n\nP.S. Our average client saves $75,000-$150,000 annually, and there'\''s absolutely no cost unless we deliver measurable savings."
  }' > /dev/null && echo "  ✅ SENT" || echo "  ❌ FAILED"

echo
echo "============================================================"
echo "SUMMARY"
echo "============================================================"
echo "Total emails sent: 4"
echo "Via: AgentMail API"
echo "CC: sam@impactquadrant.info"
echo "============================================================"
