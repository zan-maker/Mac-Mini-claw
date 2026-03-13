# 🔒 Security Corrections Skill

## 🎯 Purpose
This skill encapsulates the four critical security corrections you provided, ensuring proper API key handling, demo/production separation, auditable changelogs, and deterministic financial calculations.

## 📋 The Four Security Corrections

### 1. API Key Security - Server-Side Storage Only
**Problem:** API keys exposed in client-side code
**Solution:** Store keys server-side in environment variables

```javascript
// ✅ CORRECT: Server-side only
const mistralClient = new MistralClient(process.env.MISTRAL_API_KEY);

// ❌ WRONG: Client-side exposure
const mistralClient = new MistralClient("sk-exposed-key-12345");
```

**Implementation:**
```python
# Secure configuration loader
import os

class SecureConfig:
    @staticmethod
    def get_api_key(service_name):
        """Get API key from environment variables"""
        env_var = f"{service_name.upper()}_API_KEY"
        key = os.getenv(env_var)
        if not key:
            raise ValueError(f"Missing {env_var} environment variable")
        return key

# Usage
api_key = SecureConfig.get_api_key("mistral")
```

### 2. Demo/Production Separation
**Problem:** Demo files accidentally deployed to production
**Solution:** Clear isolation with `.gitignore` exclusions

```html
<!-- demo/demo-index.html -->
<!-- NON-PRODUCTION DEMO ONLY - Do not deploy to production -->
<!DOCTYPE html>
<html lang="en">
<head><title>Demo - Not for Production Use</title></head>
```

**Directory Structure:**
```
/demo/
├── demo-index.html          # Clearly isolated
├── README.md                # Explains this is non-production
└── .gitignore               # Excludes /demo from production artifacts
```

**.gitignore Rules:**
```gitignore
# 🔒 SECURITY: Demo files excluded from production
/demo/
demo-*
*-demo.*
config/.env
config/*_config.json
```

### 3. Auditable Changelog Entries
**Problem:** Vague changelog entries insufficient for auditing
**Solution:** Specific entries with old/new values and reasoning

```markdown
### [2024-03-15] Updated transaction fee parameters
- **Parameter**: `base_transaction_fee_percent`
- **Previous value**: `1.5%`
- **New value**: `1.75%`
- **Reason**: Adjusted to reflect updated payment processor costs per contract renewal
- **Affected flows**: Checkout, subscription renewal
- **Approved by**: Finance team (ticket: FIN-4821)
```

**Template for Financial Changes:**
```markdown
### [YYYY-MM-DD] Brief description
- **Parameter**: `parameter_name`
- **Previous value**: `old_value` (with units)
- **New value**: `new_value` (with units)
- **Reason**: Clear business justification with data/references
- **Affected flows**: List of systems/processes impacted
- **Approved by**: Name/team and ticket/reference number
- **Implementation date**: YYYY-MM-DD
- **Verification date**: YYYY-MM-DD
```

### 4. Deterministic Financial Calculations
**Problem:** LLMs performing financial arithmetic (non-deterministic)
**Solution:** Python handles calculations, LLM handles orchestration only

```python
# ✅ CORRECT: Python function handles all arithmetic
def calculate_payable(spot_price: float, floor: float, ceiling: float, grade_multiplier: float) -> float:
    """Deterministic payable calculation - never delegated to LLM."""
    capped = min(max(spot_price, floor), ceiling)
    return capped * grade_multiplier

# LLM only orchestrates and interprets
result = calculate_payable(spot_price, floor, ceiling, grade_multiplier)
narrative = llm.interpret(result, contract_params)
```

**Implementation Pattern:**
```python
class FinancialCalculations:
    """Deterministic financial calculations - never delegated to LLM"""
    
    @staticmethod
    def calculate_monthly_savings(current_costs, new_costs):
        """Calculate monthly savings (Python-only math)"""
        total_current = sum(current_costs.values())
        total_new = sum(new_costs.values())
        return total_current - total_new

# LLM orchestrates, Python calculates
llm_intent = {'action': 'calculate_savings', 'parameters': {...}}
calculator = FinancialCalculations()
savings = calculator.calculate_monthly_savings(current, new)
# LLM narrates: f"Monthly savings: ${savings:.2f}"
```

## 🛡️ Security Audit Script

**Regular security checks:**
```python
#!/usr/bin/env python3
"""
Security Audit Script
Checks for the four critical security issues
"""

import re
import os
from pathlib import Path

class SecurityAuditor:
    def check_api_key_exposure(self, file_path):
        """Check for hardcoded API keys"""
        patterns = [
            r'sk-[a-zA-Z0-9]{48}',
            r'pk_[a-z]{4}_[a-zA-Z0-9]{24}',
            r'xkeysib-[a-f0-9]{64}',
            r'AIzaSy[A-Za-z0-9_-]{33}'
        ]
        
        with open(file_path, 'r') as f:
            content = f.read()
            
        for pattern in patterns:
            if re.search(pattern, content):
                return False, f"Exposed API key pattern: {pattern}"
        
        return True, "No API keys found"
    
    def check_demo_production_separation(self, file_path):
        """Check for proper demo/production separation"""
        if 'demo' in str(file_path).lower():
            with open(file_path, 'r') as f:
                content = f.read()
                
            if 'NON-PRODUCTION DEMO ONLY' not in content:
                return False, "Demo file missing non-production warning"
        
        return True, "Proper separation"
    
    def check_financial_calculations(self, file_path):
        """Check for LLM-based financial calculations"""
        if file_path.suffix == '.py':
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Look for financial calculations in LLM prompts
            financial_keywords = ['calculate', 'sum', 'total', 'cost', 'price', 'fee']
            llm_patterns = ['llm.', 'openai.', 'anthropic.', 'chatgpt']
            
            for keyword in financial_keywords:
                for pattern in llm_patterns:
                    if keyword in content.lower() and pattern in content.lower():
                        return False, f"Financial calculation '{keyword}' with LLM pattern '{pattern}'"
        
        return True, "No LLM financial calculations"
```

## 🔧 Implementation Checklist

### API Key Security
- [ ] **Never** hardcode API keys in source files
- [ ] Use environment variables (`process.env.API_KEY`)
- [ ] Store `.env` files in `config/` directory
- [ ] Add `.env` to `.gitignore`
- [ ] Use secure configuration loader
- [ ] Rotate keys every 90 days

### Demo/Production Separation
- [ ] Create `/demo/` directory for prototypes
- [ ] Add `<!-- NON-PRODUCTION DEMO ONLY -->` headers
- [ ] Update `.gitignore` to exclude `/demo/`
- [ ] Never use real credentials in demo files
- [ ] Clear README.md explaining demo purpose

### Auditable Changelogs
- [ ] Maintain `CHANGELOG.md` with financial changes
- [ ] Include parameter names and values (old/new)
- [ ] Document reasoning and approvals
- [ ] Track affected systems
- [ ] Include ticket/reference numbers
- [ ] Regular compliance reviews

### Deterministic Financial Calculations
- [ ] **Never** perform arithmetic in LLM prompts
- [ ] Create Python functions for all calculations
- [ ] LLM handles intent parsing only
- [ ] Maintain audit trail for calculations
- [ ] Validate input parameters
- [ ] Unit test all financial functions

## 📁 File Structure

```
skills/security-corrections/
├── SKILL.md                    # This file
├── secure_config_loader.py     # API key management
├── financial_calculations.py   # Deterministic math
├── demo_template.html          # Demo file template
└── changelog_template.md       # Auditable changelog template
```

## 🚨 Emergency Response

### If API Keys Are Exposed:
1. **Immediately** rotate all exposed keys
2. Review git history for accidental commits
3. Update `.gitignore` to prevent future commits
4. Monitor for unauthorized usage
5. Contact service providers

### If Demo Files Deployed:
1. Remove from production immediately
2. Verify no real credentials were exposed
3. Update deployment process to exclude `/demo/`
4. Add pre-deployment checks

### If Financial Calculations Incorrect:
1. Audit all LLM prompts for arithmetic
2. Move calculations to Python functions
3. Validate with unit tests
4. Update documentation

## 📚 Related Skills

- `deep-research` - Evidence-based security research
- `github` - Secure repository management
- `healthcheck` - System security hardening

## 🔗 References

1. **OWASP API Security Top 10** - API key management
2. **NIST Cybersecurity Framework** - Security controls
3. **GDPR/CCPA** - Data protection regulations
4. **PCI DSS** - Financial data security

## 📅 Maintenance Schedule

- **Daily:** Security audit script runs
- **Weekly:** Review changelog entries
- **Monthly:** Rotate API keys
- **Quarterly:** Full security review
- **Annually:** Compliance certification review

---

**Created:** 2026-03-12  
**Last Updated:** 2026-03-12  
**Based on:** Four critical security corrections from user  
**Status:** ✅ Active  
**Priority:** 🔴 Critical  

*This skill must be reviewed and applied to all projects.*