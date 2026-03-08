#!/usr/bin/env python3
"""
Metals Monitoring Daemon - Runs continuously to monitor Copper, Gold, Silver, Gas prices
Generates Kalshi trading recommendations and alerts
"""

import os
import sys
import json
import time
import schedule
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
import requests
import threading

class MetalsMonitoringDaemon:
    """Continuous metals price monitoring daemon"""
    
    def __init__(self):
        self.workspace_root = Path.home() / ".openclaw" / "workspace"
        self.monitoring_dir = self.workspace_root / "metals_monitoring"
        self.monitoring_dir.mkdir(parents=True, exist_ok=True)
        
        # Database
        self.db_path = self.monitoring_dir / "metals_prices.db"
        
        # Log files
        self.price_log = self.monitoring_dir / "price_history.log"
        self.signal_log = self.monitoring_dir / "trading_signals.log"
        self.alert_log = self.monitoring_dir / "alerts.log"
        
        # Configuration
        self.config_file = self.monitoring_dir / "config.json"
        self._load_config()
        
        # Trading capital (adjust based on your available capital)
        self.trading_capital = 500  # Default $500, adjust as needed
        
        # Initialize
        self._init_database()
        
    def _load_config(self):
        """Load monitoring configuration"""
        default_config = {
            "monitoring_interval": 300,  # 5 minutes
            "alert_thresholds": {
                "copper": {"volatility": 0.03, "move": 0.02},
                "gold": {"volatility": 0.02, "move": 0.015},
                "silver": {"volatility": 0.04, "move": 0.025},
                "gas": {"volatility": 0.05, "move": 0.03}
            },
            "kalshi_integration": {
                "enabled": True,
                "min_confidence": 0.7,
                "max_positions_per_day": 3
            },
            "notification_channels": ["log_file", "discord"],
            "discord_webhook": None  # Set your Discord webhook URL here
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
    
    def _init_database(self):
        """Initialize database if needed"""
        if not self.db_path.exists():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE metal_prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metal TEXT NOT NULL,
                    price REAL NOT NULL,
                    change_percent REAL,
                    source TEXT,
                    metadata TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE trading_signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metal TEXT NOT NULL,
                    signal_type TEXT NOT NULL,
                    current_price REAL,
                    target_price REAL,
                    confidence REAL,
                    position_size REAL,
                    kalshi_market TEXT,
                    kalshi_direction TEXT,
                    executed BOOLEAN DEFAULT FALSE
                )
            ''')
            
            conn.commit()
            conn.close()
    
    def fetch_metal_price(self, metal):
        """Fetch current price for a metal"""
        # These are placeholder APIs - replace with actual API calls
        
        price_endpoints = {
            "copper": {
                "url": "https://api.metalpriceapi.com/v1/latest",
                "params": {"api_key": "YOUR_API_KEY", "base": "USD", "currencies": "XCU"},
                "extract": lambda data: data["rates"]["XCU"]
            },
            "gold": {
                "url": "https://api.metalpriceapi.com/v1/latest",
                "params": {"api_key": "YOUR_API_KEY", "base": "USD", "currencies": "XAU"},
                "extract": lambda data: data["rates"]["XAU"]
            },
            "silver": {
                "url": "https://api.metalpriceapi.com/v1/latest",
                "params": {"api_key": "YOUR_API_KEY", "base": "USD", "currencies": "XAG"},
                "extract": lambda data: data["rates"]["XAG"]
            },
            "gas": {
                "url": "https://api.eia.gov/v2/petroleum/pri/gnd/data",
                "params": {"api_key": "YOUR_API_KEY", "frequency": "weekly", "data": ["value"]},
                "extract": lambda data: data["data"][0]["value"] if data["data"] else None
            }
        }
        
        if metal not in price_endpoints:
            return None
        
        endpoint = price_endpoints[metal]
        
        try:
            # For now, use simulated data
            # Replace with actual API call when you have API keys
            
            simulated_prices = {
                "copper": 5.79,  # USD/lb
                "gold": 2185.50,  # USD/oz
                "silver": 24.85,  # USD/oz
                "gas": 3.198  # USD/gallon
            }
            
            price_data = {
                "price": simulated_prices.get(metal, 0),
                "change_percent": 0.0,  # Would calculate from previous price
                "source": "simulated",
                "timestamp": datetime.now().isoformat()
            }
            
            # Store in database
            self._store_price(metal, price_data)
            
            return price_data
            
        except Exception as e:
            print(f"Error fetching {metal} price: {e}")
            return None
    
    def _store_price(self, metal, price_data):
        """Store price in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO metal_prices (metal, price, change_percent, source, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            metal,
            price_data["price"],
            price_data.get("change_percent", 0),
            price_data.get("source", "unknown"),
            json.dumps(price_data)
        ))
        
        conn.commit()
        conn.close()
        
        # Log to file
        with open(self.price_log, 'a') as f:
            f.write(f"{datetime.now().isoformat()},{metal},{price_data['price']},{price_data.get('change_percent', 0)}\n")
    
    def analyze_price_action(self, metal):
        """Analyze price action and generate trading signals"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get last 20 prices
        cursor.execute('''
            SELECT price FROM metal_prices 
            WHERE metal = ? 
            ORDER BY timestamp DESC 
            LIMIT 20
        ''', (metal,))
        
        prices = [row[0] for row in cursor.fetchall()]
        
        if len(prices) < 5:
            conn.close()
            return None
        
        # Calculate indicators
        current_price = prices[0]
        sma_5 = sum(prices[:5]) / 5
        sma_10 = sum(prices[:10]) / 10 if len(prices) >= 10 else None
        
        # Calculate volatility
        returns = [(prices[i] - prices[i+1]) / prices[i+1] for i in range(len(prices)-1)]
        volatility = (sum([r**2 for r in returns]) / len(returns))**0.5 if returns else 0
        
        # Generate signals
        signals = []
        
        # Trend signal
        if sma_10:
            if current_price > sma_5 > sma_10:
                signals.append({
                    "type": "bullish_trend",
                    "confidence": min(0.8, (current_price - sma_5) / sma_5 * 10),
                    "target_price": current_price * 1.02  # 2% target
                })
            elif current_price < sma_5 < sma_10:
                signals.append({
                    "type": "bearish_trend",
                    "confidence": min(0.8, (sma_5 - current_price) / current_price * 10),
                    "target_price": current_price * 0.98  # -2% target
                })
        
        # Volatility signal
        threshold = self.config["alert_thresholds"][metal]["volatility"]
        if volatility > threshold:
            signals.append({
                "type": "high_volatility",
                "confidence": min(0.7, volatility / threshold),
                "target_price": None
            })
        
        # Mean reversion signal
        if len(prices) >= 10:
            avg_price = sum(prices) / len(prices)
            deviation = abs(current_price - avg_price) / avg_price
            
            if deviation > 0.05:  # 5% deviation
                direction = "above" if current_price > avg_price else "below"
                signals.append({
                    "type": f"mean_reversion_{direction}",
                    "confidence": 0.65,
                    "target_price": avg_price
                })
        
        conn.close()
        
        # Return strongest signal
        if signals:
            strongest_signal = max(signals, key=lambda x: x["confidence"])
            return strongest_signal
        return None
    
    def generate_kalshi_recommendation(self, metal, signal, current_price):
        """Generate Kalshi trading recommendation"""
        
        # Map signal to Kalshi market
        market_mapping = {
            "bullish_trend": {
                "market": f"{metal.upper()}-WEEKLY-ABOVE",
                "direction": "YES",
                "target": signal["target_price"]
            },
            "bearish_trend": {
                "market": f"{metal.upper()}-WEEKLY-BELOW",
                "direction": "NO",
                "target": signal["target_price"]
            },
            "mean_reversion_above": {
                "market": f"{metal.upper()}-WEEKLY-BELOW",
                "direction": "YES",
                "target": signal["target_price"]
            },
            "mean_reversion_below": {
                "market": f"{metal.upper()}-WEEKLY-ABOVE",
                "direction": "YES",
                "target": signal["target_price"]
            },
            "high_volatility": {
                "market": f"{metal.upper()}-WEEKLY-RANGE",
                "direction": "INSIDE",
                "target": None
            }
        }
        
        if signal["type"] not in market_mapping:
            return None
        
        market_info = market_mapping[signal["type"]]
        
        # Calculate position size (1-5% of capital based on confidence)
        position_pct = min(0.05, signal["confidence"] * 0.07)  # Max 5%, scaled by confidence
        position_size = self.trading_capital * position_pct
        
        recommendation = {
            "metal": metal,
            "signal_type": signal["type"],
            "current_price": current_price,
            "target_price": market_info["target"],
            "confidence": signal["confidence"],
            "kalshi_market": market_info["market"],
            "kalshi_direction": market_info["direction"],
            "position_size": round(position_size, 2),
            "timestamp": datetime.now().isoformat()
        }
        
        return recommendation
    
    def store_recommendation(self, recommendation):
        """Store trading recommendation in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO trading_signals 
            (metal, signal_type, current_price, target_price, confidence, position_size, kalshi_market, kalshi_direction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            recommendation["metal"],
            recommendation["signal_type"],
            recommendation["current_price"],
            recommendation["target_price"],
            recommendation["confidence"],
            recommendation["position_size"],
            recommendation["kalshi_market"],
            recommendation["kalshi_direction"]
        ))
        
        conn.commit()
        conn.close()
        
        # Log to file
        with open(self.signal_log, 'a') as f:
            f.write(f"{datetime.now().isoformat()},{recommendation['metal']},{recommendation['signal_type']},"
                   f"{recommendation['current_price']},{recommendation['target_price']},"
                   f"{recommendation['confidence']},{recommendation['position_size']},"
                   f"{recommendation['kalshi_market']},{recommendation['kalshi_direction']}\n")
        
        # Send notification if confidence > threshold
        if recommendation["confidence"] > self.config["kalshi_integration"]["min_confidence"]:
            self.send_notification(recommendation)
    
    def send_notification(self, recommendation):
        """Send notification about trading signal"""
        message = f"📈 **{recommendation['metal'].upper()} TRADING SIGNAL**\n"
        message += f"**Signal:** {recommendation['signal_type']}\n"
        message += f"**Current Price:** ${recommendation['current_price']:.2f}\n"
        
        if recommendation['target_price']:
            message += f"**Target Price:** ${recommendation['target_price']:.2f}\n"
        
        message += f"**Confidence:** {recommendation['confidence']:.1%}\n"
        message += f"**Kalshi Market:** {recommendation['kalshi_market']}\n"
        message += f"**Direction:** {recommendation['kalshi_direction']}\n"
        message += f"**Position Size:** ${recommendation['position_size']:.2f}\n"
        
        print(f"\n{'='*60}")
        print(message)
        print(f"{'='*60}\n")
        
        # Log to alert file
        with open(self.alert_log, 'a') as f:
            f.write(f"{datetime.now().isoformat()} - {message.replace('**', '').replace('\n', ' | ')}\n")
        
        # Send to Discord if webhook configured
        webhook = self.config.get("discord_webhook")
        if webhook and "discord" in self.config["notification_channels"]:
            try:
                discord_data = {
                    "content": message,
                    "embeds": [{
                        "title": f"{recommendation['metal'].upper()} Trading Signal",
                        "description": f"**{recommendation['signal_type']}** with {recommendation['confidence']:.1%} confidence",
                        "fields": [
                            {"name": "Current Price", "value": f"${recommendation['current_price']:.2f}", "inline": True},
                            {"name": "Target Price", "value": f"${recommendation['target_price']:.2f}" if recommendation['target_price'] else "N/A", "inline": True},
                            {"name": "Kalshi Market", "value": recommendation['kalshi_market'], "inline": False},
                            {"name": "Direction", "value": recommendation['kalshi_direction'], "inline": True},
                            {"name": "Position Size", "value": f"${recommendation['position_size']:.2f}", "inline": True}
                        ],
                        "color": 0x00ff00 if recommendation['confidence'] > 0.8 else 0xff9900,
                        "timestamp": datetime.now().isoformat()
                    }]
                }
                
                # Uncomment when you have Discord webhook
                # response = requests.post(webhook, json=discord_data)
                # if response.status_code != 204:
                #     print(f"Discord notification failed: {response.status_code}")
                
            except Exception as e:
                print(f"Error sending Discord notification: {e}")
    
    def monitor_all_metals(self):
        """Monitor all metals and generate signals"""
        metals = ["copper", "gold", "silver", "gas"]
        
        print(f"\n🔍 Monitoring metals at {datetime.now().strftime('%H:%M:%S')}")
        
        for metal in metals:
            # Fetch current price
            price_data = self.fetch_metal_price(metal)
            if not price_data:
                continue
            
            # Analyze price action
            signal = self.analyze_price_action(metal)
            
            if signal and signal["confidence"] > 0.6:
                # Generate Kalshi recommendation
                recommendation = self.generate_kalshi_recommendation(metal, signal, price_data["price"])
                
                if recommendation:
                    # Store recommendation
                    self.store_recommendation(recommendation)
    
    def run_daily_report(self):
        """Generate daily trading report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get today's signals
        cursor.execute('''
            SELECT COUNT(*) as total_signals,
                   AVG(confidence) as avg_confidence,
                   SUM(CASE WHEN confidence > 0.7 THEN 1 ELSE 0 END) as strong_signals
            FROM trading_signals 
            WHERE DATE(timestamp) = DATE('now')
        ''')
        
        stats = cursor.fetchone()
        
        # Get today's price changes
        cursor.execute('''
            SELECT metal, 
                   MAX(price) as high,
                   MIN(price) as low,
                   (SELECT price FROM metal_prices WHERE metal = m.metal ORDER BY timestamp DESC LIMIT 1) as last_price
            FROM metal_prices m
            WHERE DATE(timestamp) = DATE('now')
            GROUP BY metal
        ''')
        
        price_changes = cursor.fetchall()
        
        conn.close()
        
        # Generate report
        report =