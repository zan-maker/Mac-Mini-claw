# Stripe Payment System Integration

**API Key:** `pk_live_LtA4BnpnPUYfTrc0KTUupew5` (Publishable Key)
**Environment:** Live Production
**Purpose:** Payment processing for expense reduction, deal origination, and AI agency services

---

## Setup Requirements

### 1. **Secret Key Needed**
For server-side operations, you need a **secret key** (starts with `sk_live_`):
- Get from: https://dashboard.stripe.com/apikeys
- Store securely in environment variables

### 2. **Webhook Endpoint**
For payment notifications:
- URL: `https://your-domain.com/stripe-webhook`
- Events to listen for: `payment_intent.succeeded`, `invoice.paid`, `customer.subscription.created`

### 3. **Products & Prices**
Create in Stripe Dashboard:
- **Expense Reduction Service** (One-time or % of savings)
- **Deal Origination Referral Fee** (Success-based)
- **AI Agency Monthly Subscription** (Recurring)

---

## Integration Architecture

### **Payment Flow:**
```
Lead → Outreach → Service Agreement → Stripe Checkout → Payment → Service Delivery
```

### **Components:**

1. **Checkout Sessions** - One-time payments
2. **Subscriptions** - Recurring services  
3. **Invoices** - Custom billing
4. **Webhooks** - Payment notifications
5. **Customer Portal** - Self-service management

---

## Implementation Steps

### **Phase 1: Basic Setup**
```bash
# Install Stripe Python library
pip install stripe
```

### **Phase 2: Configuration**
```python
import stripe
import os

# Configure Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_version = '2025-02-24.acacia'  # Latest stable

# Publishable key for frontend
STRIPE_PUBLISHABLE_KEY = 'pk_live_LtA4BnpnPUYfTrc0KTUupew5'
```

### **Phase 3: Product Creation**
```python
# Create products in Stripe (run once)
products = {
    'expense_reduction': {
        'name': 'Expense Reduction Service',
        'description': '15-25% OPEX reduction with contingency-based pricing'
    },
    'deal_origination': {
        'name': 'Deal Origination Referral',
        'description': 'Success-based referral fee for business acquisitions'
    },
    'ai_agency_monthly': {
        'name': 'AI Agency Monthly Subscription',
        'description': 'Monthly AI-powered lead generation and outreach'
    }
}
```

### **Phase 4: Checkout Integration**
```python
def create_checkout_session(product_id, customer_email, success_url, cancel_url):
    """Create Stripe Checkout session"""
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': product_id,
            'quantity': 1,
        }],
        mode='payment',
        customer_email=customer_email,
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            'service_type': 'expense_reduction',
            'lead_id': '12345'
        }
    )
    return session.url  # Redirect customer to this URL
```

---

## Use Cases

### **1. Expense Reduction Service**
- **Pricing:** 30% of first-year savings (contingency-based)
- **Payment:** After savings verified, invoice via Stripe
- **Flow:** Agreement → Service → Verification → Invoice → Payment

### **2. Deal Origination Referral**
- **Pricing:** 1-3% of deal value (success fee)
- **Payment:** Upon deal closing
- **Flow:** Match → Intro → Deal Close → Invoice → Payment

### **3. AI Agency Subscription**
- **Pricing:** $997/month (lead generation service)
- **Payment:** Monthly recurring
- **Flow:** Signup → Subscription → Monthly billing

---

## Webhook Handling

### **Payment Success Webhook:**
```python
@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET')
        )
    except ValueError as e:
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        return 'Invalid signature', 400
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_successful_payment(payment_intent)
    
    return jsonify({'status': 'success'})
```

---

## Dashboard & Reporting

### **Stripe Dashboard Features:**
- **Revenue Tracking:** Real-time payment monitoring
- **Customer Management:** Client profiles and history
- **Invoice Generation:** Professional billing
- **Analytics:** Revenue trends, churn rates
- **Tax Compliance:** Automatic tax calculations

### **Custom Reporting:**
- Monthly revenue by service type
- Client payment history
- Outstanding invoices
- Subscription metrics

---

## Security Considerations

### **API Key Security:**
```bash
# Store in environment variables
export STRIPE_SECRET_KEY='sk_live_...'
export STRIPE_PUBLISHABLE_KEY='pk_live_LtA4BnpnPUYfTrc0KTUupew5'
export STRIPE_WEBHOOK_SECRET='whsec_...'
```

### **PCI Compliance:**
- Never store card details
- Use Stripe Elements/Checkout for card collection
- Webhook signature verification
- HTTPS required for all endpoints

---

## Integration with Existing Systems

### **AgentMail Integration:**
- Send payment links in outreach emails
- Track email → payment conversion
- Automated follow-ups for unpaid invoices

### **Lead Generator Integration:**
- Qualify leads based on payment ability
- Track lead value through payment history
- Prioritize high-value prospects

### **ROI Analyst Integration:**
- Calculate ROI based on service fees
- Track payment vs. value delivered
- Optimize pricing strategies

---

## Next Steps

### **Immediate:**
1. Get **secret key** from Stripe Dashboard
2. Set up **webhook endpoint**
3. Create **products & prices** in Stripe
4. Test with **Stripe test mode**

### **Short-term:**
1. Integrate with AgentMail for payment links
2. Create invoice templates
3. Set up subscription management
4. Build reporting dashboard

### **Long-term:**
1. Automated payment reminders
2. Client portal for self-service
3. Advanced analytics
4. Multi-currency support

---

## Testing

### **Test Mode:**
```python
# Use test keys for development
stripe.api_key = 'sk_test_...'  # Test secret key
STRIPE_PUBLISHABLE_KEY = 'pk_test_...'  # Test publishable key
```

### **Test Cards:**
- `4242 4242 4242 4242` - Success
- `4000 0000 0000 0002` - Declined
- `4000 0000 0000 0069` - Expired

---

## Support & Resources

- **Stripe Docs:** https://docs.stripe.com/api
- **Python Library:** https://github.com/stripe/stripe-python
- **Dashboard:** https://dashboard.stripe.com
- **Webhook Tester:** https://dashboard.stripe.com/test/webhooks

---

**Status:** Ready for implementation
**Priority:** High (enables monetization)
**Estimated Time:** 2-3 days for basic integration
