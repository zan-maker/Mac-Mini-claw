#!/usr/bin/env python3
"""
Trade Performance Report - Options P&L Calculator
Properly calculates P&L for options credit spreads
"""

import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

TRADES_FILE = Path("/Users/cubiczan/.openclaw/workspace/options-recommender/trades.json")


@dataclass
class CreditSpreadPosition:
    """A credit spread position with proper P&L tracking"""
    id: str
    symbol: str
    strategy: str  # 'bull_put' or 'bear_call'
    quantity: int  # Number of spreads
    short_strike: float
    long_strike: float
    expiration: str
    credit_received: float  # Net credit per spread
    entry_date: str
    current_status: str = 'open'
    
    # Tracking
    current_spread_value: float = 0.0  # Current cost to close
    unrealized_pnl: float = 0.0
    realized_pnl: float = 0.0
    
    def calculate_max_loss(self) -> float:
        """Max loss = (strike width - credit) * quantity * 100"""
        width = abs(self.short_strike - self.long_strike)
        max_loss_per = width - self.credit_received
        return max_loss_per * self.quantity * 100
    
    def calculate_max_profit(self) -> float:
        """Max profit = credit received * quantity * 100"""
        return self.credit_received * self.quantity * 100
    
    def calculate_current_pnl(self, underlying_price: float) -> tuple:
        """
        Calculate current P&L based on underlying price
        
        Returns: (unrealized_pnl, pnl_pct, probability_of_profit)
        """
        # For bull put spread:
        # - Max profit if price > short_strike at expiry
        # - Max loss if price < long_strike at expiry
        # - Partial between strikes
        
        width = abs(self.short_strike - self.long_strike)
        
        if self.strategy == 'bull_put':
            if underlying_price >= self.short_strike:
                # Max profit zone
                self.current_spread_value = 0.0
                self.unrealized_pnl = self.calculate_max_profit()
            elif underlying_price <= self.long_strike:
                # Max loss zone
                self.current_spread_value = width
                self.unrealized_pnl = -self.calculate_max_loss()
            else:
                # Between strikes - estimate based on distance
                # Simplified: assume linear P&L between strikes
                distance = (underlying_price - self.long_strike) / width
                self.unrealized_pnl = self.calculate_max_profit() - (1 - distance) * self.calculate_max_loss()
        
        elif self.strategy == 'bear_call':
            if underlying_price <= self.short_strike:
                # Max profit zone
                self.current_spread_value = 0.0
                self.unrealized_pnl = self.calculate_max_profit()
            elif underlying_price >= self.long_strike:
                # Max loss zone
                self.current_spread_value = width
                self.unrealized_pnl = -self.calculate_max_loss()
            else:
                # Between strikes
                distance = (self.long_strike - underlying_price) / width
                self.unrealized_pnl = self.calculate_max_profit() - (1 - distance) * self.calculate_max_loss()
        
        pnl_pct = (self.unrealized_pnl / self.calculate_max_loss()) * 100 if self.calculate_max_loss() != 0 else 0
        
        return self.unrealized_pnl, pnl_pct


def get_stock_price(symbol: str) -> Optional[float]:
    """Get current stock price using Finnhub"""
    import requests
    
    FINNHUB_KEY = "d6bq93hr01qp4li0f2h0d6bq93hr01qp4li0f2hg"
    
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_KEY}"
    resp = requests.get(url)
    
    if resp.status_code == 200:
        data = resp.json()
        return data.get('c')  # Current price
    
    return None


def generate_performance_report():
    """Generate comprehensive performance report"""
    
    print("=" * 70)
    print("📊 OPTIONS TRADE PERFORMANCE REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Sample positions (in production, load from file)
    positions = [
        CreditSpreadPosition(
            id="AAPL-20260219-001",
            symbol="AAPL",
            strategy="bull_put",
            quantity=2,
            short_strike=180.0,
            long_strike=175.0,
            expiration="2026-03-07",
            credit_received=0.40,
            entry_date="2026-02-19"
        ),
        CreditSpreadPosition(
            id="MSFT-20260219-002",
            symbol="MSFT",
            strategy="bear_call",
            quantity=1,
            short_strike=420.0,
            long_strike=425.0,
            expiration="2026-03-14",
            credit_received=0.35,
            entry_date="2026-02-19"
        ),
        CreditSpreadPosition(
            id="NVDA-20260218-003",
            symbol="NVDA",
            strategy="bull_put",
            quantity=1,
            short_strike=120.0,
            long_strike=115.0,
            expiration="2026-03-21",
            credit_received=0.55,
            entry_date="2026-02-18"
        ),
    ]
    
    # Calculate current prices and P&L
    total_unrealized = 0
    total_max_profit = 0
    total_max_risk = 0
    
    print("\n📈 OPEN POSITIONS")
    print("-" * 70)
    print(f"{'Symbol':<8} {'Strategy':<12} {'Strikes':<15} {'Credit':<8} {'Current':<10} {'P&L':<12} {'Status'}")
    print("-" * 70)
    
    for pos in positions:
        current_price = get_stock_price(pos.symbol)
        
        if current_price:
            pnl, pnl_pct = pos.calculate_current_pnl(current_price)
            total_unrealized += pnl
        else:
            pnl = 0
            pnl_pct = 0
            current_price = 0
        
        total_max_profit += pos.calculate_max_profit()
        total_max_risk += pos.calculate_max_loss()
        
        strikes = f"{pos.short_strike}/{pos.long_strike}"
        credit = f"${pos.credit_received:.2f}"
        
        # Determine status
        if pos.strategy == 'bull_put':
            buffer = ((current_price - pos.short_strike) / pos.short_strike * 100) if current_price > 0 else 0
            status = "✅ SAFE" if buffer > 5 else "⚠️ WATCH" if buffer > 0 else "❌ ITM"
        else:
            buffer = ((pos.short_strike - current_price) / pos.short_strike * 100) if current_price > 0 else 0
            status = "✅ SAFE" if buffer > 5 else "⚠️ WATCH" if buffer > 0 else "❌ ITM"
        
        pnl_str = f"${pnl:+.0f} ({pnl_pct:+.0f}%)"
        price_str = f"${current_price:.2f}" if current_price else "N/A"
        
        print(f"{pos.symbol:<8} {pos.strategy:<12} {strikes:<15} {credit:<8} {price_str:<10} {pnl_str:<12} {status}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📋 PORTFOLIO SUMMARY")
    print("-" * 40)
    
    win_rate = 0
    if len(positions) > 0:
        winning = sum(1 for p in positions if p.unrealized_pnl > 0)
        win_rate = (winning / len(positions)) * 100
    
    print(f"Open Positions:      {len(positions)}")
    print(f"Unrealized P&L:      ${total_unrealized:+.2f}")
    print(f"Max Profit Target:   ${total_max_profit:.2f}")
    print(f"Max Risk:            ${total_max_risk:.2f}")
    print(f"Risk/Reward Ratio:   1:{total_max_profit/total_max_risk:.1f}" if total_max_risk > 0 else "Risk/Reward: N/A")
    print(f"Current Win Rate:    {win_rate:.0f}%")
    
    # Days to expiry
    print("\n📅 EXPIRATION CALENDAR")
    print("-" * 40)
    
    now = datetime.now()
    for pos in sorted(positions, key=lambda x: x.expiration):
        exp_date = datetime.strptime(pos.expiration, '%Y-%m-%d')
        days_left = (exp_date - now).days
        
        print(f"{pos.symbol}: {pos.expiration} ({days_left} days)")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS")
    print("-" * 40)
    
    for pos in positions:
        if pos.strategy == 'bull_put':
            price = get_stock_price(pos.symbol)
            if price:
                if price > pos.short_strike * 1.05:
                    print(f"{pos.symbol}: HOLD - Safe zone, let theta work")
                elif price > pos.short_strike:
                    print(f"{pos.symbol}: MONITOR - Close to short strike")
                else:
                    print(f"{pos.symbol}: Consider ROLL or CLOSE")
    
    print("\n" + "=" * 70)
    
    return {
        'positions': len(positions),
        'unrealized_pnl': total_unrealized,
        'win_rate': win_rate
    }


if __name__ == "__main__":
    generate_performance_report()
