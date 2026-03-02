#!/bin/bash
# Stripe Payment System Setup Script
# Sets up environment and tests Stripe integration

echo "=========================================="
echo "STRIPE PAYMENT SYSTEM SETUP"
echo "=========================================="
echo

# Check for required environment variables
echo "Checking environment variables..."
echo

if [ -z "$STRIPE_SECRET_KEY" ]; then
    echo "❌ STRIPE_SECRET_KEY is not set"
    echo
    echo "To set up Stripe payments, you need:"
    echo "1. Go to: https://dashboard.stripe.com/apikeys"
    echo "2. Copy your 'Secret Key' (starts with sk_live_)"
    echo "3. Add to your environment:"
    echo
    echo "   export STRIPE_SECRET_KEY='sk_live_...'"
    echo "   export STRIPE_PUBLISHABLE_KEY='pk_live_LtA4BnpnPUYfTrc0KTUupew5'"
    echo
    echo "For testing, use test keys:"
    echo "   export STRIPE_SECRET_KEY='sk_test_...'"
    echo "   export STRIPE_PUBLISHABLE_KEY='pk_test_...'"
    echo
else
    echo "✅ STRIPE_SECRET_KEY is set"
    echo "   Key: ${STRIPE_SECRET_KEY:0:20}..."
fi

echo
echo "=========================================="
echo "TESTING INTEGRATION"
echo "=========================================="
echo

# Test Python environment
echo "Testing Python environment..."
python3 -c "import stripe; print('✅ Stripe library installed:', stripe.__version__)" 2>/dev/null || echo "❌ Stripe library not installed"

echo
echo "Testing configuration files..."
if [ -f "/Users/cubiczan/.openclaw/workspace/stripe-config.json" ]; then
    echo "✅ Configuration file exists"
else
    echo "❌ Configuration file missing"
    echo "   Run: python3 /Users/cubiczan/.openclaw/workspace/scripts/stripe-payment-links.py"
fi

echo
echo "=========================================="
echo "AVAILABLE SCRIPTS"
echo "=========================================="
echo

echo "1. Setup Stripe products & prices:"
echo "   python3 /Users/cubiczan/.openclaw/workspace/scripts/stripe-setup.py"
echo
echo "2. Generate payment links for outreach:"
echo "   python3 /Users/cubiczan/.openclaw/workspace/scripts/stripe-payment-links.py"
echo
echo "3. Integrate with AgentMail:"
echo "   python3 /Users/cubiczan/.openclaw/workspace/scripts/stripe-agentmail-integration.py"
echo
echo "4. Test payment flow (requires secret key):"
echo "   python3 -c \"import stripe; stripe.api_key = '\$STRIPE_SECRET_KEY'; print('✅ Stripe connection test:', stripe.Balance.retrieve())\""
echo

echo "=========================================="
echo "NEXT STEPS"
echo "=========================================="
echo

echo "1. Get your Stripe Secret Key"
echo "2. Export it: export STRIPE_SECRET_KEY='sk_live_...'"
echo "3. Run setup: python3 /Users/cubiczan/.openclaw/workspace/scripts/stripe-setup.py"
echo "4. Create actual payment links in Stripe Dashboard"
echo "5. Update configuration with real payment links"
echo "6. Integrate with lead generator cron jobs"
echo

echo "=========================================="
echo "PAYMENT LINKS FOR SERVICES"
echo "=========================================="
echo

echo "Create these in Stripe Dashboard (Products → Payment Links):"
echo
echo "1. Expense Reduction Service"
echo "   • Price: $0 (contingency-based)"
echo "   • Description: 30% of verified savings"
echo "   • Terms: Pay only from savings"
echo
echo "2. Deal Origination Referral"
echo "   • Price: $0 (success fee)"
echo "   • Description: 1-3% of deal value"
echo "   • Terms: Pay upon deal closing"
echo
echo "3. AI Agency Monthly Subscription"
echo "   • Price: $997/month"
echo "   • Description: Lead generation service"
echo "   • Terms: Monthly, cancel anytime"
echo

echo "=========================================="
echo "INTEGRATION WITH EXISTING SYSTEMS"
echo "=========================================="
echo

echo "To integrate with existing cron jobs:"
echo
echo "1. Modify lead generator to include payment links"
echo "2. Add payment email step after initial contact"
echo "3. Track payments in Stripe Dashboard"
echo "4. Set up webhooks for payment notifications"
echo "5. Automate follow-ups based on payment status"
echo

echo "Documentation: /Users/cubiczan/.openclaw/workspace/docs/STRIPE_INTEGRATION.md"
echo "Configuration: /Users/cubiczan/.openclaw/workspace/stripe-config.json"
echo "Logs: /Users/cubiczan/.openclaw/workspace/stripe-payment-logs.jsonl"
echo

echo "✅ Setup script complete"
echo "   Run with STRIPE_SECRET_KEY set to test actual integration"
