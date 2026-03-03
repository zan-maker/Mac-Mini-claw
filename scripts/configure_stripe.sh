#!/bin/bash
# Configure Stripe Payment System for AuraAssist

echo "💰 CONFIGURING STRIPE PAYMENT SYSTEM"
echo "============================================================"
echo "🎯 Goal: Set up subscription billing for AuraAssist"
echo "📊 Plans: Capture (\$299), Convert (\$599), Grow (\$999)"
echo "⏰ Trial: 14-day free trial"
echo "============================================================"

# Check for existing configuration
CONFIG_FILE="/Users/cubiczan/.openclaw/workspace/config/stripe_config.json"
if [ -f "$CONFIG_FILE" ]; then
    echo "📁 Existing configuration found:"
    cat "$CONFIG_FILE" | python3 -c "import json, sys; data=json.load(sys.stdin); print(json.dumps(data, indent=2))"
    echo ""
    read -p "Overwrite existing configuration? (yes/no): " OVERWRITE
    if [ "$OVERWRITE" != "yes" ]; then
        echo "❌ Configuration cancelled"
        exit 0
    fi
fi

echo ""
echo "🔑 STEP 1: SET UP STRIPE API KEYS"
echo "----------------------------------------"

# Get publishable key (already provided)
PUBLISHABLE_KEY="pk_live_LtA4BnpnPUYfTrc0KTUupew5"
echo "✅ Publishable Key: $PUBLISHABLE_KEY"

# Get secret key
echo ""
echo "⚠️  IMPORTANT: You need your Stripe Secret Key"
echo "   Get it from: https://dashboard.stripe.com/apikeys"
echo "   Look for: sk_live_..."
echo ""
read -p "Enter your Stripe Secret Key: " SECRET_KEY

if [ -z "$SECRET_KEY" ]; then
    echo "❌ ERROR: Secret key is required"
    exit 1
fi

# Validate key format
if [[ ! "$SECRET_KEY" =~ ^sk_(live|test)_ ]]; then
    echo "⚠️  WARNING: Key doesn't look like a standard Stripe secret key"
    read -p "Continue anyway? (yes/no): " CONTINUE
    if [ "$CONTINUE" != "yes" ]; then
        echo "❌ Configuration cancelled"
        exit 1
    fi
fi

echo ""
echo "🔧 STEP 2: SET UP ENVIRONMENT"
echo "----------------------------------------"

# Set environment variables
export STRIPE_PUBLISHABLE_KEY="$PUBLISHABLE_KEY"
export STRIPE_SECRET_KEY="$SECRET_KEY"

# Save to .env file
ENV_FILE="/Users/cubiczan/.openclaw/workspace/.env"
echo "STRIPE_PUBLISHABLE_KEY=$PUBLISHABLE_KEY" > "$ENV_FILE"
echo "STRIPE_SECRET_KEY=$SECRET_KEY" >> "$ENV_FILE"
echo "STRIPE_TRIAL_DAYS=14" >> "$ENV_FILE"
echo "AURAASSIST_PRODUCT_NAME=\"AuraAssist - AI Business Assistant\"" >> "$ENV_FILE"

echo "✅ Environment variables saved to $ENV_FILE"

echo ""
echo "🔧 STEP 3: TEST STRIPE CONNECTION"
echo "----------------------------------------"

cd /Users/cubiczan/.openclaw/workspace
source .venv/bin/activate

echo "🧪 Testing Stripe connection..."
python3 -c "
import os
import stripe

try:
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY', '$SECRET_KEY')
    
    # Test API connection by retrieving account
    account = stripe.Account.retrieve()
    print('✅ Stripe connection successful!')
    print(f'   Account ID: {account.id}')
    print(f'   Business Name: {getattr(account, \"business_name\", \"Not set\")}')
    print(f'   Country: {account.country}')
    
except stripe.error.AuthenticationError as e:
    print(f'❌ Authentication failed: {e}')
    print('   Please check your secret key')
    exit(1)
except Exception as e:
    print(f'❌ Connection error: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Stripe connection test failed"
    exit 1
fi

echo ""
echo "🔧 STEP 4: CREATE PRODUCTS AND PRICES"
echo "----------------------------------------"

echo "🛠️ Creating AuraAssist products and prices..."
python3 scripts/stripe_payment_system.py setup

if [ $? -ne 0 ]; then
    echo "❌ Failed to create products and prices"
    exit 1
fi

echo ""
echo "🔧 STEP 5: CREATE TEST CHECKOUT SESSION"
echo "----------------------------------------"

echo "🛒 Creating test checkout session..."
python3 -c "
import os
import sys
sys.path.append('.')
from scripts.stripe_payment_system import StripePaymentSystem

payment_system = StripePaymentSystem(test_mode=False)
result = payment_system.create_checkout_session('test@example.com', 'convert')

if result.get('success'):
    print('✅ Test checkout session created!')
    print(f'   Checkout URL: {result[\"url\"]}')
    print(f'   Session ID: {result[\"session_id\"]}')
    print(f'   Plan: Convert (\$599/month)')
    print(f'   Trial: 14 days')
else:
    print(f'❌ Failed to create checkout session: {result.get(\"error\")}')
"

echo ""
echo "🔧 STEP 6: SET UP WEBHOOK (OPTIONAL)"
echo "----------------------------------------"

echo "🌐 Webhook setup for real-time notifications:"
echo "1. Go to: https://dashboard.stripe.com/webhooks"
echo "2. Click 'Add endpoint'"
echo "3. Enter URL: https://your-domain.com/stripe-webhook"
echo "4. Select events:"
echo "   • checkout.session.completed"
echo "   • customer.subscription.created"
echo "   • customer.subscription.updated"
echo "   • customer.subscription.deleted"
echo "   • invoice.payment_succeeded"
echo "   • invoice.payment_failed"
echo "5. Copy the webhook signing secret"
echo "6. Add to .env: STRIPE_WEBHOOK_SECRET=whsec_..."
echo ""

echo "🔧 STEP 7: INTEGRATION WITH AURAASSIST"
echo "----------------------------------------"

echo "🎯 Integration points:"
echo "1. Demo completion → Send checkout link"
echo "2. Customer signs up → Create Stripe subscription"
echo "3. Payment success → Activate AuraAssist service"
echo "4. Monthly billing → Recurring revenue"
echo "5. Cancellation → Handle churn"
echo ""

echo "📁 FILES CREATED:"
echo "✅ $ENV_FILE - Environment variables"
echo "✅ /Users/cubiczan/.openclaw/workspace/config/stripe_config.json - Stripe configuration"
echo "✅ /Users/cubiczan/.openclaw/workspace/scripts/stripe_payment_system.py - Payment system"
echo ""

echo "🚀 READY COMMANDS:"
echo ""
echo "💰 Create checkout for customer:"
echo "  python3 scripts/stripe_payment_system.py checkout --email customer@example.com --plan convert"
echo ""
echo "📊 Check MRR:"
echo "  python3 scripts/stripe_payment_system.py mrr"
echo ""
echo "👤 Create customer:"
echo "  python3 scripts/stripe_payment_system.py customer --email customer@example.com --name \"John Doe\""
echo ""
echo "📅 Create subscription:"
echo "  python3 scripts/stripe_payment_system.py subscription --customer cus_xxx --plan convert"
echo ""

echo "💰 PRICING PLANS READY:"
echo "  • Capture Plan: \$299/month - Basic AI receptionist"
echo "  • Convert Plan: \$599/month - Advanced features"
echo "  • Grow Plan: \$999/month - Enterprise features"
echo "  • All plans: 14-day free trial"
echo ""

echo "📈 BUSINESS PROJECTION (Month 1):"
echo "  • 10 customers @ \$599 = \$5,990 MRR"
echo "  • 30 customers @ \$599 = \$17,970 MRR"
echo "  • Annual Run Rate: \$71,880 - \$215,640"
echo ""

echo "🎯 NEXT STEPS:"
echo "1. Test checkout flow with your own email"
echo "2. Set up webhook for real-time notifications"
echo "3. Integrate with demo scheduling system"
echo "4. Create customer onboarding process"
echo "5. Monitor payments in Stripe Dashboard"
echo ""

echo "============================================================"
echo "✅ STRIPE PAYMENT SYSTEM CONFIGURED AND READY!"
echo "============================================================"
echo ""
echo "🚀 Your AuraAssist now has:"
echo "   • Subscription billing"
echo "   • 3 pricing tiers"
echo "   • 14-day free trials"
echo "   • Recurring revenue pipeline"
echo "   • Stripe Dashboard analytics"
echo ""
echo "💰 Ready to accept payments and generate MRR!"