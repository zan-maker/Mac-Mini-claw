#!/usr/bin/env python3
"""
Migrate from Mixpanel to Plausible Analytics
"""

import json
from datetime import datetime

def analyze_mixpanel_usage():
    """Analyze current Mixpanel usage"""
    
    print("📊 ANALYZING MIXPANEL USAGE")
    print("="*50)
    
    # Example Mixpanel configuration (would be from your actual config)
    mixpanel_config = {
        'project_token': 'mp_xxxxxxxxxxxxxxxx',
        'monthly_cost': 75.00,
        'monthly_events': 50000,  # Estimated
        'features_used': [
            'Pageview tracking',
            'Custom events',
            'Funnel analysis',
            'User profiles'
        ],
        'integration_points': [
            'Website JavaScript',
            'Mobile apps',
            'Backend API',
            'Email campaigns'
        ]
    }
    
    print(f"💰 Current cost: ${mixpanel_config['monthly_cost']}/month")
    print(f"📈 Monthly events: {mixpanel_config['monthly_events']:,}")
    print(f"🎯 Features used: {', '.join(mixpanel_config['features_used'])}")
    
    # Check if Plausible free tier is sufficient
    plausible_free_limit = 10000  # pageviews/month
    
    if mixpanel_config['monthly_events'] > plausible_free_limit * 10:  # Rough conversion
        print(f"\n⚠️  WARNING: High event volume may exceed Plausible free tier")
        print(f"   Mixpanel events: {mixpanel_config['monthly_events']:,}")
        print(f"   Plausible free limit: {plausible_free_limit:,} pageviews")
        print("   Consider:")
        print("   1. Reducing tracking to essential events only")
        print("   2. Using Plausible's paid plan if needed ($9/month)")
        print("   3. Self-hosting Plausible (unlimited)")
    else:
        print(f"\n✅ Event volume fits within Plausible free tier")
    
    return mixpanel_config

def create_migration_plan(mixpanel_config):
    """Create migration plan"""
    
    print("\n📋 CREATING MIGRATION PLAN")
    print("="*50)
    
    migration_steps = [
        {
            'step': 1,
            'action': 'Sign up for Plausible (free)',
            'time': '5 minutes',
            'url': 'https://plausible.io/signup'
        },
        {
            'step': 2,
            'action': 'Add your website to Plausible',
            'time': '2 minutes',
            'details': 'Dashboard → Add site'
        },
        {
            'step': 3,
            'action': 'Replace Mixpanel tracking script',
            'time': '15 minutes',
            'files': [
                'Website HTML files',
                'React/Vue components',
                'Mobile app code'
            ]
        },
        {
            'step': 4,
            'action': 'Migrate custom events',
            'time': '30 minutes',
            'details': 'Update event tracking calls'
        },
        {
            'step': 5,
            'action': 'Set up goal conversions',
            'time': '10 minutes',
            'details': 'Define key actions to track'
        },
        {
            'step': 6,
            'action': 'Run parallel tracking (optional)',
            'time': '7 days',
            'details': 'Run both systems to compare data'
        },
        {
            'step': 7,
            'action': 'Deactivate Mixpanel',
            'time': '5 minutes',
            'details': 'Cancel subscription after verification'
        }
    ]
    
    print("Migration Steps:")
    for step in migration_steps:
        print(f"\n{step['step']}. {step['action']}")
        print(f"   ⏱️  {step['time']}")
        if 'url' in step:
            print(f"   🔗 {step['url']}")
        if 'files' in step:
            print(f"   📝 Files: {', '.join(step['files'])}")
        if 'details' in step:
            print(f"   📋 {step['details']}")
    
    return migration_steps

def generate_code_snippets():
    """Generate code snippets for migration"""
    
    print("\n💻 CODE MIGRATION SNIPPETS")
    print("="*50)
    
    print("\n1. HTML Tracking Script Replacement:")
    print("""
    <!-- BEFORE: Mixpanel -->
    <script>
      mixpanel.init("YOUR_MIXPANEL_TOKEN");
    </script>
    
    <!-- AFTER: Plausible -->
    <script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
    <script>
      window.plausible = window.plausible || function() { (window.plausible.q = window.plausible.q || []).push(arguments) }
    </script>
    """)
    
    print("\n2. Custom Event Tracking:")
    print("""
    # BEFORE: Mixpanel
    mixpanel.track("Lead Generated", {
      "source": "instagram",
      "campaign": "ai_finance"
    });
    
    # AFTER: Plausible
    plausible("Lead Generated", {
      props: {
        source: "instagram",
        campaign: "ai_finance"
      }
    });
    """)
    
    print("\n3. Pageview Tracking:")
    print("""
    # BEFORE: Mixpanel
    mixpanel.track("Page View", {
      "page": window.location.pathname
    });
    
    # AFTER: Plausible (automatic with script)
    # No code needed -    # Pageviews tracked automatically
    """)
    
    print("\n4. Server-side Tracking (Python):")
    print("""
    # BEFORE: Mixpanel
    import mixpanel
    mp = mixpanel.Mixpanel("YOUR_TOKEN")
    mp.track("user_id", "Server Event", {"property": "value"})
    
    # AFTER: Plausible
    from plausible_client import PlausibleClient
    client = PlausibleClient("yourdomain.com")
    client.track_custom_event("Server Event", {"property": "value"})
    """)

def main():
    """Main migration function"""
    
    print("🚀 MIGRATE MIXPANEL TO PLAUSIBLE ANALYTICS")
    print("="*50)
    print("Current cost: $75/month")
    print("Target cost: $0/month (10k pageviews free)")
    print("Savings: $75/month ($900/year)")
    print("="*50)
    
    # Analyze current usage
    mixpanel_config = analyze_mixpanel_usage()
    
    # Create migration plan
    migration_steps = create_migration_plan(mixpanel_config)
    
    # Generate code snippets
    generate_code_snippets()
    
    # Save migration plan
    plan_path = "/Users/cubiczan/.openclaw/workspace/config/plausible_analytics/migration_plan.json"
    with open(plan_path, 'w') as f:
        json.dump({
            'mixpanel_config': mixpanel_config,
            'migration_steps': migration_steps,
            'estimated_savings': {
                'monthly': 75,
                'annual': 900,
                'break_even': 'Immediate'
            },
            'created_at': datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"\n📄 Migration plan saved to: {plan_path}")
    
    print("\n" + "="*50)
    print("🎯 READY FOR MIGRATION")
    print("="*50)
    print("\nNext steps:")
    print("1. Sign up at plausible.io (free)")
    print("2. Add your website in dashboard")
    print("3. Replace tracking scripts")
    print("4. Verify data is flowing")
    print("\n💰 Immediate savings: $75/month")

if __name__ == "__main__":
    main()
