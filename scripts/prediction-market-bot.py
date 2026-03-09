#!/usr/bin/env python3
"""
Enhanced Kalshi Scanner with Prediction Market Bot Formulas
Adds Kelly Criterion, Expected Value, Risk Metrics to existing system
"""

import os
import sys
import json
import numpy as np
from datetime import datetime
from scipy import stats

def load_env_file():
    """Load environment variables"""
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    if line.startswith('export '):
                        line = line[7:]
                    key, value = line.split('=', 1)
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    os.environ[key.strip()] = value.strip()
        return True
    return False

class PredictionMarketBot:
    """Implements prediction market trading formulas"""
    
    def __init__(self, bankroll=1000.0):
        self.bankroll = bankroll
        self.max_drawdown = 0.08  # 8% max drawdown
        self.var_confidence = 0.95  # 95% VaR
        self.min_edge = 0.04  # 4% minimum edge
        
    def calculate_expected_value(self, p_model, p_market):
        """Calculate expected value: EV = p · b − (1 − p)"""
        # b = decimal odds - 1, where decimal odds = 1/p_market
        decimal_odds = 1 / p_market
        b = decimal_odds - 1
        ev = p_model * b - (1 - p_model)
        return ev
    
    def calculate_edge(self, p_model, p_market):
        """Calculate market edge: edge = p_model − p_market"""
        return p_model - p_market
    
    def kelly_criterion(self, p_model, p_market):
        """Kelly Criterion: f* = (p · b − q) / b"""
        decimal_odds = 1 / p_market
        b = decimal_odds - 1
        q = 1 - p_model
        f_star = (p_model * b - q) / b if b > 0 else 0
        return max(0, f_star)  # Cannot bet negative
    
    def fractional_kelly(self, f_star, alpha=0.25):
        """Fractional Kelly: f = α · f*"""
        return alpha * f_star
    
    def calculate_position_size(self, p_model, p_market, alpha=0.25):
        """Calculate optimal position size using fractional Kelly"""
        f_star = self.kelly_criterion(p_model, p_market)
        f_frac = self.fractional_kelly(f_star, alpha)
        position = f_frac * self.bankroll
        return position
    
    def calculate_var(self, returns, confidence=0.95):
        """Value at Risk: VaR = μ − 1.645 · σ (for 95% confidence)"""
        if len(returns) < 2:
            return 0
        mu = np.mean(returns)
        sigma = np.std(returns)
        z_score = stats.norm.ppf(1 - confidence)
        var = mu - z_score * sigma
        return var
    
    def calculate_sharpe(self, returns, risk_free_rate=0.02):
        """Sharpe Ratio: SR = (E[R] − Rf) / σ(R)"""
        if len(returns) < 2:
            return 0
        excess_returns = np.array(returns) - risk_free_rate/252  # Daily
        sharpe = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
        return sharpe
    
    def calculate_mispricing_score(self, p_model, p_market, sigma=0.1):
        """Mispricing Score: δ = (p_model − p_mkt) / σ"""
        return (p_model - p_market) / sigma
    
    def validate_trade(self, p_model, p_market, current_exposure=0, max_exposure=0.1):
        """Validate trade against all risk rules"""
        edge = self.calculate_edge(p_model, p_market)
        ev = self.calculate_expected_value(p_model, p_market)
        position = self.calculate_position_size(p_model, p_market)
        
        # Rule 1: Minimum edge
        rule1 = edge > self.min_edge
        
        # Rule 2: Positive expected value
        rule2 = ev > 0
        
        # Rule 3: Position size within Kelly
        kelly_fraction = self.kelly_criterion(p_model, p_market)
        rule3 = position <= kelly_fraction * self.bankroll
        
        # Rule 4: Exposure limit
        new_exposure = current_exposure + (position / self.bankroll)
        rule4 = new_exposure <= max_exposure
        
        # Rule 5: Minimum confidence (p_model > 0.55)
        rule5 = p_model > 0.55
        
        all_rules = [rule1, rule2, rule3, rule4, rule5]
        passed = all(all_rules)
        
        return {
            "passed": passed,
            "edge": edge,
            "expected_value": ev,
            "position_size": position,
            "kelly_fraction": kelly_fraction,
            "new_exposure": new_exposure,
            "rules": {
                "min_edge": rule1,
                "positive_ev": rule2,
                "kelly_size": rule3,
                "exposure_limit": rule4,
                "min_confidence": rule5
            }
        }

def analyze_kalshi_opportunities():
    """Analyze Kalshi opportunities with prediction market formulas"""
    print("🎯 PREDICTION MARKET BOT - ENHANCED ANALYSIS")
    print("=" * 70)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    # Initialize bot with $1000 bankroll
    bot = PredictionMarketBot(bankroll=1000.0)
    
    # Example opportunities (replace with real Kalshi data)
    opportunities = [
        {
            "market": "WTI >$98 by March 13",
            "p_model": 0.95,  # Our model probability
            "p_market": 0.75,  # Market implied probability (1/1.33)
            "current_price": 117.0,
            "strike": 98.0,
            "multiplier": 1.33
        },
        {
            "market": "Gasoline >$2.75",
            "p_model": 0.75,
            "p_market": 0.50,  # Assuming 2.0x odds
            "current_price": 2.65,
            "strike": 2.75,
            "multiplier": 2.00
        },
        {
            "market": "S&P 500 >5200",
            "p_model": 0.60,
            "p_market": 0.40,  # Assuming 2.5x odds
            "current_price": 5180,
            "strike": 5200,
            "multiplier": 2.50
        }
    ]
    
    print("📊 OPPORTUNITY ANALYSIS WITH PREDICTION MARKET FORMULAS:")
    print("-" * 70)
    
    total_edge = 0
    total_ev = 0
    valid_trades = 0
    
    for i, opp in enumerate(opportunities, 1):
        print(f"\n{i}. {opp['market']}")
        print(f"   📈 Model Probability: {opp['p_model']:.2%}")
        print(f"   📊 Market Probability: {opp['p_market']:.2%}")
        print(f"   🎯 Multiplier: {opp['multiplier']}x")
        
        # Calculate metrics
        edge = bot.calculate_edge(opp['p_model'], opp['p_market'])
        ev = bot.calculate_expected_value(opp['p_model'], opp['p_market'])
        position = bot.calculate_position_size(opp['p_model'], opp['p_market'])
        mispricing = bot.calculate_mispricing_score(opp['p_model'], opp['p_market'])
        
        print(f"   ⚖️  Edge: {edge:.2%}")
        print(f"   💰 Expected Value: {ev:.3f}")
        print(f"   🎯 Position Size: ${position:.2f}")
        print(f"   📊 Mispricing Score: {mispricing:.2f}")
        
        # Validate trade
        validation = bot.validate_trade(opp['p_model'], opp['p_market'])
        
        if validation['passed']:
            print(f"   ✅ TRADE VALID - All rules passed")
            valid_trades += 1
        else:
            print(f"   ❌ TRADE INVALID - Failed rules:")
            for rule_name, rule_passed in validation['rules'].items():
                if not rule_passed:
                    print(f"      - {rule_name}")
        
        total_edge += edge
        total_ev += ev
    
    # Portfolio metrics
    print("\n" + "=" * 70)
    print("📈 PORTFOLIO METRICS:")
    print("-" * 70)
    print(f"• Valid Trades: {valid_trades}/{len(opportunities)}")
    print(f"• Average Edge: {total_edge/len(opportunities):.2%}")
    print(f"• Average Expected Value: {total_ev/len(opportunities):.3f}")
    print(f"• Bankroll: ${bot.bankroll:.2f}")
    print(f"• Max Drawdown Limit: {bot.max_drawdown:.1%}")
    print(f"• VaR Confidence: {bot.var_confidence:.1%}")
    print(f"• Minimum Edge Required: {bot.min_edge:.2%}")
    
    # Simulated returns for Sharpe calculation
    simulated_returns = [0.02, -0.01, 0.03, 0.01, -0.005, 0.015, 0.02, -0.008]
    sharpe = bot.calculate_sharpe(simulated_returns)
    var = bot.calculate_var(simulated_returns)
    
    print(f"• Sharpe Ratio (simulated): {sharpe:.2f}")
    print(f"• VaR 95% (simulated): {var:.2%}")
    
    print("\n" + "=" * 70)
    print("🎯 RECOMMENDED ACTIONS:")
    print("-" * 70)
    
    if valid_trades > 0:
        print(f"✅ Execute {valid_trades} validated trades")
        print("   Use position sizes calculated above")
        print("   Monitor risk metrics daily")
    else:
        print("⚠️  No validated trades found")
        print("   Wait for better opportunities")
        print("   Adjust model probabilities or risk parameters")
    
    # Save analysis
    analysis = {
        "timestamp": datetime.now().isoformat(),
        "bankroll": bot.bankroll,
        "opportunities_analyzed": len(opportunities),
        "valid_trades": valid_trades,
        "average_edge": total_edge/len(opportunities),
        "average_ev": total_ev/len(opportunities),
        "sharpe_ratio": sharpe,
        "var_95": var,
        "opportunities": opportunities
    }
    
    os.makedirs("logs/prediction_bot", exist_ok=True)
    output_file = f"logs/prediction_bot/analysis-{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(output_file, "w") as f:
        json.dump(analysis, f, indent=2)
    
    print(f"\n✅ Analysis saved to: {output_file}")
    print("=" * 70)

if __name__ == "__main__":
    load_env_file()
    analyze_kalshi_opportunities()