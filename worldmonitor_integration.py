#!/usr/bin/env python3
"""
World Monitor Integration for Trade Recommender
Provides predictive signals for Kalshi arbitrage opportunities
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
import os

class WorldMonitorIntegration:
    """Integration with World Monitor for predictive signals"""
    
    def __init__(self, base_url: str = "https://finance.worldmonitor.app"):
        """
        Initialize World Monitor integration
        
        Args:
            base_url: World Monitor finance variant URL
        """
        self.base_url = base_url
        self.cache_dir = "/Users/cubiczan/.openclaw/workspace/cache/worldmonitor"
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def get_macro_signals(self, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get 7-signal macro dashboard from World Monitor
        
        Returns:
            Dict with macro signals including verdict (BUY/CASH/UNKNOWN)
        """
        cache_file = os.path.join(self.cache_dir, "macro_signals.json")
        
        # Check cache (5 minute TTL)
        if use_cache and os.path.exists(cache_file):
            cache_age = time.time() - os.path.getmtime(cache_file)
            if cache_age < 300:  # 5 minutes
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except:
                    pass
        
        try:
            # Try to get from World Monitor API
            # Note: World Monitor uses various endpoints, we'll try the main ones
            response = requests.get(f"{self.base_url}/api/macro-signals", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Cache the result
                with open(cache_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                return data
            else:
                # Fallback to local computation or cached data
                return self._get_fallback_signals()
                
        except Exception as e:
            print(f"Error fetching macro signals: {e}")
            return self._get_fallback_signals()
    
    def _get_fallback_signals(self) -> Dict[str, Any]:
        """Fallback signals when API is unavailable"""
        return {
            "timestamp": datetime.now().isoformat(),
            "verdict": "UNKNOWN",
            "bullish_count": 0,
            "total_count": 0,
            "signals": {
                "liquidity": {"status": "UNKNOWN", "sparkline": []},
                "flow_structure": {"status": "UNKNOWN"},
                "macro_regime": {"status": "UNKNOWN"},
                "technical_trend": {"status": "UNKNOWN", "sparkline": []},
                "hash_rate": {"status": "UNKNOWN"},
                "mining_cost": {"status": "UNKNOWN"},
                "fear_greed": {"status": "UNKNOWN", "history": []}
            },
            "meta": {"qqq_sparkline": []},
            "unavailable": True
        }
    
    def get_country_instability_index(self, country_code: str = "US") -> Dict[str, Any]:
        """
        Get country instability index for geopolitical risk assessment
        
        Args:
            country_code: ISO country code (e.g., "US", "CN", "RU")
            
        Returns:
            Dict with instability score and risk factors
        """
        cache_file = os.path.join(self.cache_dir, f"country_{country_code}.json")
        
        # Check cache (1 hour TTL)
        if os.path.exists(cache_file):
            cache_age = time.time() - os.path.getmtime(cache_file)
            if cache_age < 3600:  # 1 hour
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except:
                    pass
        
        try:
            # World Monitor likely has country-specific endpoints
            # This is a placeholder - actual endpoint may vary
            response = requests.get(
                f"{self.base_url}/api/country/{country_code}/instability",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Cache the result
                with open(cache_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                return data
            else:
                return self._get_fallback_country_data(country_code)
                
        except Exception as e:
            print(f"Error fetching country data for {country_code}: {e}")
            return self._get_fallback_country_data(country_code)
    
    def _get_fallback_country_data(self, country_code: str) -> Dict[str, Any]:
        """Fallback country data"""
        return {
            "country_code": country_code,
            "country_name": country_code,
            "instability_score": 0.5,
            "risk_level": "MEDIUM",
            "factors": [],
            "last_updated": datetime.now().isoformat(),
            "unavailable": True
        }
    
    def get_market_radar(self) -> Dict[str, Any]:
        """
        Get market radar data for trading signals
        
        Returns:
            Dict with market conditions and opportunities
        """
        cache_file = os.path.join(self.cache_dir, "market_radar.json")
        
        # Check cache (15 minute TTL)
        if os.path.exists(cache_file):
            cache_age = time.time() - os.path.getmtime(cache_file)
            if cache_age < 900:  # 15 minutes
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except:
                    pass
        
        try:
            # Try to get market data
            response = requests.get(f"{self.base_url}/api/markets", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Cache the result
                with open(cache_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                return data
            else:
                return self._get_fallback_market_data()
                
        except Exception as e:
            print(f"Error fetching market radar: {e}")
            return self._get_fallback_market_data()
    
    def _get_fallback_market_data(self) -> Dict[str, Any]:
        """Fallback market data"""
        return {
            "timestamp": datetime.now().isoformat(),
            "markets": [],
            "conditions": "UNKNOWN",
            "opportunities": [],
            "unavailable": True
        }
    
    def analyze_kalshi_arbitrage(self, kalshi_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze Kalshi prediction markets for arbitrage opportunities
        using World Monitor signals
        
        Args:
            kalshi_data: Kalshi market data
            
        Returns:
            List of arbitrage opportunities
        """
        opportunities = []
        
        # Get macro signals
        macro_signals = self.get_macro_signals()
        
        # Get market radar
        market_radar = self.get_market_radar()
        
        # Analyze each Kalshi market
        for market in kalshi_data.get("markets", []):
            opportunity = self._analyze_single_market(market, macro_signals, market_radar)
            if opportunity:
                opportunities.append(opportunity)
        
        # Sort by opportunity score
        opportunities.sort(key=lambda x: x.get("opportunity_score", 0), reverse=True)
        
        return opportunities[:5]  # Return top 5 opportunities
    
    def _analyze_single_market(self, market: Dict[str, Any], 
                              macro_signals: Dict[str, Any],
                              market_radar: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Analyze single Kalshi market for arbitrage
        
        Returns:
            Opportunity dict or None if no opportunity
        """
        try:
            # Extract market info
            market_id = market.get("id", "")
            title = market.get("title", "")
            yes_price = market.get("yes_price", 0.5)
            no_price = market.get("no_price", 0.5)
            volume = market.get("volume", 0)
            
            # Calculate basic arbitrage
            total_price = yes_price + no_price
            arbitrage_gap = abs(1.0 - total_price)
            
            # Skip if no significant arbitrage
            if arbitrage_gap < 0.01:  # Less than 1%
                return None
            
            # Analyze market title for keywords
            title_lower = title.lower()
            
            # Check macro signals alignment
            macro_verdict = macro_signals.get("verdict", "UNKNOWN")
            macro_bullish = macro_signals.get("bullish_count", 0)
            macro_total = macro_signals.get("total_count", 1)
            macro_score = macro_bullish / max(macro_total, 1)
            
            # Determine opportunity type
            opportunity_type = "NEUTRAL"
            opportunity_score = arbitrage_gap * 100  # Base score
            
            # Adjust based on macro signals
            if macro_verdict == "BUY" and macro_score > 0.6:
                opportunity_score *= 1.5
                opportunity_type = "BULLISH_ALIGNED"
            elif macro_verdict == "CASH" and macro_score < 0.4:
                opportunity_score *= 1.3
                opportunity_type = "BEARISH_ALIGNED"
            
            # Adjust based on volume (higher volume = more reliable)
            volume_factor = min(volume / 10000, 2.0)  # Cap at 2x
            opportunity_score *= (1 + volume_factor * 0.1)
            
            # Check for geopolitical keywords
            geo_keywords = ["war", "conflict", "election", "sanction", "crisis", "protest"]
            has_geo = any(keyword in title_lower for keyword in geo_keywords)
            
            if has_geo:
                # Geopolitical events are high-risk, high-reward
                opportunity_score *= 1.2
                opportunity_type = "GEOPOLITICAL"
            
            # Check for economic keywords
            econ_keywords = ["inflation", "gdp", "unemployment", "rate", "fed", "ecb"]
            has_econ = any(keyword in title_lower for keyword in econ_keywords)
            
            if has_econ:
                # Economic events align well with macro signals
                opportunity_score *= 1.1
                if opportunity_type == "NEUTRAL":
                    opportunity_type = "ECONOMIC"
            
            # Create opportunity dict
            opportunity = {
                "market_id": market_id,
                "market_title": title,
                "yes_price": yes_price,
                "no_price": no_price,
                "arbitrage_gap": arbitrage_gap,
                "arbitrage_percentage": arbitrage_gap * 100,
                "volume": volume,
                "opportunity_score": round(opportunity_score, 2),
                "opportunity_type": opportunity_type,
                "macro_alignment": macro_verdict,
                "macro_score": round(macro_score, 2),
                "analysis_timestamp": datetime.now().isoformat(),
                "recommended_action": self._get_recommended_action(opportunity_type, arbitrage_gap)
            }
            
            return opportunity
            
        except Exception as e:
            print(f"Error analyzing market {market.get('id', 'unknown')}: {e}")
            return None
    
    def _get_recommended_action(self, opportunity_type: str, arbitrage_gap: float) -> str:
        """Get recommended action based on opportunity type and gap"""
        if arbitrage_gap > 0.05:  # >5% arbitrage
            return "STRONG_BUY"
        elif arbitrage_gap > 0.02:  # >2% arbitrage
            if opportunity_type in ["BULLISH_ALIGNED", "GEOPOLITICAL"]:
                return "BUY"
            else:
                return "CONSIDER"
        else:
            return "MONITOR"
    
    def generate_daily_report(self, kalshi_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate daily report combining World Monitor signals and Kalshi opportunities
        
        Args:
            kalshi_data: Kalshi market data
            
        Returns:
            Comprehensive daily report
        """
        # Get all data
        macro_signals = self.get_macro_signals()
        market_radar = self.get_market_radar()
        opportunities = self.analyze_kalshi_arbitrage(kalshi_data)
        
        # Generate report
        report = {
            "report_date": datetime.now().isoformat(),
            "world_monitor_version": "2.5.20",
            "macro_overview": {
                "verdict": macro_signals.get("verdict", "UNKNOWN"),
                "bullish_signals": macro_signals.get("bullish_count", 0),
                "total_signals": macro_signals.get("total_count", 0),
                "bullish_percentage": round(
                    macro_signals.get("bullish_count", 0) / max(macro_signals.get("total_count", 1), 1) * 100, 1
                )
            },
            "market_conditions": market_radar.get("conditions", "UNKNOWN"),
            "kalshi_analysis": {
                "total_markets_analyzed": len(kalshi_data.get("markets", [])),
                "arbitrage_opportunities_found": len(opportunities),
                "top_opportunities": opportunities[:3]
            },
            "risk_assessment": {
                "overall_risk": "MEDIUM",
                "geopolitical_risk": self._assess_geopolitical_risk(),
                "market_risk": self._assess_market_risk(macro_signals),
                "recommended_position_size": "SMALL" if len(opportunities) > 0 else "NONE"
            },
            "detailed_opportunities": opportunities,
            "next_update_recommended": self._get_next_update_time()
        }
        
        return report
    
    def _assess_geopolitical_risk(self) -> str:
        """Assess geopolitical risk based on country instability"""
        # Check major economies
        countries = ["US", "CN", "RU", "EU", "GB"]
        scores = []
        
        for country in countries:
            data = self.get_country_instability_index(country)
            scores.append(data.get("instability_score", 0.5))
        
        avg_score = sum(scores) / len(scores)
        
        if avg_score > 0.7:
            return "HIGH"
        elif avg_score > 0.4:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _assess_market_risk(self, macro_signals: Dict[str, Any]) -> str:
        """Assess market risk based on macro signals"""
        verdict = macro_signals.get("verdict", "UNKNOWN")
        
        if verdict == "BUY":
            return "LOW"
        elif verdict == "CASH":
            return "HIGH"
        else:
            return "MEDIUM"
    
    def _get_next_update_time(self) -> str:
        """Get recommended next update time"""
        now = datetime.now()
        next_hour = now.replace(minute=0, second=0, microsecond=0)
        next_hour = next_hour.replace(hour=now.hour + 1)
        return next_hour.isoformat()


# Test function
def test_worldmonitor_integration():
    """Test World Monitor integration"""
    print("🧪 Testing World Monitor Integration")
    print("="*60)
    
    wm = WorldMonitorIntegration()
    
    # Test 1: Get macro signals
    print("\n1️⃣ Getting macro signals...")
    macro_signals = wm.get_macro_signals()
    print(f"   Verdict: {macro_signals.get('verdict', 'UNKNOWN')}")
    print(f"   Bullish: {macro_signals.get('bullish_count', 0)}/{macro_signals.get('total_count', 0)}")
    
    # Test 2: Get country data
    print("\n2️⃣ Getting US instability index...")
    us_data = wm.get_country_instability_index("US")
    print(f"   Score: {us_data.get('instability_score', 0)}")
    print(f"   Risk: {us_data.get('risk_level', 'UNKNOWN')}")
    
    # Test 3: Generate sample Kalshi analysis
    print("\n3️⃣ Testing Kalshi arbitrage analysis...")
    sample_kalshi_data = {
        "markets": [
            {
                "id": "market_1",
                "title": "Will the Fed raise rates in Q1 2026?",
                "yes_price": 0.45,
                "no_price": 0.50,
                "volume": 15000
            },
            {
                "id": "market_2", 
                "title": "Will there be a recession in 2026?",
                "yes_price": 0.30,
                "no_price": 0.65,
                "volume": 25000
            },
            {
                "id": "market_3",
                "title": "Will Bitcoin reach $100K in 2026?",
                "yes_price": 0.25,
                "no_price": 0.70,
                "volume": 50000
            }
        ]
    }
    
    opportunities = wm.analyze_kalshi_arbitrage(sample_kalshi_data)
    print(f"   Found {len(opportunities)} arbitrage opportunities")
    
    for i, opp in enumerate(opportunities[:2]):
        print(f"   {i+1}. {opp.get('market_title', 'Unknown')}")
        print(f"      Gap: {opp.get('arbitrage_percentage', 0):.1f}%")
        print