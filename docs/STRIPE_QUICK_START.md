
# Stripe Payment System - Quick Start Guide

## Three Service Models:

### 1. Expense Reduction Service (Contingency-based)
- **Pricing:** 30% of verified savings
- **Payment:** After savings verified, create invoice
- **Agreement:** https://impactquadrant.info/agreements/expense-reduction
- **Process:** Audit → Identify savings → Implement → Verify → Invoice

### 2. Deal Origination Referral (Success fee)
- **Pricing:** 1-3% of deal value
- **Payment:** Upon successful deal closing
- **Agreement:** https://impactquadrant.info/agreements/deal-origination
- **Process:** Match → Introduce → Negotiate → Close → Invoice

### 3. AI Agency Monthly Subscription
- **Pricing:** $997/month
- **Payment:** Monthly recurring via Stripe
- **Signup:** https://buy.stripe.com/aFa14nfHp7MSa6a7Fo8g000
- **Process:** Signup → Monthly billing → Service delivery

## How to Use:

### For Qualified Leads:
1. Determine which service fits the lead
2. Send appropriate email template with agreement/payment link
3. Track responses in Stripe Dashboard
4. Follow up based on payment status

### Integration with AgentMail:
Use the `stripe-agentmail-integration.py` script to:
- Generate personalized payment emails
- Send via AgentMail API
- Track sends and responses

### Monitoring Payments:
- **Dashboard:** https://dashboard.stripe.com
- **Subscriptions:** Active/Churned customers
- **Invoices:** Paid/Pending/Overdue
- **Revenue:** Monthly recurring revenue (MRR)

## Testing:
- **Test mode:** Use `sk_test_...` and `pk_test_...` keys
- **Test card:** `4242 4242 4242 4242` (success)
- **Test email:** Any email works in test mode

## Next Steps:
1. Create actual agreement documents at the URLs above
2. Integrate with lead generator cron jobs
3. Set up webhooks for payment notifications
4. Create reporting dashboard
