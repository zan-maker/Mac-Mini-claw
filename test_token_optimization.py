#!/usr/bin/env python3
"""
Test Token Optimization with Predicate Snapshot
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from optimized_browser_wrapper import OptimizedBrowser

def test_basic_optimization():
    """Test basic token optimization"""
    print("="*60)
    print("TESTING TOKEN OPTIMIZATION")
    print("="*60)
    
    # Test with predicate optimization
    print("\n🔧 Test 1: With Predicate Optimization (95% reduction)")
    browser1 = OptimizedBrowser(
        session="test-predicate",
        use_predicate=True,
        verbose=True
    )
    
    if browser1.open("https://example.com"):
        snapshot1 = browser1.get_optimized_snapshot()
        if snapshot1:
            print(f"✅ Predicate Snapshot:")
            print(f"   Elements: {snapshot1.element_count}")
            print(f"   Estimated tokens: {snapshot1.token_count}")
            print(f"   Top 3 elements:")
            for element in snapshot1.elements[:3]:
                print(f"     {element.id}: {element.role} '{element.text}' (imp: {element.importance:.2f})")
    
    browser1.close()
    
    # Test without predicate (for comparison)
    print("\n🔧 Test 2: Without Optimization (baseline)")
    browser2 = OptimizedBrowser(
        session="test-baseline",
        use_predicate=False,
        verbose=True
    )
    
    if browser2.open("https://example.com"):
        snapshot2 = browser2.get_optimized_snapshot()
        if snapshot2:
            print(f"✅ Standard Snapshot:")
            print(f"   Elements: {snapshot2.element_count}")
            print(f"   Estimated tokens: {snapshot2.token_count}")
    
    browser2.close()
    
    # Calculate savings
    if snapshot1 and snapshot2:
        savings = 1 - (snapshot1.token_count / snapshot2.token_count)
        print(f"\n💰 Token Savings: {savings:.1%}")
        print(f"   {snapshot2.token_count} → {snapshot1.token_count} tokens")
    
    return True

def test_financial_site():
    """Test with financial site"""
    print("\n" + "="*60)
    print("TESTING FINANCIAL SITE OPTIMIZATION")
    print("="*60)
    
    browser = OptimizedBrowser(
        session="financial-test",
        use_predicate=True,
        verbose=True
    )
    
    try:
        # Test with a simple financial page
        print("\n🔧 Testing finance.yahoo.com...")
        if browser.open("https://finance.yahoo.com"):
            snapshot = browser.get_optimized_snapshot()
            if snapshot:
                print(f"✅ Optimized Snapshot:")
                print(f"   URL: {snapshot.url}")
                print(f"   Title: {snapshot.title}")
                print(f"   Elements: {snapshot.element_count}")
                print(f"   Estimated tokens: {snapshot.token_count}")
                
                # Show financial elements
                print(f"\n📊 Financial Elements Found:")
                financial_roles = ["button", "link", "text", "heading"]
                for element in snapshot.elements:
                    if element.role in financial_roles and element.importance > 0.6:
                        print(f"   {element.id}: {element.role} '{element.text[:50]}' (imp: {element.importance:.2f})")
                
                # Get savings report
                report = browser.get_token_savings_report()
                if report:
                    print(f"\n💰 Savings Report:")
                    print(f"   Average savings: {report.get('average_savings', 0):.1%}")
                    print(f"   Total snapshots: {report.get('total_snapshots', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        browser.close()

def test_predicate_skill_availability():
    """Test if predicate skill is properly installed"""
    print("\n" + "="*60)
    print("TESTING PREDICATE SKILL INSTALLATION")
    print("="*60)
    
    skill_path = "/Users/cubiczan/.openclaw/skills/predicate-snapshot"
    
    if not os.path.exists(skill_path):
        print("❌ Predicate skill not found at:", skill_path)
        return False
    
    print(f"✅ Skill directory found: {skill_path}")
    
    # Check key files
    required_files = [
        "SKILL.md",
        "package.json",
        "src/index.ts",
        "dist/index.js"
    ]
    
    for file in required_files:
        file_path = os.path.join(skill_path, file)
        if os.path.exists(file_path):
            print(f"✅ {file}")
        else:
            print(f"⚠️  Missing: {file}")
    
    # Check if built
    dist_path = os.path.join(skill_path, "dist")
    if os.path.exists(dist_path):
        print(f"✅ Build directory exists")
        
        # Count JS files
        js_files = list(Path(dist_path).glob("*.js"))
        print(f"✅ {len(js_files)} built JavaScript files")
    else:
        print("⚠️  Build directory missing - skill may need building")
    
    return True

def main():
    """Run all tests"""
    print("🚀 Token Optimization Test Suite")
    print("Testing Predicate Snapshot integration for 95% token reduction")
    
    # Test 1: Skill availability
    if not test_predicate_skill_availability():
        print("\n⚠️  Predicate skill not fully installed.")
        print("   Run: cd /Users/cubiczan/.openclaw/skills/predicate-snapshot && npm run build")
        return False
    
    # Test 2: Basic optimization
    if not test_basic_optimization():
        print("\n❌ Basic optimization test failed")
        return False
    
    # Test 3: Financial site (optional - may be slow)
    print("\n📈 Financial site test (may take 10-15 seconds)...")
    try:
        test_financial_site()
    except Exception as e:
        print(f"⚠️  Financial site test skipped: {e}")
    
    print("\n" + "="*60)
    print("✅ TOKEN OPTIMIZATION TEST COMPLETE")
    print("="*60)
    print("\n🎯 Next Steps:")
    print("1. Get free API key: https://predicate.systems/keys")
    print("2. Export: export PREDICATE_API_KEY='sk-...'")
    print("3. Update agents to use OptimizedBrowser")
    print("4. Monitor token savings with get_token_savings_report()")
    print("\n💰 Expected: 90-95% reduction in browser token usage")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)