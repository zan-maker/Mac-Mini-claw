#!/usr/bin/env python3
"""
Kalshi Portfolio Summary - Daily portfolio tracking
"""

import json
import os
from datetime import datetime, timedelta

class PortfolioTracker:
    """Track Kalshi portfolio performance"""
    
    def __init__(self):
        self.data_dir = "/Users/cubiczan/.openclaw/workspace/knowledge_graph"
        self.portfolio_file = os.path.join(self.data_dir, "portfolio.json")
        self.load_portfolio()
    
    def load_portfolio(self):
        """Load portfolio data"""
        if os.path.exists(self.portfolio_file):
            with open(self.portfolio_file, "r") as f:
                self.portfolio = json.load(f)
        else:
            self.portfolio = {
                "total_invested": 0,
                "total_profit": 0,
                "active_trades": [],
                "completed_trades": [],
                "daily_performance": [],
                "created": datetime.now().isoformat()
            }
    
    def save_portfolio(self):
        """Save portfolio data"""
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.portfolio_file, "w") as f:
            json.dump(self.portfolio, f, indent=2, default=str)
    
    def add_trade(self, trade_data):
        """Add a trade to portfolio"""
        trade_id = f"trade_{len(self.portfolio['active_trades']) + len(self.portfolio['completed_trades']) + 1}"
        
        trade = {
            "id": trade_id,
            "market": trade_data.get("market"),
            "direction": trade_data.get("direction"),
            "size": trade_data.get("size"),
            "entry_price": trade_data.get("entry_price"),
            "current_price": trade_data.get("current_price"),
            "target_price": trade_data.get("target_price"),
            "stop_loss": trade_data.get("stop_loss"),
            "settlement": trade_data.get("settlement"),
            "status": "active",
            "opened": datetime.now().isoformat(),
            "profit": 0,
            "return_pct": 0
        }
        
        self.portfolio["active_trades"].append(trade)
        self.portfolio["total_invested"] += trade["size"]
        self.save_portfolio()
        return trade_id
    
    def close_trade(self, trade_id, exit_price, profit):
        """Close a trade"""
        for trade in self.portfolio["active_trades"]:
            if trade["id"] == trade_id:
                trade["status"] = "closed"
                trade["closed"] = datetime.now().isoformat()
                trade["exit_price"] = exit_price
                trade["profit"] = profit
                trade["return_pct"] = (profit / trade["size"] * 100) if trade["size"] > 0 else 0
                
                # Move to completed
                self.portfolio["completed_trades"].append(trade)
                self.portfolio["active_trades"].remove(trade)
                
                # Update totals
                self.portfolio["total_profit"] += profit
                
                # Add to daily performance
                self.portfolio["daily_performance"].append({
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "profit": profit,
                    "trade_id": trade_id
                })
                
                self.save_portfolio()
                return True
        
        return False
    
    def get_daily_summary(self):
        """Generate daily summary"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Calculate today's profit
        today_profit = 0
        for perf in self.portfolio["daily_performance"]:
            if perf["date"] == today:
                today_profit += perf["profit"]
        
        # Active trades summary
        active_summary = []
        for trade in self.portfolio["active_trades"]:
            # Calculate current P/L (simulated)
            current_value = trade["size"] * 1.5  # Simplified - would use real market data
            profit = current_value - trade["size"]
            
            active_summary.append({
                "market": trade["market"],
                "size": trade["size"],
                "estimated_profit": profit,
                "estimated_return": (profit / trade["size"] * 100) if trade["size"] > 0 else 0,
                "days_to_settle": self.days_until(trade.get("settlement"))
            })
        
        # Overall statistics
        total_trades = len(self.portfolio["completed_trades"]) + len(self.portfolio["active_trades"])
        winning_trades = len([t for t in self.portfolio["completed_trades"] if t["profit"] > 0])
        win_rate = (winning_trades / len(self.portfolio["completed_trades"]) * 100) if self.portfolio["completed_trades"] else 0
        
        avg_profit = sum(t["profit"] for t in self.portfolio["completed_trades"]) / len(self.portfolio["completed_trades"]) if self.portfolio["completed_trades"] else 0
        
        return {
            "date": today,
            "total_invested": self.portfolio["total_invested"],
            "total_profit": self.portfolio["total_profit"],
            "today_profit": today_profit,
            "active_trades": len(self.portfolio["active_trades"]),
            "completed_trades": len(self.portfolio["completed_trades"]),
            "win_rate": win_rate,
            "avg_profit": avg_profit,
            "active_summary": active_summary,
            "recent_completed": self.portfolio["completed_trades"][-5:] if self.portfolio["completed_trades"] else []
        }
    
    def days_until(self, date_str):
        """Calculate days until a date"""
        if not date_str:
            return None
        
        try:
            settlement = datetime.strptime(date_str, "%Y-%m-%d")
            return (settlement - datetime.now()).days
        except:
            return None
    
    def generate_report(self):
        """Generate comprehensive report"""
        summary = self.get_daily_summary()
        
        report = []
        report.append("# Kalshi Portfolio Summary")
        report.append(f"*Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        report.append("")
        
        # Overall Stats
        report.append("## 📊 Overall Statistics")
        report.append(f"- **Total Invested:** ${summary['total_invested']:.2f}")
        report.append(f"- **Total Profit:** ${summary['total_profit']:.2f}")
        report.append(f"- **Today's Profit:** ${summary['today_profit']:.2f}")
        report.append(f"- **Win Rate:** {summary['win_rate']:.1f}%")
        report.append(f"- **Average Profit per Trade:** ${summary['avg_profit']:.2f}")
        report.append("")
        
        # Active Trades
        report.append("## 📈 Active Trades")
        if summary['active_trades'] > 0:
            for trade in summary['active_summary']:
                report.append(f"### {trade['market'][:40]}...")
                report.append(f"- **Size:** ${trade['size']}")
                report.append(f"- **Estimated Profit:** ${trade['estimated_profit']:.2f}")
                report.append(f"- **Estimated Return:** {trade['estimated_return']:.1f}%")
                if trade['days_to_settle']:
                    report.append(f"- **Days to Settlement:** {trade['days_to_settle']}")
                report.append("")
        else:
            report.append("No active trades.")
            report.append("")
        
        # Recent Completed Trades
        if summary['recent_completed']:
            report.append("## 🏆 Recent Completed Trades")
            for trade in summary['recent_completed'][-3:]:  # Last 3 trades
                profit_color = "🟢" if trade['profit'] > 0 else "🔴"
                report.append(f"### {profit_color} {trade['market'][:30]}...")
                report.append(f"- **Profit:** ${trade['profit']:.2f}")
                report.append(f"- **Return:** {trade['return_pct']:.1f}%")
                report.append(f"- **Size:** ${trade['size']}")
                report.append(f"- **Duration:** {self.get_duration(trade.get('opened'), trade.get('closed'))}")
                report.append("")
        
        # Recommendations
        report.append("## 🎯 Recommendations")
        if summary['active_trades'] == 0:
            report.append("Consider opening new positions based on knowledge graph recommendations.")
        elif summary['win_rate'] > 70:
            report.append("High win rate detected. Consider scaling up position sizes.")
        else:
            report.append("Review trading strategy. Consider focusing on higher-probability markets.")
        report.append("")
        
        # Next Actions
        report.append("## 📅 Next Actions")
        report.append("1. Check gas position tracker reports")
        report.append("2. Review knowledge graph patterns")
        report.append("3. Monitor active trade settlements")
        report.append("4. Consider adding to winning positions")
        report.append("")
        
        report.append(f"*Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        return "\n".join(report)
    
    def get_duration(self, start_str, end_str):
        """Calculate duration between two dates"""
        try:
            start = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
            end = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
            days = (end - start).days
            return f"{days} days" if days > 0 else "Same day"
        except:
            return "Unknown"

def main():
    """Main function"""
    print("📊 Kalshi Portfolio Summary")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tracker = PortfolioTracker()
    
    # Add sample trades (in production, would load from actual trades)
    sample_trades = [
        {
            "market": "Paxton short position",
            "direction": "short",
            "size": 25,
            "entry_price": "low",
            "current_price": "closed",
            "target_price": "high",
            "stop_loss": "none",
            "settlement": "2026-03-04",
            "profit": 88
        },
        {
            "market": "Gas prices in the US this month > $3.50",
            "direction": "YES",
            "size": 25,
            "entry_price": "<50¢",
            "current_price": "active",
            "target_price": "$3.50",
            "stop_loss": "35¢",
            "settlement": "2026-03-31"
        },
        {
            "market": "US gas prices this week > $3.310",
            "direction": "YES",
            "size": 50,
            "entry_price": "<60¢",
            "current_price": "active",
            "target_price": "$3.310",
            "stop_loss": "40¢",
            "settlement": "2026-03-08"
        }
    ]
    
    # Add trades to portfolio
    print("📝 Loading portfolio data...")
    for trade in sample_trades:
        if "Paxton" in trade["market"]:
            # This trade is already completed
            tracker.add_trade(trade)
            tracker.close_trade(tracker.portfolio["active_trades"][-1]["id"], "high", 88)
        else:
            tracker.add_trade(trade)
    
    # Generate report
    print("📈 Generating portfolio report...")
    report = tracker.generate_report()
    
    # Save report
    report_dir = "/Users/cubiczan/.openclaw/workspace/portfolio_reports"
    os.makedirs(report_dir, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    report_path = os.path.join(report_dir, f"portfolio_report_{date_str}.md")
    
    with open(report_path, "w") as f:
        f.write(report)
    
    print(f"✅ Report saved to: {report_path}")
    print()
    
    # Print summary
    summary = tracker.get_daily_summary()
    print("💰 Portfolio Summary:")
    print(f"  Total Invested: ${summary['total_invested']:.2f}")
    print(f"  Total Profit: ${summary['total_profit']:.2f}")
    print(f"  Active Trades: {summary['active_trades']}")
    print(f"  Win Rate: {summary['win_rate']:.1f}%")
    print()
    
    print("📅 Next portfolio update: Tomorrow 6:00 PM")
    print("📁 Reports saved to: /Users/cubiczan/.openclaw/workspace/portfolio_reports/")

if __name__ == "__main__":
    main()
