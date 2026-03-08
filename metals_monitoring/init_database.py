#!/usr/bin/env python3
"""
Initialize metals price database with historical data
"""

import sqlite3
import json
from datetime import datetime, timedelta
import random

DB_PATH = "metals_prices.db"

# Sample historical prices (March 2026)
historical_data = {
    "copper": [5.75, 5.78, 5.79, 5.77, 5.80, 5.82, 5.79, 5.81, 5.83, 5.79],
    "gold": [2180.50, 2182.75, 2185.50, 2183.25, 2186.00, 2188.50, 2185.50, 2187.25, 2189.00, 2185.50],
    "silver": [24.60, 24.65, 24.85, 24.70, 24.90, 24.95, 24.85, 24.88, 24.92, 24.85],
    "gas": [3.15, 3.18, 3.20, 3.19, 3.21, 3.22, 3.20, 3.198, 3.205, 3.198]
}

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS metal_prices (
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
    CREATE TABLE IF NOT EXISTS trading_signals (
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

# Insert historical data
base_date = datetime.now() - timedelta(days=9)

for i in range(10):
    timestamp = base_date + timedelta(days=i)
    
    for metal, prices in historical_data.items():
        price = prices[i]
        change = random.uniform(-0.5, 0.5)  # Simulated change
        
        cursor.execute('''
            INSERT INTO metal_prices (timestamp, metal, price, change_percent, source, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            timestamp.isoformat(),
            metal,
            price,
            change,
            "historical",
            json.dumps({"simulated": True})
        ))

conn.commit()
conn.close()

print(f"✅ Database initialized with 10 days of historical data for 4 metals")
print(f"   Database: {DB_PATH}")
print(f"   Metals: Copper, Gold, Silver, Gas")
print(f"   Records: {10 * 4} price entries")
