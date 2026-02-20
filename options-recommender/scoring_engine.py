#!/usr/bin/env python3
"""
Options Recommender - Scoring Engine
Scores stocks across 4 categories: Vol-Edge, Quality, Regime, Info-Edge
"""

import math
from typing import Dict, List, Optional
from dataclasses import dataclass
from api_clients import FinnhubClient, FredClient


@dataclass
class StockScores:
    """Scores for a single stock across all categories"""
    symbol: str
    vol_edge: float  # 0-100
    quality: float   # 0-100
    regime: float    # 0-100
    info_edge: float # 0-100
    total: float     # 0-400
    pass_gate: bool  # 3 of 4 > 50


class ScoringEngine:
    """
    Multi-factor scoring engine for options trade selection
    
    Categories:
    1. Vol-Edge: Are options overpriced vs actual moves?
    2. Quality: Is the company financially solid?
    3. Regime: Does it fit current macro environment?
    4. Info-Edge: Are signals converging?
    """
    
    def __init__(self):
        self.finnhub = FinnhubClient()
        self.fred = FredClient()
        
        # Cache macro indicators
        self._macro_cache = None
    
    def _get_macro_indicators(self) -> Dict:
        """Get current macro indicators from FRED"""
        if self._macro_cache is None:
            self._macro_cache = {
                'vix': self.fred.get_vix(),
                'cpi': self.fred.get_cpi(),
                'unemployment': self.fred.get_unemployment(),
                'fed_funds': self.fred.get_fed_funds_rate(),
                'treasury_10y': self.fred.get_10y_treasury(),
                'consumer_confidence': self.fred.get_consumer_confidence()
            }
        return self._macro_cache
    
    def classify_regime(self) -> str:
        """
        Classify current macro regime
        
        Returns:
            One of: 'goldilocks', 'overheating', 'contraction', 'recovery'
        """
        macro = self._get_macro_indicators()
        
        vix = macro.get('vix') or 20
        unemployment = macro.get('unemployment') or 5
        fed_funds = macro.get('fed_funds') or 5
        confidence = macro.get('consumer_confidence') or 100
        
        # Simple regime classification
        if vix < 20 and unemployment < 5 and fed_funds < 5:
            return 'goldilocks'  # Growth, low inflation, calm
        elif vix < 20 and fed_funds > 5:
            return 'overheating'  # Growth, high inflation
        elif vix > 25 or unemployment > 6:
            return 'contraction'  # Fear, weakness
        else:
            return 'recovery'  # Mixed signals
    
    def score_vol_edge(self, symbol: str, iv: float, hv: float, 
                       iv_rank: float = None, iv_percentile: float = None) -> float:
        """
        Score volatility edge (0-100)
        
        Higher score = options are overpriced = good for selling
        """
        score = 0
        
        # 1. IV vs HV ratio (most important)
        if hv > 0 and iv > 0:
            iv_hv_ratio = iv / hv
            
            if iv_hv_ratio > 1.5:  # Options 50%+ more expensive than realized
                score += 40
            elif iv_hv_ratio > 1.2:
                score += 30
            elif iv_hv_ratio > 1.0:
                score += 20
            elif iv_hv_ratio < 0.8:  # Options cheap = bad for selling
                score += 0
            else:
                score += 10
        
        # 2. IV Rank (where is IV vs 52-week range?)
        if iv_rank is not None:
            if iv_rank > 50:  # High IV relative to history
                score += 30
            elif iv_rank > 30:
                score += 20
            else:
                score += 10
        
        # 3. Term structure (are short-term options more expensive?)
        # Simplified: use IV percentile as proxy
        if iv_percentile is not None:
            if iv_percentile > 60:
                score += 20
            elif iv_percentile > 40:
                score += 15
            else:
                score += 10
        
        # 4. Technical volatility (ATR, Bollinger width)
        # Simplified: bonus for moderate HV
        if 15 <= hv <= 40:
            score += 10
        elif hv < 15 or hv > 60:
            score -= 5
        
        return max(0, min(100, score))
    
    def score_quality(self, symbol: str, financials: Dict) -> float:
        """
        Score company quality (0-100)
        
        Uses Piotroski F-Score style metrics
        """
        score = 0
        metrics = financials.get('metric', {})
        series = financials.get('series', {})
        
        # 1. Profitability (F-Score items)
        
        # Positive net income
        net_income = metrics.get('netIncomeTTM', 0)
        if net_income and net_income > 0:
            score += 10
        
        # Positive operating cash flow
        ocf = metrics.get('operatingCashFlowTTM', 0)
        if ocf and ocf > 0:
            score += 10
        
        # Positive ROA
        roa = metrics.get('roaTTM', 0)
        if roa and roa > 0:
            score += 8
        if roa and roa > 0.10:
            score += 5
        
        # 2. Leverage/Liquidity
        
        # Low debt
        debt_equity = metrics.get('totalDebtToEquity', 0)
        if debt_equity and debt_equity < 50:
            score += 10
        elif debt_equity and debt_equity < 100:
            score += 5
        
        # Current ratio > 1
        current_ratio = metrics.get('currentRatio', 0)
        if current_ratio and current_ratio > 1:
            score += 8
        if current_ratio and current_ratio > 2:
            score += 5
        
        # 3. Operating Efficiency
        
        # Positive gross margin
        gross_margin = metrics.get('grossMarginTTM', 0)
        if gross_margin and gross_margin > 0.30:
            score += 8
        
        # Operating margin
        op_margin = metrics.get('operatingMarginTTM', 0)
        if op_margin and op_margin > 0.15:
            score += 8
        
        # 4. Growth
        
        revenue_growth = metrics.get('revenueGrowthTTM', 0)
        if revenue_growth and revenue_growth > 0.10:
            score += 8
        if revenue_growth and revenue_growth > 0.20:
            score += 5
        
        # 5. Valuation sanity check
        
        pe = metrics.get('peBasicExclExtraTTM', 0)
        if pe and 0 < pe < 25:
            score += 5
        elif pe and pe < 40:
            score += 2
        
        return max(0, min(100, score))
    
    def score_regime(self, symbol: str, beta: float = 1.0, 
                     sector: str = None) -> float:
        """
        Score fit with current macro regime (0-100)
        """
        score = 50  # Start neutral
        
        regime = self.classify_regime()
        macro = self._get_macro_indicators()
        
        # Adjust based on regime and stock characteristics
        if regime == 'goldilocks':
            # Growth stocks, cyclical sectors favored
            if beta > 1.0:
                score += 15
            if sector in ['Technology', 'Consumer Discretionary']:
                score += 10
            elif sector in ['Utilities', 'Consumer Staples']:
                score -= 5
        
        elif regime == 'overheating':
            # Inflation beneficiaries, value stocks
            if beta < 1.0:
                score += 10
            if sector in ['Energy', 'Materials', 'Financials']:
                score += 15
            elif sector in ['Technology']:
                score -= 5
        
        elif regime == 'contraction':
            # Defensive stocks
            if beta < 0.8:
                score += 20
            if sector in ['Utilities', 'Healthcare', 'Consumer Staples']:
                score += 15
            elif sector in ['Technology', 'Consumer Discretionary']:
                score -= 10
        
        elif regime == 'recovery':
            # Early cycle
            if sector in ['Financials', 'Industrials', 'Materials']:
                score += 10
        
        # Apply correlation penalty (lower correlation = lower regime importance)
        # If beta is low, regime matters less
        if beta < 0.5:
            # Strong penalty - regime doesn't matter much
            regime_weight = 0.3  # 30% of normal weight
        elif beta < 0.8:
            regime_weight = 0.6
        elif beta < 1.2:
            regime_weight = 1.0
        else:
            regime_weight = 1.2
        
        # Adjust score toward 50 based on regime weight
        score = 50 + (score - 50) * regime_weight
        
        return max(0, min(100, score))
    
    def score_info_edge(self, symbol: str, 
                        recommendations: List[Dict] = None,
                        insider_txns: List[Dict] = None,
                        news_sentiment: Dict = None,
                        earnings_surprise: float = None) -> float:
        """
        Score information convergence (0-100)
        
        Higher = more bullish signals converging
        """
        score = 50  # Start neutral
        
        # 1. Analyst recommendations
        if recommendations:
            # Format: [{'buy': 10, 'hold': 5, 'sell': 2}, ...]
            latest = recommendations[0] if recommendations else {}
            total = latest.get('buy', 0) + latest.get('hold', 0) + latest.get('sell', 0)
            if total > 0:
                buy_pct = latest.get('buy', 0) / total
                sell_pct = latest.get('sell', 0) / total
                
                if buy_pct > 0.7:
                    score += 15
                elif buy_pct > 0.5:
                    score += 8
                elif sell_pct > 0.3:
                    score -= 15
                elif sell_pct > 0.15:
                    score -= 8
        
        # 2. Insider transactions
        if insider_txns:
            # Count buys vs sells
            buys = sum(1 for t in insider_txns if t.get('acquistionOrDisposition') == 'A')
            sells = sum(1 for t in insider_txns if t.get('acquistionOrDisposition') == 'D')
            
            if buys > sells * 2:
                score += 12
            elif buys > sells:
                score += 6
            elif sells > buys * 3:
                score -= 15
            elif sells > buys * 2:
                score -= 8
        
        # 3. News sentiment
        if news_sentiment:
            buzz = news_sentiment.get('buzz', {})
            sentiment = news_sentiment.get('sentiment', {})
            
            # Articles mentioning the stock
            articles = buzz.get('articlesInLastWeek', 0)
            if articles > 50:
                score += 5
            
            # Sentiment score (-1 to 1)
            bearish = sentiment.get('bearishPercent', 0.5)
            if bearish < 0.3:
                score += 10
            elif bearish > 0.7:
                score -= 10
        
        # 4. Earnings momentum
        if earnings_surprise is not None:
            if earnings_surprise > 0.10:  # Beat by 10%+
                score += 10
            elif earnings_surprise > 0:
                score += 5
            elif earnings_surprise < -0.10:
                score -= 15
            elif earnings_surprise < 0:
                score -= 5
        
        return max(0, min(100, score))
    
    def score_stock(self, symbol: str, 
                    iv: float, hv: float,
                    financials: Dict,
                    beta: float = 1.0,
                    sector: str = None,
                    iv_rank: float = None) -> StockScores:
        """
        Calculate all scores for a stock
        """
        # Get data for scoring
        recs = self.finnhub.get_recommendation_trends(symbol)
        insider = self.finnhub.get_insider_transactions(symbol).get('data', [])
        sentiment = self.finnhub.get_news_sentiment(symbol)
        
        # Calculate individual scores
        vol_edge = self.score_vol_edge(symbol, iv, hv, iv_rank)
        quality = self.score_quality(symbol, financials)
        regime = self.score_regime(symbol, beta, sector)
        info_edge = self.score_info_edge(symbol, recs, insider, sentiment)
        
        total = vol_edge + quality + regime + info_edge
        
        # Convergence gate: 3 of 4 must be > 50
        passing = sum(1 for s in [vol_edge, quality, regime, info_edge] if s > 50)
        pass_gate = passing >= 3
        
        return StockScores(
            symbol=symbol,
            vol_edge=vol_edge,
            quality=quality,
            regime=regime,
            info_edge=info_edge,
            total=total,
            pass_gate=pass_gate
        )


if __name__ == "__main__":
    print("Testing Scoring Engine...")
    
    engine = ScoringEngine()
    
    # Test regime classification
    regime = engine.classify_regime()
    print(f"\nCurrent regime: {regime}")
    
    # Get AAPL financials
    print("\nScoring AAPL...")
    financials = engine.finnhub.get_basic_financials('AAPL')
    
    # Simulated IV/HV for testing
    iv = 28.5
    hv = 22.3
    
    scores = engine.score_stock(
        symbol='AAPL',
        iv=iv,
        hv=hv,
        financials=financials,
        beta=1.2,
        sector='Technology'
    )
    
    print(f"\nAAPL Scores:")
    print(f"  Vol-Edge:  {scores.vol_edge:.1f}")
    print(f"  Quality:   {scores.quality:.1f}")
    print(f"  Regime:    {scores.regime:.1f}")
    print(f"  Info-Edge: {scores.info_edge:.1f}")
    print(f"  ──────────────────")
    print(f"  Total:     {scores.total:.1f}/400")
    print(f"  Pass Gate: {'✅' if scores.pass_gate else '❌'}")
    
    print("\n✅ Scoring engine working!")
