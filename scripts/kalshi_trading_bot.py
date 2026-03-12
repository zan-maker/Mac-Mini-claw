#!/usr/bin/env python3
"""
Kalshi Trading Bot Core Class
"""

import os
import sys
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import requests

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.pinchtab_client import PinchtabClient, BrowserMode

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/kalshi_bot_core.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class KalshiTradingBot:
    """Automated Kalshi trading bot using Pinchtab"""
    
    def __init__(self, pinchtab_host: str = "http://localhost:9867"):
        self.client = PinchtabClient(pinchtab_host)
        self.instance_id = None
        self.tab_id = None
        self.logged_in = False
        
        # Trading configuration
        self.max_position_size = 20  # Max $ per trade
        self.stop_loss_pct = 0.30    # 30% stop loss
        self.take_profit_pct = 0.70  # 70% take profit
        
        # State tracking
        self.active_trades = []
        self.portfolio_value = 0
        self.available_capital = 47  # From user: $47 to deploy
        
        logger.info("Kalshi Trading Bot initialized")
    
    def setup(self) -> bool:
        """Setup browser instance and login to Kalshi"""
        try:
            logger.info("Setting up Kalshi trading bot")
            
            # Check Pinchtab health
            if not self.client.health_check():
                logger.error("Pinchtab server not healthy")
                return False
            
            # Create browser instance
            self.instance_id = self.client.create_instance(
                name="kalshi-trader-bot",
                mode=BrowserMode.HEADLESS
            )
            
            if not self.instance_id:
                logger.error("Failed to create browser instance")
                return False
            
            # Open Kalshi tab
            self.tab_id = self.client.open_tab(
                instance_id=self.instance_id,
                url="https://kalshi.com",
                name="kalshi-trading"
            )
            
            if not self.tab_id:
                logger.error("Failed to open Kalshi tab")
                return False
            
            # Wait for page load
            time.sleep(3)
            
            # Check if we're on login page or dashboard
            snapshot = self.client.snapshot(self.tab_id, interactive=True, compact=True)
            if snapshot:
                page_text = self.client.extract_text(self.tab_id)
                if page_text and "Log in" in page_text:
                    logger.info("On login page - manual login required")
                    # In production, would automate login with credentials
                    # For now, assume manual login or already logged in
                else:
                    logger.info("Already on dashboard or logged in")
                    self.logged_in = True
            
            logger.info("Kalshi bot setup complete")
            return True
            
        except Exception as e:
            logger.error(f"Error setting up Kalshi bot: {e}")
            return False
    
    def monitor_gas_market(self) -> Dict:
        """Monitor gas market conditions"""
        try:
            logger.info("Monitoring gas market")
            
            # Navigate to gas markets
            self.client.navigate(self.tab_id, "https://kalshi.com/markets/energy")
            time.sleep(2)
            
            # Get page snapshot
            snapshot = self.client.snapshot(self.tab_id, interactive=True, compact=True)
            page_text = self.client.extract_text(self.tab_id)
            
            market_data = {
                "timestamp": datetime.now().isoformat(),
                "gas_month_price": None,
                "gas_week_price": None,
                "market_sentiment": "neutral",
                "volume": "unknown"
            }
            
            # Parse gas prices from page text (simplified)
            if page_text:
                import re
                
                # Look for gas price patterns
                gas_patterns = [
                    r'Gas.*month.*>.*\$(\d+\.\d{2})',
                    r'gas.*>.*\$(\d+\.\d{2})',
                    r'\$(\d+\.\d{2}).*gas'
                ]
                
                for pattern in gas_patterns:
                    matches = re.findall(pattern, page_text, re.IGNORECASE)
                    if matches:
                        market_data["gas_month_price"] = float(matches[0])
                        break
            
            logger.info(f"Gas market data: {market_data}")
            return market_data
            
        except Exception as e:
            logger.error(f"Error monitoring gas market: {e}")
            return {}
    
    def get_external_gas_price(self) -> Optional[float]:
        """Get current gas price from AAA website"""
        try:
            logger.info("Getting external gas price from AAA")
            
            # Create temporary instance for AAA
            aaa_instance = self.client.create_instance(
                name="aaa-gas-check",
                mode=BrowserMode.HEADLESS
            )
            
            if not aaa_instance:
                return None
            
            aaa_tab = self.client.open_tab(
                instance_id=aaa_instance,
                url="https://gasprices.aaa.com",
                name="aaa-gas"
            )
            
            if not aaa_tab:
                self.client.close_instance(aaa_instance)
                return None
            
            time.sleep(3)
            page_text = self.client.extract_text(aaa_tab)
            
            # Clean up
            self.client.close_tab(aaa_tab)
            self.client.close_instance(aaa_instance)
            
            # Parse price
            if page_text:
                import re
                price_pattern = r'\$(\d+\.\d{2})'
                matches = re.findall(price_pattern, page_text)
                if matches:
                    price = float(matches[0])
                    logger.info(f"AAA gas price: ${price}")
                    return price
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting external gas price: {e}")
            return None
    
    def check_iran_news(self) -> List[Dict]:
        """Check for Iran conflict news"""
        try:
            logger.info("Checking Iran conflict news")
            
            # Create temporary instance for news
            news_instance = self.client.create_instance(
                name="iran-news-check",
                mode=BrowserMode.HEADLESS
            )
            
            if not news_instance:
                return []
            
            news_tabs = []
            news_sources = [
                ("reuters", "https://www.reuters.com/search/news?blob=Iran+conflict"),
                ("bloomberg", "https://www.bloomberg.com/search?query=Iran"),
                ("cnbc", "https://www.cnbc.com/search/?query=Iran%20conflict")
            ]
            
            articles = []
            
            for source_name, source_url in news_sources:
                tab_id = self.client.open_tab(news_instance, source_url, f"news-{source_name}")
                if tab_id:
                    news_tabs.append(tab_id)
                    time.sleep(2)
                    
                    page_text = self.client.extract_text(tab_id)
                    if page_text:
                        # Simple keyword analysis
                        iran_keywords = ["Iran", "conflict", "attack", "missile", "Strait of Hormuz", "oil", "gas"]
                        keyword_count = sum(1 for keyword in iran_keywords if keyword.lower() in page_text.lower())
                        
                        articles.append({
                            "source": source_name,
                            "url": source_url,
                            "keyword_count": keyword_count,
                            "has_news": keyword_count > 3
                        })
            
            # Clean up
            for tab_id in news_tabs:
                self.client.close_tab(tab_id)
            self.client.close_instance(news_instance)
            
            logger.info(f"Found {len([a for a in articles if a['has_news']])} news sources with Iran conflict coverage")
            return articles
            
        except Exception as e:
            logger.error(f"Error checking Iran news: {e}")
            return []
    
    def analyze_trading_opportunity(self) -> Dict:
        """Analyze current trading opportunities"""
        try:
            logger.info("Analyzing trading opportunities")
            
            # Gather data from multiple sources
            gas_market = self.monitor_gas_market()
            aaa_price = self.get_external_gas_price()
            iran_news = self.check_iran_news()
            
            # Calculate opportunity score
            opportunity_score = 50  # Base score
            
            # Factor 1: Price discrepancy
            if gas_market.get("gas_month_price") and aaa_price:
                market_price = gas_market["gas_month_price"]
                discrepancy = abs(market_price - aaa_price)
                if discrepancy > 0.05:  # 5 cent discrepancy
                    opportunity_score += 20
                    logger.info(f"Price discrepancy found: market=${market_price}, AAA=${aaa_price}")
            
            # Factor 2: Iran news intensity
            iran_news_count = sum(1 for article in iran_news if article.get("has_news"))
            if iran_news_count >= 2:
                opportunity_score += 25
                logger.info(f"Iran news intensity: {iran_news_count} sources")
            
            # Factor 3: Current gas price level
            if aaa_price:
                if aaa_price < 3.25:  # Low price, potential to rise
                    opportunity_score += 15
                elif aaa_price > 3.40:  # High price, potential to fall
                    opportunity_score -= 10
            
            # Factor 4: Time to settlement
            days_to_settlement = (datetime(2026, 3, 31) - datetime.now()).days
            if 10 <= days_to_settlement <= 30:  # Optimal timeframe
                opportunity_score += 10
            
            # Cap score
            opportunity_score = max(0, min(100, opportunity_score))
            
            # Determine recommendation
            recommendation = "HOLD"
            position_size = 0
            
            if opportunity_score >= 70:
                recommendation = "BUY YES (Gas Month > $3.50)"
                position_size = min(self.max_position_size, self.available_capital * 0.5)
            elif opportunity_score >= 60:
                recommendation = "BUY YES (small position)"
                position_size = min(self.max_position_size, self.available_capital * 0.3)
            elif opportunity_score <= 30:
                recommendation = "BUY NO or reduce position"
                position_size = 0
            
            analysis = {
                "timestamp": datetime.now().isoformat(),
                "opportunity_score": opportunity_score,
                "recommendation": recommendation,
                "position_size": position_size,
                "gas_market_data": gas_market,
                "aaa_price": aaa_price,
                "iran_news_count": iran_news_count,
                "available_capital": self.available_capital,
                "confidence": f"{opportunity_score}%"
            }
            
            logger.info(f"Trading analysis: {analysis}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing trading opportunity: {e}")
            return {"error": str(e)}
    
    def execute_trade(self, market: str, side: str, amount: float) -> bool:
        """Execute a trade on Kalshi (simulated for now)"""
        try:
            logger.info(f"Executing trade: {market} {side} ${amount}")
            
            # In production, this would:
            # 1. Navigate to specific market page
            # 2. Find trade interface elements
            # 3. Enter trade details
            # 4. Click confirm
            
            # For now, simulate execution
            trade_id = f"trade_{int(time.time())}"
            
            trade_record = {
                "trade_id": trade_id,
                "market": market,
                "side": side,
                "amount": amount,
                "timestamp": datetime.now().isoformat(),
                "status": "executed",
                "execution_price": None  # Would get from market
            }
            
            self.active_trades.append(trade_record)
            self.available_capital -= amount
            
            # Save trade to file
            trades_file = "/Users/cubiczan/.openclaw/workspace/kalshi_trades.json"
            try:
                if os.path.exists(trades_file):
                    with open(trades_file, 'r') as f:
                        trades = json.load(f)
                else:
                    trades = []
                
                trades.append(trade_record)
                
                with open(trades_file, 'w') as f:
                    json.dump(trades, f, indent=2)
            except Exception as e:
                logger.error(f"Error saving trade: {e}")
            
            logger.info(f"Trade executed: {trade_record}")
            return True
            
        except Exception as e:
            logger.error(f"Error executing trade: {e}")
            return False
    
    def run_trading_cycle(self):
        """Run one complete trading cycle"""
        try:
            logger.info("Starting trading cycle")
            
            # Analyze opportunities
            analysis = self.analyze_trading_opportunity()
            
            # Check if we should trade
            if analysis.get("position_size", 0) > 0 and analysis.get("opportunity_score", 0) >= 60:
                # Execute trade
                market = "Gas prices in the US this month > $3.50"
                side = "YES"
                amount = analysis["position_size"]
                
                success = self.execute_trade(market, side, amount)
                if success:
                    logger.info(f"✅ Trade executed: {side} ${amount} on {market}")
                else:
                    logger.error("❌ Trade execution failed")
            else:
                logger.info(f"⏸️  No trade recommended (score: {analysis.get('opportunity_score', 0)})")
            
            # Save analysis
            analysis_file = "/Users/cubiczan/.openclaw/workspace/kalshi_analysis.json"
            try:
                with open(analysis_file, 'w') as f:
                    json.dump(analysis, f, indent=2)
            except Exception as e:
                logger.error(f"Error saving analysis: {e}")
            
            logger.info("Trading cycle complete")
            return analysis
            
        except Exception as e:
            logger.error(f"Error in trading cycle: {e}")
            return {"error": str(e)}
    
    def monitor_active_trades(self):
        """Monitor and manage active trades"""
        try:
            logger.info("Monitoring active trades")
            
            if not self.active_trades:
                logger.info("No active trades to monitor")
                return
            
            # Check current gas price
            current_price = self.get_external_gas_price()
            if not current_price:
                logger.warning("Could not get current gas price")
                return
            
            # Update each trade
            for trade in self.active_trades[:]:  # Copy list for iteration
                if trade["status"] == "executed":
                    # Calculate P&L (simplified)
                    target_price = 3.50
                    entry_price = trade.get("execution_price") or 3.20  # Default
                    
                    price_diff = current_price - entry_price
                    target_diff = target_price - entry_price
                    
                    if target_diff != 0:
                        progress_pct = (price_diff / target_diff) * 100
                    else:
                        progress_pct = 0
                    
                    # Update trade record
                    trade["current_price"] = current_price
                    trade["progress_pct"] = progress_pct
                    trade["last_updated"] = datetime.now().isoformat()
                    
                    # Check for exit conditions
                    if progress_pct >= self.take_profit_pct * 100:
                        logger.info(f"Trade {trade['trade_id']} hit take profit at {progress_pct:.1f}%")
                        trade["status"] = "closed_profit"
                        self.available_capital += trade["amount"] * 1.7  # 70% profit
                    elif progress_pct <= -self.stop_loss_pct * 100:
                        logger.info(f"Trade {trade['trade_id']} hit stop loss at {progress_pct:.1f}%")
                        trade["status"] = "closed_loss"
                        self.available_capital += trade["amount"] * 0.7  # 30% loss
            
            logger.info(f"Active trades: {len([t for t in self.active_trades if t['status'] == 'executed'])}")
            
        except Exception as e:
            logger.error(f"Error monitoring trades: {e}")
    
    def generate_report(self) -> Dict:
        """Generate trading report"""
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "available_capital": self.available_capital,
                "active_trades": len([t for t in self.active_trades if t["status"] == "executed"]),
                "closed_trades": len([t for t in self.active_trades if t["status"] != "executed"]),
                "total_profit": sum(t.get("profit", 0) for t in self.active_trades),
                "recent_analysis": None
            }
            
            # Load recent analysis
            analysis_file = "/Users/cubiczan/.openclaw/workspace/kalshi_analysis.json"
            if os.path.exists(analysis_file):
                try:
                    with open(analysis_file, 'r') as f:
                        report["recent_analysis"] = json.load(f)
                except:
                    pass
            
            logger.info(f"Trading report: {report}")
            return report
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return {"error": str(e)}
    
    def cleanup(self):
        """Clean up resources"""
        logger.info("Cleaning up Kalshi bot")
        
        if self.tab_id:
            self.client.close_tab(self.tab_id)
        
        if self.instance_id:
            self.client.close_instance(self.instance_id)
        
        logger.info("Cleanup complete")