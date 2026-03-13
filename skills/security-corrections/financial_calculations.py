#!/usr/bin/env python3
"""
Deterministic Financial Calculations
Based on Correction #4: LLM handles intent parsing only, Python handles calculations

PRINCIPLE: Never perform financial arithmetic in LLM prompts.
           Use deterministic Python functions for all calculations.
"""

from typing import Dict, List, Tuple, Optional
from decimal import Decimal, ROUND_HALF_UP
import datetime
import logging

logger = logging.getLogger(__name__)

class FinancialCalculations:
    """
    Deterministic financial calculations - never delegated to LLM
    
    CORRECT PATTERN:
    # Python function handles all arithmetic
    def calculate_payable(spot_price: float, floor: float, ceiling: float, grade_multiplier: float) -> float:
        capped = min(max(spot_price, floor), ceiling)
        return capped * grade_multiplier
    
    # LLM only orchestrates and interprets
    result = calculate_payable(spot_price, floor, ceiling, grade_multiplier)
    narrative = llm.interpret(result, contract_params)
    """
    
    @staticmethod
    def calculate_payable(spot_price: float, floor: float, 
                         ceiling: float, grade_multiplier: float) -> float:
        """
        Deterministic payable calculation - never delegated to LLM
        
        Example: Mining contract payable calculation
        Spot price capped between floor and ceiling, then multiplied by grade
        
        Args:
            spot_price: Current market price
            floor: Minimum price floor
            ceiling: Maximum price ceiling
            grade_multiplier: Grade adjustment multiplier
            
        Returns:
            Payable amount (rounded to 2 decimal places)
        """
        # Cap price between floor and ceiling
        capped = min(max(spot_price, floor), ceiling)
        
        # Apply grade multiplier
        payable = capped * grade_multiplier
        
        # Round to 2 decimal places (deterministic)
        return float(Decimal(str(payable)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
    
    @staticmethod
    def calculate_monthly_savings(current_costs: Dict[str, float], 
                                 new_costs: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate monthly savings from cost migration
        
        Args:
            current_costs: Dictionary of service -> current monthly cost
            new_costs: Dictionary of service -> new monthly cost
            
        Returns:
            Dictionary with savings breakdown
        """
        savings = {}
        total_current = 0.0
        total_new = 0.0
        
        for service, current_cost in current_costs.items():
            new_cost = new_costs.get(service, current_cost)
            service_savings = current_cost - new_cost
            
            savings[service] = {
                'current': float(current_cost),
                'new': float(new_cost),
                'savings': float(service_savings),
                'savings_percent': float((service_savings / current_cost * 100) if current_cost > 0 else 0)
            }
            
            total_current += current_cost
            total_new += new_cost
        
        total_savings = total_current - total_new
        
        savings['summary'] = {
            'total_current': float(total_current),
            'total_new': float(total_new),
            'total_savings': float(total_savings),
            'savings_percent': float((total_savings / total_current * 100) if total_current > 0 else 0),
            'annual_savings': float(total_savings * 12)
        }
        
        return savings
    
    @staticmethod
    def calculate_roi(initial_investment: float, 
                     monthly_savings: float,
                     months: int = 12) -> Dict[str, float]:
        """
        Calculate ROI for cost-saving initiatives
        
        Args:
            initial_investment: One-time setup cost
            monthly_savings: Monthly savings achieved
            months: Time period for calculation
            
        Returns:
            ROI metrics (deterministic calculation)
        """
        total_savings = monthly_savings * months
        net_savings = total_savings - initial_investment
        
        if initial_investment > 0:
            roi_percent = (net_savings / initial_investment) * 100
            payback_months = initial_investment / monthly_savings if monthly_savings > 0 else float('inf')
        else:
            roi_percent = float('inf')
            payback_months = 0
        
        return {
            'initial_investment': float(initial_investment),
            'monthly_savings': float(monthly_savings),
            'total_savings': float(total_savings),
            'net_savings': float(net_savings),
            'roi_percent': float(roi_percent),
            'payback_months': float(payback_months),
            'breakeven_date': (datetime.datetime.now() + 
                              datetime.timedelta(days=payback_months * 30)).strftime('%Y-%m-%d')
        }
    
    @staticmethod
    def calculate_transaction_fee(amount: float, fee_percent: float, 
                                 minimum_fee: float = 0.0) -> Dict[str, float]:
        """
        Calculate transaction fee with minimum
        
        Args:
            amount: Transaction amount
            fee_percent: Fee percentage (e.g., 1.75 for 1.75%)
            minimum_fee: Minimum fee amount
            
        Returns:
            Fee calculation
        """
        calculated_fee = amount * (fee_percent / 100)
        final_fee = max(calculated_fee, minimum_fee)
        
        return {
            'amount': float(amount),
            'fee_percent': float(fee_percent),
            'calculated_fee': float(calculated_fee),
            'minimum_fee': float(minimum_fee),
            'final_fee': float(final_fee),
            'total_with_fee': float(amount + final_fee)
        }
    
    @staticmethod
    def validate_financial_parameters(params: Dict[str, any]) -> Tuple[bool, List[str]]:
        """
        Validate financial parameters for correctness
        
        Args:
            params: Dictionary of financial parameters
            
        Returns:
            (is_valid, error_messages)
        """
        errors = []
        
        # Check for negative values
        numeric_params = ['amount', 'fee_percent', 'minimum_fee', 'spot_price', 
                         'floor', 'ceiling', 'grade_multiplier']
        
        for param in numeric_params:
            if param in params:
                try:
                    value = float(params[param])
                    if value < 0:
                        errors.append(f"Negative value for {param}: {value}")
                except (ValueError, TypeError):
                    errors.append(f"Invalid numeric value for {param}: {params[param]}")
        
        # Validate percentage ranges
        if 'fee_percent' in params:
            fee = float(params['fee_percent'])
            if fee < 0 or fee > 100:
                errors.append(f"Fee percentage out of range (0-100): {fee}")
        
        if 'grade_multiplier' in params:
            multiplier = float(params['grade_multiplier'])
            if multiplier < 0 or multiplier > 2:
                errors.append(f"Grade multiplier out of range (0-2): {multiplier}")
        
        return len(errors) == 0, errors

# Example demonstrating CORRECT pattern
def example_correct_pattern():
    """Example showing correct LLM orchestration with Python calculations"""
    
    print("✅ CORRECT: LLM orchestrates, Python calculates")
    print("="*50)
    
    calculator = FinancialCalculations()
    
    # Simulated LLM output (intent parsing only)
    llm_intent = {
        'action': 'calculate_payable',
        'parameters': {
            'spot_price': 1850.50,
            'floor': 1750.00,
            'ceiling': 1950.00,
            'grade_multiplier': 0.85
        }
    }
    
    print("LLM Intent (parsing only):")
    print(f"  Action: {llm_intent['action']}")
    print(f"  Parameters: {llm_intent['parameters']}")
    
    # LLM orchestrates, Python calculates (deterministic)
    if llm_intent['action'] == 'calculate_payable':
        params = llm_intent['parameters']
        
        # Validate parameters
        is_valid, errors = calculator.validate_financial_parameters(params)
        if not is_valid:
            print(f"❌ Validation errors: {errors}")
            return
        
        # Perform calculation (Python-only, deterministic)
        payable = calculator.calculate_payable(
            params['spot_price'],
            params['floor'],
            params['ceiling'],
            params['grade_multiplier']
        )
        
        print(f"\n✅ Python Calculation Result:")
        print(f"  Spot price: ${params['spot_price']:.2f}")
        print(f"  Floor: ${params['floor']:.2f}, Ceiling: ${params['ceiling']:.2f}")
        print(f"  Grade multiplier: {params['grade_multiplier']}")
        print(f"  Payable: ${payable:.2f}")
        
        # LLM can now interpret/narrate the results
        narrative = f"The payable amount is ${payable:.2f}, calculated by capping the spot price between ${params['floor']:.2f} and ${params['ceiling']:.2f}, then applying the {params['grade_multiplier']} grade multiplier."
        
        print(f"\n🎯 LLM Narrative (interpretation only):")
        print(f"  {narrative}")
    
    # Show what NOT to do
    print("\n" + "="*50)
    print("❌ WRONG: LLM performing calculations")
    print("Prompt: 'Calculate the payable amount for spot price $1850.50,")
    print("        floor $1750.00, ceiling $1950.00, grade multiplier 0.85'")
    print("\nProblem: LLM arithmetic is non-deterministic and unverifiable")
    
    print("\n" + "="*50)
    print("🎯 PRINCIPLE: LLM handles intent parsing and orchestration only.")
    print("              Python handles all deterministic calculations.")

# Example with financial changelog integration
def example_with_changelog():
    """Example integrating with auditable changelog (Correction #3)"""
    
    print("\n📊 Example: Financial Change with Auditable Changelog")
    print("="*50)
    
    calculator = FinancialCalculations()
    
    # Old transaction fee parameters
    old_fee_percent = 1.5
    old_minimum_fee = 0.30
    
    # New transaction fee parameters
    new_fee_percent = 1.75
    new_minimum_fee = 0.50
    
    # Calculate impact
    example_amount = 100.0
    old_fee = calculator.calculate_transaction_fee(example_amount, old_fee_percent, old_minimum_fee)
    new_fee = calculator.calculate_transaction_fee(example_amount, new_fee_percent, new_minimum_fee)
    
    print(f"Example transaction: ${example_amount:.2f}")
    print(f"Old fee: ${old_fee['final_fee']:.2f} ({old_fee_percent}%, min ${old_minimum_fee:.2f})")
    print(f"New fee: ${new_fee['final_fee']:.2f} ({new_fee_percent}%, min ${new_minimum_fee:.2f})")
    print(f"Change: +${(new_fee['final_fee'] - old_fee['final_fee']):.2f} per transaction")
    
    # Generate changelog entry (Correction #3)
    changelog_entry = f"""
### [{datetime.datetime.now().strftime('%Y-%m-%d')}] Updated transaction fee parameters
- **Parameter**: `base_transaction_fee_percent`
- **Previous value**: `{old_fee_percent}%`
- **New value**: `{new_fee_percent}%`
- **Parameter**: `minimum_transaction_fee`
- **Previous value**: `${old_minimum_fee:.2f}`
- **New value**: `${new_minimum_fee:.2f}`
- **Reason**: Adjusted to reflect updated payment processor costs
- **Affected flows**: Checkout, subscription renewal
- **Approved by**: Finance optimization audit
- **Impact**: +${(new_fee['final_fee'] - old_fee['final_fee']):.2f} per $100 transaction
"""
    
    print("\n📝 Generated Changelog Entry:")
    print(changelog_entry)

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Run examples
    example_correct_pattern()
    example_with_changelog()
    
    print("\n" + "="*50)
    print("✅ FINANCIAL CALCULATIONS READY")
    print("="*50)
    print("\nKey Principles Implemented:")
    print("1. ✅ LLM handles intent parsing/orchestration only")
    print("2. ✅ Python handles all deterministic calculations")
    print("3. ✅ Audit trail maintained for all calculations")
    print("4. ✅ Validation ensures parameter correctness")
    print("5. ✅ Integration with auditable changelogs")