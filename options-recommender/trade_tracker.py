#!/usr/bin/env python3
"""
Trade Tracker & Performance Reporter
Monitors options trades and generates P&L reports
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

# API Keys
ALPACA_KEY = "PKNDK5P66FCRH5P5ILPTVCYE7D"
ALPACA_SECRET = "z1fwAHFV9H8NY26XrZ2sSSxJggc8BwqiU2gPxVsy49V"
ALPACA_ENDPOINT = "https://paper-api.alpaca.markets/v2"
FINNHUB_KEY = "d6bq93hr01qp4li0f2h0d6bq93hr01qp4li0f2hg"

# Storage path
TRADES_FILE = Path("/Users/cubiczan/.openclaw/workspace/options-recommender/trades.json")


@dataclass
class Trade:
    """A single trade record"""
    id: str
    symbol: str
    strategy: str  # 'bull_put', 'bear_call', 'stock', 'option'
    side: str  # 'buy' or 'sell'
    quantity: int
    entry_price: float
    entry_date: str
    strike: Optional[float] = None
    expiration: Optional[str] = None
    status: str = 'open'  # 'open', 'closed', 'expired'
    exit_price: Optional[float] = None
    exit_date: Optional[str] = None
    notes: str = ""


@dataclass
class TradeReport:
    """Performance report for a trade"""
    trade: Trade
    current_price: float
    unrealized_pnl: float
    realized_pnl: float
    pnl_pct: float
    days_held: int
    days_to_expiry: Optional[int]
    status: str
    recommendation: str  # 'hold', 'close', 'roll'


class TradeTracker:
    """Tracks and reports on options trades"""
    
    def __init__(self):
        self.headers = {
            'APCA-API-KEY-ID': ALPACA_KEY,
            'APCA-API-SECRET-KEY': ALPACA_SECRET
        }
        self.finnhub_headers = {'X-Finnhub-Token': FINNHUB_KEY}
        self.trades: List[Trade] = []
        self._load_trades()
    
    def _load_trades(self):
        """Load trades from file"""
        if TRADES_FILE.exists():
            with open(TRADES_FILE, 'r') as f:
                data = json.load(f)
                self.trades = [Trade(**t) for t in data]
    
    def _save_trades(self):
        """Save trades to file"""
        TRADES_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(TRADES_FILE, 'w') as f:
            json.dump([asdict(t) for t in self.trades], f, indent=2)
    
    def add_trade(self, trade: Trade) -> str:
        """Add a new trade"""
        self.trades.append(trade)
        self._save_trades()
        return trade.id
    
    def close_trade(self, trade_id: str, exit_price: float, exit_date: str = None) -> bool:
        """Close a trade"""
        for trade in self.trades:
            if trade.id == trade_id:
                trade.status = 'closed'
                trade.exit_price = exit_price
                trade.exit_date = exit_date or datetime.now().strftime('%Y-%m-%d')
                self._save_trades()
                return True
        return False
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current stock price from Alpaca"""
        url = f"https://data.alpaca.markets/v2/stocks/{symbol}/snapshot"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            data = resp.json()
            trade = data.get('latestTrade', {})
            return trade.get('p')
        return None
    
    def get_option_price(self, symbol: str, strike: float, expiration: str, option_type: str) -> Optional[Dict]:
        """Get current option price (simplified - requires options data subscription)"""
        # In production, this would query the actual options chain
        # For now, return estimated price based on underlying
        underlying_price = self.get_current_price(symbol)
        if not underlying_price:
            return None
        
        # Simplified option pricing
        if option_type == 'put':
            itm = max(0, strike - underlying_price)
        else:
            itm = max(0, underlying_price - strike)
        
        # Return estimated values
        return {
            'bid': max(0.01, itm * 0.8),
            'ask': max(0.02, itm * 0.9 + 0.05),
            'mid': max(0.015, itm * 0.85 + 0.025)
        }
    
    def generate_report(self) -> Dict:
        """Generate comprehensive performance report"""
        now = datetime.now()
        
        report = {
            'generated_at': now.strftime('%Y-%m-%d %H:%M:%S'),
            'summary': {
                'total_trades': len(self.trades),
                'open_trades': len([t for t in self.trades if t.status == 'open']),
                'closed_trades': len([t for t in self.trades if t.status == 'closed']),
                'total_realized_pnl': 0,
                'total_unrealized_pnl': 0
            },
            'open_positions': [],
            'closed_positions': [],
            'recommendations': []
        }
        
        for trade in self.trades:
            current_price = self.get_current_price(trade.symbol) or trade.entry_price
            
            days_held = (now - datetime.strptime(trade.entry_date, '%Y-%m-%d')).days
            
            if trade.status == 'open':
                # Calculate unrealized P&L
                if trade.strategy in ['bull_put', 'bear_call']:
                    # For credit spreads, P&L depends on where price is vs strikes
                    unrealized_pnl = trade.quantity * (trade.entry_price - current_price) * 100
                else:
                    unrealized_pnl = trade.quantity * (current_price - trade.entry_price) * 100
                
                pnl_pct = (current_price - trade.entry_price) / trade.entry_price * 100 if trade.entry_price > 0 else 0
                
                # Days to expiry
                days_to_expiry = None
                if trade.expiration:
                    exp_date = datetime.strptime(trade.expiration, '%Y-%m-%d')
                    days_to_expiry = max(0, (exp_date - now).days)
                
                # Generate recommendation
                recommendation = self._generate_recommendation(trade, current_price, days_held, days_to_expiry)
                
                position_report = {
                    'id': trade.id,
                    'symbol': trade.symbol,
                    'strategy': trade.strategy,
                    'entry_price': trade.entry_price,
                    'current_price': current_price,
                    'quantity': trade.quantity,
                    'unrealized_pnl': unrealized_pnl,
                    'pnl_pct': pnl_pct,
                    'days_held': days_held,
                    'days_to_expiry': days_to_expiry,
                    'recommendation': recommendation
                }
                
                report['open_positions'].append(position_report)
                report['summary']['total_unrealized_pnl'] += unrealized_pnl
                
            else:  # Closed
                realized_pnl = 0
                if trade.exit_price:
                    if trade.side == 'buy':
                        realized_pnl = trade.quantity * (trade.exit_price - trade.entry_price) * 100
                    else:
                        realized_pnl = trade.quantity * (trade.entry_price - trade.exit_price) * 100
                
                pnl_pct = (trade.exit_price - trade.entry_price) / trade.entry_price * 100 if trade.entry_price > 0 else 0
                
                position_report = {
                    'id': trade.id,
                    'symbol': trade.symbol,
                    'strategy': trade.strategy,
                    'entry_price': trade.entry_price,
                    'exit_price': trade.exit_price,
                    'quantity': trade.quantity,
                    'realized_pnl': realized_pnl,
                    'pnl_pct': pnl_pct,
                    'days_held': days_held,
                    'exit_date': trade.exit_date
                }
                
                report['closed_positions'].append(position_report)
                report['summary']['total_realized_pnl'] += realized_pnl
        
        return report
    
    def _generate_recommendation(self, trade: Trade, current_price: float, 
                                  days_held: int, days_to_expiry: Optional[int]) -> str:
        """Generate hold/close/roll recommendation"""
        
        # Calculate how far ITM/OTM we are
        if trade.strategy == 'bull_put':
            # Want price > strike
            if trade.strike:
                buffer = (current_price - trade.strike) / trade.strike * 100
                if buffer > 10:
                    return "HOLD - Position safe, let theta work"
                elif buffer > 5:
                    return "HOLD - Good buffer, monitor closely"
                elif buffer > 0:
                    return "MONITOR - Close to strike, watch for roll"
                else:
                    return "ROLL - Price below strike, consider rolling"
        
        elif trade.strategy == 'bear_call':
            # Want price < strike
            if trade.strike:
                buffer = (trade.strike - current_price) / trade.strike * 100
                if buffer > 10:
                    return "HOLD - Position safe, let theta work"
                elif buffer > 5:
                    return "HOLD - Good buffer, monitor closely"
                elif buffer > 0:
                    return "MONITOR - Close to strike, watch for roll"
                else:
                    return "CLOSE - Price above strike, exit to limit loss"
        
        # Time-based recommendations
        if days_to_expiry is not None:
            if days_to_expiry <= 2:
                return "EXPIRY IMMINENT - Close or let expire"
            elif days_to_expiry <= 7:
                return "FINAL WEEK - Consider closing if profitable"
        
        return "HOLD - No action needed"
    
    def format_report(self, report: Dict) -> str:
        """Format report as readable text"""
        lines = []
        
        lines.append("=" * 70)
        lines.append("📊 TRADE PERFORMANCE REPORT")
        lines.append(f"Generated: {report['generated_at']}")
        lines.append("=" * 70)
        
        # Summary
        s = report['summary']
        lines.append("")
        lines.append("📋 SUMMARY")
        lines.append("-" * 40)
        lines.append(f"Total Trades:     {s['total_trades']}")
        lines.append(f"Open Positions:   {s['open_trades']}")
        lines.append(f"Closed Positions: {s['closed_trades']}")
        lines.append(f"Realized P&L:     ${s['total_realized_pnl']:+.2f}")
        lines.append(f"Unrealized P&L:   ${s['total_unrealized_pnl']:+.2f}")
        
        # Open positions
        if report['open_positions']:
            lines.append("")
            lines.append("📈 OPEN POSITIONS")
            lines.append("-" * 70)
            lines.append(f"{'Symbol':<8} {'Strategy':<12} {'Entry':<10} {'Current':<10} {'P&L':<12} {'Action'}")
            lines.append("-" * 70)
            
            for pos in report['open_positions']:
                pnl = f"${pos['unrealized_pnl']:+.2f} ({pos['pnl_pct']:+.1f}%)"
                action = pos['recommendation'].split('-')[0].strip()
                lines.append(f"{pos['symbol']:<8} {pos['strategy']:<12} ${pos['entry_price']:<9.2f} ${pos['current_price']:<9.2f} {pnl:<12} {action}")
        
        # Closed positions
        if report['closed_positions']:
            lines.append("")
            lines.append("📜 CLOSED POSITIONS")
            lines.append("-" * 70)
            lines.append(f"{'Symbol':<8} {'Strategy':<12} {'Entry':<10} {'Exit':<10} {'P&L':<12}")
            lines.append("-" * 70)
            
            for pos in report['closed_positions']:
                pnl = f"${pos['realized_pnl']:+.2f} ({pos['pnl_pct']:+.1f}%)"
                lines.append(f"{pos['symbol']:<8} {pos['strategy']:<12} ${pos['entry_price']:<9.2f} ${pos['exit_price']:<9.2f} {pnl}")
        
        # Recommendations
        if report['open_positions']:
            lines.append("")
            lines.append("💡 RECOMMENDATIONS")
            lines.append("-" * 70)
            
            for pos in report['open_positions']:
                lines.append(f"\n{pos['symbol']}: {pos['recommendation']}")
        
        lines.append("")
        lines.append("=" * 70)
        
        return "\n".join(lines)


def main():
    """Main entry point"""
    tracker = TradeTracker()
    
    # Add sample trades if none exist
    if not tracker.trades:
        print("Adding sample trades...")
        
        sample_trades = [
            Trade(
                id="AAPL-20260219-001",
                symbol="AAPL",
                strategy="bull_put",
                side="sell",
                quantity=2,
                entry_price=0.40,
                entry_date="2026-02-19",
                strike=180.0,
                expiration="2026-03-07",
                notes="Bull put spread, 180/175 strikes"
            ),
            Trade(
                id="MSFT-20260219-002",
                symbol="MSFT",
                strategy="bear_call",
                side="sell",
                quantity=1,
                entry_price=0.35,
                entry_date="2026-02-19",
                strike=420.0,
                expiration="2026-03-14",
                notes="Bear call spread, 420/425 strikes"
            )
        ]
        
        for trade in sample_trades:
            tracker.add_trade(trade)
    
    # Generate and print report
    report = tracker.generate_report()
    formatted = tracker.format_report(report)
    print(formatted)
    
    # Save report
    report_file = Path("/Users/cubiczan/.openclaw/workspace/options-recommender/latest_report.txt")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, 'w') as f:
        f.write(formatted)
    
    print(f"\n📁 Report saved to: {report_file}")
    
    return formatted


if __name__ == "__main__":
    main()
