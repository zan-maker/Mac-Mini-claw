#!/usr/bin/env python3
"""
DEFENSE & EXPORT CONTROL COMPLIANCE SYSTEM
For mineral supply chain intelligence (ITAR/EAR regulated)
"""

import json
import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import logging

# Configure secure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('defense_audit.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ClassificationLevel(Enum):
    """Data classification levels"""
    PUBLIC = "PUBLIC"
    RESTRICTED = "RESTRICTED"
    CONFIDENTIAL = "CONFIDENTIAL"
    CUI = "CUI"  # Controlled Unclassified Information
    SECRET = "SECRET"
    TOP_SECRET = "TOP_SECRET"

class ExportControlCategory(Enum):
    """Export control categories"""
    EAR99 = "EAR99"  # Generally available
    ITAR_XIV = "ITAR-XIV"  # Auxiliary military equipment
    ITAR_XIII = "ITAR-XIII"  # Materials and miscellaneous articles
    USML = "USML"  # United States Munitions List

@dataclass
class UserClearance:
    """User clearance and authorization"""
    user_id: str
    clearance_level: ClassificationLevel
    is_us_person: bool
    export_training_complete: bool
    background_check_date: Optional[datetime.date]
    authorized_minerals: List[str]  # Specific minerals user can access
    access_granted: datetime.datetime
    access_expires: datetime.datetime
    
    def has_access(self, required_level: ClassificationLevel, mineral: str) -> bool:
        """Check if user has access to specific mineral data"""
        # Check clearance level
        clearance_values = list(ClassificationLevel)
        user_idx = clearance_values.index(self.clearance_level)
        required_idx = clearance_values.index(required_level)
        
        if user_idx < required_idx:
            logger.warning(f"User {self.user_id} clearance insufficient: {self.clearance_level} < {required_level}")
            return False
        
        # Check mineral authorization
        if mineral not in self.authorized_minerals:
            logger.warning(f"User {self.user_id} not authorized for mineral: {mineral}")
            return False
        
        # Check export control for non-US persons
        if not self.is_us_person and required_level in [ClassificationLevel.CONFIDENTIAL, ClassificationLevel.CUI]:
            logger.warning(f"Non-US person {self.user_id} attempting to access export-controlled data")
            return False
        
        # Check training
        if not self.export_training_complete:
            logger.warning(f"User {self.user_id} export control training incomplete")
            return False
        
        # Check access expiration
        if datetime.datetime.now() > self.access_expires:
            logger.warning(f"User {self.user_id} access expired")
            return False
        
        return True

@dataclass
class MineralData:
    """Mineral intelligence data with classification"""
    mineral_id: str
    mineral_name: str
    data_type: str  # production, reserves, supply_chain, market_data
    classification: ClassificationLevel
    export_control: ExportControlCategory
    data: Dict
    source: str
    collection_date: datetime.date
    classification_reason: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        result = asdict(self)
        result['classification'] = self.classification.value
        result['export_control'] = self.export_control.value
        result['collection_date'] = self.collection_date.isoformat()
        return result

class DefenseComplianceSystem:
    """Main compliance system for defense-relevant mineral intelligence"""
    
    # Defense-critical minerals (ITAR relevant)
    DEFENSE_CRITICAL_MINERALS = {
        'rare_earth': {
            'classification': ClassificationLevel.CUI,
            'export_control': ExportControlCategory.ITAR_XIV,
            'defense_uses': ['magnets', 'lasers', 'guidance_systems', 'radar']
        },
        'lithium': {
            'classification': ClassificationLevel.CONFIDENTIAL,
            'export_control': ExportControlCategory.EAR99,
            'defense_uses': ['batteries', 'military_electronics', 'submarines']
        },
        'cobalt': {
            'classification': ClassificationLevel.CUI,
            'export_control': ExportControlCategory.ITAR_XIV,
            'defense_uses': ['jet_engines', 'superalloys', 'armor']
        },
        'tungsten': {
            'classification': ClassificationLevel.CUI,
            'export_control': ExportControlCategory.ITAR_XIII,
            'defense_uses': ['armor_piercing', 'munitions', 'tank_armor']
        },
        'tantalum': {
            'classification': ClassificationLevel.CONFIDENTIAL,
            'export_control': ExportControlCategory.ITAR_XIV,
            'defense_uses': ['electronics', 'capacitors', 'weapon_systems']
        },
        'graphite': {
            'classification': ClassificationLevel.SECRET,
            'export_control': ExportControlCategory.USML,
            'defense_uses': ['nuclear', 'missiles', 'rocket_nozzles']
        },
        'vanadium': {
            'classification': ClassificationLevel.CONFIDENTIAL,
            'export_control': ExportControlCategory.ITAR_XIII,
            'defense_uses': ['steel_alloys', 'military_vehicles', 'armor']
        }
    }
    
    def __init__(self):
        self.users: Dict[str, UserClearance] = {}
        self.access_logs: List[Dict] = []
        self.data_store: Dict[str, MineralData] = {}
        
    def classify_mineral_data(self, mineral_type: str, data_type: str, 
                             source: str) -> Tuple[ClassificationLevel, ExportControlCategory]:
        """
        Classify mineral data based on type and sensitivity
        
        Args:
            mineral_type: Type of mineral (e.g., 'rare_earth', 'lithium')
            data_type: Type of data (production, reserves, supply_chain, market_data)
            source: Data source (open_source, government, industry)
            
        Returns:
            (classification_level, export_control_category)
        """
        # Check if mineral is defense-critical
        if mineral_type in self.DEFENSE_CRITICAL_MINERALS:
            mineral_info = self.DEFENSE_CRITICAL_MINERALS[mineral_type]
            
            # Higher classification for sensitive data types
            if data_type in ['production', 'reserves', 'supply_chain']:
                return mineral_info['classification'], mineral_info['export_control']
            elif data_type == 'market_data':
                # Market data might be less sensitive
                if mineral_info['classification'] == ClassificationLevel.CUI:
                    return ClassificationLevel.CONFIDENTIAL, mineral_info['export_control']
                else:
                    return mineral_info['classification'], mineral_info['export_control']
        
        # Non-critical minerals
        if data_type == 'production' and source != 'open_source':
            return ClassificationLevel.RESTRICTED, ExportControlCategory.EAR99
        
        return ClassificationLevel.PUBLIC, ExportControlCategory.EAR99
    
    def register_user(self, user_id: str, clearance_level: ClassificationLevel,
                     is_us_person: bool, training_complete: bool,
                     background_check: Optional[datetime.date],
                     authorized_minerals: List[str]) -> UserClearance:
        """Register a new user with clearance"""
        
        user = UserClearance(
            user_id=user_id,
            clearance_level=clearance_level,
            is_us_person=is_us_person,
            export_training_complete=training_complete,
            background_check_date=background_check,
            authorized_minerals=authorized_minerals,
            access_granted=datetime.datetime.now(),
            access_expires=datetime.datetime.now() + datetime.timedelta(days=90)  # 90-day expiration
        )
        
        self.users[user_id] = user
        logger.info(f"User registered: {user_id} with clearance {clearance_level}")
        
        return user
    
    def access_mineral_data(self, user_id: str, mineral_id: str) -> Optional[Dict]:
        """Attempt to access mineral data with compliance checks"""
        
        # Check user exists
        if user_id not in self.users:
            logger.warning(f"Unknown user attempted access: {user_id}")
            return None
        
        user = self.users[user_id]
        
        # Check data exists
        if mineral_id not in self.data_store:
            logger.warning(f"Unknown mineral data requested: {mineral_id}")
            return None
        
        data = self.data_store[mineral_id]
        
        # Check access permissions
        if not user.has_access(data.classification, data.mineral_name):
            logger.warning(f"Access denied for user {user_id} to mineral {mineral_id}")
            self.log_access_attempt(user_id, mineral_id, data.classification, 'DENIED')
            return None
        
        # Log successful access
        self.log_access_attempt(user_id, mineral_id, data.classification, 'GRANTED')
        
        # Return data (in real system, might redact based on clearance)
        return self.prepare_data_for_user(data, user)
    
    def prepare_data_for_user(self, data: MineralData, user: UserClearance) -> Dict:
        """Prepare data for user based on their clearance level"""
        
        result = data.to_dict()
        
        # Redact sensitive information based on clearance
        if user.clearance_level == ClassificationLevel.RESTRICTED:
            # Redact detailed numbers for RESTRICTED clearance
            if 'production_volume' in result['data']:
                result['data']['production_volume'] = 'CLASSIFIED'
            if 'reserve_estimates' in result['data']:
                result['data']['reserve_estimates'] = 'CLASSIFIED'
        
        elif user.clearance_level == ClassificationLevel.CONFIDENTIAL:
            # Show numbers but not sources for CONFIDENTIAL
            if 'source_details' in result['data']:
                result['data']['source_details'] = 'CLASSIFIED'
        
        # Add classification markings
        result['classification_notice'] = self.generate_classification_notice(data.classification)
        result['export_control_notice'] = self.generate_export_control_notice(data.export_control)
        
        return result
    
    def log_access_attempt(self, user_id: str, mineral_id: str,
                          classification: ClassificationLevel,
                          outcome: str) -> None:
        """Log all access attempts for audit trail"""
        
        log_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'user_id': user_id,
            'mineral_id': mineral_id,
            'classification': classification.value,
            'outcome': outcome,
            'ip_address': '127.0.0.1',  # In real system, get from request
            'user_agent': 'Python-Compliance-System'
        }
        
        self.access_logs.append(log_entry)
        
        # Also write to secure audit log
        with open('defense_access_audit.jsonl', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        logger.info(f"Access {outcome}: {user_id} -> {mineral_id} ({classification.value})")
    
    def generate_classification_notice(self, classification: ClassificationLevel) -> str:
        """Generate classification notice for data"""
        notices = {
            ClassificationLevel.PUBLIC: "UNCLASSIFIED",
            ClassificationLevel.RESTRICTED: "RESTRICTED - Internal Use Only",
            ClassificationLevel.CONFIDENTIAL: "CONFIDENTIAL - Authorized Personnel Only",
            ClassificationLevel.CUI: "CUI//SP-CTI - Controlled Unclassified Information",
            ClassificationLevel.SECRET: "SECRET",
            ClassificationLevel.TOP_SECRET: "TOP SECRET"
        }
        return notices.get(classification, "UNCLASSIFIED")
    
    def generate_export_control_notice(self, export_control: ExportControlCategory) -> str:
        """Generate export control notice"""
        notices = {
            ExportControlCategory.EAR99: "EAR99 - Generally available technology",
            ExportControlCategory.ITAR_XIV: "ITAR Category XIV - Auxiliary military equipment",
            ExportControlCategory.ITAR_XIII: "ITAR Category XIII - Materials and miscellaneous articles",
            ExportControlCategory.USML: "USML - United States Munitions List"
        }
        return notices.get(export_control, "Export control status unknown")
    
    def generate_compliance_report(self) -> Dict:
        """Generate compliance report for auditing"""
        total_accesses = len(self.access_logs)
        granted = sum(1 for log in self.access_logs if log['outcome'] == 'GRANTED')
        denied = sum(1 for log in self.access_logs if log['outcome'] == 'DENIED')
        
        # Count accesses by classification
        by_classification = {}
        for log in self.access_logs:
            cls = log['classification']
            by_classification[cls] = by_classification.get(cls, 0) + 1
        
        return {
            'report_date': datetime.datetime.now().isoformat(),
            'total_users': len(self.users),
            'total_data_items': len(self.data_store),
            'access_statistics': {
                'total': total_accesses,
                'granted': granted,
                'denied': denied,
                'grant_rate': (granted / total_accesses * 100) if total_accesses > 0 else 0
            },
            'access_by_classification': by_classification,
            'users_needing_renewal': [
                user_id for user_id, user in self.users.items()
                if datetime.datetime.now() > user.access_expires
            ],
            'export_control_compliance': 'COMPLIANT' if all(
                user.export_training_complete for user in self.users.values()
            ) else 'NON-COMPLIANT'
        }

# Example usage
def demo_compliance_system():
    """Demonstrate the compliance system"""
    print("🛡️ DEFENSE COMPLIANCE SYSTEM DEMONSTRATION")
    print("="*50)
    
    system = DefenseComplianceSystem()
    
    # Register users with different clearances
    print("\n👥 REGISTERING USERS:")
    
    # US Person with CUI clearance
    us_user = system.register_user(
        user_id="user001",
        clearance_level=ClassificationLevel.CUI,
        is_us_person=True,
        training_complete=True,
        background_check=datetime.date(2025, 1, 15),
        authorized_minerals=["rare_earth", "lithium", "cobalt"]
    )
    print(f"  ✅ US User registered: {us_user.user_id} ({us_user.clearance_level.value})")
    
    # Non-US Person with RESTRICTED clearance
    non_us_user = system.register_user(
        user_id="user002",
        clearance_level=ClassificationLevel.RESTRICTED,
        is_us_person=False,
        training_complete=True,
        background_check=None,
        authorized_minerals=["lithium"]  # Only non-sensitive minerals
    )
    print(f"  ✅ Non-US User registered: {non_us_user.user_id} ({non_us_user.clearance_level.value})")
    
    # Create some mineral data
    print("\n🗺️ CREATING MINERAL DATA:")
    
    # Rare earth data (CUI/ITAR)
    rare_earth_data = MineralData(
        mineral_id="re001",
        mineral_name="rare_earth",
        data_type="production",
        classification=ClassificationLevel.CUI,
        export_control=ExportControlCategory.ITAR_XIV,
        data={
            "production_volume": 150000,  # metric tons
            "primary_producer": "China",
            "reserve_estimates": 44000000,
            "defense_applications": ["F-35 magnets", "JDAM guidance systems"]
        },
        source="DOD intelligence",
        collection_date=datetime.date(2025, 3, 1),
        classification_reason="Defense-critical mineral with ITAR implications"
    )
    system.data_store["re001"] = rare_earth_data
    print(f"  ✅ Rare Earth data created: {rare_earth_data.classification.value}/{rare_earth_data.export_control.value}")
    
    # Lithium data (CONFIDENTIAL/EAR99)
    lithium_data = MineralData(
        mineral_id="li001",
        mineral_name="lithium",
        data_type="market_data",
        classification=ClassificationLevel.CONFIDENTIAL,
        export_control=ExportControlCategory.EAR99,
        data={
            "price_per_ton": 18500,
            "market_trend": "increasing",
            "primary_producers": ["Chile", "Australia", "China"],
            "battery_demand_growth": "25% YoY"
        },
        source="Industry reports",
        collection_date=datetime.date(2025, 2, 28),
        classification_reason="Market data with defense implications"
    )
    system.data_store["li001"] = lithium_data
    print(f"  ✅ Lithium data created: {lithium_data.classification.value}/{lithium_data.export_control.value}")
    
    # Test access attempts
    print("\n🔐 TESTING ACCESS CONTROLS:")
    
    # US user accessing rare earth (should succeed)
    print("\n1. US User accessing Rare Earth (CUI data):")
    result = system.access_mineral_data("user001", "re001")
    if result:
        print(f"  ✅ ACCESS GRANTED")
        print(f"  Classification: {result['classification_notice']}")
        print(f"  Export Control: {result['export_control_notice']}")
        print(f"  Data preview: {json.dumps(result['data'], indent=2)[:200]}...")
    else:
        print("  ❌ ACCESS DENIED")
    
    # Non-US user accessing rare earth (should fail)
    print("\n2. Non-US User accessing Rare Earth (CUI data):")
    result = system.access_mineral_data("user002", "re001")
    if result:
        print(f"  ✅ ACCESS GRANTED")
    else:
        print("  ❌ ACCESS DENIED (Expected - non-US person cannot access ITAR data)")
    
    # Non-US user accessing lithium (should succeed with redaction)
    print("\n3. Non-US User accessing Lithium (CONFIDENTIAL data):")
    result = system.access_mineral_data("user002", "li001")
    if result:
        print(f"  ✅ ACCESS GRANTED")
        print(f"  Classification: {result['classification_notice']}")
        print(f"  Data preview: {json.dumps(result['data'], indent=2)}")
    else:
        print("  ❌ ACCESS DENIED")
    
    # Generate compliance report
    print("\n📊 COMPLIANCE REPORT:")
    report = system.generate_compliance_report()
    print(f"  Total users: {report['total_users']}")
    print(f"  Total data items: {report['total_data_items']}")
    print(f"  Access attempts: {report['access_statistics']['total']}")
    print(f"  Granted: {report['access_statistics']['granted']}")
    print(f"  Denied: {report['access_statistics']['denied']}")
    print(f"  Grant rate: {report['access_statistics']['grant_rate']:.1f}%")
    print(f"  Export control compliance: {report['export_control_compliance']}")
    
    print("\n" + "="*50)
    print("✅ COMPLIANCE SYSTEM READY")
    print("="*50)
    print("\n🎯 KEY FEATURES IMPLEMENTED:")
    print("   1. Data classification (PUBLIC → TOP SECRET)")
    print("   2. Export control enforcement (ITAR/EAR)")
    print("   3. User clearance management")
    print("   4. Audit logging for all access")
    print("   5. Automatic data redaction based on clearance")
    print("   6. Compliance reporting")
    
    return system

if __name__ == "__main__":
    demo_compliance_system()
