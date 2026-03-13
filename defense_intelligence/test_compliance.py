#!/usr/bin/env python3
"""
Quick test of defense compliance system
"""

import sys
sys.path.append('.')

from compliance_system import (
    DefenseComplianceSystem, ClassificationLevel, 
    ExportControlCategory, MineralData, UserClearance
)
import datetime

def test_basic_compliance():
    """Test basic compliance functionality"""
    print("🧪 TESTING DEFENSE COMPLIANCE SYSTEM")
    print("="*50)
    
    system = DefenseComplianceSystem()
    
    # Test classification function
    print("\n🔍 Testing Mineral Classification:")
    
    test_cases = [
        ("rare_earth", "production", "government"),
        ("lithium", "market_data", "industry"),
        ("copper", "production", "open_source"),
        ("tungsten", "supply_chain", "intelligence")
    ]
    
    for mineral, data_type, source in test_cases:
        classification, export = system.classify_mineral_data(mineral, data_type, source)
        print(f"  {mineral:12} {data_type:15} {source:12} → {classification.value:15} {export.value}")
    
    # Test user registration
    print("\n👥 Testing User Registration:")
    
    user = system.register_user(
        user_id="test_user_001",
        clearance_level=ClassificationLevel.CUI,
        is_us_person=True,
        training_complete=True,
        background_check=datetime.date(2025, 1, 1),
        authorized_minerals=["rare_earth", "lithium", "cobalt"]
    )
    
    print(f"  ✅ User registered: {user.user_id}")
    print(f"     Clearance: {user.clearance_level.value}")
    print(f"     US Person: {user.is_us_person}")
    print(f"     Training: {user.export_training_complete}")
    print(f"     Authorized minerals: {', '.join(user.authorized_minerals)}")
    print(f"     Access expires: {user.access_expires.strftime('%Y-%m-%d')}")
    
    # Test access to defense-critical data
    print("\n🔐 Testing Access Control:")
    
    # Create test data
    test_data = MineralData(
        mineral_id="test_re_001",
        mineral_name="rare_earth",
        data_type="production",
        classification=ClassificationLevel.CUI,
        export_control=ExportControlCategory.ITAR_XIV,
        data={"production": 100000, "location": "Mountain Pass, CA"},
        source="DOD",
        collection_date=datetime.date(2025, 3, 1),
        classification_reason="Defense-critical"
    )
    
    system.data_store["test_re_001"] = test_data
    
    # Attempt access
    result = system.access_mineral_data("test_user_001", "test_re_001")
    
    if result:
        print(f"  ✅ ACCESS GRANTED")
        print(f"     Classification: {result['classification_notice']}")
        print(f"     Export Control: {result['export_control_notice']}")
    else:
        print("  ❌ ACCESS DENIED")
    
    # Test with unauthorized user
    print("\n🚫 Testing Unauthorized Access:")
    
    unauthorized_user = system.register_user(
        user_id="unauth_user",
        clearance_level=ClassificationLevel.RESTRICTED,
        is_us_person=False,
        training_complete=False,
        background_check=None,
        authorized_minerals=["copper"]  # Not authorized for rare earth
    )
    
    result = system.access_mineral_data("unauth_user", "test_re_001")
    
    if result:
        print("  ❌ ACCESS GRANTED (Should have been denied)")
    else:
        print("  ✅ ACCESS DENIED (Correct - user not authorized)")
    
    # Generate report
    print("\n📊 Testing Compliance Reporting:")
    report = system.generate_compliance_report()
    
    print(f"  Total users: {report['total_users']}")
    print(f"  Total data items: {report['total_data_items']}")
    print(f"  Access attempts: {report['access_statistics']['total']}")
    print(f"  Granted: {report['access_statistics']['granted']}")
    print(f"  Denied: {report['access_statistics']['denied']}")
    
    print("\n" + "="*50)
    print("✅ ALL TESTS COMPLETED")
    print("="*50)

if __name__ == "__main__":
    test_basic_compliance()
