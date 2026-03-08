#!/usr/bin/env python3
"""
Friday Kalshi Opportunities Scanner
Runs every Friday to identify and test Gold, Silver, Copper price predictions
for the following weekend settlement
"""

import os
import sys
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import random

class FridayKalshiScanner:
    """Friday metals opportunities scanner for Kalshi"""
    
    def __init__(self):
        self.workspace_root = Path.home() / ".openclaw" / "workspace"
        self.monitoring_dir = self.workspace_root / "metals_monitoring"
        self.db_path = self.monitoring_dir / "metals_prices.db"
        
        # Trading parameters
        self.trading_capital = 500  # Adjust based on your capital
        self.max_position_size = 0.05  # 5% of capital per trade
        self.min_confidence = 0.65  # Minimum confidence threshold
        
        # Metals to analyze
        self.metals = ["gold", "silver", "copper"]
        
        # Kalshi market timeframes (adjust based on actual Kalshi markets)
        self.timeframes = {
            "weekly": "WEEKLY",  # Settles following Friday
            "weekend": "WEEKEND"  # Settles Monday morning (weekend move)
        }
        
    def get_current_prices(self):
        """Get current prices for all metals"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        prices = {}
        for metal in self.metals:
            cursor.execute('''
                SELECT price FROM metal_prices 
                WHERE metal = ? 
                ORDER BY timestamp DESC 
                LIMIT 1
            ''', (metal,))
            
            result = cursor.fetchone()
            if result:
                prices[metal] = result[0]
            else:
                # Fallback prices if no data
                fallback_prices = {
                    "gold": 2185.50,
                    "silver": 24.85,
                    "copper": 5.79
                }
                prices[metal] = fallback_prices.get(metal, 0)
        
        conn.close()
        return prices
    
    def analyze_weekly_trend(self, metal, current_price):
        """Analyze weekly trend for a metal"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get last 5 trading days (Monday-Friday)
        cursor.execute('''
            SELECT price, timestamp FROM metal_prices 
            WHERE metal = ? 
            AND DATE(timestamp) >= DATE('now', 'weekday 0', '-7 days')
            ORDER BY timestamp
        ''', (metal,))
        
        weekly_prices = cursor.fetchall()
        conn.close()
        
        if len(weekly_prices) < 3:
            return None
        
        # Calculate weekly metrics
        price_values = [p[0] for p in weekly_prices]
        week_open = price_values[0]
        week_high = max(price_values)
        week_low = min(price_values)
        week_close = current_price
        
        # Weekly change
        weekly_change = ((week_close - week_open) / week_open) * 100
        
        # Determine trend strength
        if weekly_change > 1.5:
            trend = "strong_bullish"
            confidence = min(0.85, 0.7 + (weekly_change / 10))
        elif weekly_change > 0.5:
            trend = "bullish"
            confidence = 0.65 + (weekly_change / 20)
        elif weekly_change < -1.5:
            trend = "strong_bearish"
            confidence = min(0.85, 0.7 + (abs(weekly_change) / 10))
        elif weekly_change < -0.5:
            trend = "bearish"
            confidence = 0.65 + (abs(weekly_change) / 20)
        else:
            trend = "neutral"
            confidence = 0.5
        
        return {
            "metal": metal,
            "current_price": current_price,
            "week_open": week_open,
            "week_high": week_h