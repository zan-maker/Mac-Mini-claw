#!/usr/bin/env python3
"""
Enhanced Profit Scanner Core Class
Combines Pinchtab browser automation with API scanning
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.pinchtab_client import PinchtabClient, BrowserMode

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EnhancedProfitScanner:
    """Enhanced profit scanner with Pinchtab browser automation"""
    
    def __init__(self):
        self.pinchtab = PinchtabClient()
        self.scan_results = []
        
        # Load environment variables
        self.load_env()
        
        logger.info("Enhanced Profit Scanner initialized")
    
    def load_env(self):
        """Load environment variables from .env file"""
        env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        if line.startswith('export '):
                            line = line[7:]  # Remove 'export '
                        key, value = line.split('=', 1)
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        os.environ[key.strip()] = value.strip()
    
    def check_pinchtab_health(self) -> bool:
        """Check if Pinchtab is running and healthy"""
        try:
            if self.pinchtab.health_check():
                logger.info("✅ Pinchtab server is healthy")
                return True
            else:
                logger.error("❌ Pinchtab server not responding")
                return False
        except Exception as e:
            logger.error(f"Error checking Pinchtab health: {e}")
            return False
    
    def scan_with_pinchtab(self) -> List[Dict]:
        """Scan for opportunities using Pinchtab browser automation"""
        opportunities = []
        
        try:
            logger.info("Starting Pinchtab-based opportunity scan")
            
            # Create browser instance for scanning
            instance_id = self.pinchtab.create_instance(
                name="profit-scanner",
                mode=BrowserMode.HEADLESS
            )
            
            if not instance_id:
                logger.error("Failed to create browser instance")
                return opportunities
            
            # Scan multiple sources
            scan_sources = [
                ("AAA Gas Prices", "https://gasprices.aaa.com", self.scan_aaa_gas_prices),
                ("Reuters Iran News", "https://www.reuters.com/search/news?blob=Iran", self.scan_reuters_news),
                ("Bloomberg Markets", "https://www.bloomberg.com/markets", self.scan_bloomberg_markets),
            ]
            
            for source_name, source_url, scan_func in scan_sources:
                try:
                    logger.info(f"Scanning {source_name}...")
                    
                    # Open tab to source
                    tab_id = self.pinchtab.open_tab(instance_id, source_url, f"scan-{source_name}")
                    if not tab_id:
                        continue
                    
                    # Wait for page load
                    time.sleep(3)
                    
                    # Run scan function
                    result = scan_func(tab_id)
                    if result:
                        result["source"] = source_name
                        result["scan_time"] = datetime.now().isoformat()
                        opportunities.append(result)
                        logger.info(f"✅ Found {len(result.get('opportunities', []))} opportunities from {source_name}")
                    
                    # Close tab
                    self.pinchtab.close_tab(tab_id)
                    
                except Exception as e:
                    logger.error(f"Error scanning {source_name}: {e}")
            
            # Close instance
            self.pinchtab.close_instance(instance_id)
            
            logger.info(f"Pinchtab scan complete: {len(opportunities)} sources scanned")
            return opportunities
            
        except Exception as e:
            logger.error(f"Error in Pinchtab scan: {e}")
            return opportunities
    
    def scan_aaa_gas_prices(self, tab_id: str) -> Optional[Dict]:
        """Scan AAA gas prices website"""
        try:
            # Extract page text
            page_text = self.pinchtab.extract_text(tab_id)
            if not page_text:
                return None
            
            # Parse gas prices
            import re
            
            # Look for national average
            national_pattern = r'national average.*?\$(\d+\.\d{2})'
            national_match = re.search(national_pattern, page_text, re.IGNORECASE)
            
            # Look for state prices (NY)
            ny_pattern = r'New York.*?\$(\d+\.\d{2})'
            ny_match = re.search(ny_pattern, page_text, re.IGNORECASE)
            
            opportunities = []
            
            if national_match:
                national_price = float(national_match.group(1))
                opportunities.append({
                    "type": "gas_price",
                    "price": national_price,
                    "location": "national",
                    "target": 3.50,
                    "discrepancy": abs(3.50 - national_price),
                    "recommendation": "BUY YES" if national_price < 3.30 else "HOLD"
                })
            
            if ny_match:
                ny_price = float(ny_match.group(1))
                opportunities.append({
                    "type": "gas_price",
                    "price": ny_price,
                    "location": "New York",
                    "target": 3.50,
                    "discrepancy": abs(3.50 - ny_price),
                    "recommendation": "BUY YES" if ny_price < 3.30 else "HOLD"
                })
            
            return {
                "opportunities": opportunities,
                "summary": f"Found {len(opportunities)} gas price opportunities"
            }
            
        except Exception as e:
            logger.error(f"Error scanning AAA gas prices: {e}")
            return None
    
    def scan_reuters_news(self, tab_id: str) -> Optional[Dict]:
        """Scan Reuters for Iran conflict news"""
        try:
            # Extract page text
            page_text = self.pinchtab.extract_text(tab_id)
            if not page_text:
                return None
            
            # Analyze for Iran conflict keywords
            iran_keywords = [
                "Iran", "conflict", "attack", "missile", "Strait of Hormuz",
                "oil", "gas", "sanctions", "tensions", "escalation"
            ]
            
            keyword_counts = {}
            for keyword in iran_keywords:
                count = page_text.lower().count(keyword.lower())
                if count > 0:
                    keyword_counts[keyword] = count
            
            total_keywords = sum(keyword_counts.values())
            has_significant_news = total_keywords > 10
            
            opportunities = []
            
            if has_significant_news:
                opportunities.append({
                    "type": "news_catalyst",
                    "topic": "Iran conflict",
                    "intensity": total_keywords,
                    "keywords_found": list(keyword_counts.keys()),
                    "recommendation": "BULLISH for gas prices",
                    "confidence": min(100, total_keywords * 5)  # Scale confidence
                })
            
            return {
                "opportunities": opportunities,
                "summary": f"Found {len(opportunities)} news catalysts (total keywords: {total_keywords})"
            }
            
        except Exception as e:
            logger.error(f"Error scanning Reuters news: {e}")
            return None
    
    def scan_bloomberg_markets(self, tab_id: str) -> Optional[Dict]:
        """Scan Bloomberg markets page"""
        try:
            # Extract page text
            page_text = self.pinchtab.extract_text(tab_id)
            if not page_text:
                return None
            
            # Look for market indicators
            import re
            
            opportunities = []
            
            # Look for oil/gas mentions
            energy_patterns = [
                (r'oil.*?(\d+\.\d{2})', "oil_price"),
                (r'gas.*?(\d+\.\d{2})', "gas_price"),
                (r'crude.*?(\d+\.\d{2})', "crude_price"),
                (r'WTI.*?(\d+\.\d{2})', "wti_price"),
            ]
            
            for pattern, price_type in energy_patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                for match in matches[:2]:  # Take first 2 matches
                    try:
                        price = float(match)
                        opportunities.append({
                            "type": "market_price",
                            "price_type": price_type,
                            "price": price,
                            "source": "Bloomberg",
                            "timestamp": datetime.now().isoformat()
                        })
                    except ValueError:
                        continue
            
            # Look for market sentiment words
            bullish_words = ["gain", "rise", "up", "higher", "rally", "bullish"]
            bearish_words = ["drop", "fall", "down", "lower", "decline", "bearish"]
            
            bullish_count = sum(page_text.lower().count(word) for word in bullish_words)
            bearish_count = sum(page_text.lower().count(word) for word in bearish_words)
            
            sentiment = "neutral"
            if bullish_count > bearish_count + 5:
                sentiment = "bullish"
            elif bearish_count > bullish_count + 5:
                sentiment = "bearish"
            
            if sentiment != "neutral":
                opportunities.append({
                    "type": "market_sentiment",
                    "sentiment": sentiment,
                    "bullish_words": bullish_count,
                    "bearish_words": bearish_count,
                    "recommendation": "BUY YES" if sentiment == "bullish" else "BUY NO"
                })
            
            return {
                "opportunities": opportunities,
                "summary": f"Found {len(opportunities)} market indicators (sentiment: {sentiment})"
            }
            
        except Exception as e:
            logger.error(f"Error scanning Bloomberg markets: {e}")
            return None
    
    def combine_with_api_scan(self, pinchtab_results: List[Dict]) -> Dict:
        """Combine Pinchtab results with API-based scan results"""
        try:
            logger.info("Combining Pinchtab scan with API scan")
            
            # Import and run original API scan
            # Note: This assumes kalshi_profit_scanner_simple.py has a scan_kalshi_opportunities() function
            try:
                from scripts.kalshi_profit_scanner_simple import scan_kalshi_opportunities
                api_results = scan_kalshi_opportunities()
            except ImportError:
                logger.warning("API scanner not available, using Pinchtab results only")
                api_results = {"opportunities": []}
            
            # Combine results
            combined = {
                "timestamp": datetime.now().isoformat(),
                "scan_method": "hybrid_pinchtab_api",
                "pinchtab_sources": len(pinchtab_results),
                "api_opportunities": len(api_results.get("opportunities", [])),
                "combined_analysis": {}
            }
            
            # Extract key insights from Pinchtab
            pinchtab_insights = []
            for source in pinchtab_results:
                for opp in source.get("opportunities", []):
                    pinchtab_insights.append({
                        "type": opp.get("type"),
                        "source": source.get("source"),
                        "data": opp
                    })
            
            # Combine gas price data
            gas_prices = []
            for insight in pinchtab_insights:
                if insight["type"] == "gas_price":
                    gas_prices.append(insight["data"])
            
            if gas_prices:
                avg_gas_price = sum(p["price"] for p in gas_prices) / len(gas_prices)
                combined["combined_analysis"]["gas_price_analysis"] = {
                    "average_price": avg_gas_price,
                    "sources": len(gas_prices),
                    "target": 3.50,
                    "discrepancy": abs(3.50 - avg_gas_price),
                    "recommendation": "BUY YES" if avg_gas_price < 3.30 else "HOLD"
                }
            
            # Combine news analysis
            news_catalysts = [i for i in pinchtab_insights if i["type"] == "news_catalyst"]
            if news_catalysts:
                total_intensity = sum(c["data"].get("intensity", 0) for c in news_catalysts)
                combined["combined_analysis"]["news_analysis"] = {
                    "catalyst_count": len(news_catalysts),
                    "total_intensity": total_intensity,
                    "has_iran_news": any("Iran" in str(c["data"].get("keywords_found", [])) for c in news_catalysts),
                    "recommendation": "BULLISH" if total_intensity > 15 else "NEUTRAL"
                }
            
            # Add API opportunities
            combined["api_opportunities_list"] = api_results.get("opportunities", [])
            
            # Generate final recommendation
            final_score = 50
            
            # Factor 1: Gas price position
            gas_analysis = combined["combined_analysis"].get("gas_price_analysis", {})
            if gas_analysis:
                discrepancy = gas_analysis.get("discrepancy", 0)
                if discrepancy > 0.10:
                    final_score += 25
                elif discrepancy > 0.05:
                    final_score += 15
            
            # Factor 2: News intensity
            news_analysis = combined["combined_analysis"].get("news_analysis", {})
            if news_analysis:
                intensity = news_analysis.get("total_intensity", 0)
                if intensity > 20:
                    final_score += 30
                elif intensity > 10:
                    final_score += 15
            
            # Factor 3: Market sentiment
            market_sentiments = [i for i in pinchtab_insights if i["type"] == "market_sentiment"]
            if market_sentiments:
                bullish_count = sum(1 for m in market_sentiments if m["data"].get("sentiment") == "bullish")
                if bullish_count > 0:
                    final_score += 10
            
            # Cap score
            final_score = max(0, min(100, final_score))
            
            # Determine recommendation
            if final_score >= 70:
                recommendation = "STRONG BUY - Gas Month YES"
                position_size = "15-20"
            elif final_score >= 60:
                recommendation = "MODERATE BUY - Gas Month YES"
                position_size = "10-15"
            elif final_score >= 50:
                recommendation = "HOLD - Monitor closely"
                position_size = "0-5"
            else:
                recommendation = "REDUCE or BUY NO"
                position_size = "0"
            
            combined["final_recommendation"] = {
                "score": final_score,
                "recommendation": recommendation,
                "position_size": position_size,
                "confidence": f"{final_score}%",
                "reasoning": "Combined Pinchtab browser scan + API analysis"
            }
            
            logger.info(f"Combined analysis complete: score={final_score}, recommendation={recommendation}")
            return combined
            
        except Exception as e:
            logger.error(f"Error combining scans: {e}")
            return {"error": str(e)}
    
    def run_enhanced_scan(self) -> Dict:
        """Run enhanced scan with Pinchtab integration"""
        print("🎯 ENHANCED PROFIT SCANNER WITH PINCHTAB")
        print("=" * 60)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("")
        
        # Check Pinchtab health
        if not self.check_pinchtab_health():
            print("❌ Pinchtab not available, falling back to API-only scan")
            # Fall back to original scanner
            try:
                from scripts.kalshi_profit_scanner_simple import scan_kalshi_opportunities
                return scan_kalshi_opportunities()
            except ImportError:
                return {"error": "Neither Pinchtab nor API scanner available"}
        
        print("✅ Pinchtab integration active")
        print("")
        
        # Run Pinchtab scan
        print("🔍 Running Pinchtab browser scan...")
        pinchtab_results = self.scan_with_pinchtab()
        
        if not pinchtab_results:
            print("⚠️  Pinchtab scan returned no results")
            pinchtab_results = []
        
        print(f"✅ Pinchtab scan complete: {len(pinchtab_results)} sources")
        print("")
        
        # Combine with API scan
        print("🔄 Combining with API scan...")
        combined_results = self.combine_with_api_scan(pinchtab_results)
        
        if "error" in combined_results:
            print(f"❌ Error combining scans: {combined_results['error']}")
            return combined_results
        
        print("✅ Combined analysis complete")
        
        return combined_results