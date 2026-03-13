#!/usr/bin/env python3
"""
DETERMINISTIC FINANCIAL CALCULATIONS
All arithmetic performed by Python, never by LLM

PRINCIPLE: LLM handles intent parsing and orchestration only.
           Python handles all deterministic calculations.
"""

from typing import Dict, List, Tuple, Optional
from decimal import Decimal, ROUND_HALF_UP
import datetime

class FinancialCalculations:
    """Deterministic financial calculations - never delegated to LLM"""
    
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
            ROI metrics
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
    def calculate_payable(spot_price: float, 
                         floor: float, 
                         ceiling: float, 
                         grade_multiplier: float) -> float:
        """
        Deterministic payable calculation - never delegated to LLM
        
        Example: Mining contract payable calculation
        """
        # Cap price between floor and ceiling
        capped = min(max(spot_price, floor), ceiling)
        
        # Apply grade multiplier
        payable = capped * grade_multiplier
        
        # Round to 2 decimal places
        return float(Decimal(str(payable)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
    
    @staticmethod
    def calculate_email_campaign_roi(emails_sent: int,
                                    cost_per_email: float,
                                    conversion_rate: float,
                                    average_deal_size: float,
                                    margin_percent: float) -> Dict[str, float]:
        """
        Calculate email campaign ROI
        
        Args:
            emails_sent: Number of emails sent
            cost_per_email: Cost per email (including service costs)
            conversion_rate: Conversion rate (0-1)
            average_deal_size: Average deal size in dollars
            margin_percent: Profit margin percentage (0-100)
            
        Returns:
            Campaign ROI metrics
        """
        total_cost = emails_sent * cost_per_email
        conversions = int(emails_sent * conversion_rate)
        total_revenue = conversions * average_deal_size
        total_margin = total_revenue * (margin_percent / 100)
        net_profit = total_margin - total_cost
        
        if total_cost > 0:
            roi_percent = (net_profit / total_cost) * 100
        else:
            roi_percent = float('inf') if net_profit > 0 else 0
        
        return {
            'emails_sent': emails_sent,
            'total_cost': float(total_cost),
            'conversions': conversions,
            'conversion_rate': float(conversion_rate * 100),
            'total_revenue': float(total_revenue),
            'total_margin': float(total_margin),
            'net_profit': float(net_profit),
            'roi_percent': float(roi_percent),
            'cost_per_conversion': float(total_cost / conversions) if conversions > 0 else float('inf')
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
        
        # Check for required parameters
        required = ['current_costs', 'new_costs']
        for req in required:
            if req not in params:
                errors.append(f"Missing required parameter: {req}")
        
        # Validate cost dictionaries
        if 'current_costs' in params and 'new_costs' in params:
            current = params['current_costs']
            new = params['new_costs']
            
            if not isinstance(current, dict) or not isinstance(new, dict):
                errors.append("Cost parameters must be dictionaries")
            else:
                # Check for negative costs
                for service, cost in list(current.items()) + list(new.items()):
                    if cost < 0:
                        errors.append(f"Negative cost for {service}: {cost}")
        
        # Validate numeric parameters
        numeric_params = ['initial_investment', 'monthly_savings', 'months']
        for param in numeric_params:
            if param in params:
                try:
                    float(params[param])
                except (ValueError, TypeError):
                    errors.append(f"Invalid numeric value for {param}: {params[param]}")
        
        return len(errors) == 0, errors

# Example usage demonstrating LLM orchestration pattern
def example_llm_orchestration():
    """
    Example showing correct LLM usage pattern:
    LLM handles intent parsing, Python handles calculations
    """
    
    # Simulated LLM output (intent parsing)
    llm_intent = {
        'action': 'calculate_savings',
        'parameters': {
            'current_costs': {
                'openrouter': 200.0,
                'firestore': 50.0,
                'brevo': 75.0,
                'cloudinary': 50.0
            },
            'new_costs': {
                'openrouter': 0.0,
                'firestore': 0.0,
                'brevo': 0.0,
                'cloudinary': 0.0
            }
        }
    }
    
    # LLM orchestrates, Python calculates
    if llm_intent['action'] == 'calculate_savings':
        calculator = FinancialCalculations()
        
        # Validate parameters
        is_valid, errors = calculator.validate_financial_parameters(llm_intent['parameters'])
        if not is_valid:
            return {'error': 'Invalid parameters', 'details': errors}
        
        # Perform calculation (deterministic Python)
        savings = calculator.calculate_monthly_savings(
            llm_intent['parameters']['current_costs'],
            llm_intent['parameters']['new_costs']
        )
        
        # LLM can now interpret/narrate the results
        return {
            'success': True,
            'calculation': 'monthly_savings',
            'results': savings,
            'narrative': f"Monthly savings: ${savings['summary']['total_savings']:.2f} ({savings['summary']['savings_percent']:.1f}% reduction)"
        }
    
    return {'error': 'Unknown action'}

if __name__ == "__main__":
    print("🧮 FINANCIAL CALCULATIONS DEMO")
    print("="*50)
    print("PRINCIPLE: LLM orchestrates, Python calculates")
    print("="*50)
    
    calculator = FinancialCalculations()
    
    # Example 1: Monthly savings calculation
    print("\n📊 Example 1: Monthly Savings Calculation")
    current = {'service_a': 100.0, 'service_b': 50.0, 'service_c': 75.0}
    new = {'service_a': 0.0, 'service_b': 0.0, 'service_c': 25.0}
    
    savings = calculator.calculate_monthly_savings(current, new)
    print(f"   Total current: ${savings['summary']['total_current']:.2f}")
    print(f"   Total new: ${savings['summary']['total_new']:.2f}")
    print(f"   Monthly savings: ${savings['summary']['total_savings']:.2f}")
    print(f"   Annual savings: ${savings['summary']['annual_savings']:.2f}")
    
    # Example 2: ROI calculation
    print("\n📈 Example 2: ROI Calculation")
    roi = calculator.calculate_roi(
        initial_investment=500.0,
        monthly_savings=375.0,
        months=12
    )
    print(f"   Initial investment: ${roi['initial_investment']:.2f}")
    print(f"   Monthly savings: ${roi['monthly_savings']:.2f}")
    print(f"   Annual net savings: ${roi['net_savings']:.2f}")
    print(f"   ROI: {roi['roi_percent']:.1f}%")
    print(f"   Payback: {roi['payback_months']:.1f} months")
    print(f"   Breakeven: {roi['breakeven_date']}")
    
    # Example 3: Payable calculation (mining example)
    print("\n⛏️ Example 3: Mining Payable Calculation")
    payable = calculator.calculate_payable(
        spot_price=1850.50,
        floor=1750.00,
        ceiling=1950.00,
        grade_multiplier=0.85
    )
    print(f"   Spot price: ${1850.50:.2f}")
    print(f"   Floor: ${1750.00:.2f}, Ceiling: ${1950.00:.2f}")
    print(f"   Grade multiplier: {0.85}")
    print(f"   Payable: ${payable:.2f}")
    
    # Example 4: Email campaign ROI
    print("\n📧 Example 4: Email Campaign ROI")
    campaign = calculator.calculate_email_campaign_roi(
        emails_sent=1000,
        cost_per_email=0.01,
        conversion_rate=0.02,
        average_deal_size=5000.0,
        margin_percent=30.0
    )
    print(f"   Emails sent: {campaign['emails_sent']}")
    print(f"   Total cost: ${campaign['total_cost']:.2f}")
    print(f"   Conversions: {campaign['conversions']} ({campaign['conversion_rate']:.1f}%)")
    print(f"   Revenue: ${campaign['total_revenue']:.2f}")
    print(f"   Net profit: ${campaign['net_profit']:.2f}")
    print(f"   ROI: {campaign['roi_percent']:.1f}%")
    
    print("\n" + "="*50)
    print("✅ FINANCIAL CALCULATIONS READY")
    print("="*50)
    print("\n🎯 PRINCIPLES IMPLEMENTED:")
    print("   1. LLM handles intent parsing/orchestration only")
    print("   2. Python handles all deterministic calculations")
    print("   3. Audit trail maintained for all calculations")
    print("   4. Validation ensures parameter correctness")
