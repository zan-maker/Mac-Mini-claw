#!/usr/bin/env python3
"""
Working APIs Integration
Only includes APIs that are confirmed working with valid keys
"""

import os
import json
import time
from typing import Dict, Any, List
from datetime import datetime
import requests

class WorkingAPIsIntegration:
    """Integration with confirmed working APIs"""
    
    def __init__(self, cache_dir: str = None):
        self.cache_dir = cache_dir or "/Users/cubiczan/.openclaw/workspace/cache/working_apis"
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # CONFIRMED WORKING APIS
        self.apis = {
            "newsapi": {
                "key": "4eb2186b017a49c38d6f6ded502dd55b",
                "base_url": "https://newsapi.org/v2",
                "free_tier": 100,
                "cache_duration": 900  # 15 minutes
            },
            "alphavantage": {
                "key": "T0Z2YW467F7PNA9Z",
                "base_url": "https://www.alphavantage.co/query",
                "free_tier": 25,
                "cache_duration": 3600  # 1 hour
            },
            "tomba": {
                "key": "ta_hsrcgwy0fwj29bbxm0ar3dns0nc6e5p2151pg",
                "secret": "ts_576b466c-6d2a-4d3d-8730-6c6e9fe12958",
                "base_url": "https://api.tomba.io/v1",
                "free_tier": 50,  # When activated
                "cache_duration": 604800  # 1 week
            }
        }
        
        # Call statistics
        self.call_stats = self._load_call_stats()
    
    # ==================== NEWS API ====================
    
    def get_business_news(self, limit: int = 10) -> Dict[str, Any]:
        """Get latest business news"""
        cache_key = f"business_news_{limit}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        # Check cache
        cached = self._check_cache(cache_file, self.apis["newsapi"]["cache_duration"])
        if cached:
            return cached
        
        try:
            url = f"{self.apis['newsapi']['base_url']}/top-headlines"
            params = {
                "category": "business",
                "pageSize": limit,
                "country": "us",
                "apiKey": self.apis["newsapi"]["key"]
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                result = {
                    "success": True,
                    "category": "business",
                    "total_results": data.get("totalResults", 0),
                    "articles": data.get("articles", []),
                    "timestamp": datetime.now().isoformat(),
                    "source": "newsapi"
                }
                
                # Cache result
                self._save_cache(cache_file, result)
                self._update_call_stats("newsapi")
                
                return result
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def search_news(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search for news articles"""
        cache_key = f"news_search_{hash(query)}_{limit}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        # Check cache
        cached = self._check_cache(cache_file, self.apis["newsapi"]["cache_duration"])
        if cached:
            return cached
        
        try:
            url = f"{self.apis['newsapi']['base_url']}/everything"
            params = {
                "q": query,
                "pageSize": limit,
                "language": "en",
                "sortBy": "relevancy",
                "apiKey": self.apis["newsapi"]["key"]
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                result = {
                    "success": True,
                    "query": query,
                    "total_results": data.get("totalResults", 0),
                    "articles": data.get("articles", []),
                    "timestamp": datetime.now().isoformat(),
                    "source": "newsapi"
                }
                
                # Cache result
                self._save_cache(cache_file, result)
                self._update_call_stats("newsapi")
                
                return result
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_market_sentiment(self, tickers: List[str] = None) -> Dict[str, Any]:
        """Get news sentiment for specific tickers"""
        if not tickers:
            tickers = ["AAPL", "TSLA", "AMZN", "GOOGL", "MSFT"]
        
        all_articles = []
        
        for ticker in tickers:
            print(f"🔍 Getting news for {ticker}...")
            
            news_data = self.search_news(f"${ticker} OR {ticker} stock", limit=5)
            
            if news_data.get("success"):
                articles = news_data.get("articles", [])
                for article in articles:
                    article["related_ticker"] = ticker
                all_articles.extend(articles)
            
            # Respect rate limits
            time.sleep(1)
        
        # Analyze sentiment (simple keyword-based)
        sentiment_scores = {}
        for ticker in tickers:
            ticker_articles = [a for a in all_articles if a.get("related_ticker") == ticker]
            
            if ticker_articles:
                # Simple sentiment analysis
                positive_words = ["bullish", "gain", "rise", "up", "positive", "beat", "surge"]
                negative_words = ["bearish", "drop", "fall", "down", "negative", "miss", "plunge"]
                
                total_score = 0
                for article in ticker_articles:
                    title = article.get("title", "").lower()
                    description = article.get("description", "").lower()
                    text = f"{title} {description}"
                    
                    # Count positive/negative words
                    positive_count = sum(1 for word in positive_words if word in text)
                    negative_count = sum(1 for word in negative_words if word in text)
                    
                    article_score = positive_count - negative_count
                    total_score += article_score
                
                avg_score = total_score / len(ticker_articles)
                sentiment_scores[ticker] = {
                    "score": avg_score,
                    "articles_count": len(ticker_articles),
                    "sentiment": "bullish" if avg_score > 0.5 else "bearish" if avg_score < -0.5 else "neutral"
                }
        
        return {
            "success": True,
            "tickers": tickers,
            "total_articles": len(all_articles),
            "articles": all_articles[:20],  # Limit output
            "sentiment_scores": sentiment_scores,
            "timestamp": datetime.now().isoformat(),
            "source": "newsapi"
        }
    
    # ==================== STOCK DATA API ====================
    
    def get_stock_price(self, symbol: str) -> Dict[str, Any]:
        """Get current stock price"""
        cache_key = f"stock_{symbol}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        # Check cache
        cached = self._check_cache(cache_file, self.apis["alphavantage"]["cache_duration"])
        if cached:
            return cached
        
        try:
            url = self.apis["alphavantage"]["base_url"]
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": self.apis["alphavantage"]["key"]
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                quote = data.get("Global Quote", {})
                
                if quote:
                    result = {
                        "success": True,
                        "symbol": symbol,
                        "price": float(quote.get("05. price", 0)),
                        "change": float(quote.get("09. change", 0)),
                        "change_percent": quote.get("10. change percent", "0%"),
                        "volume": int(quote.get("06. volume", 0)),
                        "timestamp": datetime.now().isoformat(),
                        "source": "alphavantage"
                    }
                    
                    # Cache result
                    self._save_cache(cache_file, result)
                    self._update_call_stats("alphavantage")
                    
                    return result
                else:
                    return {
                        "success": False,
                        "error": "No quote data (might be rate limited)",
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_penny_stock_analysis(self, symbols: List[str] = None) -> Dict[str, Any]:
        """Analyze penny stocks (<$5)"""
        if not symbols:
            # Common penny stocks
            symbols = ["AMC", "BB", "NOK", "SNDL", "TLRY", "MVIS", "WKHS"]
        
        results = []
        
        for symbol in symbols:
            print(f"💰 Analyzing {symbol}...")
            
            stock_data = self.get_stock_price(symbol)
            
            if stock_data.get("success"):
                price = stock_data.get("price", 0)
                is_penny_stock = price < 5.0
                
                result = {
                    "symbol": symbol,
                    "price": price,
                    "is_penny_stock": is_penny_stock,
                    "change_percent": stock_data.get("change_percent", "0%"),
                    "volume": stock_data.get("volume", 0),
                    "analysis": self._analyze_penny_stock(symbol, price, stock_data.get("volume", 0))
                }
                results.append(result)
            
            # Respect rate limits
            time.sleep(1)
        
        # Sort by potential (higher volume + lower price = better penny stock)
        results.sort(key=lambda x: (x.get("volume", 0) / 1000000, -x.get("price", 0)), reverse=True)
        
        return {
            "success": True,
            "total_stocks": len(results),
            "penny_stocks": [r for r in results if r["is_penny_stock"]],
            "all_stocks": results,
            "timestamp": datetime.now().isoformat(),
            "source": "alphavantage"
        }
    
    def _analyze_penny_stock(self, symbol: str, price: float, volume: int) -> str:
        """Simple penny stock analysis"""
        if price < 1.0:
            price_category = "ultra-penny (<$1)"
        elif price < 3.0:
            price_category = "low-penny ($1-$3)"
        elif price < 5.0:
            price_category = "mid-penny ($3-$5)"
        else:
            price_category = "not a penny stock"
        
        if volume > 10000000:
            volume_category = "high volume (>10M)"
            liquidity = "excellent"
        elif volume > 1000000:
            volume_category = "good volume (1M-10M)"
            liquidity = "good"
        elif volume > 100000:
            volume_category = "moderate volume (100K-1M)"
            liquidity = "moderate"
        else:
            volume_category = "low volume (<100K)"
            liquidity = "poor"
        
        return f"{symbol} is a {price_category} stock with {volume_category}. Liquidity: {liquidity}."
    
    # ==================== TOMBA EMAIL API ====================
    
    def find_emails(self, domain: str, limit: int = 5) -> Dict[str, Any]:
        """Find emails for a domain using Tomba"""
        cache_key = f"tomba_emails_{domain}_{limit}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        # Check cache
        cached = self._check_cache(cache_file, self.apis["tomba"]["cache_duration"])
        if cached:
            return cached
        
        api_key = self.apis["tomba"]["key"]
        api_secret = self.apis["tomba"]["secret"]
        
        headers = {
            "X-Tomba-Key": api_key,
            "X-Tomba-Secret": api_secret,
            "Content-Type": "application/json",
            "User-Agent": "OpenClaw/1.0"
        }
        
        try:
            url = f"{self.apis['tomba']['base_url']}/domain-search"
            params = {"domain": domain}
            if limit:
                params["limit"] = limit
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                result = {
                    "success": True,
                    "domain": domain,
                    "total_emails": data.get("data", {}).get("total", 0),
                    "emails_found": len(data.get("data", {}).get("emails", [])),
                    "emails": data.get("data", {}).get("emails", []),
                    "timestamp": datetime.now().isoformat(),
                    "source": "tomba"
                }
                
                # Cache result
                self._save_cache(cache_file, result)
                self._update_call_stats("tomba")
                
                return result
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text[:100]}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def verify_email(self, email: str) -> Dict[str, Any]:
        """Verify email address using Tomba"""
        cache_key = f"tomba_verify_{hash(email)}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        # Check cache
        cached = self._check_cache(cache_file, self.apis["tomba"]["cache_duration"])
        if cached:
            return cached
        
        api_key = self.apis["tomba"]["key"]
        api_secret = self.apis["tomba"]["secret"]
        
        headers = {
            "X-Tomba-Key": api_key,
            "X-Tomba-Secret": api_secret,
            "Content-Type": "application/json",
            "User-Agent": "OpenClaw/1.0"
        }
        
        try:
            url = f"{self.apis['tomba']['base_url']}/email-verifier/{email}"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                result = {
                    "success": True,
                    "email": email,
                    "valid": data.get("data", {}).get("valid", False),
                    "mx_records": data.get("data", {}).get("mx_records", False),
                    "disposable": data.get("data", {}).get("disposable", False),
                    "score": data.get("data", {}).get("score", 0),
                    "timestamp": datetime.now().isoformat(),
                    "source": "tomba"
                }
                
                # Cache result
                self._save_cache(cache_file, result)
                self._update_call_stats("tomba")
                
                return result
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text[:100]}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_company_info(self, domain: str) -> Dict[str, Any]:
        """Get company information using Tomba"""
        cache_key = f"tomba_company_{domain}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        # Check cache
        cached = self._check_cache(cache_file, self.apis["tomba"]["cache_duration"])
        if cached:
            return cached
        
        api_key = self.apis["tomba"]["key"]
        api_secret = self.apis["tomba"]["secret"]
        
        headers = {
            "X-Tomba-Key": api_key,
            "X-Tomba-Secret": api_secret,
            "Content-Type": "application/json",
            "User-Agent": "OpenClaw/1.0"
        }
        
        try:
            url = f"{self.apis['tomba']['base_url']}/companies/find"
            params = {"domain": domain}
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                result = {
                    "success": True,
                    "domain": domain,
                    "company_name": data.get("data", {}).get("name", ""),
                    "industry": data.get("data", {}).get("industry", ""),
                    "employees": data.get("data", {}).get("employees", ""),
                    "location": data.get("data", {}).get("location", ""),
                    "twitter": data.get("data", {}).get("twitter", ""),
                    "linkedin": data.get("data", {}).get("linkedin", ""),
                    "timestamp": datetime.now().isoformat(),
                    "source": "tomba"
                }
                
                # Cache result
                self._save_cache(cache_file, result)
                self._update_call_stats("tomba")
                
                return result
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text[:100]}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    # ==================== AGENT INTEGRATION METHODS ====================
    
    def get_trade_recommendations(self) -> Dict[str, Any]:
        """Get trade recommendations combining news and stock data"""
        print("🎯 Generating trade recommendations...")
        
        # Step 1: Get market sentiment
        print("  1. Analyzing market sentiment...")
        sentiment_data = self.get_market_sentiment()
        
        # Step 2: Analyze penny stocks
        print("  2. Analyzing penny stocks...")
        penny_stock_data = self.get_penny_stock_analysis()
        
        # Step 3: Get business news for context
        print("  3. Getting business news context...")
        business_news = self.get_business_news(limit=5)
        
        # Combine recommendations
        recommendations = []
        
        # Add penny stock recommendations
        for stock in penny_stock_data.get("penny_stocks", [])[:3]:
            symbol = stock["symbol"]
            sentiment = sentiment_data.get("sentiment_scores", {}).get(symbol, {})
            
            recommendation = {
                "type": "penny_stock",
                "symbol": symbol,
                "price": stock["price"],
                "analysis": stock["analysis"],
                "news_sentiment": sentiment.get("sentiment", "unknown"),
                "sentiment_score": sentiment.get("score", 0),
                "reasoning": f"Penny stock with {stock['analysis'].split('Liquidity: ')[-1]}"
            }
            recommendations.append(recommendation)
        
        # Add news-based recommendations
        if business_news.get("success") and business_news.get("articles"):
            top_news = business_news["articles"][0]
            recommendation = {
                "type": "news_based",
                "symbol": "N/A",
                "price": "N/A",
                "analysis": "Market moving news detected",
                "news_headline": top_news.get("title", "")[:100],
                "news_source": top_news.get("source", {}).get("name", "unknown"),
                "reasoning": "Major business news that could impact markets"
            }
            recommendations.append(recommendation)
        
        return {
            "success": True,
            "total_recommendations": len(recommendations),
            "recommendations": recommendations,
            "market_sentiment": sentiment_data.get("sentiment_scores", {}),
            "business_news_count": business_news.get("total_results", 0),
            "timestamp": datetime.now().isoformat(),
            "source": "newsapi + alphavantage"
        }
    
    def get_lead_insights(self) -> Dict[str, Any]:
        """Get business insights for lead generation"""
        print("🔍 Generating lead insights...")
        
        # Get trending business news
        business_news = self.get_business_news(limit=10)
        
        # Extract potential lead topics
        lead_topics = []
        if business_news.get("success") and business_news.get("articles"):
            for article in business_news["articles"][:5]:
                title = article.get("title", "")
                description = article.get("description", "")
                
                # Extract potential business topics
                topics = self._extract_business_topics(f"{title} {description}")
                if topics:
                    lead_topics.append({
                        "headline": title[:100],
                        "topics": topics,
                        "source": article.get("source", {}).get("name", "unknown"),
                        "url": article.get("url", "")
                    })
        
        return {
            "success": True,
            "total_articles": business_news.get("total_results", 0),
            "lead_topics": lead_topics,
            "timestamp": datetime.now().isoformat(),
            "source": "newsapi",
            "suggested_actions": [
                "Use these topics for Reddit/Twitter lead searches",
                "Create content around trending business issues",
                "Target companies mentioned in news articles"
            ]
        }
    
    def _extract_business_topics(self, text: str) -> List[str]:
        """Extract business-related topics from text"""
        text_lower = text.lower()
        topics = []
        
        business_keywords = {
            "funding": ["funding", "investment", "venture capital", "series a", "series b"],
            "hiring": ["hiring", "recruiting", "job openings", "expanding team"],
            "expansion": ["expansion", "new office", "entering market", "global expansion"],
            "product": ["new product", "product launch", "beta release", "feature update"],
            "partnership": ["partnership", "collaboration", "joint venture", "strategic alliance"],
            "acquisition": ["acquisition", "merger", "buyout", "takeover"]
        }
        
        for topic, keywords in business_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    # ==================== CACHE & STATS METHODS ====================
    
    def _check_cache(self, cache_file: str, max_age_seconds: int) -> Dict[str, Any]:
        """Check cache and return data if fresh"""
        if not os.path.exists(cache_file):
            return None
        
        try:
            with open(cache_file, 'r') as f:
                cached = json.load(f)
            
            cache_time = datetime.fromisoformat(cached.get("timestamp", "2000-01-01"))
            age_seconds = (datetime.now() - cache_time).total_seconds()
            
            if age_seconds < max_age_seconds:
                cached["cached"] = True
                return cached
            
        except:
            pass
        
        return None
    
    def _save_cache(self, cache_file: str, data: Dict[str, Any]):
        """Save data to cache"""
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Cache save error: {e}")
    
    def _load_call_stats(self) -> Dict[str, Any]:
        """Load call statistics"""
        stats_file = os.path.join(self.cache_dir, "call_stats.json")
        
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r') as f:
                    stats = json.load(f)
                
                # Reset if not from today
                if stats.get("date") != datetime.now().strftime("%Y-%m-%d"):
                    stats = {"date": datetime.now().strftime("%Y-%m-%d")}
                
                return stats
            except:
                pass
        
        return {"date": datetime.now().strftime("%Y-%m-%d")}
    
    def _update_call_stats(self, api_name: str):
        """Update call statistics"""
        if api_name not in self.call_stats:
            self.call_stats[api_name] = 0
        
        self.call_stats[api_name] += 1
        
        # Save stats
        stats_file = os.path.join(self.cache_dir, "call_stats.json")
        try:
            with open(stats_file, 'w') as f:
                json.dump(self.call_stats, f, indent=2)
        except Exception as e:
            print(f"⚠️  Stats save error: {e}")
        
        # Check limits
        free_tier = self.apis.get(api_name, {}).get("free_tier", 0)
        if isinstance(free_tier, int) and free_tier > 0:
            calls = self.call_stats.get(api_name, 0)
            if calls >= free_tier * 0.8:  # 80% of limit
                print(f"⚠️  {api_name}: {calls}/{free_tier} calls used")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics"""
        return self.call_stats.copy()


# Test the integration
def test_working_apis():
    """Test working APIs integration"""
    print("🧪 Testing Working APIs Integration...")
    print("="*60)
    
    apis = WorkingAPIsIntegration()
    
    # Test 1: Business news
    print("\n📰 Testing business news...")
    news_data = apis.get_business_news(limit=3)
    print(f"   Success: {news_data.get('success', False)}")
    print(f"   Articles: {news_data.get('total_results', 0)}")
    
    if news_data.get("success") and news_data.get("articles"):
        for i, article in enumerate(news_data["articles"][:2]):
            print(f"   {i+1}. {article.get('title', 'No title')[:60]}...")
    
    # Test 2: Stock price
    print("\n💰 Testing stock price...")
    stock_data = apis.get_stock_price("AAPL")
    print(f"   Success: {stock_data.get('success', False)}")
    
    if stock_data.get("success"):
        print(f"   AAPL price: ${stock_data.get('price', 0):.2f}")
        print(f"   Change: {stock_data.get('change_percent', '0%')}")
    
    # Test 3: Penny stock analysis
    print("\n🎯 Testing penny stock analysis...")
    penny_data = apis.get_penny_stock_analysis(["AMC", "BB", "NOK"])
    print(f"   Success: {penny_data.get('success', False)}")
    print(f"   Penny stocks found: {len(penny_data.get('penny_stocks', []))}")
    
    if penny_data.get("success") and penny_data.get("penny_stocks"):
        for stock in penny_data["penny_stocks"][:3]:
            print(f"   • {stock['symbol']}: ${stock['price']:.2f} - {stock['analysis']}")
    
    # Test 4: Trade recommendations
    print("\n🚀 Testing trade recommendations...")
    recommendations = apis.get_trade_recommendations()
    print(f"   Success: {recommendations.get('success', False)}")
    print(f"   Recommendations: {recommendations.get('total_recommendations', 0)}")
    
    if recommendations.get("success") and recommendations.get("recommendations"):
        for i, rec in enumerate(recommendations["recommendations"][:2]):
            print(f"   {i+1}. {rec['type']}: {rec['symbol']} - {rec['reasoning'][:50]}...")
    
    # Test 5: Lead insights
    print("\n🔍 Testing lead insights...")
    insights = apis.get_lead_insights()
    print(f"   Success: {insights.get('success', False)}")
    print(f"   Lead topics: {len(insights.get('lead_topics', []))}")
    
    if insights.get("success") and insights.get("lead_topics"):
        for topic in insights["lead_topics"][:2]:
            print(f"   • {topic['headline'][:50]}...")
            print(f"     Topics: {', '.join(topic['topics'])}")
    
    # Show statistics
    print("\n📊 API usage:")
    stats = apis.get_stats()
    for api, calls in stats.items():
        if api != "date":
            free_tier = apis.apis.get(api, {}).get("free_tier", 0)
            if isinstance(free_tier, int) and free_tier > 0:
                print(f"   {api}: {calls}/{free_tier} calls")
            else:
                print(f"   {api}: {calls} calls")
    
    print("\n✅ Working APIs Integration Test Complete!")
    print("\n🎯 Ready for agent integration:")
    print("   • Trade Recommender: Real stock data + news sentiment")
    print("   • Lead Generator: Business news insights")
    print("   • ROI Analyst: Market data analysis")


if __name__ == "__main__":
    test_working_apis()