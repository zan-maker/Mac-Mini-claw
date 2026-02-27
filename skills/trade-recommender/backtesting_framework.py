#!/usr/bin/env python3
"""
Options Backtesting Framework
Test trading strategies against historical data from Twelve Data API
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from twelve_data_client import TwelveDataClient

class BacktestEngine:
    """Backtesting engine for options strategies"""
    
    def __init__(self, initial_capital: float = 10000):
        self.client = TwelveDataClient()
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.trades = []
        self.equity_curve = []
        
    def get_historical_data(self, symbol: str, days: int = 252) -> List[Dict]:
        """Get historical price data"""
        return self.client.get_time_series(symbol, "1day", days)
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate RSI indicator"""
        if len(prices) < period + 1:
            return 50  # Neutral
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_sma(self, prices: List[float], period: int) -> float:
        """Calculate Simple Moving Average"""
        if len(prices) < period:
            return prices[-1]
        return sum(prices[-period:]) / period
    
    def calculate_macd(self, prices: List[float]) -> Tuple[float, float, float]:
        """Calculate MACD indicator"""
        if len(prices) < 26:
            return 0, 0, 0
        
        # EMA calculation helper
        def ema(data, period):
            multiplier = 2 / (period + 1)
            ema_val = sum(data[:period]) / period
            for price in data[period:]:
                ema_val = (price - ema_val) * multiplier + ema_val
            return ema_val
        
        ema_12 = ema(prices, 12)
        ema_26 = ema(prices, 26)
        macd_line = ema_12 - ema_26
        
        # Signal line (9-period EMA of MACD)
        signal_line = macd_line  # Simplified
        
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram
    
    def generate_signals(self, prices: List[float]) -> Dict:
        """Generate trading signals based on technical indicators"""
        rsi = self.calculate_rsi(prices)
        sma_50 = self.calculate_sma(prices, 50)
        sma_200 = self.calculate_sma(prices, 200)
        macd, signal, histogram = self.calculate_macd(prices)
        
        current_price = prices[-1]
        
        # Determine trend
        if current_price > sma_50 > sma_200:
            trend = "bullish"
        elif current_price < sma_50 < sma_200:
            trend = "bearish"
        else:
            trend = "neutral"
        
        # Generate signal
        signal_score = 0
        
        # RSI signal
        if rsi < 30:
            signal_score += 25  # Oversold, bullish
        elif rsi > 70:
            signal_score -= 25  # Overbought, bearish
        
        # SMA signal
        if trend == "bullish":
            signal_score += 25
        elif trend == "bearish":
            signal_score -= 25
        
        # MACD signal
        if histogram > 0:
            signal_score += 25
        else:
            signal_score -= 25
        
        return {
            "rsi": rsi,
            "sma_50": sma_50,
            "sma_200": sma_200,
            "macd": macd,
            "signal": signal,
            "histogram": histogram,
            "trend": trend,
            "score": signal_score,
            "recommendation": "buy" if signal_score >= 50 else "sell" if signal_score <= -50 else "hold"
        }
    
    def simulate_option_trade(self, entry_price: float, exit_price: float, 
                             option_type: str, premium: float, 
                             contracts: int = 1) -> Dict:
        """Simulate an option trade"""
        
        if option_type == "call":
            # Long call: profit if price goes up
            intrinsic_value = max(0, exit_price - entry_price)
        else:
            # Long put: profit if price goes down
            intrinsic_value = max(0, entry_price - exit_price)
        
        pnl = (intrinsic_value - premium) * 100 * contracts
        roi = (pnl / (premium * 100 * contracts)) * 100 if premium > 0 else 0
        
        return {
            "entry_price": entry_price,
            "exit_price": exit_price,
            "option_type": option_type,
            "premium": premium,
            "contracts": contracts,
            "pnl": pnl,
            "roi": roi
        }
    
    def run_backtest(self, symbol: str, strategy: str = "rsi_reversal",
                     days: int = 252, position_size: float = 0.02) -> Dict:
        """Run backtest on a symbol"""
        
        print(f"\n{'='*60}")
        print(f"BACKTEST: {symbol} | Strategy: {strategy}")
        print(f"{'='*60}\n")
        
        # Get historical data
        data = self.get_historical_data(symbol, days)
        if not data:
            print("Failed to get historical data")
            return {}
        
        prices = [float(d['close']) for d in reversed(data)]
        dates = [d['datetime'] for d in reversed(data)]
        
        # Trading parameters
        trade_size = self.capital * position_size
        winning_trades = 0
        losing_trades = 0
        total_pnl = 0
        
        # Run simulation
        for i in range(200, len(prices) - 5):  # Need 200 days for SMA200
            window = prices[:i+1]
            signals = self.generate_signals(window)
            current_price = prices[i]
            
            # Entry logic based on strategy
            should_trade = False
            option_type = None
            
            if strategy == "rsi_reversal":
                if signals['rsi'] < 30:
                    should_trade = True
                    option_type = "call"  # Buy calls when oversold
                elif signals['rsi'] > 70:
                    should_trade = True
                    option_type = "put"   # Buy puts when overbought
            
            elif strategy == "trend_following":
                if signals['score'] >= 50:
                    should_trade = True
                    option_type = "call"
                elif signals['score'] <= -50:
                    should_trade = True
                    option_type = "put"
            
            # Execute trade
            if should_trade:
                # Simulate 5-day hold
                exit_price = prices[i + 5] if i + 5 < len(prices) else prices[-1]
                
                # Estimate option premium (simplified: 2% of stock price)
                premium = current_price * 0.02
                contracts = int(trade_size / (premium * 100))
                
                if contracts > 0:
                    trade = self.simulate_option_trade(
                        current_price, exit_price, option_type, premium, contracts
                    )
                    
                    trade['date'] = dates[i]
                    trade['signals'] = signals
                    self.trades.append(trade)
                    
                    self.capital += trade['pnl']
                    total_pnl += trade['pnl']
                    
                    if trade['pnl'] > 0:
                        winning_trades += 1
                    else:
                        losing_trades += 1
                    
                    self.equity_curve.append({
                        'date': dates[i],
                        'equity': self.capital
                    })
        
        # Calculate metrics
        total_trades = winning_trades + losing_trades
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        avg_win = sum([t['pnl'] for t in self.trades if t['pnl'] > 0]) / winning_trades if winning_trades > 0 else 0
        avg_loss = sum([t['pnl'] for t in self.trades if t['pnl'] < 0]) / losing_trades if losing_trades > 0 else 0
        
        results = {
            "symbol": symbol,
            "strategy": strategy,
            "initial_capital": self.initial_capital,
            "final_capital": self.capital,
            "total_return": ((self.capital - self.initial_capital) / self.initial_capital) * 100,
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": win_rate,
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "profit_factor": abs(avg_win / avg_loss) if avg_loss != 0 else 0,
            "trades": self.trades,
            "equity_curve": self.equity_curve
        }
        
        # Print results
        print(f"Initial Capital: ${self.initial_capital:,.2f}")
        print(f"Final Capital: ${self.capital:,.2f}")
        print(f"Total Return: {results['total_return']:.2f}%")
        print(f"\nTotal Trades: {total_trades}")
        print(f"Win Rate: {win_rate:.1f}%")
        print(f"Average Win: ${avg_win:,.2f}")
        print(f"Average Loss: ${avg_loss:,.2f}")
        print(f"Profit Factor: {results['profit_factor']:.2f}")
        print(f"\n{'='*60}\n")
        
        return results

def main():
    """Run backtest on major symbols"""
    
    print("="*60)
    print("OPTIONS BACKTESTING FRAMEWORK")
    print("="*60)
    
    engine = BacktestEngine(initial_capital=10000)
    
    # Test strategies
    symbols = ["SPY", "QQQ"]
    strategies = ["rsi_reversal", "trend_following"]
    
    all_results = []
    
    for symbol in symbols:
        for strategy in strategies:
            engine = BacktestEngine(initial_capital=10000)
            results = engine.run_backtest(symbol, strategy, days=252)
            if results:
                all_results.append(results)
    
    # Save results
    output_dir = os.path.expanduser("~/.openclaw/workspace/trades")
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f"backtest-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json")
    
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    
    print(f"\nResults saved to: {output_file}")
    print("\n" + "="*60)
    print("✅ BACKTEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
