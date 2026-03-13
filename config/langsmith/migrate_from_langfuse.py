#!/usr/bin/env python3
"""
Migrate from Langfuse to LangSmith
"""

import json
from datetime import datetime

def analyze_langfuse_usage():
    """Analyze current Langfuse usage"""
    
    print("📊 ANALYZING LANGFUSE USAGE")
    print("="*50)
    
    # Example Langfuse configuration
    langfuse_config = {
        'public_key': 'pk_lf_xxxxxxxx',
        'secret_key': 'sk_lf_xxxxxxxx',
        'monthly_cost': 50.00,
        'monthly_traces': 15000,  # Estimated
        'features_used': [
            'Trace collection',
            'Prompt management',
            'Evaluation',
            'Analytics dashboard'
        ],
        'integrated_services': [
            'OpenAI API calls',
            'Anthropic API calls',
            'Custom Python scripts',
            'Web application'
        ]
    }
    
    print(f"💰 Current cost: ${langfuse_config['monthly_cost']}/month")
    print(f"📈 Monthly traces: {langfuse_config['monthly_traces']:,}")
    print(f"🎯 Features used: {', '.join(langfuse_config['features_used'])}")
    
    # Check if LangSmith free tier is sufficient
    langsmith_free_limit = 1000  # traces/day
    
    daily_traces = langfuse_config['monthly_traces'] / 30
    if daily_traces > langsmith_free_limit:
        print(f"\n⚠️  WARNING: Trace volume may exceed LangSmith free tier")
        print(f"   Daily traces: {daily_traces:.0f}")
        print(f"   LangSmith free limit: {langsmith_free_limit}/day")
        print("   Consider:")
        print("   1. Sampling traces (e.g., 10% of calls)")
        print("   2. Using LangSmith's paid plan if needed")
        print("   3. Keeping Langfuse for critical traces only")
    else:
        print(f"\n✅ Trace volume fits within LangSmith free tier")
        print(f"   Daily traces: {daily_traces:.0f}")
        print(f"   LangSmith free limit: {langsmith_free_limit}/day")
    
    return langfuse_config

def create_migration_plan(langfuse_config):
    """Create migration plan"""
    
    print("\n📋 CREATING MIGRATION PLAN")
    print("="*50)
    
    migration_steps = [
        {
            'step': 1,
            'action': 'Sign up for LangSmith (free)',
            'time': '5 minutes',
            'url': 'https://smith.langchain.com'
        },
        {
            'step': 2,
            'action': 'Create API key',
            'time': '2 minutes',
            'details': 'Settings → API Keys'
        },
        {
            'step': 3,
            'action': 'Install LangSmith SDK',
            'time': '2 minutes',
            'command': 'pip install langsmith'
        },
        {
            'step': 4,
            'action': 'Update environment variables            'time': '5 minutes',
            'details': 'Set LANGSMITH_API_KEY'
        },
        {
            'step': 5,
            'action': 'Instrument LLM calls',
            'time': '30-60 minutes',
            'details': 'Add tracing to your code'
        },
        {
            'step': 6,
            'action': 'Migrate prompts (if using LangChain)',
            'time': '15 minutes',
            'details': 'Import prompts to LangSmith'
        },
        {
            'step': 7,
            'action': 'Run parallel collection (optional)',
            'time': '7 days',
            'details': 'Collect traces in both systems'
        },
        {
            'step': 8,
            'action': 'Deactivate Langfuse',
            'time': '5 minutes',
            'details': 'Cancel subscription'
        }
    ]
    
    print("Migration Steps:")
    for step in migration_steps:
        print(f"\n{step['step']}. {step['action']}")
        print(f"   ⏱️  {step['time']}")
        if 'url' in step:
            print(f"   🔗 {step['url']}")
        if 'command' in step:
            print(f"   💻 {step['command']}")
        if 'details' in step:
            print(f"   📋 {step['details']}")
    
    return migration_steps

def generate_code_snippets():
    """Generate code snippets for migration"""
    
    print("\n💻 CODE MIGRATION SNIPPETS")
    print("="*50)
    
    print("\n1. Environment Setup:")
    print("""
    # BEFORE: Langfuse
    export LANGFUSE_PUBLIC_KEY="pk_lf_..."
    export LANGFUSE_SECRET_KEY="sk_lf_..."
    
    # AFTER: LangSmith
    export LANGSMITH_API_KEY="ls_..."
    export LANGSMITH_TRACING=true
    """)
    
    print("\n2. Basic Tracing (Python):")
    print("""
    # BEFORE: Langfuse
    from langfuse import Langfuse
    langfuse = Langfuse()
    trace = langfuse.trace(name="llm_call")
    generation = trace.generation(
        name="chat_completion",
        input={"messages": messages},
        output={"content": response}
    )
    
    # AFTER: LangSmith
    from langsmith import Client
    client = Client()
    client.create_run(
        run_name="llm_call",
        run_type="llm",
        inputs={"messages": messages},
        outputs={"content": response}
    )
    """)
    
    print("\n3. With LangChain Integration:")
    print("""
    # BEFORE: Langfuse + LangChain
    from langfuse.callback import CallbackHandler
    handler = CallbackHandler()
    chain.invoke(input, config={"callbacks": [handler]})
    
    # AFTER: LangSmith (built-in)
    # No extra code needed - LangChain automatically uses LangSmith
    # when LANGSMITH_TRACING=true is set
    """)
    
    print("\n4. Custom Tracing Wrapper:")
    print("""
    # Using our LangSmith client wrapper
    from langsmith_client import LangSmithClient
    
    client = LangSmithClient(project_name="ai-agents")
    
    # Trace an LLM call
    client.trace_llm_call(
        run_id="chat_123",
        inputs={"prompt": "Explain AI finance"},
        outputs={"response": "AI finance combines..."},
        metadata={"model": "gpt-4", "tokens": 150}
    )
    
    # Trace a chain
    client.trace_chain(
        chain_id="lead_gen_123",
        steps=[
            {"name": "research", "inputs": {"query": "..."}, "outputs": {"data": "..."}},
            {"name": "analysis", "inputs": {"data": "..."}, "outputs": {"insights": "..."}},
            {"name": "email", "inputs": {"insights": "..."}, "outputs": {"email": "..."}}
        ]
    )
    """)

def main():
    """Main migration function"""
    
    print("🚀 MIGRATE LANGFUSE TO LANGSMITH")
    print("="*50)
    print("Current cost: $50/month")
    print("Target cost: $0/month (1k traces/day free)")
    print("Savings: $50/month ($600/year)")
    print("="*50)
    
    # Analyze current usage
    langfuse_config = analyze_langfuse_usage()
    
    # Create migration plan
    migration_steps = create_migration_plan(langfuse_config)
    
    # Generate code snippets
    generate_code_snippets()
    
    # Save migration plan
    plan_path = "/Users/cubiczan/.openclaw/workspace/config/langsmith/migration_plan.json"
    with open(plan_path, 'w') as f:
        json.dump({
            'langfuse_config': langfuse_config,
            'migration_steps': migration_steps,
            'estimated_savings': {
                'monthly': 50,
                'annual': 600,
                'break_even': 'Immediate'
            },
            'created_at': datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"\n📄 Migration plan saved to: {plan_path}")
    
    print("\n" + "="*50)
    print("🎯 READY FOR MIGRATION")
    print("="*50)
    print("\nNext steps:")
    print("1. Sign up at smith.langchain.com")
    print("2. Create API key")
    print("3. Install: pip install langsmith")
    print("4. Update environment variables")
    print("5. Instrument your LLM calls")
    print("\n💰 Immediate savings: $50/month")

if __name__ == "__main__":
    main()
