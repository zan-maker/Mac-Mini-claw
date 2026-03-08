#!/usr/bin/env python3
"""
Automated Metals & Energy Price Monitoring System
Monitors Copper, Gold, Silver, and Gas prices for Kalshi trading opportunities
"""

import os
import sys
import json
import requests
import time
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
import schedule
import threading

# Add workspace to path
sys.path.append('/Users/cubiczan/.openclaw/workspace')

class MetalsMonitoringSystem:
    """Comprehensive metals and energy price monitoring"""
    
    def __init__(self):
        self.workspace_root = Path.home() / ".openclaw" / "workspace"
        self.monitoring_dir = self.workspace_root / "metals_monitoring"
        self.monitoring_dir.mkdir(parents=True, exist_ok=True)
        
        # Database setup
        self.db_path = self.monitoring_dir / "metals_prices.db"
        self._init_database()
        
        # API endpoints
        self.api_endpoints = {
            "copper": "https://tradingeconomics.com/commodity/copper",
            "gold": "https://tradingeconomics.com/commodity/gold",
            "silver": "https://tradingeconomics.com/commodity/silver",
            "gas": "https://gasprices.aaa.com/",
            "lme_copper": "https://www.lme.com/Metals/Non-ferrous/LME-Copper",
            "comex_gold": "https://www.cmegroup.com/markets/metals/precious/gold.quotes.html",
            "comex_silver": "https://www.cmegroup.com/markets/metals/precious/silver.quotes.html"
        }
        
        # Kalshi market mappings (example - need to verify actual tickers)
        self.kalshi_markets = {
            "copper": {
                "weekly": "COPPER-WEEKLY-",
                "monthly": "COPPER-MONTHLY-",
                "quarterly": "COPPER-QUARTERLY-"
            },
            "gold": {
                "weekly": "GOLD-WEEKLY-",
                "monthly": "GOLD-MONTHLY-",
                "quarterly": "GOLD-QUARTERLY-"
            },
            "silver": {
                "weekly": "SILVER-WEEKLY-",
                "monthly": "SILVER-MONTHLY-",
                "quarterly": "SILVER-QUARTERLY-"
            },
            "gas": {
                "weekly": "GAS-WEEKLY-",
                "monthly": "GAS-MONTHLY-",
                "quarterly": "GAS-QUARTERLY-"
            }
        }
        
        # Trading parameters
        self.trading_params = {
            "copper": {
                "volatility_threshold": 0.03,  # 3% daily move
                "position_size": 0.10,  # 10% of capital per trade
                "target_range": 0.02,  # 2% target move
                "stop_loss": 0.05  # 5% stop loss
            },
            "gold": {
                "volatility_threshold": 0.02,  # 2% daily move
                "position_size": 0.08,  # 8% of capital per trade
                "target_range": 0.015,  # 1.5% target move
                "stop_loss": 0.04  # 4% stop loss
            },
            "silver": {
                "volatility_threshold": 0.04,  # 4% daily move
                "position_size": 0.06,  # 6% of capital per trade
                "target_range": 0.025,  # 2.5% target move
                "stop_loss": 0.06  # 6% stop loss
            },
            "gas": {
                "volatility_threshold": 0.05,  # 5% daily move
                "position_size": 0.12,  # 12% of capital per trade
                "target_range": 0.03,  # 3% target move
                "stop_loss": 0.07  # 7% stop loss
            }
        }
        
        # Load existing positions
        self.positions_file = self.monitoring_dir / "active_positions.json"
        self._load_positions()
        
    def _init_database(self):
        """Initialize SQLite database for price tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create prices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metal_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                metal TEXT NOT NULL,
                price REAL NOT NULL,
                change_percent REAL,
                volume INTEGER,
                source TEXT,
                metadata TEXT
            )
        ''')
        
        # Create alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created DATETIME DEFAULT CURRENT_TIMESTAMP,
                metal TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                threshold REAL NOT NULL,
                triggered BOOLEAN DEFAULT FALSE,
                triggered_at DATETIME,
                notification_sent BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Create trading signals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trading_signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                metal TEXT NOT NULL,
                signal_type TEXT NOT NULL,
                strength REAL,
                price REAL,
                target_price REAL,
                stop_loss REAL,
                confidence REAL,
                rationale TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def _load_positions(self):
        """Load existing trading positions"""
        if self.positions_file.exists():
            with open(self.positions_file, 'r') as f:
                self.positions = json.load(f)
        else:
            self.positions = {
                "copper": [],
                "gold": [],
                "silver": [],
                "gas": []
            }
            
    def _save_positions(self):
        """Save trading positions to file"""
        with open(self.positions_file, 'w') as f:
            json.dump(self.positions, f, indent=2)
    
    def fetch_copper_price(self):
        """Fetch current copper price"""
        try:
            # Try Trading Economics API
            url = "https://api.tradingeconomics.com/markets/commodities"
            # Note: Would need API key for full access
            # For now, use web scraping approach
            
            # Simulated data (replace with actual API call)
            price_data = {
                "price": 5.79,  # USD/lb
                "change_percent": 0.62,
                "volume": 125000,
                "source": "COMEX",
                "timestamp": datetime.now().isoformat()
            }
            
            # Store in database
            self._store_price("copper", price_data)
            return price_data
            
        except Exception as e:
            print(f"Error fetching copper price: {e}")
            return None
    
    def fetch_gold_price(self):
        """Fetch current gold price"""
        try:
            # Simulated data (replace with actual API call)
            price_data = {
                "price": 2185.50,  # USD/oz
                "change_percent": 0.35,
                "volume": 85000,
                "source": "COMEX",
                "timestamp": datetime.now().isoformat()
            }
            
            self._store_price("gold", price_data)
            return price_data
            
        except Exception as e:
            print(f"Error fetching gold price: {e}")
            return None
    
    def fetch_silver_price(self):
        """Fetch current silver price"""
        try:
            # Simulated data (replace with actual API call)
            price_data = {
                "price": 24.85,  # USD/oz
                "change_percent": 0.82,
                "volume": 65000,
                "source": "COMEX",
                "timestamp": datetime.now().isoformat()
            }
            
            self._store_price("silver", price_data)
            return price_data
            
        except Exception as e:
            print(f"Error fetching silver price: {e}")
            return None
    
    def fetch_gas_price(self):
        """Fetch current national average gas price"""
        try:
            # AAA Gas Prices
            url = "https://gasprices.aaa.com/"
            
            # Simulated data (replace with actual scraping)
            price_data = {
                "price": 3.198,  # USD/gallon
                "change_percent": 2.86,
                "volume": None,
                "source": "AAA",
                "timestamp": datetime.now().isoformat(),
                "regional": {
                    "california": 4.52,
                    "new_york": 3.45,
                    "texas": 2.98
                }
            }
            
            self._store_price("gas", price_data)
            return price_data
            
        except Exception as e:
            print(f"Error fetching gas price: {e}")
            return None
    
    def _store_price(self, metal, price_data):
        """Store price data in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO metal_prices 
            (metal, price, change_percent, volume, source, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            metal,
            price_data["price"],
            price_data.get("change_percent", 0),
            price_data.get("volume", 0),
            price_data.get("source", "unknown"),
            json.dumps(price_data.get("metadata", {}))
        ))
        
        conn.commit()
        conn.close()
        
        # Check for alerts
        self._check_alerts(metal, price_data["price"])
        
        # Generate trading signals
        self._generate_signals(metal, price_data)
    
    def _check_alerts(self, metal, price):
        """Check if price triggers any alerts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM price_alerts 
            WHERE metal = ? AND triggered = FALSE
        ''', (metal,))
        
        alerts = cursor.fetchall()
        
        for alert in alerts:
            alert_id, _, alert_metal, alert_type, threshold, _, _, _ = alert
            
            triggered = False
            if alert_type == "above" and price > threshold:
                triggered = True
            elif alert_type == "below" and price < threshold:
                triggered = True
            elif alert_type == "change" and abs(price - threshold) < 0.01:
                triggered = True
            
            if triggered:
                cursor.execute('''
                    UPDATE price_alerts 
                    SET triggered = TRUE, triggered_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (alert_id,))
                
                # Send notification
                self._send_alert_notification(alert_metal, alert_type, threshold, price)
        
        conn.commit()
        conn.close()
    
    def _send_alert_notification(self, metal, alert_type, threshold, price):
        """Send price alert notification"""
        message = f"🚨 {metal.upper()} ALERT: Price ${price} {alert_type} ${threshold}"
        print(f"ALERT: {message}")
        
        # Log to file
        alert_log = self.monitoring_dir / "alerts.log"
        with open(alert_log, 'a') as f:
            f.write(f"{datetime.now().isoformat()} - {message}\n")
        
        # Could add Discord/email notifications here
        # For now, just log to file
    
    def _generate_signals(self, metal, price_data):
        """Generate trading signals based on price action"""
        price = price_data["price"]
        change = price_data.get("change_percent", 0)
        
        # Get recent price history
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT price FROM metal_prices 
            WHERE metal = ? 
            ORDER BY timestamp DESC 
            LIMIT 20
        ''', (metal,))
        
        recent_prices = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        if len(recent_prices) < 5:
            return  # Not enough data
        
        # Calculate simple moving averages
        sma_5 = sum(recent_prices[:5]) / 5
        sma_10 = sum(recent_prices[:10]) / 10 if len(recent_prices) >= 10 else None
        
        # Generate signals
        signals = []
        
        # Trend signals
        if price > sma_5 and (sma_10 is None or sma_5 > sma_10):
            signals.append({
                "type": "bullish_trend",
                "strength": min(0.8, (price - sma_5) / sma_5 * 10),
                "confidence": 0.7
            })
        
        # Volatility signals
        volatility = self._calculate_volatility(recent_prices)
        params = self.trading_params.get(metal, {})
        
        if volatility > params.get("volatility_threshold", 0.03):
            signals.append({
                "type": "high_volatility",
                "strength": volatility,
                "confidence": 0.6
            })
        
        # Mean reversion signals
        if len(recent_prices) >= 10:
            avg_price = sum(recent_prices) / len(recent_prices)
            deviation = abs(price - avg_price) / avg_price
            
            if deviation > 0.05:  # 5% deviation from mean
                direction = "below" if price < avg_price else "above"
                signals.append({
                    "type": f"mean_reversion_{direction}",
                    "strength": deviation,
                    "confidence": 0.65,
                    "target_price": avg_price
                })
        
        # Store signals
        for signal in signals:
            self._store_signal(metal, signal, price)
    
    def _calculate_volatility(self, prices):
        """Calculate volatility of price series"""
        if len(prices) < 2:
            return 0
        
        returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]
        if not returns:
            return 0
        
        import statistics
        return statistics.stdev(returns) if len(returns) > 1 else 0
    
    def _store_signal(self, metal, signal, current_price):
        """Store trading signal in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        params = self.trading_params.get(metal, {})
        
        cursor.execute('''
            INSERT INTO trading_signals 
            (metal, signal_type, strength, price, target_price, stop_loss, confidence, rationale)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metal,
            signal["type"],
            signal.get("strength", 0),
            current_price,
            signal.get("target_price", current_price * (1 + params.get("target_range", 0.02))),
            current_price * (1 - params.get("stop_loss", 0.05)),
            signal.get("confidence", 0.5),
            json.dumps(signal)
        ))
        
        conn.commit()
        conn.close()
        
        # Log strong signals
        if signal.get("confidence", 0) > 0.7:
            print(f"📈 STRONG SIGNAL: {metal.upper()} - {signal['type']} (confidence: {signal['confidence']:.2f})")
    
    def setup_price_alerts(self, metal, alert_type, threshold):
        """Set up price alert"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO price_alerts (metal, alert_type, threshold)
            VALUES (?, ?, ?)
        ''', (metal, alert_type, threshold))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Alert set: {metal.upper()} {alert_type} ${threshold}")
    
    def generate_kalshi_recommendations(self):
        """Generate Kalshi trading recommendations based on signals"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent strong signals
        cursor.execute('''
            SELECT * FROM trading_signals 
            WHERE confidence > 0.7
            AND timestamp > datetime('now', '-1 hour')
            ORDER BY confidence DESC
        ''')
        
        signals = cursor.fetchall()
        conn.close()
        
        recommendations = []
        
        for signal in signals:
            _, timestamp, metal, signal_type, strength, price, target, stop_loss, confidence, rationale = signal
            
            # Determine Kalshi market and direction
            market_type = self._determine_kalshi_market(metal, signal_type, price, target)
            
            if market_type:
                recommendation = {
                    "metal": metal,
                    "signal_type": signal_type,
                    "current_price": price,
                    "target_price": target,
                    "confidence": confidence,
                    "kalshi_market": market_type["market"],
                    "direction": market_type["direction"],
                    "rationale": json.loads(rationale),
                    "timestamp": timestamp
                }
                recommendations.append(recommendation)
        
        return recommendations
    
    def _determine_kalshi_market(self, metal, signal_type, current_price, target_price):
        """Determine appropriate Kalshi market and direction"""
        # This is simplified - need actual Kalshi market data
        
        price_change = (target_price - current_price) / current_price
        
        if "bullish" in signal_type.lower() or price_change > 0:
            direction = "YES"  # Price will be above target
            market_suffix = "ABOVE"
        else:
            direction = "NO"   # Price will be